#!/usr/bin/env python
"""
reproduce.py (v2.0) -- one-command reproduction of every computed number in the supplementary deposit.

Steps (each prints PASS / FAIL; the script exits non-zero if any step fails):
  1. recompute_table1   on Table_S1_v2.csv if present in the deposit directory, else on the deposit-v1.3
                        Table_S1_theory_by_quantity.csv (legacy schema, auto-detected)
  2. recompute_table1 --selftest   (synthetic 12 x 10 table; schema, tallies, status logic, negative case)
  3. agreement --selftest          (kappa unit checks, 80 % agreement recovery, 6 required + 2 extra negative cases)
  4. section9_power                (analytic paired t, exact TOST + Monte Carlo, two-df omnibus, trials budget,
                                    mixed-model convergence check unless --skip-mixed)
  1b. column_typology      derived column classes from Table_S1_v2.csv + Table_S4_v2.csv
  5. consistency check             sha256 of the produced CSVs against expected_hashes.json.
                                   'exact' files (tallies, analytic power tables, trials budget) must match -> FAIL otherwise;
                                   'stochastic' files (mixed-model check, agreement self-test kappa) give WARN on mismatch,
                                   because optimiser tolerances differ across BLAS builds.
                                   --update-hashes rewrites expected_hashes.json from the current run.

Usage
-----
  python reproduce.py [--deposit DIR] [--out DIR] [--mixed-sims 200 | --skip-mixed] [--update-hashes]
Writes <out>/reproduce_log.txt and <out>/reproduce_report.json.
"""
from __future__ import annotations
import argparse, hashlib, json, os, platform, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
EXACT = ["typology/column_typology_v2.csv", "recompute/table1_tallies_v2.csv", "recompute/table1_wide_v2.csv", "recompute/table1_tallies_legacy_view.csv", "recompute/table1_tallies_legacy.csv",
         "recompute_selftest/table1_tallies_v2.csv", "recompute_selftest/recompute_selftest_log.csv",
         "power/power_study1.csv", "power/power_study2.csv", "power/trials_budget.csv",
         "agreement_selftest/selftest_log.csv"]
STOCHASTIC = ["power/power_mixed_check.csv", "agreement_selftest/agreement_summary.csv"]


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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--deposit", default=HERE, help="directory holding Table_S1_v2.csv / Table_S1_theory_by_quantity.csv and the manifests")
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
        sm_v = "not installed"
    env = dict(python=platform.python_version(), numpy=numpy.__version__, pandas=pandas.__version__, scipy=scipy.__version__, statsmodels=sm_v, platform=platform.platform())
    log.write("reproduce.py v2.0\n" + json.dumps(env, indent=1) + "\n")
    report = dict(environment=env, steps=[])
    status = {}
    T0 = time.time()

    def step(name, ok, dt, note=""):
        status[name] = ok
        line = f"[{'PASS' if ok else 'FAIL'}] {name} ({dt:.1f} s){(' -- ' + note) if note else ''}"
        print(line); log.write(line + "\n"); report["steps"].append(dict(step=name, passed=bool(ok), seconds=round(dt, 1), note=note))

    # 1. recompute_table1 on the real table
    acc = os.path.join(a.deposit, "accounts_manifest.csv"); dom = os.path.join(a.deposit, "domains_manifest.csv")
    s1v2 = os.path.join(a.deposit, "Table_S1_v2.csv"); s1v13 = os.path.join(a.deposit, "Table_S1_theory_by_quantity.csv")
    src = s1v2 if os.path.exists(s1v2) else s1v13
    if not os.path.exists(src):
        step("1 recompute_table1", False, 0.0, "neither Table_S1_v2.csv nor Table_S1_theory_by_quantity.csv found")
    else:
        rc, dt, out, err = run(["recompute_table1.py", src, "--accounts", acc, "--domains", dom, "--out", os.path.join(a.out, "recompute")], log)
        step("1 recompute_table1", rc == 0, dt, f"input {os.path.basename(src)}" + (" (v2 schema)" if src == s1v2 else " (legacy v1.3 schema; Table_S1_v2.csv not present)"))
    # 1b. column typology from Table_S1_v2 + Table_S4_v2 (class is derived, never typed)
    s4 = os.path.join(a.deposit, "Table_S4_v2.csv")
    if os.path.exists(s1v2) and os.path.exists(s4):
        os.makedirs(os.path.join(a.out, "typology"), exist_ok=True)
        rc, dt, out, err = run(["column_typology.py", s1v2, s4, os.path.join(a.out, "typology", "column_typology_v2.csv")], log)
        step("1b column_typology", rc == 0, dt, "derived classes: " + ", ".join(l.split()[0] + "=" + l.split()[-2] for l in out.strip().splitlines()[1:]) if rc == 0 else err.strip()[-200:])
    else:
        step("1b column_typology", True, 0.0, "skipped (Table_S1_v2.csv or Table_S4_v2.csv absent)")
    # 2. recompute selftest
    rc, dt, out, err = run(["recompute_table1.py", "--selftest", "--out", os.path.join(a.out, "recompute_selftest")], log)
    step("2 recompute_table1 --selftest", rc == 0, dt, out.strip().splitlines()[-1] if out.strip() else err.strip()[-200:])
    # 3. agreement selftest
    rc, dt, out, err = run(["agreement.py", "--selftest", "--out", os.path.join(a.out, "agreement_selftest")], log)
    step("3 agreement --selftest", rc == 0, dt, out.strip().splitlines()[-1] if out.strip() else err.strip()[-200:])
    # 4. power
    cmd = ["section9_power.py", "--out", os.path.join(a.out, "power"), "--mixed-sims", str(a.mixed_sims)] + (["--skip-mixed"] if a.skip_mixed else [])
    rc, dt, out, err = run(cmd, log)
    step("4 section9_power", rc == 0, dt, "mixed check skipped" if a.skip_mixed else f"{a.mixed_sims} mixed-model simulations per contrast")
    # 5. consistency
    t = time.time()
    hashes = {}
    for rel in EXACT + STOCHASTIC:
        p = os.path.join(a.out, rel)
        if os.path.exists(p):
            hashes[rel] = sha256(p)
    ref_path = os.path.join(HERE, "expected_hashes.json")
    if a.update_hashes or not os.path.exists(ref_path):
        json.dump(hashes, open(ref_path, "w"), indent=1)
        step("5 consistency check", True, time.time() - t, f"reference written to expected_hashes.json ({len(hashes)} files); rerun to compare")
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
                warns.append(f"{rel}: differs (stochastic / platform-sensitive)")
            else:
                fails.append(f"{rel}: differs from reference")
        missing = [r for r in ref if r not in hashes]
        for r in missing:
            (fails if r in EXACT else warns).append(f"{r}: not produced")
        note = f"{len(ok)} of {len(hashes)} files match" + (f"; WARN: {'; '.join(warns)}" if warns else "") + (f"; FAIL: {'; '.join(fails)}" if fails else "")
        step("5 consistency check", not fails, time.time() - t, note)
        report["hashes"] = hashes; report["hash_warnings"] = warns; report["hash_failures"] = fails
    total = time.time() - T0
    report["total_seconds"] = round(total, 1); report["all_passed"] = all(status.values())
    json.dump(report, open(os.path.join(a.out, "reproduce_report.json"), "w"), indent=1)
    line = f"reproduce.py: {sum(status.values())} of {len(status)} steps passed in {total:.1f} s"
    print(line); log.write(line + "\n"); log.close()
    sys.exit(0 if all(status.values()) else 1)


if __name__ == "__main__":
    main()
