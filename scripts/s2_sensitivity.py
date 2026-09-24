# s2_sensitivity.py — scenario counts for Table S2 v2 (unit = experiment).
# Usage: python s2_sensitivity.py [Table_S2_v2.csv] [s2_sensitivity.csv]
# Every number in s2_sensitivity.csv is produced here from the table; nothing is typed.
import csv, sys, json
from collections import Counter

src = sys.argv[1] if len(sys.argv) > 1 else 'Table_S2_v2.csv'
out = sys.argv[2] if len(sys.argv) > 2 else 's2_sensitivity.csv'
rows = list(csv.DictReader(open(src)))
B = lambda v: str(v).strip().lower() == 'true'
CLASSES = ['neutral-visual', 'neutral-nonvisual', 'motor-conflict', 'valenced', 'interoceptive']

def is_whalen(r):      return r['citation_label'].startswith('Whalen')
def is_metacog(r):     return B(r['contested_inclusion']) and 'metacognitive index' in r['contested_reason']
def is_contested(r):   return B(r['contested_inclusion'])
def is_ancillary(r):   return B(r['ancillary_experiment'])
def has_content(r):    return B(r['has_content_manipulation'])

def ta_default(r): return B(r['theory_addressed'])                 # authors or later (any evidence)
def ta_strict(r):  return B(r['theory_addressed_strict'])          # authors, or later with citing context read and theory named
def ta_coder(r):   return B(r['theory_addressed_incl_coder'])      # default plus coder inference
def ta_any(r):     return True                                     # no theory filter

# A scenario = (name, description, row filter, theory-addressed rule, unit)
def base_filter(r, whalen=False, metacog=True, other_contested=True, ancillary=True):
    if not has_content(r): return False
    if is_whalen(r): return whalen
    if is_metacog(r): return metacog
    if is_contested(r): return other_contested      # Farb, and any contested row that is neither Whalen nor metacognitive
    if is_ancillary(r) and not ancillary: return False
    return True

scenarios = [
 ('S0_baseline', 'Experiments; theory_addressed by authors or a later theory statement (any evidence); Whalen excluded; metacognition rows included; other contested rows (Farb) included; ancillary experiments included',
  lambda r: base_filter(r), ta_default),
 ('S1_plus_whalen', 'Baseline + Whalen et al. 1998', lambda r: base_filter(r, whalen=True), ta_default),
 ('S2_minus_metacognition', 'Baseline − metacognition rows (Maniscalco & Lau 2012, Rounis 2010, Fleming 2010, Fleming 2014, Garfinkel 2015)', lambda r: base_filter(r, metacog=False), ta_default),
 ('S3_minus_all_contested', 'Baseline − every contested_inclusion row (Whalen, metacognition rows, Farb)', lambda r: base_filter(r, metacog=False, other_contested=False), ta_default),
 ('S4_plus_all_contested', 'All contested_inclusion rows included (= baseline + Whalen; the others are already in)', lambda r: base_filter(r, whalen=True), ta_default),
 ('S5_plus_coder_attribution', 'Baseline, theory_addressed also by coder inference', lambda r: base_filter(r), ta_coder),
 ('S6_strict_later_attribution', 'Baseline, but a later attribution counts only if its citing sentence was read and names the theory (reference-list-only hits dropped)', lambda r: base_filter(r), ta_strict),
 ('S7_minus_ancillary', 'Baseline − ancillary/control experiments (Sergent 2021 controls 1–2; Morsella 2009 smooth-muscle control)', lambda r: base_filter(r, ancillary=False), ta_default),
 ('S8_no_theory_filter', 'All content experiments regardless of theory attribution (Whalen excluded)', lambda r: base_filter(r), ta_any),
 ('S9_no_theory_filter_plus_whalen', 'All content experiments regardless of theory attribution, Whalen included', lambda r: base_filter(r, whalen=True), ta_any),
 ('S10_strict_minus_all_contested', 'Strict later attribution and every contested row removed (most conservative)', lambda r: base_filter(r, metacog=False, other_contested=False), ta_strict),
]

def tally(sel):
    c = Counter(r['content_class_v2'] for r in sel)
    n = len(sel)
    return n, {k: c.get(k, 0) for k in CLASSES}

records = []
for name, desc, filt, ta in scenarios:
    sel = [r for r in rows if filt(r) and ta(r)]
    n, counts = tally(sel)
    rec = dict(scenario=name, unit='experiment', description=desc, n_denominator=n,
               n_publications=len({r['publication_id'] for r in sel}))
    for k in CLASSES: rec[k] = f'{counts[k]} of {n}'
    rec['neutral_visual_fraction'] = round(counts['neutral-visual'] / n, 3) if n else ''
    rec['experiment_ids'] = ';'.join(r['experiment_id'] for r in sel)
    records.append(rec)

