# Supplementary Note S6 — the independent column set and the Table 2 sensitivity scenarios

Manuscript brainsci-4583950, revision 1. This note carries the material moved out of Sections 7.5 and 7.6 of the body to keep each statement in one place; every number here is produced by the deposited scripts (`reproduce.py` steps 1d and 1e).

## S6.1 The ConTraSt column set (Section 7.5)

The sensitivity check of the submitted version — dropping M1, M2 and M5 and confirming that M8 still dominates — was not a check against an independently generated column set. The first such check uses the dimensional scheme of the ConTraSt database [78] and codes the theory rows against its twelve dimensions (Table S3; 120 cells). The S3 coding predates the present scheme: ten rows rather than twelve, higher-order thought and state space theories still merged, the neural subjective frame absent, and the earlier four codes, mapped as in Section 7.2 (YES → EXPLICIT, YES (negative) → EXPLICIT null, IMPLICIT → INTERPRETED, NO → NOT_LOCATED); the two missing rows are named as a repair in Section 7.7.

**Occupancy by dimension.** Seven of the twelve dimensions — experimental paradigm, measure type, task type, spatial findings, dependent measure, stimulus, and report versus no-report — carry stated predictions from at least four of the eight neuroscientific rows. The sparse dimensions are the electrophysiological result fields: frequency findings receive one stated prediction (GNWT) and temporal findings three (GNWT, IIT, recurrent processing theory). Per row: GNWT 11 of 12, IIT 10, recurrent processing theory 7, passive frame theory none (it declines the implementation level). Tallies: `Table_S3_tallies.csv`; the recomputation from the 120 cells is step 1e of `reproduce.py`.

**Correspondence to M1–M8.** No ConTraSt field counts concurrent response options, records conflict magnitude, or records cortical–autonomic coherence (the components of the last exist separately as cortical connectivity and cardiac tags). M7 and M8 are directly represented; M3, M4a–M4c and M6 are partly recoverable through free-text labels. The check covered every field name and value in the live schema.

**What the check does not establish, and its limits.** It does not show that the quantities are absent from experiments, since ConTraSt records what authors reported; it cannot say whether M5 is thin because the quantity is hard to measure or because theories find it uninteresting, nor whether M1 and M2 are the right variables; and it checks occupancy, not disagreement, since only its temporal and spatial dimensions record the value of a prediction rather than its presence. The scheme was reconstructed from the database's methods description and live schema because the published extraction sheet was inaccessible; several GNWT and IIT cells rest on the Cogitate preregistration rather than foundational texts; the YES code admits explicit invariance claims and inflates three dimensions (under a strictly differential reading GNWT falls to 9 stated predictions, IIT to 8; the invariance-based cells are flagged in `Table_S3_contrast_dimensions.csv`); and the coding is by one coder, with a blank form (`S3_blank_for_coder2.csv`) in the second-coder package. See also `s3_coverage_note.md` in the deposit.

## S6.2 Table 2 sensitivity scenarios (Section 7.6)

All scenarios are computed by `s2_sensitivity.py` from `Table_S2_v2_experiments.csv` and written to `s2_sensitivity.csv` (step 1d of `reproduce.py`); publication level first, experiment-row value in brackets. Baseline S0 (theory-addressed, content-bearing, suppressed-access study excluded): 21 publications (30 rows) — neutral visual 15 of 21 (18 of 30), competing motor policies 4 of 21 (8 of 30: 7 skeletal, 1 autonomic-effector), neutral non-visual 1 of 21 (3 of 30), valenced 0 of 21 (0 of 30), interoceptive 1 of 21 (1 of 30).

| Scenario | Neutral visual | Valenced | Interoceptive |
|---|---|---|---|
| S1 add the suppressed-access study [131] | 15 of 22 (18 of 31) | 1 of 22 (1 of 31) | 1 of 22 (1 of 31) |
| S2 remove the metacognition studies | 11 of 16 (14 of 25) | 0 of 16 (0 of 25) | 0 of 16 (0 of 25) |
| S3 remove every contested row | 11 of 16 (14 of 25) | 0 of 16 (0 of 25) | 0 of 16 (0 of 25) |
| S5 add the coder's inferred attributions | 18 of 25 (22 of 35) | 0 of 25 (0 of 35) | 1 of 25 (1 of 35) |
| S6 strict later attribution only (citing sentence read and names the theory) | 10 of 15 (13 of 24) | 0 of 15 (0 of 24) | 0 of 15 (0 of 24) |
| S8 no theory filter | 18 of 29 (22 of 39) | 3 of 29 (3 of 39) | 2 of 29 (2 of 39) |
| S10 strict attribution and every contested row removed | 7 of 12 (10 of 21) | 0 of 12 (0 of 21) | 0 of 12 (0 of 21) |

Seven rows carry a contested-inclusion flag with a written reason (`contested_reason`). The submitted version's publication-level counts (21 of 27 with the four paradigm-defining rows inside the denominator; 19 of 24 without) are reproduced by the script as the historical scenarios H0 and H1 from the legacy codes, so that the difference between versions is attributable to the change of attribution rule and content classes rather than to re-coding. The two scenarios reported in the body are the ones in which a headline value changes: S1 (the valenced zero does not survive) and S10 (the smallest neutral-visual share).
