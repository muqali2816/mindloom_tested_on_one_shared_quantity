#!/usr/bin/env python
"""
agreement.py (v2.1) -- inter-coder agreement for the Table S1 (theory x measurable quantity)
coding of the manuscript "Tested on one shared quantity" (Brain Sciences, brainsci-4583950,
revision 1), and for the legacy Table S2 (study inventory) coding.

Dependencies: numpy, pandas only (Cohen's kappa is implemented here; no sklearn).

Usage
-----
  python agreement.py --s1a S1_coder1.csv --s1b S1_coder2.csv \
        --accounts accounts_manifest.csv --domains domains_manifest.csv \
        [--code-scheme v2|legacy] [--ci none|multinomial|bootstrap-by-theory] --out agreement_out/
  python agreement.py --s2a S2_coder1.csv --s2b S2_coder2.csv [--s2-reference S2_coder1.csv] --out agreement_out/
        (S2: v2 experiment-unit form auto-detected by experiment_id; legacy study-unit form otherwise)
  python agreement.py --selftest [--out agreement_selftest/] [--seed 1]

Row matching (S1)
-----------------
Rows are matched on the key (theory_id, domain_id).  Both are validated against the two
manifests: `accounts_manifest.csv` (columns theory_id, theory, row_class, origin, note) and
`domains_manifest.csv` (columns domain_id, domain).  Completeness (v2.1): EACH file must contain exactly
the accounts x domains grid of the manifests (12 x 10 = 120 keys); missing or extra keys abort the run
(--allow-partial-grid downgrades this to a loud warning, for the 88-cell deposit-v1.3 comparison only).
A file may give `theory_id` directly, or a
`theory` name that is resolved through the manifest's `theory` column and a small alias table
(--extra-alias 'HOT / HOSS=HOT' adds more).  Any theory that cannot be resolved, or any domain_id
not in the manifest, aborts the run with a message naming the offending values -- nothing is
silently dropped.  Domain ids are accepted as `domain_id` or the legacy `quantity_id`.

Code schemes (--code-scheme)
----------------------------
  v2 (default)  EXPLICIT / INTERPRETED / NOT_LOCATED / NOT_APPLICABLE / UNRESOLVED, plus a
                `polarity` column (positive / stated_null / negative) that is REQUIRED for EXPLICIT and
                INTERPRETED cells and ignored otherwise.  NOT_LOCATED is "no statement found in
                the examined corpus"; it is not a prediction of no effect (that is EXPLICIT + null).
  legacy        YES / IMPLICIT / NO / YES (negative) as used in deposit v1.3 (88 cells).
Positive cells (v2: EXPLICIT, INTERPRETED; legacy: YES, IMPLICIT, YES (negative)) must carry a
non-empty `source_doi` (or `citation_doi`); a missing DOI in a positive cell aborts the run.

Statistics, in the order they are reported
------------------------------------------
  1. raw (percentage) agreement, as k of n and as a proportion;
  2. the full coder-1 x coder-2 confusion matrix on the code (v2 also on code x polarity);
  3. nominal (unweighted) Cohen's kappa on the code (v2 also on code x polarity);
  4. kappa per domain (M1 ... M8) and per theory;
  5. kappa for the subsets origin = submitted-v1 vs added-in-revision.  The subset label is taken
     from a cell-level column `origin` or `added_in_revision` if present in the coder-1 file,
     otherwise inferred: a cell is added-in-revision when the theory's `origin` in the accounts
     manifest is `added-in-revision` OR its domain_id is in --added-domains (default M4a,M4b,M4c,
     the three-way split of the former M4 column).

Confidence intervals (--ci, default none)
-----------------------------------------
No interval is reported by default, on purpose.  The 88-120 cells of Table S1 are not
independent observations: the cells of one theory are coded from the same three to five
primary sources, by the same two readers, under one reading of what that theory commits to.
Disagreement therefore clusters by theory.  The multinomial (Fleiss-Cohen-Everitt, large-sample)
standard error and a naive cell-level bootstrap both treat cells as exchangeable and are
optimistic -- they understate the sampling variance and give intervals that are too narrow.
  --ci multinomial           first-order large-sample SE for unweighted kappa (reported with the
                             caveat above; for comparison only);
  --ci bootstrap-by-theory   percentile 95 % interval from resampling THEORIES as clusters
                             (with replacement, keeping each theory's cells together).  With 12
                             clusters the interval is itself coarse and should be read as
                             indicative.  Seeded (--seed); 2000 replicates.
A 'nominal' kappa means a point estimate with no interval attached.

S2 v2 (experiment unit; v2.1 rules)
------------------------------------
  Vocabularies are strict: modality in {visual, auditory, tactile, motor, interoceptive, mixed, not applicable};
  affective_status in {neutral, valenced, interoceptive}; report_type in {report, no-report, both};
  contested_inclusion in {True, False}.  UNRESOLVED is accepted in every field as its OWN category (never collapsed;
  n_UNRESOLVED is reported per coder).  A trailing parenthetical qualifier is stripped before the check
  ('both (targets reported; ...)' -> both).  Any other value aborts, naming the row and the value.
  Attribution by the authors: a cell is 'no attribution' when empty or matching
  ^(none|not named|no theory|n/a|-|not verifiable)\b (case-insensitive), so 'none named (abstract-only)' is False.
  Otherwise the theory ids are taken from the optional column theory_attribution_by_authors_ids (semicolon-separated
  theory_ids of the accounts manifest, validated), or extracted from the free text by matching manifest names / ids.
  Coders are compared on the binary flag AND on the exact SET of theory ids (reported separately); rows whose text
  names no recognisable theory are listed as unparseable.  Both files must contain the experiment_id set of the
  reference file (--s2-reference, default: the coder-1 file); the count is reported.

Self-test (--selftest)
----------------------
Positive case: 12 theories x 10 domains, coder 2 agrees with coder 1 on 80 % of cells and picks a
random other code otherwise; the recovered kappa must match the analytic value for that
generator within Monte Carlo error.  Negative cases -- each must ABORT with a clear message:
duplicated key; theory alias not in manifest; typo in a code; NaN code; mismatched row sets;
DOI missing (NaN) in a positive cell.  v2.1 adds: none-named attribution flagged True; wrong theory id
undetected; invalid modality accepted; truncated S1 accepted; S2 id set mismatch accepted.  The self-test exits
non-zero if any case does not behave as required.

Outputs (in --out)
------------------
  agreement_summary.csv / agreement_summary.md   -- all statistics in the order above
  s1_confusion_code.csv (+ s1_confusion_code_polarity.csv for v2)
  s1_per_domain_kappa.csv                        -- per domain and per theory
  s1_subset_kappa.csv                            -- submitted-v1 vs added-in-revision
  disagreements_S1.csv (/ disagreements_S2.csv)  -- cells to adjudicate
"""
from __future__ import annotations
import argparse, os, re, sys
import numpy as np
import pandas as pd

__version__ = "2.4"

# ---------------------------------------------------------------- code schemes
V2_CODES = ["EXPLICIT", "INTERPRETED", "NOT_LOCATED", "NOT_APPLICABLE", "UNRESOLVED"]
V2_POSITIVE = {"EXPLICIT", "INTERPRETED"}            # cells that must carry a DOI and a polarity
POLARITIES = ["positive", "stated_null", "negative"]
LEGACY_CODES = ["NO", "IMPLICIT", "YES", "Y(neg)"]
LEGACY_POSITIVE = {"YES", "IMPLICIT", "Y(neg)"}
NONE_LABEL = "none of the coded theories"
DEFAULT_ADDED_DOMAINS = ("M4a", "M4b", "M4c")

SCHEMES = {
    "v2": dict(codes=V2_CODES, positive=V2_POSITIVE, valid_str="EXPLICIT / INTERPRETED / NOT_LOCATED / NOT_APPLICABLE / UNRESOLVED"),
    "legacy": dict(codes=LEGACY_CODES, positive=LEGACY_POSITIVE, valid_str="YES / IMPLICIT / NO / YES (negative)"),
}


class ValidationError(SystemExit):
    """Raised (as SystemExit with a message) whenever the input cannot be analysed safely."""
    def __init__(self, msg):
        super().__init__("VALIDATION FAILED: " + msg)


def norm_code_legacy(x) -> str:
    """Map any spelling of the four legacy codes to canonical form; unknown/empty -> 'MISSING'."""
    if pd.isna(x):
        return "MISSING"
    s = re.sub(r"\s+", "", str(x)).upper()
    if s == "YES":
        return "YES"
    if s in ("IMPLICIT", "IMPL"):
        return "IMPLICIT"
    if s in ("NO", "NONE"):
        return "NO"
    if re.fullmatch(r"(Y|YES)\(?(NEG|NEGATIVE)\)?", s) or s in ("Y(NEG)", "YES(NEGATIVE)", "YNEG"):
        return "Y(neg)"
    return "MISSING"


def norm_code_v2(x) -> str:
    """Map any spelling of the five v2 codes to canonical form; unknown/empty -> 'MISSING'."""
    if pd.isna(x):
        return "MISSING"
    s = re.sub(r"[\s\-]+", "_", str(x).strip()).upper()
    aliases = {"EXPLICIT": "EXPLICIT", "STATED": "EXPLICIT",
               "INTERPRETED": "INTERPRETED", "INFERRED": "INTERPRETED",
               "NOT_LOCATED": "NOT_LOCATED", "NOTLOCATED": "NOT_LOCATED",
               "NOT_APPLICABLE": "NOT_APPLICABLE", "NOTAPPLICABLE": "NOT_APPLICABLE", "N/A": "NOT_APPLICABLE", "NA": "NOT_APPLICABLE",
               "UNRESOLVED": "UNRESOLVED", "CONFLICTING": "UNRESOLVED"}
    return aliases.get(s, "MISSING")


def norm_polarity(x) -> str:
    if pd.isna(x):
        return ""
    s = str(x).strip().lower()
    aliases = {"positive": "positive", "pos": "positive", "+": "positive",
               "stated_null": "stated_null", "null": "stated_null", "zero": "stated_null", "no effect": "stated_null", "0": "stated_null",
               "negative": "negative", "neg": "negative", "-": "negative"}
    return aliases.get(s, "INVALID")


def norm_doi(x) -> str:
    if pd.isna(x):
        return ""
    s = str(x).strip().lower()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s)
    return "" if s in ("", "nan", "none", "na") else s


def read_csv_strict(path):
    """Read a coding table without pandas' default NA list: the polarity value 'null' and the code
    alias 'NA' must survive as strings. Only the empty field is treated as missing."""
    return pd.read_csv(path, keep_default_na=False, na_values=[""])


def norm_text(x) -> str:
    if pd.isna(x):
        return "MISSING"
    return re.sub(r"\s+", " ", str(x).strip().lower())


