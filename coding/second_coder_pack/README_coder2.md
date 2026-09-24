# Second-coder pack v3.4 — brainsci-4583950

This pack contains no first-coder codes, claim texts, sources or predictions. Table S4 (the prediction register) is NOT included: it lists every cell the first coder marked EXPLICIT, so it would reveal the codes. You receive S4 and a pair list with empty assessment fields after your S1 form is returned, for the second step (relation of every cross-theory pair of stated predictions).

Order of work
1. Read codebook_v2.md (v2.4, frozen; verify its hash: `sed '$d' codebook_v2.md | shasum -a 256` (macOS) or `head -n -1 codebook_v2.md | sha256sum` (GNU) must equal the value in codebook_v2.sha256).
2. Fill S1_blank_for_coder2_v2.csv — 120 cells (12 accounts × 10 domains): code, polarity (positive / stated_null / negative), relation, claim_text, source_label, source_doi, source_locus, evidence_status, confidence. Code from the primary sources listed in the codebook, not from memory of the submitted Table 1.
3. Fill S2_blank_for_coder2_v3.csv — 32 publications, one row each; partition each publication into experiments yourself (duplicate the row per experiment, ids <publication_id>-E1, -E2, …), then code the raw fields, attributions and contested inclusion per row (codebook §1 item 4).
3a. Optional: S3_blank_for_coder2.csv — 10 theory blocks × 12 ConTraSt dimensions (codebook §7).
4. Log start/end per block in coder2_timing_log.csv and return the forms. The first author runs agreement.py; disagreements are adjudicated jointly with a written record.

Blindness, stated plainly: the second author read the submitted manuscript, including its condensed 72-cell Table 1 with the legacy codes. The submitted Table 1 had 72 cells; in the current 120-cell table 70 cells carry the label `submitted-v1` (the 72 minus the two whose row was split and re-sourced) and 50 carry `added-in-revision`. Blindness is therefore partial for the 70 and full for the 50; agreement is reported for the two subsets separately. Nothing in this pack carries a first-coder decision on any cell, row or pair.


**Handover date:** ____ (recorded by the first author when this pack is sent; the second coder had not seen the revised manuscript, the response to reviewers or any coding file before that date).
