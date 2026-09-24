# Blind second-coding pack — brainsci-4583950 (Table S1 and Table S2)

For the second author. Do not open `S1_coder1_revised.csv` until your own coding is complete — it holds the first author's codes and is included only so the agreement script can be run afterwards.

1. Read `codebook_second_coder.md` (definitions of M1–M8, the four codes, the theory-addressed rule, the content categories, primary sources per theory).
2. Fill `S1_blank_for_coder2.csv` — 88 cells (11 theory rows × 8 quantities). One code per cell from YES / IMPLICIT / NO / YES (negative); one sentence of justification; one source label and DOI.
3. Fill `S2_blank_for_coder2.csv` — 36 studies: `content` category and `theory_addressed`.
4. Record start/end times in `coder2_timing_log.csv`.
5. Then run: `python agreement.py --s1a S1_coder1_revised.csv --s1b S1_blank_for_coder2.csv --s2a S2_coder1.csv --s2b S2_blank_for_coder2.csv --out agreement_out/`
   (S2_coder1.csv = the deposited Table S2). The script writes κ, percentage agreement, per-column κ and a disagreement list for adjudication.
6. The manuscript placeholder in §7.2 (κ, agreement of 88 cells, number of disagreements, S2 κ) is filled from `agreement_out/agreement_summary.md`. Report the *pre-adjudication* values.

Theory labels must match the coder-1 file exactly (they already do in the blank form).
