#!/usr/bin/env python
"""
recompute_table1.py (v2.0) -- every Table 1 tally, recomputed from Table S1 itself.

Nothing in the manuscript prose is typed by hand: the CSV/JSON/Markdown written here are the only
sources for the column counts.  This script does NOT depend on theory_predictions_matrix.csv or
on the round-0 72-cell matrix; it reads the long-format Table S1 directly.

Usage
-----
  python recompute_table1.py Table_S1_v2.csv [--accounts accounts_manifest.csv] [--domains domains_manifest.csv] [--out out_dir]
  python recompute_table1.py Table_S1_theory_by_quantity.csv        # deposit v1.3 file, legacy schema (auto-detected)
  python recompute_table1.py --selftest [--out out_dir]

Input schema, v2 (long format; one row per theory x domain cell; auto-detected by the columns
`theory_id` and `domain_id`)
------------------------------------------------------------------------------------------------
  theory_id        key, must exist in accounts_manifest.csv (12 accounts: AST, FM, GNWT, HOT, HOSS, IIT, NSF, PFT, PP, RPT, SIT, UAL)
  domain_id        key, must exist in domains_manifest.csv (10 domains: M1, M2, M3, M4a, M4b, M4c, M5, M6, M7, M8)
  code             EXPLICIT | INTERPRETED | NOT_LOCATED | NOT_APPLICABLE | UNRESOLVED
  polarity         positive | stated_null | negative  -- required when code is EXPLICIT or INTERPRETED; empty otherwise
  relation         free text (e.g. effect / threshold / locus / sufficiency); carried through, not tallied
  source_label, source_doi, source_locus, evidence_status   -- source_doi required for EXPLICIT/INTERPRETED
  justification    one or two sentences
  origin           submitted-v1 | added-in-revision   (optional; else inferred from the manifest + M4a/b/c)
  legacy_code      YES | IMPLICIT | NO | YES (negative)  -- optional: the deposit-v1.3 code of the same cell, for the
                   88-cell legacy view; empty for cells that did not exist in v1.3
  legacy_domain_id optional: domain the legacy code belonged to (default = domain_id; e.g. 'M4' for the M4a/b/c split)
  row_class        trial-level | origin-level  -- optional in the file, always taken from the manifest if absent
Any other column is carried through untouched.  Codes and polarity are validated; duplicated keys,
unknown theory_id/domain_id, missing polarity on positive cells and missing DOI on positive cells abort.
The file is read with keep_default_na=False; the null polarity is spelled 'stated_null' because pandas treats the bare token 'null' as missing by default.

Input schema, legacy (deposit v1.3; auto-detected by `theory` + `quantity_id`)
-------------------------------------------------------------------------------
  theory, quantity_id, quantity, code (YES / IMPLICIT / NO / YES (negative)), prediction, citation_label,
  citation_doi, row_class.  Tallied as in v1.3 (Table_1_tallies.csv format) so that the deposited tallies
  can be reproduced bit-for-bit.

Outputs (in --out, default '.')
-------------------------------
  v2 input:      table1_tallies_v2.csv     long tally: scope (trial-level / origin-level / all rows) x domain_id x code (x polarity) -> n
                 table1_wide_v2.csv        one row per scope x domain: n_EXPLICIT_positive, n_EXPLICIT_null, n_EXPLICIT_negative,
                                           n_INTERPRETED_*, n_NOT_LOCATED, n_NOT_APPLICABLE, n_UNRESOLVED, n_cells, occupants
                 table1_markdown_v2.md     compact matrix (theories x domains) plus tally rows
                 table1_numbers_v2.json    all counts (for the prose), including column status descriptors computed from the codes
                 table1_tallies_legacy_view.csv   the legacy-code view of the cells carrying legacy_code (expected 88)
  legacy input:  table1_tallies_legacy.csv (= Table_1_tallies.csv format), table1_numbers_legacy.json

Column status (v2, computed -- never an input)
----------------------------------------------
For each domain, over trial-level accounts:
  n_explicit_pos      EXPLICIT cells with polarity positive or negative (a stated directional prediction)
  n_explicit_null     EXPLICIT cells with polarity stated_null (a stated prediction of no involvement)
  n_interpreted       INTERPRETED cells
  occupancy_summary   'no-EXPLICIT' | 'one-EXPLICIT' | 'multi-EXPLICIT-same-sign' | 'sign-disagreement'
                      (>= 2 EXPLICIT cells whose polarities disagree, or any UNRESOLVED cell).
                      This is an occupancy count, not the manuscript's column class. The class
                      (contested / single-occupant / occupied-not-contested / thin / unoccupied) is
                      derived by column_typology.py from Table S1 together with the distinguishable
                      prediction pairs in Table S4 — predictions can differ in locus, timing or
                      magnitude without differing in sign.
"""
from __future__ import annotations
import argparse, json, os, sys
import numpy as np
import pandas as pd

