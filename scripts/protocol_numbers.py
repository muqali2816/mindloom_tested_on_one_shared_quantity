"""protocol_numbers.py (v3.1) -- every planning number in Supplementary Protocol S5 and Section 9.1 that is not
read directly from power_study1.csv / power_study2.csv / trials_budget.csv is derived here, from the outputs of
section9_power.py in the same directory (so the session arithmetic has one source: section9_power.py).

    python protocol_numbers.py --power-dir <dir with section9_power.py outputs> --out protocol_numbers.json

Contents of protocol_numbers.json
  study1 / study2 : session-level arithmetic copied from trials_budget.csv (presented, blocks, minutes, usable)
  power           : single-contrast power at the fixed N; Bonferroni and Holm (two contrasts, independence
                    approximation); the SUCCESS RULES stated in S5.12 under independence, each named:
                      rule_A_per_contrast_both_modalities   = P(EEG and PAS versions of ONE contrast both significant, Holm)
                      rule_B_both_contrasts_one_modality    = P(C0 and C1a both significant in one modality)  = 2ab - a^2
                      rule_C_both_contrasts_both_modalities = P(all four tests significant)
                    Independence is an approximation in every case; the dependence-corrected values come from the pilot.
  retention       : P(>= usable_target usable trials in a cell | independent loss at the planning rate); for the two
                    unpooled analysis cells of Study 1 and the nine cells of Study 2 jointly; the presented count per cell
                    that would give a 0.95 chance of reaching the floor. Illustrative: losses are not independent.
  study2          : single-contrast power and rule_A at the fixed Study 2 N (same rotation rule as Study 1).
Requires numpy, scipy, pandas.
"""
import argparse, json, math, os
import pandas as pd
from scipy import stats

__version__ = "3.1"


def paired_power(N, dz, alpha):
    df, nc, tc = N - 1, dz * math.sqrt(N), stats.t.ppf(1 - alpha / 2, N - 1)
    return float(stats.nct.sf(tc, df, nc) + stats.nct.cdf(-tc, df, nc))


def n_for(power, dz, alpha):
    n = 5
    while paired_power(n, dz, alpha) < power:
        n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--power-dir", default=".")
    ap.add_argument("--out", default="protocol_numbers.json")
    ap.add_argument("--dz", type=float, default=0.30)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--retention-target", type=float, default=0.95)
    a = ap.parse_args()

    tb = pd.read_csv(os.path.join(a.power_dir, "trials_budget.csv"))
    p1 = pd.read_csv(os.path.join(a.power_dir, "power_study1.csv"))
    key = json.load(open(os.path.join(a.power_dir, "section9_key_numbers.json")))
    b1 = tb[(tb.study == 1) & tb.cell_grouping.str.startswith("presentation cells")].iloc[0]
    b2 = tb[tb.study == 2].iloc[0]
    N = int(key["N_fixed_study1"]); N_req = int(key["N_required_dz030"])
    usable_target = int(b1.usable_target_per_cell); loss = float(b1.loss_rate); probe = float(b1.probe_fraction)

    def sess(row, s):
        return dict(presented_per_cell=int(row[f"presented_session{s}_per_cell"]), blocks=int(row[f"n_blocks_session{s}"]),
                    trials_per_block=int(row[f"block_trials_session{s}"]), probe_per_block=int(row[f"probe_per_block_session{s}"]),
                    presented_total=int(row[f"presented_session{s}_total"]), total_minutes=float(row[f"session{s}_minutes"]),
                    break_minutes=float(row["break_minutes"]) * (int(row[f"n_blocks_session{s}"]) - 1))
    out = {"version": __version__, "source": "section9_power.py v%s outputs (trials_budget.csv, power_study1.csv, power_study2.csv)" % tb.version.iloc[0]}
    out["study1"] = dict(session2=sess(b1, 2), session1=sess(b1, 1),
                         session2_probe_per_cell=int(b1.probe_trials_session2_per_cell), session2_noprobe_per_cell=int(b1.noprobe_trials_session2_per_cell),
                         usable_expected_per_cell=float(b1.usable_session2_per_cell_expected), usable_expected_pooled_3cells=round(3 * float(b1.usable_session2_per_cell_expected), 1),
                         session1_usable_per_cell_expected=float(b1.usable_session1_per_cell_expected),
                         presented_both_sessions=int(b1.presented_both_sessions_total))
    out["study2"] = dict(session2=sess(b2, 2), session1=sess(b2, 1), presented_both_sessions=int(b2.presented_both_sessions_total))

    # ---- multiplicity and success rules (two confirmatory contrasts, Holm; independence approximation)
    a1, ab = paired_power(N, a.dz, a.alpha), paired_power(N, a.dz, a.alpha / 2)
    holm = ab + (a1 - ab) * ab                       # P(a given true contrast rejected under Holm | other true, independent)
    out["power"] = dict(N_fixed=N, N_required=N_req, dz_plan=a.dz, single_alpha05=round(a1, 4), bonferroni_alpha025=round(ab, 4),
                        holm_independence_approx=round(holm, 4),
                        rule_A_per_contrast_both_modalities=round(holm ** 2, 4),
                        rule_B_both_contrasts_one_modality=round(2 * ab * a1 - ab ** 2, 4),
                        rule_C_both_contrasts_both_modalities=round((2 * ab * a1 - ab ** 2) ** 2, 4),
                        N_for_90_alpha025=n_for(0.90, a.dz, a.alpha / 2), N_for_90_rule_A=n_for(math.sqrt(0.90), a.dz, a.alpha / 2),
                        pas_sign_agreement_prob=round(float(stats.norm.cdf(a.dz * math.sqrt(N))), 4),
                        n_confirmatory_contrasts_study1=2,
                        note="independence between contrasts and between EEG and PAS versions is assumed; the pilot covariance replaces these values")
    N2 = int(p1.n_participants.iloc[0]) if False else int(math.ceil(N_req / int(key["rotations"])) * int(key["rotations"]))
    s2p = paired_power(N2, a.dz, a.alpha)
    out["study2_power"] = dict(N_fixed=N2, N_required=N_req, single_alpha05=round(s2p, 4), rule_A_both_modalities=round(s2p ** 2, 4))

    # ---- retention: the exclusion fires below the floor in ANY analysis cell, so the mean is not enough
    n_noprobe = int(b1.noprobe_trials_session2_per_cell)
    p_cell = float(1 - stats.binom.cdf(usable_target - 1, n_noprobe, 1 - loss))   # P(>= target usable | independent loss)
    need = n_noprobe
    while 1 - stats.binom.cdf(usable_target - 1, need, 1 - loss) < a.retention_target:
        need += 1
    out["retention"] = dict(model="independent Bernoulli loss at the planning rate; illustrative, losses are correlated in practice",
                            usable_target=usable_target, noprobe_per_cell=n_noprobe, loss_rate=loss,
                            P_cell_reaches_target=round(p_cell, 4),
                            P_two_unpooled_cells_study1=round(p_cell ** 2, 4), P_nine_cells_study2=round(p_cell ** 9, 4),
                            noprobe_per_cell_for_target_prob=need, presented_per_cell_for_target_prob=int(math.ceil(need / (1 - probe))),
                            rule="S5.8: a cell that ends session 2 below the floor is completed by one repeated block of that cell at the end of the session (pre-specified); participants still below the floor after the repeat are excluded and replaced")
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
