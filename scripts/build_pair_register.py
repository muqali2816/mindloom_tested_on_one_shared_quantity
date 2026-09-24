"""Build pair_register.csv for M8 (all cross-theory pairs of stated predictions) and M6 (P07 vs P10).

Codings below are the first coder's reading assistant's reading of Table_S4_v2.csv text ONLY
(condition, manipulation_or_contrast, outcome_measure, expected_result, locus/timing/distribution
predictions, auxiliary_assumptions). No sources were fetched.

Relation rules (audit §9, gpt_audit_v4.txt):
  different            no shared observable (or S4 insufficient to establish one)
  jointly compatible   shared observable, both predicted values can hold together
  discriminating       shared observable, at least one value combination is PREDICTED by one
                       prediction and EXCLUDED by the other (named in the row)
  incompatible         shared observable, no value satisfies both
A combination that is merely *consistent with* one prediction (not predicted by it) does not
make the pair discriminating: 'PFC decodability not required' does not predict PFC absence.
"""
import itertools
import pandas as pd

reg = pd.read_csv("ctx/Table_S4_v2.csv", dtype=str, keep_default_na=False)
stated = reg[reg.status == "stated"]
theory = dict(zip(stated.id, stated.theory_id))
dom = dict(zip(stated.id, stated.quantity_id))
rowconf = dict(zip(stated.id, stated.distinguishability_confidence))

COG1 = ("Cogitate Experiment 1: suprathreshold visual stimuli (faces, objects, letters, false fonts), "
        "task-relevant and task-irrelevant, 0.5/1.0/1.5 s")
COG2 = "Cogitate Experiment 2: near-threshold stimuli (video-game paradigm), seen vs unseen, pre-stimulus window"

# own expected result of each prediction, used in the 'favour' fields
own = {
    "P01": "content (category/identity/orientation) decodable from PFC after onset, for task-irrelevant stimuli as well",
    "P02": "a second, offset-locked PFC ignition (~0.3-0.5 s after offset) with an activity-silent interval between onset and offset bursts",
    "P03": "content-specific PFC-posterior (gamma/beta) synchrony present when content is consciously perceived",
    "P04": "content decodable from the posterior hot zone throughout the percept",
    "P05": "posterior content-specific activation tracks stimulus duration (0.5/1.0/1.5 s), no separate offset event",
    "P06": "sustained content-specific synchrony within posterior cortex (category-selective areas <-> V1/V2)",
    "P08": "local recurrent activity in visual cortex (~100-300 ms; VAN) present for seen, absent for unseen, independent of report",
    "P09": "dlPFC disruption reduces subjective awareness / meta-d' while d' is intact",
    "P12": "bilateral TPJ activity during awareness attribution; TPJ disruption produces neglect-like detection loss; attention control without awareness possible but impaired",
    "P29": "frontoparietal ignition for presence reports but not absence reports; PFC decodes presence and absence symmetrically",
    "P30": "higher pre-stimulus prefrontal/parietal activity -> lower probability of detection",
    "P31": "higher pre-stimulus posterior excitability or posterior-V1/V2 synchrony -> higher probability of detection",
    "P07": "phenomenal structure has the geometry of the substrate's unfolded cause-effect structure (high-dimensional)",
    "P10": "awareness judgements vary along a single dimension nested above a high-dimensional perceptual space",
}

# exclusivity / necessity statements present in the S4 text of each prediction (quote <= 30 words)
excl = {
    "P08": "P08 (RPT): \"local recurrence is necessary and sufficient for phenomenal content; frontal ignition is not necessary\" (expected_result)",
    "P09": "P09 (HOT): necessity of dlPFC - \"PFC disruption reduces awareness or meta-d' while d' is intact\" (relation: locus; necessity)",
    "P04": "P04 (IIT): denial of PFC necessity only - \"PFC decodability not required\" (distribution_prediction); no exclusivity of posterior stated",
    "P12": "P12 (AST): necessity of TPJ for awareness attribution - \"causal disruption impairs awareness attributions\" (expected_result)",
    "P07": "P07 (IIT): identity claim - \"identity of experience with the unfolded cause-effect structure\" (source_locus); \"the identity postulate\" (auxiliary_assumptions)",
}

