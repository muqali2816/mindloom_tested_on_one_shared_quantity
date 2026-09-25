# Inter-coder agreement

agreement.py v2.4

## 1. Raw agreement

Code: 88 of 120 cells (0.733).
Code x polarity: 85 of 120 (0.708).

## 2. Confusion matrix (rows coder 1, columns coder 2)

| code | coder2:EXPLICIT | coder2:INTERPRETED | coder2:NOT_LOCATED | coder2:NOT_APPLICABLE | coder2:UNRESOLVED |
|---|---|---|---|---|---|
| coder1:EXPLICIT | 16 | 3 | 2 | 0 | 0 |
| coder1:INTERPRETED | 7 | 13 | 9 | 0 | 0 |
| coder1:NOT_LOCATED | 0 | 8 | 58 | 1 | 1 |
| coder1:NOT_APPLICABLE | 0 | 0 | 0 | 1 | 1 |
| coder1:UNRESOLVED | 0 | 0 | 0 | 0 | 0 |

Code x polarity:

| code:polarity | coder2:EXPLICIT:positive | coder2:EXPLICIT:stated_null | coder2:EXPLICIT:negative | coder2:INTERPRETED:positive | coder2:INTERPRETED:stated_null | coder2:INTERPRETED:negative | coder2:NOT_LOCATED | coder2:NOT_APPLICABLE | coder2:UNRESOLVED |
|---|---|---|---|---|---|---|---|---|---|
| coder1:EXPLICIT:positive | 14 | 0 | 0 | 3 | 0 | 0 | 2 | 0 | 0 |
| coder1:EXPLICIT:stated_null | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| coder1:EXPLICIT:negative | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| coder1:INTERPRETED:positive | 3 | 1 | 0 | 10 | 0 | 0 | 8 | 0 | 0 |
| coder1:INTERPRETED:stated_null | 3 | 0 | 0 | 3 | 0 | 0 | 1 | 0 | 0 |
| coder1:INTERPRETED:negative | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| coder1:NOT_LOCATED | 0 | 0 | 0 | 8 | 0 | 0 | 58 | 1 | 1 |
| coder1:NOT_APPLICABLE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| coder1:UNRESOLVED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## 3. Nominal Cohen's kappa

kappa (code) = 0.550 (p_e = 0.408; Landis-Koch band: moderate).
Interval: cluster bootstrap over 12 theories, 2000 replicates, percentile 95 % (indicative; few clusters).
95 % interval: 0.439 to 0.661.

## 4. Kappa per domain and per theory

| unit | level | n | raw_agreement | raw_proportion | kappa_nominal | pe |
|---|---|---|---|---|---|---|
| domain | M1 | 12 | 11 of 12 | 0.917 | 0.714 | 0.708 |
| domain | M2 | 12 | 10 of 12 | 0.833 | 0.529 | 0.646 |
| domain | M3 | 12 | 8 of 12 | 0.667 | 0.520 | 0.306 |
| domain | M4a | 12 | 6 of 12 | 0.500 | 0.273 | 0.313 |
| domain | M4b | 12 | 10 of 12 | 0.833 | 0.600 | 0.583 |
| domain | M4c | 12 | 10 of 12 | 0.833 | 0.600 | 0.583 |
| domain | M5 | 12 | 9 of 12 | 0.750 | 0.438 | 0.556 |
| domain | M6 | 12 | 7 of 12 | 0.583 | 0.178 | 0.493 |
| domain | M7 | 12 | 8 of 12 | 0.667 | 0.415 | 0.431 |
| domain | M8 | 12 | 9 of 12 | 0.750 | 0.581 | 0.403 |
| theory | AST | 10 | 7 of 10 | 0.700 | 0.412 | 0.490 |
| theory | FM | 10 | 6 of 10 | 0.600 | 0.355 | 0.380 |
| theory | GNWT | 10 | 6 of 10 | 0.600 | 0.259 | 0.460 |
| theory | HOSS | 10 | 6 of 10 | 0.600 | 0.355 | 0.380 |
| theory | HOT | 10 | 6 of 10 | 0.600 | 0.333 | 0.400 |
| theory | IIT | 10 | 9 of 10 | 0.900 | 0.750 | 0.600 |
| theory | NSF | 10 | 7 of 10 | 0.700 | 0.552 | 0.330 |
| theory | PFT | 10 | 7 of 10 | 0.700 | 0.589 | 0.270 |
| theory | PP | 10 | 7 of 10 | 0.700 | 0.565 | 0.310 |
| theory | RPT | 10 | 10 of 10 | 1.000 | 1.000 | 0.820 |
| theory | SIT | 10 | 8 of 10 | 0.800 | 0.697 | 0.340 |
| theory | UAL | 10 | 9 of 10 | 0.900 | 0.815 | 0.460 |

