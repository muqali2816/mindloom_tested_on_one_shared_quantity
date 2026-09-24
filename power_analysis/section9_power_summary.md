# Section 9.1 power analysis and session arithmetic, protocol v3 (section9_power.py v2.4)

All values below are read from power_study1.csv, power_study2.csv, trials_budget.csv, trials_budget_cells.csv, trials_budget_analysis_cells.csv and power_mixed_check.csv written by this script (seed 20260924); none is typed by hand. alpha = 0.05 two-sided; target power 90 %; effect sizes are dz on per-participant contrast scores.

## Study 1 (neutral stimuli, three effectors, 0 / 1 / 3 shared pairs at count 3; count branch 1 / 2 / 3 as estimation)

**C1a, the single confirmatory contrast (P23: 0 shared pairs vs mean of 1 and 3 shared pairs at count 3; weights [-1.0, 0.5, 0.5]).** N = 119 participants are required for 90 % power at dz = 0.3 (achieved 0.901); N = 265 at dz = 0.20 and N = 68 at dz = 0.40. The fixed sample is N = 120 (the required 119 rounded up to a multiple of the 6 lever rotations); power at N = 120 and dz = 0.3 is 0.9032, uncorrected (one confirmatory contrast, so no multiplicity correction applies); minimum detectable dz at 90 % power 0.2983.
**CR, the report-based test of the stated P16 (session-1 urge rating, same cells and weights).** At the ASSUMED dz = 0.5 its power at N = 120 is 0.9997; at dz = 0.3 it is 0.9032. The anchor (Morsella et al. 2009, t(13) = 6.21) corresponds to dz = 1.660, an upper bound; the assumed value is below a third of it. Pilot stop criterion on the manipulation: a standardised urge difference (3-shared minus 0-shared) below dz = 0.5 stops the study.
**C0 (estimation; P32 positive, P25 negative; weights [-1.0, 0.5, 0.5]).** Reported two-sided with its interval; for orientation, a paired t at N = 120 would have power 0.9032 at dz = 0.3.
**P33 (count 3 - count 2, bounded estimate).** At N = 120 and a true effect of zero, exact TOST power is 0.406 (Monte Carlo 0.406 +/- 0.001) for bounds +/-0.2; 0.895 (Monte Carlo 0.896 +/- 0.001) for bounds +/-0.3; 0.993 (Monte Carlo 0.993 +/- 0.000) for bounds +/-0.4. To reach 90 % TOST power one would need N = 272 at +/-0.2, 122 at +/-0.3, 70 at +/-0.4. The bound is reported, not tested.
**C1b (exploratory).** Linear-in-shared-pairs weights ([-1.3333, -0.3333, 1.6667]): N = 265 at dz = 0.2, 119 at dz = 0.3, 68 at dz = 0.4. Two-df omnibus: N = 320 at dz = 0.2, 144 at dz = 0.3, 83 at dz = 0.4; at N = 120 power 0.476 at dz = 0.2, 0.836 at dz = 0.3, 0.979 at dz = 0.4.

### Cells, blocks and trials (session 2 carries the no-report estimate)

7 presentation cells collapsing to 5 analysis cells; 16 blocks per session (two per cell, three in the two single-cell C1a cells). Session-2 block: 52 trials (13 probe); session-1 block: 32 (8 probe). A two-block cell presents 104 in session 2 = 26 probe + 78 no-probe (raw minimum 100.39; expected usable 66.3).
Expected usable session-2 trials per analysis cell: count1@0 (1 presentation cell(s), 2 blocks) -> 66.30; count2@0 (1 presentation cell(s), 2 blocks) -> 66.30; count3@0 (1 presentation cell(s), 3 blocks) -> 99.45; count3@1 (3 presentation cell(s), 6 blocks) -> 198.90; count3@3 (1 presentation cell(s), 3 blocks) -> 99.45.
Session 2 (832 presented trials, no report in blocks): titration 6.4 min (48 trials at 8 s) + trials 83.2 min at 6 s + 15 breaks of 1 min = 104.6 min (v2, 22 blocks: 135.4 min, no titration phase).
Session 1 (512 presented trials; PAS on 384 no-probe trials, urge rating on 128 probe trials): titration 6.4 min + trials 70.4 min + practice 6.4 min (64 trials) + breaks 15 min = 98.2 min, plus training to criterion and set-up (pilot).
Urge ratings per C1a analysis cell in session 1 (probe trials, before any loss): count3@0 24; count3@1 48; count3@3 24. PAS-rated session-1 trials per analysis cell after loss: count1@0 40.8; count2@0 40.8; count3@0 61.2; count3@1 122.4; count3@3 61.2.
The mixed-model check below is calibrated at the floor of 64 usable trials per analysis cell. No sequential monitoring; N is fixed in advance.

### Mixed-model convergence check

Skipped: --skip-mixed was given; no simulation was run (n_sims = 0 in power_mixed_check.csv).

## Study 2 (valence; Supplementary Protocol S5 only)

**Main effect negative - positive at matched arousal.** N = 119 at dz = 0.3 (90 % power); N = 265 at dz = 0.20 and N = 68 at dz = 0.40.
**Incompatibility x valence interaction: estimation only.** A confirmatory test at dz = 0.20 would need N = 265; at N = 120 its power is 0.584 at dz = 0.20 and 0.903 at dz = 0.30.
Trials: 9 cells x 2 blocks = 18 blocks; 936 presented in session 2 (117.0 min with titration and breaks); 576 in session 1 (109.8 min); 1512 over both sessions.

## Assumptions to state in the protocol

- dz is defined on per-participant contrast scores of the cell-mean access index; the mixed-model check is calibrated at 64 usable session-2 trials per analysis cell (the floor) and is not an independent estimate.
- Session duration uses 6 s per trial, +2 s for a PAS rating (titration trials in both sessions; session-1 no-probe trials), +3 s for the urge rating (session-1 probe trials), 48 titration trials per session, 4 practice trials per session-1 block and 1-min breaks; planning values to be replaced by pilot timing.
- The urge-rating contrast CR is powered at an ASSUMED dz = 0.5; the pilot stop threshold equals that value.
- TOST power is computed under a true effect of exactly zero.
- The two-df omnibus power assumes the whole effect lies along one standardised contrast direction.
- Study 2 cell count (9) assumes three valence levels crossed with the three shared-pair levels at count 3, two blocks each.
- The 25 % probe-trial fraction and 15 % loss are planning values; the presented-trial counts are re-derived if piloting changes either.

Runtime of this script: 3.7 s.
