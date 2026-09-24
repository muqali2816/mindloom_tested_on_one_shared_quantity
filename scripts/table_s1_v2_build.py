#!/usr/bin/env python3
"""Build Table S1 v2 (long format), validate the prediction register S4 v2, and derive the
column typology and tallies from the two tables.

Inputs (inputs/):
  Table_S1_v1_3.csv              deposit v1.3 theory-by-quantity table (88 cells, 11 accounts x 8 quantities)
  accounts_manifest.csv          12 accounts with theory_id (HOT and HOSS separate)
  domains_manifest.csv           10 domains (M4 split into M4a/M4b/M4c)
  m4_codes_user.csv              first coder's M4a/b/c codes (plan v3.1, 'S1 v2' step)
  s1_v2_coder_annotations.csv    source loci, relation, polarity, flags (make_annotations.py)
  Table_S4_v2_register.csv       prediction register (make_register.py)
Outputs (cwd):
  Table_S1_v2.csv, Table_S4_v2.csv, column_typology_v2.csv, column_typology_v2_notes.md,
  tallies_v2.csv, key_numbers.json
Every number in the notes is computed here; nothing is typed.
"""
import pandas as pd, numpy as np, json, os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); IN = os.path.join(HERE, 'inputs')
CODES = {'EXPLICIT', 'INTERPRETED', 'NOT_LOCATED', 'NOT_APPLICABLE', 'UNRESOLVED'}
LEGACY_MAP = {'YES': ('EXPLICIT', 'positive'), 'YES (negative)': ('EXPLICIT', 'null'), 'IMPLICIT': ('INTERPRETED', None), 'NO': ('NOT_LOCATED', '')}
USER_MAP = {'YES': ('EXPLICIT', 'positive'), 'Y(neg)': ('EXPLICIT', 'null'), 'IMPLICIT': ('INTERPRETED', None), 'NO': ('NOT_LOCATED', '')}
LEGACY_DOMAIN_NAMES = {'M4': 'autonomic / interoceptive channel involvement (v1.3 M4, superseded by M4a-M4c)'}
# manuscript v3 claims per domain (for the comparison in the notes; these are the claims being audited, not inputs to the coding)
MANUSCRIPT_CLAIMS = {'M8': 'shared (occupied, not contested)', 'M4': 'contested', 'M1': 'single-occupant', 'M2': 'single-occupant', 'M5': 'thin',
                     'M6': 'occupied-not-contested', 'M7': 'occupied-not-contested', 'M3': 'occupied-not-contested'}

s1 = pd.read_csv(os.path.join(IN, 'Table_S1_v1_3.csv'))
acc = pd.read_csv(os.path.join(IN, 'accounts_manifest.csv')).fillna('')
dom = pd.read_csv(os.path.join(IN, 'domains_manifest.csv'))
m4 = pd.read_csv(os.path.join(IN, 'm4_codes_user.csv'), keep_default_na=False)
ann = pd.read_csv(os.path.join(IN, 's1_v2_coder_annotations.csv'), keep_default_na=False)
reg = pd.read_csv(os.path.join(IN, 'Table_S4_v2_register.csv'), keep_default_na=False)

assert len(acc) == 12 and len(dom) == 10, (len(acc), len(dom))
assert s1.shape[0] == 88 and s1.theory.nunique() == 11
# legacy name -> theory_id (the merged HOT/HOSS row maps to both split ids)
LEGACY_NAME = {'GNWT': 'GNWT', 'IIT (3.0/4.0)': 'IIT', 'Recurrent processing (RPT)': 'RPT', 'HOT / HOSS': None, 'AST': 'AST',
               'Predictive processing / beast machine': 'PP', 'Supramodular interaction theory (SIT)': 'SIT', 'Passive frame theory': 'PFT',
               'Neural subjective frame': 'NSF', 'UAL': 'UAL', 'Feinberg & Mallatt': 'FM'}
