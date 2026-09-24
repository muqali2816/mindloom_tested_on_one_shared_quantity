# Codebook for the independent second coding (blind pack)

Manuscript: *One quantity, nine theories: what adversarial tests of consciousness are not yet able to measure* (Brain Sciences, ms. brainsci-4583950, revision round 1).
Purpose of this pack: an independent second application of the coding scheme behind Tables 1 and 2 (Supplementary Tables S1 and S2), so that inter-coder agreement (Cohen's kappa) can be reported.

**This pack is blind.** It contains the definitions, the decision rules, the theory list with primary sources, and blank forms. It does not contain the first coder's codes, justifications, or the results reported in the manuscript's §7. Please do not consult §7.3–§7.8 of the manuscript, the filled Supplementary Tables, or the first coder until both forms are returned.

---

## 1. One-page instruction

1. **Code independently.** Do not discuss cells with the first coder before the forms are returned. Do not open the manuscript's §7 results, the filled S1/S2, or any draft of the response to reviewers.
2. **Read the sources, not the summaries.** For each theory, read the primary sources listed in §5 of this codebook (3–5 per theory). You may add further sources, but each code must be anchored to a specific citable text; record it in the `source_label` / `source_doi` columns.
3. **Fill `S1_blank_for_coder2.csv` (88 rows).** For every theory × quantity cell enter exactly one code from {YES, IMPLICIT, NO, Y(neg)} in `code`, a one- or two-sentence `justification` in your own words, and the source you relied on. If the code is NO, the justification should state what you looked for and did not find. `confidence` is optional (1 = guess, 2 = defensible, 3 = certain).
4. **Fill `S2_blank_for_coder2.csv` (36 rows).** For each study enter the `content` category (§4.2) and the `theory_addressed` value (§4.1). You will need to look at the study's methods (stimuli and task), not only its abstract.
5. **Time yourself.** Record start and end times per theory block and for the S2 form in `coder2_timing_log.csv`. The time is reported in the manuscript's method section as a property of the scheme, not as an assessment of you.
6. **Do not resolve doubt by looking for the "expected" answer.** When a cell is genuinely ambiguous, choose the code the decision rules in §3 require, and flag the cell with `confidence = 1`. Ambiguous cells are exactly what the adjudication meeting is for.
7. **Return** the three CSV files. Agreement is then computed by `agreement.py` (unweighted and linearly weighted kappa, per-column kappa, disagreement list) and the disagreements are adjudicated jointly, with the adjudication record deposited alongside the tables.

Expected effort: roughly 6–10 hours for S1 and 2–3 hours for S2, spread over several sittings.

---

## 2. The eight quantities (operational definitions)

The unit of coding in S1 is a **theory × quantity cell**. The question in each cell is the same: *does this theory, in its canonical empirical formulation, make a stated prediction about how this quantity relates to conscious access or to the presence of experience?*

"Quantity" means a variable that could in principle be measured or manipulated in an experiment. The eight quantities fall into three groups.

### 2A. The arbitration situation (what the organism has to decide)

**M1 — Number of simultaneously competing action policies.**
How many distinct courses of action (motor plans, approach/avoid tendencies, response options) are simultaneously active and compete for control of the body at the moment of interest. Operationalised by task design (single-response vs multi-response conflict tasks, Stroop-type incongruence, sustained incompatible intentions) or by decoding the number of concurrently represented plans. A theory predicts over M1 if it states that conscious access, its likelihood, or its intensity changes as a function of *how many* policies compete — not merely that consciousness "involves action".

**M2 — Degree of incompatibility between competing policies.**
Given that more than one policy is active, how mutually exclusive they are: two policies that can be executed together (look and reach) versus two that cannot (inhale and exhale; move left and move right). Operationalised as effector overlap, response-set conflict, or the impossibility of joint execution. A theory predicts over M2 if it states that the *degree* of conflict between policies changes access or experience.

**M5 — Organism-wide coherence across cortical and autonomic channels.**
The extent to which cortical activity and autonomic/visceral activity (cardiac, respiratory, gastric, electrodermal, pupillary) are coupled or coordinated at the moment of access — a measurable coupling index (phase coupling, information transfer, covariance across channels), not a metaphor of "whole-organism" unity. A theory predicts over M5 if it states that conscious access or its content depends on, or is indexed by, the coherence between cortical and autonomic dynamics. Statements that consciousness is "embodied", "for the whole organism" or "serves homeostasis" are relevant to the IMPLICIT/NO decision (§3) but are not, by themselves, a stated prediction over a coherence measure.

### 2B. The content (what is accessed)

**M3 — Valence of conscious content.**
The affective sign and magnitude of the content whose access is at issue (positive/negative, threat/reward, pain/pleasure). A theory predicts over M3 if it states that valence changes access (its threshold, priority, timing or neural signature), or that valence is itself a constitutive dimension of what becomes conscious.

**M4 — Autonomic / interoceptive channel involvement.**
Whether the content originates in, or is carried by, visceral and autonomic signalling (heartbeat, respiration, gastric rhythm, arousal) rather than exteroceptive senses. A theory predicts over M4 if it states that interoceptive content is accessed differently from exteroceptive content, or that autonomic signalling modulates the access of any content. A stated prediction that interoceptive/autonomic channels make **no** difference to access is also a prediction (code Y(neg), §3).

### 2C. The format and signature of access (how it is accessed)

**M6 — Dimensionality of phenomenal space.**
The number of independent dimensions along which conscious experience can vary at a given moment (a structured, quantifiable notion: the rank or intrinsic dimensionality of the represented state, the size of the set of distinguishable experiences). A theory predicts over M6 if it states how this dimensionality is determined, how it changes with manipulations, or how it can be measured.

**M7 — Precision of metarepresentation.**
The reliability with which the system represents its own first-order states — confidence calibration, metacognitive sensitivity (e.g. meta-d′), the precision or variance of a higher-order estimate. A theory predicts over M7 if it states that the presence, degree or content of conscious experience depends on the precision of the higher-order representation, or that a metacognitive measure indexes it.

**M8 — Cortical signature of access.**
A specific, localisable neural correlate of conscious access in cortex: a region (prefrontal, posterior "hot zone", sensory cortex), a temporal marker (P3b, late ignition, recurrent feedback in a given window), or a connectivity pattern. A theory predicts over M8 if it names such a signature and states that it should be present when content is accessed and absent when it is not (or vice versa). A stated prediction that a cortical signature is **not** necessary for experience is also a prediction (Y(neg)).

---

## 3. The four codes and their decision rules

Apply the rules in order. Stop at the first that applies.

| Code | Rule |
|---|---|
| **YES** | The theory's canonical text(s) contain a stated, nameable prediction that this quantity affects (or indexes, or constitutes) conscious access or experience. You can quote or closely paraphrase the sentence and say in which direction the prediction goes. |
| **Y(neg)** | The theory's canonical text(s) contain a stated prediction that this quantity does **not** affect access or experience, or is **not** necessary for it. Same standard as YES, opposite sign. Do not use Y(neg) for silence; use it only where the negation is stated. |
| **IMPLICIT** | No stated prediction, but one could be **constructed from the theory's stated commitments without adding new machinery**: the quantity is named or clearly referred to in the theory's own vocabulary, and its relation to access follows from a principle the theory already asserts. You should be able to write the constructed prediction in one sentence and point to the commitment it follows from. |
| **NO** | The quantity is absent from the theory's predictive apparatus: it is neither named nor clearly referred to, and deriving a prediction would require adding an assumption the theory does not make. Silence, mention in passing without a mechanism, and general rhetoric ("embodied", "for the organism", "affect matters") all fall here. |

**Three boundary rules.**

- *YES vs IMPLICIT*: YES requires that the **theory** states the prediction, not that a study using the theory's paradigm happens to manipulate the quantity. A paper by the theory's authors that reports an effect of the quantity counts as YES only if the theory is invoked to predict it.
- *IMPLICIT vs NO*: the test is "no new machinery". If your constructed prediction needs an auxiliary hypothesis that the theory's authors have not themselves asserted, code NO. Apply this conservatively: when in doubt between IMPLICIT and NO, choose IMPLICIT and set `confidence = 1`. (This makes NO a lower bound on the theory's silence, which is the reading the manuscript uses.)
- *Y(neg) vs NO*: Y(neg) requires a stated negation. A theory that simply never discusses the quantity is NO, even if its architecture makes the quantity irrelevant.

