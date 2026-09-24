"""Table 1 from the coding matrix (Table S1): compact view + tallies.

    python table1_from_matrix.py theory_predictions_matrix.csv      # original, 72 cells
    python table1_from_matrix.py table_S1_revised.csv                # revised, 88 cells

Input columns: theory, quantity_id, quantity, code, prediction, citation_label, citation_doi
(revised file also has row_class = trial-level | origin-level).
Codes: YES / IMPLICIT / NO / YES (negative).
"""
import sys
import pandas as pd

SYM = {"YES": "Y", "YES (negative)": "Y(neg)", "IMPLICIT": "i", "NO": "·"}
ORIGIN = ("UAL", "Feinberg & Mallatt")          # origin-level accounts, tallied apart

df = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else "theory_predictions_matrix.csv")
df["code"] = df["code"].str.strip()
if "row_class" not in df:
    df["row_class"] = ["origin-level" if t in ORIGIN else "trial-level" for t in df["theory"]]

# 1. compact matrix, theories in the order they appear in the file
order = list(dict.fromkeys(df["theory"]))
view = df.pivot(index="theory", columns="quantity_id", values="code").replace(SYM).loc[order]
print(view.to_string(), "\n")

# 2. tallies: YES and YES(negative) reported apart, trial-level and origin-level apart
def tally(d):
    t = d.groupby("quantity_id")["code"].value_counts().unstack(fill_value=0)
    for c in SYM:
        t[c] = t.get(c, 0)
    t = t[list(SYM)].rename(columns={"YES": "YES", "YES (negative)": "YES(neg)"})
    t["n"] = t.sum(axis=1)
    return t

for scope, sub in [("trial-level", df[df.row_class == "trial-level"]),
                   ("origin-level", df[df.row_class == "origin-level"]),
                   ("all rows", df)]:
    print(f"== {scope} ({sub.theory.nunique()} accounts)")
    print(tally(sub).to_string(), "\n")

# 3. least-favourable reclassification: promote every IMPLICIT to YES
tl = df[df.row_class == "trial-level"]
promoted = tl.assign(code=tl.code.replace({"IMPLICIT": "YES"}))
print("== stated predictions per column, trial-level, IMPLICIT promoted to YES")
print(promoted[promoted.code == "YES"].groupby("quantity_id").size().to_string())
