"""Build the revised Table S1 (trial-level + origin-level rows, two new rows) and
recompute every Table 1 tally from it.  Nothing in the prose is typed by hand:
table1_tallies_revised.csv and table1_markdown.md are the only sources.

Inputs : theory_predictions_matrix.csv (72 cells, round-0 Table S1)
Outputs: table_S1_revised.csv, table1_tallies_revised.csv, table1_markdown.md,
         table1_numbers.json
"""
import json
import sys

import pandas as pd

SRC = sys.argv[1] if len(sys.argv) > 1 else "theory_predictions_matrix.csv"
s1 = pd.read_csv(SRC)
assert s1.shape == (72, 7), s1.shape

QUANT = {q: n for q, n in s1[["quantity_id", "quantity"]].drop_duplicates().values}
ORIGIN = {"UAL", "Feinberg & Mallatt"}

# --- 1. Split the compound SIT / passive-frame row -------------------------
# The existing codes stay; the SIT row is re-anchored to the SIT statements
# (Morsella 2005; Morsella, Gray & Krieger 2009; Gray, Bargh & Morsella 2013)
# so that the passive-frame row can carry the 2015/2016 BBS statements.
SIT_OLD = "SIT / passive frame theory"
SIT_NEW = "Supramodular interaction theory (SIT)"
s1.loc[s1.theory == SIT_OLD, "theory"] = SIT_NEW
reanchor = {
    "M1": ("Morsella 2005", "10.1037/0033-295x.112.4.1000",
           "PRISM: phenomenal states are required when multiple supramodular systems send simultaneous, "
           "competing inclinations to the skeletomotor output system — the number of concurrent inclinations "
           "is the theory's own trigger variable."),
    "M4": ("Morsella, Gray & Krieger 2009", "10.1037/a0017121",
           "A sharp, testable negative: conflict in a smooth-muscle effector (pupillary light reflex) produces "
           "no comparable change in conscious experience; phenomenal states serve skeletomotor integration only."),
    "M5": ("Morsella 2005", "10.1037/0033-295x.112.4.1000",
           "Phenomenal states integrate systems competing for skeletal muscle; no organism-wide coherence "
           "measure including autonomic channels is proposed."),
    "M6": ("Morsella 2005", "10.1037/0033-295x.112.4.1000", "No dimensionality prediction."),
    "M7": ("Morsella 2005", "10.1037/0033-295x.112.4.1000",
           "Integration is stated as co-presence of contents; metarepresentational precision plays no role."),
    "M8": ("Gray, Bargh & Morsella 2013", "10.1007/s00221-013-3566-5",
           "Subjective conflict from sustained incompatible intentions was associated with left postcentral "
           "(somatosensory) cortex; a candidate substrate is named, but no discriminating cortical access "
           "signature is staked."),
}
for q, (lab, doi, just) in reanchor.items():
    m = (s1.theory == SIT_NEW) & (s1.quantity_id == q)
    assert m.sum() == 1
    s1.loc[m, ["citation_label", "citation_doi", "prediction"]] = [lab, doi, just]