**Which formulation is canonical.** For theories with several revisions, code the most recent statement that makes empirical commitments (listed first under each theory in §5). Earlier statements may be used to establish that a commitment is long-standing, but not to import predictions the recent statement has dropped.

### 3.1 Worked examples

The examples below use theories that are **not** in the coded set, so that they train the rules without revealing any coded cell. They are illustrations of how we read these texts, not claims about the theories that you are asked to accept; you may disagree with the readings and still apply the rules.

**YES**

1. *Affective consciousness (Panksepp 2005, doi:10.1016/j.concog.2004.10.004) × M3 (valence).* The theory states that primary-process affective states are intrinsically valenced and that this raw valence is itself conscious feeling, with subcortical circuits named for each affect. Direction: valence is constitutive of the earliest form of experience. Quotable, directional, nameable → YES.
2. *Dendritic integration theory (Aru, Suzuki & Larkum 2020, doi:10.1016/j.tics.2020.07.006) × M8 (cortical signature).* The theory names a specific cellular signature — coupling between apical and basal compartments of layer-5 pyramidal neurons, gated by thalamocortical input — and states it should be present during conscious processing and abolished (e.g. by anaesthesia) when processing is unconscious. → YES.

**IMPLICIT**

3. *Feelings as homeostatic states (Damasio & Carvalho 2013, doi:10.1038/nrn3403) × M5 (cortical–autonomic coherence).* The account states that feelings are experiences of the body's homeostatic state and names interoceptive pathways and their cortical targets, but it does not state a prediction over a coherence measure between cortical and autonomic dynamics. One can construct such a prediction without new machinery ("if feeling is the representation of body state, then access to feeling should covary with cortical–visceral coupling"), because the ingredients are the theory's own. → IMPLICIT, not YES (no stated prediction) and not NO (no auxiliary assumption needed).
4. *Temporo-spatial theory of consciousness (Northoff & Huang 2017, doi:10.1016/j.neubiorev.2017.07.013) × M7 (precision of metarepresentation).* The theory predicts over spontaneous activity, scale-free dynamics and stimulus–rest alignment. It does not state a prediction about metacognitive precision, but its claim that the temporo-spatial structure of ongoing activity determines what can be experienced can be extended to confidence about experience without adding machinery. → IMPLICIT. (If you judged that the extension does require an extra assumption about how confidence is computed, NO would be the defensible alternative; this is the kind of cell to flag with `confidence = 1`.)