__version__ = "2.0"
V2_CODES = ["EXPLICIT", "INTERPRETED", "NOT_LOCATED", "NOT_APPLICABLE", "UNRESOLVED"]
V2_POSITIVE = {"EXPLICIT", "INTERPRETED"}
POLARITIES = ["positive", "stated_null", "negative"]
LEGACY_CODES = ["YES", "YES (negative)", "IMPLICIT", "NO"]
LEGACY_SHORT = {"YES": "YES", "YES (negative)": "YES(neg)", "IMPLICIT": "IMPLICIT", "NO": "NO"}
DEFAULT_ADDED_DOMAINS = ("M4a", "M4b", "M4c")
SYM_V2 = {"EXPLICIT:positive": "**E+**", "EXPLICIT:stated_null": "**E0**", "EXPLICIT:negative": "**E−**",
          "INTERPRETED:positive": "*i+*", "INTERPRETED:stated_null": "*i0*", "INTERPRETED:negative": "*i−*",
          "NOT_LOCATED": "·", "NOT_APPLICABLE": "n/a", "UNRESOLVED": "?"}


def read_csv_strict(path):
    return pd.read_csv(path, keep_default_na=False, na_values=[""])


def fail(msg):
    sys.exit("VALIDATION FAILED: " + msg)


def norm_code_v2(x):
    if pd.isna(x):
        return "MISSING"
    s = str(x).strip().upper().replace(" ", "_").replace("-", "_")
    return s if s in V2_CODES else "MISSING"


def norm_legacy(x):
    if pd.isna(x):
        return "MISSING"
    s = " ".join(str(x).strip().upper().split())
    if s in ("YES (NEGATIVE)", "YES(NEG)", "Y(NEG)", "YES(NEGATIVE)", "YES NEGATIVE"):
        return "YES (negative)"
    return s if s in ("YES", "IMPLICIT", "NO") else "MISSING"


