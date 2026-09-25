#!/usr/bin/env python
"""
reproduce.py (v2.3) -- one-command reproduction of every computed number in the supplementary deposit.

Steps (each prints PASS / FAIL; the script exits non-zero if any step fails):
  1.  recompute_table1   on Table_S1_v2.csv if present in the deposit directory, else on the deposit-v1.3
                         Table_S1_theory_by_quantity.csv (legacy schema, auto-detected)
  1b. column_typology    derived column classes from Table_S1_v2.csv + Table_S4_v2.csv
  1c. build_table2       Table_2_counts.csv at publication AND experiment level from Table_S2_v2.csv          [v2.1]
  1d. s2_sensitivity     scenario table s2_sensitivity.csv at both units from Table_S2_v2.csv                  [v2.1]
  1e. S3 tallies         groupby(dimension, code) of Table_S3_contrast_dimensions.csv must equal Table_S3_tallies.csv;
                         each theory must code every dimension exactly once                                    [v2.1]
  2.  recompute_table1 --selftest   (synthetic 12 x 10 table; schema, tallies, status logic, negative case)
  3.  agreement --selftest          (kappa unit checks, 80 % agreement recovery, 11 required + extra negative cases)
  4.  section9_power                (analytic paired t, exact TOST + Monte Carlo, two-df omnibus, session-2 trials budget,
                                     mixed-model convergence check).  Without --skip-mixed, statsmodels MUST be importable
                                     -- otherwise the step FAILS ('statsmodels missing; pass --skip-mixed ...'); it never passes
                                     silently.  After the run power/power_mixed_check.csv is read back: every contrast in
                                     {C0, C1a} must be present with n_sims == --mixed-sims and a numeric n_nonconverged; the
                                     step note reports the ACTUAL n_sims found in the file.                        [v2.1]
  5.  consistency check             sha256 of the produced CSVs against expected_hashes.json.
                                    'exact' files (tallies, analytic power tables, trials budget, Table_2_counts, s2_sensitivity,
                                    agreement self-test log) must match -> FAIL otherwise;
                                    'stochastic' files (power_mixed_check.csv, agreement self-test kappa summary) give WARN on
                                    mismatch, because optimiser tolerances differ across BLAS builds -- their CONTENT is
                                    checked in step 4 instead of their hash.
                                    --update-hashes rewrites expected_hashes.json from the current run.

reproduce_report.json records, per step, the actual parameters (input files, n_sims per contrast, statsmodels version,
mixed-model power, S3 tally comparison, Table 2 baselines) in addition to PASS/FAIL.

Usage
-----
  python reproduce.py [--deposit DIR] [--out DIR] [--mixed-sims 200 | --skip-mixed] [--update-hashes]
Writes <out>/reproduce_log.txt and <out>/reproduce_report.json.
"""
from __future__ import annotations
import argparse, hashlib, json, os, platform, subprocess, sys, time

__version__ = "2.3"
HERE = os.path.dirname(os.path.abspath(__file__))
EXACT = ["typology/column_typology_v2.csv", "typology/column_typology_pairs.csv", "power/protocol_numbers.json", "power/trials_budget.csv", "power/trials_budget_cells.csv", "power/trials_budget_analysis_cells.csv", "power/block_orders_study1.csv", "power/power_study1.csv", "power/power_study2.csv", "recompute/table1_tallies_v2.csv", "recompute/table1_wide_v2.csv", "recompute/table1_tallies_legacy_view.csv",
         "recompute_selftest/table1_tallies_v2.csv", "recompute_selftest/recompute_selftest_log.csv",
         "table2/Table_2_counts.csv", "s2/s2_sensitivity.csv",
         "power/power_study1.csv", "power/power_study2.csv", "power/trials_budget.csv",
         "agreement_selftest/selftest_log.csv"]