# ---------------------------------------------------------------- manifests
BUILTIN_ALIASES = {  # lower-cased spelling -> theory_id; the manifest's own `theory` and `theory_id` columns are added at load time
    "gnwt": "GNWT", "global neuronal workspace": "GNWT", "gnw": "GNWT",
    "iit": "IIT", "iit (3.0/4.0)": "IIT", "integrated information theory": "IIT",
    "rpt": "RPT", "recurrent processing (rpt)": "RPT", "recurrent processing theory": "RPT",
    "hot": "HOT", "hot (higher-order theory)": "HOT", "higher-order theory": "HOT", "higher-order theory (hot / horor)": "HOT", "horor": "HOT",
    "hoss": "HOSS", "hoss (higher-order state space)": "HOSS", "higher-order state space": "HOSS", "higher-order state space (hoss)": "HOSS",
    "ast": "AST", "attention schema theory": "AST",
    "pp": "PP", "predictive processing / beast machine": "PP", "predictive processing": "PP", "beast machine": "PP",
    "sit": "SIT", "sit (supramodular interaction theory)": "SIT", "supramodular interaction theory": "SIT", "supramodular interaction theory (sit)": "SIT",
    "pft": "PFT", "passive frame theory": "PFT",
    "ual": "UAL", "unlimited associative learning": "UAL",
    "fm": "FM", "f&m": "FM", "feinberg & mallatt": "FM", "feinberg and mallatt": "FM",
    "nsf": "NSF", "neural subjective frame": "NSF", "neural subjective frame (tallon-baudry)": "NSF", "tallon-baudry": "NSF",
}


def load_manifests(accounts_path, domains_path, extra_alias=()):
    acc = read_csv_strict(accounts_path)
    need = {"theory_id", "theory", "row_class", "origin"}
    if not need <= set(acc.columns):
        raise ValidationError(f"accounts manifest {accounts_path} needs columns {sorted(need)}, has {list(acc.columns)}")
    if acc.theory_id.duplicated().any():
        raise ValidationError(f"accounts manifest has duplicated theory_id: {acc.theory_id[acc.theory_id.duplicated()].tolist()}")
    dom = read_csv_strict(domains_path)
    if not {"domain_id", "domain"} <= set(dom.columns):
        raise ValidationError(f"domains manifest {domains_path} needs columns ['domain_id', 'domain'], has {list(dom.columns)}")
    if dom.domain_id.duplicated().any():
        raise ValidationError(f"domains manifest has duplicated domain_id: {dom.domain_id[dom.domain_id.duplicated()].tolist()}")
    ids = set(acc.theory_id.astype(str))
    alias = {k: v for k, v in BUILTIN_ALIASES.items() if v in ids}     # never resolve to a theory that is not in the manifest
    for tid, name in zip(acc.theory_id.astype(str), acc.theory.astype(str)):
        alias[tid.lower()] = tid
        alias[re.sub(r"\s+", " ", name.strip().lower())] = tid
    for spec in extra_alias:
        if "=" not in spec:
            raise ValidationError(f"--extra-alias expects 'name=theory_id', got {spec!r}")
        k, v = spec.split("=", 1)
        v = v.strip()
        if v not in ids:
            raise ValidationError(f"--extra-alias target {v!r} is not a theory_id in the accounts manifest ({sorted(ids)})")
        alias[re.sub(r"\s+", " ", k.strip().lower())] = v
    return dict(accounts=acc.set_index("theory_id"), domains=dom.set_index("domain_id"), alias=alias,
                theory_ids=ids, domain_ids=set(dom.domain_id.astype(str)))


def resolve_theory(x, man) -> str | None:
    if pd.isna(x):
        return None
    s = re.sub(r"\s+", " ", str(x).strip().lower())
    return man["alias"].get(s)


# ---------------------------------------------------------------- kappa
def confusion(a, b, labels):
    idx = {l: i for i, l in enumerate(labels)}
    m = np.zeros((len(labels), len(labels)), dtype=float)
    for x, y in zip(a, b):
        m[idx[x], idx[y]] += 1
    return m


def cohen_kappa(a, b, labels=None, weights: str | None = None):
    """Cohen's kappa by hand.
    weights=None -> unweighted (nominal); 'linear' -> |i-j|/(k-1) over the ORDER of `labels`;
    'quadratic' -> ((i-j)/(k-1))^2.
    Returns dict(kappa, po, pe, n, n_agree, se) ; kappa is NaN when pe == 1 (no variance).
    `se` is the first-order large-sample (multinomial) SE for unweighted kappa; see the module
    docstring for why it is optimistic for clustered cells."""
    a = list(a); b = list(b)
    if labels is None:
        labels = sorted(set(a) | set(b))
    k = len(labels)
    O = confusion(a, b, labels)
    n = O.sum()
    if n == 0:
        return dict(kappa=np.nan, po=np.nan, pe=np.nan, n=0, n_agree=0, se=np.nan)
    P = O / n
    ra, cb = P.sum(1), P.sum(0)
    E = np.outer(ra, cb)
    if weights is None:
        W = 1.0 - np.eye(k)
    else:
        i, j = np.indices((k, k))
        d = np.abs(i - j) / max(k - 1, 1)
        W = d if weights == "linear" else d ** 2
    do = (W * P).sum(); de = (W * E).sum()
    po, pe = 1 - do, 1 - de
    kappa = np.nan if de == 0 else 1 - do / de
    se = np.nan
    if weights is None and not np.isnan(kappa) and pe < 1:
        se = float(np.sqrt(po * (1 - po) / (n * (1 - pe) ** 2)))
    return dict(kappa=float(kappa), po=float(po), pe=float(pe), n=int(n), n_agree=int(np.trace(O)), se=se)


def raw_agreement(a, b):
    a = np.asarray(list(a)); b = np.asarray(list(b))
    k = int((a == b).sum()); n = len(a)
    return k, n, (k / n if n else np.nan)


def bootstrap_by_theory(m, col_a, col_b, labels, n_boot=2000, seed=0):
    """Percentile 95 % interval for nominal kappa, resampling theories (clusters) with replacement."""
    rng = np.random.default_rng(seed)
    groups = [g for _, g in m.groupby("theory_id")]
    G = len(groups)
    ks = []
    for _ in range(n_boot):
        idx = rng.integers(0, G, G)
        s = pd.concat([groups[i] for i in idx])
        ks.append(cohen_kappa(s[col_a], s[col_b], labels)["kappa"])
    ks = np.array(ks, dtype=float)
    return float(np.nanpercentile(ks, 2.5)), float(np.nanpercentile(ks, 97.5)), G


def interpret(k):
    """Landis & Koch (1977) descriptive band."""
    if k is None or np.isnan(k):
        return "undefined"
    for thr, lab in [(0.0, "poor"), (0.2, "slight"), (0.4, "fair"), (0.6, "moderate"), (0.8, "substantial"), (1.01, "almost perfect")]:
        if k < thr:
            return lab
    return "almost perfect"


def md_table(df: pd.DataFrame, index=True) -> str:
    d = df.reset_index() if index else df
    cols = [str(c) for c in d.columns]
    fmt = lambda v: f"{v:.3f}" if isinstance(v, float) else str(v)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in d.itertuples(index=False)]
    return "\n".join(lines)


# ---------------------------------------------------------------- S1 loading and validation
def load_s1(path, man, scheme: str, label: str):
    df = read_csv_strict(path)
    cols = set(df.columns)
    if "code" not in cols:
        raise ValidationError(f"{label} ({path}): needs a `code` column, has {sorted(cols)}")
    dom_col = "domain_id" if "domain_id" in cols else ("quantity_id" if "quantity_id" in cols else None)
    if dom_col is None:
        raise ValidationError(f"{label} ({path}): needs `domain_id` (or legacy `quantity_id`), has {sorted(cols)}")
    if "theory_id" not in cols and "theory" not in cols:
        raise ValidationError(f"{label} ({path}): needs `theory_id` or `theory`, has {sorted(cols)}")
    df = df.copy()
    # --- theory resolution
    src_col = "theory_id" if "theory_id" in cols else "theory"
    df["theory_id_r"] = df[src_col].map(lambda x: resolve_theory(x, man))
    bad = df[df.theory_id_r.isna()][src_col].astype(str).unique().tolist()
    if bad:
        raise ValidationError(f"{label}: {len(bad)} theory label(s) not in the accounts manifest (theory_id or alias): {bad[:6]}. "
                              f"Valid theory_id: {sorted(man['theory_ids'])}; add --extra-alias 'name=theory_id' if this is a spelling variant.")
    # --- domain validation
    df["domain_id_r"] = df[dom_col].astype(str).str.strip()
    badd = sorted(set(df.domain_id_r) - man["domain_ids"])
    if badd:
        raise ValidationError(f"{label}: domain_id not in the domains manifest: {badd}. Valid: {sorted(man['domain_ids'])}")
    # --- codes
    S = SCHEMES[scheme]
    df["code_n"] = df["code"].map(norm_code_v2 if scheme == "v2" else norm_code_legacy)
    badc = df[df.code_n == "MISSING"]
    if len(badc):
        raise ValidationError(f"{label}: {len(badc)} row(s) with an empty or invalid code (valid: {S['valid_str']}); "
                              f"first offending rows (theory, domain, code): "
                              f"{badc[['theory_id_r', 'domain_id_r', 'code']].head(3).values.tolist()}")
    # --- polarity (v2)
    if scheme == "v2":
        df["polarity_n"] = df["polarity"].map(norm_polarity) if "polarity" in cols else ""
        pos = df.code_n.isin(V2_POSITIVE)
        badp = df[pos & ~df.polarity_n.isin(POLARITIES)]
        if len(badp):
            raise ValidationError(f"{label}: {len(badp)} EXPLICIT/INTERPRETED cell(s) without a valid polarity (positive / null / negative): "
                                  f"{badp[['theory_id_r', 'domain_id_r', 'code_n']].head(3).values.tolist()}"
                                  + ("" if "polarity" in cols else " (no `polarity` column in file)"))
        df.loc[~pos, "polarity_n"] = ""
        df["code_pol"] = np.where(pos, df.code_n + ":" + df.polarity_n, df.code_n)
    else:
        df["polarity_n"] = ""
        df["code_pol"] = df.code_n
    # --- DOI in positive cells
    doi_col = next((c for c in ["source_doi", "citation_doi", "doi"] if c in cols), None)
    df["_doi"] = df[doi_col].map(norm_doi) if doi_col else ""
    pos = df.code_n.isin(S["positive"])
    nodoi = df[pos & (df._doi == "")]
    if len(nodoi):
        raise ValidationError(f"{label}: {len(nodoi)} positive cell(s) ({'/'.join(sorted(S['positive']))}) without a DOI"
                              + ("" if doi_col else " (no source_doi/citation_doi column)") +
                              f": {nodoi[['theory_id_r', 'domain_id_r', 'code_n']].head(3).values.tolist()}")
    # --- duplicates
    dup = df.duplicated(["theory_id_r", "domain_id_r"], keep=False)
    if dup.any():
        raise ValidationError(f"{label}: {int(dup.sum())} rows share a duplicated key (theory_id, domain_id): "
                              f"{df.loc[dup, ['theory_id_r', 'domain_id_r']].drop_duplicates().values.tolist()[:5]}")
    just = next((c for c in ["justification", "prediction", "note"] if c in cols), None)
    src = next((c for c in ["source_label", "citation_label"] if c in cols), None)
    df["_just"] = df[just] if just else ""
    df["_src"] = df[src] if src else ""
    df["_origin_cell"] = df["origin"] if "origin" in cols else (
        df["added_in_revision"].map(lambda v: "added-in-revision" if str(v).strip().lower() in ("true", "1", "yes") else "submitted-v1")
        if "added_in_revision" in cols else np.nan)
    df["_locus"] = df["source_locus"] if "source_locus" in cols else ""
    out = df[["theory_id_r", "domain_id_r", "code_n", "polarity_n", "code_pol", "_just", "_src", "_doi", "_locus", "_origin_cell"]]
    return out.rename(columns={"theory_id_r": "theory_id", "domain_id_r": "domain_id"})