# ---------------------------------------------------------------- v2
def load_v2(path, accounts, domains):
    df = read_csv_strict(path)
    acc = read_csv_strict(accounts); dom = read_csv_strict(domains)
    for c in ("theory_id", "domain_id", "code"):
        if c not in df.columns:
            fail(f"{path}: v2 schema needs column `{c}`; has {list(df.columns)}")
    df["theory_id"] = df.theory_id.astype(str).str.strip(); df["domain_id"] = df.domain_id.astype(str).str.strip()
    bad_t = sorted(set(df.theory_id) - set(acc.theory_id.astype(str)))
    if bad_t:
        fail(f"theory_id not in accounts manifest: {bad_t}")
    bad_d = sorted(set(df.domain_id) - set(dom.domain_id.astype(str)))
    if bad_d:
        fail(f"domain_id not in domains manifest: {bad_d}")
    dup = df.duplicated(["theory_id", "domain_id"], keep=False)
    if dup.any():
        fail(f"{int(dup.sum())} rows share a duplicated (theory_id, domain_id): {df.loc[dup, ['theory_id', 'domain_id']].drop_duplicates().values.tolist()[:5]}")
    df["code"] = df.code.map(norm_code_v2)
    if (df.code == "MISSING").any():
        fail(f"invalid or empty code in rows: {df.loc[df.code == 'MISSING', ['theory_id', 'domain_id']].values.tolist()[:5]} (valid: {V2_CODES})")
    df["polarity"] = df["polarity"].map(lambda x: "" if pd.isna(x) else str(x).strip().lower()) if "polarity" in df.columns else ""
    pos = df.code.isin(V2_POSITIVE)
    badp = pos & ~df.polarity.isin(POLARITIES)
    if badp.any():
        fail(f"EXPLICIT/INTERPRETED cells without a valid polarity: {df.loc[badp, ['theory_id', 'domain_id', 'code', 'polarity']].values.tolist()[:5]}")
    df.loc[~pos, "polarity"] = ""
    doi_col = next((c for c in ("source_doi", "citation_doi") if c in df.columns), None)
    if doi_col is None:
        fail("v2 file needs a `source_doi` column")
    nodoi = pos & df[doi_col].isna()
    if nodoi.any():
        fail(f"positive cells without a DOI: {df.loc[nodoi, ['theory_id', 'domain_id', 'code']].values.tolist()[:5]}")
    # manifest joins
    df = df.drop(columns=[c for c in ("row_class", "theory") if c in df.columns]).merge(acc[["theory_id", "theory", "row_class", "origin"]].rename(columns={"origin": "theory_origin"}), on="theory_id", how="left")
    df = df.merge(dom[["domain_id", "domain"]], on="domain_id", how="left")
    if "origin" not in df.columns:
        df["origin"] = np.where((df.theory_origin == "added-in-revision") | df.domain_id.isin(DEFAULT_ADDED_DOMAINS), "added-in-revision", "submitted-v1")
    df["code_pol"] = np.where(pos, df.code + ":" + df.polarity, df.code)
    # keep manifest order
    t_order = {t: i for i, t in enumerate(acc.theory_id)}; d_order = {d: i for i, d in enumerate(dom.domain_id)}
    df = df.assign(_t=df.theory_id.map(t_order), _d=df.domain_id.map(d_order)).sort_values(["_t", "_d"]).drop(columns=["_t", "_d"]).reset_index(drop=True)
    return df, acc, dom


def tally_v2(df, scope_name, dom_order):
    rows = []
    for d in dom_order:
        sub = df[df.domain_id == d]
        for code in V2_CODES:
            if code in V2_POSITIVE:
                for pol in POLARITIES:
                    rows.append(dict(scope=scope_name, domain_id=d, code=code, polarity=pol, n=int(((sub.code == code) & (sub.polarity == pol)).sum())))
            else:
                rows.append(dict(scope=scope_name, domain_id=d, code=code, polarity="", n=int((sub.code == code).sum())))
        rows.append(dict(scope=scope_name, domain_id=d, code="ALL", polarity="", n=int(len(sub))))
    return rows


def wide_v2(df, scope_name, dom_order):
    rows = []
    for d in dom_order:
        sub = df[df.domain_id == d]
        r = dict(scope=scope_name, domain_id=d)
        for code in V2_CODES:
            if code in V2_POSITIVE:
                for pol in POLARITIES:
                    r[f"n_{code}_{pol}"] = int(((sub.code == code) & (sub.polarity == pol)).sum())
            else:
                r[f"n_{code}"] = int((sub.code == code).sum())
        r["n_cells"] = int(len(sub))
        r["occupants_EXPLICIT"] = "; ".join(f"{t} ({p})" for t, p in sub[sub.code == "EXPLICIT"][["theory_id", "polarity"]].values)
        r["occupants_INTERPRETED"] = "; ".join(f"{t} ({p})" for t, p in sub[sub.code == "INTERPRETED"][["theory_id", "polarity"]].values)
        r["UNRESOLVED_theories"] = "; ".join(sub[sub.code == "UNRESOLVED"].theory_id)
        n_exp = int((sub.code == "EXPLICIT").sum())
        pols = set(sub[sub.code == "EXPLICIT"].polarity)
        directional = {"positive", "negative"} & pols
        # Occupancy summary ONLY (how many EXPLICIT cells, and whether their signs disagree).
        # The manuscript's column class is NOT this field: it is derived by column_typology.py from
        # Table S1 together with the distinguishable-prediction pairs of Table S4.
        if (sub.code == "UNRESOLVED").any() or (n_exp >= 2 and directional and "stated_null" in pols):
            status = "sign-disagreement"
        elif n_exp == 0:
            status = "no-EXPLICIT"
        elif n_exp == 1:
            status = "one-EXPLICIT"
        else:
            status = "multi-EXPLICIT-same-sign"
        r["occupancy_summary"] = status
        r["n_stated_or_interpreted_le2"] = bool(n_exp + int((sub.code == "INTERPRETED").sum()) <= 2)
        rows.append(r)
    return rows