ID2LEGACY = {v: k for k, v in LEGACY_NAME.items() if v}; ID2LEGACY['HOT'] = 'HOT / HOSS'; ID2LEGACY['HOSS'] = 'HOT / HOSS'
assert set(LEGACY_NAME) == set(s1.theory), set(s1.theory) ^ set(LEGACY_NAME)
ANN = {(r.theory_id, r.domain_id): r for r in ann.itertuples(index=False)}
DOMNAME = dict(zip(dom.domain_id, dom.domain)); DOMNAME.update(LEGACY_DOMAIN_NAMES)
stated = reg[reg.status == 'stated']
PRED = {}
for r in stated.itertuples(index=False):
    PRED.setdefault((r.theory_id, r.quantity_id), []).append(r.id)

rows = []
def emit(base, pids):
    if not pids:
        rows.append({**base, 'prediction_id': ''}); return
    for p in pids:
        rows.append({**base, 'prediction_id': p})

for a in acc.itertuples(index=False):
    tid, tname = a.theory_id, a.theory
    split = tid in ('HOT', 'HOSS')
    # ---- 8 legacy quantities (M1..M8 of v1.3), M4 kept as a superseded row ----
    for q in ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']:
        leg = s1[(s1.theory == ID2LEGACY[tid]) & (s1.quantity_id == q)]
        assert len(leg) == 1, (tid, q)
        leg = leg.iloc[0]
        code, pol = LEGACY_MAP[leg.code]
        an = ANN[(tid, q)]
        if an.code_override:
            # allowed only for (i) NO -> NOT_APPLICABLE (theory excludes the domain by its own statement) and (ii) the HOT/HOSS split
            assert (leg.code == 'NO' and an.code_override == 'NOT_APPLICABLE') or (split and an.code_override == 'NOT_LOCATED'), (tid, q, an.code_override)
            assert an.flag_for_adjudication or an.code_override == 'NOT_APPLICABLE', (tid, q)
            code = an.code_override; pol = ''
        if code == 'INTERPRETED':
            pol = an.polarity; assert pol in ('positive', 'null', 'negative'), (tid, q, pol)
        if code == 'EXPLICIT':
            assert an.polarity == pol or an.polarity == '', (tid, q, an.polarity, pol)
        superseded = (q == 'M4')
        pids = [] if superseded else PRED.get((tid, q), [])
        base = dict(theory_id=tid, theory=tname, row_class=a.row_class, origin=a.origin, domain_id=q, domain=DOMNAME[q],
                    code=code, polarity=pol if code in ('EXPLICIT', 'INTERPRETED') else '', relation=an.relation if code in ('EXPLICIT', 'INTERPRETED') else '',
                    claim_text=an.claim_text, source_label=an.source_label, source_doi=an.source_doi, source_locus=an.source_locus, evidence_status=an.evidence_status,
                    confidence=an.confidence, provisional=bool(split), legacy_code=leg.code, legacy_justification=leg.prediction, legacy_source_label=leg.citation_label,
                    legacy_source_doi=leg.citation_doi, superseded_by='M4a;M4b;M4c' if superseded else '', flag_for_adjudication=an.flag_for_adjudication,
                    note=an.note, coder='author1')
        emit(base, pids)
    # ---- 3 new sub-columns, first coder's codes ----
    for q in ['M4a', 'M4b', 'M4c']:
        u = m4[(m4.theory_id == tid) & (m4.domain_id == q)]
        assert len(u) == 1, (tid, q); u = u.iloc[0]
        code, pol = USER_MAP[u.user_code]
        an = ANN[(tid, q)]
        assert an.code_override == '', (tid, q, 'first-coder codes are never overridden')
        if code == 'INTERPRETED':
            pol = an.polarity; assert pol in ('positive', 'null', 'negative'), (tid, q, pol)
        pids = PRED.get((tid, q), [])
        note = '; '.join(x for x in [u.user_note, an.note] if x)
        if tid in ('SIT', 'PFT') and q == 'M4c':
            assert 'not a denial of bodily feelings' in note, (tid, q)
        base = dict(theory_id=tid, theory=tname, row_class=a.row_class, origin='added-in-revision', domain_id=q, domain=DOMNAME[q],
                    code=code, polarity=pol if code in ('EXPLICIT', 'INTERPRETED') else '', relation=an.relation if code in ('EXPLICIT', 'INTERPRETED') else '',
                    claim_text=an.claim_text, source_label=an.source_label, source_doi=an.source_doi, source_locus=an.source_locus, evidence_status=an.evidence_status,
                    confidence=an.confidence, provisional=True, legacy_code='', legacy_justification='', legacy_source_label='', legacy_source_doi='',
                    superseded_by='', flag_for_adjudication=an.flag_for_adjudication, note=note, coder='author1')
        emit(base, pids)