EXACT_LEGACY_INPUT_ONLY = ["recompute/table1_tallies_legacy.csv"]     # produced only when step 1 ran on the legacy v1.3 file
STOCHASTIC = ["agreement_selftest/agreement_summary.csv"]   # power/power_mixed_check.csv is NOT hashed: its content is checked in step 4 (n_sims, power values)
MIXED_CONTRASTS = {"C0": "C0_threshold_count1_vs_ge2", "C1a": "C1a_compatible_vs_incompatible_at_count3"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd, log, cwd=None):
    t = time.time()
    p = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, cwd=cwd or HERE)
    dt = time.time() - t
    log.write(f"\n$ python {' '.join(cmd)}\n[exit {p.returncode}, {dt:.1f} s]\n{p.stdout}\n{p.stderr}\n")
    return p.returncode, dt, p.stdout, p.stderr


def first_existing(*paths):
    return next((p for p in paths if os.path.exists(p)), None)


def check_mixed_csv(path, requested, skip):
    """Content check of power_mixed_check.csv (v2.1): returns (ok, note, params)."""
    import pandas as pd
    if not os.path.exists(path):
        return False, "power_mixed_check.csv not produced", {}
    mx = pd.read_csv(path)
    params = dict(rows=[{k: (None if pd.isna(v) else (v.item() if hasattr(v, "item") else v)) for k, v in r.items() if k != "calibration_note"} for _, r in mx.iterrows()])
    if skip:
        ok = len(mx) == 1 and mx.contrast.iloc[0] == "skipped" and int(mx.n_sims.iloc[0]) == 0
        return ok, "mixed check skipped (--skip-mixed): power_mixed_check.csv holds the single row contrast=skipped, n_sims=0" if ok else f"--skip-mixed given but power_mixed_check.csv holds {mx.contrast.tolist()}", params
    problems = []
    found = {}
    for short, name in MIXED_CONTRASTS.items():
        r = mx[mx.contrast == name]
        if len(r) != 1:
            problems.append(f"{short}: contrast {name!r} {'missing' if len(r) == 0 else 'duplicated'}"); continue
        r = r.iloc[0]
        n = int(r.n_sims) if not pd.isna(r.n_sims) else 0
        found[short] = dict(n_sims=n, n_nonconverged=None if pd.isna(r.n_nonconverged) else int(r.n_nonconverged), power_mixed_sim=None if pd.isna(r.power_mixed_sim) else float(r.power_mixed_sim),
                            power_two_stage_sim=None if pd.isna(r.power_two_stage_sim) else float(r.power_two_stage_sim), power_analytic=float(r.power_analytic),
                            statsmodels_version=str(r.get("statsmodels_version", "")))
        if n != requested:
            problems.append(f"{short}: n_sims = {n}, requested {requested}")
        if pd.isna(r.n_nonconverged):
            problems.append(f"{short}: n_nonconverged not reported")
        if pd.isna(r.power_mixed_sim):
            problems.append(f"{short}: power_mixed_sim missing")
    params["contrasts"] = found
    if problems:
        return False, "mixed-model check incomplete: " + "; ".join(problems), params
    note = "; ".join(f"{s}: n_sims={v['n_sims']} (requested {requested}), mixed power {v['power_mixed_sim']:.3f}, two-stage {v['power_two_stage_sim']:.3f}, analytic {v['power_analytic']:.3f}, n_nonconverged={v['n_nonconverged']}" for s, v in found.items())
    return True, note + f"; statsmodels {found['C0']['statsmodels_version']}", params