def check_manifest_grid(df, man, label, allow_partial=False):
    """Every (theory_id, domain_id) of the accounts x domains grid must be present exactly once, and nothing else."""
    expected = {(t, d) for t in man["theory_ids"] for d in man["domain_ids"]}
    keys = set(map(tuple, df[["theory_id", "domain_id"]].values))
    missing, extra = sorted(expected - keys), sorted(keys - expected)
    if missing or extra:
        msg = (f"{label}: key set differs from the manifest grid ({len(expected)} cells expected = {len(man['theory_ids'])} theories x "
               f"{len(man['domain_ids'])} domains; {len(keys)} present): {len(missing)} missing {missing[:4]}, {len(extra)} extra {extra[:4]}")
        if not allow_partial:
            raise ValidationError(msg)
        print("WARNING (--allow-partial-grid): " + msg, file=sys.stderr)
    return len(keys)


def check_row_sets(A, B):
    ka = set(map(tuple, A[["theory_id", "domain_id"]].values)); kb = set(map(tuple, B[["theory_id", "domain_id"]].values))
    if ka != kb:
        raise ValidationError(f"S1: key sets differ ({len(ka - kb)} only in file 1, {len(kb - ka)} only in file 2); "
                              f"examples only in file 1: {sorted(ka - kb)[:3]}, only in file 2: {sorted(kb - ka)[:3]}. "
                              "Both coders must fill the same row set before kappa is meaningful.")


def infer_origin(m, man, added_domains):
    """Cell-level origin: file column if the coder-1 file has one, else manifest theory origin OR added domain."""
    if m["_origin_cell_A"].notna().all():
        lab = m["_origin_cell_A"].astype(str).str.strip().str.lower()
        lab = lab.where(lab.isin(["submitted-v1", "added-in-revision"]), other=np.nan)
        if lab.isna().any():
            raise ValidationError(f"S1 file 1: `origin` column must be 'submitted-v1' or 'added-in-revision'; found {sorted(set(m['_origin_cell_A'].astype(str)))}")
        return lab, "file column"
    th_origin = m.theory_id.map(man["accounts"]["origin"].astype(str).str.strip().str.lower())
    lab = np.where((th_origin == "added-in-revision") | m.domain_id.isin(added_domains), "added-in-revision", "submitted-v1")
    return pd.Series(lab, index=m.index), f"inferred (manifest origin or domain in {list(added_domains)})"


# ---------------------------------------------------------------- S1 analysis
def analyse_s1(pa, pb, man, scheme="v2", ci="none", seed=1, added_domains=DEFAULT_ADDED_DOMAINS, n_boot=2000, allow_partial_grid=False):
    S = SCHEMES[scheme]
    A = load_s1(pa, man, scheme, "S1 file 1"); B = load_s1(pb, man, scheme, "S1 file 2")
    check_manifest_grid(A, man, "S1 file 1", allow_partial_grid); check_manifest_grid(B, man, "S1 file 2", allow_partial_grid)
    check_row_sets(A, B)
    m = A.merge(B, on=["theory_id", "domain_id"], suffixes=("_A", "_B"), how="inner", validate="one_to_one")
    assert len(m) == len(A) == len(B)
    labels = S["codes"]
    res = {}
    res["S1_version"] = __version__; res["S1_code_scheme"] = scheme
    res["S1_n_cells_compared"] = len(m)
    res["S1_n_theories"] = int(m.theory_id.nunique()); res["S1_n_domains"] = int(m.domain_id.nunique())
    res["S1_n_manifest_grid_cells"] = len(man["theory_ids"]) * len(man["domain_ids"])
    # 1. raw agreement
    k, n, p = raw_agreement(m.code_n_A, m.code_n_B)
    res["S1_1_raw_agreement_code_k_of_n"] = f"{k} of {n}"; res["S1_1_raw_agreement_code_proportion"] = p
    if scheme == "v2":
        k2, n2, p2 = raw_agreement(m.code_pol_A, m.code_pol_B)
        res["S1_1_raw_agreement_code_polarity_k_of_n"] = f"{k2} of {n2}"; res["S1_1_raw_agreement_code_polarity_proportion"] = p2
    # 2. confusion matrices
    conf = pd.DataFrame(confusion(m.code_n_A, m.code_n_B, labels), index=[f"coder1:{c}" for c in labels], columns=[f"coder2:{c}" for c in labels]).astype(int)
    conf.index.name = "code"
    conf_pol = None
    if scheme == "v2":
        pol_labels = [f"{c}:{p}" for c in ["EXPLICIT", "INTERPRETED"] for p in POLARITIES] + ["NOT_LOCATED", "NOT_APPLICABLE", "UNRESOLVED"]
        conf_pol = pd.DataFrame(confusion(m.code_pol_A, m.code_pol_B, pol_labels), index=[f"coder1:{c}" for c in pol_labels], columns=[f"coder2:{c}" for c in pol_labels]).astype(int)
        conf_pol.index.name = "code:polarity"
    # 3. nominal kappa
    kk = cohen_kappa(m.code_n_A, m.code_n_B, labels)
    res["S1_3_kappa_nominal_code"] = kk["kappa"]; res["S1_3_kappa_nominal_code_pe"] = kk["pe"]
    res["S1_3_kappa_nominal_code_band"] = interpret(kk["kappa"])
    if scheme == "v2":
        kp = cohen_kappa(m.code_pol_A, m.code_pol_B)
        res["S1_3_kappa_nominal_code_polarity"] = kp["kappa"]
        # located vs not: {EXPLICIT, INTERPRETED} vs {NOT_LOCATED, NOT_APPLICABLE, UNRESOLVED}
        # UNRESOLVED is neither located nor not-located: cells where either coder wrote UNRESOLVED are excluded here (own denominator)
        keep = (m.code_n_A != "UNRESOLVED") & (m.code_n_B != "UNRESOLVED")
        la, lb = m.code_n_A[keep].isin(V2_POSITIVE), m.code_n_B[keep].isin(V2_POSITIVE)
        res["S1_3_kappa_binary_located_vs_not"] = cohen_kappa(la, lb, [False, True])["kappa"]
        res["S1_3_kappa_binary_located_vs_not_n_cells"] = int(keep.sum())
        res["S1_3_n_EXPLICIT_null_coder1"] = int(((m.code_n_A == "EXPLICIT") & (m.polarity_n_A == "stated_null")).sum())
        res["S1_3_n_EXPLICIT_null_coder2"] = int(((m.code_n_B == "EXPLICIT") & (m.polarity_n_B == "stated_null")).sum())
        res["S1_3_n_UNRESOLVED_either_coder"] = int(((m.code_n_A == "UNRESOLVED") | (m.code_n_B == "UNRESOLVED")).sum())
        res["S1_3_n_UNRESOLVED_coder1"] = int((m.code_n_A == "UNRESOLVED").sum()); res["S1_3_n_UNRESOLVED_coder2"] = int((m.code_n_B == "UNRESOLVED").sum())
    else:
        collapse = lambda c: "YES" if c == "Y(neg)" else c
        oa, ob = m.code_n_A.map(collapse), m.code_n_B.map(collapse)
        res["S1_3_kappa_ord3_linear_weighted"] = cohen_kappa(oa, ob, ["NO", "IMPLICIT", "YES"], "linear")["kappa"]
        sa, sb = oa.eq("YES"), ob.eq("YES")
        res["S1_3_kappa_binary_stated_vs_not"] = cohen_kappa(sa, sb, [False, True])["kappa"]
    # CI (opt-in)
    if ci == "multinomial":
        res["S1_3_kappa_ci_method"] = "multinomial large-sample SE (cells treated as independent; optimistic for clustered cells)"
        res["S1_3_kappa_se_multinomial"] = kk["se"]
        if not np.isnan(kk["se"]):
            res["S1_3_kappa_ci95_low"] = kk["kappa"] - 1.96 * kk["se"]; res["S1_3_kappa_ci95_high"] = kk["kappa"] + 1.96 * kk["se"]
    elif ci == "bootstrap-by-theory":
        lo, hi, G = bootstrap_by_theory(m, "code_n_A", "code_n_B", labels, n_boot=n_boot, seed=seed)
        res["S1_3_kappa_ci_method"] = f"cluster bootstrap over {G} theories, {n_boot} replicates, percentile 95 % (indicative; few clusters)"
        res["S1_3_kappa_ci95_low"] = lo; res["S1_3_kappa_ci95_high"] = hi
    else:
        res["S1_3_kappa_ci_method"] = "none (nominal kappa; see docstring on cell dependence)"
    # 4. per domain / per theory
    rows = []
    for d, g in m.groupby("domain_id", sort=True):
        kd = cohen_kappa(g.code_n_A, g.code_n_B, labels); k_, n_, p_ = raw_agreement(g.code_n_A, g.code_n_B)
        rows.append(dict(unit="domain", level=d, n=n_, raw_agreement=f"{k_} of {n_}", raw_proportion=p_, kappa_nominal=kd["kappa"], pe=kd["pe"]))
    for t, g in m.groupby("theory_id", sort=True):
        kd = cohen_kappa(g.code_n_A, g.code_n_B, labels); k_, n_, p_ = raw_agreement(g.code_n_A, g.code_n_B)
        rows.append(dict(unit="theory", level=t, n=n_, raw_agreement=f"{k_} of {n_}", raw_proportion=p_, kappa_nominal=kd["kappa"], pe=kd["pe"]))
    percol = pd.DataFrame(rows)
    # 5. subsets by origin
    origin, how = infer_origin(m, man, added_domains)
    m["origin_cell"] = origin.values
    res["S1_5_origin_source"] = how
    sub_rows = []
    for lab in ["submitted-v1", "added-in-revision"]:
        g = m[m.origin_cell == lab]
        if len(g) == 0:
            sub_rows.append(dict(subset=lab, n=0, raw_agreement="0 of 0", raw_proportion=np.nan, kappa_nominal=np.nan, pe=np.nan)); continue
        kd = cohen_kappa(g.code_n_A, g.code_n_B, labels); k_, n_, p_ = raw_agreement(g.code_n_A, g.code_n_B)
        sub_rows.append(dict(subset=lab, n=n_, raw_agreement=f"{k_} of {n_}", raw_proportion=p_, kappa_nominal=kd["kappa"], pe=kd["pe"]))
        res[f"S1_5_kappa_nominal_{lab}"] = kd["kappa"]; res[f"S1_5_raw_agreement_{lab}"] = f"{k_} of {n_}"
    subsets = pd.DataFrame(sub_rows)
    # disagreements
    dis = m[m.code_pol_A != m.code_pol_B][["theory_id", "domain_id", "origin_cell", "code_n_A", "polarity_n_A", "code_n_B", "polarity_n_B",
                                            "_just_A", "_just_B", "_src_A", "_doi_A", "_locus_A", "_src_B", "_doi_B", "_locus_B"]]
    dis = dis.rename(columns={"code_n_A": "code_coder1", "polarity_n_A": "polarity_coder1", "code_n_B": "code_coder2", "polarity_n_B": "polarity_coder2",
                              "_just_A": "justification_coder1", "_just_B": "justification_coder2", "_src_A": "source_coder1", "_doi_A": "doi_coder1",
                              "_locus_A": "locus_coder1", "_src_B": "source_coder2", "_doi_B": "doi_coder2", "_locus_B": "locus_coder2"})
    if scheme == "v2":
        sev = lambda a, b: 2 if ({a, b} & {"EXPLICIT"} and {a, b} & {"NOT_LOCATED", "NOT_APPLICABLE"}) else 1
    else:
        sev = lambda a, b: 2 if ({a, b} & {"YES", "Y(neg)"} and "NO" in {a, b}) else 1
    dis.insert(3, "severity", [sev(a, b) for a, b in zip(dis.code_coder1, dis.code_coder2)])
    dis["adjudicated_code"] = ""; dis["adjudicated_polarity"] = ""; dis["adjudication_note"] = ""
    res["S1_n_disagreements"] = len(dis)
    return res, percol, subsets, conf, conf_pol, dis.sort_values(["severity", "domain_id", "theory_id"], ascending=[False, True, True])


