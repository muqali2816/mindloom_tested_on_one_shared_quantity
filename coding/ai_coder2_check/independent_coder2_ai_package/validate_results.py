#!/usr/bin/env python3
"""Structural/evidence-provenance checks, not an independent semantic re-coding."""
from pathlib import Path
import csv,json,hashlib,collections
from build_results import content
BASE=Path(__file__).resolve().parent
def csvrows(name):return list(csv.DictReader((BASE/name).open(encoding='utf-8-sig',newline='')))
def main():
    checks=[]
    def check(label,condition):
        checks.append({'check':label,'passed':bool(condition)})
        if not condition:raise AssertionError(label)
    s1=json.loads((BASE/'decisions_s1.json').read_text());s2=json.loads((BASE/'decisions_s2.json').read_text());parts=json.loads((BASE/'publication_partitions.json').read_text())
    blank=csvrows('protocol/S1_blank_for_coder2_v2.csv');pubs=csvrows('protocol/S2_blank_for_coder2_v3.csv');sources=csvrows('source_audit.csv')
    cb=(BASE/'protocol/codebook_v2.md').read_bytes();body=cb[:cb.index(b'**Codebook v2.4')]
    digest=hashlib.sha256(body).hexdigest()
    check('Frozen codebook byte hash',digest=='6b2e7ad9df83b763c215eb79714fde83cf2a620eff8a9e3e95e80d3980ab8dcc')
    key=lambda r:(r['theory_id'],r['domain_id'])
    check('Exactly 120 unique S1 cells',len(s1)==len({key(r) for r in s1})==120)
    check('S1 grid equals original template',{key(r) for r in s1}=={key(r) for r in blank})
    old={key(r):r for r in blank};meta=['theory_id','theory','row_class','origin','domain_id','domain']
    check('All S1 metadata preserved',all(all(r[f]==old[key(r)][f] for f in meta) for r in s1))
    codes={'EXPLICIT','INTERPRETED','NOT_LOCATED','NOT_APPLICABLE','UNRESOLVED'};pols={'positive','stated_null','negative'};relations={'effect','modulation','necessity','sufficiency','constitution','marker','scope'}
    check('S1 permitted codes',all(r['code'] in codes for r in s1))
    check('S1 conditional polarity/relation',all((r['polarity'] in pols and r['relation'] in relations) if r['code'] in {'EXPLICIT','INTERPRETED'} else (not r['polarity'] and not r['relation']) for r in s1))
    check('Every S1 decision has claim/source/locus/confidence',all(all(r[f] for f in ['claim_text','source_label','source_doi','source_locus']) and r['confidence'] in {'1','2','3'} for r in s1))
    check('Provisional flag equals evidence-status rule',all(r['provisional']==(r['evidence_status']!='full-text') for r in s1+s2))
    audited={r['doi'].lower() for r in sources}
    check('Every S1/S2 DOI in source audit',all(d.strip().lower() in audited for r in s1+s2 for d in r.get('source_doi',r.get('doi','')).split(';')))
    check('All 75 supplied DOI identities resolve',len(sources)==75 and all(r['crossref_status']=='resolved' and r['doi'].lower()==r['resolved_doi'].lower() for r in sources))
    check('Every original publication accounted for',{r['publication_id'] for r in pubs}=={r['publication_id'] for r in parts})
    check('S2 unique experiment IDs',len(s2)==len({r['experiment_id'] for r in s2}))
    for p in parts:
        rr=[r for r in s2 if r['publication_id']==p['publication_id']]
        check('Partition '+p['publication_id'],len(rr)==p['n_rows_returned']==p['n_experiments_identified'] and all(r['n_experiments_identified']==len(rr) for r in rr) and [r['experiment_id'] for r in rr]==[p['publication_id']+'-E'+str(i+1) for i in range(len(rr))])
    check('P35 reanalysis has zero experiment rows',not any(r['publication_id']=='P35' for r in s2))
    vocab={'modality':{'visual','auditory','tactile','motor','interoceptive','mixed','not applicable','UNRESOLVED'},'affective_status':{'neutral','valenced','interoceptive','UNRESOLVED'},'report_type':{'report','no-report','both','UNRESOLVED'}}
    check('S2 vocabularies',all(r[f] in vals for r in s2 for f,vals in vocab.items()))
    check('Motor rows identify effector; nonmotor rows leave it empty',all((r['effector_type'] in {'skeletal','autonomic','UNRESOLVED'}) if r['modality']=='motor' else r['effector_type']=='' for r in s2))
    check('Every contested row has a reason',all(not r['contested_inclusion'] or r['contested_reason'] for r in s2))
    check('S2 manipulation, outcome and attribution provenance populated',all(all(r[f] for f in ['manipulation','measured_outcome','theory_attribution_by_authors','by_authors_locus','theory_attribution_later','later_attribution_evidence','source_locus']) for r in s2))
    accounts={r['theory_id'] for r in blank}
    check('Attribution tokens match account IDs or explicit missingness',all(t.strip() in accounts|{'none found','UNRESOLVED'} for r in s2 for f in ['theory_attribution_by_authors','theory_attribution_later'] for t in r[f].split(';')))
    check('Later positive attribution carries context category and DOI',all(r['theory_attribution_later']=='none found' or ('10.' in r['later_attribution_evidence'] and any(v in r['later_attribution_evidence'] for v in ['CONTEXT_NAMED','CONTEXT_UNNAMED','REFLIST'])) for r in s2))
    check('CSV outputs retain all decisions',len(csvrows('S1_coder2_AI.csv'))==len(s1) and len(csvrows('S2_coder2_AI.csv'))==len(s2))
    derived=csvrows('S2_derived.csv');lookup={r['experiment_id']:r for r in s2}
    check('Derived classes agree with explicit raw rules',all(r['content_class_7way']==content(lookup[r['experiment_id']]) for r in derived))
    sensitivity=csvrows('s2_sensitivity.csv')
    check('Each sensitivity denominator excludes state and unresolved',all(int(r['content_denominator'])==int(r['n_rows'])-int(r['state (no content)'])-int(r['UNRESOLVED']) for r in sensitivity))
    report={'status':'PASSED','checks_passed':len(checks),'codebook_sha256':digest,'S1_rows':len(s1),'S2_rows':len(s2),'publications':len(parts),'checks':checks,'semantic_limit':'Structural validation is not independent verification of literature judgments. See adjudication notes and evidence limitations.','intercoder_agreement_computed':False}
    (BASE/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