def run_v2(path, accounts, domains, out):
    df, acc, dom = load_v2(path, accounts, domains)
    dom_order = list(dom.domain_id)
    trial = df[df.row_class == "trial-level"]; origin = df[df.row_class == "origin-level"]
    scopes = [("trial-level", trial), ("origin-level", origin), ("all rows", df),
              ("trial-level, submitted-v1 cells", trial[trial.origin == "submitted-v1"]),
              ("trial-level, added-in-revision cells", trial[trial.origin == "added-in-revision"])]
    tal = pd.DataFrame([r for name, d in scopes for r in tally_v2(d, name, dom_order)])
    wide = pd.DataFrame([r for name, d in scopes for r in wide_v2(d, name, dom_order)])
    tal.to_csv(os.path.join(out, "table1_tallies_v2.csv"), index=False)
    wide.to_csv(os.path.join(out, "table1_wide_v2.csv"), index=False)
    # legacy view
    legacy_view = None
    if "legacy_code" in df.columns:
        lv = df[df.legacy_code.notna() & (df.legacy_code.astype(str).str.strip() != "")].copy()
        lv["legacy_code"] = lv.legacy_code.map(norm_legacy)
        if (lv.legacy_code == "MISSING").any():
            fail(f"invalid legacy_code: {lv.loc[lv.legacy_code == 'MISSING', ['theory_id', 'domain_id']].values.tolist()[:5]}")
        lv["legacy_domain_id"] = lv["legacy_domain_id"].fillna(lv.domain_id) if "legacy_domain_id" in lv.columns else lv.domain_id
        rows = []
        for scope_name, d in [("trial-level", lv[lv.row_class == "trial-level"]), ("origin-level", lv[lv.row_class == "origin-level"]), ("all rows", lv)]:
            for q in sorted(d.legacy_domain_id.unique()):
                sub = d[d.legacy_domain_id == q]
                r = dict(scope=scope_name, quantity_id=q)
                for c in LEGACY_CODES:
                    r[LEGACY_SHORT[c]] = int((sub.legacy_code == c).sum())
                r["n"] = int(len(sub)); rows.append(r)
        legacy_view = pd.DataFrame(rows)
        legacy_view.to_csv(os.path.join(out, "table1_tallies_legacy_view.csv"), index=False)
        if len(lv) != 88:
            print(f"NOTE: legacy view covers {len(lv)} cells, not 88 (v1.3 deposit); reported as found.", file=sys.stderr)
    # markdown
    theories = list(acc[acc.row_class == "trial-level"].theory_id) + list(acc[acc.row_class == "origin-level"].theory_id)
    first_origin = next(iter(acc[acc.row_class == "origin-level"].theory_id), None)
    md = ["| Theory | " + " | ".join(dom_order) + " |", "|---|" + "---|" * len(dom_order)]
    for t in theories:
        sub = df[df.theory_id == t].set_index("domain_id").code_pol
        if t == first_origin:
            md.append("| *Origin-level accounts* |" + " |" * len(dom_order))
        md.append(f"| {acc.set_index('theory_id').loc[t, 'theory']} | " + " | ".join(SYM_V2.get(sub.get(d, ""), "–") for d in dom_order) + " |")

    def tally_line(label, scope_df):
        cells = []
        for d in dom_order:
            sub = scope_df[scope_df.domain_id == d]
            e_dir = int(((sub.code == "EXPLICIT") & sub.polarity.isin(["positive", "negative"])).sum())
            e_null = int(((sub.code == "EXPLICIT") & (sub.polarity == "stated_null")).sum())
            i_ = int((sub.code == "INTERPRETED").sum()); nl = int((sub.code == "NOT_LOCATED").sum())
            na = int((sub.code == "NOT_APPLICABLE").sum()); un = int((sub.code == "UNRESOLVED").sum())
            s = f"{e_dir} E"
            if e_null:
                s += f" / {e_null} E0"
            s += f" / {i_} i / {nl} ·"
            if na:
                s += f" / {na} n/a"
            if un:
                s += f" / {un} ?"
            cells.append(s)
        return f"| **{label}** | " + " | ".join(cells) + " |"
    md.append(tally_line(f"Tally, trial-level accounts (n = {trial.theory_id.nunique()})", trial))
    md.append(tally_line(f"Tally, all rows (n = {df.theory_id.nunique()})", df))
    md.append("")
    md.append("E = EXPLICIT with a directional polarity (E+ positive, E− negative); E0 = EXPLICIT null (stated no involvement); i = INTERPRETED; · = NOT_LOCATED; n/a = NOT_APPLICABLE; ? = UNRESOLVED.")
    open(os.path.join(out, "table1_markdown_v2.md"), "w").write("\n".join(md) + "\n")
    # numbers
    status_tl = wide[wide.scope == "trial-level"].set_index("domain_id")
    numbers = {
        "version": __version__, "input": os.path.basename(path), "n_cells": int(len(df)),
        "n_theories": int(df.theory_id.nunique()), "n_trial_level_theories": int(trial.theory_id.nunique()), "n_origin_level_theories": int(origin.theory_id.nunique()),
        "n_domains": int(df.domain_id.nunique()),
        "code_totals_all": {c: int((df.code == c).sum()) for c in V2_CODES},
        "code_polarity_totals_all": df.code_pol.value_counts().to_dict(),
        "code_totals_trial_level": {c: int((trial.code == c).sum()) for c in V2_CODES},
        "n_cells_submitted_v1": int((df.origin == "submitted-v1").sum()), "n_cells_added_in_revision": int((df.origin == "added-in-revision").sum()),
        "per_domain_trial_level": {d: {k: (int(v) if isinstance(v, (int, np.integer)) else (bool(v) if isinstance(v, (bool, np.bool_)) else v))
                                       for k, v in status_tl.loc[d].drop("scope").items()} for d in dom_order},
        "occupancy_counts_trial_level": status_tl.occupancy_summary.value_counts().to_dict(),
        "explicit_per_theory": {t: int(((df.theory_id == t) & (df.code == "EXPLICIT")).sum()) for t in theories},
        "legacy_view_n_cells": (int(legacy_view[legacy_view.scope == "all rows"].n.sum()) if legacy_view is not None else None),
    }
    json.dump(numbers, open(os.path.join(out, "table1_numbers_v2.json"), "w"), indent=1, default=str)
    return numbers