def exclusivity(a, b):
    parts = [excl[p] for p in (a, b) if p in excl]
    return ("yes: " + " | ".join(parts)) if parts else "no: neither S4 row states exclusivity or necessity"

COG_NO = "no"
COG_BOTH_NOT_PAIRED = ("no: both predictions were tested in Cogitate 2025 (Experiment 1) but against separate criteria; "
                       "the pair was not operationalised as one test")
COG_EXP2 = "no: preregistered as Experiment 2 (pre-stimulus prediction 4) in Melloni et al. 2023; Experiment 2 not reported in Cogitate 2025"

# ---------------------------------------------------------------------------------------------
# Explicit codings. Key = (pred_a, pred_b) with pred_a < pred_b. Fields not given default to a
# 'different' row built from the 'why' note.
# ---------------------------------------------------------------------------------------------
E = {}

def diff(a, b, why, feature="condition", shared_condition="", conf=2, cog=COG_NO):
    E[(a, b)] = dict(relation="different", shared_condition=shared_condition, shared_outcome="",
                     distinguishing_feature=feature,
                     favour_a=f"{own[a]} (bears on {a} only; does not bear on {b})",
                     favour_b=f"{own[b]} (bears on {b} only; does not bear on {a})",
                     cog=cog, conf=conf, rationale=why)

def jc(a, b, shared_condition, shared_outcome, feature, favour_a, favour_b, cog, conf, rationale):
    E[(a, b)] = dict(relation="jointly compatible", shared_condition=shared_condition, shared_outcome=shared_outcome,
                     distinguishing_feature=feature, favour_a=favour_a, favour_b=favour_b, cog=cog, conf=conf,
                     rationale=rationale)

def disc(a, b, shared_condition, shared_outcome, feature, favour_a, favour_b, cog, conf, rationale):
    E[(a, b)] = dict(relation="discriminating", shared_condition=shared_condition, shared_outcome=shared_outcome,
                     distinguishing_feature=feature, favour_a=favour_a, favour_b=favour_b, cog=cog, conf=conf,
                     rationale=rationale)

# ---- GNWT x IIT (Cogitate) -------------------------------------------------------------------
jc("P01", "P04", COG1,
   "region-wise decodability of conscious content (category, identity, orientation) from iEEG/MEG/fMRI after onset (Cogitate analysis #1)",
   "locus",
   "content decodable from PFC for task-relevant and task-irrelevant stimuli (a passes on its own criterion); PFC absence challenges a but does not confirm b",
   "content decodable from the posterior hot zone throughout the percept (b passes on its own criterion); posterior absence challenges b but does not confirm a",
   "yes: Melloni et al. 2023 prediction 2 / analysis #1 - decoding of category, identity and orientation from PFC (GNWT) and from posterior cortex sustained over duration (IIT), each with its own pass criterion",
   3,
   "Same experiment and same decoding analysis, but 'PFC decodable' and 'posterior decodable, PFC not required' can both hold; S4 notes state 'P01 and P04 can both be true; they oppose only on which locus is necessary for access', and necessity is not an observable of this design.")
diff("P01", "P05", "P01 speaks to PFC decodability after onset, P05 to the temporal profile of posterior activation; different loci and different measures, so neither prediction assigns a value to the other's observable.",
     feature="locus", shared_condition=COG1, cog=COG_BOTH_NOT_PAIRED)
diff("P01", "P06", "PFC decoding (P01) vs within-posterior synchrony (P06): different measure and different locus; no shared observable.",
     feature="connectivity", shared_condition=COG1, cog=COG_BOTH_NOT_PAIRED)
diff("P01", "P31", "Post-onset PFC decoding of suprathreshold content (Exp 1) vs pre-stimulus posterior excitability and detection of near-threshold stimuli (Exp 2): no shared condition, no shared observable.",
     feature="condition")
