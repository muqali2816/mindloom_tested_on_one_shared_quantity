#!/usr/bin/env python
"""
build_table2.py (v2.2) -- Table 2 counts from Table_S2_v2.csv at BOTH units (audit section 7).

Table_S2_v2.csv carries one row per coded unit with unit_type in {experiment, experiment-group,
publication-as-one (partition unverified)}: the 42 rows are heterogeneous, so an experiment-level share is
not a verified experiment count.  This script therefore reports:

  (i)  publication level -- one row per publication_id.
         theory_addressed  = any experiment row of the publication has theory_addressed True;
         class             = the single content_class_v2 of the publication's rows, or
                             'motor-conflict (skeletal + autonomic effector)' when both motor classes occur
                             (the only mixture present; any other mixture is printed and coded 'mixed');
         content-bearing   = class is not 'state (no content)';
         baseline          = theory-addressed AND content-bearing AND not Whalen et al. 1998 (P29, access
                             suppressed rather than manipulated).  Counts per class are reported as 'k of n'.
  (ii) experiment level -- the row-level baseline as in s2_sensitivity.py S0 (has_content_manipulation,
         Whalen excluded, contested and ancillary rows included, theory_addressed True), with a
         unit-heterogeneity block: how many rows of the denominator are experiment / experiment-group /
         publication-as-one units.

No coding value is changed or typed; every number is derived from the table.
Usage:  python build_table2.py [Table_S2_v2.csv] [--out Table_2_counts.csv] [--expect-publications 21]
Also writes <out>_summary.json (the two baselines as dicts of class -> 'k of n').
"""
from __future__ import annotations
import argparse, csv, json, os, sys
from collections import Counter, OrderedDict

__version__ = "2.1"
STATE = "state (no content)"
SKELETAL, AUTONOMIC = "motor-conflict (skeletal)", "motor-conflict (autonomic effector)"
BOTH_MOTOR = "motor-conflict (skeletal + autonomic effector)"
UNIT_TYPES = ["experiment", "experiment-group", "publication-as-one (partition unverified)"]
B = lambda v: str(v).strip().lower() == "true"


def fail(msg):
    sys.exit("build_table2.py FAILED: " + msg)


def is_whalen(r):
    return r["citation_label"].strip().startswith("Whalen") or r["publication_id"].strip() == "P29"


def publication_class(classes: set[str], pub_id: str, classes_main: set[str] | None = None) -> str:
    """Class of a publication from the classes of its rows. Rows flagged ancillary_experiment (control experiments that
    remove the manipulated feature, pilots) do not define the publication's class when at least one main row exists:
    a valenced study with a neutral control experiment is a valenced publication, not 'mixed' (rule made explicit v2.2)."""
    if classes_main:
        classes = classes_main
    if len(classes) == 1:
        return next(iter(classes))
    if classes == {SKELETAL, AUTONOMIC}:
        return BOTH_MOTOR
    print(f"build_table2.py: publication {pub_id} mixes content classes {sorted(classes)} -> coded 'mixed'", file=sys.stderr)
    return "mixed"


def load(path):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    need = {"publication_id", "experiment_id", "citation_label", "content_class_v2", "theory_addressed", "has_content_manipulation", "unit_type", "contested_inclusion", "ancillary_experiment"}
    if not rows or not need <= set(rows[0].keys()):
        fail(f"{path} needs columns {sorted(need)}; has {sorted(rows[0].keys()) if rows else 'no rows'}")
    bad_unit = sorted({r["unit_type"] for r in rows} - set(UNIT_TYPES))
    if bad_unit:
        fail(f"unit_type outside {UNIT_TYPES}: {bad_unit}")
    ids = [r["experiment_id"] for r in rows]
    if len(set(ids)) != len(ids):
        fail("duplicated experiment_id in " + path)
    # content_class_v2 is DERIVED from the raw coded fields (modality, affective_status, effector_type) by the codebook
    # rule below; a stored class that disagrees with its raw fields aborts, so the class cannot drift from the coding.
    if {"modality", "affective_status", "effector_type"} <= set(rows[0].keys()):
        bad = [(r["experiment_id"], r["content_class_v2"], derive_class(r)) for r in rows if r["content_class_v2"].strip() != derive_class(r)]
        if bad:
            fail("content_class_v2 disagrees with the raw fields (experiment_id, stored, derived): " + "; ".join(map(str, bad[:8])))
    else:
        print("WARNING: raw fields modality/affective_status/effector_type absent; content_class_v2 taken as given", file=sys.stderr)
    return rows


