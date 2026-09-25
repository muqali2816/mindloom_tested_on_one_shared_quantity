# S1 full-text reading log (first coder's reading assistant)

Scope: the 57 Table S1 cells listed in `S1_cells_to_read.csv` (all `evidence_status = abstract-only` at the time of reading). Codebook v2.5 §3 rules applied; no definition changed. Reading method: each full text (`fulltext/*.txt`) was indexed by domain-specific keyword sweeps covering the whole text (body, boxes, figure legends, footnotes; reference lists excluded) and every hit passage was read in context, together with the sections named below. This is a targeted reading, not a line-by-line linear read of every paragraph; passages with no keyword match for a domain were not read for that domain.

Unavailable sources: 10.1017/s0140525x12000477 (Clark 2013) — PP M1 marked 'source still unavailable', cell unchanged. 10.1016/j.tics.2019.06.009 (Brown, Lau & LeDoux 2019) — HOT M6 read on Lau & Rosenthal 2011 only and marked partial.

Note on inputs: the task text describes the 57 cells as 27 EXPLICIT/INTERPRETED + 30 NOT_LOCATED; the file actually holds 8 EXPLICIT, 19 INTERPRETED, 29 NOT_LOCATED and 1 NOT_APPLICABLE (PFT M8). All 57 were processed.

## Sources read

