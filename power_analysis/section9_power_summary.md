# Section 9.1 power analysis, new design (section9_power.py v2.0)

All values below are read from power_study1.csv, power_study2.csv, trials_budget.csv and power_mixed_check.csv written by this script (seed 20260924); none is typed by hand. alpha = 0.05 two-sided; target power 90 %; effect sizes are dz on per-participant contrast scores.

## Study 1 (neutral stimuli, three effectors, 0 / 1 / 3 shared pairs, count branch 1 / 2 / 3)

**C0 (P16, threshold: count 1 vs >= 2 at 0 shared pairs; weights [-1.0, 0.5, 0.5]).** N = 119 participants give 90 % power at dz = 0.3 (achieved 0.901); N = 265 at dz = 0.20 and N = 68 at dz = 0.40.
**C1a (P23, author-derived: 0 shared pairs vs mean of 1 and 3 shared pairs at count 3; weights [-1.0, 0.5, 0.5]).** The same paired-t computation applies: N = 119 at dz = 0.3. The fixed sample is therefore N = 119; its minimum detectable dz at 90 % power is 0.300.
**Equivalence half of P16 (count 3 - count 2, TOST).** At N = 119 and a true effect of zero, exact TOST power is 0.400 (Monte Carlo 0.399 +/- 0.001) for bounds +/-0.2; 0.892 (Monte Carlo 0.892 +/- 0.001) for bounds +/-0.3; 0.993 (Monte Carlo 0.993 +/- 0.000) for bounds +/-0.4. To reach 90 % TOST power one would need N = 272 at +/-0.2, 122 at +/-0.3, 70 at +/-0.4. The bound +/-0.3 is the planning effect size itself; the equivalence claim is thus adequately powered at the fixed N only for that bound or wider.
**C1b (0 / 1 / 3 shared pairs, unequal steps).** With weights linear in the number of shared pairs ([-1.3333, -0.3333, 1.6667], i.e. -4, -1, +5 up to scale) the one-df test needs N = 265 at dz = 0.2, 119 at dz = 0.3, 68 at dz = 0.4. The two-df omnibus (Hotelling T^2, effect on one contrast direction) needs N = 320 at dz = 0.2, 144 at dz = 0.3, 83 at dz = 0.4; at the fixed N = 119 its power is 0.473 at dz = 0.2, 0.833 at dz = 0.3, 0.978 at dz = 0.4. The ordinal weights (-1, 0, +1) are not used: they would treat the step from 1 to 3 shared pairs as equal to the step from 0 to 1.

### Trials

With 25 % probe trials and an expected loss of 15 %, 102 presented trials per cell (raw 100.39, rounded up to a multiple of 2 sessions) yield an expected 65.0 usable no-report trials per cell (target >= 64). For the 5 analysis cells this is 510 presented trials, 255 per session; for the 11 effector-balanced presentation cells it is 1122 presented trials, 561 per session. No sequential Bayes-factor monitoring is used; N is fixed in advance.

### Mixed-model convergence check

C1a_compatible_vs_incompatible_at_count3: at N = 119, 64 usable trials per cell, 200 simulated data sets calibrated to dz = 0.3: analytic power 0.901; two-stage (paired t on contrast scores) 0.930; linear mixed model with random slopes 0.930 (Monte Carlo SE about 0.0212); non-converged fits: 0. Agreement with the analytic value is expected by construction; the check confirms the calibration.
C0_threshold_count1_vs_ge2: at N = 119, 64 usable trials per cell, 200 simulated data sets calibrated to dz = 0.3: analytic power 0.901; two-stage (paired t on contrast scores) 0.920; linear mixed model with random slopes 0.920 (Monte Carlo SE about 0.0212); non-converged fits: 0. Agreement with the analytic value is expected by construction; the check confirms the calibration.

## Study 2 (valence; Supplementary Protocol S5 only)

**Main effect negative - positive at matched arousal.** N = 119 at dz = 0.3 (90 % power); N = 265 at dz = 0.20 and N = 68 at dz = 0.40.
**Incompatibility x valence interaction: estimation only.** A confirmatory test at dz = 0.20 would need N = 265; at the Study 2 sample of N = 119 the power for that interaction is 0.581 at dz = 0.20 and 0.901 at dz = 0.30. The interaction is therefore reported with its estimate and interval, not tested.
Trials: 9 cells (valence (3) x shared pairs (3) at count 3 [assumed]) x 102 presented = 918 trials, 459 per session.

## Assumptions to state in the protocol

- dz is defined on per-participant contrast scores of the cell-mean access index; the mixed-model check is calibrated to the same dz at 64 usable trials per cell and is not an independent estimate.
- TOST power is computed under a true effect of exactly zero; if P16's trigger leaves a small residual increase, equivalence power falls.
- The two-df omnibus power assumes the whole effect lies along one standardised contrast direction (the conservative allocation for a fixed dz).
- Study 2 cell count (9) assumes three valence levels crossed with the three shared-pair levels at count 3; the confirmatory contrast uses only the negative and positive cells.
- The 25 % probe-trial fraction and 15 % loss are planning values; the presented-trial count should be re-derived if piloting changes either.

Runtime of this script: 56.6 s.
