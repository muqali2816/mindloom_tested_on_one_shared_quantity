"""protocol_numbers.py (v3.3) -- every planning number in Supplementary Protocol S5 (v3) and Section 9.1 that is not read
directly from power_study1.csv / power_study2.csv / trials_budget*.csv is derived here, from the outputs of
section9_power.py (v2.4) in the same directory, so the session arithmetic has one source.

    python protocol_numbers.py --power-dir <dir with section9_power.py outputs> --out protocol_numbers.json

Contents of protocol_numbers.json
  study1 / study2 : session-level arithmetic copied from trials_budget.csv (cells, blocks, presented, minutes, ratings)
  cells           : per-analysis-cell budget (presentation cells pooled, blocks, usable session-2 trials, session-1 ratings)
  power           : the single confirmatory access-index contrast C1a at the fixed N (no multiplicity correction);
                    the two-version success rule (EEG-index AND PAS-report versions) under independence = p^2, and the N
                    that would give it 90 %; the report-based P16 test CR at its assumed dz; the pilot stop threshold.
  retention       : P(>= usable_target usable trials in a cell | independent loss at the planning rate) for a three-block
                    C1a cell and for a two-block count cell; jointly for the two single C1a cells; the two-block presented
                    count that would give 0.95.  Illustrative: losses are correlated within a session.
  block_orders    : the counterbalancing scheme for 16 blocks with unequal block counts (7-cell cyclic Latin square row,
                    the two extra C1a blocks at the session midpoint, the reversed row), written to block_orders_study1.csv
                    with the balance checks (each cell once in blocks 1-7 and once in 10-16; equal mean block position).
Requires numpy, scipy, pandas.
"""
import argparse, json, math, os
import pandas as pd
from scipy import stats

__version__ = "3.3"

# 7-cell Latin-square labels (must match section9_power.PRESENTATION_CELLS)
CELLS7 = ["count1@0", "count2@0", "count3@0", "count3@1_pairA", "count3@1_pairB", "count3@1_pairC", "count3@3"]
EXTRA = ["count3@0", "count3@3"]    # the two single-cell C1a cells: third block at the session midpoint


def paired_power(N, dz, alpha):
    df, nc, tc = N - 1, dz * math.sqrt(N), stats.t.ppf(1 - alpha / 2, N - 1)
    return float(stats.nct.sf(tc, df, nc) + stats.nct.cdf(-tc, df, nc))


def n_for(power, dz, alpha):
    n = 5
    while paired_power(n, dz, alpha) < power:
        n += 1
    return n


def p_reach(noprobe, target, loss):
    """P(>= target usable | independent Bernoulli retention 1 - loss over noprobe trials)."""
    return float(1 - stats.binom.cdf(target - 1, noprobe, 1 - loss))