| Source | DOI | Cells | Sections read |
|---|---|---|---|
| Wilterson et al. 2020 | 10.1016/j.pneurobio.2020.101844 | AST M7 | Abstract, §1 Introduction, §5 General discussion (relation to GW and HOT); whole text keyword-indexed. |
| Kelly et al. 2014 | 10.1073/pnas.1401201111 | AST M8 | Abstract, Introduction, Results (fMRI social attribution; visual detection TMS experiment, Fig. 6), Discussion. |
| Webb & Graziano 2015 | 10.3389/fpsyg.2015.00500 | AST M8 | Whole text keyword-indexed for regions/lesions; 'Attention Schema Theory' section and Fig. 1B passage read. Names no cortical region. |
| Mashour et al. 2020 | 10.1016/j.neuron.2020.01.026 | GNWT M1, M3, M6, M4a, M4b, M4c | Hypothesis; Simulations of the Global Workspace; SDT passage; Attention/working memory; Sleep; Anaesthesia; Theory comparison; Future Directions; Conclusions. Keyword sweeps for all six domains. |
| Dehaene et al. 2006 | 10.1016/j.tics.2006.03.007 | GNWT M2, M5 | Taxonomy, Fig. 1 and Fig. 2 legends, 'Accounting for conflicting behavioural data' (Gratton effect passage). Keyword sweeps for conflict and autonomic/coherence terms. |
| Shea & Frith 2019 | 10.1016/j.tics.2019.04.007 | GNWT M7 | Abstract, Two Rival Theories, Our Hypothesis and A Simple Model, Confidence and cognitive load, Automatic Error Detection, Concluding Remarks. |
| Lau & Rosenthal 2011 | 10.1016/j.tics.2011.05.009 | HOT M1, M2, M5, M6, M7, M8, M4b | Abstract, Glossary, hierarchical model (Fig. 1), Empirically based criticisms, Box 1, Box 2, Fig. 2 legend (inattentional inflation), mismatch passage, metacognition in animals, Outstanding questions. Keyword sweeps for all seven domains. |
| Maniscalco & Lau 2012 | 10.1016/j.concog.2011.09.021 | HOT M7 | §1-2 (meta-d' definition, relation to d'), Discussion on type-1/type-2 information asymmetry. |
| LeDoux & Brown 2017 | 10.1073/pnas.1619316114 | HOT M3, M4a, M4c (and M4b, see below) | Abstract, Defensive survival circuit view, Panksepp/Damasio critique (body feedback passage), Higher-Order Theory of Emotional Consciousness and Fig. 5 (HOTEC), Conclusions. |
| Park & Tallon-Baudry 2014 | 10.1098/rstb.2013.0208 | NSF M1, M2, M3, M7, M4a, M4c | Abstract, §1, §2a-c (definition and properties of the frame; rooting in visceral signals), §3 (HER, heartbeat perception), §5 Conclusion. |
| Azzalini et al. 2021 | 10.1523/jneurosci.1932-20.2021 | NSF M3 | Abstract, Significance, Introduction, Discussion (specificity of HER-value coupling; no interaction with perceptual evidence). |
| Tallon-Baudry et al. 2018 | 10.1016/j.cortex.2017.05.019 | NSF M5, M4b | Abstract, §1, §2.3-2.4 (HER vs bodily state, arousal, criterion), §3 (self-specifying signals), §4 (integration of content with first-person perspective; stomach). |
| Tallon-Baudry 2022 | 10.1016/j.tics.2022.09.002 | NSF M6 | Entire two-page piece read. |
| Park et al. 2014 (Nat. Neurosci.) | 10.1038/nn.3671 | NSF M8, M4b | Introduction, Results (HER clusters rIPL/vACC, Table 1; bodily parameters; pupil and alpha controls), Discussion. |
| Heredia Cedillo, Lambert & Morsella 2024 | 10.3390/bs14040337 | PFT M2 | §2 (conflicts at action selection perturb the field), §3 Encapsulation ('operates blindly, whether there is conflict or not'), §4 (somatic vs autonomic nervous system). |
| Morsella et al. 2015 (BBS target article) | 10.1017/s0140525x15000643 | PFT M2; SIT M1, M4a | Target article only (first ~20% of file; commentaries excluded from quotation): §2.4 (conscious conflicts and incompatible plans), §3 (creature in the cave; urge to eat), §4 (continuous feed), notes 8-10. |
| Morsella, Godwin & Jantz 2016 (BBS reply) | 10.1017/s0140525x15002812 | PFT M3, M8 | Abstract, R1-R2, R4-R5 (contents as tokens; emotion), R8 (clues on neural correlates). |
| Joffily & Coricelli 2013 | 10.1371/journal.pcbi.1003094 | PP M3 | Abstract, Introduction, Models (valence definition), Discussion (compatibility with conscious-presence model). |
| Seth 2013 | 10.1016/j.tics.2013.09.007 | PP M3 (M7 check) | Abstract, Glossary, Interoceptive inference section, Outstanding questions; every sentence containing 'precision' inspected. |
| Kleckner et al. 2017 | 10.1038/s41562-017-0069 | PP M5 | Results (rich club; convergent validity task, dpIns-aMCC moderation), Discussion (affect as basic feature of consciousness; lower-dimensional feelings), Methods (HLM). |
| Seth & Tsakiris 2018 | 10.1016/j.tics.2018.08.008 | PP M6 | Abstract, 'Phenomenology of embodied selfhood' (objecthood hypothesis), Outstanding questions. |
| Garfinkel et al. 2015 | 10.1016/j.biopsycho.2014.11.004 | PP M7 | Abstract, §1.2 (three dimensions), Table 1, Results summary. |
| Seth & Friston 2016 | 10.1098/rstb.2016.0007 | PP M7 | Abstract, §2 (precision), §3 (interoceptive inference; conscious emotional experience passage), §4, Outstanding questions; precision-consciousness co-occurrence check. |
| Hohwy & Seth 2020 | 10.33735/phimisci.2020.ii.64 | PP M8 | Abstract, §1-2 (systematicity requirement), §4 (PP not itself a theory of consciousness; hierarchical precision-weighted architecture), §5 (Weilnhammer example), Conclusion. |
| Lamme 2006 | 10.1016/j.tics.2006.09.001 | RPT M1-M8, M4a-c | Whole paper: Table 1 (all rows), feedforward sweep and recurrent processing sections, neural stance and benefits, testable predictions; keyword sweeps for all domains. |
| Lamme & Roelfsema 2000 | 10.1016/s0166-2236(00)01657-x | RPT M3, M8 (all RPT domains swept) | Abstract, latency meta-analysis passage, 'Conscious vs unconscious processing' (blindsight, masking), Concluding remarks. |
| Morsella 2005 | 10.1037/0033-295x.112.4.1000 | SIT M1, M5, M6, M7, M4a, M4b | Abstract, Fig. 1 legend, 'Predicting Consciousness: The PRISM Principle', 'General Hypotheses', epiphenomenalism section; keyword sweeps for all six domains. |
| Gray, Bargh & Morsella 2013 | 10.1007/s00221-013-3566-5 | SIT M8 | Abstract, Introduction (SIT; predictions on urges by congruency), Results (clusters; left postcentral gyrus), General discussion. |

## Summary of proposed changes

| Direction | n | Cells |
|---|---|---|
| unchanged | 45 | (45 cells; see CSV) |
| stronger | 7 | GNWT M1, GNWT M7, HOT M4b, RPT M7, SIT M6, SIT M4a, SIT M4b |
| weaker | 3 | GNWT M5, NSF M4a, PP M7 |
| polarity | 1 | PFT M2 |
| unavailable | 1 | PP M1 |

'stronger' = proposed code is higher on NOT_LOCATED < INTERPRETED < EXPLICIT with the same or newly assigned polarity; 'weaker' = proposed code is lower, including a move to UNRESOLVED; 'polarity' = polarity differs between current and proposed code (PFT M2 also moves INTERPRETED → EXPLICIT). Cells with `flag_for_adjudication = True` (8: GNWT M1, HOT M4b, HOT M4c, PFT M2, PP M7, RPT M7, SIT M6, SIT M4b) are those where the proposal or retained code rests on a one-step inference or a rule tension and the first coder's judgement is required; 7 of them are changed cells, HOT M4c is an unchanged cell flagged for the M4c rule tension.

## Changed cells in detail

