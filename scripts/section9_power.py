#!/usr/bin/env python
"""
section9_power.py (v2.1) -- a priori power for the worked condition of Section 9.1, NEW design
(Supplementary Protocol S5).  Every number is recomputed here; nothing from the previous
3 x 3 incompatibility x valence design (including its N = 126 / N = 68 / N = 119 values) is carried
forward.

Study 1 (neutral stimuli, three effectors)
------------------------------------------
Three responses on three effectors (e.g. left hand / right hand / foot), all co-executable.
  incompatibility = number of response PAIRS that share an effector: 0 / 1 / 3
       (three responses on three distinct effectors -> 0 shared pairs; two on one effector -> 1;
        all three on one effector -> 3; with three responses, 2 shared pairs is impossible)
  count branch    = 1 / 2 / 3 co-executable responses at 0 shared pairs
Analysis cells (5): count1@0, count2@0, count3@0, count3@1, count3@3.
Presentation cells (11, effector-balanced): count 1 on each of 3 effectors (3), count 2 on each of
3 effector pairs (3), count 3 on three distinct effectors (1), count 3 with each effector doubled (3),
count 3 all on the designated effector (1).  The per-cell trial budget is given for both groupings.

Contrasts (per-participant scores on the cell means of the report-independent access index):
  C0   threshold, count 1 vs >= 2 at 0 shared pairs (P16, a trigger and not a monotonic count effect):
       w = (-1, +1/2, +1/2) over (count 1, 2, 3).
       Companion equivalence test for the 'not monotonic' half of P16: count 3 - count 2, TOST with
       bound +/- delta (in dz units), true effect 0 under P16.
  C1a  compatible vs incompatible pairs at count = 3 (P23, author-derived): w = (-1, +1/2, +1/2) over
       (0, 1, 3 shared pairs).
  C1b  0 / 1 / 3 shared pairs with UNEQUAL steps.  The manipulated quantity is the number of shared
       pairs, whose steps are 0 -> 1 -> 3; the classical weights (-1, 0, +1) encode ordinal position and
       would treat 1 -> 3 as the same step as 0 -> 1.  Two options are reported:
         (i)  linear-in-shared-pairs contrast: centred weights x - mean(x) = (-4/3, -1/3, +5/3), i.e.
              (-4, -1, +5) up to scale -- a one-df test whose dz is defined on that score;
         (ii) two-df omnibus (Hotelling T^2 on two orthogonal within-participant contrasts, exact
              F(2, N-2)); the noncentrality is calibrated so that the whole effect lies on one
              standardised contrast direction with the same dz (the conservative allocation).

Power
-----
Paired t on per-participant contrast scores: exact noncentral-t power, alpha = 0.05 two-sided.
TOST: exact power by numerical integration over the sample SD (the two one-sided tests share s, so
their joint rejection region is |mean| < delta - t_crit * s / sqrt(N)), checked by Monte Carlo.
Mixed model: trial-level simulation (participant random intercept + random slope on the contrast
code, Wald z), calibrated so the participant-level dz equals the analytic planning value at the
usable trials per cell -- a CONVERGENCE CHECK on the analytic value, not an independent estimate.
Requires statsmodels for that mode only.

Fixed N: the smallest N with >= 90 % power at dz = 0.30 for C0 and for C1a (identical by
construction since both are paired t at the same dz); dz = 0.20 and 0.40 also reported.  No
sequential Bayes-factor monitoring.

Trials (v2.1, audit section 4): the no-report access estimate comes from SESSION 2 ONLY; session 1
collects a PAS rating on every trial and trains the classifier, so its trials are not no-report
trials.  The budget is therefore computed for session 2 alone: 25 % of presented trials are probe
trials (they carry a report probe and are not part of the no-report dependent variable), 15 %
expected loss (artefact / exclusions); target >= 64 usable trials per ANALYSIS cell from session 2.
presented_session2_per_cell is the smallest integer with exactly one quarter probe trials whose
no-probe trials survive the loss rate at >= 64 (104 = 26 probe + 78 no-probe; 78 x 0.85 = 66.3).
Session 1 presents the same number per cell (equal sessions, planning choice; --session1-per-cell
overrides).  Session duration = trials x --trial-seconds (default 6 s) + (blocks - 1) breaks of
--break-minutes (default 2 min) with --block-trials (default 104) trials per block.  Analysis cells
that pool three presentation cells receive three times the per-presentation-cell count.  The
mixed-model check stays calibrated at the 64-usable-trials floor (USABLE_TARGET), not at the
expected 66.3, and says so in its output.

Study 2 (valence; Supplementary only)
-------------------------------------
Main effect negative - positive at matched arousal (neutral is lower in arousal by construction):
dz = 0.30 -> N (also 0.20, 0.40).  The incompatibility x valence interaction is reported as
estimation only: the N that WOULD be needed at dz = 0.20 is given so that the reader sees it is out
of reach; its power at the Study 2 N is also reported.

Usage
-----
  python section9_power.py [--out DIR] [--mixed-sims 200 | --skip-mixed] [--mc 200000] [--seed 20260924]
Outputs: power_study1.csv, power_study2.csv, trials_budget.csv, power_mixed_check.csv,
         section9_power_summary.md (all numbers in prose are read from the tables).
"""
from __future__ import annotations
import argparse, json, math, os, sys, time, warnings
import numpy as np
import pandas as pd
from scipy import stats, integrate, optimize