**NO**

5. *Orchestrated objective reduction (Hameroff & Penrose 2014, doi:10.1016/j.plrev.2013.08.002) × M2 (degree of incompatibility between policies).* The theory's predictive apparatus concerns microtubule quantum states and their reduction. Competing action policies and their incompatibility are not named and do not follow from any stated commitment; a prediction would require importing a decision-theoretic layer the theory does not have. → NO.
6. *Dendritic integration theory (Aru, Suzuki & Larkum 2020) × M3 (valence).* The same source that yields YES on M8 is silent on valence: the mechanism is defined over sensory-context coupling in pyramidal cells regardless of affective sign. Nothing in the stated commitments distinguishes valenced from neutral content. → NO. (This pair shows that codes are per cell, not per theory.)

**Y(neg)**

7. *Consciousness without a cerebral cortex (Merker 2007, doi:10.1017/S0140525X07000891) × M8 (cortical signature).* The paper explicitly argues that a cerebral cortex is not necessary for primary consciousness, locating the sufficient substrate in the midbrain/upper brainstem. This is a stated prediction that a cortical signature of access is **not** required. → Y(neg), not NO: the negation is asserted, not omitted.
8. *Free-energy account of the hard problem (Solms 2019, doi:10.3389/fpsyg.2018.02714) × M7 (precision of metarepresentation).* The account states that consciousness is fundamentally affective and arises in the upper brainstem, and that cortical/cognitive (including higher-order, reflective) representation is not what makes a state conscious. That is a stated denial that metarepresentation is necessary for experience. → Y(neg). (Note that Solms does use the term "precision" in a different, active-inference sense — precision-weighting of prediction errors. Do not let a shared word carry a code: the cell asks about precision of *metarepresentation*.)

---

## 4. Rules for Table S2 (study inventory)

The unit is one **empirical study** (36 rows; `citation_label` and `doi` are prefilled). Inclusion has already been decided; you code two variables.

### 4.1 `theory_addressed`

Rule: name the theory (or theories) that the study **explicitly tests or is explicitly cited as evidence for**, as stated in the study's own introduction/discussion or in the theory's primary statement (§5). Do not infer "the theory this paradigm could speak to".

- Use the short labels from §5: `GNWT`, `IIT`, `RPT`, `HOT/HOSS` (one row), `AST`, `PP`, `SIT`, `UAL`, `F&M`.
- If two theories are pitted against each other, write both separated by ` vs ` (e.g. `GNWT vs IIT`). If the study is cited in support of two theories without contrast, separate by `/` (e.g. `GNWT/RPT`).
- If the study addresses none of the coded theories (a canonical paradigm paper or a phenomenon-level report), write exactly `none of the coded theories`.
- The agreement script derives a binary flag from this column (addresses ≥ 1 coded theory vs none); the string itself is also compared.

### 4.2 `content` — the content whose access is manipulated

