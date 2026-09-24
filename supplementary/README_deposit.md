# Supplementary deposit v2 — brainsci-4583950 (revision 1, 24 September 2026)

Manuscript: *What theories of consciousness commit to, and what they leave unmeasured: an audit of stated predictions after the first adversarial test* (Brain Sciences, MDPI, under review).

Reproduce every count: `python reproduce.py --deposit . --out out` (11 steps; see README_code.md).

| File | Contents |
|---|---|
| pair_register.csv | Every cross-theory pair of stated predictions in every column with two or more (63 pairs: M8 54, M3 3, M7 3, M6 1, M4a 1, M4c 1): shared condition, shared observable, relation (different / jointly compatible / discriminating / incompatible), favouring results, pair confidence, coder. The manuscript's column class is derived from this file by column_typology_pairs.py (output: column_typology_pairs.csv). column_typology.py and column_typology_v2_legacy_rule.csv keep the earlier distinguishable_from rule as a diagnostic. |
| Table_S2_v2_publications.csv | Table S2 at publication level (32 publications; class, theory-addressed, contested), the second unit at which Table 2 is reported. |
| reading_results_20260924.csv, reading_log_20260924.md | Full-text pass over eight flagged S1 cells: sources reached, quotes, proposed codes. |
| Table_S1_v2.csv | Table S1 — 120 cells: 12 accounts (`accounts_manifest.csv`; HOT and HOSS separate; 10 trial-level, 2 origin-level) × 10 domains (`domains_manifest.csv`; M4 split into M4a/M4b/M4c). One row per cell; `prediction_id` lists Table S4 rows. Codes EXPLICIT / INTERPRETED / NOT_LOCATED / NOT_APPLICABLE / UNRESOLVED with `polarity`; `provisional`, `flag_for_adjudication`, `evidence_status`, `legacy_code`, `origin` (submitted-v1 / added-in-revision). |
| Table_S1_v2_long.csv | Same, plus the superseded legacy M4 rows (`superseded_by`). |
| Table_S1_round0_72cells.csv, Table_S1_v13_88cells.csv | Earlier versions kept for provenance. |
| Table_S4_v2.csv | Prediction register: 34 entries — 27 stated by proponents, 1 kept for provenance after re-coding to INTERPRETED (P27), 6 derived by the authors (P23, P24, P25, P32, P33, P34) — with source, locus, condition, outcome, expected result, `published_author_statement`, `explicit_endorsement_of_this_test`. |
| column_typology_v2.csv, column_typology_v2_notes.md | Derived column classes (output of `column_typology.py`; never coded). |
| Table_1_wide_v2.csv, Table_1_tallies_v2.csv | Tallies behind Table 1 (`recompute_table1.py`). |
| Table_S2_v2_experiments.csv | Table S2 — 32 publications in 42 experiment-level rows with `unit_type` (22 experiment, 2 experiment-group, 18 publication-as-one), raw fields `modality`, `affective_status`, `effector_type`, derived `content_class_v2`, three attribution columns, contested flags, evidence status. The publication is the primary unit of Table 2; the experiment-row counts are reported beside it. |
| paradigm_sources.csv | 4 paradigm-defining papers (protocol, taxonomy, review, theory) — bibliographic list, outside every denominator. |
| S2_inclusion_criteria_v2.txt, s2_sensitivity.csv | Criteria; 11 sensitivity scenarios + 2 historical publication-level reproductions. |
| Table_S3_contrast_dimensions.csv, Table_S3_tallies.csv, s3_coverage_note.md | Coding of 10 accounts against 12 ConTraSt annotation dimensions (120 cells). Covers the ten accounts of deposit v1.3 minus the neural subjective frame and before the HOT/HOSS split — see the coverage note; not the same account set as Table S1. |
| codebook_v2.md, codebook_v2.sha256, codebook_changelog.md | Frozen codebook v2.0. |
| Supplementary_Protocol_S5.md, protocol_numbers.py, protocol_changes.md | Protocol S5 v2; the script that derives its planning numbers from the section9_power.py outputs; the audit-to-change mapping. |
| power_study1.csv, power_study2.csv, trials_budget.csv, section9_power_summary.md | Power and trial budget (`section9_power.py`). |
| agreement.py | Inter-coder agreement (S1 v2 and S2 v2 forms auto-detected; raw agreement, confusion matrix, nominal κ, per-domain κ, κ by origin subset; intervals opt-in). |
| recompute_table1.py, column_typology.py, section9_power.py, reproduce.py, expected_hashes.json, README_code.md | Scripts. |
| source_verification_v4.md / .csv | Source-by-source verification with evidence status (full text / abstract only / not resolvable). |

Coding status at deposit: first coding complete and provisional (50 cells added in revision, 16 flagged for adjudication, 57 cells coded from abstracts, 5 cells re-coded on 24 September 2026 with the previous code kept); blind second coding by the second author not yet begun — κ will be added in v2.1. Codebook v2.3 frozen (hash in codebook_v2.sha256). DOIs resolved against CrossRef on 24 September 2026. Licence: data CC BY 4.0, code MIT.
