#!/usr/bin/env python
"""
agreement.py -- inter-coder agreement for the S1 (theory x quantity) and
S2 (study inventory) codings of the manuscript
"Tested on one shared quantity" (Brain Sciences, brainsci-4583950; submitted as "One quantity, nine theories").

Dependencies: numpy, pandas only (kappa is implemented here; no sklearn).

Usage
-----
  python agreement.py --s1a S1_coder1.csv --s1b S1_coder2.csv \
                      --s2a S2_coder1.csv --s2b S2_coder2.csv --out agreement_out/
  python agreement.py --selftest [--out agreement_selftest/] [--seed 1]

S1 files need columns: theory, quantity_id, code  (extra columns are kept for
the disagreement list: justification, source_label/citation_label, source_doi/citation_doi).
S2 files need columns: doi, content, theory_addressed (citation_label kept if present).

Outputs (in --out):
  agreement_summary.csv / agreement_summary.md   -- all statistics
  s1_per_column_kappa.csv                        -- kappa per quantity (M1..M8) and per theory
  s1_confusion_4level.csv                        -- coder A x coder B cross-tab on the 4-level code
  disagreements_S1.csv / disagreements_S2.csv    -- cells to adjudicate
"""
from __future__ import annotations
import argparse, os, re, sys
import numpy as np
import pandas as pd

# ---------------------------------------------------------------- codes
CODES4 = ["NO", "IMPLICIT", "YES", "Y(neg)"]
ORD3 = ["NO", "IMPLICIT", "YES"]          # ordinal collapse; Y(neg) -> YES
NONE_LABEL = "none of the coded theories"


def norm_code(x) -> str:
    """Map any spelling of the four codes to canonical form; unknown -> 'MISSING'."""
    if pd.isna(x):
        return "MISSING"
    s = re.sub(r"\s+", "", str(x)).upper()
    if s in ("YES",):
        return "YES"
    if s in ("IMPLICIT", "IMPL"):
        return "IMPLICIT"
    if s in ("NO", "NONE"):
        return "NO"
    if re.fullmatch(r"(Y|YES)\(?(NEG|NEGATIVE)\)?", s) or s in ("Y(NEG)", "YES(NEGATIVE)", "YNEG"):
        return "Y(neg)"
    return "MISSING"


def collapse_ord(c: str) -> str:
    return "YES" if c == "Y(neg)" else c


def norm_doi(x) -> str:
    s = str(x).strip().lower()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s)
    return s


THEORY_ALIASES = {  # spelling variants -> canonical key (both coders' files pass through this)
    "gnwt": "gnwt", "global neuronal workspace": "gnwt", "gnw": "gnwt",
    "iit": "iit", "iit (3.0/4.0)": "iit", "integrated information theory": "iit",
    "rpt": "rpt", "recurrent processing (rpt)": "rpt", "recurrent processing theory": "rpt",
    "hot / hoss": "hot / hoss", "hot/hoss": "hot / hoss",
    "hot": "hot", "hot (higher-order theory)": "hot", "higher-order theory": "hot",
    "hoss": "hoss", "hoss (higher-order state space)": "hoss",
    "ast": "ast", "attention schema theory": "ast",
    "pp": "pp", "predictive processing / beast machine": "pp", "predictive processing": "pp", "beast machine": "pp",
    "sit / passive frame theory": "sit / passive frame theory", "sit/pft": "sit / passive frame theory",
    "sit": "sit", "sit (supramodular interaction theory)": "sit", "supramodular interaction theory": "sit",
    "passive frame theory": "passive frame theory", "pft": "passive frame theory",
    "ual": "ual", "unlimited associative learning": "ual",
    "feinberg & mallatt": "feinberg & mallatt", "f&m": "feinberg & mallatt", "feinberg and mallatt": "feinberg & mallatt",
    "neural subjective frame (tallon-baudry)": "neural subjective frame", "neural subjective frame": "neural subjective frame", "tallon-baudry": "neural subjective frame",
}


