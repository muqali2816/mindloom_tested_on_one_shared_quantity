# FACTS SHEET v4 — every number below is produced by script from the tables in this bundle (reproduce.py, 6 of 6 PASS). Cite by name; do not retype from memory.

## Table S1 v2 (Table_S1_v2.csv; 120 cells = 12 accounts × 10 domains; HOT and HOSS separate; M4 → M4a/M4b/M4c)
Codes: EXPLICIT 22 (20 positive, 2 stated_null), INTERPRETED 32 (25 positive, 7 stated_null), NOT_LOCATED 64, NOT_APPLICABLE 2 (PFT × M8, UAL × M8), UNRESOLVED 0.
Provisional cells 50 (all M4a/b/c and all HOT/HOSS split cells); flagged for adjudication 15 (first: PP × M4c). Evidence: 62 cells full-text, 58 abstract-only (28 of the 54 positive cells rest on abstracts).
Legacy: 96 cells carry v1.3 codes (48 NO, 26 IMPLICIT, 20 YES, 2 YES (negative)) — mapped, never recoded.

## Derived column typology (column_typology_v2.csv — output of column_typology.py from S1 + S4; NOT an input)
| domain | EXPLICIT pos | EXPLICIT null | INTERPRETED | NOT_LOCATED | distinguishable pairs (conf≥2) | derived class (conf≥2) | manuscript v3 said |
| M1 | 1 | 0 | 1 | 10 | 0 (0) | single-occupant (single-occupant) | single-occupant |
| M2 | 1 | 0 | 2 | 9 | 0 (0) | single-occupant (single-occupant) | single-occupant |
| M3 | 3 | 0 | 5 | 4 | 0 (0) | occupied-not-contested (occupied-not-contested) | occupied-not-contested |
| M5 | 0 | 0 | 5 | 7 | 0 (0) | thin (thin) | thin |
| M6 | 2 | 0 | 3 | 7 | 1 (0) | contested (occupied-not-contested) | occupied-not-contested |
| M7 | 3 | 0 | 2 | 7 | 0 (0) | occupied-not-contested (occupied-not-contested) | occupied-not-contested |
| M8 | 6 | 0 | 4 | 0 | 15 (14) | contested (contested) | shared (occupied, not contested) |
| M4a | 2 | 0 | 6 | 4 | 0 (0) | occupied-not-contested (occupied-not-contested) | contested |
| M4b | 2 | 0 | 0 | 10 | 0 (0) | occupied-not-contested (occupied-not-contested) | contested |
| M4c | 0 | 2 | 4 | 6 | 0 (0) | occupied-not-contested (occupied-not-contested) | contested |
Reading: M8 is contested — 6 EXPLICIT accounts, 15 distinguishable pairs among stated predictions (14 at confidence ≥ 2; single-coder judgements) (locus / timing / connectivity; Cogitate GNWT vs IIT P01–P06, plus RPT P08, HOT P09, AST P12, HOSS P29). M4a, M4b, M4c are occupied-not-contested: the SIT/PFT null on M4c and the PP/NSF positives on M4a/M4b answer different questions; no stated conflict. M6 is contested at confidence 1 only (IIT P07 vs HOSS P10 — whether both address the same variable is open); at confidence ≥2 it is occupied-not-contested. M1, M2 single-occupant (SIT). M5 thin (0 EXPLICIT, 5 INTERPRETED). Trial-level only: M3 has 1 EXPLICIT (PP); FM and UAL are origin-level.

## Table S4 v2 (Table_S4_v2.csv): 31 predictions — 28 stated, 3 derived (P23 SIT→M2 extension by the authors, not endorsed; P24 PP→M4c feeling in autonomic conflict, pending proponents; P25 GNWT + capacity). P16 (SIT × M1) is a threshold at ≥2 inclinations, stated; no statement about a further increase. P17 (SIT × M2) stated and measured. Cogitate is the source only for GNWT/IIT rows.

