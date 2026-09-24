# Supplementary Protocol S5 — Study 1 (incompatibility at fixed count, neutral content) and Study 2 (valence)

Manuscript brainsci-4583950, revision 1. This protocol is new in revision and is referenced from §9.1 of the main text. Every power figure below is read from `power_study1.csv`, `power_study2.csv`, `trials_budget.csv` and `section9_power_summary.md`, written by `section9_power.py` (v2.0, seed 20260924); none is typed by hand. Design parameters carried over from the earlier version of §9.1 (stimulus timing, EEG window, exclusion thresholds) are design choices and are marked as such where they appear. Items the authors must still set are given as `[NUMBER: …]`.

## S5.1 Why the earlier design was replaced

The earlier §9.1 varied incompatibility through the target's feature conjunction: three rules demanded three identical keys (I1), two identical and one different (I2) or three different keys (I3), with N = 126 and sequential Bayes-factor monitoring. Under that manipulation the number of distinct responses (1, 2, 3) covaried with incompatibility, so the incompatibility contrast was also a contrast in response-set size and in congruency. The supramodular sources locate the gradation of conscious conflict along the compatibility axis and explicitly allow compatible plans to co-occur without perturbing consciousness (synchrony blindness; Morsella et al. 2016, authors' response), so the earlier design could not have tested what the theory states. The present design fixes the number of distinguishable responses at three and varies only whether they can be executed jointly.

## S5.2 What is tested

Study 1 tests two predictions (P16, P23) and estimates one quantity; P25 appears in the table because the count branch bears on it, but no contrast is powered for it.

| Label | Prediction | Status | Source |
|---|---|---|---|
| P16 | Conscious involvement when ≥ 2 incompatible inclinations reach the skeletomotor output system; nothing stated about a further increase beyond two | stated (SIT) | Morsella 2005 (abstract); Morsella et al. 2016 §2.4 |
| P23 | Access to a masked target rises with the incompatibility of the policies it licenses, at fixed count and load | derived by the authors; not endorsed by SIT proponents | this manuscript |
| P25 | More competing policies degrade access (load) | derived; GNWT plus a capacity assumption GNWT has not made — **not tested**: the count branch (C0) tests the P16 threshold; a monotone decrement across 1/2/3 would be *consistent with* P25 and is reported descriptively | this manuscript |
| — | Cortical–autonomic coupling index | estimation only; no coded theory predicts over it | — |

A null on C1a (P23) constrains the authors' derivation within the preregistered equivalence bound; it does not refute supramodular interaction theory, whose stated outcome variable is experienced conflict, not access. The condition discriminates between no two coded theories.

## S5.3 Participants

Healthy right-handed adults aged 18–40, normal or corrected acuity and colour vision (hue is a rule feature), no neurological, psychiatric or cardiovascular history or related medication (design choice, carried from the earlier version). Confirmatory sample N = 119, fixed in advance; no sequential monitoring. Recruitment continues until 119 participants have complete, non-excluded data for both sessions; the number recruited is reported.

## S5.4 Stimuli

Targets are grey-scale neutral-expression faces of six identities (three female) from the Karolinska Directed Emotional Faces set [1], equated on luminance histogram and spatial-frequency spectrum with the SHINE toolbox [2], cropped to an oval and shown at 4° (design choices carried from the earlier version). Each face carries three task features orthogonal to identity: isoluminant tint (three hues), position (above, at or below fixation) and aperture shape (circle, square, diamond). Each rule maps its three feature values onto the three positions of a lever (up, middle, down). The stimulus set is restricted to feature conjunctions for which the three demanded lever positions are mutually distinct, so that on every trial the target demands three distinguishable responses; the six permutations of (up, middle, down) over the three rules occur equally often. Rule-to-feature and value-to-position assignments are rotated across participants.

## S5.5 Effectors and the incompatibility manipulation

Three three-position levers: left hand, right hand, dominant foot. A response is a lever position. Two responses on different levers can be executed jointly; two responses on the same lever cannot. Incompatibility on a trial is the number of pairs of demanded responses that share a lever:

| Shared pairs | Effector mapping in force | Co-executable? |
|---|---|---|
| 0 | hue → lever A, position → lever B, shape → lever C | all three jointly |
| 1 | two rules on one lever, the third on another | the pair on the shared lever cannot be executed jointly |
| 3 | all three rules on one lever | none jointly |