S1 = pd.DataFrame(rows)
S1['cell_id'] = S1.theory_id + 'x' + S1.domain_id
S1['first_coder_code_M4'] = ''
for u in m4.itertuples(index=False):
    S1.loc[(S1.theory_id == u.theory_id) & (S1.domain_id == u.domain_id), 'first_coder_code_M4'] = u.user_code
COLS = ['cell_id', 'theory_id', 'theory', 'row_class', 'origin', 'domain_id', 'domain', 'prediction_id', 'code', 'polarity', 'relation', 'claim_text',
        'source_label', 'source_doi', 'source_locus', 'evidence_status', 'confidence', 'provisional', 'legacy_code', 'first_coder_code_M4', 'superseded_by',
        'flag_for_adjudication', 'legacy_justification', 'legacy_source_label', 'legacy_source_doi', 'note', 'coder']
S1 = S1[COLS]

# ---------------- validation ----------------
live = S1[S1.superseded_by == '']
cells = live.drop_duplicates('cell_id')
assert set(cells.domain_id) == set(dom.domain_id) and len(cells) == 120, len(cells)
assert cells.code.isin(CODES).all()
pos = cells[cells.code.isin(['EXPLICIT', 'INTERPRETED'])]
for r in pos.itertuples(index=False):
    assert r.source_doi and r.source_locus and r.relation and r.polarity in ('positive', 'null', 'negative'), r.cell_id
exp_cells = set(cells[cells.code == 'EXPLICIT'].cell_id)
covered = set(live[(live.code == 'EXPLICIT') & (live.prediction_id != '')].cell_id)
assert exp_cells == covered, ('EXPLICIT cells without a P-id:', exp_cells - covered)
stated_cells = {f"{r.theory_id}x{r.quantity_id}" for r in stated.itertuples(index=False)}
assert stated_cells <= exp_cells, ('stated P-ids pointing at non-EXPLICIT cells:', stated_cells - exp_cells)
assert reg.id.is_unique
allp = set(reg.id)
for r in reg.itertuples(index=False):
    for p in [x.strip() for x in r.distinguishable_from.split(';') if x.strip()]:
        assert p in allp, (r.id, p)
        assert r.id in reg.loc[reg.id == p, 'distinguishable_from'].iloc[0], ('asymmetric pair', r.id, p)
        assert reg.loc[reg.id == p, 'quantity_id'].iloc[0] == r.quantity_id, ('cross-domain pair', r.id, p)
        assert reg.loc[reg.id == p, 'status'].iloc[0] == 'stated' and r.status == 'stated', ('derived row in a distinguishable pair', r.id, p)
assert set(S1.legacy_code[S1.legacy_code != '']) == set(s1.code)
# legacy codes are kept: no legacy cell changed code except via the two documented routes
for r in S1[S1.legacy_code != ''].drop_duplicates('cell_id').itertuples(index=False):
    exp_code = LEGACY_MAP[r.legacy_code][0]
    if r.code != exp_code:
        assert (r.code == 'NOT_APPLICABLE' and r.legacy_code == 'NO') or (r.theory_id in ('HOT', 'HOSS') and r.code == 'NOT_LOCATED'), r.cell_id