__version__ = "2.1"
ALPHA, TARGET_POWER = 0.05, 0.90
DZ_PLAN, DZ_ALT = 0.30, (0.20, 0.40)
TOST_BOUNDS = (0.20, 0.30, 0.40)
USABLE_TARGET, PROBE_FRAC, LOSS_RATE, N_SESSIONS = 64, 0.25, 0.15, 2
TRIAL_SECONDS, BLOCK_TRIALS, BREAK_MINUTES = 6.0, 104, 2.0    # planning values for session duration (v2.1); CLI-adjustable
# analysis cell -> number of effector-balanced presentation cells pooled into it (sums to CELLS_STUDY1_PRESENTATION = 11)
ANALYSIS_CELL_POOLING = {"count1@0": 3, "count2@0": 3, "count3@0": 1, "count3@1": 3, "count3@3": 1}
CELLS_STUDY1_ANALYSIS, CELLS_STUDY1_PRESENTATION = 5, 11
CELLS_STUDY2 = 9   # 3 incompatibility levels (0/1/3 shared pairs at count 3) x 3 valence (negative, neutral, positive); assumption, see summary
SHARED_PAIRS = np.array([0.0, 1.0, 3.0])
W_C0 = np.array([-1.0, 0.5, 0.5])                      # count 1 vs mean(count 2, count 3)
W_C1A = np.array([-1.0, 0.5, 0.5])                     # 0 shared vs mean(1, 3 shared)
W_C1B_LIN = SHARED_PAIRS - SHARED_PAIRS.mean()         # (-4/3, -1/3, 5/3): linear in the number of shared pairs
W_C1B_ORDINAL = np.array([-1.0, 0.0, 1.0])             # reported only to show what it assumes
W_EQUIV = np.array([0.0, -1.0, 1.0])                   # count 3 - count 2 (TOST)


# ---------------------------------------------------------------- paired t
def power_paired_t(n, dz, alpha=ALPHA):
    """Exact power of the two-sided one-sample (paired) t test, noncentral t."""
    df = n - 1
    tc = stats.t.ppf(1 - alpha / 2, df)
    nc = dz * math.sqrt(n)
    up, lo = stats.nct.sf(tc, df, nc), stats.nct.cdf(-tc, df, nc)
    # scipy's nct returns NaN for very large noncentrality; power is then indistinguishable from 1
    return float(np.nan_to_num(up, nan=1.0) + np.nan_to_num(lo, nan=0.0))


def n_for_power(dz, power=TARGET_POWER, alpha=ALPHA, n_min=4, n_max=5000):
    n = n_min
    while power_paired_t(n, dz, alpha) < power:
        n += 1
        if n > n_max:
            return np.nan
    return n


def mdes(n, power=TARGET_POWER, alpha=ALPHA):
    """Minimum detectable dz at N for the target power."""
    return float(optimize.brentq(lambda d: power_paired_t(n, d, alpha) - power, 1e-4, 1.0))


# ---------------------------------------------------------------- TOST, exact
def power_tost_exact(n, delta, mu=0.0, alpha=ALPHA):
    """Exact power of the paired TOST (two one-sided t tests at level alpha each) for equivalence
    bounds +/- delta (in SD units of the paired difference), true standardised effect mu.
    Both tests use the same sample SD s.  With sigma = 1:  mean ~ N(mu, 1/n),  s*sqrt(n-1) ~ chi(n-1).
    Joint rejection: -delta + tc*s/sqrt(n) < mean < delta - tc*s/sqrt(n), which requires s < delta*sqrt(n)/tc.
    Power = int_0^{s_max} [Phi(sqrt(n)(delta - tc s/sqrt(n) - mu)) - Phi(sqrt(n)(-delta + tc s/sqrt(n) - mu))] f_s(s) ds."""
    df = n - 1
    tc = stats.t.ppf(1 - alpha, df)
    s_max = delta * math.sqrt(n) / tc
    sq = math.sqrt(n)

    def integrand(s):
        hi = delta - tc * s / sq
        p = stats.norm.cdf(sq * (hi - mu)) - stats.norm.cdf(sq * (-hi - mu))
        # density of s = chi_{df} / sqrt(df)
        return max(p, 0.0) * stats.chi.pdf(s * math.sqrt(df), df) * math.sqrt(df)
    val, err = integrate.quad(integrand, 0.0, s_max, limit=200)
    return float(val)