diff("P02", "P04", "P02 assigns a time course to PFC ignition; P04 assigns decodability and a time course to posterior cortex. Different loci; P04's 'PFC decodability not required' says nothing about PFC timing. No shared observable.",
     feature="locus", shared_condition=COG1, cog=COG_BOTH_NOT_PAIRED)
disc("P02", "P05", COG1,
     "time course of the content-specific neural response relative to stimulus onset and offset; presence of a distinct offset-locked burst; temporal generalisation between onset and offset windows (Cogitate analysis #2)",
     "timing",
     "a content-specific burst locked to stimulus offset with temporal generalisation between onset and offset bursts and minimal activity in between",
     "content-specific activation that persists for 0.5/1.0/1.5 s tracking duration, with temporal generalisation across the whole window and no separate offset event",
     "yes: Melloni et al. 2023 prediction 3 / analysis #2 (temporal dynamics) - offset ignition in PFC (GNWT) vs sustained posterior activation tracking duration with no offset event (IIT)",
     2,
     "The combination 'sustained activity tracking duration and no separate offset event' is predicted by P05 (timing_prediction) and excluded by P02 (which requires an offset ignition); caveat: P02 names PFC and P05 posterior cortex, so a PFC-phasic/posterior-sustained outcome would satisfy both - hence confidence 2, not 3.")
diff("P02", "P06", "Phasic PFC ignition timing (P02) vs within-posterior synchrony (P06): different measure and locus.",
     feature="connectivity", shared_condition=COG1, cog=COG_BOTH_NOT_PAIRED)
diff("P02", "P31", "Post-stimulus PFC ignition (Exp 1) vs pre-stimulus posterior excitability and detection (Exp 2): no shared condition or observable.")
diff("P03", "P04", "PFC-posterior synchrony (P03) vs posterior decoding (P04): different measures; both can hold.",
     feature="connectivity", shared_condition=COG1, cog=COG_BOTH_NOT_PAIRED)
diff("P03", "P05", "PFC-posterior synchrony (P03) vs duration-tracking of posterior activation (P05): different measures.",
     feature="connectivity", shared_condition=COG1, cog=COG_BOTH_NOT_PAIRED)
jc("P03", "P06", COG1,
   "content-specific synchrony pattern between cortical regions during conscious perception (which connections carry the content; Cogitate analysis #3)",
   "connectivity",
   "content-specific long-range PFC <-> category-selective posterior synchrony present when content is perceived (a passes on its own criterion)",
   "sustained content-specific short-range synchrony between category-selective areas and V1/V2 (b passes on its own criterion)",
   "yes: Melloni et al. 2023 prediction 5 / analysis #3 (functional connectivity) - PFC-posterior synchrony (GNWT) vs within-posterior synchrony (IIT), each with its own criterion",
   2,
   "Same experiment and analysis, but neither S4 row excludes the other's connection: long-range and short-range content-specific synchrony can both be present; neither prediction *predicts* the absence of the other's synchrony, so no value combination is predicted by one and excluded by the other.")
diff("P03", "P31", "Post-stimulus PFC-posterior synchrony (Exp 1) vs pre-stimulus posterior excitability (Exp 2): no shared condition or observable.")
diff("P04", "P30", "Posterior decoding of suprathreshold content (Exp 1) vs pre-stimulus fronto-parietal activity and detection (Exp 2): no shared condition or observable.")
diff("P05", "P30", "Duration-tracking of posterior activation (Exp 1) vs pre-stimulus fronto-parietal activity and detection (Exp 2): no shared condition or observable.")
diff("P06", "P30", "Within-posterior synchrony (Exp 1) vs pre-stimulus fronto-parietal activity and detection (Exp 2): no shared condition or observable.")
jc("P30", "P31", COG2,
   "probability that a near-threshold stimulus is experienced, as a function of pre-stimulus activity (region-wise)",
   "locus",
   "negative relation between pre-stimulus prefrontal/parietal activity and detection",
   "positive relation between pre-stimulus posterior excitability (or posterior-V1/V2 synchrony) and detection",
   COG_EXP2,
   2,
   "Same experiment and same outcome, but the two predictions concern different pre-stimulus signals (fronto-parietal vs posterior); the 'opposite sign' in the old register is a sign difference across loci, and a negative fronto-parietal relation plus a positive posterior relation can hold simultaneously. Neither row states that the other region's relation is absent.")

