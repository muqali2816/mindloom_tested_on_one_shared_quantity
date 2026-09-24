# Response to the Editor and Reviewers

**Manuscript:** brainsci-4583950 — *Brain Sciences* (MDPI)
**Title as submitted:** One quantity, nine theories: what adversarial tests of consciousness are not yet able to measure
**Title as revised:** What theories of consciousness commit to, and what they leave unmeasured: an audit of stated predictions after the first adversarial test
**Decision:** Major revision (23 September 2026)

We thank the Editor and both Reviewers. Reviewer 1's first two points identified an equivocation in the central argument — between a column no theory occupies and a column theories disagree about — and the revision is built around removing it. In removing it we also re-audited our own tables, and that re-audit changed several claims the Reviewers did not challenge; those changes are reported separately in Section 4, because a reviewer should not have to discover them by comparison.

**How to read this document.** Every comment is quoted verbatim, in the order in which it appears in the decision letter, followed by our response, a status and the location of the change in the revised manuscript. Four statuses are used and used strictly:

- **DONE** — the change is in the revised text now.
- **PREPARED** — the material exists (files, scripts, placeholders) but the item awaits an action only the authors can take (a second coding, a deposit, a letter), and the manuscript says so.
- **PARTLY** — part of the request is in the text; the rest is stated as not done, with reasons.
- **DECLINED** — not done, with reasons.

Two kinds of number remain as bracketed placeholders in the text and are never reported here as if they existed: the inter-coder agreement statistics (κ), which depend on a second coding that has not been carried out, and the DOI of the supplementary deposit. Every other count in this document is taken from the fact sheet produced by the reproduction script that accompanies the deposit (`reproduce.py`), not from memory.

**On the highlighting.** The revised manuscript is written in markdown and converted to DOCX and PDF. The yellow highlighting in the PDF is therefore a *reconstructed text comparison* against the submitted version — every passage that was inserted or rewritten is marked — and not Microsoft Word Track Changes. Deleted passages cannot be highlighted; each deletion is listed in Section 5 and at the comment where it is answered. Reviewer line numbers (ll.) refer to the submitted PDF; section numbers below refer to the revised manuscript.

---

## 1. Editor's comments

### E1

> Well written, and Sections 3–5 are a genuinely useful synthesis. But the paper's only original evidence — the 72-cell coding and the 36-study classification — was not supplied, so no reviewer could check a single cell.

**Response.** We apologise. The tables existed at submission and were not uploaded. Because the Editor and Reviewer 1 both ask for a public deposit with a DOI, we distinguish three things that are at different stages, so that no statement in the manuscript or in this letter outruns what has actually happened:

1. *Assembled archive* — exists. The deposit package (v2) contains: Table S1 v2, the theory-by-quantity matrix, now 120 cells (12 accounts × 10 domains; see R1-6 and Section 4b), each with code, polarity, claim text, source, source locus and evidence status; Table S2 v2, the content inventory rebuilt at the level of the experiment (42 experiments from 32 publications; see R1-8), with the four paradigm-defining papers listed separately in `paradigm_sources.csv` and the sensitivity scenarios in `s2_sensitivity.csv`; Table S3, the ConTraSt-dimension coding (see R1-2); Table S4 v2, a register of the 31 predictions on which the column classes rest (28 stated by proponents, 3 derived by us and labelled as such); the frozen codebook v2.0 with its hash; the inclusion criteria; and the scripts (`agreement.py`, `column_typology.py`, `section9_power.py`, `reproduce.py`) with a README. Of the 120 cells, 96 carry the codes of the earlier scheme, mapped to the new code set by rule and never recoded; the remainder are new cells created by the splits described in Section 4, and the earlier undivided M4 cells are superseded by the three-way split and kept in the file for traceability.
2. *Reserved DOI* — not yet reserved. The authors will reserve a DOI (Zenodo or OSF) before resubmission so that the same identifier can be written into all three statements the Editor names in E3.
3. *Public deposit* — not yet made. It is made by the authors when the archive is uploaded; the manuscript carries `[10.xxxx/PLACEHOLDER]` until then.

The archive is also supplied as supplementary files with this resubmission, so that the Reviewers can check every cell now, independently of the deposit.

**Status:** PREPARED (archive assembled and supplied with the resubmission; DOI reservation and public deposit are author actions still to be taken).
**Location of change:** Supplementary Materials; Data Availability Statement; §7.2 Coding procedure.

### E2

> **Author count vs. single coder.** Two authors are listed, but the text says one reader and the AI statement uses the singular. There is also no Author Contributions section. Reconcile this.

**Response.** §7.2 now states that the first coding was carried out by the first author and that the second author will carry out an independent second coding against the frozen codebook (see R1-5 for what exists and what does not). The Use of Generative AI statement is in the plural. An Author Contributions statement in CRediT form has been added to the Declarations. We have been deliberate about one entry: the *validation* role (the second coding) is not attributed to the second author until the second coding has been done; the statement carries it as a bracketed line to be activated at that point, so that the CRediT entry does not describe work that has not yet happened. Author names and affiliations are placeholders for the authors to complete.

**Status:** PARTLY (plural and CRediT section in place; the validation entry and the names await the authors).
**Location of change:** §7.2 Coding procedure; Declarations — Author Contributions; Declarations — Use of Generative AI.

### E3

> **Three contradictory statements about the materials.** Supplementary Materials says "N/A"; §7.8 says the coding is deposited; Data Availability says it is available on request. Deposit publicly with a DOI and make all three agree.

**Response.** The three passages now carry one identical sentence naming the deposited items, the repository and the DOI. The DOI in that sentence is a placeholder, for the reason given in E1: the archive is assembled and supplied, the DOI has not yet been reserved, and the public deposit has not yet been made. We prefer to say this here rather than write "deposited" in three places for a deposit that does not yet exist — which is the fault the Editor found in the submitted version.

**Status:** PREPARED (statements agree; the shared DOI is filled in by the authors at upload).
**Location of change:** Supplementary Materials; Data Availability Statement; §7.2 Coding procedure (the former §7.8 sentence).

### E4

> **M5 is not empty.** Heartbeat-evoked responses have been used to predict conscious detection, and respiratory phase modulates detection thresholds, cortical measures indexed to a visceral signal. You may be able to argue this falls short of a stated prediction, but that argument must be made explicitly, not by omission.

**Response.** The omission was a fault and the argument is now made explicitly. We read and cite the literature the Editor names: pre-stimulus heartbeat-evoked responses predict visual detection (Park et al., 2014) and somatosensory detection (Al et al., 2020, 2021); respiratory phase aligns perception with cortical excitability (Kluger et al., 2021; Grund et al., 2022); heartbeat-evoked responses have been used to detect residual consciousness after coma (Candia-Rivera et al., 2021). We then added the neural subjective frame programme (Park and Tallon-Baudry, 2014; Tallon-Baudry et al., 2018; Azzalini et al., 2019) as a coded account of Table S1, since it states an empirical prediction and meets the inclusion rule.

The argument, made in §7.4: these studies show that a cortical response to *one* visceral signal predicts detection, and the original authors' own control analyses separate that response from the measured autonomic state. They do not state a prediction over organism-wide coherence between cortical and autonomic channels as a joint measure. The neural subjective frame is therefore coded EXPLICIT on M4b (visceral modulation of access to exteroceptive content) and INTERPRETED on M5. The sentence "none operationalises it" has been withdrawn. M5 is now described as *thin*, the class the coding script derives for it: 0 EXPLICIT and 5 INTERPRETED cells among the 12 accounts. The text says in so many words that a coder who read the heartbeat-evoked response as a cortical–autonomic coherence metric would fill one cell of the column, and M5 has been demoted from the headline to a qualified secondary claim (see R1-3).

