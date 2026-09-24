# Analysis code, supplementary deposit v2 (brainsci-4583950, revision 1)

Nine scripts, numpy/pandas/scipy (statsmodels for the mixed-model check, which `reproduce.py` requires unless `--skip-mixed` is passed — then it says so in its output and does not report PASS for the check). Every number that appears in the manuscript, Tables 1 and 2, Protocol S5 and the response to reviewers is produced by these scripts from the deposited tables; none is typed by hand. Polarity of a stated null is spelled `stated_null` (pandas reads a bare `null` as missing).

## Run order

```
python reproduce.py --deposit . --out out                 # 11 steps, PASS/FAIL per step, hash check; about 1 min with the 200-simulation mixed check
python reproduce.py --deposit . --out out --skip-mixed    # about 9 s; the mixed-model check is skipped and announced as skipped
python reproduce.py ... --update-hashes                   # only when a table has changed: rewrites expected_hashes.json
```

## Steps (as `reproduce.py` runs them)

| Step | Script | What it does | Hashed output |
|---|---|---|---|
| 1 | `recompute_table1.py Table_S1_v2.csv` | Table 1 tallies from the cell-level Table S1 (12 accounts × 10 domains); EXPLICIT stated nulls apart; trial- vs origin-level apart; legacy-code view. The `occupancy_summary` field is a polarity summary, not the column class. | `recompute/table1_tallies_v2.csv`, `table1_wide_v2.csv`, `table1_tallies_legacy_view.csv` |
| 1b | `column_typology.py` | **Legacy rule (diagnostic only):** classes from the `distinguishable_from` field of Table S4. Kept so the change of rule is reproducible; NOT the manuscript's class. | `typology/column_typology_v2.csv` |
| 1c | `build_table2.py Table_S2_v2_experiments.csv` | Table 2 at publication level (primary) and experiment-row level; derives `content_class_v2` from the raw fields `modality`, `affective_status`, `effector_type` and aborts if a stored class disagrees; unit-type composition of each denominator. | `table2/Table_2_counts.csv` |
| 1d | `s2_sensitivity.py` | Every attribution scenario of §7.6 at both units, plus the two historical (legacy-code) scenarios. | `s2/s2_sensitivity.csv` |
| 1e | (internal) | Recomputes the Table S3 tallies from `Table_S3_contrast_dimensions.csv` (10 accounts × 12 ConTraSt dimensions). | — |
| 1f | `column_typology_pairs.py Table_S1_v2.csv Table_S4_v2.csv pair_register.csv` | **The manuscript's column class.** Required pairs are derived from Table S4 (every cross-theory pair of stated predictions in every column with ≥ 2); a column with any pair missing from the register is 'pair assessment incomplete', never occupied-not-contested; contested requires a `discriminating` or `incompatible` pair. | `typology/column_typology_pairs.csv` |
| 2 | `recompute_table1.py --selftest` | Synthetic table with random codes: schema, tallies, negative cases (duplicate key aborts; legacy v1.3 file gives 88 cells). | `recompute_selftest/recompute_selftest_log.csv` |
| 3 | `agreement.py --selftest` | 24 cases: raw agreement, confusion matrices, nominal κ (code; code × polarity), per-domain κ, κ by origin subset; rejects duplicates, incomplete grids, unknown vocabularies; parses attribution structurally ('none named (...)' is not an attribution); S2 v2 path compares raw fields, by-authors and later attribution separately. | `agreement_selftest/agreement_summary.csv` (κ mean only; stochastic) |
| 4 | `section9_power.py` | Power for Study 1 and Study 2 (paired t, TOST, omnibus), N fixed by the rotation rule (120), the **per-session trial budget** (session 1: 64 per cell, PAS on every trial; session 2: 104 per cell = 26 probe + 78 no-probe), and the mixed-model check (200 simulations per contrast). | `power/power_study1.csv`, `power_study2.csv`, `trials_budget.csv`; `power_mixed_check.csv` is checked for content (n_sims, power) rather than hashed |
| 4b | `protocol_numbers.py --power-dir power/` | Every remaining planning number of Protocol S5 from the step-4 outputs: session arithmetic, Bonferroni/Holm, the success-rule powers under independence (rule A per contrast; rules B and C reported, not used), Study 2 power at N = 120, retention probabilities under independent loss. | `power/protocol_numbers.json` |
| 5 | (internal) | SHA-256 of every hashed output against `expected_hashes.json`. | — |

`build_pair_register.py` is the script that produced the first version of `pair_register.csv` from Table S4 text (55 pairs, M8 and M6); the eight pairs in M3, M7, M4a and M4c were added by hand by the first coder on 24 September 2026 and are marked so in the `coder` column. All pair relations are single-coder judgements from S4 text until the second coding.

## Second coding

`agreement.py --s1a <coder1.csv> --s1b <coder2.csv> --accounts accounts_manifest.csv --domains domains_manifest.csv --code-scheme v2 --out agreement_out/` (Table S1); `--s2a/--s2b` for Table S2 v2 (auto-detected by `experiment_id`). Reports raw agreement → confusion matrix → nominal κ; intervals only with `--ci`. κ for the `submitted-v1` and `added-in-revision` subsets is reported separately because blindness differs between them.