# ---- GNWT x RPT -------------------------------------------------------------------------------
jc("P01", "P08",
   "consciously seen visual stimuli without report / task relevance (P01 suprathreshold task-irrelevant; P08 near-threshold no-report - overlap approximate)",
   "prefrontal content-specific activity for consciously seen but unreported stimuli (P01: decodable in PFC for task-irrelevant stimuli; P08: frontal ignition 'not necessary')",
   "locus",
   "PFC content decoding present for task-irrelevant seen stimuli (a holds); absence would challenge a and is consistent with b but not predicted by it",
   "VAN/local recurrence at ~100-300 ms in visual cortex present for seen, absent for unseen, independent of report (b holds)",
   COG_NO, 2,
   "P08 states frontal ignition is 'not necessary', which does not predict PFC absence, so PFC decodability (P01) and local recurrence (P08) can both hold; the pair would become discriminating only under a report-independent measure of phenomenal content (P08 auxiliary: phenomenal content without access), which S4 does not provide.")
jc("P02", "P08",
   "consciously seen visual stimuli (P02 suprathreshold onset/offset; P08 near-threshold seen vs unseen - conditions differ)",
   "latency and locus of the content-specific neural correlate of a seen stimulus after onset",
   "timing",
   "PFC ignition at ~0.3-0.5 s after onset and again after offset",
   "local recurrent activity in visual cortex at ~100-300 ms present for seen, absent for unseen",
   COG_NO, 2,
   "Different windows in different regions (100-300 ms visual cortex vs 300-500 ms PFC) can both occur in the same trial; P08's 'frontal ignition not necessary' does not predict its absence, and P02 does not deny an earlier local correlate. Old register conf 3 rested on a difference of description, not of predicted value.")
diff("P03", "P08", "PFC-posterior synchrony (P03) vs local recurrent activity/VAN in visual cortex (P08): different measures; RPT's 'frontal ignition not necessary' concerns ignition, not synchrony. S4 insufficient for a shared observable.",
     feature="connectivity", shared_condition="conscious perception of visual stimuli (present vs absent / seen vs unseen; conditions differ)")
diff("P08", "P30", "Pre-stimulus fronto-parietal activity and detection (P30) vs post-onset local recurrence (P08): different observables.")

# ---- GNWT x HOT -------------------------------------------------------------------------------
diff("P01", "P09", "Correlational PFC content decoding in suprathreshold viewing (P01) vs causal dlPFC disruption and metacognitive sensitivity at matched d' (P09): different conditions and measures; both PFC-positive.", feature="condition")
diff("P02", "P09", "PFC ignition timing (P02) vs dlPFC disruption and meta-d' (P09): no shared observable.")
diff("P03", "P09", "PFC-posterior synchrony (P03) vs dlPFC disruption and meta-d' (P09): no shared observable.")
diff("P09", "P30", "Spontaneous pre-stimulus fronto-parietal activity and detection (P30) vs TMS/lesion disruption of dlPFC and meta-d' (P09): different manipulations and outcomes; both predict prefrontal state modulates awareness but no shared observable is defined in S4.")

# ---- GNWT x AST -------------------------------------------------------------------------------
diff("P01", "P12", "PFC content decoding during passive suprathreshold viewing (P01) vs TPJ activity/disruption in attention-control tasks (P12): different conditions and measures; AST's attention-control network is not stated to exclude PFC, and GNWT does not exclude TPJ. Locus difference alone gives no shared observable.", feature="locus")
diff("P02", "P12", "PFC ignition timing (P02) vs TPJ substrate (P12): no shared observable.", feature="locus")
diff("P03", "P12", "PFC-posterior synchrony (P03) vs TPJ substrate (P12): no shared observable.", feature="locus")
diff("P12", "P30", "Pre-stimulus prefrontal/parietal activity and detection (P30) vs TPJ disruption and detection loss (P12): different manipulations (spontaneous fluctuation vs causal disruption) and conditions; S4 insufficient for a shared observable.", feature="condition")

