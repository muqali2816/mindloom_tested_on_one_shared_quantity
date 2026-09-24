# build_s2_v2.py — Table S2 v2 (unit = one empirical experiment) and paradigm_sources.csv
# All codes below were entered after reading the source named in evidence_status (full text or abstract).
# Derived fields (content_class_v2, theory_addressed, theory_addressed_strict) are computed, never typed.
import csv, json, re

legacy = {r['citation_label']: r for r in csv.DictReader(open('base/dep13/deposit/Table_S2_content_inventory.csv'))}
meta = json.load(open('handoff/meta.json'))

FT = 'full text read'
AB = 'abstract only (full text not accessible in sandbox)'

# ---------- A. paradigm sources ----------
paradigm_sources = [
 dict(publication_id='P02', citation_label='Melloni et al. 2023', doi='10.1371/journal.pone.0268577', type='preregistered protocol (no data)',
      what_it_defines='Preregistered adversarial-collaboration protocol (GNWT vs IIT): stimulus set (faces/objects/letters/false fonts), durations, task relevance, predictions and analysis plan for Experiments 1 and 2 (protocol §Methods, Figs 1–4)',
      used_by_rows='P01 (Cogitate Consortium et al. 2025, same study family F01)', evidence_status=FT),
 dict(publication_id='P05', citation_label='Dehaene et al. 2006', doi='10.1016/j.tics.2006.03.007', type='taxonomy / review of own paradigms',
      what_it_defines='Testable taxonomy of subliminal, preconscious and conscious processing built on visual masking and attentional-blink paradigms (cites Dehaene et al. 2001 and Sergent et al. 2005 as its empirical base)',
      used_by_rows='P04 (Dehaene et al. 2001), P07 (Sergent, Baillet & Dehaene 2005), P03 (Del Cul et al. 2007), P29 (Charles et al. 2013) — masking / attentional-blink family', evidence_status=AB),
 dict(publication_id='P15', citation_label='Boly et al. 2017', doi='10.1523/jneurosci.3218-16.2017', type='review (lesion and neuroimaging evidence)',
      what_it_defines='Front-versus-back framing of the content-NCC debate; Fig. 1 legend uses Lumer et al. 1998, Dehaene et al. 2001 (report-based contrasts) and Frässle et al. 2014 (report-independent contrast) as exemplar paradigms',
      used_by_rows='P09 (Lumer et al. 1998), P04 (Dehaene et al. 2001), P10 (Frässle et al. 2014); also cited by Melloni et al. 2023 (P02)', evidence_status=FT),
 dict(publication_id='P25', citation_label='Poehlman, Jantz & Morsella 2012', doi='10.3389/fpsyg.2012.00369', type='theory paper (no new data)',
      what_it_defines='Action-based framing of conscious broadcasting for skeletal muscle; supplies the theoretical rationale of the sustained-incompatible-intentions paradigm (cites Morsella, Gray & Krieger 2009)',
      used_by_rows='P22 (Morsella, Gray & Krieger 2009), P23 (Gray, Bargh & Morsella 2013), P24 (Morsella et al. 2009b)', evidence_status=FT),
]

# ---------- B. experiments ----------
# helper: one publication → list of experiment dicts
rows = []
def pub(pid, fam, label, year, paradigm, exps, common):
    for i, e in enumerate(exps, 1):
        r = dict(publication_id=pid, study_family_id=fam, experiment_id=f'{pid}-E{i}', citation_label=label,
                 doi=legacy[label]['doi'], year=year, paradigm=paradigm,
                 legacy_content=legacy[label]['content'], legacy_theory_addressed=legacy[label]['theory_addressed'])
        r.update(common); r.update(e)
        r.setdefault('sample_id', f'{pid}-E{i}-S1'); r.setdefault('ancillary_experiment', False)
        r.setdefault('contested_inclusion', False); r.setdefault('contested_reason', '')
        r.setdefault('theory_attribution_later', ''); r.setdefault('later_attribution_evidence', '')
        r.setdefault('theory_attribution_coder', ''); r.setdefault('notes', '')
        rows.append(r)

NONE = ''  # empty = no attribution located

pub('P01','F01','Cogitate Consortium et al. 2025',2025,'Suprathreshold viewing of faces/objects/letters/false fonts for 0.5/1.0/1.5 s, target detection; fMRI, MEG, iEEG',
 [dict(experiment_label='Experiment 1 of the preregistered protocol (three modality arms)', sample_id='P01-E1-S1;P01-E1-S2;P01-E1-S3',
       samples_detail='S1 fMRI: 120 tested, 108 analysed (12 excluded: motion, coverage, incomplete); S2 MEG: 102 tested, 97 analysed (5 excluded); S3 iEEG: 34 recruited, 32 implanted, 29 analysed',
       participants_total=256, participants_in_analysis=234, report_type='both (task-relevant targets reported; task-irrelevant stimuli seen without report)',
       theory_attribution_by_authors='GNWT vs IIT — title; abstract; preregistered predictions (Methods, Supplementary)',
       theory_attribution_later='', later_attribution_evidence='not needed (attribution by authors)')],
 dict(modality='visual', affective_status='neutral', manipulation='Stimulus category (face/object/letter/false font), orientation, duration, task relevance', measured_outcome='Decoding of conscious content and duration; sustained activity; fronto-visual synchrony (preregistered predictions)', evidence_status=FT))