## Table S2 v2 (Table_S2_v2.csv; 42 experiments from 32 publications; 4 paradigm-defining papers moved to paradigm_sources.csv and out of every denominator)
Baseline S0 (experiments; theory_addressed by the study's authors or a later theory paper; Whalen 1998 excluded as access-suppressed; metacognition rows included; Farb 2013 included but contested): n = 30 from 21 publications — neutral-visual 18 of 30, neutral-nonvisual 3 of 30, motor-conflict 8 of 30 (7 skeletal + 1 autonomic-effector: Morsella 2009 control, re-coded from interoceptive on 24 Sep), valenced 0 of 30, interoceptive 1 of 30 (Garfinkel, contested; 0 in strict scenarios).
Sensitivity (s2_sensitivity.csv): + Whalen → valenced 1 of 31; − metacognition rows → 14 of 25 neutral-visual; strict later attribution → 13 of 24; strict − all contested → 10 of 21 (the smallest neutral-visual share); + coder-inferred attribution → 22 of 35; no theory filter → 22 of 39 neutral-visual, valenced 3 of 39, interoceptive 2 of 39. Historical publication-level scenarios reproduce: 21 of 27 (with paradigm rows), 19 of 24 (without). Contested-inclusion rows 7. Evidence: 19 of 32 publications abstract-only — experiment partition and participant counts provisional for those.
The claim 'no theory claims this literature' must not be made; the defensible statement is about the checked sample under the stated attribution rule.

## §9.1 power (section9_power_summary.md; power_study1.csv, power_study2.csv, trials_budget.csv)
Study 1 (neutral): three responses on three effectors, all co-executable; incompatibility = shared-effector pairs 0 / 1 / 3 at count 3; count branch 1 / 2 / 3 at 0 shared pairs; 11 presentation cells, 5 analysis cells. C0 (threshold 1 vs ≥2, P16) and C1a (0 vs shared pairs, P23): N = 119 is required for 90 % power at dz = 0.30; fixed N = 120 (multiple of six rotations), power 0.903 (dz 0.20 → 265; dz 0.40 → 68). TOST equivalence bound ±0.30 dz: power 0.895 analytic, 0.896 Monte Carlo at N = 120 (N = 122 for 0.90). C1b two-df omnibus: 0.84 at N = 120 (N = 144 for 0.90). Trials: 102 presented per cell → ≈65 usable (25 % probe trials, 15 % loss), 561 presented per session over 11 cells; two sessions. Mixed-model check (200 sims) 0.93 / 0.92, 0 non-converged. No sequential monitoring. Autonomic recording (ECG, EDA, pupil) in Study 1; the cortical–autonomic coupling index is ESTIMATION only, not a test of M5; the EEG-only frozen index is a candidate marker of access, not a measure of M5.
Study 2 (valence, Supplementary Protocol S5 only): main effect negative − positive at matched arousal dz = 0.30 → N = 119; incompatibility × valence interaction at dz = 0.20 would need N = 265 (power 0.58 at N = 119) → estimation only.
Old design (3 rules, 1/2/3 keys, N = 126, BF monitoring) is replaced because number of distinct responses covaried with incompatibility.

## Source verification (source_verification_v4.md; 11 full-text, 7 abstract-only, 3 accepted from prior check)
- Ruby et al. 2018 critique AND Bor et al. 2018 reply both read: the Rounis TMS dispute is open — cite both, decide nothing.
- Hall et al. 2012 measured immediate detection/justification only: 'durably' is unsupported → remove.
- Morsella et al. 2016 BBS §2.4: smooth-muscle/autonomic conflict is excluded from the function of the conscious field and the authors decline to extend PFT to the ANS; the text does NOT deny bodily feelings (tooth pain, urges are named as contents). Wording for the null: 'exclusion from the field's function, not a denial of bodily feelings'.
- Cogitate: three preregistered divergences (locus of decodable content; onset–offset ignition vs sustained posterior activity; fronto-posterior vs within-posterior connectivity); IIT passed duration, failed sustained posterior synchrony; GNWT found PFC category decoding but no offset ignition and no identity decoding. Basis for 'M8 shared at the quantity, contested at locus/timing/connectivity'.
- Seth 2013 / Seth & Friston 2016: no statement on autonomic-only conflict; P24 is the authors' derivation and must be labelled so; Seth & Friston name predictions (not prediction errors) as the likelier correlate.
- Morsella 2005 body text not read (403); P16 locus cites BBS 2016 §2.4 until checked.
- Lau & Rosenthal 2011, Lamme 2006, Lamme & Roelfsema 2000, Park & Tallon-Baudry 2014, Azzalini 2019: abstract-only — locus claims P08, P09, P11 need full-text confirmation; say so in the limitations.
- Fleming 2020 (HOSS) vs Lau & Rosenthal 2011 (HOT): differences documented → separate rows justified (R1-6).
- Reference [84] author order should be Webb & Graziano 2015; AST locus (TPJ) rests on Kelly et al. 2014 abstract, not on Graziano & Webb 2015 as cited.
- Maniscalco & Lau 2012: 30 participants (Methods) — empirical, kept; Bor et al. 2017 replication of Rounis: no impairment, methodological differences; Huber–Payne–Puto 1982: decoy effect exists, nothing about consciousness.


## v4.4 (24 Sep 2026, after the second external audit)
- S1: 21 EXPLICIT (19 positive, 2 stated_null) / 29 INTERPRETED (22 / 7) / 68 NOT_LOCATED / 2 NOT_APPLICABLE; 16 flagged; 50 provisional; 57 abstract-only; 5 re-coded today (HOSS×M4a, HOSS×M4c → NOT_LOCATED; PP×M4b → INTERPRETED; FM×M4c, PP×M2 → NOT_LOCATED after full-text reading), previous code kept in previous_code.
- S4: 34 rows — 27 stated, 1 interpreted (P27, provenance), 6 derived (P23, P24, P25, P32, P33, P34). endorsed_by_proponents split into published_author_statement / explicit_endorsement_of_this_test.
- Pair register: 55 pairs (M8 54, M6 1): 43 different, 10 jointly compatible, 2 discriminating (P02–P05 conf 2, Cogitate-operationalised; P08–P09 conf 1), 0 incompatible. Classes (pair rule): M8 contested; M6 occupied-not-contested; M4b single-occupant; M1, M2 single-occupant; M3, M4a, M4c, M7 occupied-not-contested; M5 thin.
- S2: unit_type column (22 experiment / 2 experiment-group / 18 publication-as-one). Experiment level n = 30: NV 18, NNV 3, motor 8 (7 skeletal + 1 autonomic), valenced 0, intero 1. Publication level n = 21: NV 15, NNV 1, motor 4 (3 + 1 mixed), valenced 0, intero 1.
- §9.1: C0 tests P32 (derived), C0-eq estimates P33 (derived), C1a tests P23 (derived); C1b exploratory; two confirmatory contrasts, Holm; conjunctive rule (index + PAS sign agreement). Session 2: 104 presented per cell (26 probe + 78), 66.3 usable expected, 1144 trials, 22 blocks, ~135 min; session 1: 64 per cell. N = 120 both studies. Power at 120: single 0.903; Holm ~0.894; conjunctive product 0.799 (independence); TOST ±0.30 0.895/0.896 MC; mixed check C0 0.900, C1a 0.935 (200 sims).
- Codebook v2.2 (blind copy: no row-level S2 decisions, pair-register class rule), hash aa72e422…; coder pack v3.2.
- reproduce.py v2.1: 10 steps; full run with statsmodels 0.14.6 passes; --skip-mixed is announced, not silent.
