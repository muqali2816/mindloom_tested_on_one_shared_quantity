# S3 (ConTraSt dimensions) coverage note

Table_S3_contrast_dimensions.csv (deposit v1.3) codes 10 theory rows against 12 ConTraSt dimensions (120 cells) with the v1.3 four-code scheme (YES / IMPLICIT / NO / Y(neg)).

## Which of the 12 manifest accounts are absent, and why

The 12-account manifest (accounts_manifest.csv) has 12 theory_ids; S3 covers 11 of them through 10 rows:

1. **NSF (neural subjective frame) — no row.** The account was added to Table S1 after the ConTraSt coding had been done (manuscript v3, §7.5: "ten rows, since the neural subjective frame was added after that coding"). Its absence is a sequencing artefact of the revision, not a judgement that the account has nothing to say on the ConTraSt axes; C9 (dependent measure, which in ConTraSt includes cardiac tags such as the heartbeat-evoked potential) and C11 (spatial findings) would in fact be the two dimensions on which NSF states most.
2. **HOSS — not separated from HOT.** S3 carries a single merged row 'HOT / HOSS'. The manifest now splits the two (row note: 'split from merged HOT/HOSS row in v1.3'), so S3 has 10 rows where S1 v2 has 12. The merged row was coded from both Lau & Rosenthal 2011 and Fleming 2020; separating it requires re-reading each cell against one source, as done for S1 v2 (all split cells provisional).

Both gaps are repairable by coding 2 further rows (24 cells); until then any S1 v2 vs S3 comparison must be run on the 10 shared accounts (HOT and HOSS collapsed).

## Can ConTraSt's 12 dimensions serve as an author-independent comparison scheme for this question?

Not as a substitute, and only partly as a check. The scheme is author-independent in provenance — it was built by Yaron, Melloni, Mudrik and colleagues to index what 412 published experiments reported, not to test the present argument — and that is its value: it shows that the accounts coded silent on M1, M2 and M5 are not silent on the axes the field records (GNWT states on 11 of 12 dimensions, IIT on 10, RPT on 7; passive frame theory on 0 of 12, because it declines the implementation level). But three properties limit it as a comparison scheme for *this* question. First, it is a taxonomy of reported experiments, not of theoretical commitments: its dimensions are properties of studies (task type, technique, sample, paradigm), so a 'YES' means the theory states something about a kind of study, not that it predicts how a measurable quantity relates to access. Second, only C10 (temporal findings) and C11 (spatial findings) are dimensions on which predictions can differ in value; the rest record coverage. C10/C11 partly recover M8 and C9 partly recovers M7 and the cardiac side of M4b, but no dimension counts competing response options, codes conflict magnitude, or records cortical–autonomic coherence — none of M1, M2 or M5 has a ConTraSt field, and M3, M4a/M4c and M6 are recoverable only through free-text stimulus and measure labels. Third, ConTraSt was built for human and animal neuroscience experiments, so the origin-level accounts answer its dimensions at the level of comparative markers rather than of experiments (UAL 5 of 12 YES, Feinberg & Mallatt 3 of 12), which makes their S3 rows hard to compare with the trial-level rows. The scheme therefore checks that the M1/M2/M5 result is not the rediscovery of an existing axis and that occupancy elsewhere is uneven in the same direction as the corpus; it cannot adjudicate whether a column is contested, because it has no field for the sign, locus or timing of a prediction outside C10/C11. The S3 tallies per dimension (YES/IMPLICIT/NO) are in Table_S3_tallies.csv; the two S3 dimensions with the fewest stated predictions are C12 (frequency findings, 1 YES) and C10 (temporal findings, 3 YES).

## S3 dimensions
- C1: Type of consciousness (content / state)
- C2: Report / no-report paradigm
- C3: Consciousness measure type (objective / subjective / condition assessment / none)
- C4: Experimental paradigm (family / specific)
- C5: Task type
- C6: Stimulus (modality / category / duration / contrast)
- C7: Sample / population type (healthy adults / patients / non-human / computer)
- C8: Neuroscientific technique
- C9: Dependent measure / analysis type (incl. connectivity, complexity, PHI, cardiac tags)
- C10: Temporal findings (component / time window)
- C11: Spatial findings (AAL3 label / lobe / stream)
- C12: Frequency findings (delta–gamma bands)