pub('P03','F03','Del Cul, Baillet & Dehaene 2007',2007,'Backward masking of digits at variable SOA; EEG',
 [dict(experiment_label='Single experiment', participants_total=12, participants_in_analysis=12, samples_detail='12 participants; ERP seen/not-seen comparison at SOA 50 ms on a 9-participant subset with enough trials',
       report_type='report', theory_attribution_by_authors='GNWT — Introduction and Fig. 1 (schematic predictions of the "global neuronal workspace" model)',
       theory_attribution_later='GNWT: Mashour et al. 2020, doi:10.1016/j.neuron.2020.01.026 (cited as evidence for P300 ignition); PFT: Morsella et al. 2015, doi:10.1017/s0140525x15000643 (integration consensus)', later_attribution_evidence='context read')],
 dict(modality='visual', affective_status='neutral', manipulation='Target–mask SOA (masking strength)', measured_outcome='Subjective visibility, objective comparison accuracy, ERP components (nonlinear P3 transition)', evidence_status=FT))

pub('P04','F04','Dehaene et al. 2001',2001,'Masked vs unmasked word presentation, repetition priming; fMRI and ERP',
 [dict(experiment_label='fMRI and ERP study of masked words (partition into experiments not verifiable from abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract',
       report_type='report', theory_attribution_by_authors='not verifiable from abstract (no theory named in abstract)',
       theory_attribution_later='GNWT: Dehaene & Changeux 2011, doi:10.1016/j.neuron.2011.03.018; Dehaene et al. 2006, doi:10.1016/j.tics.2006.03.007; HOSS: Fleming 2020, doi:10.1093/nc/niz020; Boly et al. 2017 Fig. 1F (report-based fronto-parietal contrast; theory not named at locus)',
       later_attribution_evidence='reference list only (OpenAlex) except Boly et al. 2017 (context read, theory not named)',
       theory_attribution_coder='GNWT (authors are GNWT proponents; reduced prefrontal/parietal activation for unseen words is the GNWT signature) — coder inference')],
 dict(modality='visual', affective_status='neutral', manipulation='Masking of words (seen vs unseen), repetition', measured_outcome='fMRI activation and repetition suppression; ERP', evidence_status=AB))

pub('P06','F06','Salti et al. 2015',2015,'Threshold detection of a faint square with location report; EEG/MEG decoding',
 [dict(experiment_label='Single experiment', participants_total=17, participants_in_analysis=12, samples_detail='5 excluded for calibration failure; 12 analysed, one without EEG',
       report_type='report', theory_attribution_by_authors='GNWT — Introduction ("The Global Neuronal Workspace (GNW) model asserts…")',
       theory_attribution_later='GNWT: Mashour et al. 2020, doi:10.1016/j.neuron.2020.01.026 (decodable ignition)', later_attribution_evidence='context read')],
 dict(modality='visual', affective_status='neutral', manipulation='Near-threshold contrast; seen vs unseen at matched behaviour (blindsight trials)', measured_outcome='MVPA decoding of location on seen vs unseen trials; timing of divergence', evidence_status=FT))

pub('P07','F07','Sergent, Baillet & Dehaene 2005',2005,'Attentional blink with visibility ratings; ERP',
 [dict(experiment_label='Single ERP experiment (per abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract',
       report_type='report', theory_attribution_by_authors='not verifiable from abstract (abstract speaks of a "late wave… distributed network", no theory named)',
       theory_attribution_later='GNWT: Mashour et al. 2020, doi:10.1016/j.neuron.2020.01.026 (early processing preserved on unseen trials); Dehaene & Changeux 2011; Dehaene et al. 2006; RPT: Lamme 2010, doi:10.1080/17588921003731586',
       later_attribution_evidence='Mashour 2020 context read; others reference list only')],
 dict(modality='visual', affective_status='neutral', manipulation='Attentional blink (T2 seen vs unseen at identical stimulation)', measured_outcome='Visibility ratings; ERP divergence around 270 ms', evidence_status=AB))

pub('P08','F08','Sergent et al. 2021',2021,'Near-threshold vowels in noise; active (report) and passive (no-report) sessions; EEG',
 [dict(experiment_label='Main experiment (active and passive sessions)', participants_total=25, participants_in_analysis=20, samples_detail='25 recruited, 2 discontinued, 3 excluded; 20 analysed',
       report_type='both', theory_attribution_by_authors='GNWT — abstract/Discussion: tests and updates "predictions of the global neuronal workspace model"',
       theory_attribution_later='Melloni et al. 2023 protocol, doi:10.1371/journal.pone.0268577 (reference list)', later_attribution_evidence='reference list only'),
  dict(experiment_label='Control experiment 1: passive session only (naïve participants)', participants_total=10, participants_in_analysis=10, report_type='no-report', ancillary_experiment=True,
       theory_attribution_by_authors='GNWT — same framing as main experiment (Methods, "Control experiment 1")'),
  dict(experiment_label='Control experiment 2: vowels replaced by simple tones', participants_total=5, participants_in_analysis=5, report_type='not verified (design of control 2 not fully read)', ancillary_experiment=True,
       theory_attribution_by_authors='GNWT — same framing as main experiment (Methods, "Control experiment 2")')],
 dict(modality='auditory', affective_status='neutral', manipulation='Signal-to-noise ratio around audibility threshold; report vs no report', measured_outcome='Bifurcation in late EEG activity; prediction of audibility reports and of randomly sampled conscious contents', evidence_status=FT))

