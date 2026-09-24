# Source verification v4 — contested sources (track «Литература»)

Manuscript brainsci-4583950, round 1 revision. Each section records: DOI(s); `evidence_status` (full_text = the body text was read; abstract_only = only the abstract/PubMed record could be read; accepted_prior_verification = verified by another reviewer, DOI recorded only); what the paper actually claims (own words); the exact passage(s) read; and the sentence(s) the manuscript may use. Where the manuscript's current wording (manuscript_v3.md) goes beyond what was read, this is stated. Nothing here modifies manuscript prose; that is a later phase.

Access notes. All DOIs resolved through CrossRef. Full texts came from PMC, publisher PDFs (PLOS, Cambridge, Frontiers), the Sussex repository (Seth 2013 author manuscript) and arXiv (Fleming 2020, v3 preprint of the published article). Four items could be read only as abstracts: Morsella 2005 (the PhilPapers/PhilArchive open-access copy returned HTTP 403 to automated requests), Lau & Rosenthal 2011, Lamme 2006, Lamme & Roelfsema 2000 (all closed access, no open copy listed by Unpaywall/OpenAlex/Semantic Scholar), Park & Tallon-Baudry 2014 (PMC record without OA body) and Azzalini et al. 2019 (the HAL deposit hal-02355098 labelled as this paper contains a different manuscript — Rutishauser, «Testing models of human declarative memory at the single-neuron level» — so the deposit is unusable). Counts of sources by evidence status are computed in source_verification_v4.csv.

---

## 0. Accepted from prior verification (DOI recorded only)

| Source | DOI | Note carried over |
|---|---|---|
| Maniscalco & Lau 2012, *Consciousness and Cognition* 21, 422–430 | 10.1016/j.concog.2011.09.021 | 30 participants (Methods) |
| Bor, Schwartzman, Barrett & Seth 2017, *PLoS ONE* 12, e0171793 | 10.1371/journal.pone.0171793 | replication of Rounis et al. 2010 found no metacognitive impairment; methodological differences from the original |
| Huber, Payne & Puto 1982, *Journal of Consumer Research* 9, 90 ff. (CrossRef lists the first page only) | 10.1086/208899 | decoy (asymmetric dominance) effect exists; the paper says nothing about consciousness |

`evidence_status`: accepted_prior_verification for all three.

---

## 1. Ruby, Maniscalco & Peters 2018 and Bor, Barrett, Schwartzman & Seth 2018 — the dispute is open

**Ruby, E.; Maniscalco, B.; Peters, M.A.K. On a 'failed' attempt to manipulate visual metacognition with transcranial magnetic stimulation to prefrontal cortex. *Consciousness and Cognition* 2018, 62, 34–41.** DOI 10.1016/j.concog.2018.04.009. `evidence_status`: full_text (PMC).

What the paper claims (own words). Ruby et al. argue that Bor et al. (2017) changed the design of Rounis et al. (2010) in ways that lowered the chance of a positive finding (between-subjects design in Experiment 1; an unusual 'double-repeat' within-subjects design in Experiment 2; confidence instead of visibility ratings; no instruction to use the two rating levels evenly), that Bor et al.'s data showed the Rounis-type interaction before roughly 30 per cent of participants were excluded, and that the exclusion criteria, in simulations, did not lower false-positive rates. Putting Bor et al.'s 'positive-then-null' pattern into Bayes' rule with a 0.5 prior, they compute a posterior probability of 0.7542 that TMS to PFC impaired metacognition in Bor et al.'s sample. They also cite lesion and inactivation studies as converging evidence.

Passages read (verbatim).
- Abstract: «Despite that, their results appeared initially consistent with the effect reported by Rounis et al., but the authors subsequently claimed it was necessary to discard ~30% of their subjects, after which they reported a null result. Using computer simulations, we found that, contrary to their supposed purpose, excluding subjects by Bor et al.'s criteria does not reduce false positive rates.»
- Bayesian analysis: «Putting these values into Bayes' rule (Equation 1), we find that the probability of TMS actually causing metacognitive deficits at the population level given that an effect was observed but then disappeared to be high, p(e|d) = .7542.»
- Discussion: «Most importantly, upon seeing the pattern of results in Bor et al.'s Experiment 1 (positive result turned negative after exclusion), we showed with Bayesian analysis that the correct interpretation should be to conclude that the effect is very likely to be present, contrary to their claims.»

**Bor, D.; Barrett, A.B.; Schwartzman, D.J.; Seth, A.K. Response to Ruby et al: On a 'failed' attempt to manipulate conscious perception with transcranial magnetic stimulation to prefrontal cortex. *Consciousness and Cognition* 2018, 65, 334–341.** DOI 10.1016/j.concog.2018.07.011 (preprint 10.31234/osf.io/rhvtq). `evidence_status`: full_text (PMC).

What the paper claims (own words). Bor et al. reject the Bayesian re-analysis on the ground that its prior rests on data they consider invalid (obtained without participant exclusion), argue that once only 'valid' data are considered both Rounis et al. and Bor et al. yield null results, and note that Rahnev et al. (2016) found TMS to prefrontal cortex *enhanced* metacognition, so any reasonable prior would be far from 0.5. They maintain that the evidence so far does not demonstrate that theta-burst TMS to PFC disrupts visual metacognition and stress that the outcome of each study depends on the fine details of methods and analyses. They call for open data and simulation code and for further studies.

