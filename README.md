# What theories of consciousness commit to, and what they leave unmeasured

Supplementary materials and analysis code for the manuscript submitted to *Brain Sciences* (MDPI), ms. brainsci-4583950 (revision 1, September 2026).

The manuscript codes theories of consciousness against eight measurable quantities (M1–M8) and asks which quantities theories share, contest, occupy alone, or leave unoccupied. Everything the argument rests on is here, cell by cell, with a justification and a DOI.

## Layout (v4, 24 September 2026)

| Path | Contents |
|---|---|
| `supplementary/Table_S1_v2.csv` | **Table S1 v2** — 120 cells: 12 accounts (HOT and HOSS separate) × 10 domains (M4 split into M4a/M4b/M4c); one row per cell; `code` ∈ {EXPLICIT, INTERPRETED, NOT_LOCATED, NOT_APPLICABLE, UNRESOLVED}, `polarity`, `relation`, `claim_text`, source label/DOI/locus, `evidence_status`, `provisional`, `flag_for_adjudication`, `legacy_code`, `origin`. `Table_S1_v2_long.csv` keeps the superseded legacy M4 rows. |
| `supplementary/Table_S1_round0_72cells.csv`, `Table_S1_v13_88cells.csv` | Earlier versions, for provenance. |
| `supplementary/Table_S4_v2.csv` | Prediction register — 31 predictions (28 stated, 3 derived), each with source locus and `distinguishable_from`. |
| `supplementary/column_typology_v2.csv` | Derived column classes (output of `scripts/column_typology.py`, never coded). |
| `supplementary/Table_S2_v2_experiments.csv`, `paradigm_sources.csv`, `S2_inclusion_criteria_v2.txt`, `s2_sensitivity.csv` | Content inventory at experiment level (42 experiments, 32 publications), paradigm papers kept apart, criteria, 11 + 2 sensitivity scenarios. |
| `supplementary/Table_S3_*` | ConTraSt-dimension coding (10 accounts) and coverage note. |
| `supplementary/codebook_v2.md` (+ `.sha256`, `codebook_changelog.md`) | **Frozen** codebook v2.0. |
| `supplementary/Supplementary_Protocol_S5.md` | Study 1 (neutral; three effectors; 0/1/3 shared pairs; count branch) and Study 2 (valence). |
| `coding/second_coder_pack/` | Blank forms (S1 120 rows, S2 42 rows), manifests, S4 reference, `agreement.py`, timing log. No first-coder answers. |
| `scripts/` | `reproduce.py` (one command, 6 steps, hash check), `recompute_table1.py`, `column_typology.py`, `agreement.py`, `section9_power.py`, builders. |
| `power_analysis/` | Power tables and trial budget for Study 1 / Study 2. |
| `manuscript/` | Revision 1 v4 (MDPI numbered references) and the highlighted PDF (reconstructed text comparison with the submitted version). |
| `review_round1/` | Reviews transcribed verbatim; response v3. |

Reproduce every count: `cd supplementary && python ../scripts/reproduce.py --deposit . --out out --skip-mixed`.

Status: first coding complete (provisional); blind second coding by the second author pending; public deposit and DOI pending — placeholders in the manuscript mark both.
