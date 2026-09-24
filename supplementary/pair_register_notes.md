> **Scope note (24 Sep 2026, integration pass).** This file documents the first build of the register — the 55 pairs of M8 and M6 produced by `build_pair_register.py`. The deposited `pair_register.csv` now holds 63 pairs: the eight cross-theory pairs of M3 (3), M7 (3), M4a (1) and M4c (1) were assessed by hand by the first coder from the Table S4 text and are marked in the `coder` column; all eight are *different* or *jointly compatible* (P18–P19, the two stated nulls on autonomic conflict, are the clearest jointly compatible pair). Completeness against S4 is enforced by `column_typology_pairs.py`.

# Pair register for Table S4 — method and mapping (audit §9, gpt_audit_v4.txt)

Coder: first coder, reading assistant. Input: `Table_S4_v2.csv` only (fields condition, manipulation_or_contrast,
outcome_measure, expected_result, locus/timing/distribution predictions, auxiliary_assumptions, notes). No sources were
fetched; nothing in the register rests on text outside S4. British spelling. Date of coding: 24 September 2026.

## 1. Scope

* **M8 (cortical signature of access).** 12 stated predictions: GNWT P01, P02, P03, P30; IIT P04, P05, P06, P31; RPT P08;
  HOT P09; AST P12; HOSS P29. All pairs with distinct `theory_id`: C(12,2) − 6 (within GNWT) − 6 (within IIT) = **54 pairs**.
* **M6 (dimensionality of phenomenal structure).** P07 (IIT) vs P10 (HOSS): **1 pair**.
* Derived predictions (status = derived, theory_id = AUTHORS) are excluded, as in `column_typology.py`.

## 2. Relation rules as applied

| relation | rule | operational test used |
|---|---|---|
| different | no shared observable | the two rows assign values to different measures (decoding vs synchrony vs ignition vs behavioural detection), or to different loci with no statement about the other's locus, or to pre- vs post-stimulus windows; **also used whenever S4 was insufficient to establish a shared observable** (noted "S4 insufficient" in the rationale) |
| jointly compatible | shared observable; both predicted values can hold together | both rows speak to the same measure in an overlapping condition, and neither row *excludes* the other's value |
| discriminating | shared observable; ≥ 1 value combination *predicted* by one row and *excluded* by the other | the combination is named in `pair_confidence_rationale`; the excluding row must contain a statement that rules it out, not merely fail to mention it |
| incompatible | shared observable; no value satisfies both | none found |

Two rules decided most cases:

1. **"Not required" is not "absent".** IIT's "PFC decodability not required" (P04) and RPT's "frontal ignition is not
   necessary" (P08) deny necessity; they do not predict the absence of PFC activity. A result "PFC decodable" therefore
   satisfies P01 without contradicting P04 or P08. This is the audit's point that representations in PFC and in
   posterior cortex can coexist unless exclusivity, necessity and a shared outcome are all given.
2. **A sign or window difference across loci is not a value difference.** P30 (fronto-parietal, negative) and P31
   (posterior, positive) concern different pre-stimulus signals in the same experiment; both relations can hold. P02
   (PFC, 300–500 ms) and P08 (visual cortex, 100–300 ms) can both occur in one trial. Such pairs are *jointly compatible*.

`shared_condition` is filled when the conditions overlap even approximately (e.g. suprathreshold Cogitate stimuli vs
near-threshold RPT stimuli, both "consciously seen visual stimuli"); the mismatch is then stated in the field and
lowers `pair_confidence`. `shared_outcome` is empty **iff** relation = different (enforced by the script).

`exclusivity_stated` is answered from the S4 text of the two rows. Statements found: P08 (necessary and sufficient;
frontal ignition not necessary), P09 (dlPFC necessity), P04 (denial of PFC necessity only), P12 (TPJ disruption impairs
awareness attributions), P07 (identity postulate). GNWT rows P01–P03, P30 and IIT rows P05, P06, P31, HOSS P29, P10
contain no exclusivity or necessity statement in S4.

