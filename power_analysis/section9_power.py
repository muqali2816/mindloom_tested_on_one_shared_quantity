"""
section9_power.py — a priori power for the worked §9 condition
(3 incompatibility levels x 3 valence levels, within-subject, policy count fixed).

Two estimates are produced for each of two effects:
  (A) main effect of incompatibility  — linear trend over I1 < I2 < I3 (weights -1, 0, +1)
  (B) incompatibility x valence        — difference in that trend between valenced
                                         (mean of negative, positive) and neutral content
Analytic route:   per-participant contrast score -> one-sample t (paired t), noncentral t power.
Simulation route: trial-level linear mixed model on the continuous report-independent
                  access index (decoded evidence for 'seen', logit scale, standardised),
                  participant random intercept + random slope for the tested contrast,
                  Wald z on the fixed effect; power = P(|z| > 1.96).
The trial-level model makes the participant-level dz depend on trials per cell:
  Var(contrast_i) = sigma_slope^2 + sigma_e^2 * sum(w^2)/n_trials_per_cell
so the simulation reports N participants needed at several trial counts.

alpha = 0.05 two-sided, target power = 0.90.

Effect-size anchors (verified this session, see section9_worked_condition_en.md):
  Morsella, Gray, Krieger & Bargh 2009 (Emotion): incompatible vs compatible skeletomotor
     intentions, t(13) = 6.21 -> dz ~ 1.66 on *report-based* urge ratings. Report-based and
     therefore an upper bound; not adopted.
  Konstantinou & Lavie 2013 (JEP:HPP): VSTM load reduces masked detection d',
     t(15) = 3.29, d = 0.62; t(7) = 2.38, d = 0.86. A load (not conflict) effect on a
     criterion-free detection measure; the nearest published effect of a held task-set on visibility.
  Al et al. 2020 (PNAS, N = 37): cardiac phase on somatosensory detection, t(36) = -3.95 -> dz ~ 0.65;
     prestimulus HEP -> criterion, F(2,36) = 10.3. The nearest quantitative autonomic-cortical
     effect on detection; Park et al. 2014 (Nat Neurosci) reported the visual analogue with the
     opposite sign (full text not accessible this session; magnitude taken from Al et al. 2020).
  Coll et al. 2021 (NBR meta-analysis): HEP effects g = 0.37-0.39 for attention/interoceptive
     performance, g = 0.72 for arousal — the scale of HEP-related within-subject effects.
Planning values: 'medium' dz = 0.40 for the trend (about two-thirds of the published
  load/cardiac detection effects, since matching and no-report measurement remove variance
  those studies retained); 'small' dz = 0.25. For the interaction, a contrast of contrasts,
  'medium' dz = 0.30 and 'small' dz = 0.20.
"""
import sys, json, itertools, warnings
import numpy as np, pandas as pd
from scipy import stats, optimize

ALPHA, POWER = 0.05, 0.90
RNG = np.random.default_rng(20260924)

# ---------------------------------------------------------------- analytic
def power_paired_t(n, dz, alpha=ALPHA):
    df = n - 1
    tc = stats.t.ppf(1 - alpha / 2, df)
    nc = dz * np.sqrt(n)
    upper = stats.nct.sf(tc, df, nc); lower = stats.nct.cdf(-tc, df, nc)
    return float(np.nan_to_num(upper) + np.nan_to_num(lower))

def n_for_power(dz, power=POWER, alpha=ALPHA):
    n = 4
    while power_paired_t(n, dz, alpha) < power:
        n += 1
    return n

# ---------------------------------------------------------------- simulation
W_INC = np.array([-1.0, 0.0, 1.0])          # linear trend over incompatibility
W_VAL = np.array([0.5, -1.0, 0.5])          # valenced (neg,pos) minus neutral
SIGMA_E = 1.0                               # trial-level SD of the standardised access index
K_TRIALS_REF = 64                           # trials per cell at which dz is defined