# ---------------------------------------------------------------- legacy (deposit v1.3)
def run_legacy(path, out):
    df = read_csv_strict(path)
    need = {"theory", "quantity_id", "code"}
    if not need <= set(df.columns):
        fail(f"{path}: legacy schema needs {sorted(need)}; has {list(df.columns)}")
    df["code"] = df.code.map(norm_legacy)
    if (df.code == "MISSING").any():
        fail(f"invalid legacy code in rows: {df.loc[df.code == 'MISSING', ['theory', 'quantity_id']].values.tolist()[:5]}")
    dup = df.duplicated(["theory", "quantity_id"], keep=False)
    if dup.any():
        fail(f"{int(dup.sum())} duplicated (theory, quantity_id) rows")
    if "row_class" not in df.columns:
        df["row_class"] = np.where(df.theory.isin(["UAL", "Feinberg & Mallatt"]), "origin-level", "trial-level")
    quant = dict(df[["quantity_id", "quantity"]].drop_duplicates().values) if "quantity" in df.columns else {}
    qs = sorted(df.quantity_id.unique())
    rows = []
    for scope, d in [("trial-level", df[df.row_class == "trial-level"]), ("origin-level", df[df.row_class == "origin-level"]), ("all rows", df)]:
        for q in qs:
            sub = d[d.quantity_id == q]
            r = dict(scope=scope, quantity_id=q, quantity=quant.get(q, ""))
            for c in LEGACY_CODES:
                r[LEGACY_SHORT[c]] = int((sub.code == c).sum())
            r["n"] = int(len(sub)); rows.append(r)
    tal = pd.DataFrame(rows)
    tal.to_csv(os.path.join(out, "table1_tallies_legacy.csv"), index=False)
    trial = df[df.row_class == "trial-level"]
    numbers = {"version": __version__, "input": os.path.basename(path), "schema": "legacy", "n_cells": int(len(df)),
               "n_theories": int(df.theory.nunique()), "n_trial_level_theories": int(trial.theory.nunique()),
               "code_totals": {LEGACY_SHORT[c]: int((df.code == c).sum()) for c in LEGACY_CODES},
               "stated_per_column_trial_level": {q: int(((trial.quantity_id == q) & trial.code.isin(["YES", "YES (negative)"])).sum()) for q in qs},
               "promotion_IMPLICIT_to_YES_trial_level": {q: int(((trial.quantity_id == q) & trial.code.isin(["YES", "YES (negative)", "IMPLICIT"])).sum()) for q in qs}}
    json.dump(numbers, open(os.path.join(out, "table1_numbers_legacy.json"), "w"), indent=1)
    return numbers