# ---------------------------------------------------------------- S2 (legacy form, unchanged logic)
def load_s2(path):
    df = read_csv_strict(path)
    need = {"doi", "content", "theory_addressed"}
    if not need <= set(df.columns):
        raise ValidationError(f"{path}: needs columns {sorted(need)}, has {list(df.columns)}")
    df = df.copy()
    df["doi_k"] = df["doi"].map(norm_doi)
    df["content_n"] = df["content"].map(norm_text)
    df["ta_n"] = df["theory_addressed"].map(norm_text)
    df["ta_flag"] = df["ta_n"].map(lambda s: "MISSING" if s == "MISSING" else (s != NONE_LABEL))
    df["label"] = df["citation_label"] if "citation_label" in df.columns else df["doi"]
    return df[["label", "doi", "doi_k", "content_n", "ta_n", "ta_flag"]]


def analyse_s2(pa, pb):
    A, B = load_s2(pa), load_s2(pb)
    for name, d in (("file 1", A), ("file 2", B)):
        empty = d.doi_k == ""
        if empty.any():
            raise ValidationError(f"S2 {name} has {int(empty.sum())} rows without a DOI; DOI is the merge key")
        dup = d.duplicated("doi_k", keep=False)
        if dup.any():
            raise ValidationError(f"S2 {name}: {int(dup.sum())} rows share a duplicated DOI: {d.loc[dup, 'doi_k'].drop_duplicates().tolist()[:5]}")
    ka, kb = set(A.doi_k), set(B.doi_k)
    if ka != kb:
        raise ValidationError(f"S2: DOI sets differ ({len(ka - kb)} only in file 1, {len(kb - ka)} only in file 2)")
    m = A.merge(B, on="doi_k", suffixes=("_A", "_B"), how="inner", validate="one_to_one")
    res = {"S2_n_studies_compared": len(m)}
    c = m[(m.content_n_A != "MISSING") & (m.content_n_B != "MISSING")]
    k, n, p = raw_agreement(c.content_n_A, c.content_n_B)
    res["S2_content_raw_agreement"] = f"{k} of {n}"; res["S2_content_kappa_nominal"] = cohen_kappa(c.content_n_A, c.content_n_B)["kappa"]
    t = m[(m.ta_flag_A != "MISSING") & (m.ta_flag_B != "MISSING")]
    k, n, p = raw_agreement(t.ta_flag_A, t.ta_flag_B)
    res["S2_theory_addressed_binary_raw_agreement"] = f"{k} of {n}"
    res["S2_theory_addressed_binary_kappa_nominal"] = cohen_kappa(t.ta_flag_A, t.ta_flag_B, [False, True])["kappa"]
    res["S2_theory_addressed_label_kappa_nominal"] = cohen_kappa(t.ta_n_A, t.ta_n_B)["kappa"]
    dis = m[(m.content_n_A != m.content_n_B) | (m.ta_n_A != m.ta_n_B)][["label_A", "doi_A", "content_n_A", "content_n_B", "ta_n_A", "ta_n_B"]]
    dis = dis.rename(columns={"label_A": "citation_label", "doi_A": "doi", "content_n_A": "content_coder1", "content_n_B": "content_coder2",
                              "ta_n_A": "theory_addressed_coder1", "ta_n_B": "theory_addressed_coder2"})
    dis["adjudicated_content"] = ""; dis["adjudicated_theory_addressed"] = ""; dis["adjudication_note"] = ""
    return res, dis



# ---------------------------------------------------------------- S2 v2 (experiment unit)
S2V2_FIELDS = ["modality", "affective_status", "report_type", "contested_inclusion"]
S2V2_VOCAB = {   # strict vocabularies (v2.1); a trailing parenthetical qualifier is allowed and stripped, e.g. 'both (targets reported; ...)'
    "modality": ["visual", "auditory", "tactile", "motor", "interoceptive", "mixed", "not applicable"],
    "affective_status": ["neutral", "valenced", "interoceptive"],
    "report_type": ["report", "no-report", "both"],
    "contested_inclusion": ["True", "False"],
}
UNRESOLVED = "UNRESOLVED"     # its own category in every kappa; never collapsed into another label
S2V2_UNRESOLVED_ALIASES = {"not verified": UNRESOLVED}   # spelling present in the frozen Table_S2_v2 (P08-E3 report_type); reported per row
S2V2_SPELLINGS = {"no report": "no-report", "no_report": "no-report", "n/a": "not applicable", "na": "not applicable", "not-applicable": "not applicable"}
NO_ATTRIBUTION_RE = re.compile(r"^(none|not named|no theory|n/a|-|not verifiable)\b", re.IGNORECASE)
IDS_COLUMN = "theory_attribution_by_authors_ids"      # optional structured column: semicolon-separated theory_ids from accounts_manifest.csv


def strip_qualifier(s: str) -> str:
    """'both (task-relevant targets reported)' -> 'both'; 'not applicable (state)' -> 'not applicable'."""
    return re.sub(r"\s*\([^()]*\)\s*$", "", s).strip()


def norm_s2v2_value(field: str, raw, key: str, path) -> str:
    """Canonical label for one S2 v2 categorical field, or a ValidationError naming the row and the value."""
    if pd.isna(raw) or str(raw).strip() == "":
        raise ValidationError(f"{path}: row {key!r} has an empty '{field}'; every experiment must be coded before agreement is computed")
    s = re.sub(r"\s+", " ", str(raw).strip())
    base = strip_qualifier(s)
    if base.upper() == UNRESOLVED:
        return UNRESOLVED
    low = base.lower()
    if low in S2V2_UNRESOLVED_ALIASES:
        return S2V2_UNRESOLVED_ALIASES[low]
    if field == "contested_inclusion":
        if low in ("true", "false"):
            return "True" if low == "true" else "False"
        raise ValidationError(f"{path}: row {key!r} has contested_inclusion={raw!r}; allowed: True / False / UNRESOLVED")
    low = S2V2_SPELLINGS.get(low, low)
    if low in S2V2_VOCAB[field]:
        return low
    raise ValidationError(f"{path}: row {key!r} has {field}={raw!r} (base value {base!r}), which is not in the {field} vocabulary "
                          f"{S2V2_VOCAB[field] + [UNRESOLVED]} (a trailing parenthetical qualifier is allowed)")


def _default_manifest_for(path):
    """Manifests beside the S2 file if present; otherwise the built-in alias table over all built-in theory ids."""
    d = os.path.dirname(os.path.abspath(str(path)))
    pa, pdm = os.path.join(d, "accounts_manifest.csv"), os.path.join(d, "domains_manifest.csv")
    if os.path.exists(pa) and os.path.exists(pdm):
        return load_manifests(pa, pdm)
    ids = sorted(set(BUILTIN_ALIASES.values()))
    alias = dict(BUILTIN_ALIASES); alias.update({i.lower(): i for i in ids})
    return dict(accounts=None, domains=None, alias=alias, theory_ids=set(ids), domain_ids=set())


def _alias_patterns(man):
    """Compiled patterns for every manifest spelling. Short all-caps ids (GNWT, SIT, HOT, PP ...) match case-SENSITIVELY as whole
    words so that ordinary words ('sit', 'hot') in free text do not become theories; longer names match case-insensitively."""
    pats = []
    for spelling, tid in man["alias"].items():
        sp = spelling.strip()
        if not sp:
            continue
        if len(sp) <= 5 or sp.lower() == tid.lower():      # ids and short abbreviations: exact upper-case match only
            pats.append((re.compile(r"(?<![A-Za-z0-9])" + re.escape(sp.upper()) + r"(?![A-Za-z0-9])"), tid))
        else:
            pats.append((re.compile(r"(?<![A-Za-z0-9])" + re.escape(sp) + r"(?![A-Za-z0-9])", re.IGNORECASE), tid))
    return pats


def parse_attribution(raw, man, patterns=None):
    """Structured reading of a theory-attribution free-text cell.
    Returns dict(status, ids): status 'none' (empty, or matches NO_ATTRIBUTION_RE, e.g. 'none named (abstract-only)'),
    'ids' (>= 1 manifest theory found by name or id), or 'unparseable' (text present, no manifest theory recognised)."""
    if pd.isna(raw) or str(raw).strip() == "":
        return dict(status="none", ids=frozenset())
    s = re.sub(r"\s+", " ", str(raw).strip())
    if NO_ATTRIBUTION_RE.match(s):
        return dict(status="none", ids=frozenset())
    patterns = patterns or _alias_patterns(man)
    ids = frozenset(tid for pat, tid in patterns if pat.search(s))
    return dict(status="ids" if ids else "unparseable", ids=ids)


def parse_ids_column(raw, man, key, path):
    if pd.isna(raw) or str(raw).strip() == "":
        return frozenset()
    ids = [x.strip() for x in str(raw).split(";") if x.strip()]
    bad = [x for x in ids if x not in man["theory_ids"]]
    if bad:
        raise ValidationError(f"{path}: row {key!r} has {IDS_COLUMN} value(s) {bad} that are not a theory_id in the accounts manifest ({sorted(man['theory_ids'])})")
    return frozenset(ids)