def sigma_slope_from_dz(beta, dz, n_trials, w_sq_sum):
    """Choose the random-slope SD so that participant-level dz equals `dz` at n_trials/cell."""
    var_total = (beta / dz) ** 2
    var_meas = SIGMA_E ** 2 * w_sq_sum / n_trials
    return np.sqrt(max(var_total - var_meas, 1e-6))

def simulate_dataset(n_sub, n_trials, beta_inc, beta_int, sd_inc, sd_int):
    """Trial-level data: 3 x 3 cells, n_trials per cell, per participant."""
    cells = np.array(list(itertools.product(range(3), range(3))))   # (inc, val)
    inc_code = W_INC[cells[:, 0]]
    val_code = W_VAL[cells[:, 1]]
    rows = []
    for s in range(n_sub):
        u0 = RNG.normal(0, 0.5)
        b_inc = beta_inc + RNG.normal(0, sd_inc)
        b_int = beta_int + RNG.normal(0, sd_int)
        mu = u0 + b_inc * inc_code + b_int * inc_code * val_code
        y = np.repeat(mu, n_trials) + RNG.normal(0, SIGMA_E, 9 * n_trials)
        rows.append(pd.DataFrame({"subj": s, "inc": np.repeat(inc_code, n_trials),
                                  "val": np.repeat(val_code, n_trials), "y": y}))
    return pd.concat(rows, ignore_index=True)

def fit_mixed(df, effect):
    import statsmodels.formula.api as smf
    df = df.copy(); df["ix"] = df["inc"] * df["val"]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = smf.mixedlm("y ~ inc + val + ix", df, groups=df["subj"],
                        re_formula="~ inc + ix").fit(method="lbfgs", reml=True, maxiter=200)
    z = m.tvalues["inc" if effect == "main" else "ix"]
    return abs(z) > stats.norm.ppf(1 - ALPHA / 2)

def two_stage(df, effect):
    """Per-participant OLS contrast -> one-sample t (the balanced-design equivalent)."""
    df = df.copy(); df["ix"] = df["inc"] * df["val"]
    col = "inc" if effect == "main" else "ix"
    est = []
    for _, g in df.groupby("subj"):
        X = np.column_stack([np.ones(len(g)), g["inc"], g["val"], g["ix"]])
        b = np.linalg.lstsq(X, g["y"].values, rcond=None)[0]
        est.append(b[1] if col == "inc" else b[3])
    t, p = stats.ttest_1samp(est, 0)
    return p < ALPHA

BETA_TRIAL = 0.10   # fixed slope in trial-level SD units per unit of the contrast code
                    # (a shift of ~0.1 SD in decoded access evidence per incompatibility level)

