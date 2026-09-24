"""Column typology from Table S1 v2 + Table S4 v2 + pair_register.csv (audit §9 variant of column_typology.py).

    python column_typology_pairs.py Table_S1_v2.csv Table_S4_v2.csv pair_register.csv [out.csv]

Two definitions of `contested` are computed side by side; the class is an OUTPUT of the coding.
  OLD (column_typology.py):  >= 2 EXPLICIT cells AND >= 1 pair listed in S4 `distinguishable_from`
                             (a difference of description in sign/magnitude/locus/timing/distribution/condition).
                             `old_conf2_either_end` counts a pair if distinguishability_confidence >= 2 at EITHER
                             row (the behaviour of column_typology.py); `old_conf2_both_ends` requires it at BOTH.
  NEW (pair register):       >= 2 EXPLICIT cells AND >= 1 pair in pair_register.csv with
                             relation in {discriminating, incompatible} - i.e. a shared observable on which at
                             least one value combination is predicted by one prediction and excluded by the other.
                             `new_conf2` restricts to pairs whose PAIR-LEVEL pair_confidence >= 2 (the confidence
                             is a property of the pair, not inherited from either row).
Other classes as before: single-occupant (exactly 1 EXPLICIT), occupied-not-contested (>= 2 EXPLICIT, no
qualifying pair), thin (0 EXPLICIT, >= 1 INTERPRETED), unoccupied. EXPLICIT with polarity stated_null counts.
"""
import itertools
import sys
import pandas as pd

RELATIONS = ["different", "jointly compatible", "discriminating", "incompatible"]
CONTESTING = {"discriminating", "incompatible"}

ARGS = [x for x in sys.argv[1:] if not x.startswith("--")]
s1_path = ARGS[0] if len(ARGS) > 0 else "Table_S1_v2.csv"
s4_path = ARGS[1] if len(ARGS) > 1 else "Table_S4_v2.csv"
pr_path = ARGS[2] if len(ARGS) > 2 else "pair_register.csv"
out = ARGS[3] if len(ARGS) > 3 else "column_typology_pairs.csv"

cells = pd.read_csv(s1_path, dtype=str, keep_default_na=False)
if "superseded_by" in cells:
    cells = cells[cells.superseded_by == ""]
dup = cells[cells.duplicated(["theory_id", "domain_id"], keep=False)]
if len(dup):
    sys.exit("VALIDATION FAILED: Table S1 must be one row per (theory_id, domain_id); duplicates: "
             + str(dup[["theory_id", "domain_id"]].drop_duplicates().values.tolist()))
reg = pd.read_csv(s4_path, dtype=str, keep_default_na=False)
for col in ("id", "theory_id", "quantity_id", "status", "distinguishable_from"):
    if col not in reg:
        sys.exit(f"VALIDATION FAILED: S4 lacks column {col}")
if "distinguishability_confidence" not in reg:
    reg["distinguishability_confidence"] = "1"
pr = pd.read_csv(pr_path, dtype=str, keep_default_na=False)
for col in ("pair_id", "pred_a", "pred_b", "theory_a", "theory_b", "domain_id", "shared_outcome", "relation",
            "pair_confidence"):
    if col not in pr:
        sys.exit(f"VALIDATION FAILED: pair register lacks column {col}")