def norm_theory(x) -> str:
    s = re.sub(r"\s+", " ", str(x).strip().lower())
    return THEORY_ALIASES.get(s, s)


def norm_text(x) -> str:
    if pd.isna(x):
        return "MISSING"
    return re.sub(r"\s+", " ", str(x).strip().lower())


# ---------------------------------------------------------------- kappa
def confusion(a, b, labels):
    idx = {l: i for i, l in enumerate(labels)}
    m = np.zeros((len(labels), len(labels)), dtype=float)
    for x, y in zip(a, b):
        m[idx[x], idx[y]] += 1
    return m


def cohen_kappa(a, b, labels=None, weights: str | None = None):
    """Cohen's kappa by hand.
    weights=None -> unweighted; 'linear' -> linear disagreement weights |i-j|/(k-1)
    over the ORDER given by `labels`; 'quadratic' -> ((i-j)/(k-1))^2.
    Returns dict(kappa, po, pe, n, se) ; kappa is NaN when pe == 1 (no variance)."""
    a = list(a); b = list(b)
    if labels is None:
        labels = sorted(set(a) | set(b))
    k = len(labels)
    O = confusion(a, b, labels)
    n = O.sum()
    if n == 0:
        return dict(kappa=np.nan, po=np.nan, pe=np.nan, n=0, se=np.nan)
    P = O / n
    ra, cb = P.sum(1), P.sum(0)
    E = np.outer(ra, cb)
    if weights is None:
        W = 1.0 - np.eye(k)
    else:
        i, j = np.indices((k, k))
        d = np.abs(i - j) / max(k - 1, 1)
        W = d if weights == "linear" else d ** 2
    do = (W * P).sum()                 # observed weighted disagreement
    de = (W * E).sum()                 # expected weighted disagreement
    po, pe = 1 - do, 1 - de
    kappa = np.nan if de == 0 else 1 - do / de
    # large-sample SE for unweighted kappa (Fleiss, Cohen & Everitt 1969 first-order approx.)
    se = np.nan
    if weights is None and not np.isnan(kappa) and pe < 1:
        se = float(np.sqrt(po * (1 - po) / (n * (1 - pe) ** 2)))
    return dict(kappa=float(kappa), po=float(po), pe=float(pe), n=int(n), se=se)


def pct_agree(a, b):
    a = np.asarray(list(a)); b = np.asarray(list(b))
    return float((a == b).mean()) if len(a) else np.nan


def interpret(k):
    """Landis & Koch (1977) descriptive band."""
    if np.isnan(k):
        return "undefined"
    bands = [(0.0, "poor"), (0.2, "slight"), (0.4, "fair"), (0.6, "moderate"), (0.8, "substantial"), (1.01, "almost perfect")]
    for thr, lab in bands:
        if k < thr:
            return lab
    return "almost perfect"


def md_table(df: pd.DataFrame, index=True) -> str:
    """Markdown table without the optional 'tabulate' dependency."""
    d = df.reset_index() if index else df
    cols = [str(c) for c in d.columns]
    fmt = lambda v: f"{v:.3f}" if isinstance(v, float) else str(v)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in d.itertuples(index=False)]
    return "\n".join(lines)


# ---------------------------------------------------------------- S1
def load_s1(path):
    df = pd.read_csv(path)
    need = {"theory", "quantity_id", "code"}
    if not need <= set(df.columns):
        sys.exit(f"{path}: needs columns {need}, has {list(df.columns)}")
    df = df.copy()
    df["theory_k"] = df["theory"].map(norm_theory)
    df["q_k"] = df["quantity_id"].astype(str).str.strip().str.upper()
    df["code_n"] = df["code"].map(norm_code)
    just = next((c for c in ["justification", "prediction"] if c in df.columns), None)
    src = next((c for c in ["source_label", "citation_label"] if c in df.columns), None)
    doi = next((c for c in ["source_doi", "citation_doi"] if c in df.columns), None)
    df["_just"] = df[just] if just else ""
    df["_src"] = df[src] if src else ""
    df["_doi"] = df[doi] if doi else ""
    df["cell_origin"] = df["cell_origin"] if "cell_origin" in df.columns else np.nan
    return df[["theory", "theory_k", "quantity_id", "q_k", "code_n", "_just", "_src", "_doi", "cell_origin"]]