# ---- GNWT x HOSS ------------------------------------------------------------------------------
diff("P01", "P29", "PFC decoding of stimulus content (P01, suprathreshold) vs PFC decoding of the awareness state presence/absence (P29, near-threshold): different decoded variables and conditions; S4 does not state whether GNWT predicts symmetric PFC coding of absence. S4 insufficient.", feature="condition")
jc("P02", "P29",
   "consciously seen visual stimuli (P02 suprathreshold; P29 near-threshold presence reports - conditions differ)",
   "frontoparietal/prefrontal ignition on conscious detection of a stimulus",
   "timing",
   "phasic PFC ignition at onset and a second ignition at offset",
   "ignition for presence reports and none for absence reports; symmetric PFC coding of presence and absence",
   COG_NO, 2,
   "Both predict ignition for a consciously seen stimulus; P29 adds absence of ignition on absence reports and P02 adds an offset event - neither value is excluded by the other row (S4 notes: 'HOSS derives ignition rather than staking a timing window').")
diff("P03", "P29", "PFC-posterior synchrony (P03) vs frontoparietal ignition/awareness-state decoding (P29): different measures.", feature="connectivity")
diff("P29", "P30", "Pre-stimulus fronto-parietal activity and detection (P30) vs post-stimulus ignition for presence reports (P29): both near-threshold detection, but pre- vs post-stimulus observables differ.",
     feature="timing", shared_condition="near-threshold visual detection (seen vs unseen / presence vs absence reports)")

# ---- IIT x RPT --------------------------------------------------------------------------------
jc("P04", "P08",
   "consciously seen visual stimuli (P04 suprathreshold 0.5-1.5 s; P08 near-threshold seen vs unseen - conditions differ)",
   "content-specific activity in posterior/visual cortex for seen stimuli",
   "timing",
   "content decodable from the posterior hot zone sustained for the whole percept",
   "local recurrent activity in visual cortex at ~100-300 ms for seen, absent for unseen",
   COG_NO, 2,
   "Both predict posterior content-specific activity for seen stimuli (RPT's local recurrent loops lie within IIT's posterior hot zone); P08 does not state that recurrence ends at 300 ms and P04 does not deny an early recurrent phase.")
jc("P05", "P08",
   "consciously seen visual stimuli (P05 suprathreshold 0.5-1.5 s; P08 near-threshold - conditions differ)",
   "time course of content-specific activity in posterior/visual cortex after onset",
   "timing",
   "posterior activation tracks stimulus duration with no separate offset event",
   "recurrent activity at ~100-300 ms present for seen, absent for unseen",
   COG_NO, 1,
   "Compatible on S4 text (an early recurrent phase persisting for the duration satisfies both), but S4 does not state whether RPT predicts that recurrence persists for long stimuli; confidence 1 for the mismatch of conditions.")
jc("P06", "P08",
   "conscious perception of visual stimuli (P06 content present vs absent, suprathreshold; P08 seen vs unseen, near-threshold)",
   "recurrent / synchronous interaction between higher visual (category-selective) areas and V1/V2 during conscious perception",
   "timing",
   "sustained content-specific synchrony between category-selective areas and V1/V2 for the whole percept",
   "feedback/recurrent interaction in visual cortex at ~100-300 ms present for seen, absent for unseen",
   COG_NO, 2,
   "Both name the same intra-posterior loop (higher visual areas <-> V1/V2) as the correlate; they differ only in the window (sustained vs ~100-300 ms), and neither excludes the other's window.")
diff("P08", "P31", "Pre-stimulus posterior excitability and detection (P31) vs post-onset local recurrence (P08): pre- vs post-stimulus observables differ.", feature="timing")