The mapping is announced at the start of each block and overlearned in training; the stimulus set is identical across mappings. The count branch keeps all rules on separate levers (0 shared pairs) and puts one, two or three rules in force.

## S5.6 Cell list

Eleven presentation cells, balanced over effectors within participant, collapsing to five analysis cells:

| Analysis cell | Presentation cells | Balance |
|---|---|---|
| count 1, 0 shared | 3 | which single rule/lever is in force |
| count 2, 0 shared | 3 | which pair of rules/levers is in force |
| count 3, 0 shared | 1 | one mapping (levers rotated across participants) |
| count 3, 1 shared | 3 | which pair of rules shares a lever |
| count 3, 3 shared | 1 | all rules on one lever (lever rotated across participants) |

Cells are intermixed in blocks; block order is counterbalanced across participants and sessions.

## S5.7 Trial structure and sessions

Fixation 500–800 ms; target 33 ms at an individually titrated contrast; pattern mask at 50 ms SOA for 200 ms, contrast staircased to about 50 % visibility [3]; 1,000 ms blank (design choices carried from the earlier version). On 25 % of trials a probe names one rule in force and the participant executes it on the appropriate lever, or gives a fourth response for "no face"; on 75 % nothing is required. Probe trials keep the rules active and are the manipulation check. Session 1 adds a Perceptual Awareness Scale rating [4] after the probe phase on every trial; session 2 repeats the stimulation without the rating. Two sessions at least 48 h apart.

## S5.8 Presented and usable trials

From `trials_budget.csv` (version 2.0): target ≥ 64 usable no-report trials per cell; probe fraction 0.25; assumed loss 0.15; raw presented per cell 100.39, rounded to 102 (a multiple of two sessions); expected usable 65.0 per cell; probe trials per cell 25.5.

| Grouping | Cells | Presented per cell | Presented per session | Presented total | Expected usable total |
|---|---|---|---|---|---|
| Analysis cells | 5 | 102 | 255 | 510 | 325.1 |
| Presentation cells (effector-balanced) | 11 | 102 | 561 | 1122 | 715.3 |

The 11-cell budget is what is run: 561 presented trials per session. Analysis cells that pool three presentation cells therefore exceed 64 usable trials; the count-3/0-shared and count-3/3-shared cells have the expected 65. If piloting changes the probe fraction or the loss rate, the presented-trial count is re-derived by the script before preregistration.

## S5.9 Exclusions (preregistered)

Below 90 % accuracy on full-contrast probe trials after training; titrated visibility outside 35–65 % on the Perceptual Awareness Scale in session 1; cross-validated decoder AUC below 0.70 in session 1; more than 30 % of trials lost to artefact in either session (thresholds carried from the earlier version as design choices). A participant excluded on any criterion is replaced until N = 119 is reached.

## S5.10 The access index and its freezing

Trial-wise decoded evidence (logit) for "seen" from a per-participant classifier trained on session-1 trials labelled by the Perceptual Awareness Scale rating, using posterior EEG in the 100–350 ms window, where the visual awareness negativity survives removal of report while the P3b does not [5–8]. The index is EEG-only: no pupil, blink or oculomotor feature enters it, so that the autonomic channels of S5.11 remain independent of it. Freezing: the channel set, time window, preprocessing pipeline and classifier family are fixed at preregistration and adjusted only by the pilot (S5.13); per-participant weights are estimated on session 1 and written to the archive before any session-2 trial is scored. Two preregistered validity conditions: (i) trained on trials from one incompatibility level, the classifier must generalise to the other two at the pilot-set accuracy, so that it indexes seeing rather than conflict; (ii) applied under cross-validation to session 1, it must reproduce the rating-based cell differences. The index is a candidate marker of access and not a measure of M5. Every contrast is also computed on the session-1 rating; a result is claimed only where both arms agree.

## S5.11 Autonomic channels and the coupling metric