- **GNWT M1** — NOT_LOCATED → INTERPRETED / positive (stronger, confidence 1). Stroop simulation: workspace activation rises under effortful (conflictual) execution; with ignition = access this yields a one-step inference that conflict tasks engage access more. Not a statement about the number of policies. Candidate INTERPRETED; first coder may keep NOT_LOCATED. Flag.
- **GNWT M5** — INTERPRETED / positive → NOT_LOCATED (weaker, confidence 2). Full text weakens the abstract-based INTERPRETED: the only coherence statements are cortical (parieto-frontal synchrony). No organism-wide or embodied statement exists that could anchor the inference to a cortical-autonomic metric. Propose NOT_LOCATED.
- **GNWT M7** — INTERPRETED / positive → EXPLICIT / positive (stronger, confidence 2). Full text states the prediction directly (metacognitive component always accompanies workspace content; testable via cognitive-load effects on confidence). Stronger than abstract-based INTERPRETED. Caveat: auxiliary source; GNWT proponents (Mashour 2020) do not state it.
- **HOT M4b** — NOT_LOCATED → INTERPRETED / positive (stronger, confidence 1). Not in the cell's current source, but a §5 HOT source states that body/brain arousal feedback alters GNC processing and 'may well' influence attentional control of sensory processing - a hedged mechanism by which visceral arousal modulates exteroceptive access. Candidate INTERPRETED; flag.
- **NSF M4a** — INTERPRETED / stated_null → UNRESOLVED (weaker, confidence 2). Two readings: (i) the frame is not experienced as content (basis of the current null); (ii) the source treats explicit heartbeat perception as a real, HER-related ability - interoceptive content can be accessed. The null concerns the frame, a different quantity from interoceptive content as content. Propose UNRESOLVED for adjudication.
- **PFT M2** — INTERPRETED / stated_null → EXPLICIT / positive (polarity, confidence 2). Both sources state that incompatible action plans perturb the field (positive effect on experience) AND that the field runs whether or not conflict exists (null on presence). Strongest statement rule gives EXPLICIT positive, matching the current SIT M2 code on the same source; polarity change from stated_null. Flag.
- **PP M7** — EXPLICIT / positive → INTERPRETED / positive (weaker, confidence 2). Weakens EXPLICIT: Garfinkel names the metacognitive operationalisation but 'interoceptive awareness' there is metacognitive awareness of accuracy, not conscious access; Seth & Friston state precision as control parameter and speculate on correlates, never linking precision to presence of experience. Rules give INTERPRETED. Flag.
- **RPT M7** — NOT_LOCATED → INTERPRETED / stated_null (stronger, confidence 2). Stronger than NOT_LOCATED: the source states that introspective/report measures do not determine the presence of (neurally defined) consciousness - a null on metacognitive access as index. Precision/metacognitive sensitivity not named, hence INTERPRETED stated_null. Flag.
- **SIT M6** — NOT_LOCATED → INTERPRETED / positive (stronger, confidence 1). Candidate INTERPRETED: mechanism - each supramodular response system modulates a distinct aspect of the field; inference - the number of aspects (dimensions) of experience is set by the number of active supramodular systems. Dimensionality is not named; first coder may keep NOT_LOCATED. Flag.
- **SIT M4a** — INTERPRETED / positive → EXPLICIT / positive (stronger, confidence 2). Stronger than INTERPRETED: the sources state when bodily-need/visceral-process content becomes conscious (phases requiring skeletomotor coordination) and that such content enters the field under the same rule as external objects. EXPLICIT positive.
- **SIT M4b** — NOT_LOCATED → INTERPRETED / stated_null (stronger, confidence 2). Stronger than NOT_LOCATED: cardiovascular activity is hypothesised not to modulate the phenomenal field. Access to exteroceptive content is not named (general field modulation), hence INTERPRETED stated_null. Flag.

## Observations bearing on cells outside this list

- Morsella et al. 2015 BBS note 8 states that 'no such changes accompany conflicts involving smooth muscle' — direct support for the existing EXPLICIT stated_null codes in SIT M4c and PFT M4c.
- The PFT M2 proposal (EXPLICIT positive) aligns PFT M2 with the current SIT M2 code (EXPLICIT positive) on the shared source; PFT M1 (INTERPRETED stated_null, not in this list) may warrant the same within-row check.
- Kleckner et al. 2017 states that 'interoceptive sensations are usually experienced as lower-dimensional feelings of affect' — relevant to PP M6 as a second anchor.
- Lau & Rosenthal 2011 hedge for HOT M8: 'some higher-order theories do not hold that conscious awareness is invariably associated with increased prefrontal activity'; worth recording in the S4 register entry.
- Tallon-Baudry et al. 2018 specify that the M4b modulator is the cortical response to the heartbeat, independent of measured bodily state — the S4 register wording for NSF M4b should not say 'cardiac phase'.

## Evidence-status consequence

Reading the full text clears `provisional` for the 56 cells read (55 fully, HOT M6 partially); PP M1 remains provisional. Codes themselves change only after the first coder accepts a proposal.