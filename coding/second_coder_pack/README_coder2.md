# Blind second-coding pack — brainsci-4583950 (Tables S1, S2 and, optionally, S3)

For the second author. This pack contains **no first-coder codes or justifications**. Agreement is computed by the first author after your forms are returned; you receive the first-coder file only then, for the adjudication meeting.

Before you start, one honest caveat that the manuscript states in §7.2: you have read the submitted version, including its condensed Table 1, so blindness is complete for the justifications, for the sixteen cells added in revision (passive frame theory; neural subjective frame) and for Table S3, and partial for the seventy-two original cells. Code from the sources, not from memory of that table.

1. Read `codebook_second_coder.md` (definitions of M1–M8, the four codes, the theory-addressed rule, the content categories, primary sources per theory; §7 for the S3 dimensions).
2. Fill `S1_blank_for_coder2.csv` — 88 cells (11 theory blocks × 8 quantities). One code per cell from YES / IMPLICIT / NO / YES (negative); one sentence of justification; one source label and DOI.
3. Fill `S2_blank_for_coder2.csv` — 36 rows: `content` category and `theory_addressed`.
4. Optional, if time allows before final submission: fill `S3_blank_for_coder2.csv` — 120 cells (10 theory blocks × 12 ConTraSt dimensions).
5. Record start/end times per block in `coder2_timing_log.csv`.
6. Return the CSV files. The first author runs `agreement.py` (unweighted and linearly weighted κ, per-column and per-theory κ, disagreement list); the pre-adjudication values fill the placeholder in §7.2, and disagreements are adjudicated jointly with a deposited record.

Theory labels in the blank forms match the deposited tables exactly; do not edit them.


Agreement is also reported for two subsets: `cell_origin = submitted-v1` (72 cells whose condensed codes were visible in the submitted Table 1) and `added-in-revision` (16 cells: passive frame theory, neural subjective frame). The blank form carries the `cell_origin` column; leave it as is.