Mutually exclusive; code by the **content whose access (visibility, detectability, report) is the manipulated or measured dimension**, not by any content that merely appears in the display.

| Category | Definition |
|---|---|
| `neutral-visual` | Visual content used as a neutral exemplar: gratings, letters, words, digits, false fonts, objects, faces *as a category*, geometric shapes, motion, contrast-defined stimuli. Faces or words count here when their affective value is not the manipulated dimension. |
| `neutral-nonvisual` | Auditory or tactile content with no affective manipulation. |
| `valenced` | Content whose affective value is the manipulated dimension: emotional expressions contrasted with neutral, threat, reward, pain. |
| `interoceptive` | Content originating in visceral/autonomic channels (heartbeat, respiration) whose detection, accuracy or awareness is what is measured. |
| `motor-conflict` | Competing action policies over the body as the manipulated content: sustained incompatible intentions, response conflict where the conflict itself is what is made conscious or rated. |
| `state (no content)` | Global state manipulation or whole-brain state contrast without a stimulus-level content contrast (e.g. mind blanking, spontaneous fluctuations, no-report state comparisons). |

Boundary rules: (i) if a study has both a valenced and a neutral condition and the valence contrast is analysed, code `valenced`; if emotional faces are used only as stimuli and the analysed contrast is seen/unseen regardless of expression, code `neutral-visual`; (ii) error awareness paradigms are `motor-conflict` only if the conscious content is the conflict/error itself, otherwise code the stimulus content; (iii) heartbeat-evoked responses used as a *modulator* of visual detection are coded by the accessed content (`neutral-visual`), not `interoceptive`.

Record a one-sentence `justification` for each row (which condition and which analysed contrast drove the code).

---

## 5. Theories and primary sources

Twelve row blocks appear in `S1_blank_for_coder2.csv`. The first nine correspond to the manuscript's theory set; in the blind form two composite labels are split so that their components can be coded separately (HOT and HOSS; SIT and passive frame theory), and one supplementary block (neural subjective frame) is added for a robustness check. The `theory_level` column marks two accounts as **origin-level**: they are theories of how and when consciousness arose in evolution rather than theories of moment-to-moment access. For origin-level accounts, read each quantity's question as "does the theory state that this quantity is a marker or condition of the *presence* of consciousness in an organism?"

Sources are listed most-recent-empirical-statement first; that is the canonical statement for the "which formulation" rule in §3. DOIs were resolved through CrossRef on the day this pack was prepared.

**GNWT — Global neuronal workspace theory** (content-level)
- Mashour, Roelfsema, Changeux & Dehaene 2020 — doi:10.1016/j.neuron.2020.01.026
- Cogitate Consortium et al. 2025 (adversarial test, preregistered predictions) — doi:10.1038/s41586-025-08888-1
- Dehaene & Changeux 2011 — doi:10.1016/j.neuron.2011.03.018
- Dehaene, Changeux, Naccache, Sackur & Sergent 2006 — doi:10.1016/j.tics.2006.03.007
- Dehaene & Naccache 2001 — doi:10.1016/s0010-0277(00)00123-2

**IIT (3.0/4.0) — Integrated information theory** (content-level)
- Albantakis et al. 2023 (IIT 4.0) — doi:10.1371/journal.pcbi.1011465
- Cogitate Consortium et al. 2025 (adversarial test, preregistered predictions) — doi:10.1038/s41586-025-08888-1
- Tononi, Boly, Massimini & Koch 2016 — doi:10.1038/nrn.2016.44
- Oizumi, Albantakis & Tononi 2014 (IIT 3.0) — doi:10.1371/journal.pcbi.1003588

**RPT — Recurrent processing theory** (content-level)
- Lamme 2010 — doi:10.1080/17588921003731586
- Lamme 2006 — doi:10.1016/j.tics.2006.09.001
- Lamme & Roelfsema 2000 — doi:10.1016/s0166-2236(00)01657-x

**HOT / HOSS — Higher-order theory (representational / HOROR family) and higher-order state space, coded as one row** (content-level)
- Brown, Lau & LeDoux 2019 — doi:10.1016/j.tics.2019.06.009
- LeDoux & Brown 2017 — doi:10.1073/pnas.1619316114
- Lau & Rosenthal 2011 — doi:10.1016/j.tics.2011.05.009
- Fleming 2020 — doi:10.1093/nc/niz020
- Dijkstra & Fleming 2023 — doi:10.1038/s41467-023-37322-1
- Fleming & Daw 2017 — doi:10.1037/rev0000045
- Maniscalco & Lau 2012 (measurement framework, meta-d′) — doi:10.1016/j.concog.2011.09.021