# ---- historical scenarios (publication level, legacy columns), for reproduction only — not targets ----
pubs = {}
for r in rows: pubs.setdefault(r['publication_id'], r)          # one row per publication (legacy fields identical across experiments)
legacy_ta = lambda r: r['legacy_theory_addressed'].strip() != 'none of the coded theories'
legacy_content_ok = lambda r: r['legacy_content'] != 'state (no content)'
# v1.3 reported 21 of 27 with the four paradigm-defining rows inside the denominator; those rows are no longer in this table,
# so the closest reproducible historical scenario here is "publication level, legacy codes, paradigm rows out" (v3 §7.6 reported 19 of 24).
hist_sel = [r for r in pubs.values() if legacy_content_ok(r) and legacy_ta(r)]
n = len(hist_sel); c = Counter(r['legacy_content'] for r in hist_sel)
rec = dict(scenario='H1_legacy_publication_level_no_paradigm_rows', unit='publication (legacy codes)',
           description='Historical reproduction: v1.3 legacy content and theory codes, one row per publication, paradigm-defining rows outside the denominator (manuscript v3 §7.6 reported 19 of 24 neutral visual)',
           n_denominator=n, n_publications=n)
for k in CLASSES: rec[k] = f'{c.get(k,0)} of {n}'
rec['neutral_visual_fraction'] = round(c.get('neutral-visual',0)/n,3) if n else ''
rec['experiment_ids'] = ';'.join(sorted(r['publication_id'] for r in hist_sel))
records.append(rec)
# with the four paradigm rows added back (their legacy codes: 3 neutral-visual GNWT-linked + 1 motor-conflict; Boly 2017 was 'state')
para = [('P02','neutral-visual'),('P05','neutral-visual'),('P25','motor-conflict')]   # P15 Boly 2017 legacy 'state (no content)' → outside content denominator
n2 = n + len(para); c2 = Counter(c); 
for _, k in para: c2[k] += 1
rec = dict(scenario='H0_legacy_publication_level_with_paradigm_rows', unit='publication (legacy codes)',
           description='Historical reproduction: as H1 with the three content-coded paradigm-defining rows (Melloni 2023, Dehaene 2006, Poehlman 2012) added back (manuscript v3 Table 2 reported 21 of 27)',
           n_denominator=n2, n_publications=n2)
for k in CLASSES: rec[k] = f'{c2.get(k,0)} of {n2}'
rec['neutral_visual_fraction'] = round(c2.get('neutral-visual',0)/n2,3)
rec['experiment_ids'] = rec['experiment_ids'] = ';'.join(sorted([r['publication_id'] for r in hist_sel] + [p for p,_ in para]))
records.append(rec)

cols = ['scenario','unit','description','n_denominator','n_publications'] + CLASSES + ['neutral_visual_fraction','experiment_ids']
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(records)

# summary numbers for the structured report
base = records[0]
exp_rows = [r for r in rows]
summary = dict(
    n_experiments_total=len(exp_rows), n_publications_total=len({r['publication_id'] for r in exp_rows}),
    n_content_experiments=sum(has_content(r) for r in exp_rows),
    baseline={k: base[k] for k in ['n_denominator','n_publications'] + CLASSES},
    n_contested_inclusion_rows=sum(is_contested(r) for r in exp_rows),
    n_contested_publications=len({r['publication_id'] for r in exp_rows if is_contested(r)}),
    n_abstract_only_rows=sum(r['evidence_status'].startswith('abstract only') for r in exp_rows),
    n_abstract_only_publications=len({r['publication_id'] for r in exp_rows if r['evidence_status'].startswith('abstract only')}),
    smallest_neutral_visual_share=min((r for r in records if r['unit']=='experiment' and r['neutral_visual_fraction']!=''), key=lambda r: r['neutral_visual_fraction'])['scenario'],
    largest_neutral_visual_share=max((r for r in records if r['unit']=='experiment' and r['neutral_visual_fraction']!=''), key=lambda r: r['neutral_visual_fraction'])['scenario'],
)
json.dump(summary, open('handoff/s2_summary.json','w'), indent=1)
for r in records:
    print(f"{r['scenario']:<48} n={r['n_denominator']:>3} | " + ' | '.join(f"{k[:9]} {r[k]}" for k in CLASSES) + f" | frac {r['neutral_visual_fraction']}")
print(json.dumps(summary, indent=1))