pub('P09','F09','Lumer, Friston & Rees 1998',1998,'Binocular rivalry (face vs grating) vs replay; fMRI',
 [dict(experiment_label='Single fMRI experiment (per abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract',
       report_type='report', theory_attribution_by_authors='not verifiable from abstract (no theory named; frontoparietal role in conscious perception asserted)',
       theory_attribution_later='GNWT: Dehaene & Naccache 2001, doi:10.1016/s0010-0277(00)00123-2 (reference list); Boly et al. 2017 Fig. 1E (report-based fronto-parietal contrast; theory not named at locus)',
       later_attribution_evidence='reference list only / Boly 2017 context read, theory not named',
       theory_attribution_coder='GNWT (frontoparietal correlates of perceptual switching) — coder inference; legacy also listed RPT, for which no source was located')],
 dict(modality='visual', affective_status='neutral', manipulation='Rivalrous vs non-rivalrous (replay) perceptual transitions', measured_outcome='fMRI activity time-locked to perceptual alternations', evidence_status=AB))

pub('P10','F10','Frässle et al. 2014',2014,'Binocular rivalry with OKN/pupil as objective readout; active-report vs passive (no-report); fMRI',
 [dict(experiment_label='Single fMRI experiment with active and passive conditions (per abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract',
       report_type='both', theory_attribution_by_authors='none named (abstract questions "the popular view of a driving role of frontal areas"; no theory label)',
       theory_attribution_later='Boly et al. 2017 Fig. 1G, doi:10.1523/jneurosci.3218-16.2017 (cited as evidence that report-independent correlates are posterior; theory not named at locus); NSF: Babo-Rebelo et al. 2016, doi:10.1523/JNEUROSCI.0262-16.2016 (reference list); Melloni et al. 2023 and Cogitate 2025 (reference lists)',
       later_attribution_evidence='Boly 2017 context read (theory not named); others reference list only',
       theory_attribution_coder='Bears on GNWT (frontal involvement) as a no-report challenge; legacy coded GNWT — coder inference')],
 dict(modality='visual', affective_status='neutral', manipulation='Report vs no report of rivalry alternations (gratings)', measured_outcome='fMRI correlates of alternations in frontal vs occipito-parietal cortex', evidence_status=AB))

pub('P11','F11','Tsuchiya & Koch 2005',2005,'Continuous flash suppression; negative afterimage strength',
 [dict(experiment_label='Psychophysical experiments (number not verifiable from abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract',
       report_type='report', theory_attribution_by_authors='not verifiable from abstract (no theory named)',
       theory_attribution_later='GNWT: Dehaene & Changeux 2011, doi:10.1016/j.neuron.2011.03.018 (reference list)', later_attribution_evidence='reference list only',
       theory_attribution_coder='IIT/RPT per legacy; no source located naming either — coder inference only')],
 dict(modality='visual', affective_status='neutral', manipulation='Perceptual suppression of an adaptor by CFS', measured_outcome='Afterimage strength; trial-wise visibility', evidence_status=AB))

pub('P12','F12','Pitts et al. 2014',2014,'Inattentional blindness with task-irrelevant textures; masking SOA; EEG (no-report during task, awareness assessed post hoc)',
 [dict(experiment_label='EEG experiment (a separate 12-participant behavioural calibration study set the SOAs; not counted as an access experiment)', participants_total=26, participants_in_analysis=18, samples_detail='26 tested; 3 excluded for EEG artefact, 5 for awareness of 16 ms stimuli',
       report_type='no-report (awareness assessed post hoc)', theory_attribution_by_authors='none named (full text: cites Dehaene & Naccache 2001 / Dehaene et al. 2006 for the definition of "access consciousness"; no theory tested or named)',
       theory_attribution_later='Boly et al. 2017, doi:10.1523/jneurosci.3218-16.2017 (reference list)', later_attribution_evidence='reference list only',
       theory_attribution_coder='GNWT-relevant (P3b dissociated from awareness) — coder inference; legacy coded GNWT')],
 dict(modality='visual', affective_status='neutral', manipulation='Awareness (aware vs unaware phase) × task relevance of line-texture shapes; masking SOA', measured_outcome='ERP components (VAN, P3b) as a function of awareness and task relevance', evidence_status=FT))

pub('P13','F13','Kronemer et al. 2022',2022,'Visual detection of faint discs at threshold; Report and Report + No-Report paradigms; hdEEG, fMRI, pupillometry, thalamic iEEG',
 [dict(experiment_label='Report Paradigm', sample_id='P13-E1-S1;P13-E1-S2;P13-E1-S3', samples_detail='S1 fMRI N=37 (34 in the reported fMRI analysis); S2 hdEEG+eye tracking N=59 (57 analysed); S3 patients with thalamic electrodes N=7 (6 with scalp+icEEG)',
       participants_total='144 healthy recruited across the four healthy data sets (publication level) + 7 patients', participants_in_analysis='fMRI 34; hdEEG 57; patients 7',
       report_type='report', theory_attribution_by_authors='none named (full text: Baars 2005 and Tononi et al. 2016 cited only as background refs 2–3; no theory tested)',
       theory_attribution_coder='GNWT per legacy — coder inference only'),
  dict(experiment_label='Report + No-Report Paradigm (eye-metric classification of perceived vs not perceived)', sample_id='P13-E2-S1;P13-E2-S2', samples_detail='S1 fMRI+eye tracking N=65; S2 hdEEG+eye tracking N=65',
       participants_total='see E1 (144 healthy recruited at publication level)', participants_in_analysis='fMRI 65; hdEEG 65',
       report_type='both', theory_attribution_by_authors='none named (as E1)', theory_attribution_coder='GNWT per legacy — coder inference only')],
 dict(modality='visual', affective_status='neutral', manipulation='Perceived vs not perceived threshold stimuli; report vs no report', measured_outcome='ERPs, fMRI network changes, thalamic awareness potential', evidence_status=FT))