**Status:** DONE.
**Location of change:** §7.4 Reading the columns ("Thin, not empty: M5"); Table 1; Table S1 v2 (neural subjective frame row); §7.7 What survives reclassification; Abstract.

### E5

> **§9 is an idea, not a design.** No stimulus set, no task, no specified report-independent signature, no power analysis. Since the paper's contribution is a prescription for measurement, one fully worked condition would transform its standing.

**Response.** §9.1 now specifies one condition completely, and a Supplementary Protocol S5 carries the full protocol for two studies. Two things should be said plainly. First, the design changed between our first revision draft and this one, for a reason we found ourselves: in the first draft, incompatibility was manipulated through three rules mapped onto the same keys, so that the number of *distinct* responses demanded rose with incompatibility and the two were confounded. That design is replaced. Second, an internal re-audit of the present draft found that we had described the condition as a direct test of a *stated* prediction (P16, the supramodular threshold) when it is not: P16 concerns experienced conflict between incompatible skeletomotor inclinations, and our condition measures no-report access to a masked visual target under incompatible response rules. The condition therefore tests two operationalisations *we* derived from one account's stated commitments — P32 (a threshold of access at two or more co-executable policies) and P23 (a graded effect of incompatibility at fixed count) — and estimates a third quantity (P33, no further increase from two to three policies, where the source is silent; silence is not a stated null). It tests no stated prediction of any theory directly and discriminates between no two theories; §9.1 and Protocol S5.2 say so, and the register carries P32–P34 as author-derived entries.

*Study 1 (neutral content; §9.1 and Protocol S5).* Three responses on three different effectors, all of which can be executed together, so that policy count and incompatibility are separable by construction. Incompatibility is the number of shared-effector pairs among the three demanded responses — 0, 1 or 3 — at a fixed count of three; a count branch varies the number of licensed responses (1, 2, 3) at zero shared pairs. This gives 11 effector-balanced presentation cells and 5 analysis cells; the shared lever is rotated within participant and the rule-to-lever assignment across participants in six orders. Two confirmatory contrasts, Holm-corrected: C0 (count 1 against 2 or more at zero shared pairs; P32) and C1a (zero against one or three shared pairs at count three; P23); C1b, the two-degree-of-freedom omnibus over the shared-pair levels, is exploratory everywhere. The success rule requires the EEG-based access index and the PAS-report version of each contrast to agree in sign. The task, the block scheme (mapping fixed per block, cells blocked and counterbalanced), the probe (one named rule on a quarter of trials), the access index (regularised LDA on 100–500 ms post-target amplitudes, PAS binarised 1 against 2–4, nested block-wise cross-validation, specification to be frozen after session 1), the pilot criteria, the autonomic windows and the recording set are specified in S5 and labelled "to be preregistered"; nothing has yet been preregistered or deposited.

*Trial budget (S5.8, `trials_budget.csv`).* The re-audit also found that our earlier budget pooled both sessions although only session 2 (no-report) yields confirmatory trials. Session 2 now presents 104 trials per presentation cell (26 probe, 78 no-probe); with 15 % expected loss that is 66 usable no-report trials per cell (the mixed-model check is calibrated at 64), 1144 presented trials in 22 blocks, about 135 min including breaks — long for one EEG visit, and S5.8 names a split-visit variant to be decided at preregistration. Session 1 (titration, PAS on every trial, classifier training) presents 64 per cell.