# ---- IIT x HOT --------------------------------------------------------------------------------
diff("P04", "P09", "P04's 'PFC decodability not required' is a statement about decoding; P09 is a causal claim about dlPFC disruption and meta-d' at matched d'. S4 does not state an IIT prediction for the TMS outcome (a derived one - dlPFC disruption leaves phenomenal awareness intact if the substrate is posterior - is not in S4). S4 insufficient.", feature="locus")
diff("P05", "P09", "Duration-tracking of posterior activation (P05) vs dlPFC disruption and meta-d' (P09): no shared observable.")
diff("P06", "P09", "Within-posterior synchrony (P06) vs dlPFC disruption and meta-d' (P09): no shared observable.")
diff("P09", "P31", "Pre-stimulus posterior excitability and detection (P31) vs dlPFC disruption and meta-d' (P09): no shared observable.")

# ---- IIT x AST --------------------------------------------------------------------------------
diff("P04", "P12", "Posterior hot-zone decoding (P04) vs TPJ activity/disruption in attention-control tasks (P12): different conditions and measures; note TPJ lies within IIT's 'occipital, temporal, parietal' hot zone, so even the locus contrast is weak.", feature="locus")
diff("P05", "P12", "Duration-tracking of posterior activation (P05) vs TPJ substrate (P12): no shared observable.", feature="locus")
diff("P06", "P12", "Within-posterior synchrony (P06) vs TPJ substrate (P12): no shared observable.", feature="locus")
diff("P12", "P31", "Pre-stimulus posterior excitability and detection (P31) vs TPJ disruption and detection loss (P12): different manipulations and conditions.", feature="condition")

# ---- IIT x HOSS -------------------------------------------------------------------------------
diff("P04", "P29", "Posterior decoding of content (P04) vs prefrontal decoding of the awareness state and frontoparietal ignition (P29): different decoded variables and conditions; P04's 'PFC decodability not required' does not predict absence of PFC awareness-state coding.", feature="locus")
diff("P05", "P29", "Posterior activation tracking duration (P05, suprathreshold duration manipulation) vs asymmetric frontoparietal ignition for presence vs absence (P29, near-threshold): different loci, conditions and contrasts; old register 'distribution/timing' contrast has no shared observable.", feature="distribution")
diff("P06", "P29", "Within-posterior synchrony (P06) vs frontoparietal ignition/awareness-state decoding (P29): different measures.", feature="connectivity")
diff("P29", "P31", "Pre-stimulus posterior excitability and detection (P31) vs post-stimulus ignition for presence reports (P29): both near-threshold detection, but pre- vs post-stimulus observables differ.",
     feature="timing", shared_condition="near-threshold visual detection (seen vs unseen / presence vs absence reports)")

# ---- singles ----------------------------------------------------------------------------------
disc("P08", "P09",
     "conscious perception of a visual stimulus with prefrontal function intact vs disrupted (P08 seen vs unseen with/without report; P09 dlPFC disruption at matched d' - conditions differ)",
     "dependence of awareness of a seen stimulus on prefrontal function (P08: frontal ignition 'not necessary'; P09: dlPFC disruption reduces awareness/meta-d')",
     "locus",
     "dlPFC disruption leaves subjective awareness and meta-d' unchanged at matched d' while VAN/local recurrence is intact",
     "dlPFC disruption reduces subjective awareness / meta-d' while d' is intact",
     COG_NO, 1,
     "Opposite stated necessity claims about prefrontal cortex: the value 'awareness reduced by dlPFC disruption at matched d'' is predicted by P09 and excluded by P08 IF 'awareness/meta-d'' (P09) and 'phenomenal content' (P08) are the same variable; P08's auxiliary 'phenomenal content can exist without access/report' lets RPT reinterpret a P09 result as access - S4 cannot settle the identity of the variable, hence confidence 1 (flag for adjudication).")