pub('P14','F14','Dellert et al. 2025',2025,'No-report inattentional deafness; aware vs unaware groups; fMRI',
 [dict(experiment_label='Single fMRI experiment (per abstract)', participants_total=63, participants_in_analysis='not stated in abstract', report_type='no-report',
       theory_attribution_by_authors='not verifiable from abstract ("prominent theories disagree about sensory versus fronto-parietal activity"; no theory named in abstract)',
       theory_attribution_coder='GNWT vs IIT framing per legacy — coder inference only')],
 dict(modality='auditory', affective_status='neutral', manipulation='Awareness of task-irrelevant critical sounds (between-group aware vs unaware)', measured_outcome='fMRI activation in auditory vs fronto-parietal/attention regions', evidence_status=AB))

pub('P16','F16','Maniscalco & Lau 2012',2012,'2-interval forced-choice visual task with confidence ratings; meta-d′ estimation',
 [dict(experiment_label='Single experiment accompanying the method', participants_total=30, participants_in_analysis=30, samples_detail='30 participants per Methods (count confirmed by the first coder; abstract read here)',
       report_type='report', theory_attribution_by_authors='not verifiable from abstract (measurement paper; no theory named)',
       theory_attribution_later='HOT: Brown, Lau & LeDoux 2019, doi:10.1016/j.tics.2019.06.009 (reference list); HOSS: Fleming & Daw 2017, doi:10.1037/rev0000045 (context read: cited for the meta-d′ method, not as evidence)',
       later_attribution_evidence='reference list / method citation only', theory_attribution_coder='HOT/HOSS measurement framework (codebook §5) — coder inference',
       contested_inclusion=True, contested_reason='metacognitive index, not access manipulation')],
 dict(modality='visual', affective_status='neutral', manipulation='None over access; confidence ratings on a visual discrimination', measured_outcome='Metacognitive sensitivity (meta-d′) relative to d′', evidence_status=AB))

pub('P17','F17','Rounis et al. 2010',2010,'Bilateral theta-burst TMS to DLPFC; visual discrimination with visibility ratings',
 [dict(experiment_label='Single experiment (per abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract', report_type='report',
       theory_attribution_by_authors='not verifiable from abstract (no theory named; PFC activations "may reflect a critical metacognitive process")',
       theory_attribution_later='HOSS: Fleming & Daw 2017, doi:10.1037/rev0000045 (context read: evidence for PFC role in confidence); HOT: Lau & Rosenthal 2011, doi:10.1016/j.tics.2011.05.009; Brown, Lau & LeDoux 2019 (reference lists); GNWT: Dehaene & Changeux 2011 (reference list)',
       later_attribution_evidence='Fleming & Daw 2017 context read; others reference list only',
       contested_inclusion=True, contested_reason='metacognitive index, not access manipulation (TMS alters visibility ratings/metacognitive sensitivity with d′ unchanged)')],
 dict(modality='visual', affective_status='neutral', manipulation='TMS to DLPFC vs control; stimulus discrimination held constant', measured_outcome='Visibility ratings and metacognitive sensitivity (type-2 SDT)', evidence_status=AB))

pub('P18','F18','Fleming et al. 2010',2010,'Perceptual 2-IFC with confidence; VBM/DTI',
 [dict(experiment_label='Single experiment', participants_total=32, participants_in_analysis=32, report_type='report',
       theory_attribution_by_authors='none named (full text: no theory of consciousness named)',
       theory_attribution_later='HOSS: Fleming & Daw 2017, doi:10.1037/rev0000045 (context read: aPFC role; data set re-used); HOT: Lau & Rosenthal 2011 (reference list); GNWT: Dehaene & Changeux 2011 (reference list)',
       later_attribution_evidence='Fleming & Daw 2017 context read; others reference list only',
       contested_inclusion=True, contested_reason='metacognitive index, not access manipulation (individual differences in confidence–accuracy correspondence)')],
 dict(modality='visual', affective_status='neutral', manipulation='None over access; inter-individual metacognitive accuracy at matched performance', measured_outcome='Metacognitive accuracy vs grey-matter volume and white-matter microstructure', evidence_status=FT))

pub('P19','F19','Fleming et al. 2014',2014,'Perceptual and memory tasks with confidence in aPFC lesion patients vs comparison groups',
 [dict(experiment_label='Single experiment (three groups)', sample_id='P19-E1-S1;P19-E1-S2;P19-E1-S3', samples_detail='S1 anterior PFC lesion n=7; S2 temporal-lobe lesion n=11; S3 healthy controls n=19',
       participants_total=37, participants_in_analysis=37, report_type='report',
       theory_attribution_by_authors='none named (full text: Lau & Rosenthal 2011 cited among evidence for aPFC in metacognition; no theory tested)',
       theory_attribution_later='HOSS: Fleming & Daw 2017, doi:10.1037/rev0000045 (context read: lesion evidence for PFC in confidence); HOT: Brown, Lau & LeDoux 2019 (reference list)',
       later_attribution_evidence='Fleming & Daw 2017 context read; Brown 2019 reference list only',
       contested_inclusion=True, contested_reason='metacognitive index, not access manipulation (domain-specific meta-d′ deficit)')],
 dict(modality='visual', affective_status='neutral', manipulation='Lesion group (aPFC vs temporal vs control) × domain (perception vs memory)', measured_outcome='Metacognitive accuracy (meta-d′) with performance matched', evidence_status=FT))

