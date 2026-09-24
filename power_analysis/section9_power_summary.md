# Section 9.1 power analysis, new design (section9_power.py v2.2)

All values below are read from power_study1.csv, power_study2.csv, trials_budget.csv and power_mixed_check.csv written by this script (seed 20260924); none is typed by hand. alpha = 0.05 two-sided; target power 90 %; effect sizes are dz on per-participant contrast scores.

## Study 1 (neutral stimuli, three effectors, 0 / 1 / 3 shared pairs, count branch 1 / 2 / 3)

**C0 (P16, threshold: count 1 vs >= 2 at 0 shared pairs; weights [-1.0, 0.5, 0.5]).** N = 119 participants give 90 % power at dz = 0.3 (achieved 0.901); N = 265 at dz = 0.20 and N = 68 at dz = 0.40.
**C1a (P23, author-derived: 0 shared pairs vs mean of 1 and 3 shared pairs at count 3; weights [-1.0, 0.5, 0.5]).** The same paired-t computation applies: N = 119 at dz = 0.3. The fixed sample is therefore N = 119; its minimum detectable dz at 90 % power is 0.298.
**Equivalence half of P16 (count 3 - count 2, TOST).** At N = 119 and a true effect of zero, exact TOST power is 0.406 (Monte Carlo 0.406 +/- 0.001) for bounds +/-0.2; 0.895 (Monte Carlo 0.896 +/- 0.001) for bounds +/-0.3; 0.993 (Monte Carlo 0.993 +/- 0.000) for bounds +/-0.4. To reach 90 % TOST power one would need N = 272 at +/-0.2, 122 at +/-0.3, 70 at +/-0.4. The bound +/-0.3 is the planning effect size itself; the equivalence claim is thus adequately powered at the fixed N only for that bound or wider.
**C1b (0 / 1 / 3 shared pairs, unequal steps).** With weights linear in the number of shared pairs ([-1.3333, -0.3333, 1.6667], i.e. -4, -1, +5 up to scale) the one-df test needs N = 265 at dz = 0.2, 119 at dz = 0.3, 68 at dz = 0.4. The two-df omnibus (Hotelling T^2, effect on one contrast direction) needs N = 320 at dz = 0.2, 144 at dz = 0.3, 83 at dz = 0.4; at the fixed N = 119 its power is 0.476 at dz = 0.2, 0.836 at dz = 0.3, 0.979 at dz = 0.4. The ordinal weights (-1, 0, +1) are not used: they would treat the step from 1 to 3 shared pairs as equal to the step from 0 to 1.

### Trials (session 2 carries the no-report estimate)

Session 1 collects a PAS rating on every trial and trains the access classifier; only session-2 trials enter the no-report estimate. With 25 % probe trials and an expected loss of 15 %, the smallest session-2 count per presentation cell with exactly one quarter probe trials that leaves an expected >= 64 usable trials is 104 = 26 probe + 78 no-probe (raw minimum 100.39; expected usable 66.3). Session 1 presents 64 per cell (a design choice: a quarter-probe integer per block; expected 54.4 usable PAS-rated trials per cell for the classifier and the PAS version of the contrasts). For the 11 effector-balanced presentation cells that is 1144 presented trials in session 2 and 1848 over both sessions; at 6 s per trial in 22 blocks of 52 (13 probe per block) with 1-min breaks, session 2 lasts about 135.4 min; session 1, at 8 s per trial in 22 blocks of 32, about 114.9 min. The previous rule pooled both sessions (102 presented per cell) and over-counted usable no-report trials by a factor of two.
Expected usable session-2 trials per analysis cell: count1@0 pools 3 -> 198.9; count2@0 pools 3 -> 198.9; count3@0 pools 1 -> 66.3; count3@1 pools 3 -> 198.9; count3@3 pools 1 -> 66.3. The mixed-model check below is calibrated at the floor of 64 usable trials per analysis cell, the target that the single-presentation-cell analysis cells (count3@0, count3@3) just meet. No sequential Bayes-factor monitoring is used; N is fixed in advance.

### Mixed-model convergence check

Skipped: --skip-mixed was given; no simulation was run (n_sims = 0 in power_mixed_check.csv).

## Study 2 (valence; Supplementary Protocol S5 only)

**Main effect negative - positive at matched arousal.** N = 119 at dz = 0.3 (90 % power); N = 265 at dz = 0.20 and N = 68 at dz = 0.40.
**Incompatibility x valence interaction: estimation only.** A confirmatory test at dz = 0.20 would need N = 265; at the Study 2 sample of N = 119 the power for that interaction is 0.584 at dz = 0.20 and 0.903 at dz = 0.30. The interaction is therefore reported with its estimate and interval, not tested.
Trials: 9 cells (valence (3) x shared pairs (3) at count 3 [assumed]) x 104 presented in session 2 = 936 session-2 trials (about 110.6 min); 1512 over both sessions.

## Assumptions to state in the protocol

- dz is defined on per-participant contrast scores of the cell-mean access index; the mixed-model check is calibrated to the same dz at 64 usable session-2 trials per analysis cell (the planning floor) and is not an independent estimate.
- Session duration uses 6 s per trial (+2 s for the PAS rating in session 1), 2 blocks per presentation cell and 1-min breaks; these are planning values to be replaced by pilot timing.
- TOST power is computed under a true effect of exactly zero; if P16's trigger leaves a small residual increase, equivalence power falls.
- The two-df omnibus power assumes the whole effect lies along one standardised contrast direction (the conservative allocation for a fixed dz).
- Study 2 cell count (9) assumes three valence levels crossed with the three shared-pair levels at count 3; the confirmatory contrast uses only the negative and positive cells.
- The 25 % probe-trial fraction and 15 % loss are planning values; the presented-trial count should be re-derived if piloting changes either.

Runtime of this script: 3.7 s.