def sim_power(n_sub, n_trials, effect, dz, n_sims, use_mixed):
    """dz is defined at K_TRIALS_REF trials per cell; the per-participant OLS coefficient on an
    orthogonal cell-coded regressor x has sampling variance sigma_e^2 / (n_trials * sum_c x_c^2)."""
    sum_x2 = {"main": float(np.sum(np.tile(W_INC, 3) ** 2)),                       # = 6
              "int": float(np.sum((W_INC[:, None] * W_VAL[None, :]) ** 2))}[effect]  # = 3
    sd_tested = sigma_slope_from_dz(BETA_TRIAL, dz, K_TRIALS_REF, 1.0 / sum_x2)
    if effect == "main":
        beta_inc, beta_int, sd_inc, sd_int = BETA_TRIAL, 0.0, sd_tested, 0.05
    else:
        beta_inc, beta_int, sd_inc, sd_int = BETA_TRIAL, BETA_TRIAL, 0.15, sd_tested
    hits = 0
    for _ in range(n_sims):
        df = simulate_dataset(n_sub, n_trials, beta_inc, beta_int, sd_inc, sd_int)
        hits += fit_mixed(df, effect) if use_mixed else two_stage(df, effect)
    return hits / n_sims

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "analytic"
    scenarios = [("main", "small", 0.25), ("main", "medium", 0.40),
                 ("int", "small", 0.20), ("int", "medium", 0.30)]
    if mode == "analytic":
        rows = []
        for eff, lab, dz in scenarios:
            for pw in (0.80, 0.90):
                rows.append(dict(effect=eff, assumption=lab, dz=dz, method="analytic_paired_t",
                                 alpha=ALPHA, target_power=pw, n_participants=n_for_power(dz, pw),
                                 trials_per_cell=np.nan, achieved_power=np.nan))
        pd.DataFrame(rows).to_csv("handoff/power_analytic.csv", index=False)
        print(pd.DataFrame(rows)[["effect", "assumption", "dz", "target_power", "n_participants"]].to_string(index=False))
    elif mode == "twostage":
        # Vectorised trial-level simulation of the two-stage estimator (per-participant OLS on
        # orthogonal cell codes -> one-sample t). Identical estimator to two_stage(), 100x faster.
        n_sims = 2000
        x_inc = np.repeat(W_INC, 3); x_val = np.tile(W_VAL, 3); x_ix = x_inc * x_val   # 9 cells, (inc, val)
        rows = []
        for eff, lab, dz in scenarios:
            x = x_inc if eff == "main" else x_ix
            sum_x2 = float(np.sum(x ** 2))
            sd_tested = sigma_slope_from_dz(BETA_TRIAL, dz, K_TRIALS_REF, 1.0 / sum_x2)
            for n_trials in (16, 32, 48, 64, 96):
                for n_sub in range(20, 361, 10):
                    b = BETA_TRIAL + RNG.normal(0, sd_tested, (n_sims, n_sub, 1))         # true slopes
                    cell_mu = b * x[None, None, :]                                          # (sims, sub, 9)
                    cell_mean = cell_mu + RNG.normal(0, SIGMA_E / np.sqrt(n_trials), cell_mu.shape)
                    est = (cell_mean * x[None, None, :]).sum(-1) / sum_x2                   # OLS coefficient
                    t = est.mean(1) / (est.std(1, ddof=1) / np.sqrt(n_sub))
                    p = float(np.mean(np.abs(t) > stats.t.ppf(1 - ALPHA / 2, n_sub - 1)))
                    rows.append(dict(effect=eff, assumption=lab, dz=dz, method="simulation_two_stage",
                                     alpha=ALPHA, n_participants=n_sub, trials_per_cell=n_trials, power=p, n_sims=n_sims))
                    if p >= 0.97: break
        pd.DataFrame(rows).to_csv("handoff/power_twostage.csv", index=False)
        print(len(rows))
    elif mode == "mixed":
        # coarse grid; sharded across independent processes:  python section9_power.py mixed N_SIMS SHARD N_SHARDS
        import zlib
        n_sims = int(sys.argv[2]) if len(sys.argv) > 2 else 200
        shard, n_shards = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, 1)
        n_grid = {("main", "medium"): (40, 50, 60, 70, 80, 100),
                  ("main", "small"): (100, 130, 150, 170, 190, 220),
                  ("int", "medium"): (60, 80, 100, 120, 140, 170),
                  ("int", "small"): (150, 190, 230, 265, 300, 340)}
        grid = [(eff, lab, dz, n_trials, n_sub) for eff, lab, dz in scenarios
                for n_trials in (32, 64) for n_sub in n_grid[(eff, lab)]]
        rows = []
        for i, cfg in enumerate(grid):
            if i % n_shards != shard:
                continue
            eff, lab, dz, n_trials, n_sub = cfg
            RNG = np.random.default_rng(zlib.crc32(repr(cfg).encode()))
            p = sim_power(n_sub, n_trials, eff, dz, n_sims, use_mixed=True)
            rows.append(dict(effect=eff, assumption=lab, dz=dz, method="simulation_mixed_model",
                             alpha=ALPHA, n_participants=n_sub, trials_per_cell=n_trials, power=p, n_sims=n_sims))
            pd.DataFrame(rows).to_csv(f"handoff/power_mixed_{shard:02d}.csv", index=False)
        print(shard, len(rows))
    elif mode == "assemble":
        import glob
        # --- TOST equivalence power (true effect 0, bounds +/- delta), paired design
        def power_tost(n, delta, alpha=ALPHA):
            df = n - 1; tc = stats.t.ppf(1 - alpha, df); nc = delta * np.sqrt(n)
            # both one-sided tests reject when |t| < nc - tc approximately -> use exact via nct
            # P(t > -nc + tc  and  t < nc - tc) where t ~ central t (true effect 0)
            crit = nc - tc
            return max(0.0, stats.t.cdf(crit, df) - stats.t.cdf(-crit, df))
        def n_tost(delta, power=POWER):
            n = 4
            while power_tost(n, delta) < power: n += 1
            return n
        rows = []
        an = pd.read_csv("handoff/power_analytic.csv")
        an["power"] = an["target_power"]; an["n_sims"] = np.nan
        rows.append(an[["effect", "assumption", "dz", "method", "alpha", "n_participants", "trials_per_cell", "power", "n_sims"]])
        ts = pd.read_csv("handoff/power_twostage.csv")
        # keep only the smallest N reaching 0.9 per (effect, assumption, trials) plus the full curve at 64 trials
        keep = ts[(ts.power >= 0.9)].groupby(["effect", "assumption", "trials_per_cell"]).head(1)
        keep = keep.assign(method="simulation_two_stage_N90")
        rows += [keep[["effect", "assumption", "dz", "method", "alpha", "n_participants", "trials_per_cell", "power", "n_sims"]],
                 ts[ts.trials_per_cell == 64][["effect", "assumption", "dz", "method", "alpha", "n_participants", "trials_per_cell", "power", "n_sims"]]]
        mx = pd.concat([pd.read_csv(f) for f in glob.glob("handoff/power_mixed_*.csv")])
        rows.append(mx[["effect", "assumption", "dz", "method", "alpha", "n_participants", "trials_per_cell", "power", "n_sims"]])
        extra = []
        for delta in (0.25, 0.30, 0.35):
            extra.append(dict(effect="main", assumption=f"equivalence_bound_dz{delta}", dz=delta, method="analytic_TOST_paired",
                              alpha=ALPHA, n_participants=n_tost(delta), trials_per_cell=np.nan, power=POWER, n_sims=np.nan))
        for N in (68, 120, 150):
            mdes = optimize.brentq(lambda d: power_paired_t(N, d) - POWER, 0.05, 0.8)
            extra.append(dict(effect="main_or_int", assumption=f"minimum_detectable_dz_at_N{N}", dz=round(mdes, 3),
                              method="analytic_paired_t_MDES", alpha=ALPHA, n_participants=N, trials_per_cell=np.nan, power=POWER, n_sims=np.nan))
            extra.append(dict(effect="main", assumption=f"TOST_power_at_N{N}_bound_dz0.30", dz=0.30, method="analytic_TOST_paired",
                              alpha=ALPHA, n_participants=N, trials_per_cell=np.nan, power=round(power_tost(N, 0.30), 3), n_sims=np.nan))
        rows.append(pd.DataFrame(extra))
        out = pd.concat(rows, ignore_index=True)
        out.to_csv("section9_power.csv", index=False)
        print(out[out.method.isin(["analytic_paired_t", "simulation_two_stage_N90", "analytic_TOST_paired", "analytic_paired_t_MDES"])].to_string(index=False))
        m90 = mx[mx.power >= 0.9].groupby(["effect", "assumption", "trials_per_cell"]).n_participants.min()
        print("\nmixed-model smallest N in grid with power>=0.9:\n", m90)
    elif mode == "time":
        import time
        df = simulate_dataset(100, 64, 0.3, 0.0, 0.5, 0.1)
        t0 = time.time(); r = fit_mixed(df, "main"); print("rows", len(df), "sec", round(time.time() - t0, 2), r)