pub('P20','F20','Dijkstra & Fleming 2023',2023,'One-trial-per-participant imagery/perception judgements; reality threshold model (fMRI re-analysis of an earlier data set not counted as a new experiment)',
 [dict(experiment_label='Experiment 1 (online, one trial per participant)', participants_total=400, participants_in_analysis=272, report_type='report',
       theory_attribution_by_authors='HOT — Discussion: results "in line with both higher-order theories of consciousness and recent models of… perceptual reality monitoring" (consistency claim, not a stated test)'),
  dict(experiment_label='Experiment 2 (online, one trial per participant)', participants_total=461, participants_in_analysis=339, report_type='report',
       theory_attribution_by_authors='HOT — as Experiment 1 (Discussion)')],
 dict(modality='visual', affective_status='neutral', manipulation='Imagined vs presented gratings; signal strength / vividness', measured_outcome='Reality judgements; vividness; model comparison', evidence_status=FT))

pub('P21','F21','Wilterson et al. 2020',2020,'Cued attention tasks with awareness of cue or of cue–target contingency manipulated (eight experiments per abstract)',
 [dict(experiment_label='Experiments 1–6 (cue-awareness and contingency-awareness manipulations; per-experiment partition not verifiable from abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract',
       report_type='report', theory_attribution_by_authors='AST — abstract: "over six experiments, we examined… to test predictions of AST"',
       notes='Abstract reports eight experiments in total; only the abstract could be read, so the eight are carried as two blocks (1–6 and 7–8) rather than eight rows; this understates the experiment count for this publication'),
  dict(experiment_label='Experiments 7–8 (implicit attention shift generalisation; per abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract',
       report_type='report', theory_attribution_by_authors='AST — abstract ("Each of these findings matched predictions of AST")')],
 dict(modality='visual', affective_status='neutral', manipulation='Visual awareness of the cue; awareness of the cue–target contingency', measured_outcome='Exogenous and endogenous attention effects (reaction time)', evidence_status=AB))

pub('P22','F22','Morsella, Gray & Krieger 2009',2009,'Sustaining identical, compatible or incompatible intentions without movement; introspective ratings of "activity"',
 [dict(experiment_label='Study 1: arm movements (reach vs wiggle)', participants_total=18, participants_in_analysis=18, report_type='report',
       theory_attribution_by_authors='SIT — Introduction: "This hypothesis is from a theory (Morsella, 2005) in which the primary function of consciousness is to integrate potentially conflicting skeletomotor intentions"',
       theory_attribution_later='PFT: Morsella et al. 2015, doi:10.1017/s0140525x15000643 (context read; cited as evidence)', later_attribution_evidence='context read',
       modality='motor', affective_status='neutral'),
  dict(experiment_label='Study 2: finger movements', participants_total=14, participants_in_analysis=14, report_type='report',
       theory_attribution_by_authors='SIT — as Study 1', theory_attribution_later='PFT: Morsella et al. 2015 (context read)', later_attribution_evidence='context read',
       modality='motor', affective_status='neutral'),
  dict(experiment_label='Control study: smooth-muscle (pupillary light reflex) conflict vs no conflict', participants_total=14, participants_in_analysis=14, report_type='report', ancillary_experiment=True,
       theory_attribution_by_authors='SIT — corollary hypothesis that conflict outside the skeletomotor system produces no subjective effect (Introduction; Control Study)',
       theory_attribution_later='PFT: Morsella et al. 2015 (context read: "Integrations involving smooth muscle effectors… can occur unconsciously (Morsella et al. 2009a)")', later_attribution_evidence='context read',
       modality='interoceptive', affective_status='interoceptive',
       notes='Content is autonomic (pupillary) conflict; coded interoceptive by the affective_status/modality rule. Result: no subjective effect. Flagged ancillary; see scenario ±ancillary')],
 dict(manipulation='Compatibility of sustained intentions (identical / compatible / incompatible); effector system', measured_outcome='Introspective ratings of activity / urge', evidence_status=FT))

pub('P23','F23','Gray, Bargh & Morsella 2013',2013,'Sustaining compatible vs incompatible finger intentions and Stroop-like task during fMRI',
 [dict(experiment_label='Single fMRI experiment', participants_total=14, participants_in_analysis=14, report_type='report',
       theory_attribution_by_authors='SIT — abstract states the skeletomotor-conflict hypothesis of consciousness as the hypothesis tested (theory label itself not in abstract)',
       theory_attribution_later='PFT: Morsella et al. 2015, doi:10.1017/s0140525x15000643 (context read)', later_attribution_evidence='context read')],
 dict(modality='motor', affective_status='neutral', manipulation='Compatible vs incompatible sustained intentions; congruent vs incongruent Stroop-like trials', measured_outcome='Subjective ratings in scanner; BOLD correlates', evidence_status=AB))