`cogitate_operationalised` = yes only for the three GNWT–IIT pairs tested against each other in Cogitate 2025
(Experiment 1): P01–P04 (prediction 2 / analysis #1, decoding), P02–P05 (prediction 3 / analysis #2, temporal dynamics),
P03–P06 (prediction 5 / analysis #3, connectivity). P30–P31 was preregistered (prediction 4, Experiment 2) but
Experiment 2 is not reported in Cogitate 2025 → no. Cross-analysis GNWT–IIT pairs (e.g. P01–P05) were both tested but not
as one criterion → no, with that note.

`pair_confidence` (1–3) is the confidence in the *relation call*, assigned to the pair; it is not inherited from
`distinguishability_confidence` of either S4 row. The S4 row confidences are carried alongside
(`s4_row_confidence_a/b`) for the diagnostic recount only.

## 3. Results

| | M8 | M6 | total |
|---|---|---|---|
| pairs registered | 54 | 1 | 55 |
| different | 42 | 1 | 43 |
| jointly compatible | 10 | 0 | 10 |
| discriminating | 2 | 0 | 2 |
| incompatible | 0 | 0 | 0 |
| discriminating/incompatible with pair_confidence ≥ 2 | 1 (P02–P05) | 0 | 1 |

Discriminating pairs:

* **P02–P05** (GNWT–IIT, timing; confidence 2). Shared observable: time course of the content-specific response relative
  to onset and offset (Cogitate analysis #2). "Sustained activity tracking duration, no separate offset event" is predicted
  by P05 and excluded by P02, which requires an offset ignition. Confidence 2, not 3, because P02 names PFC and P05
  posterior cortex: a PFC-phasic / posterior-sustained outcome would satisfy both rows.
* **P08–P09** (RPT–HOT, prefrontal necessity; confidence 1). Opposite stated necessity claims: "frontal ignition is not
  necessary" vs "PFC disruption reduces awareness or meta-d′ while d′ is intact". Discriminating only if "awareness /
  meta-d′" (P09) and "phenomenal content" (P08) are the same variable; P08's auxiliary assumption (phenomenal content
  without access/report) lets RPT reinterpret a positive P09 result as access. Flagged for adjudication.

Typology (from `column_typology_pairs.py`):

| column | EXPLICIT | old class (distinguishable_from) | old, conf ≥ 2 either end | old, conf ≥ 2 both ends | **new class (pair register)** | new, pair_confidence ≥ 2 |
|---|---|---|---|---|---|---|
| M8 | 6 | contested (15 pairs) | contested (14) | contested (11) | **contested** (2 pairs) | contested (1 pair) |
| M6 | 2 | contested (1 pair) | occupied-not-contested (0) | occupied-not-contested (0) | **occupied-not-contested** (0) | occupied-not-contested |

The old script's numbers 15 / 14 / 11 are reproduced exactly (the audit's recount is confirmed). M8 remains contested
under the new definition, but on the strength of one Cogitate-operationalised timing pair (plus one confidence-1
necessity pair), not of 15. M6 changes class: the P07–P10 difference is a difference of level (structure of experience
vs the awareness-judgement axis), and S4 itself says adjudication is needed on whether the two claims address the same
variable — under the rules above that is "S4 insufficient → different".

## 4. Mapping of the 15 old M8 "distinguishable" pairs onto the four relations

| old pair | old feature (S4) | S4 row conf (a, b) | new relation | pair_conf | reason in one line |
|---|---|---|---|---|---|
| P01–P04 | locus and necessity | 2, 2 | jointly compatible | 3 | S4 notes: "P01 and P04 can both be true"; necessity is not an observable of the design |
| P01–P08 | locus and necessity | 2, 2 | jointly compatible | 2 | "frontal ignition not necessary" does not predict PFC absence |
| P01–P12 | locus (TPJ vs PFC) | 2, 2 | different | 2 | different conditions and measures; neither excludes the other's locus |
| P02–P05 | timing | 3, 1 | **discriminating** | 2 | "no separate offset event" predicted by P05, excluded by P02; locus caveat |
| P02–P08 | timing and locus | 3, 2 | jointly compatible | 2 | 100–300 ms visual and 300–500 ms PFC can both occur |
| P03–P06 | connectivity locus | 3, 3 | jointly compatible | 2 | long- and short-range synchrony can both be present; neither predicts the other's absence |
| P04–P09 | locus and necessity | 2, 2 | different | 2 | decoding statement vs causal TMS claim; IIT prediction for TMS not in S4 |
| P04–P12 | locus | 2, 2 | different | 2 | different measures; TPJ lies inside the "posterior hot zone" |
| P04–P29 | locus and distribution | 2, 1 | different | 2 | content decoding vs awareness-state decoding |
| P05–P29 | distribution/timing | 1, 1 | different | 2 | duration tracking vs presence/absence ignition: no shared observable |
| P08–P09 | locus and necessity | 2, 2 | **discriminating** | 1 | opposite necessity claims; identity of the awareness variable unsettled |
| P08–P12 | locus | 2, 2 | different | 2 | VAN vs TPJ disruption; sufficiency claim bears only if TPJ spares recurrence |
| P08–P29 | locus and necessity | 2, 1 | jointly compatible | 2 | ignition for presence (P29) not excluded by "not necessary" (P08) |
| P09–P12 | locus | 2, 2 | different | 2 | different sites and different outcomes (meta-d′ vs detection) |
| P30–P31 | sign and locus | 3, 3 | jointly compatible | 2 | opposite signs at different loci can hold simultaneously |

Summary of the mapping: 7 different, 6 jointly compatible, 2 discriminating, 0 incompatible. Four of the pairs the old
register rated confidence 3 (P02–P08, P03–P06, P30–P31 and, at one end, P02–P05) turn out to be compatible or only
conditionally discriminating; the highest S4 row confidences attached to the *clarity of the description*, not to
exclusion of a value.

Pairs new to the register (39 M8 pairs not in `distinguishable_from`) are almost all *different*; four are jointly
compatible and allied (P04–P08, P05–P08, P06–P08: RPT's local recurrent loop lies within IIT's posterior hot zone;
P02–P29: both predict ignition on conscious detection).

## 5. Consequences for the manuscript (for the first coder to decide)

* The introduction's formula "only a contested column lets a prediction lose" should go (audit §9): P01, P02, P03, P06
  each failed or were challenged on their *own* Cogitate criterion inside pairs coded here as jointly compatible.
* "15 pairs" and "14 pairs with confidence ≥ 2" should be replaced by the pair-level counts above, with the
  relation vocabulary (different / jointly compatible / discriminating / incompatible).
* M6 should be reported as occupied-not-contested unless the first coder adjudicates P07–P10 as addressing one variable.

## 6. Limitations

* Reading assistant coding only; all 55 relation calls await the first coder's review, and P08–P09 and P07–P10 are
  flagged for adjudication.
* No source was consulted beyond S4; where S4 lacked a statement (e.g. whether IIT predicts the outcome of dlPFC TMS,
  whether RPT predicts sustained recurrence for 1.5 s stimuli), the pair was coded *different* or given confidence 1
  rather than filled from memory of the literature.
* `exclusivity_stated` reflects S4 text, not the full sources.