EVIDENCE_STATUS = ["CONTEXT_NAMED", "CONTEXT_READ_NOT_NAMED", "REFLIST", "NONE_FOUND", "NOT_CHECKED"]
_EVIDENCE_PATTERNS = [(re.compile(r"context.*named|named in (?:the )?(?:citing )?sentence|sentence names", re.I), "CONTEXT_NAMED"),
                      (re.compile(r"context.*(?:read|checked).*not named|not named in", re.I), "CONTEXT_READ_NOT_NAMED"),
                      (re.compile(r"ref(?:erence)?[ _-]?list|reflist|cited in the reference", re.I), "REFLIST"),
                      (re.compile(r"^(none|none found|no citation|not cited|-|n/a)\b", re.I), "NONE_FOUND"),
                      (re.compile(r"not checked|not verified|unverified", re.I), "NOT_CHECKED")]


def normalise_evidence(v):
    """later_attribution_evidence -> one of EVIDENCE_STATUS (or UNRESOLVED). The DOI and free explanation are not compared here;
    they are carried into the disagreement list for adjudication."""
    s = re.sub(r"\s+", " ", str(v).strip())
    if s == "" or s.lower() == "nan":
        return "NONE_FOUND"
    head = s.split(";")[0].split("(")[0].strip().upper().replace(" ", "_")
    if head in EVIDENCE_STATUS:
        return head
    for pat, lab in _EVIDENCE_PATTERNS:
        if pat.search(s):
            return lab
    return UNRESOLVED


def load_s2_v2(path, man=None):
    """Load and validate one S2 v2 (experiment-unit) coding file.  Adds: key, <field>_n (canonical labels), by_authors_ids
    (frozenset), by_authors_status, by_authors_flag (bool), attribution_source, later_ids / later_status when the later column exists."""
    man = man or _default_manifest_for(path)
    df = read_csv_strict(path)
    need = {"experiment_id", "theory_attribution_by_authors"} | set(S2V2_FIELDS)
    if not need <= set(df.columns):
        raise ValidationError(f"{path}: S2 v2 needs columns {sorted(need)}, has {list(df.columns)}")
    df = df.copy()
    df["key"] = df["experiment_id"].astype(str).str.strip()
    if (df.key == "").any() or df.key.isna().any() or (df.key == "nan").any():
        raise ValidationError(f"{path}: S2 v2 rows without experiment_id")
    dup = df.duplicated("key", keep=False)
    if dup.any():
        raise ValidationError(f"{path}: {int(dup.sum())} rows share a duplicated experiment_id: {df.loc[dup, 'key'].drop_duplicates().tolist()[:5]}")
    for f in S2V2_FIELDS:
        df[f + "_n"] = [norm_s2v2_value(f, v, k, path) for v, k in zip(df[f], df.key)]
        df[f + "_alias_used"] = [strip_qualifier(re.sub(r"\s+", " ", str(v).strip())).lower() in S2V2_UNRESOLVED_ALIASES for v in df[f]]
    pats = _alias_patterns(man)
    parsed = [parse_attribution(v, man, pats) for v in df["theory_attribution_by_authors"]]
    df["by_authors_text_status"] = [p["status"] for p in parsed]
    text_ids = [p["ids"] for p in parsed]
    if IDS_COLUMN in df.columns:
        df["by_authors_ids"] = [parse_ids_column(v, man, k, path) for v, k in zip(df[IDS_COLUMN], df.key)]
        df["attribution_source"] = "ids column"
        clash = [(k, sorted(i)) for k, i, st in zip(df.key, df.by_authors_ids, df.by_authors_text_status) if st == "none" and i]
        if clash:
            raise ValidationError(f"{path}: {len(clash)} row(s) whose free text says no attribution but whose {IDS_COLUMN} names a theory: {clash[:3]}")
        df["by_authors_status"] = ["ids" if i else "none" for i in df.by_authors_ids]
    else:
        df["by_authors_ids"] = text_ids
        df["attribution_source"] = "free text (manifest names / ids matched)"
        df["by_authors_status"] = df["by_authors_text_status"]
    df["by_authors_flag"] = df["by_authors_status"] != "none"          # 'unparseable' counts as an attribution present but unidentified
    if "by_authors_named" in df.columns:
        coder_flag = df["by_authors_named"].astype(str).str.strip().str.lower().map({"true": True, "false": False})
        mism = df[coder_flag.notna() & (coder_flag != df.by_authors_flag)]
        if len(mism):
            raise ValidationError(f"{path}: {len(mism)} row(s) whose by_authors_named flag contradicts the attribution text: "
                                  f"{mism[['key', 'by_authors_named', 'theory_attribution_by_authors']].head(3).values.tolist()}")
    if "theory_attribution_later" in df.columns:
        lp = [parse_attribution(v, man, pats) for v in df["theory_attribution_later"]]
        df["later_status"] = [p["status"] for p in lp]; df["later_ids"] = [p["ids"] for p in lp]
    # v2.3 optional fields (codebook v2.3): effector_type (motor rows), later_attribution_evidence (normalised status),
    # and the coder's own partition of each publication (unit_type / unit_type_coder2, n_experiments_identified)
    if "effector_type" in df.columns:
        eff = df["effector_type"].astype(str).str.strip().str.lower().replace({"nan": "", "autonomic effector": "autonomic", "smooth muscle": "autonomic", "skeletomotor": "skeletal"})
        bad = df[(df.modality_n == "motor") & ~eff.isin(["skeletal", "autonomic", UNRESOLVED.lower()])]
        if len(bad):
            raise ValidationError(f"{path}: {len(bad)} motor row(s) without effector_type in {{skeletal, autonomic, UNRESOLVED}}: {bad.key.tolist()[:5]}")
        df["effector_n"] = [(e.upper() if e == UNRESOLVED.lower() else e) if mo == "motor" else "(not motor)" for e, mo in zip(eff, df.modality_n)]
    if "later_attribution_evidence" in df.columns:
        df["later_evidence_n"] = [normalise_evidence(v) for v in df["later_attribution_evidence"]]
    ut_col = "unit_type_coder2" if "unit_type_coder2" in df.columns else "unit_type" if "unit_type" in df.columns else None
    if ut_col:
        df["unit_type_n"] = df[ut_col].astype(str).str.strip().str.lower().str.replace(r"\s*\(.*\)$", "", regex=True).replace({"nan": "", "publication-as-one": "publication-as-one", "publication as one": "publication-as-one", "experiment group": "experiment-group"})
    if "n_experiments_identified" in df.columns:
        df["n_exp_n"] = pd.to_numeric(df["n_experiments_identified"], errors="coerce")
    df["label"] = df["citation_label"] if "citation_label" in df.columns else df["key"]
    return df


def check_s2_reference(A, B, reference, pa, pb, man):
    """Both coder files must hold exactly the experiment_id set of the reference file (default: coder-1 file)."""
    ref_ids = set(load_s2_v2(reference, man).key) if reference not in (None, pa) else set(A.key)
    for name, d in (("file 1 (" + str(pa) + ")", A), ("file 2 (" + str(pb) + ")", B)):
        ids = set(d.key)
        if ids != ref_ids:
            raise ValidationError(f"S2 v2: experiment_id set of {name} differs from the reference set ({len(ref_ids)} ids in {reference or pa}): "
                                  f"{len(ref_ids - ids)} missing {sorted(ref_ids - ids)[:5]}, {len(ids - ref_ids)} extra {sorted(ids - ref_ids)[:5]}")
    return ref_ids