pub('P24','F24','Morsella et al. 2009b',2009,'Vocal and subvocal Stroop; trial-level introspection of urge to err',
 [dict(experiment_label='Experiment 1 (subvocal Stroop, motionless)', participants_total=15, participants_in_analysis=15, report_type='report',
       theory_attribution_by_authors='SIT — Introduction ("According to supramodular interaction theory (Morsella, 2005)…")',
       theory_attribution_later='PFT: Morsella et al. 2015, doi:10.1017/s0140525x15000643 (context read)', later_attribution_evidence='context read'),
  dict(experiment_label='Experiment 2 (vocal vs subvocal, within-participant)', participants_total=112, participants_in_analysis=112, report_type='report',
       theory_attribution_by_authors='SIT — as Experiment 1', theory_attribution_later='PFT: Morsella et al. 2015 (context read)', later_attribution_evidence='context read'),
  dict(experiment_label='Experiment 3 (difficulty, competition, control ratings)', participants_total=34, participants_in_analysis=34, report_type='report',
       theory_attribution_by_authors='SIT — as Experiment 1', theory_attribution_later='PFT: Morsella et al. 2015 (context read)', later_attribution_evidence='context read')],
 dict(modality='motor', affective_status='neutral', manipulation='Stroop congruency; expressed vs unexpressed (subvocal) response', measured_outcome='Trial-level urge-to-err / difficulty / competition ratings', evidence_status=FT,
      notes='Participant counts taken from results sentences ("k of the N participants"); recruited totals not separately stated in the extracted text'))

pub('P26','F26','Yang, Zald & Blake 2007',2007,'Breaking continuous flash suppression; fearful vs neutral vs happy faces, upright, inverted, eyes-only',
 [dict(experiment_label='b-CFS experiments (abstract lists upright, inverted and eyes-only stimulus sets; partition into experiments not verifiable from abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract', report_type='report',
       theory_attribution_by_authors='none named (abstract-only)', theory_attribution_coder='none of the coded theories')],
 dict(modality='visual', affective_status='valenced', manipulation='Emotional expression (fear vs neutral vs happy); inversion; eyes-only', measured_outcome='Time to break suppression (detection latency)', evidence_status=AB))

pub('P27','F27','Sheth & Pham 2008',2008,'Binocular rivalry with IAPS-type natural images varied in arousal and valence',
 [dict(experiment_label='Rivalry dominance experiment(s) (partition not verifiable from abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract', report_type='report',
       theory_attribution_by_authors='none named (abstract-only)', theory_attribution_coder='none of the coded theories')],
 dict(modality='visual', affective_status='valenced', manipulation='Arousal and valence of rival images (iso-valence / iso-arousal pairs)', measured_outcome='Dominance durations', evidence_status=AB))

pub('P28','F28','Gayet et al. 2016',2016,'Fear conditioning of colour annuli followed by breaking CFS',
 [dict(experiment_label='Conditioning + b-CFS experiment(s) (partition not verifiable from abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract', report_type='report',
       theory_attribution_by_authors='none named (abstract-only)', theory_attribution_coder='none of the coded theories')],
 dict(modality='visual', affective_status='valenced', manipulation='Shock-paired vs unpaired stimulus (acquired threat value)', measured_outcome='Time to break suppression', evidence_status=AB))

pub('P29','F29','Whalen et al. 1998',1998,'Backward-masked fearful vs happy faces; amygdala fMRI',
 [dict(experiment_label='Single fMRI experiment', participants_total=10, participants_in_analysis=10, samples_detail='10 participants; 8 of 10 reported not seeing the masked expressions', report_type='report (post hoc awareness questionnaire)',
       theory_attribution_by_authors='none named (abstract-only; framed as nonconscious amygdala processing)',
       theory_attribution_later='GNWT: Dehaene & Naccache 2001, doi:10.1016/s0010-0277(00)00123-2 (reference list; presumably as subliminal-processing evidence — context not read)', later_attribution_evidence='reference list only',
       contested_inclusion=True, contested_reason='access suppressed by masking, not manipulated; excluded from the baseline scenario')],
 dict(modality='visual', affective_status='valenced', manipulation='Valence of masked expression (fear vs happy); access held below threshold by masking', measured_outcome='Amygdala and substantia innominata BOLD', evidence_status=AB))

pub('P30','F30','Charles et al. 2013',2013,'Masked digit comparison under time pressure; conscious vs subliminal error detection; EEG/MEG',
 [dict(experiment_label='Experiment 1 (high time pressure)', participants_total=17, participants_in_analysis=13, report_type='report',
       theory_attribution_by_authors='GNWT — Introduction: "The Global Neuronal Workspace (GNW) model proposes that conscious access is associated with a sharp non-linear transition"; higher-order/metacognitive identification of consciousness discussed critically',
       theory_attribution_later='GNWT: Mashour et al. 2020, doi:10.1016/j.neuron.2020.01.026 (context read: conscious error-detection model); HOSS: Fleming & Daw 2017, doi:10.1037/rev0000045 (context read: error signals modulated by uncertainty)', later_attribution_evidence='context read'),
  dict(experiment_label='Experiment 2 (reduced time pressure, replication)', participants_total=16, participants_in_analysis=13, report_type='report',
       theory_attribution_by_authors='GNWT — as Experiment 1', theory_attribution_later='as Experiment 1', later_attribution_evidence='context read')],
 dict(modality='visual', affective_status='neutral', manipulation='Masking SOA (seen vs unseen digit); error vs correct response', measured_outcome='ERN amplitude and source; error-detection accuracy by visibility', evidence_status=FT,
      notes='Access manipulation is over the visual digit; error detection is the outcome, so content stays neutral-visual (codebook §4.2 boundary rule ii)'))

