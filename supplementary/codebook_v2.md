# Codebook for the independent second coding (blind pack)

Manuscript: *What theories of consciousness commit to, and what they leave unmeasured: an audit of stated predictions after the first adversarial test* (working title, revision 1) (Brain Sciences, ms. brainsci-4583950, revision round 1; submitted under the title *One quantity, nine theories*).
Purpose of this pack: an independent second application of the coding scheme behind Tables 1 and 2 (Supplementary Tables S1 and S2), so that inter-coder agreement (Cohen's kappa) can be reported.

**This pack is blind.** It contains the definitions, the decision rules, the theory list with primary sources, and blank forms. It does not contain the first coder's codes, justifications, or the results reported in the manuscript's §7. Please do not consult §7.3–§7.8 of the manuscript, the filled Supplementary Tables, or the first coder until both forms are returned.

---
## 1. One-page instruction

1. **Code independently.** Do not discuss cells with the first coder before the forms are returned. Do not open the manuscript's §7 results, the filled S1/S2, or any draft of the response to reviewers.
2. **Read the sources, not the summaries.** For each theory, read the primary sources listed in §5 of this codebook (3–5 per theory). You may add further sources, but each code must be anchored to a specific citable text; record it in the `source_label` / `source_doi` columns.
3. **Fill `S1_blank_for_coder2_v2.csv` (120 rows).** For every account × domain cell enter exactly one code from {EXPLICIT, INTERPRETED, NOT_LOCATED, NOT_APPLICABLE, UNRESOLVED} in `code`, `polarity` (positive / stated_null / negative) for EXPLICIT and INTERPRETED, `relation`, a one- or two-sentence `claim_text` in your own words, and `source_label`, `source_doi`, `source_locus`. If the code is NOT_LOCATED, `claim_text` should state what you looked for and did not find. `confidence` is optional (1 = guess, 2 = defensible, 3 = certain).
4. **Fill `S2_blank_for_coder2_v2.csv` (42 rows, one per row of the first coder's partition of 32 publications).** For each row enter the raw fields `modality`, `affective_status`, `effector_type` (skeletal / autonomic, motor rows only), `manipulation`, `measured_outcome`, `report_type`; the attribution fields `theory_attribution_by_authors` (with `by_authors_locus`), `theory_attribution_later` (post-publication attribution by others, with `later_attribution_evidence` — a citable DOI or 'none found'); and `contested_inclusion`. The content class is not entered: it is derived from the raw fields by script (§4). **Your own partition:** in `unit_type_coder2` state whether the row is, in your reading of the paper, one experiment, a group of experiments, or the whole publication treated as one because the paper's partition could not be verified; in `n_experiments_identified` give the number of separately analysed experiments you find in the publication, and in `partition_note` say where they differ from the row structure. You will need the methods (stimuli and task), not only the abstract.
5. **Time yourself.** Record start and end times per theory block and for the S2 form in `coder2_timing_log.csv`. The time is reported in the manuscript's method section as a property of the scheme, not as an assessment of you.
6. **Do not resolve doubt by looking for the "expected" answer.** When a cell is genuinely ambiguous, choose the code the decision rules in §3 require, and flag the cell with `confidence = 1`. Ambiguous cells are exactly what the adjudication meeting is for.
7. **Return** the S1 and S2 forms, the timing log and, if you took it on, the S3 form. Agreement is then computed by `agreement.py` (raw agreement, confusion matrix, nominal κ for code and for code × polarity, per-domain κ, κ by origin subset; for S2 agreement on the raw fields, on the by-authors attribution and separately on the later attribution and its evidence; disagreement lists) and the disagreements are adjudicated jointly, with the adjudication record deposited alongside the tables. **Second step, after S1 is returned:** you receive the prediction register (Table S4) and a pair list with the assessment fields empty, and code the relation of every cross-theory pair of stated predictions (different / jointly compatible / discriminating / incompatible) with a pair confidence; that step checks the first coder's pair judgements, not the completeness of the register's extraction, which only your S1 can check.

Expected effort: roughly 6–10 hours for S1 and 2–3 hours for S2, spread over several sittings.

---
## 2. The ten domains (operational definitions)

The unit of coding in S1 is a **theory × quantity cell**. The question in each cell is the same: *does this theory, in its canonical empirical formulation, make a stated prediction about how this quantity relates to conscious access or to the presence of experience?*

"Quantity" means a variable that could in principle be measured or manipulated in an experiment. The ten domains fall into three groups.

### 2A. The arbitration situation (what the organism has to decide)

**M1 — Number of simultaneously competing action policies.**
How many distinct courses of action (motor plans, approach/avoid tendencies, response options) are simultaneously active and compete for control of the body at the moment of interest. Operationalised by task design (single-response vs multi-response conflict tasks, Stroop-type incongruence, sustained incompatible intentions) or by decoding the number of concurrently represented plans. A theory predicts over M1 if it states that conscious access, its likelihood, or its intensity changes as a function of *how many* policies compete — not merely that consciousness "involves action".

**M2 — Degree of incompatibility between competing policies.**
Given that more than one policy is active, how mutually exclusive they are: two policies that can be executed together (look and reach) versus two that cannot (inhale and exhale; move left and move right). Operationalised as effector overlap, response-set conflict, or the impossibility of joint execution. A theory predicts over M2 if it states that the *degree* of conflict between policies changes access or experience.

**M5 — Organism-wide coherence across cortical and autonomic channels.**
The extent to which cortical activity and autonomic/visceral activity (cardiac, respiratory, gastric, electrodermal, pupillary) are coupled or coordinated at the moment of access — a measurable coupling index (phase coupling, information transfer, covariance across channels), not a metaphor of "whole-organism" unity. A theory predicts over M5 if it states that conscious access or its content depends on, or is indexed by, the coherence between cortical and autonomic dynamics. Statements that consciousness is "embodied", "for the whole organism" or "serves homeostasis" are relevant to the INTERPRETED/NOT_LOCATED decision (§3) but are not, by themselves, a stated prediction over a coherence measure.

### 2B. The content (what is accessed)

**M3 — Valence of conscious content.**
The affective sign and magnitude of the content whose access is at issue (positive/negative, threat/reward, pain/pleasure). A theory predicts over M3 if it states that valence changes access (its threshold, priority, timing or neural signature), or that valence is itself a constitutive dimension of what becomes conscious.

**M4a — Access to interoceptive content as content.**
Whether the theory states that interoceptive or visceral signals (heartbeat, respiration, gastric rhythm, thermal and homeostatic states) can themselves become the accessed content, and whether such content is accessed by the same mechanism as exteroceptive content. A stated prediction that interoceptive content is accessed like any other content is EXPLICIT positive; a stated prediction that it is not experienced as content is EXPLICIT stated_null.

**M4b — Visceral modulation of access to exteroceptive content.**
Whether the theory states that the state or phase of an autonomic signal (cardiac phase, heartbeat-evoked response amplitude, respiratory phase, arousal level) changes the probability or quality of access to an *exteroceptive* content. This is a modulation claim, not a content claim: the accessed content is visual or auditory, the modulator is visceral.

**M4c — Conscious involvement in purely autonomic conflict.**
Whether the theory states that a conflict resolved wholly by autonomic (smooth-muscle, glandular) effectors, with no skeletomotor plan at any point, involves conscious experience. A stated exclusion of autonomic conflict from the function of consciousness is EXPLICIT stated_null — record in `claim_text` that this is an exclusion from the theory's function, not a denial that bodily states can be felt. A mechanism that would produce a feeling here but is not stated for this condition is INTERPRETED positive. Coding requires the source to define conflict and to exclude skeletomotor involvement; if it does neither, code NOT_LOCATED.

*Coding note for all three:* a legacy M4 code (v1.3) does not transfer. Each M4a/M4b/M4c cell is coded from the source anew; the v1.3 justification is reference material only.
### 2C. The format and signature of access (how it is accessed)

**M6 — Dimensionality of phenomenal space.**
The number of independent dimensions along which conscious experience can vary at a given moment (a structured, quantifiable notion: the rank or intrinsic dimensionality of the represented state, the size of the set of distinguishable experiences). A theory predicts over M6 if it states how this dimensionality is determined, how it changes with manipulations, or how it can be measured.

**M7 — Precision of metarepresentation.**
The reliability with which the system represents its own first-order states — confidence calibration, metacognitive sensitivity (e.g. meta-d′), the precision or variance of a higher-order estimate. A theory predicts over M7 if it states that the presence, degree or content of conscious experience depends on the precision of the higher-order representation, or that a metacognitive measure indexes it.

**M8 — Cortical signature of access.**
A specific, localisable neural correlate of conscious access in cortex: a region (prefrontal, posterior "hot zone", sensory cortex), a temporal marker (P3b, late ignition, recurrent feedback in a given window), or a connectivity pattern. A theory predicts over M8 if it names such a signature and states that it should be present when content is accessed and absent when it is not (or vice versa). A stated prediction that a cortical signature is **not** necessary for experience is also a prediction (EXPLICIT stated_null).

---
## 3. The codes and their decision rules (scheme v2)

Each cell = one account × one domain. Code the **statement**, not your belief about the theory.

| Code | Meaning | Decision rule |
|---|---|---|
| **EXPLICIT** | The source states a prediction over this domain. | You can quote a sentence (or a preregistered prediction) that names the quantity or its operationalisation and says what should happen to access/awareness when it varies. Record `polarity`: **positive** (involvement/effect predicted), **stated_null** (the source states that the quantity makes *no* difference, or excludes the domain from the theory's function), **negative** (access predicted to *decrease*). A stated null is a stated prediction. |
| **INTERPRETED** | The prediction follows from the stated mechanism but the source does not state it for this domain. | You can name the mechanism and the inference step in one sentence. Record `polarity` as above. This is the old IMPLICIT. |
| **NOT_LOCATED** | No statement found in the examined corpus. | Applies only to the sources listed in §5 plus any you name in `source_locus`. NOT_LOCATED is **not** a prediction of no effect and is never counted as a null. |
| **NOT_APPLICABLE** | The theory itself places the domain outside its scope. | The source says so (e.g. an origin-level account that declines trial-level predictions). Quote the scope statement. |
| **UNRESOLVED** | Sources of the same account conflict, or the statement cannot be classified. | Record both readings in `claim_text`; the cell goes to adjudication. |

Every EXPLICIT or INTERPRETED cell carries: `relation` ∈ {effect, modulation, necessity, sufficiency, constitution, marker, scope}, `source_label`, `source_doi`, `source_locus` (section / page / figure / preregistered-prediction number), `evidence_status` (full-text / abstract-only / secondary), `confidence` (1–3). Several distinct predictions in one cell are **not** separate S1 rows: S1 holds one row per cell with the code of the strongest statement; each prediction is a row of Table S4 (register) with its own P-id, listed in `prediction_id` separated by `;`.

**Legacy mapping (for the 96 cells carried from v1.3, HOT/HOSS split):** YES → EXPLICIT positive; YES (negative) → EXPLICIT stated_null; IMPLICIT → INTERPRETED; NO → NOT_LOCATED, unless the source states a scope exclusion → NOT_APPLICABLE. The legacy code stays in `legacy_code` and is never overwritten.

**What the column class means and who assigns it.** No coder assigns a column class. `column_typology_pairs.py` derives it from S1, S4 and a pair register after both codings: contested (≥ 2 EXPLICIT and ≥ 1 cross-theory pair of stated predictions whose relation is *discriminating* or *incompatible* — a shared observable under a shared condition, with a value predicted by one and excluded by the other; pairs that merely *differ* or are *jointly compatible* do not count), single-occupant (exactly 1 EXPLICIT), occupied-not-contested (≥ 2 EXPLICIT, no discriminating pair), thin (0 EXPLICIT, ≥ 1 INTERPRETED), unoccupied (none). The pair relations are coded in a second step, after S1 is returned. Do not let the expected class influence a code.
## 4. Rules for Table S2 v2.1 (study inventory)

The unit of analysis, inclusion rules, content classes and the attribution rule are given in `S2_inclusion_criteria_v2.txt` (v2.1) and reproduced here without the first coder's row-level decisions.

```
INCLUSION CRITERIA, TABLE S2 v2.1 (content inventory) — supersedes v2 (24 Sep 2026: content classes sharpened) and S2_inclusion_criteria.txt (v1.3)

UNIT OF ANALYSIS
U1. The unit is one empirical experiment: a data collection with its own sample (or sub-samples) and its own
    analysed contrast. A publication reporting several experiments contributes several rows (experiment_id);
    a preregistered protocol and its final report share one study_family_id and the protocol contributes no row.
    Control and ancillary experiments reported in the same publication are rows, flagged ancillary_experiment = True.
    Re-analyses of previously published data sets are not new experiments and are not rows.
    Where only the abstract could be read and the partition into experiments cannot be verified, the publication
    is carried as one row (or as the blocks the abstract itself names) and evidence_status records the limitation.
U2. participants_total (recruited/tested) and participants_in_analysis are recorded separately; multi-arm
    experiments (e.g. fMRI / MEG / iEEG arms of the same design) list one sample_id per arm in samples_detail.

INCLUSION
I1. The experiment manipulates conscious access / awareness of a specific content (content-NCC), or measures
    awareness of a specific content trial by trial or between groups. Purely computational, purely philosophical
    and purely clinical-outcome papers are excluded. Experiments that hold access below threshold throughout
    (e.g. masked presentation with no seen/unseen contrast) and experiments in which the measured variable is a
    metacognitive index (confidence–accuracy correspondence, meta-d′) rather than access are admissible only
    as contested rows: contested_inclusion = True with a written contested_reason, and their effect on every
    count is reported in s2_sensitivity.csv. No borderline row is included or excluded automatically.
I2. Theory attribution is recorded in three separate columns and is never merged:
      theory_attribution_by_authors — the theory the study's own authors name as tested, or as the framework
                                      their result bears on, in the study's own abstract, introduction or
                                      discussion, with the locus given;
      theory_attribution_later      — a later paper that is a coded theory's primary statement (codebook §5)
                                      cites the study, with DOI; later_attribution_evidence states whether the
                                      citing sentence was read and names the theory (CONTEXT_NAMED), was read
                                      but names no theory (CONTEXT_UNNAMED), or whether only the reference list
                                      was checked (REFLIST);
      theory_attribution_coder      — the coder's own inference, marked as such.
    theory_addressed (baseline) = True if and only if theory_attribution_by_authors or theory_attribution_later
    names a coded theory. Coder inference alone is NOT sufficient for the baseline; it enters only the
    sensitivity scenario "plus coder attribution". A stricter variant (theory_addressed_strict) accepts a later
    attribution only when its citing context was read and names the theory.
I3. Canonical paradigm papers — the protocol, taxonomy, theory or review paper that defines a paradigm the coded
    theories are tested with — are paradigm sources, not theory-addressed studies (consistent with codebook §4.1:
    a canonical paradigm paper addresses none of the coded theories as an empirical test). They are listed in
    paradigm_sources.csv with the rows that rely on them and are outside every S2 denominator. In v2 these are
    Melloni et al. 2023 (protocol), Dehaene et al. 2006 (taxonomy), Boly et al. 2017 (review) and Poehlman,
    Jantz & Morsella 2012 (theory paper). Meta-analyses and databases (e.g. ConTraSt) are not inventory rows.
I4. Citations must resolve through CrossRef (DOI); abstracts and, where accessible, full texts were read for every
    row, and evidence_status records which.

CONTENT CODING (two orthogonal fields; the five-way class used in counts is derived by script)
  modality          : visual / auditory / tactile / motor / interoceptive / mixed / not applicable (state)
  affective_status  : neutral / valenced (affective value is the manipulated dimension) / interoceptive
                      (content originates in visceral or autonomic channels)
  content_class_v2 (derived) : neutral-visual = neutral × visual; neutral-nonvisual = neutral × auditory or
                      tactile; motor-conflict (skeletal) = modality motor, competing action policies realised by
                      skeletal effectors (including awareness of one's own response errors when the error itself is
                      the accessed content, codebook §4.2 rule ii); motor-conflict (autonomic effector) = an intention
                      directed at an autonomic (smooth-muscle, glandular) effector against a reflex or a competing
                      intention — the accessed content is the experienced conflict of intentions, not a visceral
                      signal; valenced = affective_status valenced;
                      interoceptive = the accessed content originates in visceral AFFERENTS (heartbeat, respiration,
                      gastric rhythm, thermal/homeostatic state) or an autonomic signal modulates access to another
                      content; state (no content) = no content contrast, outside the content denominators.
                      Motor-conflict rows of both kinds count together as 'motor-conflict' in the five-way tallies and
                      are shown apart in the seven-way breakdown.
  Boundary rules of codebook §4.2 (i)–(iii) apply unchanged. Code by the content whose access is manipulated
  or measured, not by any content that merely appears in the display.

(Row-level decisions of the first coder are withheld from this blind copy; they are listed in the deposit version of this file and released with Table S4 after the second coding is returned.)
```

Coder 2 fills, for every experiment row: `modality`, `affective_status`, `effector_type` (motor rows), `manipulation`, `measured_outcome`, `report_type`, `theory_attribution_by_authors` (with locus), `theory_attribution_later` with `later_attribution_evidence` (search the coded theories' primary statements in §5 for citations of the study; enter 'none found' when none), `contested_inclusion` + `contested_reason`, and the partition fields `unit_type_coder2`, `n_experiments_identified`, `partition_note`. The later attribution is coded independently by both coders because it moves the theory-addressed denominator; agreement on it is reported separately. Code by the content whose access is manipulated or measured: an intention directed at an autonomic effector is motor conflict (autonomic effector), not interoceptive content; interoceptive content originates in visceral afferents. `theory_attribution_later`, `theory_attribution_coder` and `theory_addressed` are derived or first-coder fields and are never typed by coder 2.

## 5. Theories and primary sources

Twelve row blocks appear in `S1_blank_for_coder2_v2.csv` (120 rows: 12 accounts × 10 domains). Ten are trial-level accounts and two are origin-level. Relative to the submitted manuscript, the composite label is split (supramodular interaction theory; passive frame theory), the neural subjective frame is added, and HOT and HOSS are coded as separate accounts on their own primary sources (§5).

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

**HOT — Higher-order theory (representational / HOROR family)** and **HOSS — Higher-order state space**, coded as two separate rows (content-level); HOT sources first, HOSS sources (Fleming and colleagues) second
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
## 6. Files in this pack (v3.3)

| File | Purpose |
|---|---|
| accounts_manifest.csv | 12 accounts with `theory_id`, `row_class`, `origin`. Labels must match exactly. |
| domains_manifest.csv | 10 domains M1, M2, M3, M4a, M4b, M4c, M5, M6, M7, M8. |
| S1_blank_for_coder2_v2.csv | 120 rows (theory_id × domain_id) with code, polarity, relation, claim_text, source_label, source_doi, source_locus, evidence_status, confidence empty. |
| S2_blank_for_coder2_v2.csv | 42 rows (the first coder's partition of 32 publications into experiment-level rows), all coding columns empty; includes your own partition fields (`unit_type_coder2`, `n_experiments_identified`, `partition_note`), `effector_type` and the later-attribution fields. |
| S3_blank_for_coder2.csv | Optional: 120 rows (10 theory blocks × 12 ConTraSt dimensions), coding columns empty (§7). |
| agreement.py | `python agreement.py --s1a <coder1> --s1b <coder2> --accounts accounts_manifest.csv --domains domains_manifest.csv --code-scheme v2 --out agreement_out/` — raw agreement, confusion matrix, nominal κ, per-domain κ, κ by origin subset. No interval unless `--ci` is given. |
| coder2_timing_log.csv | Start/end time per block. |

**Blindness.** The second author read the submitted manuscript, including its condensed Table 1 (72 cells, legacy codes). Blindness is therefore partial for the `submitted-v1` cells and full for the `added-in-revision` cells (M4a/M4b/M4c and the PFT/NSF rows); agreement is reported for the two subsets separately. Do not open the first coder's file until your own is complete and time-stamped.

**Freeze.** This codebook is frozen at the version and hash printed in the footer. Any change to a definition, code or rule after the second coder has started requires re-coding the affected cells by both coders and is logged in `codebook_changelog.md`.
## 7. Table S3 — the same theories against the ConTraSt annotation dimensions (optional)

`S3_blank_for_coder2.csv` (in this pack) has 120 rows: the ten theory blocks of the submitted manuscript (HOT/HOSS as one block; the neural subjective frame is not part of S3) × the twelve annotation dimensions of the ConTraSt database (Yaron et al. 2022, *Nature Human Behaviour* 6, 593–604). The codes are the same four as in S1. The question in each cell: *does the theory's canonical empirical statement — or, for GNWT and IIT, the preregistered Cogitate predictions — state which value of this dimension an experiment should observe, or state that the dimension should make no difference?* An explicit invariance claim ("the signature does not depend on the task") is a stated prediction: code YES and set `invariance_based_YES = TRUE`, so that the strictly differential count can be computed.

| Dimension | What a stated prediction looks like |
|---|---|
| C1 Type of consciousness (content / state) | Predicts differently for content-NCC and state-NCC paradigms, or claims invariance across them |
| C2 Report / no-report | Predicts what changes, or does not change, when report is removed |
| C3 Consciousness measure type (objective / subjective / condition assessment / none) | Commits to a measure type, or predicts divergence between measure types |
| C4 Experimental paradigm (family / specific) | Names paradigms in which its signature should, or should not, appear |
| C5 Task type | Predicts dependence of the signature on task (e.g. task relevance), or invariance to it |
| C6 Stimulus (modality / category / duration / contrast) | Predicts dependence on a stimulus property, or invariance to it |
| C7 Sample / population (healthy adults / patients / non-human / computer) | Makes a prediction for a population other than healthy adults, including artificial systems |
| C8 Neuroscientific technique | Predicts which technique should detect the signature (e.g. intracranial gamma, fMRI, EEG) |
| C9 Dependent measure / analysis type (activation, connectivity, complexity, Φ, cardiac tags …) | Commits to a dependent measure or analysis |
| C10 Temporal findings (component / time window) | Predicts a time window or ERP component |
| C11 Spatial findings (region / lobe / stream) | Predicts a location |
| C12 Frequency findings (delta–gamma) | Predicts a frequency band |

Anchor every non-NO cell to a citable source, as in S1. If the theory says nothing that bears on the dimension, code NO and state what you looked for.

---
**Codebook v2.3 — frozen 24 September 2026. sha256 of everything above this line (all bytes up to and including the newline that precedes it): `3b4b0cac6995df03c730b211d5d4d3dae3b070e252308610dae730f08ab479f1`.** Changes after the second coder starts → `codebook_changelog.md` and re-coding of affected cells.