# ---- validate the pair register against S4 ------------------------------------------------------
s4 = reg.set_index("id")
seen_pairs = set()
for r in pr.itertuples(index=False):
    for p in (r.pred_a, r.pred_b):
        if p not in s4.index:
            sys.exit(f"VALIDATION FAILED: {r.pair_id} names unknown prediction {p}")
        if s4.loc[p, "status"] != "stated":
            sys.exit(f"VALIDATION FAILED: {r.pair_id} contains derived prediction {p}")
    if s4.loc[r.pred_a, "theory_id"] == s4.loc[r.pred_b, "theory_id"]:
        sys.exit(f"VALIDATION FAILED: {r.pair_id} pairs two predictions of the same theory")
    if s4.loc[r.pred_a, "theory_id"] != r.theory_a or s4.loc[r.pred_b, "theory_id"] != r.theory_b:
        sys.exit(f"VALIDATION FAILED: {r.pair_id} theory ids disagree with S4")
    if s4.loc[r.pred_a, "quantity_id"] != r.domain_id or s4.loc[r.pred_b, "quantity_id"] != r.domain_id:
        sys.exit(f"VALIDATION FAILED: {r.pair_id} predictions are not both in {r.domain_id}")
    if r.relation not in RELATIONS:
        sys.exit(f"VALIDATION FAILED: {r.pair_id} relation '{r.relation}' not in {RELATIONS}")
    if (r.relation == "different") != (r.shared_outcome.strip() == ""):
        sys.exit(f"VALIDATION FAILED: {r.pair_id} relation/shared_outcome mismatch (different <=> no shared observable)")
    if r.pair_confidence not in ("1", "2", "3"):
        sys.exit(f"VALIDATION FAILED: {r.pair_id} pair_confidence must be 1-3")
    key = tuple(sorted((r.pred_a, r.pred_b)))
    if key in seen_pairs:
        sys.exit(f"VALIDATION FAILED: duplicate pair {key}")
    seen_pairs.add(key)
# completeness: the set of REQUIRED pairs is derived from S4 alone (every cross-theory pair of stated predictions in
# every column with >= 2 stated predictions) and checked against the register; a domain absent from the register is
# therefore caught, and a column with any missing pair is classed 'pair assessment incomplete', never
# 'occupied-not-contested' (absence of a row is not evidence of absence of a discriminating pair).
required = {}
for d in sorted(reg.quantity_id.unique()):
    ids = sorted(reg[(reg.quantity_id == d) & (reg.status == "stated")].id)
    req = [(a, b) for a, b in itertools.combinations(ids, 2) if s4.loc[a, "theory_id"] != s4.loc[b, "theory_id"]]
    if req:
        required[d] = req
incomplete = {}
for d, req in required.items():
    missing = [f"{a}-{b}" for a, b in req if (a, b) not in seen_pairs and (b, a) not in seen_pairs]
    if missing:
        incomplete[d] = missing
        print(f"WARNING: pair register incomplete for {d}: {len(missing)} of {len(req)} required pairs missing ({'; '.join(missing[:6])}{'...' if len(missing) > 6 else ''}) -> class 'pair assessment incomplete'")
if incomplete and "--allow-incomplete" not in sys.argv:
    sys.exit("VALIDATION FAILED: pair register incomplete for " + ", ".join(incomplete) + " (pass --allow-incomplete to derive classes with 'pair assessment incomplete' for those columns)")
covered = sorted(set(pr.domain_id.unique()) | set(required))   # columns whose class depends on pairs: from S4, not from the register

# ---- old definition: symmetric stated-only pairs from distinguishable_from --------------------------
for r in reg.itertuples(index=False):
    for p in [x.strip() for x in r.distinguishable_from.split(";") if x.strip()]:
        other = reg[reg.id == p]
        if other.empty:
            sys.exit(f"VALIDATION FAILED: {r.id} names unknown prediction {p}")
        if r.id not in other.distinguishable_from.iloc[0]:
            sys.exit(f"VALIDATION FAILED: asymmetric distinguishable pair {r.id}-{p}")

def rowconf(pid):
    v = s4.loc[pid, "distinguishability_confidence"].strip()
    return int(v) if v else 0

def old_pairs(domain_id, mode):
    """mode: 'all' | 'either' (conf>=2 at either end, as column_typology.py) | 'both' (conf>=2 at both ends)."""
    sub = reg[(reg.quantity_id == domain_id) & (reg.status == "stated")]
    seen = set()
    for r in sub.itertuples(index=False):
        for p in [x.strip() for x in r.distinguishable_from.split(";") if x.strip()]:
            ca, cb = rowconf(r.id), rowconf(p)
            if mode == "all" or (mode == "either" and max(ca, cb) >= 2) or (mode == "both" and min(ca, cb) >= 2):
                seen.add(tuple(sorted((r.id, p))))
    return seen