# ---------------------------------------------------------------- self-test on synthetic data
def selftest(out, seed=3):
    """Synthetic 12 x 10 table with RANDOM codes (not the study's codes): checks schema handling, tallies summing
    to cell counts, status logic, legacy view, and that the deposit-v1.3 tally format is reproduced."""
    rng = np.random.default_rng(seed)
    here = os.path.dirname(os.path.abspath(__file__))
    acc = read_csv_strict(os.path.join(here, "accounts_manifest.csv")); dom = read_csv_strict(os.path.join(here, "domains_manifest.csv"))
    rows = []
    for t in acc.theory_id:
        for d in dom.domain_id:
            code = rng.choice(V2_CODES, p=[0.2, 0.25, 0.45, 0.06, 0.04])
            pol = rng.choice(POLARITIES, p=[0.7, 0.2, 0.1]) if code in V2_POSITIVE else ""
            legacy = "" if (d in DEFAULT_ADDED_DOMAINS or t in ("PFT", "NSF") or t == "HOSS") else rng.choice(["YES", "IMPLICIT", "NO"])
            rows.append(dict(theory_id=t, domain_id=d, code=code, polarity=pol, relation="sim", source_label="sim", source_doi="10.0/sim" if code in V2_POSITIVE else "",
                             source_locus="p. 1", evidence_status="synthetic", justification="synthetic", legacy_code=legacy))
    sim = pd.DataFrame(rows)
    # one hand-planted contested column and one single-occupant column so the status logic is exercised deterministically
    sim.loc[(sim.domain_id == "M8") & (sim.theory_id == "GNWT"), ["code", "polarity", "source_doi"]] = ["EXPLICIT", "positive", "10.0/sim"]
    sim.loc[(sim.domain_id == "M8") & (sim.theory_id == "SIT"), ["code", "polarity", "source_doi"]] = ["EXPLICIT", "stated_null", "10.0/sim"]
    sim.loc[sim.domain_id == "M6", ["code", "polarity", "source_doi"]] = ["NOT_LOCATED", "", ""]
    sim.loc[(sim.domain_id == "M6") & (sim.theory_id == "IIT"), ["code", "polarity", "source_doi"]] = ["EXPLICIT", "positive", "10.0/sim"]
    p = os.path.join(out, "selftest_S1_v2_synthetic.csv"); sim.to_csv(p, index=False)
    numbers = run_v2(p, os.path.join(here, "accounts_manifest.csv"), os.path.join(here, "domains_manifest.csv"), out)
    log = []
    tal = pd.read_csv(os.path.join(out, "table1_tallies_v2.csv"), keep_default_na=False)
    per_dom = tal[(tal.scope == "all rows") & (tal.code != "ALL")].groupby("domain_id").n.sum()
    log.append(("tallies sum to cells per domain (all rows)", bool((per_dom == 12).all())))
    log.append(("n_cells == 120", numbers["n_cells"] == 120))
    log.append(("M8 occupancy sign-disagreement (E+ vs E0)", numbers["per_domain_trial_level"]["M8"]["occupancy_summary"] == "sign-disagreement"))
    log.append(("M6 occupancy one-EXPLICIT", numbers["per_domain_trial_level"]["M6"]["occupancy_summary"] == "one-EXPLICIT"))
    log.append(("legacy view counts exactly the cells carrying legacy_code", numbers["legacy_view_n_cells"] == int((sim.legacy_code != "").sum())))
    log.append(("origin split: 2 x 10 + 10 x 3 = 50 added cells", numbers["n_cells_added_in_revision"] == 50))
    # legacy schema path on the deposit v1.3 file, if present next to the manifests
    leg = next((p for p in (os.path.join(here, "Table_S1_theory_by_quantity.csv"), os.path.join(here, "Table_S1_v13_88cells.csv")) if os.path.exists(p)), None)
    if leg:
        n = run_legacy(leg, out)
        log.append(("legacy v1.3 file: 88 cells", n["n_cells"] == 88))
    # negative: duplicated key must abort
    bad = pd.concat([sim, sim.iloc[[0]]]); pb = os.path.join(out, "selftest_bad_dup.csv"); bad.to_csv(pb, index=False)
    try:
        run_v2(pb, os.path.join(here, "accounts_manifest.csv"), os.path.join(here, "domains_manifest.csv"), out)
        log.append(("negative: duplicated key aborts", False))
    except SystemExit as e:
        log.append(("negative: duplicated key aborts", "duplicated" in str(e)))
    # rerun the good file so the outputs in `out` belong to the valid table
    run_v2(p, os.path.join(here, "accounts_manifest.csv"), os.path.join(here, "domains_manifest.csv"), out)
    logdf = pd.DataFrame(log, columns=["case", "passed"])
    logdf.to_csv(os.path.join(out, "recompute_selftest_log.csv"), index=False)
    for c, ok in log:
        print(f"[{'PASS' if ok else 'FAIL'}] {c}")
    if not logdf.passed.all():
        sys.exit("recompute_table1 SELFTEST FAILED")
    print(f"recompute_table1 selftest: {int(logdf.passed.sum())} of {len(logdf)} passed")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("table", nargs="?", help="Table_S1_v2.csv (v2 schema) or Table_S1_theory_by_quantity.csv (legacy)")
    ap.add_argument("--accounts", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts_manifest.csv"))
    ap.add_argument("--domains", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "domains_manifest.csv"))
    ap.add_argument("--out", default=".")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    if a.selftest:
        return selftest(a.out)
    if not a.table:
        ap.error("give the Table S1 file or --selftest")
    cols = set(pd.read_csv(a.table, nrows=0).columns)
    if {"theory_id", "domain_id"} <= cols:
        n = run_v2(a.table, a.accounts, a.domains, a.out); print(json.dumps({k: n[k] for k in ("input", "n_cells", "n_theories", "n_domains", "code_totals_all", "occupancy_counts_trial_level")}, indent=1))
    elif {"theory", "quantity_id"} <= cols:
        n = run_legacy(a.table, a.out); print(json.dumps(n, indent=1))
    else:
        fail(f"cannot detect schema from columns {sorted(cols)}")


if __name__ == "__main__":
    main()