def analyse_s2_v2(pa, pb, man=None, reference=None):
    man = man or _default_manifest_for(pa)
    A, B = load_s2_v2(pa, man), load_s2_v2(pb, man)
    res = {"S2v2_version": __version__, "S2v2_reference_file": str(reference or pa)}
    pub_mode = "publication_id" in A.columns and "publication_id" in B.columns and set(A.key) != set(B.key)
    if pub_mode:
        # Coder 2 partitioned the publications herself (blank v3.4: one row per publication, rows added per experiment she identified,
        # experiment_id = <publication_id>-E<k>). Publication sets must match exactly; experiment ids are compared only where both
        # coders used the same id, and the partition itself is compared as a count per publication.
        pa_ids, pb_ids = set(A.publication_id), set(B.publication_id)
        if pa_ids != pb_ids:
            raise ValidationError(f"S2 v2: publication_id sets differ: {sorted(pa_ids - pb_ids)[:5]} only in file 1, {sorted(pb_ids - pa_ids)[:5]} only in file 2")
        res["S2v2_mode"] = "publication-level (coder 2 partitioned independently)"
        res["S2v2_n_publications"] = len(pa_ids)
        ra = A.groupby("publication_id").size(); rb = B.groupby("publication_id").size()
        part = pd.DataFrame({"rows_coder1": ra, "rows_coder2": rb}).fillna(0).astype(int)
        res["S2v2_partition_agreement_publications"] = f"{int((part.rows_coder1 == part.rows_coder2).sum())} of {len(part)}"
        res["S2v2_partition_disagreeing_publications"] = ";".join(part.index[part.rows_coder1 != part.rows_coder2].astype(str)) or "(none)"
        common = sorted(set(A.key) & set(B.key)); res["S2v2_n_experiment_ids_shared"] = len(common)
        res["S2v2_n_experiment_ids_only_coder1"] = len(set(A.key) - set(B.key)); res["S2v2_n_experiment_ids_only_coder2"] = len(set(B.key) - set(A.key))
        A, B = A[A.key.isin(common)].copy(), B[B.key.isin(common)].copy()
        ref_ids = set(common)
        if not common:
            res["S2v2_note"] = "no shared experiment_id; field-level agreement not computable — align ids at the adjudication meeting"
            return res, pd.DataFrame()
    else:
        ref_ids = check_s2_reference(A, B, reference, pa, pb, man)
    m = A.merge(B, on="key", suffixes=("_A", "_B"), how="inner", validate="one_to_one")
    assert len(m) == len(ref_ids)
    res.update({"S2v2_n_experiments_compared": len(m), "S2v2_n_reference_experiment_ids": len(ref_ids)})
    for f in S2V2_FIELDS:
        labels = S2V2_VOCAB[f] + [UNRESOLVED]
        k, n, p = raw_agreement(m[f + "_n_A"], m[f + "_n_B"])
        res[f"S2v2_{f}_raw_agreement"] = f"{k} of {n}"
        res[f"S2v2_{f}_kappa_nominal"] = cohen_kappa(m[f + "_n_A"], m[f + "_n_B"], labels)["kappa"]
        res[f"S2v2_{f}_n_UNRESOLVED_coder1"] = int((m[f + "_n_A"] == UNRESOLVED).sum()); res[f"S2v2_{f}_n_UNRESOLVED_coder2"] = int((m[f + "_n_B"] == UNRESOLVED).sum())
        al = m.loc[m[f + "_alias_used_A"] | m[f + "_alias_used_B"], "key"].tolist()
        if al:
            res[f"S2v2_{f}_rows_read_as_UNRESOLVED_via_alias"] = ";".join(al)
    # attribution by the authors: binary flag and theory-id SETS, reported separately
    k, n, p = raw_agreement(m.by_authors_flag_A, m.by_authors_flag_B)
    res["S2v2_attribution_by_authors_binary_raw_agreement"] = f"{k} of {n}"
    res["S2v2_attribution_by_authors_binary_kappa_nominal"] = cohen_kappa(m.by_authors_flag_A, m.by_authors_flag_B, [False, True])["kappa"]
    set_a = m.by_authors_ids_A.map(lambda s: ";".join(sorted(s)) or "(none)"); set_b = m.by_authors_ids_B.map(lambda s: ";".join(sorted(s)) or "(none)")
    k, n, p = raw_agreement(set_a, set_b)
    res["S2v2_attribution_by_authors_set_raw_agreement"] = f"{k} of {n}"
    res["S2v2_attribution_by_authors_set_kappa_nominal"] = cohen_kappa(set_a, set_b)["kappa"]
    res["S2v2_attribution_source_coder1"] = A.attribution_source.iloc[0]; res["S2v2_attribution_source_coder2"] = B.attribution_source.iloc[0]
    res["S2v2_n_by_authors_flag_True_coder1"] = int(m.by_authors_flag_A.sum()); res["S2v2_n_by_authors_flag_True_coder2"] = int(m.by_authors_flag_B.sum())
    for c, d in (("coder1", "A"), ("coder2", "B")):
        unp = m.loc[m[f"by_authors_status_{d}"] == "unparseable", "key"].tolist()
        res[f"S2v2_attribution_n_unparseable_{c}"] = len(unp)
        res[f"S2v2_attribution_unparseable_rows_{c}"] = ";".join(unp) if unp else "(none)"
    if "later_ids_A" in m.columns and "later_ids_B" in m.columns:
        la = m.later_ids_A.map(lambda s: ";".join(sorted(s)) or "(none)"); lb = m.later_ids_B.map(lambda s: ";".join(sorted(s)) or "(none)")
        k, n, p = raw_agreement(la, lb)
        res["S2v2_attribution_later_set_raw_agreement"] = f"{k} of {n}"; res["S2v2_attribution_later_set_kappa_nominal"] = cohen_kappa(la, lb)["kappa"]
        for c, d in (("coder1", "A"), ("coder2", "B")):
            unp = m.loc[m[f"later_status_{d}"] == "unparseable", "key"].tolist()
            res[f"S2v2_attribution_later_unparseable_rows_{c}"] = ";".join(unp) if unp else "(none)"
    # optional v2.3 fields: compared only when BOTH files carry them; otherwise reported as 'not compared' (never as agreement)
    opt = {}
    if "effector_n_A" in m.columns and "effector_n_B" in m.columns:
        mot = m[(m.effector_n_A != "(not motor)") | (m.effector_n_B != "(not motor)")]
        k, n, p = raw_agreement(mot.effector_n_A, mot.effector_n_B)
        res["S2v2_effector_type_motor_rows_raw_agreement"] = f"{k} of {n}"
        res["S2v2_effector_type_motor_rows_kappa_nominal"] = cohen_kappa(mot.effector_n_A, mot.effector_n_B, ["skeletal", "autonomic", UNRESOLVED, "(not motor)"])["kappa"] if n else float("nan")
        opt["effector"] = m.effector_n_A != m.effector_n_B
    else:
        res["S2v2_effector_type"] = "not compared (field absent in at least one file)"
    if "later_evidence_n_A" in m.columns and "later_evidence_n_B" in m.columns:
        k, n, p = raw_agreement(m.later_evidence_n_A, m.later_evidence_n_B)
        res["S2v2_later_attribution_evidence_status_raw_agreement"] = f"{k} of {n}"
        res["S2v2_later_attribution_evidence_status_kappa_nominal"] = cohen_kappa(m.later_evidence_n_A, m.later_evidence_n_B, EVIDENCE_STATUS + [UNRESOLVED])["kappa"]
        opt["evidence"] = m.later_evidence_n_A != m.later_evidence_n_B
    else:
        res["S2v2_later_attribution_evidence"] = "not compared (field absent in at least one file)"
    if "unit_type_n_A" in m.columns and "unit_type_n_B" in m.columns:
        k, n, p = raw_agreement(m.unit_type_n_A, m.unit_type_n_B)
        res["S2v2_unit_type_raw_agreement"] = f"{k} of {n}"
        res["S2v2_unit_type_kappa_nominal"] = cohen_kappa(m.unit_type_n_A, m.unit_type_n_B)["kappa"]
        opt["unit_type"] = m.unit_type_n_A != m.unit_type_n_B
    else:
        res["S2v2_unit_type"] = "not compared (coder-2 partition field absent in at least one file)"
    nexp_col = "n_exp_n_B" if "n_exp_n_B" in m.columns else ("n_exp_n" if ("n_exp_n" in m.columns and "n_exp_n" in B.columns) else None)   # unsuffixed when only coder 2 has the column
    if nexp_col and "publication_id_A" in m.columns:   # coder 1 supplies the partition as rows; coder 2 states the count
        # publication-level: coder 1's row count per publication vs coder 2's stated number of experiments
        pub = m.groupby("publication_id_A").agg(rows_coder1=("key", "size"), n_exp_coder2=(nexp_col, "max")).reset_index()
        pub_diff = pub[pub.n_exp_coder2.notna() & (pub.rows_coder1 != pub.n_exp_coder2)]
        res["S2v2_publication_partition_publications_compared"] = int(pub.n_exp_coder2.notna().sum())
        res["S2v2_publication_partition_disagreements"] = int(len(pub_diff))
        res["S2v2_publication_partition_disagreeing_publications"] = ";".join(pub_diff.publication_id_A.astype(str)) if len(pub_diff) else "(none)"
        opt["partition"] = m.publication_id_A.isin(pub_diff.publication_id_A)
    else:
        res["S2v2_publication_partition"] = "not compared (coder-2 n_experiments_identified or publication_id absent)"
    diff = pd.Series(False, index=m.index)
    for f in S2V2_FIELDS:
        diff |= m[f + "_n_A"] != m[f + "_n_B"]
    for v in opt.values():
        diff |= v
    diff |= m.by_authors_flag_A != m.by_authors_flag_B
    diff |= set_a != set_b
    if "later_ids_A" in m.columns and "later_ids_B" in m.columns:
        diff |= la != lb                                    # later (post-publication) attribution: sets differ
        diff |= m.later_status_A != m.later_status_B
    cols = ["key", "label_A"] + [f + s for f in S2V2_FIELDS for s in ("_n_A", "_n_B")] + ["by_authors_flag_A", "by_authors_flag_B"]
    dis = m.loc[diff, cols].rename(columns={"key": "experiment_id", "label_A": "citation_label"})
    dis["by_authors_ids_coder1"] = set_a[diff].values; dis["by_authors_ids_coder2"] = set_b[diff].values
    if "later_ids_A" in m.columns and "later_ids_B" in m.columns:
        dis["later_ids_coder1"] = la[diff].values; dis["later_ids_coder2"] = lb[diff].values
        dis["later_status_coder1"] = m.later_status_A[diff].values; dis["later_status_coder2"] = m.later_status_B[diff].values
    if "effector" in opt:
        dis["effector_coder1"] = m.effector_n_A[diff].values; dis["effector_coder2"] = m.effector_n_B[diff].values
    if "evidence" in opt:
        dis["later_evidence_status_coder1"] = m.later_evidence_n_A[diff].values; dis["later_evidence_status_coder2"] = m.later_evidence_n_B[diff].values
        dis["later_evidence_text_coder1"] = m.later_attribution_evidence_A[diff].values; dis["later_evidence_text_coder2"] = m.later_attribution_evidence_B[diff].values
    if "unit_type" in opt:
        dis["unit_type_coder1"] = m.unit_type_n_A[diff].values; dis["unit_type_coder2"] = m.unit_type_n_B[diff].values
    if "partition" in opt:
        dis["partition_disagreement"] = opt["partition"][diff].values
        pn_col = "partition_note_B" if "partition_note_B" in m.columns else "partition_note" if "partition_note" in m.columns else None
        if pn_col:
            dis["partition_note_coder2"] = m[pn_col][diff].values
    dis["adjudication_note"] = ""
    res["S2v2_n_disagreements"] = len(dis)
    return res, dis

# ---------------------------------------------------------------- output
def write_outputs(out, res, percol=None, subsets=None, conf=None, conf_pol=None, dis1=None, dis2=None, title="Inter-coder agreement"):
    os.makedirs(out, exist_ok=True)
    pd.DataFrame({"statistic": list(res.keys()), "value": list(res.values())}).to_csv(os.path.join(out, "agreement_summary.csv"), index=False)
    if percol is not None:
        percol.to_csv(os.path.join(out, "s1_per_domain_kappa.csv"), index=False)
    if subsets is not None:
        subsets.to_csv(os.path.join(out, "s1_subset_kappa.csv"), index=False)
    if conf is not None:
        conf.to_csv(os.path.join(out, "s1_confusion_code.csv"))
    if conf_pol is not None:
        conf_pol.to_csv(os.path.join(out, "s1_confusion_code_polarity.csv"))
    if dis1 is not None:
        dis1.to_csv(os.path.join(out, "disagreements_S1.csv"), index=False)
    if dis2 is not None:
        dis2.to_csv(os.path.join(out, "disagreements_S2.csv"), index=False)
    L = [f"# {title}", "", f"agreement.py v{__version__}", ""]
    if "S1_1_raw_agreement_code_k_of_n" in res:
        L += ["## 1. Raw agreement", "", f"Code: {res['S1_1_raw_agreement_code_k_of_n']} cells ({res['S1_1_raw_agreement_code_proportion']:.3f})."]
        if "S1_1_raw_agreement_code_polarity_k_of_n" in res:
            L += [f"Code x polarity: {res['S1_1_raw_agreement_code_polarity_k_of_n']} ({res['S1_1_raw_agreement_code_polarity_proportion']:.3f})."]
    if conf is not None:
        L += ["", "## 2. Confusion matrix (rows coder 1, columns coder 2)", "", md_table(conf)]
        if conf_pol is not None:
            L += ["", "Code x polarity:", "", md_table(conf_pol)]
    if "S1_3_kappa_nominal_code" in res:
        L += ["", "## 3. Nominal Cohen's kappa", "", f"kappa (code) = {res['S1_3_kappa_nominal_code']:.3f} (p_e = {res['S1_3_kappa_nominal_code_pe']:.3f}; Landis-Koch band: {res['S1_3_kappa_nominal_code_band']}).",
              f"Interval: {res['S1_3_kappa_ci_method']}."]
        if "S1_3_kappa_ci95_low" in res:
            L += [f"95 % interval: {res['S1_3_kappa_ci95_low']:.3f} to {res['S1_3_kappa_ci95_high']:.3f}."]
    if percol is not None and len(percol):
        L += ["", "## 4. Kappa per domain and per theory", "", md_table(percol, index=False)]
    if subsets is not None:
        L += ["", f"## 5. Kappa by origin subset ({res.get('S1_5_origin_source', '')})", "", md_table(subsets, index=False)]
    L += ["", "## All statistics", "", "| statistic | value |", "|---|---|"]
    for k, v in res.items():
        L.append(f"| {k} | {v:.3f} |" if isinstance(v, float) else f"| {k} | {v} |")
    if dis1 is not None:
        L += ["", f"## S1 disagreements for adjudication (n = {len(dis1)}; severity 2 = stated prediction vs not located / not applicable)", "",
              md_table(dis1[["theory_id", "domain_id", "origin_cell", "code_coder1", "polarity_coder1", "code_coder2", "polarity_coder2", "severity"]], index=False)]
    if dis2 is not None:
        L += ["", f"## S2 disagreements for adjudication (n = {len(dis2)})", "",
              md_table(dis2[[c for c in (["citation_label", "content_coder1", "content_coder2", "theory_addressed_coder1", "theory_addressed_coder2"]
                                         if "content_coder1" in dis2.columns else list(dis2.columns)) if c in dis2.columns]], index=False)]
    L += ["", "Kappa is Cohen's kappa from the coder-by-coder cross-tabulation (unweighted). Undefined (NaN) kappa means both coders used a single category "
          "in that block, so chance agreement is 1 and kappa has no value; raw agreement is still reported. No interval is attached unless --ci was given: "
          "cells within a theory are coded from the same sources and are not independent, so the multinomial SE and a cell-level bootstrap are both optimistic."]
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


