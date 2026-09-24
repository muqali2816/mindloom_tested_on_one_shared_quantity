# Second-coder pack v3.2 — brainsci-4583950

This pack contains no first-coder codes, claim texts, sources or predictions. Table S4 (the prediction register) is NOT included: it lists every cell the first coder marked EXPLICIT, so it would reveal the codes. You receive S4 after your S1 form is returned, for the second step (distinguishability of prediction pairs).

Order of work
1. Read codebook_v2.md (v2.2, frozen; verify its hash: `sed '$d' codebook_v2.md | shasum -a 256` (macOS) or `head -n -1 codebook_v2.md | sha256sum` (GNU) must equal the value in codebook_v2.sha256).
2. Fill S1_blank_for_coder2_v2.csv — 120 cells (12 accounts × 10 domains): code, polarity (positive / stated_null / negative), relation, claim_text, source_label, source_doi, source_locus, evidence_status, confidence. Code from the primary sources listed in the codebook, not from memory of the submitted Table 1.
3. Fill S2_blank_for_coder2_v2.csv — 42 experiments: modality, affective_status, manipulation, measured_outcome, report_type, theory_attribution_by_authors (with locus), contested_inclusion (with reason).
4. Log start/end per block in coder2_timing_log.csv and return the two forms. The first author runs agreement.py; disagreements are adjudicated jointly with a written record.