def derive_class(r):
    """Codebook v2.2 rule: class from the raw coded fields, never assigned directly."""
    m, aff, eff = r["modality"].strip(), r["affective_status"].strip(), r.get("effector_type", "").strip()
    if m == "not applicable (state)":
        return "state (no content)"
    if aff == "valenced":
        return "valenced"
    if m == "interoceptive" or aff == "interoceptive":
        return "interoceptive"
    if m == "motor":
        return "motor-conflict (autonomic effector)" if eff == "autonomic" else "motor-conflict (skeletal)"
    return "neutral-visual" if m == "visual" else "neutral-nonvisual"


def build(rows):
    out = []
    add = lambda unit, block, category, k, n, ids="": out.append(OrderedDict(unit=unit, block=block, category=category, k=k, n=n, k_of_n=f"{k} of {n}", ids=ids))
    # ---------------- publication level
    pubs = OrderedDict()
    for r in rows:
        pubs.setdefault(r["publication_id"], []).append(r)
    pub_info = OrderedDict()
    for pid, prs in pubs.items():
        classes = {r["content_class_v2"].strip() for r in prs}
        classes_main = {r["content_class_v2"].strip() for r in prs if not B(r["ancillary_experiment"])}
        pub_info[pid] = dict(cls=publication_class(classes, pid, classes_main), ta=any(B(r["theory_addressed"]) for r in prs), whalen=any(is_whalen(r) for r in prs),
                             unit_types=sorted({r["unit_type"] for r in prs}), n_rows=len(prs), label=prs[0]["citation_label"])
    base_pub = [p for p, i in pub_info.items() if i["ta"] and i["cls"] != STATE and not i["whalen"]]
    n_pub = len(base_pub)
    add("publication", "denominator", "theory-addressed, content-bearing, Whalen excluded", n_pub, n_pub, ";".join(base_pub))
    add("publication", "all_publications", "publications in Table S2 v2", len(pubs), len(pubs), ";".join(pubs))
    add("publication", "excluded", "Whalen et al. 1998 (access suppressed, not manipulated)", sum(i["whalen"] for i in pub_info.values()), len(pubs), ";".join(p for p, i in pub_info.items() if i["whalen"]))
    add("publication", "excluded", "not theory-addressed", sum((not i["ta"]) for i in pub_info.values()), len(pubs), ";".join(p for p, i in pub_info.items() if not i["ta"]))
    add("publication", "excluded", STATE, sum(i["cls"] == STATE for i in pub_info.values()), len(pubs), ";".join(p for p, i in pub_info.items() if i["cls"] == STATE))
    pub_counts = Counter(pub_info[p]["cls"] for p in base_pub)
    pub_order = ["neutral-visual", "neutral-nonvisual", SKELETAL, AUTONOMIC, BOTH_MOTOR, "valenced", "interoceptive", "mixed"]
    for c in pub_order + sorted(set(pub_counts) - set(pub_order)):
        if c in pub_counts or c in pub_order[:7]:
            add("publication", "class", c, pub_counts.get(c, 0), n_pub, ";".join(p for p in base_pub if pub_info[p]["cls"] == c))
    add("publication", "class_collapsed", "motor-conflict (any effector)", sum(v for c, v in pub_counts.items() if c.startswith("motor-conflict")), n_pub, ";".join(p for p in base_pub if pub_info[p]["cls"].startswith("motor-conflict")))
    for ut in UNIT_TYPES:
        add("publication", "unit_type_composition", f"publications whose rows are all '{ut}'", sum(pub_info[p]["unit_types"] == [ut] for p in base_pub), n_pub, ";".join(p for p in base_pub if pub_info[p]["unit_types"] == [ut]))
    add("publication", "unit_type_composition", "publications with more than one row", sum(pub_info[p]["n_rows"] > 1 for p in base_pub), n_pub, ";".join(p for p in base_pub if pub_info[p]["n_rows"] > 1))
    # ---------------- experiment level (row-level baseline as in s2_sensitivity.py S0)
    base_exp = [r for r in rows if B(r["has_content_manipulation"]) and not is_whalen(r) and B(r["theory_addressed"])]
    n_exp = len(base_exp)
    add("experiment", "denominator", "rows with content manipulation, theory-addressed, Whalen excluded (contested and ancillary rows included)", n_exp, n_exp, ";".join(r["experiment_id"] for r in base_exp))
    add("experiment", "all_rows", "rows in Table S2 v2", len(rows), len(rows))
    exp_counts = Counter(r["content_class_v2"].strip() for r in base_exp)
    for c in ["neutral-visual", "neutral-nonvisual", SKELETAL, AUTONOMIC, "valenced", "interoceptive"] + sorted(set(exp_counts) - {"neutral-visual", "neutral-nonvisual", SKELETAL, AUTONOMIC, "valenced", "interoceptive"}):
        add("experiment", "class", c, exp_counts.get(c, 0), n_exp, ";".join(r["experiment_id"] for r in base_exp if r["content_class_v2"].strip() == c))
    add("experiment", "class_collapsed", "motor-conflict (any effector)", sum(v for c, v in exp_counts.items() if c.startswith("motor-conflict")), n_exp, ";".join(r["experiment_id"] for r in base_exp if r["content_class_v2"].startswith("motor-conflict")))
    add("experiment", "publications_in_denominator", "distinct publication_id", len({r["publication_id"] for r in base_exp}), n_exp, ";".join(sorted({r["publication_id"] for r in base_exp})))
    for ut in UNIT_TYPES:
        add("experiment", "unit_heterogeneity", f"{ut} rows in the denominator", sum(r["unit_type"] == ut for r in base_exp), n_exp, ";".join(r["experiment_id"] for r in base_exp if r["unit_type"] == ut))
    for ut in UNIT_TYPES:
        add("experiment", "unit_heterogeneity_all_rows", f"{ut} rows in the whole table", sum(r["unit_type"] == ut for r in rows), len(rows))
    summary = dict(version=__version__,
                   pub_level_baseline={row["category"]: row["k_of_n"] for row in out if row["unit"] == "publication" and row["block"] == "class"},
                   pub_level_n=n_pub, pub_level_ids=base_pub,
                   exp_level_baseline={row["category"]: row["k_of_n"] for row in out if row["unit"] == "experiment" and row["block"] == "class"},
                   exp_level_n=n_exp,
                   unit_heterogeneity_in_exp_denominator={row["category"].split(" rows")[0]: row["k_of_n"] for row in out if row["block"] == "unit_heterogeneity"},
                   unit_heterogeneity_all_rows={row["category"].split(" rows")[0]: row["k_of_n"] for row in out if row["block"] == "unit_heterogeneity_all_rows"},
                   mixed_publications=[p for p, i in pub_info.items() if i["cls"] == "mixed"])
    return out, summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", nargs="?", default="Table_S2_v2.csv")
    ap.add_argument("--out", default="Table_2_counts.csv")
    ap.add_argument("--expect-publications", type=int, default=None, help="fail unless the publication-level baseline has exactly this many publications")
    a = ap.parse_args(argv)
    rows = load(a.src)
    out, summary = build(rows)
    if a.expect_publications is not None and summary["pub_level_n"] != a.expect_publications:
        fail(f"publication-level baseline has {summary['pub_level_n']} publications, expected {a.expect_publications}: {summary['pub_level_ids']}")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(out)
    json.dump(summary, open(a.out[:-4] + "_summary.json" if a.out.endswith(".csv") else a.out + "_summary.json", "w"), indent=1)
    print(f"build_table2.py v{__version__}: publication-level baseline n = {summary['pub_level_n']}: " + "; ".join(f"{k} {v}" for k, v in summary["pub_level_baseline"].items() if not v.startswith("0 of")))
    print(f"experiment-level baseline n = {summary['exp_level_n']}: " + "; ".join(f"{k} {v}" for k, v in summary["exp_level_baseline"].items() if not v.startswith("0 of")))
    print("unit heterogeneity in the experiment-level denominator: " + "; ".join(f"{k} {v}" for k, v in summary["unit_heterogeneity_in_exp_denominator"].items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