# ---------------- typology and tallies ----------------
def pairs_in(domain_id, min_conf=1):
    sub = reg[(reg.quantity_id == domain_id) & (reg.status == 'stated')]
    seen = set()
    for r in sub.itertuples(index=False):
        c = int(r.distinguishability_confidence) if str(r.distinguishability_confidence).strip() else 0
        for p in [x.strip() for x in r.distinguishable_from.split(';') if x.strip()]:
            if c >= min_conf:
                seen.add(tuple(sorted((r.id, p))))
    return seen

def classify(n_explicit, n_interp, n_pairs):
    if n_explicit >= 2 and n_pairs >= 1: return 'contested'
    if n_explicit == 1: return 'single-occupant'
    if n_explicit >= 2: return 'occupied-not-contested'
    if n_explicit == 0 and n_interp >= 1: return 'thin'
    return 'unoccupied'

typ = []
for d in dom.itertuples(index=False):
    c = cells[cells.domain_id == d.domain_id]
    n_exp_pos = int(((c.code == 'EXPLICIT') & (c.polarity == 'positive')).sum()); n_exp_null = int(((c.code == 'EXPLICIT') & (c.polarity == 'null')).sum())
    n_exp = n_exp_pos + n_exp_null; n_int = int((c.code == 'INTERPRETED').sum())
    p_all = pairs_in(d.domain_id, 1); p_conf2 = pairs_in(d.domain_id, 2)
    n_stated = int(((stated.quantity_id == d.domain_id)).sum()); n_derived = int(((reg.quantity_id == d.domain_id) & (reg.status == 'derived')).sum())
    typ.append(dict(domain_id=d.domain_id, domain=d.domain, n_explicit_pos=n_exp_pos, n_explicit_null=n_exp_null, n_interpreted=n_int,
                    n_not_located=int((c.code == 'NOT_LOCATED').sum()), n_not_applicable=int((c.code == 'NOT_APPLICABLE').sum()), n_unresolved=int((c.code == 'UNRESOLVED').sum()),
                    explicit_theories=';'.join(c[c.code == 'EXPLICIT'].theory_id), n_stated_predictions=n_stated, n_derived_predictions=n_derived,
                    n_distinguishable_pairs=len(p_all), distinguishable_pairs=';'.join('-'.join(p) for p in sorted(p_all)),
                    n_distinguishable_pairs_conf2=len(p_conf2), derived_class=classify(n_exp, n_int, len(p_all)), derived_class_conf2=classify(n_exp, n_int, len(p_conf2)),
                    n_flagged_cells=int((c.flag_for_adjudication != '').sum()), n_provisional_cells=int(c.provisional.sum()),
                    manuscript_v3_claim=MANUSCRIPT_CLAIMS.get(d.domain_id, MANUSCRIPT_CLAIMS.get('M4') if d.domain_id.startswith('M4') else '')))
typ = pd.DataFrame(typ)
typ['differs_from_manuscript'] = [('' if not m else ('no' if (m.split(' ')[0] == c) else 'yes')) for m, c in zip(typ.manuscript_v3_claim, typ.derived_class)]