Passages read (verbatim).
- §2.3: «We are not compelled by this logic since we have argued that the results found in Rounis et al. are based on invalid data (i.e., data obtained without subject exclusion). It therefore seems arbitrary and unjustified to assign any Bayesian prior (including a neutral prior of 0.5) to the probability that the effect found in that study is true.»
- §3 Conclusions: «In summary, we continue to think the evidence so far, across studies, does not (so far) demonstrate that theta-burst TMS to prefrontal cortex can disrupt visual metacognition. Moreover, the findings from each study depend on the fine details of methods and analyses.»

Sentences the manuscript may use.
- «Whether theta-burst TMS to dorsolateral prefrontal cortex impairs metacognitive sensitivity remains disputed: Rounis et al. [135] reported an impairment, Bor et al. [new] did not replicate it with a modified design, Ruby et al. [new] argued that Bor et al.'s own pre-exclusion data and a Bayesian re-analysis favour the effect, and Bor et al. [new] replied that the prior of that re-analysis rests on data they consider invalid. Neither side has conceded.»
- Not licensed by the sources: any sentence stating that the Rounis effect has been «refuted» or «confirmed».

`claim_supported` (that the dispute is open and unresolved): yes.

---

## 2. Hall, Johansson & Strandberg 2012 — what was measured

**Hall, L.; Johansson, P.; Strandberg, T. Lifting the Veil of Morality: Choice Blindness and Attitude Reversals on a Self-Transforming Survey. *PLoS ONE* 2012, 7, e45457.** DOI 10.1371/journal.pone.0045457. `evidence_status`: full_text (publisher PDF).

What the paper claims (own words). 160 volunteers recruited in a park rated 12 moral principles (condition one, N = 81) or 12 current moral issues (condition two, N = 79) on a 9-point scale; a paper-slip trick then reversed two of their own ratings. Outcome measures were (a) whether the reversal was detected concurrently (spontaneous detection) or claimed retrospectively in the debriefing, and (b) whether, when asked to explain, participants argued for the reversed position. The majority of manipulated trials went undetected; in the authors' words 69 per cent of participants accepted at least one of the two reversals, and 53 per cent argued unequivocally for the opposite of their original attitude in at least one manipulated trial. There is no delayed re-test and no follow-up; the persistence of the reversed attitude is raised only as a counterfactual speculation in the Discussion.

Passages read (verbatim).
- Measures: «All manipulated trials were categorized as either corrected or accepted. In the trials categorized as corrected, the participants either noticed the change immediately after reading the manipulated statement (spontaneous detection), or claimed in the debriefing session to have felt something to be wrong when reading the manipulated sentence (retrospective correction).»
- Discussion (first sentence): «It is easy to summarize the present study; participants express their moral opinions, then moments later many of them are blind to the mismatched outcome and endorse the opposite view.»
- Discussion (the only passage on persistence): «For all we know, had the participants not been debriefed at the end of the experiments, the attitudes we registered in the manipulation trials might had lived on to become persistent features of their ideology.»

Comparison with manuscript_v3.md (§ on reconstruction, reference [182]): the manuscript states that «switching participants' own answers in a moral survey shifted the attitudes themselves, durably [182]». The word «durably» is not supported: the study measured immediate detection and immediate argumentation within the same session and explicitly frames persistence as an untested possibility.

Sentences the manuscript may use.
- «When two of their own ratings on a moral survey were reversed by a paper-slip trick, most participants failed to detect the reversal, and about half argued for the position opposite to the one they had given moments earlier [182]; the study measured immediate acceptance and justification, not the durability of the altered attitude.»
- Not licensed: «shifted the attitudes themselves, durably».

`claim_supported`: partly (immediate reversal and justification: yes; durability: no).

---

## 3. Morsella, Godwin, Jantz, Krieger & Gazzaley 2016 (BBS) — §2.4 on smooth-muscle / autonomic integration

