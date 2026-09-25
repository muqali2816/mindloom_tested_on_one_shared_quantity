#!/usr/bin/env python
"""
section9_power.py (v2.4) -- a priori power and session arithmetic for the worked condition of Section 9.1
(Supplementary Protocol S5, protocol version 3).  Every number is recomputed here; nothing from the earlier
designs (3 x 3 incompatibility x valence, N = 126; or the 11-cell / 22-block protocol v2) is carried forward
except where the v2 value is reported for comparison and labelled as such.

Study 1 (neutral stimuli, three effectors) -- protocol v3
---------------------------------------------------------
Three responses on three effectors (left hand / right hand / dominant foot), each a three-position lever.
  incompatibility = number of response PAIRS that share an effector: 0 / 1 / 3
       (three responses on three distinct levers -> 0 shared pairs; two on one lever -> 1;
        all three on one lever -> 3; with three responses, 2 shared pairs is impossible)
  count branch    = 1 / 2 / 3 co-executable responses at 0 shared pairs
Analysis cells (5): count1@0, count2@0, count3@0, count3@1, count3@3.
Presentation cells (7, v3): count 1 on ONE lever (the lever rotated BETWEEN participants) [1 cell]; count 2 on ONE
lever pair (rotated between participants) [1]; count 3 on three distinct levers [1]; count 3 with one lever doubled,
one cell per doubled pair of rules [3]; count 3 all on the designated lever (lever rotated between participants) [1].
Protocol v2 had 11 presentation cells (count 1 and count 2 were run on every lever / lever pair WITHIN participant).

Blocks per presentation cell (v3): 2, except the two single-cell C1a cells (count3@0, count3@3), which receive 3.
Blocks per session = 2 + 2 + 3 + 3 x 2 + 3 = 16 (v2: 22).  The extra block does NOT equalise precision between the
single cells and the pooled count3@1 cell (3 presentation cells x 2 blocks); it removes the floor risk in the
single cells and roughly halves the gap in usable trials.

Sessions (v3).  Each session opens with a separate TITRATION PHASE (PAS rating on every titration trial; a
staircase sets the mask/target contrast); the contrast is then FROZEN for all blocks of the session and nothing
adapts within blocks.  Session 1: PAS rating on no-probe trials (classifier labels and the PAS-report version of the
contrast; the rating does not feed the staircase) and, on probe trials only, AFTER the probe response, the
experienced-conflict ("urge to err") rating of Morsella et al. 2009 (8-point scale).  Session 2: no report in any
block (the no-report confirmatory data).  Sessions are >= 48 h apart, hence the re-titration.

Contrasts (per-participant scores on the cell means of the report-independent access index):
  C1a  CONFIRMATORY (the only one).  0 shared pairs vs mean of 1 and 3 shared pairs at count 3, w = (-1, +1/2, +1/2).
       Tests P23, the authors' one-step derivation from SIT's stated P16: the same condition (incompatible
       intentions), a different outcome (access instead of experienced conflict).  Two-version rule: the EEG-index
       and the PAS-report versions must both be significant in the predicted direction.  No multiplicity correction
       (single confirmatory contrast).
  CR   CONFIRMATORY on the REPORT variable, separately preregistered: the session-1 urge rating at 0 vs mean of 1
       and 3 shared pairs at count 3, same weights.  A direct test of the stated P16 on its own outcome variable
       (register row P35).  Power is computed at an ASSUMED dz (RATING_DZ_ASSUMED), stated as an assumption.
  C0   ESTIMATION.  count 1 vs mean(2, 3) at 0 shared pairs, w = (-1, +1/2, +1/2), two-sided with CI.  Two author
       derivations with opposite signs sit on it: P32 (threshold: positive) and P25 (load decrement: negative).
       The nuisance account "more levers in force -> more access" predicts a POSITIVE C0 and a NEGATIVE C1a
       (0 shared = three levers, 3 shared = one lever), which is why the count branch is kept as an estimate.
  C0-eq ESTIMATION.  count 3 - count 2, bounded estimate: the TOST bound within which the difference falls is
       reported (P33); not a confirmatory test.
  C1b  EXPLORATORY.  0 / 1 / 3 shared pairs with unequal steps: linear-in-shared-pairs weights (-4/3, -1/3, +5/3)
       and the two-df omnibus (Hotelling T^2).  Ordinal weights (-1, 0, +1) are reported only to show what they assume.

Pilot stop criterion on the manipulation (v3): pilot standardised urge-rating difference (3-shared minus 0-shared,
count 3, session-1 probe trials) below STOP_DZ -> intentions are not being formed -> stop and redesign.  STOP_DZ is
set equal to RATING_DZ_ASSUMED: below it the confirmatory rating test would not be warranted at the planned N.
The anchor (Morsella et al. 2009, t(13) = 6.21) is reported as dz for comparison.

Power
-----
Paired t on per-participant contrast scores: exact noncentral-t power, alpha = 0.05 two-sided.
TOST: exact power by numerical integration over the sample SD, checked by Monte Carlo.
Mixed model: trial-level simulation (participant random intercept + random slope on the contrast code, Wald z),
calibrated so the participant-level dz equals the analytic planning value at the usable-trial FLOOR -- a
CONVERGENCE CHECK on the analytic value, not an independent estimate.  Requires statsmodels for that mode only
(--skip-mixed runs without it and writes a single 'skipped' row).

Fixed N: the smallest N with >= 90 % power at dz = 0.30 for C1a, rounded up to a multiple of the six lever
rotations; dz = 0.20 and 0.40 also reported.  No sequential monitoring.

Trials: the no-report access estimate comes from SESSION 2 ONLY.  Budget parameters: probe fraction 0.25, expected
loss 0.15, target >= 64 usable no-report trials per analysis cell.  The session-2 BLOCK size is derived as half of the
smallest two-block presentation count with exactly one quarter probe trials whose no-probe trials survive the loss
rate at >= 64 (104 = 26 probe + 78 no-probe -> 52 per block, 13 probe).  A three-block cell then presents 156
(39 probe + 117 no-probe; 99.45 expected usable).  Session-1 blocks hold SESSION1_BLOCK_TRIALS trials (32, 8 probe).

Study 2 (valence; Supplementary only)
-------------------------------------
Nine cells (valence 3 x shared pairs 3 at count 3), two blocks each, same session template (titration phase,
session-1 ratings).  Main effect negative - positive at matched arousal: N at dz = 0.30 (also 0.20, 0.40).  The
incompatibility x valence interaction is estimation only.

Usage
-----
  python section9_power.py [--out DIR] [--mixed-sims 200 | --skip-mixed] [--mc 200000] [--seed 20260924]
Outputs: power_study1.csv, power_study2.csv, trials_budget.csv, power_mixed_check.csv, section9_key_numbers.json,
         section9_power_summary.md (all numbers in prose are read back from the tables).
"""
from __future__ import annotations
import argparse, json, math, os, sys, time, warnings
import numpy as np
import pandas as pd
from scipy import stats, integrate, optimize