tal = []
for d in dom.itertuples(index=False):
    for rc in ['trial-level', 'origin-level', 'all']:
        c = cells[(cells.domain_id == d.domain_id) & ((cells.row_class == rc) if rc != 'all' else True)]
        tal.append(dict(domain_id=d.domain_id, row_class=rc, n_rows=len(c), n_explicit_pos=int(((c.code == 'EXPLICIT') & (c.polarity == 'positive')).sum()),
                        n_explicit_null=int(((c.code == 'EXPLICIT') & (c.polarity == 'null')).sum()), n_interpreted=int((c.code == 'INTERPRETED').sum()),
                        n_interpreted_null=int(((c.code == 'INTERPRETED') & (c.polarity == 'null')).sum()), n_not_located=int((c.code == 'NOT_LOCATED').sum()),
                        n_not_applicable=int((c.code == 'NOT_APPLICABLE').sum()), n_unresolved=int((c.code == 'UNRESOLVED').sum()),
                        n_submitted_v1=int((c.origin == 'submitted-v1').sum()), n_added_in_revision=int((c.origin == 'added-in-revision').sum())))
tal = pd.DataFrame(tal)

# ---------------- write ----------------
S1.to_csv(os.path.join(HERE, 'Table_S1_v2.csv'), index=False)
reg.to_csv(os.path.join(HERE, 'Table_S4_v2.csv'), index=False)
typ.to_csv(os.path.join(HERE, 'column_typology_v2.csv'), index=False)
tal.to_csv(os.path.join(HERE, 'tallies_v2.csv'), index=False)

flagged = cells[cells.flag_for_adjudication != '']
key = dict(rows_total=int(len(S1)), cells_total=int(len(cells)), cells_superseded_legacy_M4=int(S1[S1.superseded_by != ''].cell_id.nunique()),
           cells_explicit=int((cells.code == 'EXPLICIT').sum()), cells_explicit_positive=int(((cells.code == 'EXPLICIT') & (cells.polarity == 'positive')).sum()),
           cells_explicit_null=int(((cells.code == 'EXPLICIT') & (cells.polarity == 'null')).sum()), cells_interpreted=int((cells.code == 'INTERPRETED').sum()),
           cells_not_located=int((cells.code == 'NOT_LOCATED').sum()), cells_not_applicable=int((cells.code == 'NOT_APPLICABLE').sum()), cells_unresolved=int((cells.code == 'UNRESOLVED').sum()),
           cells_provisional=int(cells.provisional.sum()), n_flagged_for_adjudication=int(len(flagged)), flagged_cells=sorted(flagged.cell_id.tolist()),
           n_abstract_only=int((cells.evidence_status == 'abstract-only').sum()), n_full_text=int((cells.evidence_status == 'full-text').sum()), n_secondary=int((cells.evidence_status == 'secondary').sum()),
           n_abstract_only_positive_cells=int(((cells.evidence_status == 'abstract-only') & cells.code.isin(['EXPLICIT', 'INTERPRETED'])).sum()),
           register_rows=int(len(reg)), register_stated=int((reg.status == 'stated').sum()), register_derived=int((reg.status == 'derived').sum()),
           n_distinguishable_pairs_total=int(typ.n_distinguishable_pairs.sum()), per_domain_derived_class=dict(zip(typ.domain_id, typ.derived_class)),
           per_domain_derived_class_conf2=dict(zip(typ.domain_id, typ.derived_class_conf2)), legacy_cells_mapped=int(S1[S1.legacy_code != ''].cell_id.nunique()),
           legacy_code_counts=S1[S1.legacy_code != ''].drop_duplicates('cell_id').legacy_code.value_counts().to_dict())
json.dump(key, open(os.path.join(HERE, 'key_numbers.json'), 'w'), indent=1)