def block_orders(n_sequences_note=True):
    """16-block sequences: cyclic 7x7 Latin square row r (blocks 1-7), the two extra C1a blocks (8-9, order alternating),
    the reversed row r (blocks 10-16).  7 rows x 2 extra-pair orders = 14 sequences; session 2 uses row (r + 1) mod 7 with the
    extra pair swapped.  Balance: every cell once in each outer half; mean block position 8.5 for every cell."""
    k = len(CELLS7)
    seqs = []
    for r in range(k):
        row = [CELLS7[(r + i) % k] for i in range(k)]
        for swap in (0, 1):
            extra = EXTRA[::-1] if swap else EXTRA
            seq = row + extra + row[::-1]
            seqs.append(dict(sequence_id=f"S{r + 1}{'b' if swap else 'a'}", latin_row=r + 1, extra_pair_order="-".join(extra),
                             session2_sequence_id=f"S{(r + 1) % k + 1}{'a' if swap else 'b'}", **{f"block_{i + 1:02d}": c for i, c in enumerate(seq)}))
    df = pd.DataFrame(seqs)
    # balance checks
    pos = {c: [] for c in CELLS7}
    first_half_ok = second_half_ok = True
    for _, s in df.iterrows():
        seq = [s[f"block_{i + 1:02d}"] for i in range(16)]
        for i, c in enumerate(seq):
            pos[c].append(i + 1)
        first_half_ok &= sorted(seq[:7]) == sorted(CELLS7); second_half_ok &= sorted(seq[9:]) == sorted(CELLS7)
    # consecutive same-cell blocks (occur when the Latin row ends in a C1a cell: its third block then follows its second across one break)
    n_adjacent = 0
    for _, s in df.iterrows():
        seq = [s[f"block_{i + 1:02d}"] for i in range(16)]
        n_adjacent += sum(seq[i] == seq[i + 1] for i in range(15))
    mean_pos = {c: round(sum(v) / len(v), 3) for c, v in pos.items()}
    blocks_per_cell = {c: len(v) // len(df) for c, v in pos.items()}
    return df, dict(n_sequences=len(df), latin_square="cyclic 7 x 7, row reversed in the second half", extra_blocks_at=[8, 9],
                    each_cell_once_in_blocks_1_7=bool(first_half_ok), each_cell_once_in_blocks_10_16=bool(second_half_ok),
                    mean_block_position_by_cell=mean_pos, blocks_per_cell_per_session=blocks_per_cell,
                    sequences_with_a_consecutive_same_cell_pair=int(sum(1 for _, s in df.iterrows() if any(s[f"block_{i + 1:02d}"] == s[f"block_{i + 2:02d}"] for i in range(15)))),
                    consecutive_same_cell_pairs_total=int(n_adjacent),
                    assignment_rule="sequence = participant index mod 14, lever rotation = participant index mod 6, both from lists fixed at preregistration; realised counts per sequence (8 or 9 at N = 120) are reported")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--power-dir", default=".")
    ap.add_argument("--out", default="protocol_numbers.json")
    ap.add_argument("--dz", type=float, default=0.30)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--retention-target", type=float, default=0.95)
    a = ap.parse_args()

    tb = pd.read_csv(os.path.join(a.power_dir, "trials_budget.csv"))
    an = pd.read_csv(os.path.join(a.power_dir, "trials_budget_analysis_cells.csv")).set_index("analysis_cell")
    key = json.load(open(os.path.join(a.power_dir, "section9_key_numbers.json")))
    b1 = tb[tb.study == 1].iloc[0]; b2 = tb[tb.study == 2].iloc[0]
    N = int(key["N_fixed_study1"]); N_req = int(key["N_required_dz030"])
    usable_target = int(b1.usable_target_per_cell); loss = float(b1.loss_rate); probe = float(b1.probe_fraction)

    def sess(row, s):
        d = dict(blocks=int(row.n_blocks_per_session), trials_per_block=int(row[f"block_trials_session{s}"]), probe_per_block=int(row[f"probe_per_block_session{s}"]),
                 presented_total=int(row[f"presented_session{s}_total"]), probe_total=int(row[f"probe_session{s}_total"]), noprobe_total=int(row[f"noprobe_session{s}_total"]),
                 titration_trials=int(row.titration_trials_per_session), titration_minutes=float(row[f"session{s}_titration_minutes"]),
                 trial_minutes=float(row[f"session{s}_trial_minutes"]), break_minutes=float(row[f"session{s}_break_minutes"]), total_minutes=float(row[f"session{s}_minutes"]))
        if s == 1:
            d.update(practice_trials=int(row.practice_trials_session1), practice_minutes=float(row.session1_practice_minutes), urge_ratings_total=int(row.urge_ratings_session1_total),
                     pas_rated_trials=int(row.noprobe_session1_total), report="PAS on no-probe trials (labels; PAS version), urge rating after the probe response on probe trials")
        else:
            d.update(report="none in blocks (no-report); PAS only in the titration phase")
        return d
    out = {"version": __version__, "source": "section9_power.py v%s outputs (trials_budget.csv, trials_budget_analysis_cells.csv, power_study1.csv, power_study2.csv, section9_key_numbers.json)" % tb.version.iloc[0]}
    out["study1"] = dict(n_presentation_cells=int(b1.n_presentation_cells), n_analysis_cells=int(b1.n_analysis_cells), n_blocks_per_session=int(b1.n_blocks_per_session),
                         blocks_per_cell=key["blocks_per_cell"], session2=sess(b1, 2), session1=sess(b1, 1),
                         two_block_cell=dict(presented_session2=int(b1.two_block_cell_presented_session2), probe=int(b1.two_block_cell_probe), noprobe=int(b1.two_block_cell_noprobe),
                                             usable_expected=float(b1.two_block_cell_usable_expected), raw_minimum=float(b1.two_block_cell_raw_min)),
                         usable_single_c1a_cell=float(an.loc["count3@0", "usable_session2_expected"]), usable_pooled_c1a_cell=float(an.loc["count3@1", "usable_session2_expected"]),
                         usable_count_cell=float(an.loc["count1@0", "usable_session2_expected"]),
                         precision_ratio_single_to_pooled=round(float(an.loc["count3@0", "usable_session2_expected"] / an.loc["count3@1", "usable_session2_expected"]), 3),
                         v2_precision_ratio_single_to_pooled=round(float(b1.two_block_cell_usable_expected) / (3 * float(b1.two_block_cell_usable_expected)), 3),
                         presented_both_sessions=int(b1.presented_both_sessions_total), v2_session2_minutes_22_blocks=key["v2_session2_minutes_22_blocks"])
    out["cells"] = {c: dict(presentation_cells_pooled=int(r.presentation_cells_pooled), blocks_per_session=int(r.blocks_per_session), presented_session2=int(r.presented_session2),
                            noprobe_session2=int(r.noprobe_session2), usable_session2_expected=float(r.usable_session2_expected), pas_rated_session1_expected=float(r.pas_rated_session1_expected),
                            urge_rated_session1=int(r.urge_rated_session1), role=r.role) for c, r in an.iterrows()}
    out["study2"] = dict(n_cells=int(b2.n_presentation_cells), n_blocks_per_session=int(b2.n_blocks_per_session), session2=sess(b2, 2), session1=sess(b2, 1), presented_both_sessions=int(b2.presented_both_sessions_total))

    # ---- power: one confirmatory access-index contrast; two-version rule; report-based P16 test
    p1 = paired_power(N, a.dz, a.alpha)
    rc = key["rating_contrast"]
    out["power"] = dict(N_fixed=N, N_required=N_req, dz_plan=a.dz, n_confirmatory_contrasts_access_index=1, multiplicity_correction="none (single confirmatory contrast)",
                        C1a_single_alpha05=round(p1, 4), mdes_at_N=key["mdes_at_N"],
                        two_version_rule_independence=round(p1 ** 2, 4), N_for_90_two_version_rule=n_for(math.sqrt(0.90), a.dz, a.alpha),
                        pas_sign_agreement_prob=round(float(stats.norm.cdf(a.dz * math.sqrt(N))), 4),
                        rating_contrast_CR=dict(hypothesis="P16 (stated) on its own outcome variable; register row P35", assumed_dz=rc["assumed_dz"], power_at_N=rc["power_at_N"], power_at_dz030=rc["power_at_dz030"],
                                                anchor=dict(source="Morsella et al. 2009, Emotion 9, t(13) = 6.21", dz=rc["anchor_dz"]), assumed_over_anchor=round(rc["assumed_dz"] / rc["anchor_dz"], 3),
                                                urge_ratings_per_cell_session1=key["urge_ratings_session1_per_c1a_cell"], own_family="yes: a separately preregistered test of a different hypothesis on a different variable; alpha 0.05, no correction across C1a and CR"),
                        pilot_stop=dict(criterion="pilot standardised urge difference, 3-shared minus 0-shared at count 3, session-1 probe trials", threshold_dz=key["pilot_stop_dz"],
                                        rule="below the threshold: intentions are not being formed -> stop and redesign", justification="equals the dz assumed for CR: below it the confirmatory rating test would not be warranted at the planned N; it is under a third of the anchor"),
                        note="independence between the EEG-index and PAS-report versions is assumed for the two-version figure; the pilot covariance replaces it")
    N2 = int(math.ceil(N_req / int(key["rotations"])) * int(key["rotations"]))
    s2p = paired_power(N2, a.dz, a.alpha)
    out["study2_power"] = dict(N_fixed=N2, N_required=N_req, single_alpha05=round(s2p, 4), two_version_rule_independence=round(s2p ** 2, 4))

    # ---- retention
    n3 = int(an.loc["count3@0", "noprobe_session2"]); n2b = int(an.loc["count1@0", "noprobe_session2"])
    p3, p2b = p_reach(n3, usable_target, loss), p_reach(n2b, usable_target, loss)
    from fractions import Fraction
    step = int(2 * Fraction(probe).limit_denominator(100).denominator)        # two-block cell: presented count step with integer probe trials per block (8)
    pres_feasible = int(b1.two_block_cell_presented_session2)
    while p_reach(int(round(pres_feasible * (1 - probe))), usable_target, loss) < a.retention_target:
        pres_feasible += step
    out["retention"] = dict(model="independent Bernoulli loss at the planning rate; illustrative, losses are correlated in practice", usable_target=usable_target, loss_rate=loss,
                            three_block_c1a_cell=dict(noprobe=n3, P_reaches_target=round(p3, 6), P_both_single_c1a_cells=round(p3 ** 2, 6)),
                            two_block_count_cell=dict(noprobe=n2b, P_reaches_target=round(p2b, 4), P_both_count_cells=round(p2b ** 2, 4),
                                                      presented_for_target_prob_feasible=pres_feasible, P_at_feasible=round(p_reach(int(round(pres_feasible * (1 - probe))), usable_target, loss), 4)),
                            v2_two_single_c1a_cells_at_two_blocks=round(p2b ** 2, 4),
                            rule="S5.9: the usable-trial floor is an exclusion criterion for the three C1a analysis cells; a count cell below the floor is completed by one repeated block at the end of session 2 (pre-specified) and, if still below, the participant is kept for C1a and flagged in the count estimate")
    # ---- block orders
    bo, checks = block_orders()
    bo.to_csv(os.path.join(os.path.dirname(os.path.abspath(a.out)), "block_orders_study1.csv"), index=False)
    out["block_orders"] = checks
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