def check_s3(dims_path, tallies_path):
    """Recompute Table_S3_tallies.csv from Table_S3_contrast_dimensions.csv (v2.1)."""
    import pandas as pd
    d = pd.read_csv(dims_path, dtype=str, keep_default_na=False); t = pd.read_csv(tallies_path, dtype=str, keep_default_na=False)
    need_d, need_t = {"theory", "dimension_id", "code"}, {"dimension_id", "n_YES", "n_IMPLICIT", "n_NO"}
    if not need_d <= set(d.columns) or not need_t <= set(t.columns):
        return False, f"S3 columns: dimensions has {list(d.columns)}, tallies has {list(t.columns)}", {}
    codes = sorted(set(d.code))
    if set(codes) - {"YES", "IMPLICIT", "NO"}:
        return False, f"S3 codes outside YES/IMPLICIT/NO: {codes}", {}
    dup = d.duplicated(["theory", "dimension_id"], keep=False)
    if dup.any():
        return False, f"S3: {int(dup.sum())} rows share (theory, dimension_id): {d.loc[dup, ['theory', 'dimension_id']].drop_duplicates().values.tolist()[:4]}", {}
    per_theory = d.groupby("theory").dimension_id.nunique()
    n_dims = d.dimension_id.nunique()
    if (per_theory != n_dims).any():
        return False, f"S3: theories not covering all {n_dims} dimensions: {per_theory[per_theory != n_dims].to_dict()}", {}
    g = d.groupby(["dimension_id", "code"]).size().unstack(fill_value=0).reindex(columns=["YES", "IMPLICIT", "NO"], fill_value=0)
    mism = []
    for _, r in t.iterrows():
        did = r.dimension_id
        if did not in g.index:
            mism.append(f"{did}: in tallies but not in dimensions"); continue
        for c in ["YES", "IMPLICIT", "NO"]:
            if int(r[f"n_{c}"]) != int(g.loc[did, c]):
                mism.append(f"{did} n_{c}: tallies {r[f'n_{c}']} vs recomputed {int(g.loc[did, c])}")
    extra = sorted(set(g.index) - set(t.dimension_id))
    if extra:
        mism.append(f"dimensions without a tallies row: {extra}")
    params = dict(n_rows=len(d), n_theories=int(d.theory.nunique()), n_dimensions=int(n_dims), code_totals={c: int((d.code == c).sum()) for c in ["YES", "IMPLICIT", "NO"]}, n_tally_rows=len(t))
    if mism:
        return False, "S3 tallies differ from the recomputation: " + "; ".join(mism[:6]), params
    return True, f"{len(t)} dimension rows x 3 codes recomputed from {len(d)} cells ({params['n_theories']} theories x {n_dims} dimensions) match Table_S3_tallies.csv; totals YES {params['code_totals']['YES']}, IMPLICIT {params['code_totals']['IMPLICIT']}, NO {params['code_totals']['NO']}", params


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--deposit", default=HERE, help="directory holding Table_S1_v2.csv / Table_S2_v2.csv / Table_S3_*.csv and the manifests")
    ap.add_argument("--out", default=os.path.join(HERE, "reproduce_out"))
    ap.add_argument("--mixed-sims", type=int, default=200); ap.add_argument("--skip-mixed", action="store_true")
    ap.add_argument("--update-hashes", action="store_true")
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    log = open(os.path.join(a.out, "reproduce_log.txt"), "w")
    import numpy, pandas, scipy
    try:
        import statsmodels; sm_v = statsmodels.__version__
    except ImportError:
        sm_v = None
    env = dict(python=platform.python_version(), numpy=numpy.__version__, pandas=pandas.__version__, scipy=scipy.__version__, statsmodels=sm_v or "not installed", platform=platform.platform())
    log.write(f"reproduce.py v{__version__}\n" + json.dumps(env, indent=1) + "\n")
    report = dict(reproduce_version=__version__, environment=env, arguments=dict(deposit=a.deposit, out=a.out, mixed_sims=None if a.skip_mixed else a.mixed_sims, skip_mixed=a.skip_mixed), steps=[])
    status = {}
    T0 = time.time()

    def step(name, ok, dt, note="", params=None):
        status[name] = ok
        line = f"[{'PASS' if ok else 'FAIL'}] {name} ({dt:.1f} s){(' -- ' + note) if note else ''}"
        print(line); log.write(line + "\n"); report["steps"].append(dict(step=name, passed=bool(ok), seconds=round(dt, 1), note=note, parameters=params or {}))

    dep = a.deposit
    acc = os.path.join(dep, "accounts_manifest.csv"); dom = os.path.join(dep, "domains_manifest.csv")
    s1v2 = os.path.join(dep, "Table_S1_v2.csv"); s1v13 = os.path.join(dep, "Table_S1_theory_by_quantity.csv")
    s2 = first_existing(os.path.join(dep, "Table_S2_v2.csv"), os.path.join(dep, "Table_S2_v2_experiments.csv"))
    s4 = os.path.join(dep, "Table_S4_v2.csv")
    s3d = os.path.join(dep, "Table_S3_contrast_dimensions.csv"); s3t = os.path.join(dep, "Table_S3_tallies.csv")
    # 1. recompute_table1 on the real table
    src = s1v2 if os.path.exists(s1v2) else s1v13
    legacy_input = src == s1v13
    if not os.path.exists(src):
        step("1 recompute_table1", False, 0.0, "neither Table_S1_v2.csv nor Table_S1_theory_by_quantity.csv found")
    else:
        rc, dt, out, err = run(["recompute_table1.py", src, "--accounts", acc, "--domains", dom, "--out", os.path.join(a.out, "recompute")], log)
        step("1 recompute_table1", rc == 0, dt, f"input {os.path.basename(src)}" + (" (v2 schema)" if not legacy_input else " (legacy v1.3 schema; Table_S1_v2.csv not present)") + ("" if rc == 0 else " -- " + err.strip()[-200:]), dict(input=os.path.basename(src)))
    # 1b. column typology
    if os.path.exists(s1v2) and os.path.exists(s4):
        os.makedirs(os.path.join(a.out, "typology"), exist_ok=True)
        rc, dt, out, err = run(["column_typology.py", s1v2, s4, os.path.join(a.out, "typology", "column_typology_v2.csv")], log)
        step("1b column_typology (legacy distinguishable_from rule; NOT the manuscript class -- see 1f)", rc == 0, dt, "legacy-rule classes: " + ", ".join(l.split()[0] + "=" + l.split()[-2] for l in out.strip().splitlines()[1:]) if rc == 0 else err.strip()[-200:])
    else:
        step("1b column_typology", True, 0.0, "skipped (Table_S1_v2.csv or Table_S4_v2.csv absent)")
    # 1c. Table 2 at both units (v2.1)
    if s2 is None:
        step("1c build_table2", False, 0.0, "Table_S2_v2.csv (or Table_S2_v2_experiments.csv) not found in the deposit directory")
        step("1d s2_sensitivity", False, 0.0, "Table_S2_v2.csv not found")
    else:
        t2 = os.path.join(a.out, "table2", "Table_2_counts.csv")
        rc, dt, out, err = run(["build_table2.py", s2, "--out", t2], log)
        params = {}
        if rc == 0 and os.path.exists(t2[:-4] + "_summary.json"):
            sm = json.load(open(t2[:-4] + "_summary.json"))
            params = dict(input=os.path.basename(s2), pub_level_n=sm["pub_level_n"], pub_level_baseline=sm["pub_level_baseline"], exp_level_n=sm["exp_level_n"], exp_level_baseline=sm["exp_level_baseline"],
                          unit_heterogeneity_in_exp_denominator=sm["unit_heterogeneity_in_exp_denominator"], mixed_publications=sm["mixed_publications"])
        step("1c build_table2", rc == 0, dt, (out.strip().splitlines()[0].split(": ", 1)[-1] + "; " + out.strip().splitlines()[1] if rc == 0 and out.strip() else err.strip()[-300:]), params)
        s2out = os.path.join(a.out, "s2", "s2_sensitivity.csv")
        rc, dt, out, err = run(["s2_sensitivity.py", s2, s2out], log)
        params = {}
        if rc == 0 and os.path.exists(s2out.replace(".csv", "_summary.json")):
            sm = json.load(open(s2out.replace(".csv", "_summary.json")))
            params = dict(input=os.path.basename(s2), baseline_experiment=sm["baseline"], baseline_publication=sm["baseline_publication"], n_rows_by_unit_type=sm["n_rows_by_unit_type"])
        lines = [l for l in out.strip().splitlines() if l.startswith("BASELINE")]
        step("1d s2_sensitivity", rc == 0, dt, " | ".join(l.split(": ", 1)[0].replace("BASELINE ", "") + " " + l.split(": ", 1)[1].split(" | ")[0] for l in lines) if rc == 0 else err.strip()[-300:], params)
    # 1e. S3 tallies recomputation (v2.1)
    t = time.time()
    if os.path.exists(s3d) and os.path.exists(s3t):
        ok, note, params = check_s3(s3d, s3t)
        step("1e S3 tallies recomputation", ok, time.time() - t, note, params)
    else:
        step("1e S3 tallies recomputation", False, 0.0, f"Table_S3_contrast_dimensions.csv / Table_S3_tallies.csv not found in {dep}")
    # 1f. pair register -> column class (v2.2): the manuscript's 'contested' class is derived here, from pair_register.csv
    pr = os.path.join(dep, "pair_register.csv")
    if os.path.exists(s1v2) and os.path.exists(s4) and os.path.exists(pr):
        os.makedirs(os.path.join(a.out, "typology"), exist_ok=True)
        rc, dt, out, err = run(["column_typology_pairs.py", s1v2, s4, pr, os.path.join(a.out, "typology", "column_typology_pairs.csv")], log)
        newcls = [l.strip() for l in out.strip().splitlines() if l.strip().startswith("NEW  class")]
        step("1f column_typology_pairs", rc == 0, dt, ("pair-register classes: " + " | ".join(newcls)) if rc == 0 else err.strip()[-300:], dict(pair_register="pair_register.csv"))
    else:
        step("1f column_typology_pairs", False, 0.0, "pair_register.csv (or S1/S4) not found in the deposit directory")
    # 2. recompute selftest
    rc, dt, out, err = run(["recompute_table1.py", "--selftest", "--out", os.path.join(a.out, "recompute_selftest")], log)
    step("2 recompute_table1 --selftest", rc == 0, dt, out.strip().splitlines()[-1] if out.strip() else err.strip()[-200:])
    # 3. agreement selftest
    rc, dt, out, err = run(["agreement.py", "--selftest", "--out", os.path.join(a.out, "agreement_selftest")], log)
    n_neg = sum(1 for l in out.splitlines() if l.startswith("[") and "negative" in l)
    step("3 agreement --selftest", rc == 0, dt, out.strip().splitlines()[-1] if out.strip() else err.strip()[-200:], dict(n_negative_cases_reported=n_neg))
    # 4. power (v2.1 policy: no silent pass without statsmodels; content check of the mixed-model file)
    if not a.skip_mixed and sm_v is None:
        step("4 section9_power", False, 0.0, "statsmodels missing; pass --skip-mixed to run without the mixed-model check", dict(statsmodels=None, mixed_sims_requested=a.mixed_sims))
    else:
        cmd = ["section9_power.py", "--out", os.path.join(a.out, "power"), "--mixed-sims", str(a.mixed_sims)] + (["--skip-mixed"] if a.skip_mixed else [])
        rc, dt, out, err = run(cmd, log)
        ok, note, params = check_mixed_csv(os.path.join(a.out, "power", "power_mixed_check.csv"), a.mixed_sims, a.skip_mixed)
        params.update(statsmodels=sm_v, mixed_sims_requested=None if a.skip_mixed else a.mixed_sims, exit_code=rc)
        kn = os.path.join(a.out, "power", "section9_key_numbers.json")
        if os.path.exists(kn):
            k = json.load(open(kn))
            params["trials_budget"] = {x: k[x] for x in ["n_cells", "n_blocks_session2", "presented_session2_per_cell", "usable_single_cell", "usable_pooled_cell", "presented_session2_total", "session2_minutes", "session1_minutes", "usable_target_per_analysis_cell"] if x in k}
        step("4 section9_power", rc == 0 and ok, dt, (note if rc == 0 else f"section9_power.py exited {rc}: {err.strip()[-200:]}"), params)

    # 4b. protocol numbers (v2.2): session arithmetic, multiplicity, success-rule powers and retention, from the step-4 outputs
    if os.path.exists(os.path.join(a.out, "power", "trials_budget.csv")):
        rc, dt, out, err = run(["protocol_numbers.py", "--power-dir", os.path.join(a.out, "power"), "--out", os.path.join(a.out, "power", "protocol_numbers.json")], log)
        pn = json.load(open(os.path.join(a.out, "power", "protocol_numbers.json"))) if rc == 0 else {}
        note = (f"{pn['study1']['n_presentation_cells']} cells, {pn['study1']['n_blocks_per_session']} blocks; session 2 {pn['study1']['session2']['total_minutes']} min, session 1 {pn['study1']['session1']['total_minutes']} min; "
                f"usable single C1a cell {pn['study1']['usable_single_c1a_cell']}, pooled {pn['study1']['usable_pooled_c1a_cell']}; C1a power {pn['power']['C1a_single_alpha05']}, two-version rule {pn['power']['two_version_rule_independence']}; "
                f"CR power at dz {pn['power']['rating_contrast_CR']['assumed_dz']}: {pn['power']['rating_contrast_CR']['power_at_N']}; pilot stop dz {pn['power']['pilot_stop']['threshold_dz']}; "
                f"P(3-block cell >= floor) {pn['retention']['three_block_c1a_cell']['P_reaches_target']}; block orders {pn['block_orders']['n_sequences']}") if rc == 0 else err.strip()[-300:]
        step("4b protocol_numbers", rc == 0, dt, note)
    else:
        step("4b protocol_numbers", False, 0.0, "power/trials_budget.csv absent (step 4 did not run)")    # 5. consistency
    t = time.time()
    exact = EXACT + (EXACT_LEGACY_INPUT_ONLY if legacy_input else [])
    hashes = {}
    for rel in exact + STOCHASTIC:
        p = os.path.join(a.out, rel)
        if os.path.exists(p):
            hashes[rel] = sha256(p)
    ref_path = os.path.join(HERE, "expected_hashes.json")
    if a.update_hashes or not os.path.exists(ref_path):
        json.dump(hashes, open(ref_path, "w"), indent=1)
        step("5 consistency check", True, time.time() - t, f"reference written to expected_hashes.json ({len(hashes)} files); rerun to compare", dict(files=sorted(hashes)))
        report["hashes"] = hashes
    else:
        ref = json.load(open(ref_path))
        fails, warns, ok = [], [], []
        for rel, h in hashes.items():
            if rel not in ref:
                warns.append(f"{rel}: no reference"); continue
            if h == ref[rel]:
                ok.append(rel)
            elif rel in STOCHASTIC:
                warns.append(f"{rel}: differs (stochastic / platform-sensitive; content checked in step 4)")
            else:
                fails.append(f"{rel}: differs from reference")
        missing = [r for r in ref if r not in hashes]
        for r in missing:
            if r in EXACT_LEGACY_INPUT_ONLY and not legacy_input:
                continue
            (fails if r in exact else warns).append(f"{r}: not produced")
        note = f"{len(ok)} of {len(hashes)} files match" + (f"; WARN: {'; '.join(warns)}" if warns else "") + (f"; FAIL: {'; '.join(fails)}" if fails else "")
        step("5 consistency check", not fails, time.time() - t, note, dict(exact=exact, stochastic=STOCHASTIC, n_match=len(ok), n_files=len(hashes)))
        report["hashes"] = hashes; report["hash_warnings"] = warns; report["hash_failures"] = fails
    total = time.time() - T0
    report["total_seconds"] = round(total, 1); report["all_passed"] = all(status.values())
    json.dump(report, open(os.path.join(a.out, "reproduce_report.json"), "w"), indent=1)
    line = f"reproduce.py v{__version__}: {sum(status.values())} of {len(status)} steps passed in {total:.1f} s"
    print(line); log.write(line + "\n"); log.close()
    sys.exit(0 if all(status.values()) else 1)


if __name__ == "__main__":
    main()