def _write_manifests(out):
    acc = pd.DataFrame({"theory_id": ["GNWT", "IIT", "RPT", "HOT", "HOSS", "AST", "PP", "SIT", "PFT", "NSF", "UAL", "FM"],
                        "theory": ["GNWT", "IIT (3.0/4.0)", "Recurrent processing (RPT)", "Higher-order theory (HOT / HOROR)", "Higher-order state space (HOSS)",
                                   "AST", "Predictive processing / beast machine", "Supramodular interaction theory (SIT)", "Passive frame theory",
                                   "Neural subjective frame", "UAL", "Feinberg & Mallatt"],
                        "row_class": ["trial-level"] * 10 + ["origin-level"] * 2,
                        "origin": ["submitted-v1"] * 8 + ["added-in-revision"] * 2 + ["submitted-v1"] * 2, "note": ""})
    dom = pd.DataFrame({"domain_id": ["M1", "M2", "M3", "M4a", "M4b", "M4c", "M5", "M6", "M7", "M8"], "domain": [f"domain {i}" for i in range(10)]})
    pa, pd_ = os.path.join(out, "sim_accounts_manifest.csv"), os.path.join(out, "sim_domains_manifest.csv")
    acc.to_csv(pa, index=False); dom.to_csv(pd_, index=False)
    return pa, pd_


def _sim_pair(base, rng, p_agree, probs):
    c1 = list(rng.choice(V2_CODES, size=len(base), p=probs))
    c2 = _perturb(c1, V2_CODES, p_agree, rng)
    pol = lambda cs: [rng.choice(POLARITIES, p=[0.7, 0.2, 0.1]) if c in V2_POSITIVE else "" for c in cs]
    doi = lambda cs: ["10.0/sim" if c in V2_POSITIVE else "" for c in cs]
    s1a = base.assign(code=c1, polarity=pol(c1), justification="sim", source_label="sim", source_doi=doi(c1), source_locus="sim p. 1")
    s1b = base.assign(code=[x.lower().replace("_", " ") for x in c2], polarity=pol(c2), justification="sim", source_label="sim", source_doi=doi(c2))
    return s1a, s1b


def _sim_s2_v2():
    """Small synthetic S2 v2 coding table (values are illustrative, not the study's codes)."""
    return pd.DataFrame([
        dict(experiment_id="X-gnwt-iit", citation_label="sim A", modality="visual", affective_status="neutral", report_type="both (targets reported; irrelevant stimuli unreported)", contested_inclusion="False",
             theory_attribution_by_authors="GNWT vs IIT — title; abstract; preregistered predictions"),
        dict(experiment_id="X-none", citation_label="sim B", modality="visual", affective_status="neutral", report_type="report", contested_inclusion="False",
             theory_attribution_by_authors="none named (abstract-only)"),
        dict(experiment_id="X-sit", citation_label="sim C", modality="motor", affective_status="neutral", report_type="report", contested_inclusion="False",
             theory_attribution_by_authors="SIT — Introduction (\"According to supramodular interaction theory (Morsella, 2005)\")"),
        dict(experiment_id="X-state", citation_label="sim D", modality="not applicable (state)", affective_status="neutral", report_type="report (experience sampling)", contested_inclusion="True",
             theory_attribution_by_authors=""),
        dict(experiment_id="X-unres", citation_label="sim E", modality="auditory", affective_status="neutral", report_type="UNRESOLVED", contested_inclusion="False",
             theory_attribution_by_authors="not verifiable from abstract (no theory named)"),
        dict(experiment_id="X-hot", citation_label="sim F", modality="visual", affective_status="valenced", report_type="no-report", contested_inclusion="True",
             theory_attribution_by_authors="HOT — Discussion: in line with higher-order theories"),
    ])


def _expect_failure(name, fn, must_contain):
    """Run fn(); it must raise SystemExit whose message contains `must_contain`. Returns a log row."""
    try:
        fn()
    except SystemExit as e:
        msg = str(e)
        ok = must_contain.lower() in msg.lower()
        return dict(case=name, outcome="aborted as required" if ok else "aborted with UNEXPECTED message", passed=ok, message=msg)
    except Exception as e:  # any other exception is a failure: the error must be a clear, deliberate abort
        return dict(case=name, outcome=f"raised {type(e).__name__} instead of a validation abort", passed=False, message=str(e))
    return dict(case=name, outcome="DID NOT ABORT", passed=False, message="")