def power_tost_mc(n, delta, mu=0.0, alpha=ALPHA, n_sim=200_000, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.normal(mu, 1.0, (n_sim, n))
    m = x.mean(1); s = x.std(1, ddof=1)
    tc = stats.t.ppf(1 - alpha, n - 1)
    t_lo = (m + delta) / (s / math.sqrt(n)); t_hi = (m - delta) / (s / math.sqrt(n))
    rej = (t_lo > tc) & (t_hi < -tc)
    p = rej.mean()
    return float(p), float(math.sqrt(p * (1 - p) / n_sim))


def n_for_tost(delta, power=TARGET_POWER, mu=0.0, alpha=ALPHA, n_max=5000):
    n = 4
    while power_tost_exact(n, delta, mu, alpha) < power:
        n += 1
        if n > n_max:
            return np.nan
    return n


# ---------------------------------------------------------------- two-df omnibus
def power_omnibus_2df(n, dz, alpha=ALPHA):
    """Hotelling T^2 on two orthogonal within-participant contrasts (3 levels): exact F(2, n-2) with
    noncentrality n * delta^2, delta^2 = dz^2 when the whole effect lies on one standardised contrast."""
    df1, df2 = 2, n - 2
    fc = stats.f.ppf(1 - alpha, df1, df2)
    return float(stats.ncf.sf(fc, df1, df2, n * dz ** 2))


def n_for_omnibus(dz, power=TARGET_POWER, alpha=ALPHA):
    n = 5
    while power_omnibus_2df(n, dz, alpha) < power:
        n += 1
    return n


# ---------------------------------------------------------------- mixed-model convergence check
def mixed_check(n_sub, dz, n_trials, w, n_sims, seed, beta_trial=0.10, sigma_e=1.0):
    """Trial-level simulation for one contrast with weights w over K cells.  Cell code c_k = w_k / sum(w_k^2)
    so that the per-participant contrast score sum_k w_k * mean_k estimates the participant's slope b_i.
    b_i ~ N(beta, sd_b^2); sd_b chosen so that dz = beta / sqrt(sd_b^2 + sigma_e^2 sum(w^2)/n_trials).
    Fits (a) participant-level paired t on contrast scores (the analytic route) and (b) a linear mixed model
    y ~ c with random intercept and random slope, Wald z on c.  Returns power estimates and the count of
    non-converged fits."""
    import statsmodels.formula.api as smf
    rng = np.random.default_rng(seed)
    w = np.asarray(w, float); K = len(w); sw2 = float((w ** 2).sum())
    c = w / sw2
    var_meas = sigma_e ** 2 * sw2 / n_trials
    var_total = (beta_trial / dz) ** 2
    if var_total <= var_meas:
        raise ValueError("dz not reachable at this trial count with beta_trial; raise beta_trial or trials")
    sd_b = math.sqrt(var_total - var_meas)
    hits_t = hits_mixed = nonconv = 0
    for _ in range(n_sims):
        b = rng.normal(beta_trial, sd_b, n_sub); u = rng.normal(0, 0.5, n_sub)
        mu = u[:, None] + b[:, None] * c[None, :]                                   # (sub, K)
        y = np.repeat(mu[:, :, None], n_trials, axis=2) + rng.normal(0, sigma_e, (n_sub, K, n_trials))
        cell_mean = y.mean(2)
        score = (cell_mean * w[None, :]).sum(1)
        t, p = stats.ttest_1samp(score, 0.0); hits_t += p < ALPHA
        df = pd.DataFrame({"y": y.reshape(-1), "c": np.repeat(np.tile(c, n_sub), n_trials), "subj": np.repeat(np.arange(n_sub), K * n_trials)})
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            m = smf.mixedlm("y ~ c", df, groups=df["subj"], re_formula="~ c").fit(method="lbfgs", reml=True, maxiter=200)
        if not getattr(m, "converged", True):
            nonconv += 1
        hits_mixed += abs(m.tvalues["c"]) > stats.norm.ppf(1 - ALPHA / 2)
    return dict(power_two_stage=hits_t / n_sims, power_mixed=hits_mixed / n_sims, n_nonconverged=nonconv, sd_slope=sd_b, beta_trial=beta_trial)


# ---------------------------------------------------------------- trials budget
def presented_per_cell(usable=USABLE_TARGET, probe=PROBE_FRAC, loss=LOSS_RATE, sessions=N_SESSIONS):
    """v2.0 rule (both sessions pooled) -- kept for reference only; it over-counted usable no-report trials by a factor of two."""
    raw = usable / ((1 - probe) * (1 - loss))
    n = math.ceil(raw)
    n += (-n) % sessions           # multiple of the session count so cells split evenly
    return n, raw


def presented_session2_per_cell(usable=USABLE_TARGET, probe=PROBE_FRAC, loss=LOSS_RATE):
    """Smallest integer n such that exactly a fraction `probe` of n are probe trials (n divisible by the probe denominator)
    and the remaining no-probe trials survive the loss rate with expectation >= usable:  n (1 - probe)(1 - loss) >= usable.
    Returns (n, n_probe, n_noprobe, expected_usable, raw_minimum)."""
    from fractions import Fraction
    step = Fraction(probe).limit_denominator(100).denominator      # 0.25 -> 4
    raw = usable / ((1 - probe) * (1 - loss))
    n = math.ceil(raw); n += (-n) % step
    n_probe = round(n * probe); n_noprobe = n - n_probe
    exp_usable = n_noprobe * (1 - loss)
    assert exp_usable >= usable and n_probe == n * probe, (n, n_probe, exp_usable)
    return n, n_probe, n_noprobe, exp_usable, raw


def session_minutes(n_trials, trial_seconds=TRIAL_SECONDS, block_trials=BLOCK_TRIALS, break_minutes=BREAK_MINUTES):
    n_blocks = math.ceil(n_trials / block_trials)
    breaks = max(n_blocks - 1, 0) * break_minutes
    return n_trials * trial_seconds / 60.0 + breaks, n_blocks, breaks


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=".")
    ap.add_argument("--mixed-sims", type=int, default=200)
    ap.add_argument("--skip-mixed", action="store_true")
    ap.add_argument("--mc", type=int, default=200_000, help="Monte Carlo replicates for the TOST check")
    ap.add_argument("--seed", type=int, default=20260924)
    ap.add_argument("--trial-seconds", type=float, default=TRIAL_SECONDS); ap.add_argument("--block-trials", type=int, default=BLOCK_TRIALS)
    ap.add_argument("--break-minutes", type=float, default=BREAK_MINUTES)
    ap.add_argument("--session1-per-cell", type=int, default=None, help="presented trials per presentation cell in session 1 (default: equal to session 2)")
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    dzs = sorted({DZ_PLAN, *DZ_ALT})

    # ---- Study 1: N for the two confirmatory contrasts
    rows = []
    for contrast, w, hyp in [("C0_threshold_count1_vs_ge2", W_C0, "P16 (stated, SIT)"), ("C1a_compatible_vs_incompatible_at_count3", W_C1A, "P23 (author-derived)")]:
        for dz in dzs:
            for pw in (0.80, 0.90):
                n = n_for_power(dz, pw)
                rows.append(dict(study=1, contrast=contrast, hypothesis=hyp, weights=str(w.tolist()), test="paired t, two-sided", dz=dz, target_power=pw,
                                 n_participants=n, achieved_power=round(power_paired_t(n, dz), 4), role="confirmatory" if (dz == DZ_PLAN and pw == TARGET_POWER) else "sensitivity"))
    N_REQUIRED = n_for_power(DZ_PLAN, TARGET_POWER)            # smallest N reaching the target (119 at dz 0.30)
    ROTATIONS = 6                                              # rule-to-effector assignments rotated across participants
    N_FIXED = int(math.ceil(N_REQUIRED / ROTATIONS) * ROTATIONS) # rounded UP to a multiple of the rotation count (120); power can only rise
    # C1b: linear-in-shared-pairs (one df) and the omnibus (two df)
    for dz in dzs:
        n1 = n_for_power(dz, TARGET_POWER); n2 = n_for_omnibus(dz, TARGET_POWER)
        rows.append(dict(study=1, contrast="C1b_linear_in_shared_pairs", hypothesis="exploratory (0/1/3 shared pairs)", weights=str(np.round(W_C1B_LIN, 4).tolist()),
                         test="paired t on the centred shared-pairs score", dz=dz, target_power=TARGET_POWER, n_participants=n1, achieved_power=round(power_paired_t(n1, dz), 4), role="exploratory"))
        rows.append(dict(study=1, contrast="C1b_omnibus_2df", hypothesis="exploratory (0/1/3 shared pairs)", weights="two orthogonal contrasts",
                         test="Hotelling T^2, F(2, N-2), effect on one direction", dz=dz, target_power=TARGET_POWER, n_participants=n2, achieved_power=round(power_omnibus_2df(n2, dz), 4), role="exploratory"))
    # what the fixed N buys for each contrast
    for contrast, dz in [("C0_threshold_count1_vs_ge2", DZ_PLAN), ("C1a_compatible_vs_incompatible_at_count3", DZ_PLAN)] + [("C1b_linear_in_shared_pairs", d) for d in dzs] + [("C1b_omnibus_2df", d) for d in dzs]:
        pw = power_omnibus_2df(N_FIXED, dz) if contrast.endswith("2df") else power_paired_t(N_FIXED, dz)
        rows.append(dict(study=1, contrast=contrast, hypothesis="power at the fixed N", weights="", test="", dz=dz, target_power=np.nan, n_participants=N_FIXED, achieved_power=round(pw, 4), role="at_fixed_N"))
    rows.append(dict(study=1, contrast="any_paired_contrast", hypothesis="minimum detectable dz at the fixed N", weights="", test="paired t", dz=round(mdes(N_FIXED), 4), target_power=TARGET_POWER, n_participants=N_FIXED, achieved_power=TARGET_POWER, role="MDES"))
    # TOST for the equivalence half of P16 (count 3 vs count 2)
    tost_rows = []
    for delta in TOST_BOUNDS:
        p_an = power_tost_exact(N_FIXED, delta)
        p_mc, se_mc = power_tost_mc(N_FIXED, delta, n_sim=a.mc, seed=a.seed)
        n_t = n_for_tost(delta)
        tost_rows.append(dict(study=1, contrast="C0_equivalence_count3_vs_count2", hypothesis="P16: no further increase beyond the trigger (true effect 0)", weights=str(W_EQUIV.tolist()),
                              test=f"TOST, bounds +/-{delta} dz, alpha {ALPHA} each side", dz=delta, target_power=TARGET_POWER, n_participants=N_FIXED,
                              achieved_power=round(p_an, 4), role="equivalence_at_fixed_N", tost_power_mc=round(p_mc, 4), tost_mc_se=round(se_mc, 5), n_for_90pct_tost=n_t))
    s1 = pd.DataFrame(rows + tost_rows)
    s1.insert(0, "version", __version__)
    s1.to_csv(os.path.join(a.out, "power_study1.csv"), index=False)

    # ---- Study 2 (valence, Supplementary)
    rows2 = []
    for dz in dzs:
        for pw in (0.80, 0.90):
            n = n_for_power(dz, pw)
            rows2.append(dict(study=2, contrast="valence_main_negative_minus_positive_matched_arousal", test="paired t, two-sided", dz=dz, target_power=pw, n_participants=n,
                              achieved_power=round(power_paired_t(n, dz), 4), role="confirmatory" if (dz == DZ_PLAN and pw == TARGET_POWER) else "sensitivity"))
    N2 = n_for_power(DZ_PLAN, TARGET_POWER)
    for dz in (0.20, 0.30):
        n = n_for_power(dz, TARGET_POWER)
        rows2.append(dict(study=2, contrast="incompatibility_x_valence_interaction", test="paired t on the contrast-of-contrasts score", dz=dz, target_power=TARGET_POWER, n_participants=n,
                          achieved_power=round(power_paired_t(n, dz), 4), role="estimation_only_N_that_would_be_needed"))
        rows2.append(dict(study=2, contrast="incompatibility_x_valence_interaction", test="paired t on the contrast-of-contrasts score", dz=dz, target_power=np.nan, n_participants=N2,
                          achieved_power=round(power_paired_t(N2, dz), 4), role="estimation_only_power_at_study2_N"))
    rows2.append(dict(study=2, contrast="any_paired_contrast", test="paired t", dz=round(mdes(N2), 4), target_power=TARGET_POWER, n_participants=N2, achieved_power=TARGET_POWER, role="MDES"))
    s2 = pd.DataFrame(rows2); s2.insert(0, "version", __version__)
    s2.to_csv(os.path.join(a.out, "power_study2.csv"), index=False)

    # ---- trials budget (v2.1): session 2 alone carries the no-report estimate
    ppc, raw = presented_per_cell()                      # v2.0 pooled rule, reported for comparison only
    ppc2, n_probe2, n_noprobe2, usable2, raw2 = presented_session2_per_cell()
    ppc1 = a.session1_per_cell if a.session1_per_cell is not None else ppc2
    smin = lambda n: session_minutes(n, a.trial_seconds, a.block_trials, a.break_minutes)
    brows = []
    def budget_row(study, grouping, ncells, pooled=1):
        p2 = ppc2 * pooled; p1 = ppc1 * pooled
        m2, nb2, br2 = smin(p2 * ncells); m1, nb1, br1 = smin(p1 * ncells)
        return dict(study=study, cell_grouping=grouping, n_cells=ncells, presentation_cells_pooled_per_cell=pooled,
                    usable_target_per_cell=USABLE_TARGET, probe_fraction=PROBE_FRAC, loss_rate=LOSS_RATE,
                    presented_session2_per_cell_raw_min=round(raw2 * pooled, 2), presented_session2_per_cell=p2,
                    probe_trials_session2_per_cell=n_probe2 * pooled, noprobe_trials_session2_per_cell=n_noprobe2 * pooled,
                    usable_session2_per_cell_expected=round(usable2 * pooled, 2),
                    presented_session1_per_cell=p1, presented_both_sessions_per_cell=p1 + p2,
                    presented_session2_total=p2 * ncells, presented_session1_total=p1 * ncells, presented_both_sessions_total=(p1 + p2) * ncells,
                    usable_session2_total_expected=round(usable2 * pooled * ncells, 2),
                    trial_seconds=a.trial_seconds, block_trials=a.block_trials, break_minutes=a.break_minutes,
                    n_blocks_session2=nb2, break_minutes_session2_total=br2, session2_minutes=round(m2, 1),
                    n_blocks_session1=nb1, session1_minutes=round(m1, 1),
                    v20_presented_per_cell_both_sessions_pooled=presented_per_cell()[0])
    brows.append(budget_row(1, "presentation cells, effector-balanced (this is the budget that is run)", CELLS_STUDY1_PRESENTATION))
    brows.append(budget_row(1, "analysis cells if run unpooled (count1@0, count2@0, count3@0, count3@1, count3@3)", CELLS_STUDY1_ANALYSIS))
    for cell, pooled in ANALYSIS_CELL_POOLING.items():
        brows.append(budget_row(1, f"analysis cell {cell} (pools {pooled} presentation cell{'s' if pooled > 1 else ''})", 1, pooled))
    brows.append(budget_row(2, "valence (3) x shared pairs (3) at count 3 [assumed]", CELLS_STUDY2))
    tb = pd.DataFrame(brows); tb.insert(0, "version", __version__)
    tb.to_csv(os.path.join(a.out, "trials_budget.csv"), index=False)

    # ---- mixed-model convergence check (C1a and C0 at the fixed N, calibrated at USABLE_TARGET = 64 usable session-2 trials per analysis cell)
    CALIB_NOTE = (f"calibrated at the planning floor of {USABLE_TARGET} usable session-2 no-report trials per analysis cell "
                  f"(expected count for a single-presentation-cell analysis cell: {usable2:.1f}); a convergence check on the analytic value, not an independent estimate")
    mixed = None
    if not a.skip_mixed:
        try:
            import statsmodels  # noqa
        except ImportError:
            sys.exit("section9_power.py: statsmodels is not importable but the mixed-model check was requested; "
                     "install statsmodels or pass --skip-mixed to run without it (the check is then reported as skipped, never as done)")
        if a.mixed_sims < 1:
            sys.exit("section9_power.py: --mixed-sims must be >= 1 (or pass --skip-mixed)")
        mc_rows = []
        for i, (contrast, w) in enumerate([("C1a_compatible_vs_incompatible_at_count3", W_C1A), ("C0_threshold_count1_vs_ge2", W_C0)]):
            r = mixed_check(N_FIXED, DZ_PLAN, USABLE_TARGET, w, a.mixed_sims, a.seed + i)
            mc_rows.append(dict(version=__version__, contrast=contrast, n_participants=N_FIXED, dz_calibrated=DZ_PLAN, trials_per_cell=USABLE_TARGET, n_sims=a.mixed_sims,
                                power_analytic=round(power_paired_t(N_FIXED, DZ_PLAN), 4), power_two_stage_sim=r["power_two_stage"], power_mixed_sim=r["power_mixed"],
                                mc_se=round(math.sqrt(0.9 * 0.1 / a.mixed_sims), 4), n_nonconverged=r["n_nonconverged"], sd_slope=round(r["sd_slope"], 4), beta_trial=r["beta_trial"],
                                statsmodels_version=statsmodels.__version__, seed=a.seed + i, calibration_note=CALIB_NOTE))
        mixed = pd.DataFrame(mc_rows)
    if mixed is None:
        mixed = pd.DataFrame([dict(version=__version__, contrast="skipped", n_participants=N_FIXED, dz_calibrated=DZ_PLAN, trials_per_cell=USABLE_TARGET, n_sims=0,
                                   power_analytic=round(power_paired_t(N_FIXED, DZ_PLAN), 4), power_two_stage_sim=np.nan, power_mixed_sim=np.nan, mc_se=np.nan, n_nonconverged=np.nan, sd_slope=np.nan, beta_trial=np.nan,
                                   statsmodels_version="", seed=a.seed, calibration_note="--skip-mixed given: no simulation was run")])
    mixed.to_csv(os.path.join(a.out, "power_mixed_check.csv"), index=False)

    # ---- summary in prose, all numbers read back from the tables
    s1r = pd.read_csv(os.path.join(a.out, "power_study1.csv")); s2r = pd.read_csv(os.path.join(a.out, "power_study2.csv"))
    tbr = pd.read_csv(os.path.join(a.out, "trials_budget.csv")); mxr = pd.read_csv(os.path.join(a.out, "power_mixed_check.csv"))
    g = lambda df, **k: df[np.logical_and.reduce([df[c] == v for c, v in k.items()])].iloc[0]
    c0 = g(s1r, contrast="C0_threshold_count1_vs_ge2", dz=DZ_PLAN, target_power=0.9)
    c1a = g(s1r, contrast="C1a_compatible_vs_incompatible_at_count3", dz=DZ_PLAN, target_power=0.9)
    c0_20 = g(s1r, contrast="C0_threshold_count1_vs_ge2", dz=0.2, target_power=0.9); c0_40 = g(s1r, contrast="C0_threshold_count1_vs_ge2", dz=0.4, target_power=0.9)
    lin = {d: g(s1r, contrast="C1b_linear_in_shared_pairs", dz=d, role="exploratory") for d in dzs}
    omn = {d: g(s1r, contrast="C1b_omnibus_2df", dz=d, role="exploratory") for d in dzs}
    omn_at = {d: g(s1r, contrast="C1b_omnibus_2df", dz=d, role="at_fixed_N") for d in dzs}
    md_ = g(s1r, role="MDES")
    to = {d: g(s1r, contrast="C0_equivalence_count3_vs_count2", dz=d) for d in TOST_BOUNDS}
    v = g(s2r, contrast="valence_main_negative_minus_positive_matched_arousal", dz=DZ_PLAN, target_power=0.9)
    v20 = g(s2r, contrast="valence_main_negative_minus_positive_matched_arousal", dz=0.2, target_power=0.9); v40 = g(s2r, contrast="valence_main_negative_minus_positive_matched_arousal", dz=0.4, target_power=0.9)
    ix_n = g(s2r, contrast="incompatibility_x_valence_interaction", dz=0.2, role="estimation_only_N_that_would_be_needed")
    ix_p = g(s2r, contrast="incompatibility_x_valence_interaction", dz=0.2, role="estimation_only_power_at_study2_N")
    ix_p30 = g(s2r, contrast="incompatibility_x_valence_interaction", dz=0.3, role="estimation_only_power_at_study2_N")
    b_an = tbr[(tbr.study == 1) & tbr.cell_grouping.str.startswith("analysis cells if")].iloc[0]; b_pr = tbr[(tbr.study == 1) & tbr.cell_grouping.str.startswith("presentation")].iloc[0]; b2 = tbr[tbr.study == 2].iloc[0]
    b_cells = tbr[(tbr.study == 1) & tbr.cell_grouping.str.startswith("analysis cell ")]
    L = [f"# Section 9.1 power analysis, new design (section9_power.py v{__version__})", "",
         f"All values below are read from power_study1.csv, power_study2.csv, trials_budget.csv and power_mixed_check.csv written by this script (seed {a.seed}); none is typed by hand. "
         f"alpha = {ALPHA} two-sided; target power {int(TARGET_POWER * 100)} %; effect sizes are dz on per-participant contrast scores.", "",
         "## Study 1 (neutral stimuli, three effectors, 0 / 1 / 3 shared pairs, count branch 1 / 2 / 3)", "",
         f"**C0 (P16, threshold: count 1 vs >= 2 at 0 shared pairs; weights {c0.weights}).** N = {int(c0.n_participants)} participants give {int(TARGET_POWER * 100)} % power at dz = {DZ_PLAN} "
         f"(achieved {c0.achieved_power:.3f}); N = {int(c0_20.n_participants)} at dz = 0.20 and N = {int(c0_40.n_participants)} at dz = 0.40.",
         f"**C1a (P23, author-derived: 0 shared pairs vs mean of 1 and 3 shared pairs at count 3; weights {c1a.weights}).** The same paired-t computation applies: N = {int(c1a.n_participants)} at dz = {DZ_PLAN}. "
         f"The fixed sample is therefore N = {int(c0.n_participants)}; its minimum detectable dz at {int(TARGET_POWER * 100)} % power is {md_.dz:.3f}.",
         f"**Equivalence half of P16 (count 3 - count 2, TOST).** At N = {int(c0.n_participants)} and a true effect of zero, exact TOST power is "
         + "; ".join(f"{to[d].achieved_power:.3f} (Monte Carlo {to[d].tost_power_mc:.3f} +/- {to[d].tost_mc_se:.3f}) for bounds +/-{d}" for d in TOST_BOUNDS)
         + f". To reach {int(TARGET_POWER * 100)} % TOST power one would need N = " + ", ".join(f"{int(to[d].n_for_90pct_tost)} at +/-{d}" for d in TOST_BOUNDS) + ". "
         f"The bound +/-{DZ_PLAN} is the planning effect size itself; the equivalence claim is thus adequately powered at the fixed N only for that bound or wider.",
         f"**C1b (0 / 1 / 3 shared pairs, unequal steps).** With weights linear in the number of shared pairs ({lin[DZ_PLAN].weights}, i.e. -4, -1, +5 up to scale) the one-df test needs N = "
         + ", ".join(f"{int(lin[d].n_participants)} at dz = {d}" for d in dzs) + f". The two-df omnibus (Hotelling T^2, effect on one contrast direction) needs N = "
         + ", ".join(f"{int(omn[d].n_participants)} at dz = {d}" for d in dzs) + f"; at the fixed N = {int(c0.n_participants)} its power is "
         + ", ".join(f"{omn_at[d].achieved_power:.3f} at dz = {d}" for d in dzs) + ". The ordinal weights (-1, 0, +1) are not used: they would treat the step from 1 to 3 shared pairs as equal to the step from 0 to 1.", "",
         "### Trials (session 2 carries the no-report estimate)", "",
         f"Session 1 collects a PAS rating on every trial and trains the access classifier; only session-2 trials enter the no-report estimate. "
         f"With {int(PROBE_FRAC * 100)} % probe trials and an expected loss of {int(LOSS_RATE * 100)} %, the smallest session-2 count per presentation cell with exactly one quarter probe trials that leaves an expected >= {USABLE_TARGET} usable trials is "
         f"{int(b_pr.presented_session2_per_cell)} = {int(b_pr.probe_trials_session2_per_cell)} probe + {int(b_pr.noprobe_trials_session2_per_cell)} no-probe (raw minimum {b_pr.presented_session2_per_cell_raw_min}; expected usable {b_pr.usable_session2_per_cell_expected}). "
         f"Session 1 presents {int(b_pr.presented_session1_per_cell)} per cell (equal sessions). "
         f"For the {int(b_pr.n_cells)} effector-balanced presentation cells that is {int(b_pr.presented_session2_total)} presented trials in session 2 and {int(b_pr.presented_both_sessions_total)} over both sessions; "
         f"at {b_pr.trial_seconds:g} s per trial in {int(b_pr.n_blocks_session2)} blocks of {int(b_pr.block_trials)} with {b_pr.break_minutes:g}-min breaks, session 2 lasts about {b_pr.session2_minutes} min (session 1: {b_pr.session1_minutes} min). "
         f"The previous rule pooled both sessions ({int(b_pr.v20_presented_per_cell_both_sessions_pooled)} presented per cell) and over-counted usable no-report trials by a factor of two.",
         "Expected usable session-2 trials per analysis cell: " + "; ".join(f"{r.cell_grouping.split(' (')[0].replace('analysis cell ', '')} pools {int(r.presentation_cells_pooled_per_cell)} -> {r.usable_session2_per_cell_expected}" for _, r in b_cells.iterrows())
         + f". The mixed-model check below is calibrated at the floor of {USABLE_TARGET} usable trials per analysis cell, the target that the single-presentation-cell analysis cells (count3@0, count3@3) just meet. "
         "No sequential Bayes-factor monitoring is used; N is fixed in advance.", "",
         "### Mixed-model convergence check", ""]
    if mxr.contrast.iloc[0] != "skipped":
        for _, r in mxr.iterrows():
            L.append(f"{r.contrast}: at N = {int(r.n_participants)}, {int(r.trials_per_cell)} usable session-2 trials per analysis cell (calibration floor), {int(r.n_sims)} simulated data sets calibrated to dz = {r.dz_calibrated} (statsmodels {r.statsmodels_version}): "
                     f"analytic power {r.power_analytic:.3f}; two-stage (paired t on contrast scores) {r.power_two_stage_sim:.3f}; linear mixed model with random slopes {r.power_mixed_sim:.3f} "
                     f"(Monte Carlo SE about {r.mc_se}); non-converged fits: {int(r.n_nonconverged)}. Agreement with the analytic value is expected by construction; the check confirms the calibration.")
    else:
        L.append("Skipped: --skip-mixed was given; no simulation was run (n_sims = 0 in power_mixed_check.csv).")
    L += ["", "## Study 2 (valence; Supplementary Protocol S5 only)", "",
          f"**Main effect negative - positive at matched arousal.** N = {int(v.n_participants)} at dz = {DZ_PLAN} ({int(TARGET_POWER * 100)} % power); N = {int(v20.n_participants)} at dz = 0.20 and N = {int(v40.n_participants)} at dz = 0.40.",
          f"**Incompatibility x valence interaction: estimation only.** A confirmatory test at dz = 0.20 would need N = {int(ix_n.n_participants)}; at the Study 2 sample of N = {int(v.n_participants)} the power for that interaction is "
          f"{ix_p.achieved_power:.3f} at dz = 0.20 and {ix_p30.achieved_power:.3f} at dz = 0.30. The interaction is therefore reported with its estimate and interval, not tested.",
          f"Trials: {int(b2.n_cells)} cells ({b2.cell_grouping}) x {int(b2.presented_session2_per_cell)} presented in session 2 = {int(b2.presented_session2_total)} session-2 trials (about {b2.session2_minutes} min); {int(b2.presented_both_sessions_total)} over both sessions.", "",
          "## Assumptions to state in the protocol", "",
          f"- dz is defined on per-participant contrast scores of the cell-mean access index; the mixed-model check is calibrated to the same dz at {USABLE_TARGET} usable session-2 trials per analysis cell (the planning floor) and is not an independent estimate.",
          f"- Session duration uses {a.trial_seconds:g} s per trial, {a.block_trials} trials per block and {a.break_minutes:g}-min breaks; these are planning values to be replaced by pilot timing.",
          "- TOST power is computed under a true effect of exactly zero; if P16's trigger leaves a small residual increase, equivalence power falls.",
          "- The two-df omnibus power assumes the whole effect lies along one standardised contrast direction (the conservative allocation for a fixed dz).",
          f"- Study 2 cell count ({CELLS_STUDY2}) assumes three valence levels crossed with the three shared-pair levels at count 3; the confirmatory contrast uses only the negative and positive cells.",
          "- The 25 % probe-trial fraction and 15 % loss are planning values; the presented-trial count should be re-derived if piloting changes either.",
          f"", f"Runtime of this script: {time.time() - t0:.1f} s."]
    open(os.path.join(a.out, "section9_power_summary.md"), "w").write("\n".join(L) + "\n")
    key = dict(N_fixed_study1=int(N_FIXED), N_required_dz030=int(N_REQUIRED), rotations=ROTATIONS, N_C0_dz030=int(c0.n_participants), N_C1a_dz030=int(c1a.n_participants), N_C0_dz020=int(c0_20.n_participants), N_C0_dz040=int(c0_40.n_participants),
               usable_target_per_analysis_cell=USABLE_TARGET, presented_session2_per_cell=int(ppc2), probe_trials_session2_per_cell=int(n_probe2), noprobe_trials_session2_per_cell=int(n_noprobe2),
               usable_session2_per_cell_expected=round(float(usable2), 2), presented_session1_per_cell=int(ppc1),
               presented_session2_total=int(b_pr.presented_session2_total), presented_both_sessions_total=int(b_pr.presented_both_sessions_total),
               session2_minutes=float(b_pr.session2_minutes), session1_minutes=float(b_pr.session1_minutes), n_blocks_session2=int(b_pr.n_blocks_session2),
               usable_session2_pooled_analysis_cells={r.cell_grouping.split(" (")[0].replace("analysis cell ", ""): float(r.usable_session2_per_cell_expected) for _, r in b_cells.iterrows()},
               v20_presented_per_cell_both_sessions_pooled=int(ppc), presented_session2_total_5_analysis_cells_unpooled=int(b_an.presented_session2_total),
               study2_presented_session2_total=int(b2.presented_session2_total), study2_session2_minutes=float(b2.session2_minutes),
               mixed_check_n_sims={r.contrast: int(r.n_sims) for _, r in mxr.iterrows()}, mixed_check_power_mixed={r.contrast: (None if pd.isna(r.power_mixed_sim) else float(r.power_mixed_sim)) for _, r in mxr.iterrows()},
               tost_power_at_N_bound030_analytic=float(to[0.30].achieved_power), tost_power_at_N_bound030_mc=float(to[0.30].tost_power_mc),
               N_study2_valence_dz030=int(v.n_participants), N_interaction_dz020=int(ix_n.n_participants), runtime_s=round(time.time() - t0, 1))
    json.dump(key, open(os.path.join(a.out, "section9_key_numbers.json"), "w"), indent=1)
    print(json.dumps(key, indent=1))


if __name__ == "__main__":
    main()
