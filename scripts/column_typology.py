"""Derive the column typology from Table S1 v2 (cell-level) and Table S4 v2 (prediction register).

    python column_typology.py Table_S1_v2.csv Table_S4_v2.csv [out.csv]

The class of a column is an OUTPUT of the coding, never an input:
  contested              >= 2 EXPLICIT cells AND >= 1 pair of stated predictions in S4 that differ
                         in sign, magnitude, locus, timing, distribution or condition
  single-occupant        exactly 1 EXPLICIT cell
  occupied-not-contested >= 2 EXPLICIT cells, no distinguishable pair
  thin                   0 EXPLICIT, >= 1 INTERPRETED
  unoccupied             0 EXPLICIT, 0 INTERPRETED
EXPLICIT with polarity null counts as EXPLICIT (a stated null is a stated prediction).
`derived_class_conf2` uses only distinguishable pairs with distinguishability_confidence >= 2.
"""
import sys
import pandas as pd

s1_path = sys.argv[1] if len(sys.argv) > 1 else "Table_S1_v2.csv"
s4_path = sys.argv[2] if len(sys.argv) > 2 else "Table_S4_v2.csv"
out = sys.argv[3] if len(sys.argv) > 3 else "column_typology_v2.csv"

cells = pd.read_csv(s1_path, dtype=str, keep_default_na=False)
if "superseded_by" in cells:
    cells = cells[cells.superseded_by == ""]
dup = cells[cells.duplicated(["theory_id", "domain_id"], keep=False)]
if len(dup):
    sys.exit("VALIDATION FAILED: Table S1 must be one row per (theory_id, domain_id); duplicates: "
             + str(dup[["theory_id", "domain_id"]].drop_duplicates().values.tolist()))
reg = pd.read_csv(s4_path, dtype=str, keep_default_na=False)
for col in ("id", "quantity_id", "status", "distinguishable_from"):
    if col not in reg:
        sys.exit(f"VALIDATION FAILED: S4 lacks column {col}")
if "distinguishability_confidence" not in reg:
    reg["distinguishability_confidence"] = "1"

# symmetric, stated-only pairs
for r in reg.itertuples(index=False):
    for p in [x.strip() for x in r.distinguishable_from.split(";") if x.strip()]:
        other = reg[reg.id == p]
        if other.empty:
            sys.exit(f"VALIDATION FAILED: {r.id} names unknown prediction {p}")
        if r.id not in other.distinguishable_from.iloc[0]:
            sys.exit(f"VALIDATION FAILED: asymmetric distinguishable pair {r.id}-{p}")
        if r.status != "stated" or other.status.iloc[0] != "stated":
            sys.exit(f"VALIDATION FAILED: derived row in distinguishable pair {r.id}-{p}")

def pairs_in(domain_id, min_conf):
    sub = reg[(reg.quantity_id == domain_id) & (reg.status == "stated")]
    seen = set()
    for r in sub.itertuples(index=False):
        c = int(r.distinguishability_confidence) if r.distinguishability_confidence.strip() else 0
        for p in [x.strip() for x in r.distinguishable_from.split(";") if x.strip()]:
            if c >= min_conf:
                seen.add(tuple(sorted((r.id, p))))
    return seen

def classify(n_explicit, n_interp, n_pairs):
    if n_explicit >= 2 and n_pairs >= 1:
        return "contested"
    if n_explicit == 1:
        return "single-occupant"
    if n_explicit >= 2:
        return "occupied-not-contested"
    if n_interp >= 1:
        return "thin"
    return "unoccupied"

rows = []
for d in sorted(cells.domain_id.unique(), key=lambda x: (len(x), x)):
    c = cells[cells.domain_id == d]
    n_pos = int(((c.code == "EXPLICIT") & (c.polarity == "positive")).sum())
    n_null = int(((c.code == "EXPLICIT") & (c.polarity == "stated_null")).sum())
    n_neg = int(((c.code == "EXPLICIT") & (c.polarity == "negative")).sum())
    n_exp = n_pos + n_null + n_neg
    n_int = int((c.code == "INTERPRETED").sum())
    p1, p2 = pairs_in(d, 1), pairs_in(d, 2)
    rows.append(dict(
        domain_id=d, domain=c.domain.iloc[0], n_cells=len(c),
        n_explicit_pos=n_pos, n_explicit_null=n_null, n_explicit_neg=n_neg, n_interpreted=n_int,
        n_not_located=int((c.code == "NOT_LOCATED").sum()), n_not_applicable=int((c.code == "NOT_APPLICABLE").sum()),
        n_unresolved=int((c.code == "UNRESOLVED").sum()),
        explicit_theories=";".join(sorted(c[c.code == "EXPLICIT"].theory_id)),
        n_stated_predictions=int(((reg.quantity_id == d) & (reg.status == "stated")).sum()),
        n_derived_predictions=int(((reg.quantity_id == d) & (reg.status == "derived")).sum()),
        n_distinguishable_pairs=len(p1), distinguishable_pairs=";".join("-".join(p) for p in sorted(p1)),
        n_distinguishable_pairs_conf2=len(p2),
        derived_class=classify(n_exp, n_int, len(p1)), derived_class_conf2=classify(n_exp, n_int, len(p2)),
        n_flagged_cells=int((c.flag_for_adjudication != "").sum()) if "flag_for_adjudication" in c else 0,
        n_provisional_cells=int((c.provisional.str.lower() == "true").sum()) if "provisional" in c else 0,
        n_abstract_only_cells=int((c.evidence_status == "abstract-only").sum()) if "evidence_status" in c else 0,
    ))
typ = pd.DataFrame(rows)
typ.to_csv(out, index=False)
print(typ[["domain_id", "n_explicit_pos", "n_explicit_null", "n_interpreted", "n_not_located",
           "n_distinguishable_pairs", "derived_class", "derived_class_conf2"]].to_string(index=False))