## 5. Kappa by origin subset (file column)

| subset | n | raw_agreement | raw_proportion | kappa_nominal | pe |
|---|---|---|---|---|---|
| submitted-v1 | 70 | 52 of 70 | 0.743 | 0.563 | 0.411 |
| added-in-revision | 50 | 36 of 50 | 0.720 | 0.529 | 0.405 |

## All statistics

| statistic | value |
|---|---|
| S1_version | 2.4 |
| S1_code_scheme | v2 |
| S1_n_cells_compared | 120 |
| S1_n_theories | 12 |
| S1_n_domains | 10 |
| S1_n_manifest_grid_cells | 120 |
| S1_1_raw_agreement_code_k_of_n | 88 of 120 |
| S1_1_raw_agreement_code_proportion | 0.733 |
| S1_1_raw_agreement_code_polarity_k_of_n | 85 of 120 |
| S1_1_raw_agreement_code_polarity_proportion | 0.708 |
| S1_3_kappa_nominal_code | 0.550 |
| S1_3_kappa_nominal_code_pe | 0.408 |
| S1_3_kappa_nominal_code_band | moderate |
| S1_3_kappa_nominal_code_polarity | 0.522 |
| S1_3_kappa_binary_located_vs_not | 0.668 |
| S1_3_kappa_binary_located_vs_not_n_cells | 118 |
| S1_3_n_EXPLICIT_null_coder1 | 2 |
| S1_3_n_EXPLICIT_null_coder2 | 3 |
| S1_3_n_UNRESOLVED_either_coder | 2 |
| S1_3_n_UNRESOLVED_coder1 | 0 |
| S1_3_n_UNRESOLVED_coder2 | 2 |
| S1_3_kappa_ci_method | cluster bootstrap over 12 theories, 2000 replicates, percentile 95 % (indicative; few clusters) |
| S1_3_kappa_ci95_low | 0.439 |
| S1_3_kappa_ci95_high | 0.661 |
| S1_5_origin_source | file column |
| S1_5_kappa_nominal_submitted-v1 | 0.563 |
| S1_5_raw_agreement_submitted-v1 | 52 of 70 |
| S1_5_kappa_nominal_added-in-revision | 0.529 |
| S1_5_raw_agreement_added-in-revision | 36 of 50 |
| S1_n_disagreements | 35 |

## S1 disagreements for adjudication (n = 35; severity 2 = stated prediction vs not located / not applicable)