__version__ = "2.4"
ALPHA, TARGET_POWER = 0.05, 0.90
DZ_PLAN, DZ_ALT = 0.30, (0.20, 0.40)
TOST_BOUNDS = (0.20, 0.30, 0.40)
USABLE_TARGET, PROBE_FRAC, LOSS_RATE = 64, 0.25, 0.15
ROTATIONS = 6                                              # lever / rule-to-lever assignments rotated across participants
# ---- session configuration (v2.4): the ONE place the protocol's session arithmetic lives; S5.6-S5.8 and S9.1 read from the outputs
TRIAL_SECONDS = 6.0          # fixation + target + mask + blank + probe phase + ITI, both sessions (planning value)
PAS_SECONDS = 2.0            # PAS rating: session-1 no-probe trials and every titration trial (both sessions)
URGE_SECONDS = 3.0           # experienced-conflict / urge rating after the probe response: session-1 probe trials only
BREAK_MINUTES = 1.0          # break between blocks
TITRATION_TRIALS = 48        # separate titration phase at the start of EACH session (PAS on every trial), design choice; contrast frozen afterwards
PRACTICE_PER_BLOCK_S1 = 4    # unanalysed full-contrast practice trials at the start of each session-1 block
SESSION1_BLOCK_TRIALS = 32   # session-1 block (8 probe + 24 no-probe): design choice, quarter-probe integer
BLOCKS_DEFAULT, BLOCKS_C1A_SINGLE = 2, 3                   # blocks per presentation cell; the two single-cell C1a cells get 3
# presentation cells (v3): name, analysis cell, blocks per session, what is balanced and how
PRESENTATION_CELLS = [
    dict(cell="count1@0", analysis="count1@0", blocks=BLOCKS_DEFAULT, balance="one rule on one lever; lever rotated between participants"),
    dict(cell="count2@0", analysis="count2@0", blocks=BLOCKS_DEFAULT, balance="two rules on two levers; lever pair rotated between participants"),
    dict(cell="count3@0", analysis="count3@0", blocks=BLOCKS_C1A_SINGLE, balance="three rules on three levers; rule-to-lever assignment rotated between participants (C1a cell)"),
    dict(cell="count3@1_pairA", analysis="count3@1", blocks=BLOCKS_DEFAULT, balance="rules 1 and 2 share a lever (shared lever rotated between participants)"),
    dict(cell="count3@1_pairB", analysis="count3@1", blocks=BLOCKS_DEFAULT, balance="rules 1 and 3 share a lever (shared lever rotated between participants)"),
    dict(cell="count3@1_pairC", analysis="count3@1", blocks=BLOCKS_DEFAULT, balance="rules 2 and 3 share a lever (shared lever rotated between participants)"),
    dict(cell="count3@3", analysis="count3@3", blocks=BLOCKS_C1A_SINGLE, balance="all rules on one lever; lever rotated between participants (C1a cell)"),
]
ANALYSIS_CELLS = ["count1@0", "count2@0", "count3@0", "count3@1", "count3@3"]
C1A_CELLS = ["count3@0", "count3@1", "count3@3"]
CELLS_STUDY1_PRESENTATION, CELLS_STUDY1_ANALYSIS = len(PRESENTATION_CELLS), len(ANALYSIS_CELLS)
CELLS_STUDY2, BLOCKS_STUDY2 = 9, 2   # 3 incompatibility levels (0/1/3 shared pairs at count 3) x 3 valence (negative, neutral, positive)
SHARED_PAIRS = np.array([0.0, 1.0, 3.0])
W_C0 = np.array([-1.0, 0.5, 0.5])                      # count 1 vs mean(count 2, count 3)   -- estimation
W_C1A = np.array([-1.0, 0.5, 0.5])                     # 0 shared vs mean(1, 3 shared)       -- the confirmatory contrast
W_CR = W_C1A                                           # same weights on the session-1 urge rating -- report-based test of P16
W_C1B_LIN = SHARED_PAIRS - SHARED_PAIRS.mean()         # (-4/3, -1/3, 5/3): linear in the number of shared pairs
W_C1B_ORDINAL = np.array([-1.0, 0.0, 1.0])             # reported only to show what it assumes
W_EQUIV = np.array([0.0, -1.0, 1.0])                   # count 3 - count 2 (bounded estimate)
# ---- report-based P16 test and pilot stop criterion (v2.4)
RATING_DZ_ASSUMED = 0.50     # assumed dz for the urge-rating contrast CR (an assumption, stated as such in S5.13)
STOP_DZ = RATING_DZ_ASSUMED  # pilot stop criterion: standardised urge difference (3-shared minus 0-shared) below this -> stop and redesign
ANCHOR_T, ANCHOR_DF = 6.21, 13   # Morsella et al. 2009 (Emotion 9): incompatible vs compatible intentions on the urge rating, t(13) = 6.21


