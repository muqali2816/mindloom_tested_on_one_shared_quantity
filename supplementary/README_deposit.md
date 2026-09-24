# Supplementary deposit v2 — brainsci-4583950 (revision 1, 24 September 2026)

Manuscript: *What theories of consciousness commit to, and what they leave unmeasured: an audit of stated predictions after the first adversarial test* (Brain Sciences, MDPI, under review).

Reproduce every count: `python reproduce.py --deposit . --out out --skip-mixed` (6 steps; `--update-hashes` only when tables change).

| File | Contents |
|---|---|
| Table_S1_v2.csv | Table S1 — 120 cells: 12 accounts (`accounts_manifest.csv`; HOT and HOSS separate; 10 trial-level, 2 origin-level) × 10 domains (`domains_manifest.csv`; M4 split into M4a/M4b/M4c). One row per cell; `prediction_id` lists Table S4 rows. Codes EXPLICIT / INTERPRETED / NOT_LOCATED / NOT_APPLICABLE / UNRESOLVED with `polarity`; `provisional`, `flag_for_adjudication`, `evidence_status`, `legacy_code`, `origin` (submitted-v1 / added-in-revision). |
| Table_S1_v2_long.csv | Same, plus the superseded legacy M4 rows (`superseded_by`). |
| Table_S1_round0_72cells.csv, Table_S1_v13_88cells.csv | Earlier versions kept for provenance. |
| Table_S4_v2.csv | Prediction register: 31 predictions (28 stated, 3 derived by the authors: P23, P24, P25), each with source, locus, `distinguishable_from`, `distinguishability_confidence`. |
| column_typology_v2.csv, column_typology_v2_notes.md | Derived column classes (output of `column_typology.py`; never coded). |
| Table_1_wide_v2.csv, Table_1_tallies_v2.csv | Tallies behind Table 1 (`recompute_table1.py`). |
| Table_S2_v2_experiments.csv | Table S2 — 42 empirical experiments from 32 publications; identifiers publication / study family / experiment / sample; attribution split by-authors / later / coder; `theory_addressed` derived by script. |
| paradigm_sources.csv | 4 paradigm-defining papers (protocol, taxonomy, review, theory) — bibliographic list, outside every denominator. |
| S2_inclusion_criteria_v2.txt, s2_sensitivity.csv | Criteria; 11 sensitivity scenarios + 2 historical publication-level reproductions. |
| Table_S3_contrast_dimensions.csv, Table_S3_tallies.csv, s3_coverage_note.md | Coding of 10 accounts against 12 ConTraSt annotation dimensions (120 cells). Covers the ten accounts of deposit v1.3 minus the neural subjective frame and before the HOT/HOSS split — see the coverage note; not the same account set as Table S1. |
| codebook_v2.md, codebook_v2.sha256, codebook_changelog.md | Frozen codebook v2.0. |
| Supplementary_Protocol_S5.md | Study 1 (neutral, three effectors, 0/1/3 shared pairs, count branch) and Study 2 (valence). |
| power_study1.csv, power_study2.csv, trials_budget.csv, section9_power_summary.md | Power and trial budget (`section9_power.py`). |
| agreement.py | Inter-coder agreement (S1 v2 and S2 v2 forms auto-detected; raw agreement, confusion matrix, nominal κ, per-domain κ, κ by origin subset; intervals opt-in). |
| recompute_table1.py, column_typology.py, section9_power.py, reproduce.py, expected_hashes.json, README_code.md | Scripts. |
| source_verification_v4.md / .csv | Source-by-source verification with evidence status (full text / abstract only / not resolvable). |

Coding status at deposit: first coding complete and provisional (50 cells added in revision, 15 flagged for adjudication, 58 cells coded from abstracts); blind second coding by the second author not yet begun — κ will be added in v2.1. DOIs resolved against CrossRef on 24 September 2026. Licence: data CC BY 4.0, code MIT.