def selftest(out, seed=1, p_agree=0.80, n_reps=200):
    rng = np.random.default_rng(seed)
    os.makedirs(out, exist_ok=True)
    log = []
    # ---- unit checks on kappa
    a = ["x"] * 25 + ["y"] * 25; b = ["x"] * 20 + ["y"] * 5 + ["x"] * 10 + ["y"] * 15   # po=0.70, pe=0.50, kappa=0.40
    k = cohen_kappa(a, b, ["x", "y"])
    log.append(dict(case="hand-checked 2x2 kappa = 0.40", outcome=f"kappa={k['kappa']:.6f}", passed=abs(k["kappa"] - 0.40) < 1e-12 and abs(k["po"] - 0.70) < 1e-12, message=""))
    log.append(dict(case="identical codings give kappa = 1", outcome="", passed=cohen_kappa(a, a, ["x", "y"])["kappa"] == 1.0, message=""))
    # ---- positive case: 12 theories x 10 domains, 80 % agreement
    pa, pdm = _write_manifests(out)
    man = load_manifests(pa, pdm)
    base = pd.DataFrame([(t, d) for t in man["accounts"].index for d in man["domains"].index], columns=["theory_id", "domain_id"])
    probs = [0.20, 0.22, 0.48, 0.06, 0.04]   # EXPLICIT, INTERPRETED, NOT_LOCATED, NOT_APPLICABLE, UNRESOLVED
    ks, pos = [], []
    for _ in range(n_reps):
        c1 = list(rng.choice(V2_CODES, size=len(base), p=probs)); c2 = _perturb(c1, V2_CODES, p_agree, rng)
        kk = cohen_kappa(c1, c2, V2_CODES); ks.append(kk["kappa"]); pos.append(kk["po"])
    p = np.array(probs); pe_th = float((p * (p_agree * p + (1 - p_agree) * (1 - p) / (len(p) - 1))).sum())
    k_th = (p_agree - pe_th) / (1 - pe_th)
    k_mean, k_sd = float(np.mean(ks)), float(np.std(ks))
    tol = 3 * k_sd / np.sqrt(n_reps) + 0.01
    log.append(dict(case=f"positive: kappa recovered from simulated {int(p_agree * 100)} % agreement ({n_reps} reps)",
                    outcome=f"mean kappa={k_mean:.3f}, analytic={k_th:.3f}, mean po={np.mean(pos):.3f}", passed=abs(k_mean - k_th) < tol, message=f"tolerance {tol:.3f}"))
    s1a, s1b = _sim_pair(base, rng, p_agree, probs)
    f1, f2 = os.path.join(out, "sim_S1_coder1.csv"), os.path.join(out, "sim_S1_coder2.csv")
    s1a.to_csv(f1, index=False); s1b.to_csv(f2, index=False)
    res1, percol, subsets, conf, conf_pol, dis1 = analyse_s1(f1, f2, man, scheme="v2", ci="none", seed=seed)
    log.append(dict(case="positive: full pipeline on 120 simulated cells", outcome=f"n={res1['S1_n_cells_compared']}, kappa={res1['S1_3_kappa_nominal_code']:.3f}",
                    passed=res1["S1_n_cells_compared"] == 120 and 0 < res1["S1_3_kappa_nominal_code"] < 1, message=""))
    n_added = int(subsets.set_index("subset").loc["added-in-revision", "n"])
    log.append(dict(case="positive: origin subsets inferred (2 added theories x 10 + 10 other theories x 3 added domains = 50)", outcome=f"added-in-revision n={n_added}", passed=n_added == 50, message=""))
    # both CI options run
    r_mult = analyse_s1(f1, f2, man, scheme="v2", ci="multinomial", seed=seed)[0]
    r_boot = analyse_s1(f1, f2, man, scheme="v2", ci="bootstrap-by-theory", seed=seed, n_boot=200)[0]
    log.append(dict(case="positive: --ci options run and bracket the point estimate", outcome=f"multinomial [{r_mult['S1_3_kappa_ci95_low']:.3f},{r_mult['S1_3_kappa_ci95_high']:.3f}], cluster bootstrap [{r_boot['S1_3_kappa_ci95_low']:.3f},{r_boot['S1_3_kappa_ci95_high']:.3f}]",
                    passed=r_mult["S1_3_kappa_ci95_low"] < res1["S1_3_kappa_nominal_code"] < r_mult["S1_3_kappa_ci95_high"] and r_boot["S1_3_kappa_ci95_low"] <= res1["S1_3_kappa_nominal_code"] <= r_boot["S1_3_kappa_ci95_high"], message=""))
    # legacy scheme on the same grid
    leg_codes = list(rng.choice(LEGACY_CODES, size=len(base), p=[0.5, 0.27, 0.2, 0.03]))
    la = base.assign(code=leg_codes, source_doi="10.0/sim"); lb = base.assign(code=[{"Y(neg)": "YES (negative)"}.get(x, x.lower()) for x in _perturb(leg_codes, LEGACY_CODES, p_agree, rng)], source_doi="10.0/sim")
    fl1, fl2 = os.path.join(out, "sim_S1_legacy_coder1.csv"), os.path.join(out, "sim_S1_legacy_coder2.csv"); la.to_csv(fl1, index=False); lb.to_csv(fl2, index=False)
    rl = analyse_s1(fl1, fl2, man, scheme="legacy")[0]
    log.append(dict(case="positive: legacy scheme (YES/IMPLICIT/NO/YES (negative)) accepted", outcome=f"kappa={rl['S1_3_kappa_nominal_code']:.3f}", passed=rl["S1_n_cells_compared"] == 120, message=""))
    # ---- NEGATIVE cases: each must abort with a clear message
    def run(a_df, b_df=None, **kw):
        ga, gb = os.path.join(out, "neg_a.csv"), os.path.join(out, "neg_b.csv")
        a_df.to_csv(ga, index=False); (b_df if b_df is not None else s1b).to_csv(gb, index=False)
        return lambda: analyse_s1(ga, gb, man, scheme="v2", **kw)
    neg = []
    dup = pd.concat([s1a, s1a.iloc[[5]]], ignore_index=True)
    neg.append(_expect_failure("negative: duplicated key (theory_id, domain_id)", run(dup), "duplicated key"))
    alias = s1a.copy(); alias.loc[3, "theory_id"] = "Global Workspace Theory of Baars"
    neg.append(_expect_failure("negative: theory alias not in manifest", run(alias), "not in the accounts manifest"))
    typo = s1a.copy(); typo.loc[7, "code"] = "EXPLICT"
    neg.append(_expect_failure("negative: typo in code", run(typo), "invalid code"))
    nan = s1a.copy(); nan.loc[11, "code"] = np.nan
    neg.append(_expect_failure("negative: NaN code", run(nan), "empty or invalid code"))
    mism = s1a.drop(index=[0, 1, 2])
    neg.append(_expect_failure("negative: mismatched row sets", run(mism), "differs from the manifest grid"))
    nodoi = s1a.copy(); i = nodoi.index[nodoi.code.isin(V2_POSITIVE)][0]; nodoi.loc[i, "source_doi"] = np.nan
    neg.append(_expect_failure("negative: DOI NaN in a positive cell", run(nodoi), "without a DOI"))
    baddom = s1a.copy(); baddom.loc[4, "domain_id"] = "M9"
    neg.append(_expect_failure("negative (extra): domain_id not in manifest", run(baddom), "not in the domains manifest"))
    nopol = s1a.copy(); i = nopol.index[nopol.code.isin(V2_POSITIVE)][0]; nopol.loc[i, "polarity"] = np.nan
    neg.append(_expect_failure("negative (extra): EXPLICIT cell without polarity", run(nopol), "without a valid polarity"))
    # ---- v2.1 negative cases (audit sections 4-7); each defect must be caught
    neg.append(_expect_failure("negative (v2.1): truncated S1 accepted (both files 2 rows)", run(s1a.iloc[:2], s1b.iloc[:2]), "differs from the manifest grid"))
    s2 = _sim_s2_v2()
    f21, f22 = os.path.join(out, "sim_S2v2_coder1.csv"), os.path.join(out, "sim_S2v2_coder2.csv")
    s2.to_csv(f21, index=False)
    A2 = load_s2_v2(f21, man)
    r_none = A2.set_index("key").loc["X-none", "by_authors_flag"]
    log.append(dict(case="negative (v2.1): none-named attribution flagged True", outcome=f"'none named (abstract-only)' -> by_authors_flag={bool(r_none)}",
                    passed=not bool(r_none), message="must be False"))
    ids_found = A2.set_index("key").loc["X-gnwt-iit", "by_authors_ids"]
    log.append(dict(case="positive (v2.1): theory ids extracted from free text", outcome=f"'GNWT vs IIT — title' -> {sorted(ids_found)}", passed=ids_found == frozenset({"GNWT", "IIT"}), message=""))
    s2.to_csv(f22, index=False)
    r_same, d_same = analyse_s2_v2(f21, f22, man)
    log.append(dict(case="positive (v2.1): S2 v2 pipeline, identical files", outcome=f"n={r_same['S2v2_n_experiments_compared']}, set agreement {r_same['S2v2_attribution_by_authors_set_raw_agreement']}, disagreements {len(d_same)}",
                    passed=r_same["S2v2_n_experiments_compared"] == len(s2) and len(d_same) == 0 and r_same["S2v2_report_type_n_UNRESOLVED_coder1"] == 1, message="UNRESOLVED kept as its own category"))
    wrong = s2.copy(); wrong.loc[wrong.experiment_id == "X-gnwt-iit", "theory_attribution_by_authors"] = "SIT"; wrong.to_csv(f22, index=False)
    r_w, d_w = analyse_s2_v2(f21, f22, man)
    log.append(dict(case="negative (v2.1): wrong theory id undetected", outcome=f"binary {r_w['S2v2_attribution_by_authors_binary_raw_agreement']}, set {r_w['S2v2_attribution_by_authors_set_raw_agreement']}, in disagreements: {bool((d_w.experiment_id == 'X-gnwt-iit').any())}",
                    passed=bool((d_w.experiment_id == "X-gnwt-iit").any()) and r_w["S2v2_attribution_by_authors_set_raw_agreement"] == f"{len(s2) - 1} of {len(s2)}", message="binary flag alone cannot see this"))
    banana = s2.copy(); banana.loc[0, "modality"] = "BANANA"; fb = os.path.join(out, "neg_s2_banana.csv"); banana.to_csv(fb, index=False)
    neg.append(_expect_failure("negative (v2.1): invalid modality accepted (BANANA)", lambda: analyse_s2_v2(f21, fb, man), "modality"))
    short = s2.iloc[:-1]; fs = os.path.join(out, "neg_s2_short.csv"); short.to_csv(fs, index=False)
    neg.append(_expect_failure("negative (v2.1): S2 id set mismatch accepted", lambda: analyse_s2_v2(f21, fs, man), "experiment_id set"))
    badid = s2.copy(); badid[IDS_COLUMN] = ""; badid.loc[0, IDS_COLUMN] = "GWT"; fi = os.path.join(out, "neg_s2_badid.csv"); badid.to_csv(fi, index=False)
    neg.append(_expect_failure("negative (v2.1, extra): ids column with a theory_id not in the manifest", lambda: analyse_s2_v2(f21, fi, man), "not a theory_id"))
    badc = s2.copy(); badc.loc[1, "contested_inclusion"] = "maybe"; fc = os.path.join(out, "neg_s2_contested.csv"); badc.to_csv(fc, index=False)
    neg.append(_expect_failure("negative (v2.1, extra): contested_inclusion outside {True, False}", lambda: analyse_s2_v2(f21, fc, man), "contested_inclusion"))
    log += neg
    n_neg_required = 6 + 5; n_neg_total = len(neg) + 2   # 2 detection cases are logged above as pass/fail rows rather than aborts
    # ---- write log (messages made independent of the output directory so that the log is hash-stable across runs)
    logdf = pd.DataFrame(log)
    for pre in sorted({os.path.abspath(out) + os.sep, out.rstrip(os.sep) + os.sep}, key=len, reverse=True):
        logdf["message"] = logdf["message"].astype(str).str.replace(pre, "<out>/", regex=False)
    logdf["message"] = logdf["message"].str[:300]
    logdf.to_csv(os.path.join(out, "selftest_log.csv"), index=False)
    res = {"selftest_version": __version__, "selftest_seed": seed, "selftest_p_agree_simulated": p_agree, "selftest_n_reps": n_reps,
           "selftest_kappa_mean": k_mean, "selftest_kappa_sd": k_sd, "selftest_kappa_analytic": float(k_th), "selftest_pe_analytic": pe_th,
           "selftest_n_negative_cases_required": n_neg_required, "selftest_n_negative_cases_run": n_neg_total,
           "selftest_n_cases_total": len(logdf), "selftest_n_cases_passed": int(logdf.passed.sum()), **res1}
    write_outputs(out, res, percol, subsets, conf, conf_pol, dis1, None, title="agreement.py self-test on synthetic data (codes are random, not the study's codes)")
    with open(os.path.join(out, "selftest_log.md"), "w") as f:
        f.write("# agreement.py --selftest log\n\n" + md_table(logdf[["case", "outcome", "passed", "message"]], index=False) + "\n")
    return res, logdf


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--s1a"); ap.add_argument("--s1b"); ap.add_argument("--s2a"); ap.add_argument("--s2b")
    ap.add_argument("--accounts", default="accounts_manifest.csv"); ap.add_argument("--domains", default="domains_manifest.csv")
    ap.add_argument("--code-scheme", choices=["v2", "legacy"], default="v2")
    ap.add_argument("--ci", choices=["none", "multinomial", "bootstrap-by-theory"], default="none")
    ap.add_argument("--added-domains", default=",".join(DEFAULT_ADDED_DOMAINS), help="domain_ids treated as added-in-revision when no cell-level origin column exists")
    ap.add_argument("--extra-alias", action="append", default=[], help="'spelling=theory_id', repeatable (e.g. 'HOT / HOSS=HOT' for the merged legacy row)")
    ap.add_argument("--out", default="agreement_out")
    ap.add_argument("--s2-reference", default=None, help="S2 v2: file whose experiment_id set both coder files must match (default: the --s2a file)")
    ap.add_argument("--allow-partial-grid", action="store_true", help="S1: warn instead of abort when a file does not cover the full manifest grid (legacy 88-cell comparison only)")
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args(argv)
    if args.selftest:
        out = args.out if args.out != "agreement_out" else "agreement_selftest"
        res, logdf = selftest(out, seed=args.seed)
        for _, r in logdf.iterrows():
            print(f"[{'PASS' if r.passed else 'FAIL'}] {r.case} -- {r.outcome}")
        print(f"selftest: {int(logdf.passed.sum())} of {len(logdf)} cases passed; kappa mean {res['selftest_kappa_mean']:.3f} vs analytic {res['selftest_kappa_analytic']:.3f}")
        if not logdf.passed.all():
            sys.exit("SELFTEST FAILED: " + "; ".join(logdf[~logdf.passed].case))
        return 0
    res = {}; percol = subsets = conf = conf_pol = dis1 = dis2 = None
    if args.s1a and args.s1b:
        man = load_manifests(args.accounts, args.domains, args.extra_alias)
        added = tuple(x.strip() for x in args.added_domains.split(",") if x.strip())
        r1, percol, subsets, conf, conf_pol, dis1 = analyse_s1(args.s1a, args.s1b, man, scheme=args.code_scheme, ci=args.ci, seed=args.seed, added_domains=added, allow_partial_grid=args.allow_partial_grid)
        res.update(r1)
    if args.s2a and args.s2b:
        cols_a = set(read_csv_strict(args.s2a).columns)
        if "experiment_id" in cols_a:          # S2 v2 (experiment unit) auto-detected
            man2 = load_manifests(args.accounts, args.domains, args.extra_alias) if os.path.exists(args.accounts) and os.path.exists(args.domains) else None
            r2, dis2 = analyse_s2_v2(args.s2a, args.s2b, man2, args.s2_reference); res.update(r2)
        else:                                  # legacy 36-row study-unit form
            r2, dis2 = analyse_s2(args.s2a, args.s2b); res.update(r2)
    if not res:
        ap.error("provide --s1a/--s1b and/or --s2a/--s2b, or --selftest")
    write_outputs(args.out, res, percol, subsets, conf, conf_pol, dis1, dis2)
    for k, v in res.items():
        print(f"{k}: {v:.3f}" if isinstance(v, float) else f"{k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