Lead-II ECG, skin conductance and pupil diameter are recorded throughout both sessions alongside 64-channel EEG (0.1–40 Hz; epochs −200 to 800 ms). Heartbeat-evoked potential: mean fronto-central amplitude 250–400 ms after the last R-peak preceding the target by at least 400 ms, cardiac-field artefact controlled by surrogate-R-peak permutation; direction preregistered two-sided [9,10]; cardiac phase at onset as covariate. Phasic skin conductance deconvolved 1–5 s post-target [11,12]; pupil dilation as baseline-corrected mean 0.5–2 s post-target [13]. Coupling index: (a) the per-participant, per-cell standardised slope of decoded access on pre-stimulus heartbeat-evoked amplitude; (b) the trial-wise correlation of decoded access with the phasic skin-conductance and pupil responses. Both are reported with point estimate and 95 % interval per cell and as a function of shared pairs. **Estimation only:** no coded theory predicts over the index, it is not a measure of M5 in the organism-wide sense of §7, and no hypothesis test is attached to it.

## S5.12 Contrasts, weights and tests

Effect sizes are dz on per-participant contrast scores of the cell-mean access index; α = 0.05 two-sided; target power 0.90.

| Contrast | Cells (order) | Weights | Test | Tests |
|---|---|---|---|---|
| C0 | count 1, 2, 3 at 0 shared | −1, 0.5, 0.5 | paired t | P16 (threshold: 1 vs ≥ 2) |
| C0-eq | count 2, 3 at 0 shared | 0, −1, 1 | TOST, bounds ±0.30 dz, α 0.05 each side [14] | the unstated further increase (estimation with a bound) |
| C1a | shared 0, 1, 3 at count 3 | −1, 0.5, 0.5 | paired t | P23 (authors' derivation) |
| C1b-lin | shared 0, 1, 3 at count 3 | −1.3333, −0.3333, 1.6667 (linear in shared pairs) | paired t | exploratory |
| C1b-omni | shared 0, 1, 3 at count 3 | two orthogonal contrasts | Hotelling T², F(2, N − 2) | exploratory |

Ordinal weights (−1, 0, +1) are not used for C1b because they would treat the step from 1 to 3 shared pairs as equal to the step from 0 to 1. A null on C1a is interpreted through a TOST with the same ±0.30 dz bound, whose power at N = 119 is that given for C0-eq below. Analyses are mirrored on the session-1 rating.

## S5.13 Power (from `power_study1.csv`)

Paired-t sample sizes for C0 and C1a (identical computations):

| dz | N for 80 % | N for 90 % |
|---|---|---|
| 0.20 | 199 | 265 |
| 0.30 | 90 | 119 |
| 0.40 | 52 | 68 |

Fixed sample N = 119: achieved power 0.9008 at dz = 0.30 for C0 and C1a; minimum detectable dz at 90 % power 0.2996.

Exploratory C1b at N = 119: linear-in-shared-pairs power 0.5808 (dz 0.20), 0.9008 (0.30), 0.9911 (0.40); N for 90 % 265 / 119 / 68. Two-df omnibus power 0.4727 / 0.8326 / 0.978; N for 90 % 320 / 144 / 83.

Equivalence (C0-eq) at N = 119, true effect 0: bounds ±0.20 dz, power 0.400 (Monte Carlo 0.399 ± 0.001), N for 90 % 272; bounds ±0.30, power 0.892 (Monte Carlo 0.892 ± 0.001), N for 90 % 122; bounds ±0.40, power 0.993 (Monte Carlo 0.993), N for 90 % 70. The ±0.30 bound is the planning effect size itself; the equivalence claim is adequately powered at the fixed N only for that bound or wider, and if P16's trigger leaves a small residual increase the equivalence power falls.

Mixed-model check (`power_mixed_check.csv`): at N = 119 and 64 usable trials per cell, 200 simulated data sets calibrated to dz = 0.30 — C1a: analytic 0.901, two-stage paired t 0.930, linear mixed model with random slopes 0.930 (Monte Carlo SE about 0.0212), 0 non-converged; C0: 0.901 / 0.920 / 0.920, 0 non-converged. Agreement with the analytic value is expected by construction; the check confirms the calibration and is not an independent estimate. The two-df omnibus power assumes the whole effect lies along one contrast direction.

Effect-size anchor: incompatible against compatible intentions on report-based ratings, t(13) = 6.21 [15], an upper bound that retained variance this design removes; the planning value dz = 0.30 sits below it.

## S5.14 Mandatory pilot

A pilot of `[NUMBER: pilot sample size — to be set by the authors]` participants runs the full session-1 procedure. Three criteria, each preregistered, must all be met before the confirmatory sample begins:

1. **Threshold.** The masking staircase holds Perceptual Awareness Scale visibility within 35–65 % across the session for every included pilot participant, and the titrated contrast is stable across blocks.
2. **Transfer.** The frozen classifier, trained at one incompatibility level, reaches cross-validated AUC ≥ 0.70 at each of the other two levels (index of seeing, not of conflict), and reproduces the rating-based cell differences under cross-validation.
3. **Accuracy.** Full-contrast probe accuracy ≥ 90 % in every cell, including joint execution of co-executable responses on 0-shared trials and correct single-lever execution on 3-shared trials, confirming that the co-executability assumption of S5.5 holds behaviourally.

If any criterion fails the study stops and the pilot is reported. If the probe fraction or the loss rate observed in the pilot differs from the planning values, the presented-trial count is re-derived before preregistration.

## S5.15 Study 2 — valence (Supplementary only)

**Rationale.** Study 2 asks whether valenced content shifts the access threshold at matched arousal, the cell that Table 2 shows to be empty in the checked theory-addressed sample, and whether the incompatibility effect of Study 1 differs by valence. The first is a confirmatory test of a prediction stated only by predictive processing (M3); the second is estimation.

**Stimuli.** The Study 1 identities in sad, neutral and happy expressions from the same set, whose validation supplies hit-rate, intensity and arousal norms [1]. Sad rather than fearful expressions are used because threat gains access through routes that need not involve valence [16,17]. Sad and happy exemplars are matched on normative arousal; neutral exemplars are necessarily lower, so the critical contrast is negative against positive at matched arousal, with trial-wise pupil and skin-conductance responses as covariates. Equated with SHINE as in Study 1.

**Design.** Nine cells: valence (negative, neutral, positive) × shared pairs (0, 1, 3) at count 3 (the count branch is not repeated); 102 presented trials per cell, 918 per participant, 459 per session; two sessions; access index, autonomic channels and exclusions as in Study 1, with one added exclusion — a participant whose own post-session ratings fail to order the faces negative < neutral < positive is excluded.

**Sample and power (from `power_study2.csv`).** Confirmatory contrast: negative − positive at matched arousal, paired t, dz = 0.30 → N = 119 at 90 % power (80 %: 90); dz = 0.20 → 265 (80 %: 199); dz = 0.40 → 68 (80 %: 52). Study 2 sample N = 119, fixed, no sequential monitoring. Incompatibility × valence interaction (contrast-of-contrasts): a confirmatory test at dz = 0.20 would need N = 265; at N = 119 its power is 0.581 at dz = 0.20 and 0.901 at dz = 0.30. **The interaction is therefore estimated and reported with its estimate and interval, not tested.** Minimum detectable dz for any paired contrast at N = 119 is 0.2996.

**Interpretation.** A negative − positive effect corroborates the one trial-level account that predicts over M3 and separates none of the coded theories, since GNWT, higher-order thought theory, supramodular interaction theory and passive frame theory carry constructed nulls over valence that none has stated. The interaction estimate is deposited for any theory that later states a prediction over it.

## S5.16 Data, code and deposit

`section9_power.py` (v2.0) writes `power_study1.csv`, `power_study2.csv`, `trials_budget.csv` and `power_mixed_check.csv`; `reproduce.py` re-derives every number in this protocol and in §9.1. The frozen index specification, the effector-mapping tables and the preregistration document are deposited with Tables S1–S4 at [repository], DOI [DOI to be inserted on public deposit — archive assembled].

## References (Protocol S5)

1. Goeleven, E.; De Raedt, R.; Leyman, L.; Verschuere, B. The Karolinska Directed Emotional Faces: A validation study. *Cognition & Emotion* **2008**, *22*, 1094–1118. https://doi.org/10.1080/02699930701626582
2. Willenbockel, V.; Sadr, J.; Fiset, D.; Horne, G.O.; Gosselin, F.; Tanaka, J.W. Controlling low-level image properties: The SHINE toolbox. *Behavior Research Methods* **2010**, *42*, 671–684. https://doi.org/10.3758/brm.42.3.671
3. Del Cul, A.; Baillet, S.; Dehaene, S. Brain Dynamics Underlying the Nonlinear Threshold for Access to Consciousness. *PLoS Biology* **2007**, *5*, e260. https://doi.org/10.1371/journal.pbio.0050260
4. Ramsøy, T.Z.; Overgaard, M. Introspection and subliminal perception. *Phenomenology and the Cognitive Sciences* **2004**, *3*, 1–23. https://doi.org/10.1023/b:phen.0000041900.30172.e8
5. Pitts, M.A.; Metzler, S.; Hillyard, S.A. Isolating neural correlates of conscious perception from neural correlates of reporting one's perception. *Frontiers in Psychology* **2014**, *5*. https://doi.org/10.3389/fpsyg.2014.01078
6. Cohen, M.A.; Ortego, K.; Kyroudis, A.; Pitts, M. Distinguishing the Neural Correlates of Perceptual Awareness and Postperceptual Processing. *The Journal of Neuroscience* **2020**, *40*, 4925–4935. https://doi.org/10.1523/jneurosci.0120-20.2020
7. Schlossmacher, I.; Dellert, T.; Pitts, M.; Bruchmann, M.; Straube, T. Differential Effects of Awareness and Task Relevance on Early and Late ERPs in a No-Report Visual Oddball Paradigm. *The Journal of Neuroscience* **2020**, *40*, 2906–2913. https://doi.org/10.1523/jneurosci.2077-19.2020
8. Dellert, T.; Müller-Bardorff, M.; Schlossmacher, I.; Pitts, M.; Hofmann, D.; Bruchmann, M.; Straube, T. Dissociating the Neural Correlates of Consciousness and Task Relevance in Face Perception Using Simultaneous EEG-fMRI. *The Journal of Neuroscience* **2021**, *41*, 7864–7875. https://doi.org/10.1523/jneurosci.2799-20.2021
9. Park, H.D.; Correia, S.; Ducorps, A.; Tallon-Baudry, C. Spontaneous fluctuations in neural responses to heartbeats predict visual detection. *Nature Neuroscience* **2014**, *17*, 612–618. https://doi.org/10.1038/nn.3671
10. Al, E.; Iliopoulos, F.; Forschack, N.; Nierhaus, T.; Grund, M.; Motyka, P.; Gaebler, M.; Nikulin, V.V.; Villringer, A. Heart–brain interactions shape somatosensory perception and evoked potentials. *Proceedings of the National Academy of Sciences* **2020**, *117*, 10575–10584. https://doi.org/10.1073/pnas.1915629117
11. Benedek, M.; Kaernbach, C. A continuous measure of phasic electrodermal activity. *Journal of Neuroscience Methods* **2010**, *190*, 80–91. https://doi.org/10.1016/j.jneumeth.2010.04.028
12. Boucsein, W.; Fowles, D.C.; Grimnes, S.; Ben-Shakhar, G.; Roth, W.T.; Dawson, M.E.; Filion, D.L. Publication recommendations for electrodermal measurements. *Psychophysiology* **2012**, *49*, 1017–1034. https://doi.org/10.1111/j.1469-8986.2012.01384.x
13. Mathôt, S.; Vilotijević, A. Methods in cognitive pupillometry: Design, preprocessing, and statistical analysis. *Behavior Research Methods* **2022**, *55*, 3055–3077. https://doi.org/10.3758/s13428-022-01957-7
14. Lakens, D.; Scheel, A.M.; Isager, P.M. Equivalence Testing for Psychological Research: A Tutorial. *Advances in Methods and Practices in Psychological Science* **2018**, *1*, 259–269. https://doi.org/10.1177/2515245918770963
15. Morsella, E.; Gray, J.R.; Krieger, S.C.; Bargh, J.A. The essence of conscious conflict: Subjective effects of sustaining incompatible intentions. *Emotion* **2009**, *9*, 717–728. https://doi.org/10.1037/a0017121
16. Yang, E.; Zald, D.H.; Blake, R. Fearful expressions gain preferential access to awareness during continuous flash suppression. *Emotion* **2007**, *7*, 882–886. https://doi.org/10.1037/1528-3542.7.4.882
17. Gayet, S.; Paffen, C.L.E.; Belopolsky, A.V.; Theeuwes, J.; Van der Stigchel, S. Visual input signaling threat gains preferential access to awareness in a breaking continuous flash suppression paradigm. *Cognition* **2016**, *149*, 77–83. https://doi.org/10.1016/j.cognition.2016.01.009