def new_pairs(domain_id, min_conf=1):
    sub = pr[(pr.domain_id == domain_id) & pr.relation.isin(CONTESTING) & (pr.pair_confidence.astype(int) >= min_conf)]
    return set(tuple(sorted((a, b))) for a, b in zip(sub.pred_a, sub.pred_b))

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
    n_exp = int(((c.code == "EXPLICIT") & c.polarity.isin(["positive", "stated_null", "negative"])).sum())
    n_int = int((c.code == "INTERPRETED").sum())
    o_all, o_either, o_both = old_pairs(d, "all"), old_pairs(d, "either"), old_pairs(d, "both")
    n_all, n_c2 = new_pairs(d, 1), new_pairs(d, 2)
    prd = pr[pr.domain_id == d]
    rel_counts = {f"n_pairs_{k.replace(' ', '_')}": int((prd.relation == k).sum()) for k in RELATIONS}
    rows.append(dict(
        domain_id=d, domain=c.domain.iloc[0], n_explicit=n_exp, n_interpreted=n_int,
        explicit_theories=";".join(sorted(c[c.code == "EXPLICIT"].theory_id)),
        n_stated_predictions=int(((reg.quantity_id == d) & (reg.status == "stated")).sum()),
        n_pairs_registered=len(prd), **rel_counts,
        n_pairs_conf2=int((prd.pair_confidence.astype(int) >= 2).sum()) if len(prd) else 0,
        old_n_distinguishable=len(o_all), old_n_conf2_either_end=len(o_either), old_n_conf2_both_ends=len(o_both),
        old_class=classify(n_exp, n_int, len(o_all)),
        old_class_conf2_either_end=classify(n_exp, n_int, len(o_either)),
        old_class_conf2_both_ends=classify(n_exp, n_int, len(o_both)),
        new_n_contesting=len(n_all), new_contesting_pairs=";".join("-".join(p) for p in sorted(n_all)),
        new_n_contesting_conf2=len(n_c2),
        new_class=("pair assessment incomplete" if d in incomplete and classify(n_exp, n_int, len(n_all)) == "occupied-not-contested" else classify(n_exp, n_int, len(n_all))),
        new_class_conf2=("pair assessment incomplete" if d in incomplete and classify(n_exp, n_int, len(n_c2)) == "occupied-not-contested" else classify(n_exp, n_int, len(n_c2))),
        n_required_pairs=len(required.get(d, [])), n_missing_pairs=len(incomplete.get(d, [])),
        pair_register_coverage=("complete" if d in required and d not in incomplete else "incomplete" if d in incomplete else "n/a (fewer than two stated predictions)"),
    ))
typ = pd.DataFrame(rows)
typ.to_csv(out, index=False)

show = typ[typ.domain_id.isin(covered)]
print("Columns whose class depends on pairs:", ", ".join(covered))
for r in show.itertuples(index=False):
    print(f"\n== {r.domain_id} ({r.domain}) : {r.n_explicit} EXPLICIT [{r.explicit_theories}], "
          f"{r.n_stated_predictions} stated predictions, {r.n_pairs_registered} cross-theory pairs registered")
    print(f"  pairs by relation: different={r.n_pairs_different}  jointly compatible={r.n_pairs_jointly_compatible}  "
          f"discriminating={r.n_pairs_discriminating}  incompatible={r.n_pairs_incompatible}")
    print(f"  OLD  distinguishable_from pairs: all={r.old_n_distinguishable}  conf>=2 either end={r.old_n_conf2_either_end}  "
          f"conf>=2 both ends={r.old_n_conf2_both_ends}")
    print(f"  OLD  class: {r.old_class}  | conf2 either end: {r.old_class_conf2_either_end}  | conf2 both ends: {r.old_class_conf2_both_ends}")
    print(f"  NEW  contesting pairs (discriminating/incompatible): {r.new_n_contesting} [{r.new_contesting_pairs}]  "
          f"with pair_confidence>=2: {r.new_n_contesting_conf2}")
    print(f"  NEW  class: {r.new_class}  | pair_confidence>=2: {r.new_class_conf2}")
print("\nPair-level counts by relation x pair_confidence (all covered columns):")
print(pd.crosstab(pr.relation, pr.pair_confidence.astype(int), margins=True).to_string())
print(f"\nwritten {out}")