**AST — Attention schema theory** (content-level)
- Wilterson et al. 2020 — doi:10.1016/j.pneurobio.2020.101844
- Graziano, Guterstam, Bio & Wilterson 2019 — doi:10.1080/02643294.2019.1670630
- Graziano & Webb 2015 — doi:10.3389/fpsyg.2015.00500

**PP — Predictive processing / beast-machine account** (content-level)
- Hohwy & Seth 2020 — doi:10.33735/phimisci.2020.ii.64
- Seth & Tsakiris 2018 — doi:10.1016/j.tics.2018.08.008
- Seth & Friston 2016 — doi:10.1098/rstb.2016.0007
- Seth 2013 — doi:10.1016/j.tics.2013.09.007
- Clark 2013 (general predictive-processing framework) — doi:10.1017/s0140525x12000477
- Auxiliary empirical/theoretical sources used in the PP literature and admissible as anchors: Pezzulo, Rigoli & Friston 2018 — doi:10.1016/j.tics.2018.01.009; Joffily & Coricelli 2013 — doi:10.1371/journal.pcbi.1003094; Kleckner et al. 2017 — doi:10.1038/s41562-017-0069; Garfinkel et al. 2015 — doi:10.1016/j.biopsycho.2014.11.004.

**SIT — Supramodular interaction theory** (content-level)
- Morsella, Gray & Krieger 2009 — doi:10.1037/a0017121
- Morsella, Krieger & Bargh 2008 — doi:10.1093/oso/9780195309980.003.0030
- Morsella 2005 — doi:10.1037/0033-295x.112.4.1000

**Passive frame theory** (content-level; successor synthesis to SIT — code it on its own statements)
- Morsella, Godwin & Jantz 2016 — doi:10.1017/s0140525x15002812
- Morsella, Godwin, Jantz, Krieger & Gazzaley 2015 — doi:10.1017/s0140525x15000643
- Poehlman, Jantz & Morsella 2012 — doi:10.3389/fpsyg.2012.00369

**UAL — Unlimited associative learning** (origin-level)
- Birch, Ginsburg & Jablonka 2021 — doi:10.1007/s10539-021-09802-5
- Birch, Ginsburg & Jablonka 2020 — doi:10.1007/s10539-020-09772-0
- Ginsburg & Jablonka 2019 (book) — doi:10.7551/mitpress/11006.001.0001
- Ginsburg & Jablonka 2010 — doi:10.1016/j.jtbi.2010.06.017

**Feinberg & Mallatt — Neurobiological naturalism** (origin-level)
- Feinberg & Mallatt 2020 — doi:10.3389/fpsyg.2020.01041
- Feinberg & Mallatt 2016 (book) — doi:10.7551/mitpress/10714.001.0001
- Feinberg & Mallatt 2013 — doi:10.3389/fpsyg.2013.00667

**Neural subjective frame (Tallon-Baudry)** (content-level; supplementary block)
- Azzalini, Rebollo & Tallon-Baudry 2019 — doi:10.1016/j.tics.2019.03.007
- Babo-Rebelo, Richter & Tallon-Baudry 2016 — doi:10.1523/JNEUROSCI.0262-16.2016
- Park, Correia, Ducorps & Tallon-Baudry 2014 — doi:10.1038/nn.3671
- Park & Tallon-Baudry 2014 — doi:10.1098/rstb.2013.0208

---

## 6. Files in this pack

| File | Contents |
|---|---|
| `codebook_second_coder.md` | This document |
| `S1_blank_for_coder2.csv` | 88 rows = 11 theory blocks × 8 quantities; columns `theory, theory_level, quantity_id, quantity, code, justification, source_label, source_doi, confidence` |
| `S2_blank_for_coder2.csv` | 36 rows with `citation_label, doi` prefilled; fill `content, theory_addressed, justification` |
| `coder2_timing_log.csv` | One row per block; record start/end/minutes |
| `agreement.py` | Agreement script (run after both codings are complete): `python agreement.py --s1a S1_coder1.csv --s1b S1_coder2.csv --s2a S2_coder1.csv --s2b S2_coder2.csv --out agreement_out/` (add `--exclude-theories tallon` to report the headline kappa without the supplementary block; `python agreement.py --selftest` reproduces the synthetic check) |

Before comparison the first coder completes the same 88-row form (the split SIT/passive-frame block and the supplementary block) without access to your form; the script matches rows by theory name and quantity, so both files must contain the same blocks. Rows without a counterpart are reported, not silently dropped.

Codes are accepted in any of the spellings `YES`, `IMPLICIT`, `NO`, `Y(neg)` / `YES (negative)` / `YES(neg)`; the script normalises case and spacing.