# ---------------------------------------------------------------- paired t
def power_paired_t(n, dz, alpha=ALPHA):
    """Exact power of the two-sided one-sample (paired) t test, noncentral t."""
    df = n - 1
    tc = stats.t.ppf(1 - alpha / 2, df)
    nc = dz * math.sqrt(n)
    up, lo = stats.nct.sf(tc, df, nc), stats.nct.cdf(-tc, df, nc)
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
    """Exact power of the paired TOST (two one-sided t tests at level alpha each) for equivalence bounds +/- delta
    (in SD units of the paired difference), true standardised effect mu.  Both tests share the sample SD s."""
    df = n - 1
    tc = stats.t.ppf(1 - alpha, df)
    s_max = delta * math.sqrt(n) / tc
    sq = math.sqrt(n)

    def integrand(s):
        hi = delta - tc * s / sq
        p = stats.norm.cdf(sq * (hi - mu)) - stats.norm.cdf(sq * (-hi - mu))
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
    """Trial-level simulation for one contrast with weights w over K cells (see v2.3 docstring: cell code c_k = w_k / sum(w_k^2);
    b_i ~ N(beta, sd_b^2) with sd_b chosen so that dz = beta / sqrt(sd_b^2 + sigma_e^2 sum(w^2)/n_trials)).  Fits the participant-level
    paired t and a linear mixed model with random intercept and slope (Wald z)."""
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
        mu = u[:, None] + b[:, None] * c[None, :]
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
def presented_session2_two_block_cell(usable=USABLE_TARGET, probe=PROBE_FRAC, loss=LOSS_RATE, blocks=BLOCKS_DEFAULT):
    """Smallest integer n, divisible by blocks and by the probe denominator per block, such that the no-probe trials survive the loss
    rate with expectation >= usable:  n (1 - probe)(1 - loss) >= usable.  Returns (n, n_probe, n_noprobe, expected_usable, raw_minimum)."""
    from fractions import Fraction
    step = Fraction(probe).limit_denominator(100).denominator * blocks      # 0.25, 2 blocks -> 8
    raw = usable / ((1 - probe) * (1 - loss))
    n = math.ceil(raw); n += (-n) % step
    n_probe = round(n * probe); n_noprobe = n - n_probe
    exp_usable = n_noprobe * (1 - loss)
    assert exp_usable >= usable and n_probe == n * probe, (n, n_probe, exp_usable)
    return n, n_probe, n_noprobe, exp_usable, raw


def cell_table(cells, block_trials_s2, block_trials_s1, loss=LOSS_RATE, probe=PROBE_FRAC):
    """Per-presentation-cell budget rows for a list of cell dicts."""
    rows = []
    for c in cells:
        b = c["blocks"]
        p2, p1 = b * block_trials_s2, b * block_trials_s1
        pr2, pr1 = int(p2 * probe), int(p1 * probe)
        rows.append(dict(cell=c["cell"], analysis_cell=c["analysis"], blocks_per_session=b, balance=c["balance"],
                         presented_session2=p2, probe_session2=pr2, noprobe_session2=p2 - pr2, usable_session2_expected=round((p2 - pr2) * (1 - loss), 2),
                         presented_session1=p1, probe_session1=pr1, noprobe_session1=p1 - pr1,
                         pas_rated_session1_expected=round((p1 - pr1) * (1 - loss), 2),    # PAS on session-1 no-probe trials (labels, PAS version)
                         urge_rated_session1=pr1))                                          # urge rating on session-1 probe trials (behavioural; no EEG loss applied)
    return pd.DataFrame(rows)