diff("P08", "P12", "Local recurrence in visual cortex for seen vs unseen (P08) vs TPJ activity/disruption in attention-control tasks (P12): different observables; RPT's sufficiency claim would bear on P12 only if TPJ disruption spared local recurrence, which S4 does not state. S4 insufficient.", feature="locus")
jc("P08", "P29",
   "near-threshold visual detection, seen vs unseen (P08) / presence vs absence reports (P29)",
   "frontoparietal ignition on seen / presence trials",
   "locus",
   "local recurrence in visual cortex present for seen trials independent of report; frontal ignition may or may not occur",
   "frontoparietal ignition on presence reports and not on absence reports; symmetric PFC coding of presence/absence",
   COG_NO, 2,
   "P29 predicts ignition for presence reports; P08 states frontal ignition is 'not necessary' but does not predict its absence, so both can hold; P08's report-independence claim and P29's report-based contrast do not share a value.")
diff("P09", "P12", "dlPFC disruption reducing meta-d' at matched d' (P09) vs TPJ disruption producing neglect-like detection loss (P12): different sites, different outcomes (metacognitive sensitivity vs detection) and conditions; neither row states the other site is ineffective. S4 insufficient to equate the outcomes.", feature="locus")
diff("P09", "P29", "Causal dlPFC disruption and meta-d' (P09) vs correlational PFC coding of the awareness state and ignition (P29): allied prefrontal predictions with no shared observable.", feature="condition")
diff("P12", "P29", "TPJ substrate in attention-control tasks (P12) vs frontoparietal ignition / PFC awareness-state coding in near-threshold detection (P29): different conditions and measures; P29's frontoparietal network is not stated to exclude TPJ.", feature="locus")

# ---- M6 ---------------------------------------------------------------------------------------
diff("P07", "P10", "P07 concerns the geometry (dimensionality) of phenomenal structure itself, identified with the substrate's unfolded cause-effect structure; P10 concerns the dimensionality of the awareness judgement, explicitly nested ABOVE a high-dimensional perceptual space. HOSS thus grants high-dimensional content; IIT's identity claim does not address the awareness-judgement axis. S4's own distinguishing_feature says 'adjudication needed on whether the two claims address the same variable'. S4 insufficient -> different.",
     feature="magnitude",
     shared_condition="perception tasks (P07 'any system with a definable substrate' nominally includes P10's perception/imagery/reality-monitoring tasks)")

# ---------------------------------------------------------------------------------------------
rows = []
for d in ("M8", "M6"):
    ids = sorted(stated[stated.quantity_id == d].id)
    for a, b in itertools.combinations(ids, 2):
        if theory[a] == theory[b]:
            continue
        e = E[(a, b)]
        rows.append(dict(
            pair_id=f"{d}-{a}-{b}", pred_a=a, pred_b=b, theory_a=theory[a], theory_b=theory[b], domain_id=d,
            shared_condition=e["shared_condition"], shared_outcome=e["shared_outcome"], relation=e["relation"],
            distinguishing_feature=e["distinguishing_feature"],
            what_result_would_favour_a=e["favour_a"], what_result_would_favour_b=e["favour_b"],
            exclusivity_stated=exclusivity(a, b), cogitate_operationalised=e["cog"],
            pair_confidence=e["conf"], pair_confidence_rationale=e["rationale"],
            in_old_distinguishable_from="yes" if b in [x.strip() for x in reg.loc[reg.id == a, "distinguishable_from"].iloc[0].split(";")] else "no",
            s4_row_confidence_a=rowconf[a], s4_row_confidence_b=rowconf[b],
            coder="first coder, reading assistant",
        ))
pr = pd.DataFrame(rows)
assert len(pr) == 55, len(pr)
assert set(E) == set(zip(pr.pred_a, pr.pred_b)), set(E) ^ set(zip(pr.pred_a, pr.pred_b))
assert pr.relation.isin(["different", "jointly compatible", "discriminating", "incompatible"]).all()
assert ((pr.relation == "different") == (pr.shared_outcome == "")).all()
pr.to_csv("pair_register.csv", index=False)
print(pr.groupby(["domain_id", "relation"]).size())
print(pr.groupby(["relation", "pair_confidence"]).size())
print(pr[pr.in_old_distinguishable_from == "yes"][["pair_id", "relation", "pair_confidence"]].to_string(index=False))