pub('P31','F31','Nieuwenhuis et al. 2001',2001,'Antisaccade task; perceived vs unperceived saccade errors; ERP (Ne/ERN, Pe)',
 [dict(experiment_label='Single ERP experiment (per abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract', report_type='report (trial-wise subjective accuracy judgement)',
       theory_attribution_by_authors='none named (abstract-only; two-process error-monitoring account)',
       theory_attribution_later='GNWT: Mashour et al. 2020, doi:10.1016/j.neuron.2020.01.026 (context read: late ignition only for consciously detected errors); Dehaene & Changeux 2011 (reference list)', later_attribution_evidence='Mashour 2020 context read',
       notes='Content re-coded from legacy neutral-visual to motor-conflict under codebook §4.2 boundary rule (ii): the content whose awareness is measured is the erroneous reflexive saccade itself (competing prosaccade vs antisaccade policies); no stimulus-level access manipulation. Judgement call — flagged for second coder')],
 dict(modality='motor', affective_status='neutral', manipulation='None over access; awareness of own saccade errors measured trial by trial', measured_outcome='Ne/ERN and Pe amplitude for perceived vs unperceived errors; post-error slowing', evidence_status=AB))

pub('P32','F32','Garfinkel et al. 2015',2015,'Heartbeat tracking and detection; confidence ratings; questionnaires',
 [dict(experiment_label='Single normative study', participants_total=80, participants_in_analysis=80, report_type='report',
       theory_attribution_by_authors='none named (abstract-only; three-dimensional model of interoception)',
       theory_attribution_later='NSF: Azzalini, Rebollo & Tallon-Baudry 2019, doi:10.1016/j.tics.2019.03.007 (reference list)', later_attribution_evidence='reference list only',
       theory_attribution_coder='PP auxiliary anchor (listed as admissible anchor in codebook §5) — coder/manuscript inference',
       contested_inclusion=True, contested_reason='interoceptive accuracy (first-order detection) and interoceptive awareness (metacognitive confidence–accuracy correspondence) are measured, not manipulated; metacognitive index, not access manipulation')],
 dict(modality='interoceptive', affective_status='interoceptive', manipulation='None over access; individual differences in heartbeat detection accuracy, sensibility and metacognitive awareness', measured_outcome='Interoceptive accuracy, sensibility, awareness and their dissociation', evidence_status=AB))

pub('P33','F33','Farb et al. 2013',2013,'Interoceptive (respiratory) attention vs visual tasks; MBSR graduates vs waitlist; fMRI',
 [dict(experiment_label='Single fMRI experiment (two groups)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract', report_type='report (task compliance; no awareness report)',
       theory_attribution_by_authors='none named (abstract-only)', theory_attribution_coder='none of the coded theories',
       contested_inclusion=True, contested_reason='the contrast is attentional focus (interoceptive attention to breath vs exteroceptive visual tasks) crossed with training group; awareness or access of the interoceptive content is neither manipulated nor measured, so the study meets I1 only under a broad reading of "measures awareness"')],
 dict(modality='interoceptive', affective_status='interoceptive', manipulation='Attentional target (respiratory sensations vs visual) × mindfulness training vs waitlist', measured_outcome='Insula and DMPFC activity and connectivity during interoceptive attention', evidence_status=AB))

pub('P34','F34','Pinto et al. 2017',2017,'Split-brain patients: cross-hemifield comparison, detection, localisation, identification with confidence ratings',
 [dict(experiment_label='Battery of tasks in two patients (partition into experiments not verifiable from abstract)', sample_id='P34-E1-S1;P34-E1-S2', samples_detail='two split-brain patients', participants_total=2, participants_in_analysis=2, report_type='report',
       theory_attribution_by_authors='not verifiable from abstract (conclusion about "two independent conscious perceivers"; no theory named in abstract)',
       theory_attribution_coder='IIT / GNWT (unity of consciousness bears on integration claims) per legacy — coder inference only')],
 dict(modality='visual', affective_status='neutral', manipulation='Visual hemifield × response type (left hand, right hand, verbal); confidence', measured_outcome='Detection, localisation, identification accuracy and confidence across hemifields', evidence_status=AB))

pub('P35','F35','Boulakis et al. 2023',2023,'Experience sampling of uninduced mind blanking; fMRI',
 [dict(experiment_label='Single fMRI experiment', participants_total=31, participants_in_analysis=31, report_type='report (experience sampling)',
       theory_attribution_by_authors='none named (full text: no theory of consciousness named)', theory_attribution_coder='GNWT per legacy — no source located; coder inference only')],
 dict(modality='not applicable (state)', affective_status='neutral', manipulation='None over content access; spontaneous mental states sampled (mind blanking vs content-oriented states)', measured_outcome='Whole-brain deactivations preceding mind-blanking reports', evidence_status=FT))

pub('P36','F36','Kawagoe et al. 2019',2019,'Instructed mind blanking vs mind wandering; fMRI',
 [dict(experiment_label='Single fMRI experiment (per abstract)', participants_total='not stated in abstract', participants_in_analysis='not stated in abstract', report_type='report',
       theory_attribution_by_authors='none named (abstract-only)', theory_attribution_coder='GNWT per legacy — no source located; coder inference only')],
 dict(modality='not applicable (state)', affective_status='neutral', manipulation='Instructed state (mind blanking vs mind wandering); no content contrast', measured_outcome='fMRI activation/deactivation (Broca, hippocampus, ACC)', evidence_status=AB))