def session_minutes(n_blocks, n_probe, n_noprobe, session, trial_seconds=TRIAL_SECONDS, pas_seconds=PAS_SECONDS, urge_seconds=URGE_SECONDS,
                    break_minutes=BREAK_MINUTES, titration_trials=TITRATION_TRIALS, practice_per_block=PRACTICE_PER_BLOCK_S1):
    """Per-session arithmetic (v2.4).  Both sessions: titration phase (PAS on every titration trial) + blocks + breaks between blocks.
    Session 1 additionally: PAS on no-probe trials, urge rating on probe trials, practice trials per block.  Session 2: no report in blocks."""
    titration = titration_trials * (trial_seconds + pas_seconds) / 60.0
    breaks = max(n_blocks - 1, 0) * break_minutes
    if session == 2:
        trials = (n_probe + n_noprobe) * trial_seconds / 60.0
        practice = 0.0
    else:
        trials = (n_noprobe * (trial_seconds + pas_seconds) + n_probe * (trial_seconds + urge_seconds)) / 60.0
        practice = n_blocks * practice_per_block * trial_seconds / 60.0
    total = titration + trials + practice + breaks
    return dict(titration_minutes=round(titration, 1), trial_minutes=round(trials, 1), practice_minutes=round(practice, 1), break_minutes_total=breaks, total_minutes=round(total, 1))


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=".")
    ap.add_argument("--mixed-sims", type=int, default=200)
    ap.add_argument("--skip-mixed", action="store_true")
    ap.add_argument("--mc", type=int, default=200_000, help="Monte Carlo replicates for the TOST check")
    ap.add_argument("--seed", type=int, default=20260924)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    dzs = sorted({DZ_PLAN, *DZ_ALT})

    # ---- Study 1: N for the confirmatory contrast C1a (C0 reported as the estimation contrast it now is)
    rows = []
    for contrast, w, hyp, role in [("C1a_compatible_vs_incompatible_at_count3", W_C1A, "P23 (one-step derivation from P16: same condition, access instead of experienced conflict)", "confirmatory"),
                                   ("C0_threshold_count1_vs_ge2", W_C0, "P32 / P25 (two author derivations, opposite signs) -- ESTIMATION, two-sided with CI", "estimation")]:
        for dz in dzs:
            for pw in (0.80, 0.90):
                n = n_for_power(dz, pw)
                rows.append(dict(study=1, contrast=contrast, hypothesis=hyp, weights=str(w.tolist()), test="paired t, two-sided", dz=dz, target_power=pw,
                                 n_participants=n, achieved_power=round(power_paired_t(n, dz), 4), role=role if (dz == DZ_PLAN and pw == TARGET_POWER) else "sensitivity"))
    N_REQUIRED = n_for_power(DZ_PLAN, TARGET_POWER)            # smallest N reaching the target (119 at dz 0.30)
    N_FIXED = int(math.ceil(N_REQUIRED / ROTATIONS) * ROTATIONS) # rounded UP to a multiple of the rotation count (120)
    # C1b: linear-in-shared-pairs (one df) and the omnibus (two df)
    for dz in dzs:
        n1 = n_for_power(dz, TARGET_POWER); n2 = n_for_omnibus(dz, TARGET_POWER)
        rows.append(dict(study=1, contrast="C1b_linear_in_shared_pairs", hypothesis="exploratory (0/1/3 shared pairs)", weights=str(np.round(W_C1B_LIN, 4).tolist()),
                         test="paired t on the centred shared-pairs score", dz=dz, target_power=TARGET_POWER, n_participants=n1, achieved_power=round(power_paired_t(n1, dz), 4), role="exploratory"))
        rows.append(dict(study=1, contrast="C1b_omnibus_2df", hypothesis="exploratory (0/1/3 shared pairs)", weights="two orthogonal contrasts",
                         test="Hotelling T^2, F(2, N-2), effect on one direction", dz=dz, target_power=TARGET_POWER, n_participants=n2, achieved_power=round(power_omnibus_2df(n2, dz), 4), role="exploratory"))
    # what the fixed N buys for each contrast
    for contrast, dz in [("C1a_compatible_vs_incompatible_at_count3", DZ_PLAN), ("C0_threshold_count1_vs_ge2", DZ_PLAN)] + [("C1b_linear_in_shared_pairs", d) for d in dzs] + [("C1b_omnibus_2df", d) for d in dzs]:
        pw = power_omnibus_2df(N_FIXED, dz) if contrast.endswith("2df") else power_paired_t(N_FIXED, dz)
        rows.append(dict(study=1, contrast=contrast, hypothesis="power at the fixed N", weights="", test="", dz=dz, target_power=np.nan, n_participants=N_FIXED, achieved_power=round(pw, 4), role="at_fixed_N"))
    rows.append(dict(study=1, contrast="any_paired_contrast", hypothesis="minimum detectable dz at the fixed N", weights="", test="paired t", dz=round(mdes(N_FIXED), 4), target_power=TARGET_POWER, n_participants=N_FIXED, achieved_power=TARGET_POWER, role="MDES"))
    # CR: report-based test of the stated P16 on the session-1 urge rating (v2.4)
    for dz in sorted({RATING_DZ_ASSUMED, *dzs}):
        rows.append(dict(study=1, contrast="CR_urge_rating_0_vs_incompatible_at_count3", hypothesis="P16 (stated, SIT) on its own outcome variable -- report-based, separately preregistered",
                         weights=str(W_CR.tolist()), test="paired t, two-sided, session-1 probe-trial urge ratings", dz=dz, target_power=np.nan, n_participants=N_FIXED,
                         achieved_power=round(power_paired_t(N_FIXED, dz), 4), role="confirmatory_report_at_assumed_dz" if dz == RATING_DZ_ASSUMED else "sensitivity"))
    anchor_dz = ANCHOR_T / math.sqrt(ANCHOR_DF + 1)
    rows.append(dict(study=1, contrast="CR_urge_rating_0_vs_incompatible_at_count3", hypothesis="effect-size anchor: Morsella et al. 2009, t(13) = 6.21, incompatible vs compatible intentions (upper bound)",
                     weights="", test="dz = t / sqrt(n)", dz=round(anchor_dz, 4), target_power=np.nan, n_participants=ANCHOR_DF + 1, achieved_power=np.nan, role="anchor"))
    rows.append(dict(study=1, contrast="pilot_stop_urge_manipulation_check", hypothesis="pilot stop criterion: standardised urge difference (3-shared minus 0-shared, count 3) below this value -> stop and redesign",
                     weights="", test="paired dz on pilot participants", dz=STOP_DZ, target_power=np.nan, n_participants=np.nan, achieved_power=np.nan, role="pilot_stop_threshold"))
    # TOST for the bounded estimate P33 (count 3 vs count 2)
    tost_rows = []
    for delta in TOST_BOUNDS:
        p_an = power_tost_exact(N_FIXED, delta)
        p_mc, se_mc = power_tost_mc(N_FIXED, delta, n_sim=a.mc, seed=a.seed)
        n_t = n_for_tost(delta)
        tost_rows.append(dict(study=1, contrast="C0_equivalence_count3_vs_count2", hypothesis="P33 (author-derived): no further increase from 2 to 3 (true effect 0) -- BOUNDED ESTIMATE, not a confirmatory test", weights=str(W_EQUIV.tolist()),
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
    N2_REQUIRED = n_for_power(DZ_PLAN, TARGET_POWER)
    N2 = int(math.ceil(N2_REQUIRED / ROTATIONS) * ROTATIONS)
    for dz in (0.20, 0.30):
        n = n_for_power(dz, TARGET_POWER)
        rows2.append(dict(study=2, contrast="incompatibility_x_valence_interaction", test="paired t on the contrast-of-contrasts score", dz=dz, target_power=TARGET_POWER, n_participants=n,
                          achieved_power=round(power_paired_t(n, dz), 4), role="estimation_only_N_that_would_be_needed"))
        rows2.append(dict(study=2, contrast="incompatibility_x_valence_interaction", test="paired t on the contrast-of-contrasts score", dz=dz, target_power=np.nan, n_participants=N2,
                          achieved_power=round(power_paired_t(N2, dz), 4), role="estimation_only_power_at_study2_N"))
    rows2.append(dict(study=2, contrast="any_paired_contrast", test="paired t", dz=round(mdes(N2), 4), target_power=TARGET_POWER, n_participants=N2, achieved_power=TARGET_POWER, role="MDES"))
    s2 = pd.DataFrame(rows2); s2.insert(0, "version", __version__)
    s2.to_csv(os.path.join(a.out, "power_study2.csv"), index=False)

    # ---- trials budget (v2.4): 7 presentation cells, unequal block counts, titration phase, session-1 ratings
    ppc2, n_probe2, n_noprobe2, usable2, raw2 = presented_session2_two_block_cell()
    block_trials_s2 = ppc2 // BLOCKS_DEFAULT; block_trials_s1 = SESSION1_BLOCK_TRIALS
    assert (block_trials_s2 * PROBE_FRAC).is_integer() and (block_trials_s1 * PROBE_FRAC).is_integer(), "probe count per block must be an integer"
    ct = cell_table(PRESENTATION_CELLS, block_trials_s2, block_trials_s1)
    ct.insert(0, "study", 1)
    # analysis-cell view: pool presentation cells
    an = ct.groupby("analysis_cell", sort=False).agg(presentation_cells_pooled=("cell", "count"), blocks_per_session=("blocks_per_session", "sum"),
                                                     presented_session2=("presented_session2", "sum"), noprobe_session2=("noprobe_session2", "sum"),
                                                     usable_session2_expected=("usable_session2_expected", "sum"), presented_session1=("presented_session1", "sum"),
                                                     pas_rated_session1_expected=("pas_rated_session1_expected", "sum"), urge_rated_session1=("urge_rated_session1", "sum")).reset_index()
    for col in ("usable_session2_expected", "pas_rated_session1_expected"):
        an[col] = an[col].round(2)
    an["role"] = an.analysis_cell.map(lambda c: "confirmatory C1a cell" if c in C1A_CELLS else "estimation (count branch)")
    # session totals
    def totals(df, study):
        nb = int(df.blocks_per_session.sum())
        s2m = session_minutes(nb, int(df.probe_session2.sum()), int(df.noprobe_session2.sum()), 2)
        s1m = session_minutes(nb, int(df.probe_session1.sum()), int(df.noprobe_session1.sum()), 1)
        return dict(version=__version__, study=study, n_presentation_cells=len(df), n_analysis_cells=int(df.analysis_cell.nunique()), n_blocks_per_session=nb,
                    block_trials_session2=block_trials_s2, probe_per_block_session2=int(block_trials_s2 * PROBE_FRAC), block_trials_session1=block_trials_s1, probe_per_block_session1=int(block_trials_s1 * PROBE_FRAC),
                    usable_target_per_cell=USABLE_TARGET, probe_fraction=PROBE_FRAC, loss_rate=LOSS_RATE,
                    two_block_cell_presented_session2=ppc2, two_block_cell_raw_min=round(raw2, 2), two_block_cell_probe=n_probe2, two_block_cell_noprobe=n_noprobe2, two_block_cell_usable_expected=round(usable2, 2),
                    presented_session2_total=int(df.presented_session2.sum()), probe_session2_total=int(df.probe_session2.sum()), noprobe_session2_total=int(df.noprobe_session2.sum()),
                    usable_session2_total_expected=round(float(df.usable_session2_expected.sum()), 2),
                    presented_session1_total=int(df.presented_session1.sum()), probe_session1_total=int(df.probe_session1.sum()), noprobe_session1_total=int(df.noprobe_session1.sum()),
                    practice_trials_session1=nb * PRACTICE_PER_BLOCK_S1, urge_ratings_session1_total=int(df.urge_rated_session1.sum()),
                    presented_both_sessions_total=int(df.presented_session2.sum() + df.presented_session1.sum()),
                    titration_trials_per_session=TITRATION_TRIALS, trial_seconds=TRIAL_SECONDS, pas_seconds=PAS_SECONDS, urge_seconds=URGE_SECONDS, break_minutes=BREAK_MINUTES,
                    session2_titration_minutes=s2m["titration_minutes"], session2_trial_minutes=s2m["trial_minutes"], session2_break_minutes=s2m["break_minutes_total"], session2_minutes=s2m["total_minutes"],
                    session1_titration_minutes=s1m["titration_minutes"], session1_trial_minutes=s1m["trial_minutes"], session1_practice_minutes=s1m["practice_minutes"], session1_break_minutes=s1m["break_minutes_total"], session1_minutes=s1m["total_minutes"])
    tot1 = totals(ct, 1)
    cells2 = [dict(cell=f"{v}@{s}", analysis=f"{v}@{s}", blocks=BLOCKS_STUDY2, balance="valence x shared pairs at count 3 (assumed cell structure)") for v in ("negative", "neutral", "positive") for s in (0, 1, 3)]
    ct2 = cell_table(cells2, block_trials_s2, block_trials_s1); ct2.insert(0, "study", 2)
    tot2 = totals(ct2, 2)
    # v2 (11 cells x 2 blocks) reported for comparison only
    v2_blocks = 22; v2_s2 = dict(total_minutes=round(v2_blocks * block_trials_s2 * TRIAL_SECONDS / 60 + (v2_blocks - 1) * BREAK_MINUTES, 1))
    ct.insert(1, "version", __version__); ct2.insert(1, "version", __version__); an.insert(0, "version", __version__); an.insert(1, "study", 1)
    tb = pd.DataFrame([tot1, tot2])
    tb.to_csv(os.path.join(a.out, "trials_budget.csv"), index=False)
    pd.concat([ct, ct2]).to_csv(os.path.join(a.out, "trials_budget_cells.csv"), index=False)
    an.to_csv(os.path.join(a.out, "trials_budget_analysis_cells.csv"), index=False)

    # ---- mixed-model convergence check (C1a and C0 at the fixed N, calibrated at the USABLE_TARGET floor)
    single_usable = float(an.set_index("analysis_cell").loc["count3@0", "usable_session2_expected"])
    CALIB_NOTE = (f"calibrated at the planning floor of {USABLE_TARGET} usable session-2 no-report trials per analysis cell "
                  f"(expected count in the three-block single C1a cells: {single_usable:.2f}; in the pooled count3@1 cell: {float(an.set_index('analysis_cell').loc['count3@1', 'usable_session2_expected']):.2f}); "
                  "a convergence check on the analytic value, not an independent estimate")
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
    tbr = pd.read_csv(os.path.join(a.out, "trials_budget.csv")); anr = pd.read_csv(os.path.join(a.out, "trials_budget_analysis_cells.csv")); mxr = pd.read_csv(os.path.join(a.out, "power_mixed_check.csv"))
    g = lambda df, **k: df[np.logical_and.reduce([df[c] == v for c, v in k.items()])].iloc[0]
    c1a = g(s1r, contrast="C1a_compatible_vs_incompatible_at_count3", dz=DZ_PLAN, target_power=0.9)
    c1a_20 = g(s1r, contrast="C1a_compatible_vs_incompatible_at_count3", dz=0.2, target_power=0.9); c1a_40 = g(s1r, contrast="C1a_compatible_vs_incompatible_at_count3", dz=0.4, target_power=0.9)
    c1a_at = g(s1r, contrast="C1a_compatible_vs_incompatible_at_count3", role="at_fixed_N")
    cr = g(s1r, contrast="CR_urge_rating_0_vs_incompatible_at_count3", role="confirmatory_report_at_assumed_dz"); cr30 = g(s1r, contrast="CR_urge_rating_0_vs_incompatible_at_count3", dz=DZ_PLAN)
    anc = g(s1r, role="anchor"); stop = g(s1r, role="pilot_stop_threshold")
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
    b1 = tbr[tbr.study == 1].iloc[0]; b2 = tbr[tbr.study == 2].iloc[0]
    A = anr.set_index("analysis_cell")
    L = [f"# Section 9.1 power analysis and session arithmetic, protocol v3 (section9_power.py v{__version__})", "",
         f"All values below are read from power_study1.csv, power_study2.csv, trials_budget.csv, trials_budget_cells.csv, trials_budget_analysis_cells.csv and power_mixed_check.csv written by this script (seed {a.seed}); none is typed by hand. "
         f"alpha = {ALPHA} two-sided; target power {int(TARGET_POWER * 100)} %; effect sizes are dz on per-participant contrast scores.", "",
         "## Study 1 (neutral stimuli, three effectors, 0 / 1 / 3 shared pairs at count 3; count branch 1 / 2 / 3 as estimation)", "",
         f"**C1a, the single confirmatory contrast (P23: 0 shared pairs vs mean of 1 and 3 shared pairs at count 3; weights {c1a.weights}).** N = {int(c1a.n_participants)} participants are required for {int(TARGET_POWER * 100)} % power at dz = {DZ_PLAN} "
         f"(achieved {c1a.achieved_power:.3f}); N = {int(c1a_20.n_participants)} at dz = 0.20 and N = {int(c1a_40.n_participants)} at dz = 0.40. The fixed sample is N = {N_FIXED} (the required {int(c1a.n_participants)} rounded up to a multiple of the {ROTATIONS} lever rotations); "
         f"power at N = {N_FIXED} and dz = {DZ_PLAN} is {c1a_at.achieved_power:.4f}, uncorrected (one confirmatory contrast, so no multiplicity correction applies); minimum detectable dz at {int(TARGET_POWER * 100)} % power {md_.dz:.4f}.",
         f"**CR, the report-based test of the stated P16 (session-1 urge rating, same cells and weights).** At the ASSUMED dz = {RATING_DZ_ASSUMED} its power at N = {N_FIXED} is {cr.achieved_power:.4f}; at dz = {DZ_PLAN} it is {cr30.achieved_power:.4f}. "
         f"The anchor (Morsella et al. 2009, t({ANCHOR_DF}) = {ANCHOR_T}) corresponds to dz = {anc.dz:.3f}, an upper bound; the assumed value is below a third of it. "
         f"Pilot stop criterion on the manipulation: a standardised urge difference (3-shared minus 0-shared) below dz = {stop.dz} stops the study.",
         f"**C0 (estimation; P32 positive, P25 negative; weights {g(s1r, contrast='C0_threshold_count1_vs_ge2', dz=DZ_PLAN, target_power=0.9).weights}).** Reported two-sided with its interval; for orientation, a paired t at N = {N_FIXED} would have power {g(s1r, contrast='C0_threshold_count1_vs_ge2', role='at_fixed_N').achieved_power:.4f} at dz = {DZ_PLAN}.",
         f"**P33 (count 3 - count 2, bounded estimate).** At N = {N_FIXED} and a true effect of zero, exact TOST power is "
         + "; ".join(f"{to[d].achieved_power:.3f} (Monte Carlo {to[d].tost_power_mc:.3f} +/- {to[d].tost_mc_se:.3f}) for bounds +/-{d}" for d in TOST_BOUNDS)
         + f". To reach {int(TARGET_POWER * 100)} % TOST power one would need N = " + ", ".join(f"{int(to[d].n_for_90pct_tost)} at +/-{d}" for d in TOST_BOUNDS) + ". The bound is reported, not tested.",
         f"**C1b (exploratory).** Linear-in-shared-pairs weights ({lin[DZ_PLAN].weights}): N = " + ", ".join(f"{int(lin[d].n_participants)} at dz = {d}" for d in dzs)
         + f". Two-df omnibus: N = " + ", ".join(f"{int(omn[d].n_participants)} at dz = {d}" for d in dzs) + f"; at N = {N_FIXED} power " + ", ".join(f"{omn_at[d].achieved_power:.3f} at dz = {d}" for d in dzs) + ".", "",
         "### Cells, blocks and trials (session 2 carries the no-report estimate)", "",
         f"{int(b1.n_presentation_cells)} presentation cells collapsing to {int(b1.n_analysis_cells)} analysis cells; {int(b1.n_blocks_per_session)} blocks per session "
         f"(two per cell, three in the two single-cell C1a cells). Session-2 block: {int(b1.block_trials_session2)} trials ({int(b1.probe_per_block_session2)} probe); session-1 block: {int(b1.block_trials_session1)} ({int(b1.probe_per_block_session1)} probe). "
         f"A two-block cell presents {int(b1.two_block_cell_presented_session2)} in session 2 = {int(b1.two_block_cell_probe)} probe + {int(b1.two_block_cell_noprobe)} no-probe (raw minimum {b1.two_block_cell_raw_min}; expected usable {b1.two_block_cell_usable_expected}).",
         "Expected usable session-2 trials per analysis cell: " + "; ".join(f"{c} ({int(A.loc[c, 'presentation_cells_pooled'])} presentation cell(s), {int(A.loc[c, 'blocks_per_session'])} blocks) -> {A.loc[c, 'usable_session2_expected']:.2f}" for c in ANALYSIS_CELLS) + ".",
         f"Session 2 ({int(b1.presented_session2_total)} presented trials, no report in blocks): titration {b1.session2_titration_minutes} min ({int(b1.titration_trials_per_session)} trials at {b1.trial_seconds + b1.pas_seconds:g} s) + trials {b1.session2_trial_minutes} min at {b1.trial_seconds:g} s + {int(b1.n_blocks_per_session) - 1} breaks of {b1.break_minutes:g} min = {b1.session2_minutes} min (v2, 22 blocks: {v2_s2['total_minutes']} min, no titration phase).",
         f"Session 1 ({int(b1.presented_session1_total)} presented trials; PAS on {int(b1.noprobe_session1_total)} no-probe trials, urge rating on {int(b1.urge_ratings_session1_total)} probe trials): titration {b1.session1_titration_minutes} min + trials {b1.session1_trial_minutes} min + practice {b1.session1_practice_minutes} min ({int(b1.practice_trials_session1)} trials) + breaks {b1.session1_break_minutes:g} min = {b1.session1_minutes} min, plus training to criterion and set-up (pilot).",
         "Urge ratings per C1a analysis cell in session 1 (probe trials, before any loss): " + "; ".join(f"{c} {int(A.loc[c, 'urge_rated_session1'])}" for c in C1A_CELLS) + ". PAS-rated session-1 trials per analysis cell after loss: " + "; ".join(f"{c} {A.loc[c, 'pas_rated_session1_expected']:.1f}" for c in ANALYSIS_CELLS) + ".",
         f"The mixed-model check below is calibrated at the floor of {USABLE_TARGET} usable trials per analysis cell. No sequential monitoring; N is fixed in advance.", "",
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
          f"**Incompatibility x valence interaction: estimation only.** A confirmatory test at dz = 0.20 would need N = {int(ix_n.n_participants)}; at N = {N2} its power is {ix_p.achieved_power:.3f} at dz = 0.20 and {ix_p30.achieved_power:.3f} at dz = 0.30.",
          f"Trials: {int(b2.n_presentation_cells)} cells x {BLOCKS_STUDY2} blocks = {int(b2.n_blocks_per_session)} blocks; {int(b2.presented_session2_total)} presented in session 2 ({b2.session2_minutes} min with titration and breaks); {int(b2.presented_session1_total)} in session 1 ({b2.session1_minutes} min); {int(b2.presented_both_sessions_total)} over both sessions.", "",
          "## Assumptions to state in the protocol", "",
          f"- dz is defined on per-participant contrast scores of the cell-mean access index; the mixed-model check is calibrated at {USABLE_TARGET} usable session-2 trials per analysis cell (the floor) and is not an independent estimate.",
          f"- Session duration uses {TRIAL_SECONDS:g} s per trial, +{PAS_SECONDS:g} s for a PAS rating (titration trials in both sessions; session-1 no-probe trials), +{URGE_SECONDS:g} s for the urge rating (session-1 probe trials), {TITRATION_TRIALS} titration trials per session, {PRACTICE_PER_BLOCK_S1} practice trials per session-1 block and {BREAK_MINUTES:g}-min breaks; planning values to be replaced by pilot timing.",
          f"- The urge-rating contrast CR is powered at an ASSUMED dz = {RATING_DZ_ASSUMED}; the pilot stop threshold equals that value.",
          "- TOST power is computed under a true effect of exactly zero.",
          "- The two-df omnibus power assumes the whole effect lies along one standardised contrast direction.",
          f"- Study 2 cell count ({CELLS_STUDY2}) assumes three valence levels crossed with the three shared-pair levels at count 3, two blocks each.",
          "- The 25 % probe-trial fraction and 15 % loss are planning values; the presented-trial counts are re-derived if piloting changes either.",
          "", f"Runtime of this script: {time.time() - t0:.1f} s."]
    open(os.path.join(a.out, "section9_power_summary.md"), "w").write("\n".join(L) + "\n")
    key = dict(version=__version__, N_fixed_study1=int(N_FIXED), N_required_dz030=int(N_REQUIRED), rotations=ROTATIONS,
               N_C1a_dz030=int(c1a.n_participants), N_C1a_dz020=int(c1a_20.n_participants), N_C1a_dz040=int(c1a_40.n_participants),
               power_C1a_at_N=float(c1a_at.achieved_power), mdes_at_N=float(md_.dz), n_confirmatory_contrasts_access_index=1,
               rating_contrast=dict(assumed_dz=RATING_DZ_ASSUMED, power_at_N=float(cr.achieved_power), power_at_dz030=float(cr30.achieved_power), anchor_dz=round(float(anc.dz), 4), anchor_t=ANCHOR_T, anchor_df=ANCHOR_DF),
               pilot_stop_dz=STOP_DZ,
               n_cells=int(b1.n_presentation_cells), n_analysis_cells=int(b1.n_analysis_cells), n_blocks_session1=int(b1.n_blocks_per_session), n_blocks_session2=int(b1.n_blocks_per_session),
               blocks_per_cell={c["cell"]: c["blocks"] for c in PRESENTATION_CELLS},
               usable_target_per_analysis_cell=USABLE_TARGET, presented_session2_per_cell=int(ppc2), probe_trials_session2_per_cell=int(n_probe2), noprobe_trials_session2_per_cell=int(n_noprobe2),
               usable_session2_per_cell_expected=round(float(usable2), 2), presented_session1_per_cell=int(BLOCKS_DEFAULT * block_trials_s1),
               usable_single_cell=float(A.loc["count3@0", "usable_session2_expected"]), usable_pooled_cell=float(A.loc["count3@1", "usable_session2_expected"]),
               usable_session2_analysis_cells={c: float(A.loc[c, "usable_session2_expected"]) for c in ANALYSIS_CELLS},
               urge_ratings_session1_per_c1a_cell={c: int(A.loc[c, "urge_rated_session1"]) for c in C1A_CELLS},
               pas_rated_session1_analysis_cells={c: float(A.loc[c, "pas_rated_session1_expected"]) for c in ANALYSIS_CELLS},
               presented_session2_total=int(b1.presented_session2_total), presented_session1_total=int(b1.presented_session1_total), presented_both_sessions_total=int(b1.presented_both_sessions_total),
               session2_minutes=float(b1.session2_minutes), session1_minutes=float(b1.session1_minutes), titration_minutes_per_session=float(b1.session2_titration_minutes),
               v2_session2_minutes_22_blocks=v2_s2["total_minutes"],
               study2_presented_session2_total=int(b2.presented_session2_total), study2_session2_minutes=float(b2.session2_minutes), study2_n_blocks=int(b2.n_blocks_per_session),
               mixed_check_n_sims={r.contrast: int(r.n_sims) for _, r in mxr.iterrows()}, mixed_check_power_mixed={r.contrast: (None if pd.isna(r.power_mixed_sim) else float(r.power_mixed_sim)) for _, r in mxr.iterrows()},
               tost_power_at_N_bound030_analytic=float(to[0.30].achieved_power), tost_power_at_N_bound030_mc=float(to[0.30].tost_power_mc),
               N_study2_valence_dz030=int(v.n_participants), N_interaction_dz020=int(ix_n.n_participants), runtime_s=round(time.time() - t0, 1))
    json.dump(key, open(os.path.join(a.out, "section9_key_numbers.json"), "w"), indent=1)
    print(json.dumps(key, indent=1))


if __name__ == "__main__":
    main()