| theory_id | domain_id | origin_cell | code_coder1 | polarity_coder1 | code_coder2 | polarity_coder2 | severity |
|---|---|---|---|---|---|---|---|
| HOT | M7 | submitted-v1 | EXPLICIT | positive | NOT_LOCATED |  | 2 |
| PP | M7 | submitted-v1 | EXPLICIT | positive | NOT_LOCATED |  | 2 |
| PFT | M1 | added-in-revision | INTERPRETED | stated_null | INTERPRETED | positive | 1 |
| SIT | M1 | submitted-v1 | EXPLICIT | positive | INTERPRETED | positive | 1 |
| GNWT | M2 | submitted-v1 | NOT_LOCATED |  | INTERPRETED | positive | 1 |
| PFT | M2 | added-in-revision | INTERPRETED | stated_null | EXPLICIT | positive | 1 |
| AST | M3 | submitted-v1 | NOT_LOCATED |  | INTERPRETED | positive | 1 |
| GNWT | M3 | submitted-v1 | INTERPRETED | stated_null | NOT_LOCATED |  | 1 |
| HOT | M3 | submitted-v1 | INTERPRETED | stated_null | EXPLICIT | positive | 1 |
| IIT | M3 | submitted-v1 | NOT_LOCATED |  | UNRESOLVED |  | 1 |
| PFT | M3 | added-in-revision | INTERPRETED | stated_null | INTERPRETED | positive | 1 |
| SIT | M3 | submitted-v1 | INTERPRETED | stated_null | INTERPRETED | positive | 1 |
| AST | M4a | added-in-revision | NOT_LOCATED |  | INTERPRETED | positive | 1 |
| GNWT | M4a | added-in-revision | NOT_LOCATED |  | INTERPRETED | positive | 1 |
| HOSS | M4a | added-in-revision | NOT_LOCATED |  | INTERPRETED | positive | 1 |
| NSF | M4a | added-in-revision | INTERPRETED | stated_null | EXPLICIT | positive | 1 |
| PFT | M4a | added-in-revision | INTERPRETED | positive | EXPLICIT | positive | 1 |
| SIT | M4a | added-in-revision | INTERPRETED | positive | EXPLICIT | positive | 1 |
| HOSS | M4b | added-in-revision | NOT_LOCATED |  | INTERPRETED | positive | 1 |
| HOT | M4b | added-in-revision | NOT_LOCATED |  | INTERPRETED | positive | 1 |
| HOT | M4c | added-in-revision | INTERPRETED | positive | NOT_LOCATED |  | 1 |
| PP | M4c | added-in-revision | INTERPRETED | positive | NOT_LOCATED |  | 1 |
| FM | M5 | submitted-v1 | INTERPRETED | positive | NOT_LOCATED |  | 1 |
| GNWT | M5 | submitted-v1 | INTERPRETED | positive | NOT_LOCATED |  | 1 |
| UAL | M5 | submitted-v1 | INTERPRETED | positive | NOT_LOCATED |  | 1 |
| AST | M6 | submitted-v1 | INTERPRETED | positive | NOT_LOCATED |  | 1 |
| FM | M6 | submitted-v1 | NOT_LOCATED |  | INTERPRETED | positive | 1 |
| HOSS | M6 | submitted-v1 | EXPLICIT | positive | INTERPRETED | positive | 1 |
| NSF | M6 | added-in-revision | INTERPRETED | positive | NOT_LOCATED |  | 1 |
| PP | M6 | submitted-v1 | INTERPRETED | positive | NOT_LOCATED |  | 1 |
| FM | M7 | submitted-v1 | NOT_LOCATED |  | NOT_APPLICABLE |  | 1 |
| HOSS | M7 | submitted-v1 | EXPLICIT | positive | INTERPRETED | positive | 1 |
| FM | M8 | submitted-v1 | INTERPRETED | positive | EXPLICIT | stated_null | 1 |
| NSF | M8 | added-in-revision | INTERPRETED | positive | EXPLICIT | positive | 1 |
| PFT | M8 | added-in-revision | NOT_APPLICABLE |  | UNRESOLVED |  | 1 |

Kappa is Cohen's kappa from the coder-by-coder cross-tabulation (unweighted). Undefined (NaN) kappa means both coders used a single category in that block, so chance agreement is 1 and kappa has no value; raw agreement is still reported. No interval is attached unless --ci was given: cells within a theory are coded from the same sources and are not independent, so the multinomial SE and a cell-level bootstrap are both optimistic.