def analyse_s1(pa, pb, exclude=()):
    A, B = load_s1(pa), load_s1(pb)
    if exclude:
        keep = lambda d: d[~(d.theory_k + " | " + d.theory.astype(str).str.lower()).apply(lambda t: any(e.lower() in t for e in exclude))]
        A, B = keep(A), keep(B)
    m = A.merge(B, on=["theory_k", "q_k"], suffixes=("_A", "_B"), how="inner")
    only_a = sorted(set(A.theory_k) - set(B.theory_k)); only_b = sorted(set(B.theory_k) - set(A.theory_k))
    unmatched = len(A) + len(B) - 2 * len(m)
    n_merged = len(m)
    m = m[(m.code_n_A != "MISSING") & (m.code_n_B != "MISSING")].copy()
    res = {}
    res["S1_n_cells_compared"] = len(m)
    res["S1_n_rows_unmatched"] = unmatched
    res["S1_n_cells_missing_code"] = n_merged - len(m)
    res["S1_theory_blocks_only_in_file1"] = "; ".join(only_a) if only_a else "-"
    res["S1_theory_blocks_only_in_file2"] = "; ".join(only_b) if only_b else "-"
    if unmatched:
        print(f"WARNING: {unmatched} S1 rows had no counterpart (theory blocks only in file 1: {only_a}; only in file 2: {only_b}). "
              "Both coders must fill the same row set (the 88-row form) before the headline kappa is meaningful.", file=sys.stderr)
    # 4-level nominal
    k4 = cohen_kappa(m.code_n_A, m.code_n_B, CODES4)
    res["S1_code4_pct_agreement"] = pct_agree(m.code_n_A, m.code_n_B)
    res["S1_code4_kappa_unweighted"] = k4["kappa"]
    res["S1_code4_kappa_se"] = k4["se"]
    res["S1_code4_pe"] = k4["pe"]
    # ordinal collapse
    oa, ob = m.code_n_A.map(collapse_ord), m.code_n_B.map(collapse_ord)
    res["S1_ord3_pct_agreement"] = pct_agree(oa, ob)
    res["S1_ord3_kappa_unweighted"] = cohen_kappa(oa, ob, ORD3)["kappa"]
    res["S1_ord3_kappa_linear_weighted"] = cohen_kappa(oa, ob, ORD3, weights="linear")["kappa"]
    # 'is there a stated prediction' binary: {YES, Y(neg)} vs {IMPLICIT, NO}
    sa, sb = oa.eq("YES"), ob.eq("YES")
    res["S1_stated_prediction_binary_kappa"] = cohen_kappa(sa, sb, [False, True])["kappa"]
    res["S1_stated_prediction_binary_pct"] = pct_agree(sa, sb)
    # IMPLICIT/NO boundary (restricted to cells where neither coder said YES/Y(neg))
    sub = m[(oa != "YES") & (ob != "YES")]
    res["S1_IMPLICIT_vs_NO_n_cells"] = len(sub)
    res["S1_IMPLICIT_vs_NO_kappa"] = cohen_kappa(sub.code_n_A, sub.code_n_B, ["NO", "IMPLICIT"])["kappa"] if len(sub) else np.nan
    # Y(neg) reported separately
    na, nb = m.code_n_A.eq("Y(neg)"), m.code_n_B.eq("Y(neg)")
    res["S1_Yneg_n_A"] = int(na.sum()); res["S1_Yneg_n_B"] = int(nb.sum())
    res["S1_Yneg_n_both"] = int((na & nb).sum())
    res["S1_Yneg_flag_kappa"] = cohen_kappa(na, nb, [False, True])["kappa"]
    # per column / per theory
    rows = []
    for q, g in m.groupby("q_k"):
        kk = cohen_kappa(g.code_n_A, g.code_n_B, CODES4)
        rows.append(dict(unit="quantity", level=q, n=len(g), pct_agreement=pct_agree(g.code_n_A, g.code_n_B),
                         kappa_4level=kk["kappa"], pe=kk["pe"],
                         kappa_ord3_linear=cohen_kappa(g.code_n_A.map(collapse_ord), g.code_n_B.map(collapse_ord), ORD3, "linear")["kappa"]))
    for t, g in m.groupby("theory_A"):
        kk = cohen_kappa(g.code_n_A, g.code_n_B, CODES4)
        rows.append(dict(unit="theory", level=t, n=len(g), pct_agreement=pct_agree(g.code_n_A, g.code_n_B),
                         kappa_4level=kk["kappa"], pe=kk["pe"],
                         kappa_ord3_linear=cohen_kappa(g.code_n_A.map(collapse_ord), g.code_n_B.map(collapse_ord), ORD3, "linear")["kappa"]))
    # blindness subsets: cells whose condensed codes appeared in the submitted manuscript vs cells added in revision.
    # Uses a cell_origin column if either file carries one; otherwise infers from theory names added in revision.
    oc = next((c for c in ("cell_origin_A", "cell_origin_B", "cell_origin") if c in m.columns and m[c].notna().any()), None)
    origin = m[oc].astype(str) if oc else m.theory_A.astype(str).str.lower().apply(
        lambda t: "added-in-revision" if any(k in t for k in ("passive frame", "subjective frame")) else "submitted-v1")
    for sub_name, g in m.groupby(origin):
        if len(g) < 2:
            continue
        kk = cohen_kappa(g.code_n_A, g.code_n_B, CODES4)
        rows.append(dict(unit="subset", level=sub_name, n=len(g), pct_agreement=pct_agree(g.code_n_A, g.code_n_B),
                         kappa_4level=kk["kappa"], pe=kk["pe"],
                         kappa_ord3_linear=cohen_kappa(g.code_n_A.map(collapse_ord), g.code_n_B.map(collapse_ord), ORD3, "linear")["kappa"]))
        tag = "submitted" if sub_name.startswith("submitted") else "added"
        res[f"S1_subset_{tag}_n"] = len(g)
        res[f"S1_subset_{tag}_pct_agreement"] = pct_agree(g.code_n_A, g.code_n_B)
        res[f"S1_subset_{tag}_kappa_4level"] = kk["kappa"]
        res[f"S1_subset_{tag}_kappa_ord3_linear"] = rows[-1]["kappa_ord3_linear"]
    percol = pd.DataFrame(rows)
    conf = pd.DataFrame(confusion(m.code_n_A, m.code_n_B, CODES4), index=[f"A:{c}" for c in CODES4], columns=[f"B:{c}" for c in CODES4]).astype(int)
    dis = m[m.code_n_A != m.code_n_B][["theory_A", "quantity_id_A", "code_n_A", "code_n_B", "_just_A", "_just_B", "_src_A", "_doi_A", "_src_B", "_doi_B"]]
    dis = dis.rename(columns={"theory_A": "theory", "quantity_id_A": "quantity_id", "code_n_A": "code_coder1", "code_n_B": "code_coder2",
                              "_just_A": "justification_coder1", "_just_B": "justification_coder2",
                              "_src_A": "source_coder1", "_doi_A": "doi_coder1", "_src_B": "source_coder2", "_doi_B": "doi_coder2"})
    sev = {("NO", "YES"): 2, ("YES", "NO"): 2, ("NO", "Y(neg)"): 2, ("Y(neg)", "NO"): 2}
    dis.insert(4, "severity", [sev.get((a, b), 1) for a, b in zip(dis.code_coder1, dis.code_coder2)])
    dis.insert(5, "adjudicated_code", "")
    dis.insert(6, "adjudication_note", "")
    return res, percol, conf, dis.sort_values(["severity", "quantity_id"], ascending=[False, True])