# --- 2. New row: Passive frame theory (Morsella et al. 2015/2016 BBS) -------
BBS15 = ("Morsella et al. 2015", "10.1017/s0140525x15000643")
BBS16 = ("Morsella, Godwin & Jantz 2016", "10.1017/s0140525x15002812")
HC24 = ("Heredia Cedillo, Lambert & Morsella 2024", "10.3390/bs14040337")
pft = [
    ("M1", "IMPLICIT",
     "The function of the conscious field is still stated as integration of multiple skeletomotor inclinations, "
     "but the passive-frame formulation makes no trial-level prediction from their number: the field presents "
     "contents whether one or many inclinations are present.", *BBS15),
    ("M2", "IMPLICIT",
     "Incompatibility is what downstream systems resolve using the field's contents, but the field is stated to "
     "operate blindly whether or not conflict is present, so incompatibility is no longer a predictor of access "
     "(cf. §4).", *HC24),
    ("M3", "IMPLICIT",
     "The reply to commentators accepts that affective contents enter the field but states no valence-dependent "
     "access prediction.", *BBS16),
    ("M4", "YES (negative)",
     "Consciousness serves the somatic nervous system: it is a frame that constrains and directs skeletal-muscle "
     "output, and conflicts without a skeletomotor plan are stated to lie outside it.", *BBS15),
    ("M5", "NO",
     "The frame is scoped to skeletal-muscle output; no organism-wide cortical–autonomic coherence variable is "
     "proposed.", *BBS15),
    ("M6", "NO", "No dimensionality prediction; the field is described as low-level and unintelligent.", *BBS15),
    ("M7", "NO",
     "The frame is passive: contents are presented without being evaluated, so metarepresentational precision "
     "plays no role.", *BBS15),
    ("M8", "NO",
     "The theory explicitly declines the implementation level — how neurons produce conscious states is not "
     "part of the account — so no cortical signature of access is stated.", *BBS16),
]
# --- 3. New row: Neural subjective frame (codes from m5_assessment_en.md) ---
nsf = [
    ("M1", "NO", "No statement relates access to the number of competing action policies.",
     "Park & Tallon-Baudry 2014", "10.1098/rstb.2013.0208"),
    ("M2", "NO", "Policy incompatibility is not a variable in the proposal.",
     "Park & Tallon-Baudry 2014", "10.1098/rstb.2013.0208"),
    ("M3", "IMPLICIT",
     "The frame could also underlie emotional feelings and vmPFC heartbeat-evoked responses contribute to "
     "preference-based decisions, but no valence-dependent access prediction is stated.",
     "Azzalini et al. 2021", "10.1523/jneurosci.1932-20.2021"),
    ("M4", "YES",
     "Neural monitoring of cardiac (and gastric) input is the stated generator of first-person perspective, and "
     "pre-stimulus heartbeat-evoked responses predict detection.",
     "Park et al. 2014", "10.1038/nn.3671"),
    ("M5", "IMPLICIT",
     "A cortical response to one visceral signal predicts access, independently of measured bodily state; no "
     "organism-wide joint cortical–autonomic metric is specified.",
     "Tallon-Baudry et al. 2018", "10.1016/j.cortex.2017.05.019"),
    ("M6", "IMPLICIT",
     "The dimensionality and topology of subjective experience are posed as open questions, without a "
     "quantitative prediction.", "Tallon-Baudry 2022", "10.1016/j.tics.2022.09.002"),
    ("M7", "NO",
     "The frame is a low-level building block not explicitly experienced by itself; no claim about "
     "metarepresentational precision.", "Park & Tallon-Baudry 2014", "10.1098/rstb.2013.0208"),
    ("M8", "IMPLICIT",
     "Pre-stimulus heartbeat-evoked response amplitude in right inferior parietal and ventral anterior "
     "cingulate cortex is a stated cortical predictor of detection, framed as a precondition rather than as "
     "the signature of access itself.", "Park et al. 2014", "10.1038/nn.3671"),
]
new_rows = [("Passive frame theory", *r) for r in pft] + [("Neural subjective frame", *r) for r in nsf]
new = pd.DataFrame(new_rows, columns=["theory", "quantity_id", "code", "prediction", "citation_label", "citation_doi"])
new["quantity"] = new.quantity_id.map(QUANT)
s1 = pd.concat([s1, new[s1.columns]], ignore_index=True)

ORDER = ["GNWT", "IIT (3.0/4.0)", "Recurrent processing (RPT)", "HOT / HOSS", "AST",
         "Predictive processing / beast machine", SIT_NEW, "Passive frame theory",
         "Neural subjective frame", "UAL", "Feinberg & Mallatt"]
assert set(ORDER) == set(s1.theory.unique()), set(s1.theory.unique()) ^ set(ORDER)
s1["row_class"] = s1.theory.map(lambda t: "origin-level" if t in ORIGIN else "trial-level")
s1["_o"] = s1.theory.map(ORDER.index)
s1 = s1.sort_values(["_o", "quantity_id"]).drop(columns="_o").reset_index(drop=True)
assert s1.shape[0] == 88 and s1.groupby("theory").size().eq(8).all()
assert set(s1.code) <= {"YES", "YES (negative)", "IMPLICIT", "NO"}, set(s1.code)
s1.to_csv("table_S1_revised.csv", index=False)

