# Analysis code, supplementary deposit v2 (brainsci-4583950, revision 1)

Four scripts, numpy/pandas/scipy only (statsmodels for the optional mixed-model check). All numbers that
appear in the manuscript, Table 1, Protocol S5 and the response to reviewers are produced by these scripts
from the tables; none is typed by hand.

## Run order

```
python reproduce.py                      # everything below, PASS/FAIL per step, hash check; ~1 min
python reproduce.py --skip-mixed         # ~6 s; mixed-model convergence check omitted
```

Or step by step (from this directory):

| # | Command | What it does | Output |
|---|---|---|---|
| 1 | `python recompute_table1.py Table_S1_v2.csv --out recompute/` | Table 1 tallies from the long-format Table S1 (v2 codes EXPLICIT / INTERPRETED / NOT_LOCATED / NOT_APPLICABLE / UNRESOLVED with polarity; EXPLICIT-null apart; trial- vs origin-level apart; submitted-v1 vs added-in-revision apart; legacy-code view of the cells that carry `legacy_code`). On `Table_S1_theory_by_quantity.csv` (deposit v1.3) the legacy schema is auto-detected and reproduces `Table_1_tallies.csv` byte for byte. | `table1_tallies_v2.csv`, `table1_wide_v2.csv`, `table1_markdown_v2.md`, `table1_numbers_v2.json`, `table1_tallies_legacy_view.csv` |
| 2 | `python recompute_table1.py --selftest --out recompute_selftest/` | Synthetic 12 x 10 table with RANDOM codes (not the study's codes): schema, tallies, status logic, negative case | `recompute_selftest_log.csv` |
| 3 | `python agreement.py --selftest --out agreement_selftest/` | kappa unit checks; recovery of kappa from simulated 80 % agreement; 6 required negative cases (duplicated key, theory alias not in manifest, typo code, NaN code, mismatched row sets, DOI NaN in a positive cell) + 2 extra (domain not in manifest, positive cell without polarity) -- each must abort with a clear message; exit non-zero on any failure | `selftest_log.csv`, `selftest_log.md`, `agreement_summary.*` |
| 3b | `python agreement.py --s1a S1_coder1.csv --s1b S1_coder2.csv --accounts accounts_manifest.csv --domains domains_manifest.csv --out agreement_out/` | The real agreement run once the blind second coding is returned. Add `--code-scheme legacy` for v1.3-style files, `--ci bootstrap-by-theory` for an indicative cluster-bootstrap interval (default: no interval; see the docstring on why cells are not independent), `--extra-alias 'HOT / HOSS=HOT'` for the merged legacy row | `agreement_summary.md/.csv`, `s1_confusion_code.csv`, `s1_confusion_code_polarity.csv`, `s1_per_domain_kappa.csv`, `s1_subset_kappa.csv`, `disagreements_S1.csv` |
| 4 | `python section9_power.py --out power/ [--mixed-sims 200 \| --skip-mixed]` | Power for the new Section 9.1 design (three effectors, 0/1/3 shared pairs, count branch): C0, C1a, C1b (linear-in-shared-pairs and two-df omnibus), exact TOST with Monte Carlo check, Study 2 valence, trials budget, mixed-model convergence check | `power_study1.csv`, `power_study2.csv`, `trials_budget.csv`, `power_mixed_check.csv`, `section9_power_summary.md`, `section9_key_numbers.json` |
| 5 | (inside `reproduce.py`) | sha256 of the produced CSVs against `expected_hashes.json`. Exact files (tallies, analytic power tables, trials budget, self-test logs) must match; `power_mixed_check.csv` and the self-test `agreement_summary.csv` only warn, because optimiser tolerances differ across BLAS builds. `--update-hashes` rewrites the reference | `reproduce_log.txt`, `reproduce_report.json` |

## Input files expected in this directory

`accounts_manifest.csv` (12 accounts: theory_id, theory, row_class, origin, note), `domains_manifest.csv`
(10 domains: M1, M2, M3, M4a, M4b, M4c, M5, M6, M7, M8), and either `Table_S1_v2.csv` (schema documented at the
top of `recompute_table1.py`) or the deposit-v1.3 `Table_S1_theory_by_quantity.csv` (used automatically when
the v2 table is absent).

Coding tables are read with `keep_default_na=False`: the polarity value `null` and the code alias `NA` are
strings, not missing values. Do not open and re-save the tables with a tool that converts `null` to empty.

## Versions used for the deposited run

Python 3.11.15, numpy 2.4.6, pandas 2.3.3, scipy 1.17.1, statsmodels 0.14.6 (macOS, arm64).
Expected runtime: `reproduce.py` about 60 s (of which section9_power with 200 mixed-model simulations per
contrast about 56 s); with `--skip-mixed` about 6 s. The TOST Monte Carlo check uses 200 000 replicates
(about 1 s per bound).

## What changed from v1.3

- `agreement.py` 1.3 -> 2.0: rows matched on `(theory_id, domain_id)` through the manifests instead of free-text
  theory names; both code schemes; report order fixed (raw agreement, confusion, nominal kappa, per domain,
  origin subsets); bootstrap CI removed from the default and replaced by `--ci none|multinomial|bootstrap-by-theory`;
  negative self-test cases added; `--allow-partial` removed (a partial comparison is no longer computed).
- `recompute_table1.py` 1.3 -> 2.0: reads the long-format Table S1 directly; no dependency on the round-0 72-cell
  matrix or on `theory_predictions_matrix.csv`; v2 codes with polarity; column status is computed from the codes.
- `section9_power.py` 1.3 -> 2.0: new design; everything recomputed (the previous N = 126 / 68 / 119 / 171 / 265
  values of the 3 x 3 design are not carried forward); exact TOST replaces the approximate one; fixed N, no
  sequential monitoring; trials budget added.
- `reproduce.py`, `README_code.md`, `expected_hashes.json`: new.