**Morsella, E.; Godwin, C.A.; Jantz, T.K.; Krieger, S.C.; Gazzaley, A. Homing in on consciousness in the nervous system: An action-based synthesis. *Behavioral and Brain Sciences* 2016, 39, e168.** DOI 10.1017/S0140525X15000643 (CrossRef issue date 2015; printed volume 39, 2016). `evidence_status`: full_text (publisher PDF; target article, commentaries and authors' response).

What the text does and does not say. §2.4 states that consciousness is unnecessary for integrations involving smooth-muscle effectors (peristalsis, pupillary reflex) and for perceptual-level integrations, and necessary for integrating multiple inclinations toward the skeletomotor output system. It is a claim about the *function* of the conscious field (what it is for), not a denial that bodily states are experienced: the target article names «tooth pain» and «urges to scratch an itch» among the most basic conscious contents (§1), and the authors' response acknowledges awareness of hunger-type cravings while insisting that the *conflict* in salivation or the pupillary reflex is not experienced. In the response the authors explicitly decline Seth's invitation to extend the theory to the autonomic nervous system, on grounds of falsifiability and evidential weight — they do not argue that autonomic events are never felt.

Passages read (verbatim).
- §2.4: «Integrations involving smooth muscle effectors (e.g., in peristalsis or in the pupillary reflex), too, can occur unconsciously (Morsella et al. 2009a), as can another form of integration known as efference binding (Haggard et al. 2002).»
- §2.4: «This form of integration has been distinguished from unconscious integrations/conflicts, such as the McGurk effect and smooth muscle conflicts (e.g., in the pupillary reflex). In short, conflicts at the stage of processing of action selection are experienced consciously, whereas conflicts at perceptual stages of processing are unconscious.»
- §2.4: «From this standpoint, the conscious field is unnecessary to integrate perceptual-level processes (as in feature binding or intersensory conflicts), smooth muscle processes (e.g., pupillary reflex; Morsella et al. 2009a), or processes associated with motor control (discussed in sect. 3.1 below). Instead, the conscious field is necessary to integrate what appear to be multiple inclinations toward the skeletomotor output system, as captured by the principle of Parallel Responses into Skeletal Muscle (PRISM; Morsella 2005).»
- §1 (basic contents): «one should focus not on high forms of consciousness (e.g., "self-consciousness"), but on the most basic forms of consciousness (e.g., the experience of a smell, visual afterimages, tooth pain, or urges to scratch an itch).»
- Authors' response, on Seth's commentary: «Thus, in response to Seth, the integration achieved through conscious processing is intimately related, not to perceptual processing, smooth muscle control, or motor control, but to skeletomotor action selection. Simply put, PFT explains that consciousness is for voluntary action.»
- Authors' response: «(For example, Seth astutely recommends that we extend PFT to include effects upon the autonomic nervous system.) We believe that, first, our restriction renders the framework more falsifiable and fecund, and, second, the majority of the strongest bits of evidence corroborates it.»
- Authors' response: «Consistent with PFT, because conflicts involving salivation (or the pupillary reflex) do not involve the skeletomotor output system, one is oblivious about their existence.»
- Seth's commentary (e196, «Infer yourself: Interoception and internal 'action' in conscious selfhood»): «a narrow focus on skeletomotor control neglects the contributions to conscious selfhood and subjectivity that rest on interoception and autonomic regulation (internal "action").»

Comparison with manuscript_v3.md (Abstract): «supramodular interaction theory denies what interoceptive-inference accounts assert». What SIT/PFT denies is that smooth-muscle/autonomic *conflict* is integrated by, or experienced through, the conscious field; it does not deny bodily feelings. Whether this is opposed to interoceptive inference depends on what interoceptive inference asserts about autonomic-only conflict (see item 5): the two sets of statements are about different propositions unless the interoceptive-inference side is read through the author-derived P24.

Sentences the manuscript may use.
- «Passive frame theory holds that the conscious field is unnecessary for integrations carried out by smooth-muscle effectors — peristalsis, the pupillary reflex — and necessary only for integrating multiple inclinations toward the skeletomotor output system [39]; its authors declined to extend the theory to the autonomic nervous system when invited to do so [39, response to Seth].»
- «The theory excludes autonomic conflict from the function of consciousness; it does not deny that bodily states such as pain or urges are experienced [39, §1].»
- Not licensed: «SIT denies bodily feelings» or «SIT predicts no interoceptive content».

`claim_supported` (that §2.4 excludes smooth-muscle/autonomic integration from the field's function): yes. (That the text denies bodily feelings): no.

---

## 4. Cogitate Consortium 2025 (Nature) and Melloni et al. 2023 (PLoS ONE protocol) — divergent GNWT vs IIT predictions and their outcomes

**Melloni, L.; Mudrik, L.; Pitts, M.; Bendtz, K.; Ferrante, O.; Gorska, U.; et al. An adversarial collaboration protocol for testing contrasting predictions of global neuronal workspace and integrated information theory. *PLoS ONE* 2023, 18, e0268577.** DOI 10.1371/journal.pone.0268577. `evidence_status`: full_text (publisher PDF).

**Cogitate Consortium; Ferrante, O.; Gorska-Klimowska, U.; Henin, S.; Hirschhorn, R.; Khalaf, A.; et al. Adversarial testing of global neuronal workspace and integrated information theories of consciousness. *Nature* 2025.** DOI 10.1038/s41586-025-08888-1. `evidence_status`: full_text (PMC).

Divergent predictions as preregistered (Melloni et al. 2023 list five; the Nature paper tests three of them as critical). Verbatim from the protocol, «Differential predictions of the theories»:
1. Location of NCC — «GNW posits that every conscious experience is accompanied by activation of a fronto-parietal network in tandem with high-level sensory cortices. In contrast, an auxiliary prediction of IIT states that the NCC is primarily localized to the posterior hot zone.»
2. Decoding content — GNW: content «should be present both in the prefrontal-parietal network and high-level sensory cortices»; IIT: «the contents of consciousness should be maximally decodable from posterior areas.»
3. Temporal dynamics — GNW: «all experiences, regardless of their duration, are accompanied by an initial ignition … This activity, however, need not stay sustained»; «a brief ignition is also expected at the offset of the stimuli»; IIT: «the physical substrate of consciousness should persist over the duration of a conscious experience.»
4. Pre-stimulus activity — GNW: higher prestimulus fronto-parietal activity should reduce the chance a new stimulus is experienced; IIT: higher pre-stimulus excitability or synchrony in posterior category-specific areas should increase it. (Experiment 2; not reported in the 2025 paper.)
5. Functional connectivity — «GNW predicts increased neural synchronization between nodes of the prefrontal cortex and category selective areas»; IIT «posits increased neural synchr[onization]» between posterior category-selective areas and early sensory areas.

Outcomes in Cogitate 2025 (verbatim where possible).
- Prediction 1 (decoding of conscious content). Posterior ROIs: «face–object decoding showed significant cross-task generalization (more than 95% accuracy) for the approximate duration of the stimulus». PFC ROIs: «significant cross-task face–object decoding accuracy (approximately 70%) was also evident, but the temporal generalization of this decoding was restricted to approximately 0.2–0.4 s». «In PFC ROIs, identity information was absent for all categories across analysed time windows». «adding prefrontal ROIs did not improve—and in some cases reduced—category and orientation decoding». Extended Data Fig. 7 summary: for GNWT, «a partly supported one, given the inconclusive result for orientation (of global broadcasting of information in the PFC)».
- Prediction 2 (maintenance over time). Posterior: «25 electrodes (out of 657) measured sustained activity tracking stimulus duration … consistent with IIT's»; «just 15% (8 of 53) of face-selective electrodes showed sustained activity as predicted by IIT, suggesting a sparse neural substrate». PFC: «99 and 24 electrodes showed non-selective and category-selective onset responses, respectively … However, none of the 655 electrodes measured the temporal profile predicted by GNWT (that is, onset and offset).» «In PFC ROIs, cross-temporal RSA revealed transient face–object categorical representation at stimulus onset, but not at stimulus offset.» Discussion: «although IIT passed the predefined criteria for the duration prediction (number 2), there was no evidence for a sustained representation of orientation». «For GNWT, the most substantial challenge based on our preregistered criteria pertains to its account for the maintenance of a conscious percept over time and, in particular, the lack of ignition at stimulus offset.»
- Prediction 3 (interareal connectivity). «The results of the preregistered PPC metric for prediction 3, critical for both IIT and the GNWT, supported neither theory.» With the DFC metric: «In contrast to the predictions of IIT, the observed connectivity was brief.» Discussion: «For IIT, the lack of sustained synchronization within posterior cortex represents the most direct challenge, based on our preregistration.»
- Overall (Extended Data Fig. 7 caption): «For IIT, the results mix a passed prediction (content-specific complex of neural units in posterior cortex, throughout the persistence of a percept, independent of the task) with a failure (maximum integrated information). For GNWT, the results consisted of a mixture of a partly challenged prediction (of an all-or-none threshold and amplification of information updating the content of consciousness in PFC) and a partly supported one».
- Abstract: «These results align with some predictions of IIT and GNWT, while substantially challenging key tenets of both theories.»

Basis for «M8 contested at the level of locus/timing». The protocol's own framing (abstract): the experiments «test contrasting predictions of these theories concerning the location and timing of correlates of visual consciousness». The Nature paper: «our study focuses on brain regions where the predictions diverge most notably—posterior cortex for IIT and PFC for GNWT». The theories therefore agree that there is a cortical signature of conscious content (the M8 column is shared) and disagree on its locus (posterior hot zone vs PFC), its temporal profile (sustained vs onset/offset ignition) and its connectivity pattern (short-range posterior vs long-range fronto-posterior). Both theories had at least one preregistered prediction passed and at least one failed; neither was adjudicated over the other.

Sentences the manuscript may use.
- «Cogitate tested three preregistered predictions on which GNWT and IIT diverge — where content is decodable (PFC vs posterior cortex), how it is maintained (onset–offset ignition vs sustained posterior activity) and which connectivity carries it (fronto-posterior vs within-posterior). Each theory passed at least one criterion and failed at least one: IIT passed the duration prediction and failed sustained posterior synchrony; GNWT found PFC category decoding but no ignition at stimulus offset and no identity information in PFC [Cogitate 2025; Melloni 2023].»
- «The M8 column is shared at the level of the quantity — a cortical signature of conscious content — and contested at the level of locus, timing and connectivity.»

`claim_supported`: yes.

Note on P01–P06 (Table S4). P04's status «passed for category and duration, not for sustained orientation» and P05 «passed», P02 «challenged (no offset ignition found)», P06 «challenged (absent)» are consistent with the text read. P01 («content decodable in PFC, for task-irrelevant stimuli as well») should carry the outcome: category decodable in PFC (about 70 per cent, 0.2–0.4 s), identity absent, orientation inconclusive — «partly supported». P03 («PFC–posterior synchrony carries the content»): the preregistered PPC metric supported neither theory; DFC found content-selective synchrony in the PFC ROI in iEEG and brief alpha–beta DFC in MEG — record as «inconclusive / not supported by preregistered metric».

---

## 5. Seth 2013 (TICS) and Seth & Friston 2016 (Phil Trans B) — does interoceptive inference say anything about conflict resolved purely by autonomic effectors (P24)?

**Seth, A.K. Interoceptive inference, emotion, and the embodied self. *Trends in Cognitive Sciences* 2013, 17, 565–573.** DOI 10.1016/j.tics.2013.09.007. `evidence_status`: full_text (author accepted manuscript, Sussex repository; page numbers differ from the print version).

**Seth, A.K.; Friston, K.J. Active interoceptive inference and the emotional brain. *Philosophical Transactions of the Royal Society B* 2016, 371, 20160007.** DOI 10.1098/rstb.2016.0007. `evidence_status`: full_text (PMC).

What is stated. Both papers propose that subjective feeling states (emotions) arise from actively inferred generative models of the causes of interoceptive afferents, and that interoceptive predictions regulate the body by enslaving autonomic reflexes, in exact analogy to proprioceptive predictions enslaving motor reflexes. Seth & Friston 2016 explicitly leave open which aspects of inference support *conscious* emotional experience, offering only a speculation that deep, domain-general expectations at higher hierarchical levels are candidates. In Seth 2013 the word «conflict» occurs 4 times, always meaning conflict between predicted and actual signals or between sensory modalities (multisensory conflict in the rubber-hand illusion); in Seth & Friston 2016 it occurs once, in a reference title. Neither paper contains any statement about a scenario in which two incompatible demands are resolved by autonomic effectors alone, nor any statement about whether such a scenario is or is not accompanied by a feeling. The word «skeletomotor»/«skeletal» does not occur in either paper.

Passages read (verbatim).
- Seth 2013, abstract: «'interoceptive inference' conceives of subjective feeling states (emotions) as arising from actively-inferred generative (predictive) models of the causes of interoceptive afferents.»
- Seth 2013: «Sympathetic and parasympathetic outflow from the AIC and ACC are in the form of interoceptive predictions that enslave autonomic reflexes (e.g., heart/respiratory rate, smooth muscle behaviour), just as proprioceptive predictions enslave classical motor reflexes in PC formulations of motor control [9].»
- Seth 2013, Concluding remarks: «Subjective feeling states (emotional experiences) arise from active interoceptive inference».
- Seth & Friston 2016: «An important challenge in this context is to identify which aspects of inference support specifically conscious emotional experience, with predictions (rather than prediction errors) being the preferred vehicle [32]. It is tempting to speculate that deep expectations at higher levels of the neuronal hierarchy are candidates for—or correlates of—conscious experience, largely because their predictions are domain general and can therefore be articulated (through autonomic or motor reflexes).»
- Seth & Friston 2016: «The resulting prediction error then drives sympathetic or parasympathetic effector systems to ensure homoeostasis or allostasis, for example, sympathetic smooth-muscle vasodilatation as a reflexive response to the predicted interoceptive consequences of 'blushing with embarrassment'.»

Stated vs derived. Stated: feelings are inferences over interoceptive causes; autonomic reflexes are the effectors of interoceptive predictions; which inferences are conscious is an open question. Derived by the manuscript authors (P24, Table S4: «unresolved interoceptive prediction error yields a feeling»): this is not stated in either paper. Seth & Friston 2016 in fact name predictions, not prediction errors, as «the preferred vehicle» for conscious emotional experience, which points against the derivation as phrased. P24 must remain «author-derived, pending endorsement», and its wording should not attribute to Seth 2013 or Seth & Friston 2016 a claim about conflict.

Sentences the manuscript may use.
- «Interoceptive inference holds that subjective feeling states arise from actively inferred models of the causes of interoceptive afferents, and that interoceptive predictions regulate the body by enslaving autonomic reflexes [47, 48]; which aspects of this inference are consciously experienced is left open, with predictions rather than prediction errors proposed as the more likely vehicle [48].»
- «Neither source states what happens, experientially, when incompatible demands are resolved by autonomic effectors alone; the prediction we register as P24 is our derivation, not a stated claim of the theory.»
- Not licensed: «interoceptive-inference accounts assert that autonomic conflict is felt».

Consequence for the M4b column. The opposition «SIT denies what interoceptive inference asserts» is not established by the sources read: SIT/PFT excludes autonomic conflict from the function of the conscious field; interoceptive inference is silent on autonomic conflict. The column can be coded as EXPLICIT/null for SIT and NOT_LOCATED (or INTERPRETED, if P24 is retained with its derivation stated) for interoceptive inference; the status of the column is then an output of that coding.

`claim_supported` (that P24 is stated by the sources): no. (That the sources support the mechanism from which P24 is derived): partly.

---

## 6. Morsella 2005 (Psych Rev) and Morsella et al. 2016 (BBS) — the threshold statement (P16)

**Morsella, E. The function of phenomenal states: Supramodular interaction theory. *Psychological Review* 2005, 112, 1000–1021.** DOI 10.1037/0033-295X.112.4.1000. `evidence_status`: abstract_only (PubMed record; the open-access PhilPapers copy returned HTTP 403 to automated requests). Table S4 P16 cites this paper for the PRISM principle; the 2005 wording could not be checked and P16's `source_locus` should not name a page of the 2005 paper until it has been read.

**Morsella et al. 2016 (BBS), as in item 3.** `evidence_status`: full_text.

What the 2005 abstract states: «Supramodular interaction theory proposes that phenomenal states play an essential role in permitting interactions among supramodular response systems … Unlike unconscious processes (e.g., pupillary reflex), these processes may conflict with skeletal muscle plans, as described by the principle of parallel responses into skeletal muscle (PRISM). Without phenomenal states, these systems would be encapsulated and incapable of collectively influencing skeletomotor action.» No numerical threshold appears in the abstract.

What the 2016 text states about the threshold. The trigger is described as *two* streams of efference binding, or *incompatible* skeletomotor plans, or *multiple* inclinations; the wording alternates between «two» and «multiple» and never states a threshold above two, nor any function relating the number of inclinations to the strength of conscious involvement. What the 2016 text does say about gradation is that the *strongest* perturbations are found for *incompatible* plans and that harmonious (congruent) plans produce little perturbation, to the point that participants may not notice that more than one plan was active («synchrony blindness»). Gradation is thus stated along the compatibility axis, not along the number axis.

Passages read (verbatim, BBS 2016).
- §2.4: «Involving urges and other action-related inclinations, conscious conflicts occur when two streams of efference binding are trying to influence skeletomotor action simultaneously (Morsella & Bargh 2011).»
- §2.4: «These conscious conflicts appear to be triggered into existence by the activation of incompatible skeletomotor plans.»
- §2.4: «Instead, the conscious field is necessary to integrate what appear to be multiple inclinations toward the skeletomotor output system, as captured by the principle of Parallel Responses into Skeletal Muscle (PRISM; Morsella 2005).»
- Authors' response: «Regarding laboratory data, of the many conditions in interference paradigms, the strongest perturbations in consciousness (e.g., urges to err) are found in conditions involving the activation of incompatible skeletomotor plans (Morsella et al. 2009a; 2009c), such as in the incongruent Stroop condition or the response interference (versus perceptual interference) condition of the flanker task». «Conversely, when distinct processes lead to harmonious action plans, as when a congruent Stroop stimulus activates harmonious word-reading and color-naming plans (e.g., BLUE in blue font), there are little such perturbations in consciousness, and participants may even be unaware that more than one plan influenced overt action (e.g., uttering "blue"). This phenomenon, called synchrony blindness (Molapour et al. 2011)».

Implications for P16 and §9.1. (a) SIT/PFT does state that conscious conflict arises when two (incompatible) skeletomotor inclinations are simultaneously active — P16's «≥ 2 inclinations» is a fair reading of «two streams … simultaneously» and «multiple inclinations», provided the incompatibility qualifier is kept. (b) It states nothing about more than two; «no stated increase with further inclinations» (P16) is correct as a NOT_LOCATED, not as a prediction of no increase. (c) The passage on synchrony blindness bears directly on the reviewer's point that §9.1 confounded number of keys with congruency: the theory's own gradation runs with incompatibility, and it explicitly allows that two *compatible* plans may leave no trace in consciousness. A design that varies the number of simultaneously active plans while holding compatibility fixed tests a question the theory has not answered; a design that varies compatibility at fixed number tests what it has stated.

Sentences the manuscript may use.
- «Supramodular interaction theory and its passive-frame formulation state that conscious conflict arises when two incompatible inclinations toward the skeletomotor output system are active simultaneously [38, 39, §2.4]; they say nothing about how conscious involvement changes when more than two are active, and they state that compatible plans may co-occur without any perturbation of consciousness [39, response, on synchrony blindness].»
- Not licensed: «SIT predicts that conscious involvement grows with the number of competing plans» or «SIT predicts a step at two and no further change».

`claim_supported` (P16 as «≥ 2 incompatible inclinations trigger conscious involvement; nothing stated above two»): yes, on the 2016 text; the 2005 wording remains unread.

---

## 7. Park & Tallon-Baudry 2014 (Phil Trans B) and Azzalini, Rebollo & Tallon-Baudry 2019 (TICS) — neural subjective frame

**Park, H.-D.; Tallon-Baudry, C. The neural subjective frame: from bodily signals to perceptual consciousness. *Philosophical Transactions of the Royal Society B* 2014, 369, 20130208.** DOI 10.1098/rstb.2013.0208. `evidence_status`: abstract_only (PMC record without open body; publisher PDF returned 403).

**Azzalini, D.; Rebollo, I.; Tallon-Baudry, C. Visceral Signals Shape Brain Dynamics and Cognition. *Trends in Cognitive Sciences* 2019, 23, 488–509.** DOI 10.1016/j.tics.2019.03.007. `evidence_status`: abstract_only (the HAL deposit hal-02355098 contains a different manuscript).

**Added for verification: Park, H.-D.; Correia, S.; Ducorps, A.; Tallon-Baudry, C. Spontaneous fluctuations in neural responses to heartbeats predict visual detection. *Nature Neuroscience* 2014, 17, 612–618.** DOI 10.1038/nn.3671 (already reference [119] in manuscript_v3; cited in Table S4 P20). `evidence_status`: abstract_only (PubMed).

What is claimed (from the abstracts). The Phil Trans B opinion piece proposes the neural subjective frame: constantly updated neural maps of the body's internal state, rooted in visceral representations (posterior insula, ventral anterior cingulate, amygdala, somatosensory cortex), which constitute the first-person referential from which perceptual experience is created. It is «a low-level building block of subjective experience which is not explicitly experienced by itself which is necessary but not sufficient for perceptual experience». The Nature Neuroscience paper reports that pre-stimulus heartbeat-locked neural events in the posterior right inferior parietal lobule and ventral anterior cingulate predict detection of a faint visual grating, and that neither measured bodily parameters nor overall cortical excitability account for the effect. The TICS review states that cardiac and gastric signals shape resting brain dynamics and influence the processing of external sensory information and spontaneous cognition.

Passages read (verbatim, abstracts).
- Park & Tallon-Baudry 2014: «The neural subjective frame is a low-level building block of subjective experience which is not explicitly experienced by itself which is necessary but not sufficient for perceptual experience.»
- Park et al. 2014 (Nat Neurosci): «neural events locked to heartbeats before stimulus onset predict the detection of a faint visual grating in the posterior right inferior parietal lobule and the ventral anterior cingulate cortex … Neither fluctuations in measured bodily parameters nor overall cortical excitability could account for this finding.»
- Azzalini et al. 2019: «Cardiac signals also influence the processing of external sensory information and the production of spontaneous, internal cognition.»

M4b (heartbeat-evoked responses predicting detection). Supported by the Nature Neuroscience abstract as an empirical finding: the HER is a pre-stimulus predictor of visual detection. The Phil Trans B and TICS abstracts frame this as evidence that visceral signals shape perceptual experience. Note that, as coded in Table S4, P20 is filed under M4a; on the abstracts the finding is about a bodily signal predicting detection of an *exteroceptive* stimulus, that is, the M4b sense (interoceptive channel modulating access), not interoceptive content as content.

M4a (interoceptive content as content). The Phil Trans B abstract states the opposite: the neural subjective frame is «not explicitly experienced by itself». On the abstracts, the neural-subjective-frame account does not claim that visceral signals are experienced as content; it claims they constitute the first-person perspective from which exteroceptive content is experienced. The abstract does add that the frame «could also underlie other types of subjective experiences such as self-consciousness and emotional feelings» — a possibility, not a prediction. The body texts may contain more; they could not be read.

Sentences the manuscript may use.
- «The neural subjective frame is proposed as a first-person referential built from visceral representations that is necessary but not sufficient for perceptual experience and is not itself experienced as content [116]; the empirical anchor is that pre-stimulus heartbeat-evoked responses in right inferior parietal and ventral anterior cingulate cortex predict detection of a faint grating, independently of measured cardiac parameters and overall excitability [119].»
- Not licensed (on the abstracts): «the neural subjective frame predicts that interoceptive content is experienced as content»; page/figure loci for the 2014 Phil Trans B or 2019 TICS body text.

`claim_supported`: M4b — yes (abstract level); M4a as content — no (the abstract says the frame is not experienced by itself); reclassification of P20 from M4a to M4b recommended for the coding phase.

---

## 8. Fleming 2020 (HOSS) vs Lau & Rosenthal 2011 (HOT) — where they differ

**Fleming, S.M. Awareness as inference in a higher-order state space. *Neuroscience of Consciousness* 2020, 2020(1), niz020.** DOI 10.1093/nc/niz020. `evidence_status`: full_text (arXiv 1906.00728v3, dated 4 December 2019, the preprint of the published article; section numbering follows the preprint).

**Lau, H.; Rosenthal, D. Empirical support for higher-order theories of conscious awareness. *Trends in Cognitive Sciences* 2011, 15, 365–373.** DOI 10.1016/j.tics.2011.05.009. `evidence_status`: abstract_only (closed access).

What each claims. Lau & Rosenthal (abstract): conscious awareness «crucially depends on higher-order mental representations that represent oneself as being in particular mental states»; the paper reviews evidence distinguishing this view from first-order, global workspace and recurrent processing theories and defends it against the objections that prefrontal activity reflects attention rather than awareness and that prefrontal lesions do not abolish awareness. Fleming: awareness reports are metacognitive decisions (inference) about a generative model of perceptual content, in a factorised hierarchical state space in which an abstract one-dimensional awareness state (absent–present) sits above perceptual content; the architecture is asymmetric (many states nested under «present», few under «absent»), and this asymmetry is offered as an account of «global ignition».

Points of difference stated in Fleming 2020 (§7 «Relationship to other theories of consciousness»).
1. Scope: HOSS is offered first as a model of the computations behind *reports* of awareness — «The goal of the higher-order state-space (HOSS) approach outlined here is modest - to delineate computations supporting metacognitive reports about awareness.» Only «A stronger reading of the model is that conscious awareness and metacognitive reports depend on shared mechanisms in the human brain [43, 44]. This stronger version shares similarities with higher-order theories of consciousness, particularly Lau's proposal that consciousness involves "signal detection on the mind" [40, 45].»
2. Sufficiency and joint determination: «However, while inference on higher-order states is, on this view, necessary for awareness, it may not be sufficient. In HOSS, the higher-order awareness state is simple and low-dimensional. Lower-order states clearly must make a contribution to perceptual experience under this arrangement – a variant of the "joint determination" view advocated by Lau and Brown [48]. However it seems an empirical question as to the relative granularity of higher-order and first-order representations in terms of their contribution to conscious experience».
3. Content of the higher-order state: in HOSS the higher-order state is a one-dimensional presence/absence variable factorised from content — «the state space is factorised to allow two separate causes of the sensory data – what it is, and whether I have seen it» — whereas HOT (per the 2011 abstract) speaks of representations «that represent oneself as being in particular mental states».
4. Distinctive prediction: «HOSS predicts prefrontal involvement for active decisions about stimulus absence, whereas GWS predicts that PFC remains quiescent on such trials».
5. Mechanism: HOSS is a generative/Bayesian model with simulations; it recasts ignition «as asymmetric inference about stimulus presence rather than a consequence of stimulus content being "broadcast"».

What could not be verified: the body text of Lau & Rosenthal 2011 (their specific claims on the prefrontal locus and on meta-d′) was not read; P09 and P11 in Table S4 cite it for those claims and should carry `evidence_status` abstract_only until read.

Sentences the manuscript may use.
- «Higher-order thought theory holds that awareness depends on higher-order representations of oneself as being in a particular mental state [78]; the higher-order state-space model characterises awareness reports as metacognitive inference over a one-dimensional presence–absence state factorised from perceptual content, treats higher-order inference as necessary but possibly not sufficient for awareness, and predicts prefrontal involvement in decisions about stimulus absence [82]. The two are coded as separate rows because they differ in scope (report vs awareness), in the content of the higher-order state, and in the predictions they make about absence trials.»

`claim_supported` (that separate rows are justified by stated differences): yes, on Fleming 2020's own account of the relation; the HOT side rests on the abstract.

---

## 9. Lamme 2006 / Lamme & Roelfsema 2000 (RPT) and Graziano & Webb 2015 (AST) — locus/timing claims for M8

**Lamme, V.A.F.; Roelfsema, P.R. The distinct modes of vision offered by feedforward and recurrent processing. *Trends in Neurosciences* 2000, 23, 571–579.** DOI 10.1016/S0166-2236(00)01657-X. `evidence_status`: abstract_only.

**Lamme, V.A.F. Towards a true neural stance on consciousness. *Trends in Cognitive Sciences* 2006, 10, 494–501.** DOI 10.1016/j.tics.2006.09.001. `evidence_status`: abstract_only.

What the abstracts state. Lamme & Roelfsema 2000: «The feedforward sweep rapidly groups feature constellations that are hardwired in the visual brain, yet is probably incapable of yielding visual awareness; in many cases, recurrent processing is necessary before the features of an object are attentively grouped and the stimulus can enter consciousness.» This is a timing/processing-mode claim (feedforward insufficient; recurrent necessary) with a hedge («probably», «in many cases»); it does not, in the abstract, name a cortical locus or state sufficiency. Lamme 2006 (abstract): argues that neural and behavioural measures should be «put on an equal footing» and that neuroscience arguments «converge towards a coherent scientific definition of visual consciousness»; the abstract does not itself state the locus or timing claim.

Comparison with Table S4 P08 («local recurrence is necessary and sufficient for phenomenal content; frontal ignition is not necessary»). On the abstracts: «necessary» is supported (2000); «sufficient» and «frontal ignition is not necessary» are not present in either abstract and would need the body text (or a later source, for example Lamme 2010 *Cognitive Neuroscience* or Lamme 2018 *Phil Trans B*, DOI 10.1098/rstb.2017.0344 — abstract fetched, body not open). The Cogitate paper's own reading is that IIT's «non-core prediction 1 about the posterior cortex … is also shared by many theories (for example, recurrent processing theory 14 )».

**Webb, T.W.; Graziano, M.S.A. The attention schema theory: a mechanistic account of subjective awareness. *Frontiers in Psychology* 2015, 6, 500.** DOI 10.3389/fpsyg.2015.00500. `evidence_status`: full_text (publisher PDF). **Author order.** The published article lists Webb as first author («Citation: Webb TW and Graziano MSA (2015)»); CrossRef metadata lists Graziano first, which is how manuscript_v3 reference [84] renders it. The reference should read Webb & Graziano 2015.

What the 2015 paper claims about locus and timing: nothing. The text contains no occurrence of TPJ, temporo-parietal junction or superior temporal sulcus, and no millisecond timing claim; «parietal» occurs only in a passage about the body schema (area 5 / superior parietal lobule), and the paper's brain-basis statements are architectural («integrating information across disparate brain areas into a single, larger, brain-spanning representation»). The paper's content is the mechanism (attention schema as a model of attention) and behavioural predictions about attention control with and without awareness.

Where AST's locus claim is stated: **Graziano, M.S.A.; Kastner, S. Human consciousness and its relationship to social neuroscience: A novel hypothesis. *Cognitive Neuroscience* 2011, 2, 98–113.** DOI 10.1080/17588928.2011.565121. `evidence_status`: full_text (PMC author manuscript). Verbatim: «The present hypothesis does, however, make a clear prediction: damage to the right TPJ and STS should often be associated with a deficit in consciousness. The clinical syndrome that comes closest to an awareness deficit is hemispatial neglect». The paper makes no timing claim.

Comparison with Table S4 P12 («TPJ/STS substrate; causal disruption impairs awareness attributions; attention can be controlled without awareness but less well», source Graziano & Webb 2015; Wilterson et al. 2020). The TPJ/STS substrate is not in the 2015 paper; it is in Graziano & Kastner 2011 (and later empirical work not read here). The attention-control-without-awareness claim is in the 2015 paper («In the absence of awareness of a stimulus, the effects of that stimulus on attention and therefore on behavior cannot be regulated in line with goals or task demands as well as when the stimulus is consciously perceived.»). P12 should split its source attribution accordingly.

Sentences the manuscript may use.
- «Recurrent processing theory holds that the feedforward sweep is probably incapable of yielding visual awareness and that recurrent processing is, in many cases, necessary for a stimulus to enter consciousness [75]; the locus is thereby placed in the visual cortical hierarchy rather than in a frontal ignition, a reading shared by the Cogitate consortium [Cogitate 2025].» (The words «sufficient» and «frontal ignition is not necessary» are not licensed by the abstracts read.)
- «Attention schema theory predicts that damage to the right temporo-parietal junction and superior temporal sulcus should be associated with a deficit in awareness [Graziano & Kastner 2011]; the 2015 mechanistic account [84] adds behavioural predictions about attention control with and without awareness but no anatomical or timing claim.»

`claim_supported`: RPT locus/timing — partly (necessity of recurrence: yes; sufficiency and «no frontal ignition»: not located in abstracts); AST locus in the cited 2015 paper — no; AST locus in Graziano & Kastner 2011 — yes; AST timing — not located.

---

## Summary of issues for the coding phase (not prose changes)

1. Hall et al. 2012: drop «durably»; the study measured immediate acceptance and justification only.
2. Morsella et al. 2016 §2.4 excludes autonomic *conflict* from the function of the field; it does not deny bodily feelings. Code SIT/PFT on M4b as EXPLICIT/null for «autonomic conflict integrated by consciousness», not as a denial of interoceptive content.
3. Seth 2013 / Seth & Friston 2016 contain no statement about autonomic-only conflict; P24 is author-derived and Seth & Friston name predictions, not prediction errors, as the likelier vehicle of conscious feeling. The «contested» status of M4b is therefore not established by the sources; it is an output of the re-coding.
4. Morsella 2005 body text unread; the threshold wording is verified only from the 2016 BBS text (two incompatible streams; «multiple inclinations»; nothing above two; gradation stated along incompatibility, with synchrony blindness for compatible plans).
5. Cogitate: M8 shared at the level of the quantity, contested at locus/timing/connectivity; P01 and P03 statuses should be updated as noted in item 4.
6. Park et al. 2014 (Nat Neurosci) is an M4b finding (bodily signal predicting detection of an exteroceptive stimulus); P20 is currently filed under M4a. The Phil Trans B abstract says the neural subjective frame is «not explicitly experienced by itself».
7. Fleming 2020 states scope, sufficiency and absence-trial differences from HOT/GWS; separate rows are justified. Lau & Rosenthal 2011 body unread.
8. Webb & Graziano 2015 (author order to be corrected) carries no locus/timing claim; AST's TPJ/STS prediction is in Graziano & Kastner 2011. Lamme 2000/2006 abstracts support necessity of recurrence only.
9. Bor et al. 2017 and Huber et al. 1982 are not yet in the manuscript's reference list; Ruby et al. 2018 and Bor et al. 2018 are new. Metadata for all new DOIs is in citation_pool_additions.json.