# --- 4. Tallies ---------------------------------------------------------------
CODES = [("YES", "YES"), ("YES (negative)", "YES(neg)"), ("IMPLICIT", "IMPLICIT"), ("NO", "NO")]
QS = sorted(QUANT)


def tally(df):
    out = {}
    for q in QS:
        c = df[df.quantity_id == q].code.value_counts()
        out[q] = {short: int(c.get(code, 0)) for code, short in CODES}
        out[q]["n"] = int((df.quantity_id == q).sum())
        assert sum(out[q][s] for _, s in CODES) == out[q]["n"]
    return out


trial = s1[s1.row_class == "trial-level"]
origin = s1[s1.row_class == "origin-level"]
T = {"trial-level": tally(trial), "origin-level": tally(origin), "all rows": tally(s1)}
rows = []
for scope, d in T.items():
    for q in QS:
        rows.append({"scope": scope, "quantity_id": q, "quantity": QUANT[q], **d[q]})
tal = pd.DataFrame(rows)
tal.to_csv("table1_tallies_revised.csv", index=False)

# Promotion sensitivity: every IMPLICIT -> YES
prom = {}
for scope, df in [("trial-level", trial), ("all rows", s1)]:
    prom[scope] = {}
    for q in QS:
        d = T[scope][q]
        occ = df[(df.quantity_id == q) & df.code.isin(["YES", "IMPLICIT"])].theory.tolist()
        prom[scope][q] = {"as_coded_YES": d["YES"], "after_promotion": d["YES"] + d["IMPLICIT"],
                          "n": d["n"], "occupants_after_promotion": occ}

# Per-row YES counts (for prose)
per_row = {t: int(((s1.theory == t) & s1.code.isin(["YES", "YES (negative)"])).sum()) for t in ORDER}

# --- 5. Table 1 markdown, condensed ------------------------------------------
SYM = {"YES": "**Y**", "YES (negative)": "**Y(neg)**", "IMPLICIT": "*i*", "NO": "·"}
hdr = ("| Theory | M1 N of policies | M2 Incompat. | M3 Valence | M4 Autonomic | M5 Org-wide coh. | "
       "M6 Dim. of phen. space | M7 Metarep. precision | M8 Cortical signature |")
sep = "|---|" + "---|" * 8
md = [hdr, sep]
SHORT = {SIT_NEW: "Supramodular interaction theory (SIT)"}


def tally_line(label, d):
    cells = []
    for q in QS:
        x = d[q]
        s = f"{x['YES']} Y"
        if x["YES(neg)"]:
            s += f" / {x['YES(neg)']} Y(neg)"
        s += f" / {x['IMPLICIT']} i / {x['NO']} ·"
        cells.append(s)
    return f"| **{label}** | " + " | ".join(cells) + " |"


for t in ORDER:
    if t == "UAL":
        md.append("| *Origin-level accounts* | | | | | | | | |")
    r = s1[s1.theory == t].set_index("quantity_id").code
    md.append(f"| {SHORT.get(t, t)} | " + " | ".join(SYM[r[q]] for q in QS) + " |")
    if t == "Neural subjective frame":
        md.append(tally_line(f"Tally, trial-level accounts (n = {T['trial-level']['M1']['n']})", T["trial-level"]))
md.append(tally_line(f"Tally, all rows (n = {T['all rows']['M1']['n']})", T["all rows"]))
open("table1_markdown.md", "w").write("\n".join(md) + "\n")

numbers = {"tally": T, "promotion": prom, "yes_per_row": per_row,
           "n_cells": int(len(s1)), "n_trial_rows": int(trial.theory.nunique()),
           "n_origin_rows": int(origin.theory.nunique()),
           "code_totals": s1.code.value_counts().to_dict(),
           "m4_occupants": s1[(s1.quantity_id == "M4") & s1.code.isin(["YES", "YES (negative)"])][["theory", "code"]].values.tolist(),
           "m5_occupants": s1[(s1.quantity_id == "M5") & s1.code.isin(["YES", "IMPLICIT"])][["theory", "code"]].values.tolist(),
           "m8_occupants": s1[(s1.quantity_id == "M8") & (s1.code == "YES")].theory.tolist()}
json.dump(numbers, open("table1_numbers.json", "w"), indent=1)
print(json.dumps(numbers, indent=1))