# ---------------- notes (all numbers from the tables) ----------------
L = ['# Column typology v2 — derived from Table_S1_v2.csv and Table_S4_v2.csv', '',
     f"Screening positions: {key['cells_total']} cells (12 accounts x 10 domains), {key['rows_total']} rows in long format including {key['cells_superseded_legacy_M4']} superseded legacy M4 cells (kept for traceability, excluded from all counts below).",
     f"Codes over the {key['cells_total']} live cells: EXPLICIT {key['cells_explicit']} (positive {key['cells_explicit_positive']}, null {key['cells_explicit_null']}), INTERPRETED {key['cells_interpreted']}, NOT_LOCATED {key['cells_not_located']}, NOT_APPLICABLE {key['cells_not_applicable']}, UNRESOLVED {key['cells_unresolved']}.",
     f"Provisional cells (HOT/HOSS split and M4a-c): {key['cells_provisional']} of {key['cells_total']}. Cells flagged for adjudication: {key['n_flagged_for_adjudication']} of {key['cells_total']}. Cells whose source was read as abstract only: {key['n_abstract_only']} of {key['cells_total']} (full text {key['n_full_text']}, secondary {key['n_secondary']}).",
     f"Register: {key['register_rows']} predictions, {key['register_stated']} stated and {key['register_derived']} derived; {key['n_distinguishable_pairs_total']} distinguishable pairs among stated predictions.", '',
     '| domain | EXPLICIT pos | EXPLICIT null | INTERPRETED | NOT_LOCATED | NOT_APPLICABLE | distinguishable pairs (conf>=2) | derived class | manuscript v3 claim | differs |', '|---|---|---|---|---|---|---|---|---|---|']
for r in typ.itertuples(index=False):
    L.append(f"| {r.domain_id} {r.domain} | {r.n_explicit_pos} | {r.n_explicit_null} | {r.n_interpreted} | {r.n_not_located} | {r.n_not_applicable} | {r.n_distinguishable_pairs} ({r.n_distinguishable_pairs_conf2}) | {r.derived_class}{'' if r.derived_class == r.derived_class_conf2 else ' [conf>=2: ' + r.derived_class_conf2 + ']'} | {r.manuscript_v3_claim} | {r.differs_from_manuscript} |")
L += ['', '## Where the derived class differs from the manuscript (v3) claims', '']
for r in typ.itertuples(index=False):
    if r.differs_from_manuscript == 'yes':
        L.append(f"- **{r.domain_id}**: manuscript says '{r.manuscript_v3_claim}'; the tables give '{r.derived_class}' ({r.n_explicit_pos + r.n_explicit_null} EXPLICIT: {r.explicit_theories}; {r.n_distinguishable_pairs} distinguishable pairs: {r.distinguishable_pairs or 'none'}).")
L += ['', '## Where it agrees', '']
for r in typ.itertuples(index=False):
    if r.differs_from_manuscript == 'no':
        L.append(f"- {r.domain_id}: '{r.derived_class}' ({r.n_explicit_pos + r.n_explicit_null} EXPLICIT: {r.explicit_theories or '—'}; INTERPRETED {r.n_interpreted}).")
L += ['', '## Sensitivity', '']
for r in typ.itertuples(index=False):
    if r.derived_class != r.derived_class_conf2:
        L.append(f"- {r.domain_id}: the class rests on a pair with distinguishability confidence 1 ({r.distinguishable_pairs}); with confidence >= 2 required it is '{r.derived_class_conf2}'.")
fl = cells[(cells.flag_for_adjudication != '') & cells.code.isin(['EXPLICIT'])]
if len(fl):
    L.append(f"- EXPLICIT cells carrying an adjudication flag ({len(fl)} of {key['cells_explicit']}): {', '.join(fl.cell_id)}. If a flagged EXPLICIT cell were downgraded to INTERPRETED, the class of its domain would change only where the EXPLICIT count crosses 1 or 2.")
open(os.path.join(HERE, 'column_typology_v2_notes.md'), 'w').write('\n'.join(L) + '\n')
if __name__ == '__main__':
    print(json.dumps({k: v for k, v in key.items() if k not in ('flagged_cells',)}, indent=1))
    print(typ[['domain_id', 'n_explicit_pos', 'n_explicit_null', 'n_interpreted', 'n_not_located', 'n_not_applicable', 'n_distinguishable_pairs', 'derived_class', 'derived_class_conf2', 'differs_from_manuscript']].to_string(index=False))