# ---------------------------------------------------------------- S2
def load_s2(path):
    df = pd.read_csv(path)
    need = {"doi", "content", "theory_addressed"}
    if not need <= set(df.columns):
        sys.exit(f"{path}: needs columns {need}, has {list(df.columns)}")
    df = df.copy()
    df["doi_k"] = df["doi"].map(norm_doi)
    df["content_n"] = df["content"].map(norm_text)
    df["ta_n"] = df["theory_addressed"].map(norm_text)
    df["ta_flag"] = df["ta_n"].map(lambda s: "MISSING" if s == "MISSING" else (s != NONE_LABEL))
    df["label"] = df["citation_label"] if "citation_label" in df.columns else df["doi"]
    return df[["label", "doi", "doi_k", "content_n", "ta_n", "ta_flag"]]


def analyse_s2(pa, pb):
    A, B = load_s2(pa), load_s2(pb)
    m = A.merge(B, on="doi_k", suffixes=("_A", "_B"), how="inner")
    res = {"S2_n_studies_compared": len(m), "S2_n_unmatched": len(A) + len(B) - 2 * len(m)}
    c = m[(m.content_n_A != "MISSING") & (m.content_n_B != "MISSING")]
    res["S2_content_pct_agreement"] = pct_agree(c.content_n_A, c.content_n_B)
    res["S2_content_kappa"] = cohen_kappa(c.content_n_A, c.content_n_B)["kappa"]
    t = m[(m.ta_flag_A != "MISSING") & (m.ta_flag_B != "MISSING")]
    res["S2_theory_addressed_binary_pct_agreement"] = pct_agree(t.ta_flag_A, t.ta_flag_B)
    res["S2_theory_addressed_binary_kappa"] = cohen_kappa(t.ta_flag_A, t.ta_flag_B, [False, True])["kappa"]
    res["S2_theory_addressed_label_pct_agreement"] = pct_agree(t.ta_n_A, t.ta_n_B)
    res["S2_theory_addressed_label_kappa"] = cohen_kappa(t.ta_n_A, t.ta_n_B)["kappa"]
    dis = m[(m.content_n_A != m.content_n_B) | (m.ta_n_A != m.ta_n_B)][["label_A", "doi_A", "content_n_A", "content_n_B", "ta_n_A", "ta_n_B"]]
    dis = dis.rename(columns={"label_A": "citation_label", "doi_A": "doi", "content_n_A": "content_coder1", "content_n_B": "content_coder2",
                              "ta_n_A": "theory_addressed_coder1", "ta_n_B": "theory_addressed_coder2"})
    dis["adjudicated_content"] = ""; dis["adjudicated_theory_addressed"] = ""; dis["adjudication_note"] = ""
    return res, dis