# ---------- derived fields ----------
def content_class(r):
    if r['modality'].startswith('not applicable'): return 'state (no content)'
    if r['affective_status']=='valenced': return 'valenced'
    if r['affective_status']=='interoceptive' or r['modality']=='interoceptive': return 'interoceptive'
    if r['modality']=='motor': return 'motor-conflict'
    if r['modality']=='visual': return 'neutral-visual'
    if r['modality'] in ('auditory','tactile'): return 'neutral-nonvisual'
    raise ValueError(r['experiment_id'])

def has_named_theory(s):
    """True if the attribution string names a coded theory (not a 'none' / 'not verifiable' statement)."""
    if not s: return False
    low = s.lower()
    if low.startswith(('none','not verifiable','not needed','as experiment')): return False
    return bool(re.search(r'\b(GNWT|IIT|HOT|HOSS|RPT|AST|PP|SIT|PFT|UAL|NSF|F&M)\b', s))

# Controlled vocabulary for how the later attribution was verified (per publication):
#   CONTEXT_NAMED   = citing sentence read; the citing paper is a coded theory's primary statement (codebook §5) and uses the study as evidence
#   CONTEXT_UNNAMED = citing sentence read, but no coded theory is named at the locus (e.g. Boly et al. 2017 figure legend)
#   REFLIST         = study appears in the reference list of a coded theory's primary statement (OpenAlex); citing sentence not read
EVID = {'P03':'CONTEXT_NAMED','P04':'REFLIST;CONTEXT_UNNAMED','P06':'CONTEXT_NAMED','P07':'CONTEXT_NAMED;REFLIST',
        'P09':'REFLIST;CONTEXT_UNNAMED','P10':'CONTEXT_UNNAMED;REFLIST','P11':'REFLIST','P12':'REFLIST','P16':'REFLIST',
        'P17':'CONTEXT_NAMED;REFLIST','P18':'CONTEXT_NAMED;REFLIST','P19':'CONTEXT_NAMED;REFLIST','P22':'CONTEXT_NAMED','P23':'CONTEXT_NAMED',
        'P24':'CONTEXT_NAMED','P29':'REFLIST','P30':'CONTEXT_NAMED','P31':'CONTEXT_NAMED;REFLIST','P32':'REFLIST'}
for r in rows:
    r['content_class_v2'] = content_class(r)
    r['by_authors_named'] = has_named_theory(r['theory_attribution_by_authors'])
    later = r['theory_attribution_later']
    if later.startswith('as Experiment'):  # inherit from E1 of same publication
        later = next(x['theory_attribution_later'] for x in rows if x['publication_id']==r['publication_id'])
    r['later_attribution_detail'] = r['later_attribution_evidence']
    r['later_attribution_evidence'] = EVID.get(r['publication_id'], '')
    r['later_named'] = has_named_theory(later)
    assert r['later_named'] == bool(r['later_attribution_evidence']) or r['publication_id'] in ('P08','P12'), r['experiment_id']
    r['later_context_read'] = ('CONTEXT_NAMED' in r['later_attribution_evidence']) and r['later_named']
    r['theory_addressed'] = bool(r['by_authors_named'] or r['later_named'])
    # strict variant: later attribution counts only when the citing context was read and names a theory
    r['theory_addressed_strict'] = bool(r['by_authors_named'] or r['later_context_read'])
    r['theory_addressed_incl_coder'] = bool(r['theory_addressed'] or (r['theory_attribution_coder'] and 'none of the coded' not in r['theory_attribution_coder']))
    r['has_content_manipulation'] = r['content_class_v2'] != 'state (no content)'

cols = ['publication_id','study_family_id','experiment_id','sample_id','citation_label','doi','year','experiment_label','participants_total','participants_in_analysis','samples_detail',
        'paradigm','modality','affective_status','content_class_v2','manipulation','measured_outcome','report_type',
        'theory_attribution_by_authors','theory_attribution_later','later_attribution_evidence','later_attribution_detail','theory_attribution_coder',
        'by_authors_named','later_named','later_context_read','theory_addressed','theory_addressed_strict','theory_addressed_incl_coder',
        'contested_inclusion','contested_reason','ancillary_experiment','has_content_manipulation','legacy_content','legacy_theory_addressed','evidence_status','notes']
for r in rows:
    for c in cols: r.setdefault(c,'')
with open('Table_S2_v2.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
with open('paradigm_sources.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(paradigm_sources[0].keys())); w.writeheader(); w.writerows(paradigm_sources)

# consistency checks
legacy_labels=set(legacy); covered={r['citation_label'] for r in rows}|{p['citation_label'] for p in paradigm_sources}
assert legacy_labels==covered, legacy_labels^covered
assert len({r['experiment_id'] for r in rows})==len(rows)
print('experiments',len(rows),'publications',len({r['publication_id'] for r in rows}),'paradigm sources',len(paradigm_sources))
print('abstract-only experiments',sum(r['evidence_status']==AB for r in rows),'abstract-only publications',len({r['publication_id'] for r in rows if r['evidence_status']==AB}))
print('contested rows',sum(r['contested_inclusion'] for r in rows))
from collections import Counter
print(Counter((r['content_class_v2'],r['theory_addressed']) for r in rows))