*Power (Protocol S5, `section9_power.py`; all values from the script's output).* For C0 and C1a, N = 119 is required for 90 % power at dz = 0.30 at α = 0.05 (N = 265 at dz = 0.20; N = 68 at dz = 0.40); the fixed N is 120, a multiple of the six rotations. With the Holm correction over two contrasts the power of each is about 0.89 (Bonferroni floor 0.84); the conjunctive rule — both contrasts significant and both index–report sign agreements — has power about 0.80 under independence, and the dependence-corrected value is to be computed from the pilot. For the equivalence half (P33; two one-sided tests, bound ±0.30 dz) power at N = 120 is 0.895 analytic and 0.896 by Monte Carlo. A mixed-model check with random slopes (200 simulated data sets per contrast, deposited) gives 0.935 (C1a) and 0.900 (C0) against the analytic 0.903, with no non-converged fits. N is fixed in advance; there is no sequential monitoring. The cortical–autonomic coupling index is prepared as *estimation only*; it is not a test of M5.

*Study 2 (valence; Protocol S5 only).* The Study 2 hypothesis is likewise derived (P34): P13 concerns experienced valence and free-energy change, not the direction of access differences between negative and positive content at matched arousal. N = 120 as in Study 1; the incompatibility × valence interaction at dz = 0.20 would need N = 265 and is estimated, not tested.

**Status:** PREPARED — the condition is fully specified and its power computed; it is not yet preregistered, and the conjunctive power under dependence awaits the pilot.
**Location of change:** §9 Conclusion; §9.1 One worked condition; Supplementary Protocol S5 (v2); Table S4 rows P32–P34; deposit files `section9_power.py`, `power_study1.csv`, `power_study2.csv`, `power_mixed_check.csv`, `trials_budget.csv`.


### E6

> **Article type.** Submitted as a Review but reporting original percentages. Either adopt systematic-review methodology (protocol, search strategy, PRISMA, two coders, κ) or drop the percentages and frame the coding consistently as a purposive audit.

**Response.** We took the second route, and the title now says "audit". Every percentage has been removed; every count is given as *k of n*, with the denominator named, and never as an estimate of a population quantity. §7.1 states that the audit is not a systematic review — no registered search, no PRISMA flow — and describes both the theory sample and the study sample as purposive. One element of the first route is also adopted because Reviewer 1 asked for it and because the coding cannot otherwise be endorsed: a second, independent coding against a frozen codebook, with agreement reported. Its status is PREPARED, not DONE, and is described at R1-5. One further change belongs under this heading: the *class* of a column (contested, single-occupant, occupied-not-contested, thin) is no longer a judgement written into the text by the first author. It is derived by a script (`column_typology.py`) from Table S1 and the prediction register S4 under a rule stated in the codebook, and the text reports the classes as results of the coding.

**Status:** DONE (percentages removed, purposive audit framing throughout); the second coding is PREPARED (R1-5).
**Location of change:** Title; Abstract; §7.1 What is coded and why; §7.2 Coding procedure; §7.4; §7.6; §7.7; codebook v2.0 §3.

### E7

> **Format.** Author–date citations with a numbered reference list, neither MDPI style. Converting will also fix the Birch 2020 a/b/c problem and the two inline-only sources.

**Response.** The manuscript now uses MDPI numbered citations in order of first appearance, with the reference list generated from CrossRef records and checked entry by entry. The three Birch items are distinct numbered references, so the a/b/c ambiguity no longer arises. Maturana and Varela (1980) and the New York Declaration on Animal Consciousness (2024) are in the reference list in standard form and are cited by number.

**Status:** DONE.
**Location of change:** throughout; References.

---

## 2. Reviewer 1

We are grateful for a review that was both severe and exact, and we have taken the Reviewer's own ordering: points 1 and 2 are the substance.

### R1-1

> The diagnosis in §1 (ll. 49–54) is that a prediction shared with competitors cannot discriminate, since the experiment testing it tests everyone at once. I agree. The prescription is to find a quantity "at least two live theories disagree about" (ll. 52–53), which is also right, and then the ms. proceeds as though "unoccupied" and "disagreed about" were the same thing. They are not. A column that eight theories are silent on cannot adjudicate between them. If the crossed manipulation in §9 returns a clean effect of incompatibility, GNWT is untouched, IIT is untouched, RPT and AST are untouched, because none of them said anything either way. Silence is not a contrary prediction, and the ms. needs to confront that squarely rather than slide between the two senses of "gap."
>
> The clearest place this bites is ll. 783–786, where a positive dependence of access on conflict load is said to discriminate against GNWT "which predicts none." Table 1 codes GNWT on M1 and M2 as "·", absent from the predictive apparatus, not as "Y(neg)". The author cannot have it both ways within four pages. And there is a further problem: GNWT plus almost any capacity assumption does predict that multiple competing policies eat workspace resources, which is more or less conceded at ll. 771–774 where load is said to degrade access under every theory in the table.
>
> The one cell that genuinely contains opposed predictions is M4, SIT's Y(neg) against interoceptive-inference accounts (ll. 519–525, restated ll. 788–793). That is a real adversarial cell and the ms. is right to prize it. Then ll. 594–598 and 807–815 concede that it cannot be tested, because no report-independent measure of access to interoceptive content has been validated. So the condition that can be run does not discriminate and the condition that discriminates cannot be run. I do not think that is fatal to publication, but it is the actual conclusion of the paper and the abstract currently advertises something else.

**Response.** Accepted in full, and the correction went further than the Reviewer asked, because when we tried to make the distinction operational it changed two of our own classifications.

*The distinction is now operational, not rhetorical.* We built a register of every prediction the coded accounts state over the ten quantities (Table S4 v2: 31 predictions, 28 stated by proponents, 3 derived by us and labelled as derived). A column's class is then derived by script from Table S1 and that register: *contested* if at least two accounts state predictions and at least one pair of stated predictions differs in sign, magnitude, locus, timing, distribution or condition; *single-occupant* if exactly one account states a prediction; *occupied-not-contested* if two or more state predictions and no pair is distinguishable; *thin* if no prediction is stated but at least one account is compatible; *unoccupied* if none. The classes appear in §7.4 as results of the coding, and §1 explains what an experiment on each kind of column can and cannot show. "Silence is not a contrary prediction" is now stated in §1, §7.4 and §9.1.

*What the rule returned.* M1 and M2 are single-occupant (one EXPLICIT account, supramodular interaction theory). M3 and M7 are occupied-not-contested. M5 is thin. M6 is contested only at the lowest confidence level (one pair, IIT against higher-order state space theory, where it is open whether the two address the same variable); at confidence ≥ 2 it is occupied-not-contested, and the text reports it with that caveat. Two results overturned what the submitted version and our first revision draft said, and they are reported in Section 4 as well as here. First, M8 is *contested*, not merely shared: six accounts state predictions and 15 pairs of stated predictions are distinguishable — on the locus of decodable content, on onset–offset ignition versus sustained posterior activity, and on fronto-posterior versus within-posterior connectivity. That is exactly what Cogitate preregistered and tested, and Cogitate did discriminate on those pairs (IIT passed its duration prediction and failed sustained posterior synchrony; GNWT found prefrontal category decoding but no offset ignition and no identity decoding). Our sentence that a shared prediction cannot discriminate was therefore wrong as applied to M8 and has been withdrawn; what is true is that the six predictions share the *quantity* and differ in locus, timing and connectivity. Second, the M4 column — the one the Reviewer and we both prized as the adversarial cell — does not survive as contested once the quantity is stated precisely. We split it into three (Section 4b): M4a, access to interoceptive content as content; M4b, visceral modulation of access to exteroceptive content; M4c, conscious involvement in a purely autonomic conflict. Supramodular interaction theory's and passive frame theory's stated null is a prediction over M4c; the predictive-processing and neural-subjective-frame positives are predictions over M4a and M4b. They answer different questions, and no pair is distinguishable, so all three are occupied-not-contested. The sentence "M4 is the only contested column" has been withdrawn. A stated conflict over M4c would require an interoceptive-inference account to state that a purely autonomic conflict *is* consciously felt; we derived that prediction ourselves (P24) and it is labelled as our derivation, pending the proponents (see Section 6).

*The specific passages.* The §1 diagnosis (old ll. 49–54) is rewritten around the derived classes. The §9 sentence that a conflict-load effect discriminates against GNWT "which predicts none" (old ll. 783–786) is deleted. §9 now concedes that GNWT joined to any capacity assumption predicts that competing policies degrade access through load, notes that no coded account other than supramodular interaction theory states a prediction about incompatibility at matched load, and explains that the design therefore holds count, salience and load fixed and varies only shared-effector incompatibility — and that a positive result still refutes no silent theory. The abstract now says what the Reviewer identified as the paper's actual conclusion: the condition that can be run tests one stated single-occupant prediction and one derivation of ours, and its informative outcome is the null; the interoceptive conditions wait on a report-independent measure of access to interoceptive content that does not exist.

**Status:** DONE.
**Location of change:** Abstract; §1 Introduction (diagnosis paragraph); §7.4 Reading the columns; §7.7 What survives reclassification; §9 Conclusion; §9.1; Table S4 v2; `column_typology_v2.csv`.

### R1-2

> Three of the eight columns are the author's own. This is disclosed (ll. 476–479), and I am glad it was, but the sensitivity analysis offered in response tests the wrong proposition. Dropping M1, M2 and M5 and rechecking that M8 still dominates (ll. 479–484) establishes something nobody was going to contest. What it does not establish is that M5 is empty for an interesting reason. If M5 was specified as a coordinate of Arbitration Format Theory, then its emptiness across nine frameworks that all predate that theory is close to a tautology, and Table 1 records the fact rather than discovering it.
>
> What would carry weight is a column set generated independently of the author. Two routes, either acceptable to me. Take the dimensional scheme in the ConTraSt database, which the ms. already cites at l. 552 and which was assembled by people with no stake in this argument, and code against it. Or write to proponents of four or five of the theories, ask each what quantities they take their theory to be committed to, and code against the union. If empty columns survive either procedure, the finding is a finding. As the ms. stands, an unsympathetic reader can restate the whole of §7 as: my theory predicts things other theories do not predict.

**Response.** We agree that the sensitivity analysis tested the wrong proposition, and that sentence and the framing of the drop-M1/M2/M5 check as a test of independence are removed. We also agree with the tautology point as it applies to M5, and the text now says so: the thinness of a column relative to a column set chosen by someone whose theory occupies it is not evidence of anything until the column set has been checked against one that person did not choose.

*First route — taken, with a gap we name.* §7.5 reports Table S3: the accounts coded on the same scale against the twelve annotation dimensions of the ConTraSt database (type of consciousness; report/no-report; consciousness measure; paradigm; task; stimulus; population; technique; dependent measure; temporal, spatial and frequency findings). What it shows, stated without advocacy: along the author-external column set no dimension is empty — the accounts that are silent on M1, M2 and M5 speak on most of the axes the field's own inventory is organised on, so the theories are not uniformly underspecified; and none of M1, M2 or M5 corresponds to a ConTraSt field — no field counts concurrent response options, records conflict magnitude, or encodes joint cortical–autonomic coherence, although cortical connectivity tags and cardiac tags exist separately. §7.5 also states what this does not establish (ConTraSt records what authors reported, not what they could have varied; only two of its dimensions can carry predictions that differ in value, so it cannot say whether a column is contested) and its limits: the scheme was reconstructed from the database's methods description and live schema; it was done by one coder; and Table S3 covers 10 rows, not the 12 of Table S1 v2, because the neural subjective frame was added and the HOT/HOSS row was split after the ConTraSt coding was done. Those 24 cells are listed as outstanding (Section 6), and any S1–S3 comparison in the text is confined to the ten shared accounts.

*Second route — prepared, not taken.* Two letters to proponents have been drafted, each asking one answerable question about one register row (P24, the derived interoceptive-inference prediction over M4c, to its proponents; and the skeletomotor boundary of the conscious field, register rows P18 and P19, to the proponents of supramodular interaction and passive frame theory). They have not been sent at the time of writing. The manuscript says the route has not been taken and names it as the next check; if a reply arrives before final submission its content enters Table S4 verbatim, with permission, and the relevant cell is recoded from derived to stated.

*What we did instead to remove the author from the classification.* The column classes are now derived by script from the coding under a rule fixed in the codebook before the second coding starts (see R1-1); the codebook instructs the second coder not to let an expected class influence a code. This does not make the column *set* independent — only the second route does that — and §7.7 says so among the limitations.

**Status:** PARTLY (ConTraSt coding done for 10 of 12 accounts and reported; letters drafted but not sent; the author-chosen column set remains a stated limitation).
**Location of change:** §7.1 What is coded and why (column-set paragraph); §7.5 An independently generated column set; §7.7 limitations; Table S3; `s3_coverage_note.md`.

### R1-3

> §7.8 (ll. 647–653) states that the M5 result does not survive the least favorable reclassification: promote the four IMPLICIT cells and the empty column becomes four of nine. The abstract (ll. 13–14) carries the claim unqualified. One of those two has to change. My preference is that the M1/M2 result, which does survive, becomes the headline, and M5 is demoted to a secondary claim stated with the qualification attached.

**Response.** Done as the Reviewer prefers. The title no longer names a count of theories or a single empty quantity. The abstract leads with what the coding shows across all ten columns — that the stated commitments of the coded theories concentrate on a few quantities and that most of what the theories could be tested on is unmeasured — and states the M1/M2 result as the robust finding: single-occupant columns whose only stated occupant is supramodular interaction theory, and which no reclassification of borderline cells makes contested, since no account states that policy count or incompatibility does *not* affect access. M5 appears as thin (0 EXPLICIT, 5 INTERPRETED) with the qualification attached, and §7.7 spells out that promoting its INTERPRETED cells would fill the column, whereas promoting the INTERPRETED cells of M1 (one) and M2 (two) adds occupants from the same or a neighbouring family and creates no stated conflict.

**Status:** DONE.
**Location of change:** Title; Abstract; §7.4 ("Single-occupant: M1 and M2"; "Thin, not empty: M5"); §7.7 What survives reclassification.

### R1-4

> Tables S1 and S2 were not supplied. The captions say they "should be supplied" (ll. 503–504, 536), the Supplementary Materials section says they "should accompany the submission" (l. 829), and the Data Availability Statement says they are provided (ll. 837–839). Whatever the explanation, the consequence is that the entire evidential content of §7 was unavailable to me. I could not check a single cell, could not see which studies were counted as theory-addressed, and could not evaluate the IMPLICIT/NO boundary that the author himself identifies as bearing the weight. Everything I say about §7 below is about the argument as written, not about whether the coding supports it.

**Response.** See E1 for the three stages. What matters for this point: every cell the Reviewer could not check is supplied with this resubmission as a supplementary file, with its code, the claim in our words, the source, the source locus and whether the source was read in full or as an abstract (62 of the 120 cells rest on full text, 58 on abstracts; 28 of the 54 positive cells rest on abstracts, and the text says so). The IMPLICIT/NO boundary the Reviewer names is now the INTERPRETED/NOT_LOCATED boundary of codebook v2.0, with its decision rules written down so that the second coder — and the Reviewer — can apply them. Which studies count as theory-addressed is visible row by row in Table S2 v2, with the attribution split into three columns (R1-8). The captions of Tables 1 and 2 now point to the supplementary tables with no conditional wording.

**Status:** PREPARED (supplied with the resubmission; public deposit and DOI pending, as at E1).
**Location of change:** Table 1 and Table 2 captions; Supplementary Materials; Data Availability Statement; Table S1 v2; Table S2 v2.

### R1-5

> On the single coder: the author says a second coding and a kappa are "the necessary next step rather than an optional robustness check" (ll. 625–634). I would say necessary now. Seventy-two cells and thirty-six studies is a couple of afternoons for a competent second reader, the scheme is written down, and the whole argument turns on the judgment call the author has already flagged as the most contestable. I am not willing to endorse the coding without it.

**Response.** Accepted, and we will not ask the Reviewer to endorse the coding until the numbers are in. We report exactly what exists and what does not.

*Exists.* Codebook v2.0, frozen on 24 September 2026 with its SHA-256 hash printed in its footer (`1c18deae…cc1d06`); any change after the second coder starts is logged and forces re-coding of the affected cells by both coders. It contains operational definitions of the ten quantities, the decision rules for the five codes (EXPLICIT, INTERPRETED, NOT_LOCATED, NOT_APPLICABLE, UNRESOLVED), the attribution and inclusion rules for Table S2, and the primary sources per account. Blank forms: 120 rows for Table S1 and one row per experiment for Table S2. A second-coder pack (v3.1) that contains the frozen codebook (hash verifiable with `sed '$d' codebook_v2.md | shasum -a 256`), the blank forms, the manifests and the agreement script, and does *not* contain the first coder's codes, justifications, the prediction register (Table S4 lists every EXPLICIT cell and is released to the second coder only after Table S1 is returned) or the manuscript's results section. An agreement script (`agreement.py`) that computes raw agreement, the confusion matrix and nominal κ for the whole matrix and for stated subsets (per account, per column, positive versus null predictions, the INTERPRETED/NOT_LOCATED boundary), and writes the disagreement list for adjudication.

*Does not exist.* The second coding itself. It is planned, to be carried out by the second author, and has not begun at the time of writing. Every κ, agreement and disagreement count in §7.2 is a bracketed placeholder, and the Author Contributions statement does not yet credit validation (E2). We do not report the coding as validated anywhere.

*One limit on blindness, stated in the text rather than left to be found.* The second author has read the submitted manuscript, including its condensed Table 1. Blindness is therefore complete for the per-cell justifications and for the cells that did not exist in the submitted version — the M4a/M4b/M4c cells, the separated HOT and HOSS rows, passive frame theory and the neural subjective frame — and partial for the cells whose condensed code appeared in the submitted Table 1. Agreement will be reported for the two subsets separately as well as overall.

*On effort.* The codebook's own estimate is 6–10 hours for Table S1 and 2–3 hours for Table S2, because the coder is asked to read the primary sources rather than the summaries; this is more than the Reviewer's couple of afternoons and is the reason an extension of the revision deadline has been drafted (Section 6).

**Status:** PREPARED (codebook frozen, forms and script exist; the second coding and κ are outstanding).
**Location of change:** §7.2 Coding procedure; §7.7 limitations (first limitation); Declarations — Author Contributions; deposit files `codebook_v2.md`, `agreement.py`, second-coder pack v3.

### R1-6

> The nine theories. The stated rule (ll. 472–474) does not pick out these nine and no others — dendritic integration theory, temporo-spatial theory and active inference treated separately from predictive processing would all qualify on the same criterion. More importantly, two of the rows are doing a different job from the other seven. UAL and the Feinberg–Mallatt scheme are accounts of when and in which lineages consciousness appeared. They are not accounts of what makes a particular content accessible on a particular trial, and coding them silent on M8 records a difference of subject matter rather than a hole in a predictive apparatus. Since they contribute four of the absent cells in the M8 column and several elsewhere, this inflates exactly the unevenness the paper is arguing for.
>
> Two rows are also compounds. Collapsing SIT with passive frame theory is hard to square with §4 (ll. 283–293), where the ms. itself argues that the passive frame formulation gives up the variable a discriminating prediction would need. If the difference matters there, it should be two rows here. HOT/HOSS has the same problem in milder form.
>
> If the sample is purposive, say so in the terms already used for the study sample at ll. 634–638, and stop reporting the tallies as fractions of nine. Five of nine reads like an estimate of a population quantity and it is not one.

**Response.** All four parts accepted.

*The rule and what it admits.* §7.1 states the inclusion rule and the coverage aim, describes the theory sample as purposive in the terms already used for the study sample, and names the three accounts the Reviewer lists — dendritic integration theory, the temporo-spatial theory, and active inference treated apart from predictive processing — as meeting the rule and not coded, so that the omission is visible and a second coder can add them.

*Origin-level accounts.* Unlimited associative learning and the Feinberg–Mallatt scheme form their own block in Table 1 with their own tally and are excluded from the trial-level counts, for the reason the Reviewer gives and in his terms: a difference of subject matter, not a hole in a predictive apparatus. Where a quantity cannot be asked of an account at all, the code is NOT_APPLICABLE rather than NOT_LOCATED (two cells: unlimited associative learning on M8, and passive frame theory on M8, which declines the implementation level), so that an absence of subject matter is not counted as silence.

*Compound rows — both split.* Supramodular interaction theory and passive frame theory are two rows, each coded from its own statements; the split matters in exactly the way §4 says, since passive frame theory is INTERPRETED where supramodular interaction theory is EXPLICIT on M1 and M2. Higher-order thought theory and higher-order state space theory are also two rows now — a change from our first revision draft, in which they remained merged. The reason: when we checked the primary sources against each other, the state space formulation (Fleming, 2020) states a prediction the classical formulation (Lau and Rosenthal, 2011) does not — over the dimensionality of the represented state (register row P10) — and the two also differ on valence, where the classical formulation is INTERPRETED and the state space formulation is NOT_LOCATED; a merged row would have credited both with a prediction only one makes. Each is coded from its own source. The consequence is a matrix of 12 accounts × 10 quantities = 120 cells. Every cell produced by the two splits and by the M4 split (50 of the 120) is flagged *provisional* in Table S1 v2 until the second coding, and 15 cells are flagged for adjudication.

*Tallies.* Every tally is a count of coded accounts (*k* of *n*) and the text nowhere reports a fraction as an estimate of a population.

**Status:** DONE (the split cells are provisional pending the second coding, and are labelled so).
**Location of change:** §7.1 What is coded and why; §7.2; Table 1 (origin-level block; separate HOT and HOSS rows; SIT and PFT rows); §7.7 limitations (fourth limitation); Table S1 v2; `accounts_manifest.csv`.

### R1-7

> I may be wrong about this and the author may have a reason, but the claim that nobody operationalizes cortical–autonomic coherence as an access criterion (ll. 526–532) needs to be checked against the heartbeat-evoked response work, where cortical responses to a visceral signal are used to predict whether a stimulus is consciously detected, and against Tallon-Baudry's visceral-self proposal more generally. Respiratory-phase modulation of detection is adjacent. None of it is cited. An omitted literature is always awkward; an omitted literature sitting in the one column the paper says is empty is worse than awkward.

**Response.** The Reviewer was right. See E4 for the literature added, the neural subjective frame row, its codes, the withdrawn sentence and its replacement. We add one point specific to the Reviewer's phrasing: the visceral-self proposal is now coded as an account in its own right rather than absorbed into the interoceptive-inference row, because its stated predictions (cortical monitoring of cardiac and gastric input as a precondition of the first-person perspective) are its own.

**Status:** DONE.
**Location of change:** §7.4 ("Thin, not empty: M5"); Table 1; Table S1 v2 (neural subjective frame row); §7.7.

### R1-8

> The zeros in Table 2 appear only when the denominator drops from 33 to 27 (ll. 545–549), and the category that does the dropping, "theory-addressed," is never given an operational definition. Yang et al. (2007) and Gayet et al. (2016) turn up routinely in access debates, so excluding them is a substantive decision and it is the decision that produces the result. Give the inclusion rule, list which of the 36 fell on each side, and state how sensitive the zeros are to moving one study. If 0 of 27 becomes 1 of 27 under a reasonable alternative reading, the reader is entitled to know that before the abstract tells them the cell is empty.
>
> Separately, and easily fixed: the tally row counts Y(neg) as Y. The abstract and ll. 480–482 both say three of nine theories explicitly predict M4, which a reader will take to mean three theories agree the quantity matters. One of the three predicts that it does not. Report them apart.

**Response.** Accepted, and the inventory was rebuilt rather than annotated, because the Reviewer's question could not be answered honestly from the old table.

*Unit and denominator.* The unit is now the experiment, not the publication: Table S2 v2 has 42 experiments from 32 publications, with publication, study-family, experiment and sample identifiers. The four papers that define a paradigm but report no test of a theory (Melloni et al., 2023, the Cogitate protocol; Dehaene et al., 2006; Boly et al., 2017; Poehlman, Jantz and Morsella, 2012) are listed in `paradigm_sources.csv` with the rows that rely on them and are outside every denominator — in the submitted version they were inside it.

*The operational rule.* Theory attribution is recorded in three separate columns that are never merged: what the study's own authors name as the theory tested or borne on, with the locus in their text; whether a later paper that is a coded theory's primary statement cites the study, with the DOI and whether the citing sentence was read and names the theory; and the coder's own inference, marked as such. A study is *theory-addressed* in the baseline if and only if the first or the second column names a coded theory. Coder inference alone is never sufficient for the baseline; it enters only a sensitivity scenario.

*Which side each study fell on, and why the Reviewer's two examples fall where they do.* This is visible row by row in Table S2 v2. Yang, Zald and Blake (2007), Gayet et al. (2016) and Sheth and Pham (2008): in the texts we could check, their authors name no coded theory, and no coded theory's primary statement cites them; they are in the inventory and outside the baseline denominator. Whalen et al. (1998) is cited in the reference list of Dehaene and Naccache (2001), which makes it theory-addressed under the rule, but it is a contested row because access is suppressed by masking throughout rather than manipulated; it is excluded from the baseline and enters the first sensitivity scenario. We note that 19 of the 32 publications could be read only as abstracts, so the experiment partition and the attribution for those rows are provisional and are marked so.

*The baseline, and the sensitivity the Reviewer asked for, verbatim from §7.6.* Baseline: 30 experiments from 21 publications — neutral visual 18 of 30, neutral non-visual 3 of 30, competing motor policies 8 of 30 (7 skeletal, 1 autonomic-effector), valenced 0 of 30, interoceptive 1 of 30. Adding Whalen: valenced 1 of 31. Removing the metacognition rows: neutral visual 14 of 25. Accepting a later attribution only when its citing sentence was read and names the theory: 13 of 24. Strict attribution with every contested row removed (the most conservative reading): 10 of 21, the smallest neutral-visual share. Adding coder-inferred attribution: 22 of 35. No theory filter at all: neutral visual 22 of 39, valenced 3 of 39, interoceptive 3 of 39. Seven rows carry a contested-inclusion flag with a written reason. The old publication-level figures (21 of 27 with the paradigm rows inside the denominator; 19 of 24 without) are reproduced by the script as historical scenarios so that the reader can see what c* The interoceptive cell holds 1 of 30 in the baseline — Garfinkel et al., 2015, which the neural subjective frame programme cites, itself a contested inclusion — and is empty in the strict scenarios. The smooth-muscle control study of Morsella, Gray and Krieger, 2009, which the earlier version counted as interoceptive, is re-coded as motor conflict at an autonomic effector: the content whose access it measures is the experienced conflict between a sustained intention and the pupillary reflex, not a visceral afferent signal. The class definitions were sharpened in the codebook (v2.1) before the second coding begins; interoceptive now means content from visceral afferents or autonomic modulation of access, and motor conflict is split by effector. The abstract carries no interoceptive count; §7.6 gives the baseline and the strict scenario. The valenced cell is zero in the baseline and non-zero under two reasonable readings, and the abstract carries the imbalance, not the zero. The sentence that the valenced and interoceptive literature "is claimed by no coded theory" has been withdrawn as too strong: what the table supports is a statement about the checked sample under the stated attribution rule, and that is how it is now written. and that is how it is now written.

*Y(neg).* In the new code set a stated null is an EXPLICIT prediction with polarity *null*, and it is reported apart everywhere: Table 1 has separate tally entries for positive and null EXPLICIT codes; the two null cells in the matrix (supramodular interaction theory and passive frame theory on M4c) are never summed with positive predictions, and the text nowhere says that three theories predict M4.

**Status:** DONE (experiment-level partition and attribution for abstract-only publications provisional, as labelled).
**Location of change:** §7.6 Table 2: content inventory (rule, baseline, sensitivity paragraph); Table 2; §7.2 (polarity); Table 1 tally rows; Abstract; Table S2 v2; `paradigm_sources.csv`; `s2_sensitivity.csv`; `S2_inclusion_criteria_v2.txt`.

### R1-9

> §7.7 (ll. 604–623) corrects a formulation in the author's companion framework. It may well be a good correction. It is theory development and it does not belong in a review that insists four times over that it is not arguing for the theory. Move it to the companion paper. The single sentence at ll. 822–825 is the right amount of signposting and should be the only such passage in the manuscript.

**Response.** The old §7.7 is deleted from the review and kept by the authors for the companion paper. We then applied the Reviewer's principle to §9.1, where our first revision draft had labelled contrasts by the companion theory's predictions: those predictions are removed from §9.1. The condition is now stated entirely in terms of the register: C0 tests P16, a prediction stated by supramodular interaction theory; C1a tests P23, which is our extension of that theory and is labelled as the authors' derivation; the coupling index and the valence interaction are estimation. The single companion-paper sentence at the close of §9 is the only such passage in the manuscript.

**Status:** DONE.
**Location of change:** old §7.7 (deleted); §9.1 (contrast labels); §9 (closing paragraph).

### Minor and editorial issues

#### R1-m1

> Three different 2020 items by Birch sit in the reference list (refs 21, 22, 23) and the in-text form "Birch et al., 2020" is used for at least two of them, l. 116 and again l. 179. Needs a/b/c.

**Response.** Resolved by the change to numbered citations (E7); each item has its own number.
**Status:** DONE. **Location of change:** References; §2 and §3 citations.

#### R1-m2

> Percentages to one decimal on denominators of 27 and 33, single-coded, from a purposive sample (ll. 537–549). 81.5% is 22 of 27. Use the fractions and drop the decimals throughout; the false precision undercuts the candor of §7.8.

**Response.** Every percentage is removed; all counts are *k* of *n* with the denominator named.
**Status:** DONE. **Location of change:** §7.3; §7.4; §7.6; §7.7; Abstract; §9.

#### R1-m3

> Spelling switches between conventions, and in one case switches on the same word: "operationalized" at l. 14 of the abstract against "operationalised" at l. 78. "judgement," "organisation" and "synchronisation" are British throughout. MDPI takes either. Pick one and run it through.

**Response.** British spelling throughout; the text was searched for the American forms of the words the Reviewer names and none remains.
**Status:** DONE. **Location of change:** throughout.

#### R1-m4

> Words have lost spaces or hyphens in the file I received: "metaanalysis" (l. 319), "loadbearing" (l. 313), "noreport" (l. 439), "corticaland-autonomic" (l. 526), "reportindependent" (l. 573), "secondorder" (l. 658), and "Conflicts of Interest:The" (l. 844). Some of these may be conversion artifacts rather than the author's.

**Response.** They were conversion artefacts: "meta-analysis", "load-bearing", "no-report", "cortical and autonomic", "report-independent", "second-order" and "Conflicts of Interest: The" are correct in the source. The PDF for this resubmission is generated by a different route (markdown → DOCX/PDF) and the joined forms are searched for before upload; that check is listed among the author actions in Section 6 because it has to be repeated on the final build.
**Status:** PARTLY (source correct; the check on the final PDF is an author action). **Location of change:** throughout; production check.

#### R1-m5

> Maturana and Varela is given inline with full bibliographic detail and a "no DOI" note at ll. 141–143, and the New York Declaration the same way at ll. 188–189. Both should go in the reference list in the normal format.

**Response.** Both are in the reference list in MDPI form and are cited by number.
**Status:** DONE. **Location of change:** §3; §3 (Declaration); References.

#### R1-m6

> §3–5 run to something like 40% of the text and are largely separable from the coding contribution. They are good, but a reader who has come for the measurement argument waits a long time for it. I would cut them by roughly a third, keeping the closing judgments, which are the parts that earn their keep.

**Response.** Done. Counted on the current text against the submitted version: §3 from 814 to 490 words, §4 from 1,067 to 663, §5 from 932 to 677 — 2,813 to 1,830 in all, a cut of roughly a third. The closing judgement of each section is kept, and the passage in §4 that separates supramodular interaction theory from passive frame theory is kept intact because Table 1 now depends on it (R1-6). References cited only in the removed passages have dropped out of the list.
**Status:** DONE. **Location of change:** §3 From regulation to a minimal bearer; §4 Arbitration as a function; §5 Valence and organism-wide reconfiguration.

#### R1-m7

> The judgment-at-the-end-of-every-section device works, but by §8 it has become a tic, and at l. 748 ("Three dissociations are named and none measured") it overstates what §8.2 has just conceded about option generation at ll. 714–719. Vary it.

**Response.** The §8 closing is rewritten under a new heading, "What is measured and what is not", as an uneven ledger that matches what §8.2 concedes about option generation: metacognitive precision has validated instruments and no experiment asking whether precision gates access; policy candidacy is measured in part; write-back has been demonstrated but not turned into a measure. "Three dissociations are named and none measured" is removed, and the closing device is varied across §8.
**Status:** DONE. **Location of change:** §8.4 What is measured and what is not.

#### R1-m8

> Mudrik et al. 2026, Dellert et al. 2025 and the two 2025 Nature Neuroscience pieces have load-bearing and too recent for me to have verified pagination or attribution. Flagging for the production check, not as errors.

**Response.** All four were re-verified against CrossRef records while preparing this response: Mudrik, Faivre, Pitts and Schurger (2026), *Trends in Cognitive Sciences* 30(8), 687–699; Dellert et al. (2025), *Current Biology* 35(23), 5721–5733.e3; IIT-Concerned et al. (2025), *Nature Neuroscience* 28(4), 689–693; Tononi et al. (2025), *Nature Neuroscience* 28(4), 694–702. No discrepancy in volume, issue, pages or attribution.
**Status:** DONE. **Location of change:** References.

---

## 3. Reviewer 2

> The manuscript is well written and comprehensive. However, the authors have neglected the two most significant works on consciousness: 1. Kuhn, R.L. (2024) A landscape of consciousness: toward a taxonomy of explanations and implications. Progress in Biophysics and Molecular Biology 190, 28–169. 2. Poznanski, R.R. (2026) Processual relational geometry: generative unfolding and self-intending closure constituting consciousness — a transscale ontophysical framework. Journal of Multiscale Neuroscience 5, 30–53. Both papers deal with ontological predictors of consciousness, not necessarily cortical signatures. The second reference in particular is required where the author claims on p8 that "few theories predict phenomenality rather than access". In addition, the word "nine" should be removed from the title.

### R2-1

> Cite Kuhn (2024).

**Response.** Added and used substantively in §6.2. Kuhn's taxonomy is the natural frame for the distinction §6.2 draws between frameworks that address phenomenality at the ontological level and theories that state a measurable prediction; we note that the taxonomy does not attempt to adjudicate among theories, and that whole regions of it contribute no row to Table 1 because they state no measurable quantity — which is a fact about the inclusion rule of §7, not a judgement on those frameworks.
**Status:** DONE. **Location of change:** §6.2 Who predicts phenomenality; References.

### R2-2

> Cite Poznanski (2026) at the "few theories predict phenomenality rather than access" passage.

**Response.** Cited at that passage in §6.2, in one sentence, as an example of a framework that addresses phenomenality at the ontological level and, as presented, states no measurable prediction — and so falls outside the inclusion rule of §7. We should be clear about the scope of the change: the sentence the Reviewer points to concerns predictive content, not the number of frameworks that address phenomenality, and the added citation illustrates that distinction rather than altering it. The full text was not accessible to us; the characterisation rests on the published abstract, hence "as presented". The bibliographic record (volume 5, pages 30–53) is as the Reviewer gives it; confirming the DOI against the journal's record before final submission is on the authors' list (Section 6).
**Status:** DONE. **Location of change:** §6.2 Who predicts phenomenality; References.

### R2-3

> Remove "nine" from the title.

**Response.** Done. The title no longer contains a count of theories; see R1-3 for the reasoning behind the new title.
**Status:** DONE. **Location of change:** Title; running head.

---

## 4. Changes prompted by internal re-audit

None of the following was requested by a reviewer. Each was found when we rebuilt the tables so that every number in the text is produced by script, and each changes a claim of the submitted version or of our own first revision draft. We list them so that they are reviewed rather than discovered.

**(a) M8 was called shared and treated as non-discriminating; it is contested, on one pair.** The submitted version described the cortical signature of access as a column on which predictions converge, and drew the conclusion that an experiment on it "tests many and discriminates none". Our first revision draft over-corrected: it counted 15 "distinguishable" pairs of stated predictions and called the column contested "at locus, timing and connectivity". A second internal audit pointed out that differing descriptions are not contradicting predictions — a locus claim beside a timing claim is not a disagreement — so every cross-theory pair of stated predictions in M8 (54 pairs) was entered in a deposited pair register with its shared condition, shared observable and a four-way relation. The result: 42 pairs are *different* (no shared observable), 10 *jointly compatible*, 2 *discriminating* and none *incompatible*. The column is contested on the strength of the two: the GNWT–IIT pair on temporal profile (offset-locked ignition against sustained activation with no offset event), which is the pair Cogitate operationalised and tested, and — at low confidence and flagged — the recurrent-processing–higher-order pair on the necessity of dorsolateral prefrontal function for awareness at matched performance. The statement in §6.4, §7.4 and §9 is now that the M8 predictions share the *quantity* and are contested at one value, the temporal profile. The definition of *contested* in §7.3 has been rewritten so that it requires a discriminating pair, and the sentence that only a contested column lets a stated prediction lose has been withdrawn: a single stated prediction can fail on its own; what a contested column adds is a result that favours one occupant over another. The same rule moved M6 from "contested at low confidence" to occupied-not-contested, because the IIT and higher-order state space statements on dimensionality concern different variables.

**(b) M4 split into M4a, M4b, M4c; "the only contested column" withdrawn.** "Autonomic/interoceptive channel involvement" conflated three quantities: access to interoceptive content as content (M4a), visceral modulation of access to exteroceptive content (M4b), and conscious involvement in a purely autonomic conflict (M4c). Once separated, the stated null of supramodular interaction theory and passive frame theory is a prediction over M4c (and, on our reading of the primary text, an exclusion from the *function* of the conscious field rather than a denial that bodily feelings exist — the manuscript's wording has been corrected accordingly), while the positives of predictive processing, the neural subjective frame and the Feinberg–Mallatt scheme are predictions over M4a and M4b. No pair of stated predictions in M4a or M4c is discriminating, so both are *occupied-not-contested* by the derived rule; M4b, after the predictive-processing cell was re-coded from EXPLICIT to INTERPRETED (the coded sentence reviews evidence rather than stating a framework prediction), has one stated occupant and is *single-occupant*. The claim that M4 is the only contested column, and the abstract's description of it as carrying opposed predictions, are withdrawn. What would make M4c contested is a stated interoceptive-inference prediction that a purely autonomic conflict is felt; we have derived it (P24) and labelled it as our derivation pending the proponents. The 36 M4a/b/c cells are provisional pending the second coding. This changes what §9 says about "the condition that discriminates cannot be run": it is now "the condition that *would* discriminate, if the proponents state the prediction we have derived for them, cannot yet be run".

**(c) Table S2 rebuilt at experiment level; paradigm papers out of the denominator; attribution split.** Described at R1-8. The consequences for the numbers: the submitted 21 of 27 (publication level, paradigm-defining rows inside the denominator) becomes 18 of 30 experiments at baseline, with the neutral-visual share ranging from 10 of 21 (strict attribution, all contested rows removed) to 22 of 35 (coder inference admitted) across the sensitivity scenarios; the interoceptive cell is 1 of 30 at baseline and 0 under strict attribution; the valenced cell is 0 of 30 at baseline and 1 of 31 or 3 of 39 under alternative readings. The statement "no theory claims this literature" is withdrawn and replaced by a statement about the checked sample under the stated rule.

**(d) §9.1 redesigned; N recomputed.** Described at E5. The first revision draft's design (three rules over the same keys, N = 126, sequential Bayes-factor monitoring) confounded the number of distinct responses with incompatibility and is replaced by three co-executable responses on three effectors, with incompatibility as the number of shared-effector pairs (0/1/3) and a separate count branch. N = 120 fixed (119 required for 90 % power at dz = 0.30 on C0 and C1a); no sequential monitoring; valence moved to Study 2 in Protocol S5; the coupling index and the interaction preregistered as estimation only. We also withdrew the sentence that "three quantities from Table 1 then become jointly observable for the first time", which the redesigned condition does not support.

**(e) Codebook v2.2 frozen with a verifiable hash; second coding planned with partial blindness stated.** Described at R1-5. The freeze (24 September 2026; SHA-256 of the file above its footer, checkable with one shell command) precedes the second coder's start. Two earlier versions of the coder pack were not blind — the first carried the prediction register, the second reproduced the first coder's row-level Table S2 decisions inside the codebook — and both were caught by internal audit before anything was sent; the pack now contains no first-coder codes, decisions or predictions, and the register is released only after Table S1 is returned; the limit on blindness — the second author has read the submitted manuscript's condensed Table 1 — is stated in §7.2 and agreement will be reported separately for the cells whose codes appeared in the submitted version and for the cells that did not exist then.

**(g) Five cells re-coded by the first coder after a second pass; codes from unreachable sources marked provisional.** Three cells carried codes that their own adjudication notes contradicted — two HOSS cells inherited the merged HOT/HOSS row's code although the HOSS source contains no statement, and one predictive-processing cell was kept EXPLICIT against the boundary rule the note applied — and were brought into line (NOT_LOCATED, NOT_LOCATED, INTERPRETED). A full-text pass over the eight flagged cells that rested on abstracts or on an unread book reached 3 of 12 sources; on that reading two INTERPRETED cells (Feinberg–Mallatt × M4c, predictive processing × M2) became NOT_LOCATED, with the sections searched recorded in the table. The codes of the five cells whose sources remain closed to us are marked provisional. The previous code is kept beside the current one in every re-coded cell. Totals moved from 22/32/64 to 21 EXPLICIT / 29 INTERPRETED / 68 NOT_LOCATED; the register's stated count from 28 to 27.

**(h) Scripts hardened after the audit found them permissive.** `agreement.py` had flagged "none named (...)" attributions as attributions, accepted any vocabulary and any incomplete matrix, and let a duplicated row pass; it now parses attribution structurally, compares theory-id sets, enforces the codebook vocabularies and the 12 × 10 grid, keeps UNRESOLVED as its own category, and fails on the five planted defects in its self-test. `reproduce.py` had reported PASS with the mixed-model simulations skipped; it now fails when statsmodels is absent unless the skip is requested explicitly, checks the simulation count in the output, and adds the Table 2, sensitivity, S3 and pair-register steps to the chain (10 steps). Table S2 now carries a unit-type column (experiment, experiment group, publication-as-one where the partition could not be verified from the abstract) and Table 2 is reported at both publication (21) and experiment (30) level.

**(f) The highlighting is a reconstructed text comparison.** The revised manuscript is authored in markdown; the yellow highlighting in the DOCX and PDF marks every passage inserted or rewritten relative to the submitted text and was produced by comparing the two texts, not by Word Track Changes. Deletions are listed in Section 5. Passages that were only renumbered or re-cited are not highlighted.

Two further corrections from the source check that accompanied the re-audit: the word "durably" was removed from the description of Hall et al. (2012), who measured immediate detection and justification only; and the Rounis et al. (2010) TMS result is now cited together with the Ruby et al. (2018) critique and the Bor et al. (2018) reply, with the dispute left open.

---

## 5. Sentences withdrawn or deleted (not visible in the highlighting)

1. "a prediction shared with competitors cannot discriminate" as applied to M8 (§1, §6.4, §7.4, §9) — replaced by "shared at the quantity, contested at locus, timing and connectivity".
2. "M4 is the only contested column" / "autonomic channel involvement … carries opposed predictions" (Abstract, §7.4, §7.7, §9) — replaced by the three occupied-not-contested columns M4a/M4b/M4c.
3. "Three quantities from Table 1 then become jointly observable for the first time" (§9).
4. "which predicts none" — the claim that a conflict-load effect discriminates against GNWT (old ll. 783–786, §9).
5. "none operationalises it" — of cortical–autonomic coherence (old ll. 526–532, §7.3/§7.4).
6. The emptiness of M5 is "for theoretical rather than technical" reasons, and the drop-M1/M2/M5 sensitivity check as a test of independence (old §7.6).
7. "the valenced and interoceptive access literature … is claimed as evidence by no coded theory" — replaced by a statement about the checked sample under the stated attribution rule (§7.6, Abstract).
8. "three of nine theories explicitly predict M4" (Abstract, old ll. 480–482).
9. "Three dissociations are named and none measured" (old l. 748, §8).
10. Old §7.7, the correction to the companion framework (about 320 words), and the companion theory's prediction labels in the first-draft §9.1.
11. "durably", of Hall et al. (2012).
12. Every percentage; the title's "nine".

---

## 6. Outstanding before final submission (authors)

These items cannot be completed by editing the text and are not reported as done anywhere in the manuscript or in this response.

1. **Second coding of Tables S1 v2 and S2 v2** by the second author from the v3 pack; run `agreement.py`; fill the κ, agreement and disagreement placeholders in §7.2 with pre-adjudication values; adjudicate and deposit the adjudication record; then activate the *validation* line in the Author Contributions statement. If the second coding cannot be completed within the deadline, the fallback is to withdraw every provisional count from the abstract and §7 and present the audit as a single-coder inventory.
2. **Extension of the revision deadline.** A request has been drafted; it has not been sent. It should go through the editorial system before the current deadline and must not describe the second coding as complete.
3. **Letters to proponents.** Two letters drafted (P24 to the interoceptive-inference proponents; P18/P19, the skeletomotor boundary, to the supramodular interaction / passive frame proponents); not sent. Record the date sent; if a reply arrives, enter it in Table S4 verbatim with permission and recode the cell from derived to stated.
4. **Deposit.** Reserve a DOI (Zenodo or OSF); upload deposit package v2; replace `[10.xxxx/PLACEHOLDER]` in Supplementary Materials, §7.2 and the Data Availability Statement with the same identifier.
5. **Table S3 completion.** Code the neural subjective frame and the separated HOSS row against the twelve ConTraSt dimensions (24 cells) so that S3 matches the 12 accounts of S1 v2; until then any S1–S3 comparison is confined to the ten shared accounts, as the text states.
6. **Full-text confirmation of abstract-only sources** on which locus claims rest (Lau and Rosenthal, 2011; Lamme, 2006; Lamme and Roelfsema, 2000; Park and Tallon-Baudry, 2014; Azzalini et al., 2019; Morsella, 2005, whose body text could not be retrieved), and correction of the author order of Webb and Graziano (2015) with the attention-schema locus re-anchored to Kelly et al. (2014).
7. **Names, affiliations, corresponding author, funding**, the conflicts-of-interest sentence (the manuscript argues at length with supramodular interaction theory; any professional relationship with its proponents belongs there), and the name and version of the generative-AI tools.
8. **Production checks on the final PDF:** search for the joined forms listed at R1-m4; confirm the Poznanski (2026) DOI against the journal's record; confirm that the highlighting in the final PDF is complete after the last edit.

---

## Appendix. Status by comment

| Comment | Status | Comment | Status |
|---|---|---|---|
| E1 | PREPARED | R1-7 | DONE |
| E2 | PARTLY | R1-8 | DONE |
| E3 | PREPARED | R1-9 | DONE |
| E4 | DONE | R1-m1 | DONE |
| E5 | PREPARED | R1-m2 | DONE |
| E6 | DONE | R1-m3 | DONE |
| E7 | DONE | R1-m4 | PARTLY |
| R1-1 | DONE | R1-m5 | DONE |
| R1-2 | PARTLY | R1-m6 | DONE |
| R1-3 | DONE | R1-m7 | DONE |
| R1-4 | PREPARED | R1-m8 | DONE |
| R1-5 | PREPARED | R2-1 | DONE |
| R1-6 | DONE | R2-2 | DONE |
| | | R2-3 | DONE |