# ---------------------------------------------------------------- output
def write_outputs(out, res, percol=None, conf=None, dis1=None, dis2=None, title="Inter-coder agreement"):
    os.makedirs(out, exist_ok=True)
    summ = pd.DataFrame({"statistic": list(res.keys()), "value": list(res.values())})
    summ.to_csv(os.path.join(out, "agreement_summary.csv"), index=False)
    if percol is not None:
        percol.to_csv(os.path.join(out, "s1_per_column_kappa.csv"), index=False)
    if conf is not None:
        conf.to_csv(os.path.join(out, "s1_confusion_4level.csv"))
    if dis1 is not None:
        dis1.to_csv(os.path.join(out, "disagreements_S1.csv"), index=False)
    if dis2 is not None:
        dis2.to_csv(os.path.join(out, "disagreements_S2.csv"), index=False)
    L = [f"# {title}", ""]
    L += ["| statistic | value |", "|---|---|"]
    for k, v in res.items():
        vs = f"{v:.3f}" if isinstance(v, float) else str(v)
        L.append(f"| {k} | {vs} |")
    if "S1_code4_kappa_unweighted" in res:
        L += ["", f"Landis–Koch band for the 4-level unweighted kappa: **{interpret(res['S1_code4_kappa_unweighted'])}**."]
    if conf is not None:
        L += ["", "## S1 confusion (rows coder 1, columns coder 2)", "", md_table(conf)]
    if percol is not None and len(percol):
        L += ["", "## S1 per-column and per-theory kappa", "", md_table(percol, index=False)]
    if dis1 is not None:
        L += ["", f"## S1 disagreements for adjudication (n = {len(dis1)}; severity 2 = NO vs YES/Y(neg))", "",
              md_table(dis1[["theory", "quantity_id", "code_coder1", "code_coder2", "severity"]], index=False)]
    if dis2 is not None:
        L += ["", f"## S2 disagreements for adjudication (n = {len(dis2)})", "",
              md_table(dis2[["citation_label", "content_coder1", "content_coder2", "theory_addressed_coder1", "theory_addressed_coder2"]], index=False)]
    L += ["", "Kappa is Cohen's kappa computed from the coder-by-coder cross-tabulation (unweighted: disagreement weight 1 off the diagonal; "
          "linear: weight |i−j|/(k−1) over the ordinal collapse NO < IMPLICIT < YES with Y(neg) mapped to YES). "
          "Undefined (NaN) kappa means both coders used a single category, so chance agreement is 1 and kappa has no value; the percentage agreement is still reported."]
    with open(os.path.join(out, "agreement_summary.md"), "w") as f:
        f.write("\n".join(L) + "\n")


# ---------------------------------------------------------------- self-test
def _perturb(codes, labels, p_agree, rng):
    out = []
    for c in codes:
        if rng.random() < p_agree:
            out.append(c)
        else:
            others = [l for l in labels if l != c]
            out.append(others[rng.integers(len(others))])
    return out


def selftest(out, seed=1, p_agree=0.80, n_reps=200):
    rng = np.random.default_rng(seed)
    # 1) hand-checked 2x2 table: a=20,b=5,c=10,d=15  -> po=0.70, pe=0.50, kappa=0.40
    a = ["x"] * 25 + ["y"] * 25
    b = ["x"] * 20 + ["y"] * 5 + ["x"] * 10 + ["y"] * 15
    k = cohen_kappa(a, b, ["x", "y"])
    assert abs(k["kappa"] - 0.40) < 1e-12 and abs(k["po"] - 0.70) < 1e-12, k
    # 2) weighted kappa == unweighted for 2 categories; identical -> 1; linear weights sanity
    assert abs(cohen_kappa(a, b, ["x", "y"], "linear")["kappa"] - 0.40) < 1e-12
    assert cohen_kappa(a, a, ["x", "y"])["kappa"] == 1.0
    # 3) synthetic S1: 96 cells, marginals roughly like a sparse matrix
    theories = [f"T{i}" for i in range(12)]; quants = [f"M{i}" for i in range(1, 9)]
    base = pd.DataFrame([(t, q) for t in theories for q in quants], columns=["theory", "quantity_id"])
    probs = [0.52, 0.24, 0.22, 0.02]  # NO, IMPLICIT, YES, Y(neg)
    ks, pos, kws = [], [], []
    for r in range(n_reps):
        c1 = list(rng.choice(CODES4, size=len(base), p=probs))
        c2 = _perturb(c1, CODES4, p_agree, rng)
        kk = cohen_kappa(c1, c2, CODES4)
        ks.append(kk["kappa"]); pos.append(kk["po"])
        kws.append(cohen_kappa([collapse_ord(x) for x in c1], [collapse_ord(x) for x in c2], ORD3, "linear")["kappa"])
    # analytic expectation for this generator: po = p_agree exactly in expectation; pe from marginals
    p = np.array(probs); pe_th = float((p * (p_agree * p + (1 - p_agree) * (1 - p) / 3)).sum())
    k_th = (p_agree - pe_th) / (1 - pe_th)
    # write one concrete replicate through the full pipeline
    c1 = list(rng.choice(CODES4, size=len(base), p=probs)); c2 = _perturb(c1, CODES4, p_agree, rng)
    s1a = base.assign(code=c1, justification="sim", source_label="sim", source_doi="10.0/sim")
    s1b = base.assign(code=[{"Y(neg)": "YES (negative)"}.get(x, x.lower()) for x in c2], justification="sim", source_label="sim", source_doi="10.0/sim")
    os.makedirs(out, exist_ok=True)
    s1a.to_csv(os.path.join(out, "sim_S1_coder1.csv"), index=False); s1b.to_csv(os.path.join(out, "sim_S1_coder2.csv"), index=False)
    cats = ["neutral-visual", "valenced", "interoceptive", "motor-conflict", "state (no content)", "neutral-nonvisual"]
    tas = ["GNWT", "IIT", "HOT/HOSS", "SIT", NONE_LABEL]
    dois = [f"10.0/sim{i}" for i in range(36)]
    ca = list(rng.choice(cats, 36, p=[.6, .12, .06, .1, .08, .04])); ta = list(rng.choice(tas, 36, p=[.4, .15, .15, .12, .18]))
    s2a = pd.DataFrame(dict(citation_label=dois, doi=dois, content=ca, theory_addressed=ta))
    s2b = pd.DataFrame(dict(citation_label=dois, doi=[d.upper() for d in dois], content=_perturb(ca, cats, p_agree, rng), theory_addressed=_perturb(ta, tas, p_agree, rng)))
    s2a.to_csv(os.path.join(out, "sim_S2_coder1.csv"), index=False); s2b.to_csv(os.path.join(out, "sim_S2_coder2.csv"), index=False)
    res1, percol, conf, dis1 = analyse_s1(os.path.join(out, "sim_S1_coder1.csv"), os.path.join(out, "sim_S1_coder2.csv"))
    res2, dis2 = analyse_s2(os.path.join(out, "sim_S2_coder1.csv"), os.path.join(out, "sim_S2_coder2.csv"))
    assert res1["S1_n_cells_compared"] == 96 and res2["S2_n_studies_compared"] == 36
    res = {"selftest_hand_2x2_kappa": 0.40, "selftest_p_agree_simulated": p_agree, "selftest_n_reps": n_reps,
           "selftest_S1_po_mean": float(np.mean(pos)), "selftest_S1_kappa4_mean": float(np.mean(ks)), "selftest_S1_kappa4_sd": float(np.std(ks)),
           "selftest_S1_kappa4_analytic": float(k_th), "selftest_S1_pe_analytic": pe_th,
           "selftest_S1_kappa_ord3_linear_mean": float(np.mean(kws)), **res1, **res2}
    write_outputs(out, res, percol, conf, dis1, dis2, title="agreement.py self-test on synthetic data")
    return res


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--s1a"); ap.add_argument("--s1b"); ap.add_argument("--s2a"); ap.add_argument("--s2b")
    ap.add_argument("--out", default="agreement_out")
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--exclude-theories", default="", help="comma-separated theory-name substrings to drop before computing S1 kappa (e.g. 'tallon')")
    args = ap.parse_args(argv)
    if args.selftest:
        res = selftest(args.out if args.out != "agreement_out" else "agreement_selftest", seed=args.seed)
        for k in ["selftest_p_agree_simulated", "selftest_S1_po_mean", "selftest_S1_kappa4_mean", "selftest_S1_kappa4_analytic", "selftest_S1_kappa_ord3_linear_mean"]:
            print(f"{k}: {res[k]:.3f}")
        return
    res = {}; percol = conf = dis1 = dis2 = None
    if args.s1a and args.s1b:
        excl = [e.strip() for e in args.exclude_theories.split(",") if e.strip()]
        r1, percol, conf, dis1 = analyse_s1(args.s1a, args.s1b, exclude=excl); res.update(r1)
    if args.s2a and args.s2b:
        r2, dis2 = analyse_s2(args.s2a, args.s2b); res.update(r2)
    if not res:
        ap.error("provide --s1a/--s1b and/or --s2a/--s2b, or --selftest")
    write_outputs(args.out, res, percol, conf, dis1, dis2)
    for k, v in res.items():
        print(f"{k}: {v:.3f}" if isinstance(v, float) else f"{k}: {v}")


if __name__ == "__main__":
    main()
