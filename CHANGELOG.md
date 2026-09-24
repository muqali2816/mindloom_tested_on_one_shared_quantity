# CHANGELOG — unified v4 (24 September 2026), brainsci-4583950

Baseline: manuscript v3 (sha256 dec8007fb39d42e2), deposit v1.3 (e7ea015ce7b91714), S4 draft (e8cc697a063f4be7). See INTAKE_v4.md.

## Manuscript (manuscript/paper1_revised_v4_mdpi_en.md → _highlighted.pdf/.docx, 40 pp)
- Title: "What theories of consciousness commit to, and what they leave unmeasured: an audit of stated predictions after the first adversarial test".
- Abstract, §1, §6.4, §7 (entire), §9 rewritten; §4 (3 paragraphs), §5 (2), §8 (4) edited at anchored sentences; §2, §3 untouched. Highlight = reconstructed text comparison with the submitted version (pandoc `{.mark}` spans), not Word Track Changes.
- Withdrawn: "shared ⇒ no discrimination" (M8 is contested at locus/timing/connectivity: 6 EXPLICIT, 15 distinguishable pairs); "M4 the only contested column" (M4a/M4b/M4c occupied-not-contested); "three quantities jointly observable"; "durably" (Hall 2012); C1 as a stated SIT prediction (now P23, authors' derivation); old design with 1/2/3 keys and N = 126.
- References renumbered by first appearance: 205 (200 carried from v3, 5 new: Bor 2017, Ruby 2018, Bor 2018, Huber 1982, Graziano & Kastner 2011); 11 v3 entries no longer cited (moved with the protocol to S5).
- Body incl. tables 17 083 words (v3 ≈ 13 600) — §7 grew; cut candidates: §7.5 third paragraph, §7.1 second paragraph, §6.2 second half (authors' decision).
- Placeholders that stay until authors act: κ (4 slots, §7.2), deposit DOI (Supplementary Materials, §7.2, Data Availability, S5.16), names/affiliations/funding/CoI/AI tool name.

## Tables and code (deposit_v2/, reproduce.py 6 of 6 PASS)
- Table_S1_v2.csv: 120 cells (12 accounts incl. HOT/HOSS split × 10 domains incl. M4a/b/c), codes EXPLICIT 22 (20+2∅) / INTERPRETED 32 (25+7∅) / NOT_LOCATED 64 / NOT_APPLICABLE 2; 50 provisional, 15 flagged (first: PP × M4c), 58 abstract-only. One row per cell; multi-prediction cells list S4 ids. Long form with superseded legacy M4 rows in Table_S1_v2_long.csv.
- Table_S4_v2.csv: 31 predictions (28 stated, 3 derived: P23, P24, P25).
- column_typology.py (new): class derived after coding —
| domain | EXPLICIT | INTERPRETED | NOT_LOCATED | pairs (conf≥2) | class |
|---|---|---|---|---|---|
| M1 | 1+0∅ | 1 | 10 | 0 (0) | single-occupant |
| M2 | 1+0∅ | 2 | 9 | 0 (0) | single-occupant |
| M3 | 3+0∅ | 5 | 4 | 0 (0) | occupied-not-contested |
| M5 | 0+0∅ | 5 | 7 | 0 (0) | thin |
| M6 | 2+0∅ | 3 | 7 | 1 (0) | contested |
| M7 | 3+0∅ | 2 | 7 | 0 (0) | occupied-not-contested |
| M8 | 6+0∅ | 4 | 0 | 15 (14) | contested |
| M4a | 2+0∅ | 6 | 4 | 0 (0) | occupied-not-contested |
| M4b | 2+0∅ | 0 | 10 | 0 (0) | occupied-not-contested |
| M4c | 0+2∅ | 4 | 6 | 0 (0) | occupied-not-contested |
- Table_S2_v2_experiments.csv: 42 experiments / 32 publications; paradigm_sources.csv (4) out of every denominator; baseline 18 of 30 neutral-visual, 0 of 30 valenced, 2 of 30 interoceptive; s2_sensitivity.csv 11 scenarios + 2 historical.
- agreement.py 2.0 (+ S2 v2 path added at integration): manifest keys, code scheme v2, raw agreement → confusion → nominal κ, subset κ (submitted-v1 / added-in-revision), negative self-tests 15 of 15; rejects blank forms, duplicates, aliases.
- section9_power.py: Study 1 C0/C1a N = 119 (dz 0.30, 90 %), TOST ±0.30 power 0.892, C1b 0.83; 102 presented → ≈65 usable trials per cell; Study 2 valence N = 119, interaction estimation only.
- codebook_v2.md FROZEN (sha256 b32e0703… see codebook_v2.sha256); changelog started.

## Coder pack v3 (coder_pack_v3/): blank S1 (120) and S2 (42), manifests, S4 for reference, agreement.py, timing log. No coder-1 answers inside.
## Response (response/response_to_reviewers_v3.md, 20 pp): 27 comments verbatim; statuses DONE 20 / PREPARED 4 / PARTLY 3; re-audit section; outstanding list.
## Gates (gates/): extension request; two letters to proponents — drafts, not sent.

## Integration fixes after audit findings
- agreement.py: S2 v2 (experiment-unit) path added; blank S2 form now rejected; planted disagreements detected.
- recompute_table1.py: polarity-based field renamed `occupancy_summary` (no-EXPLICIT / one-EXPLICIT / multi-EXPLICIT-same-sign / sign-disagreement) so it cannot be read as the column class, which only column_typology.py derives.
- S5 §S5.2: P25 marked "not tested" (count branch tests P16; a decrement is reported descriptively), consistent with §9.1.
- Table 1 caption: legend for "IIT (3.0/4.0)".
- §7.2 and CRediT: second coding described as scheduled, not in progress.
- deposit_v2/README.md: Table S3 covers 10 accounts (v1.3 set without NSF, before the HOT/HOSS split), not the S1 set.

## v4.2 — after the second internal check (24 Sep, 13:30)
- Coder pack v3.1: Table S4 removed (it lists every EXPLICIT cell); released to the second coder only after S1 is returned. README states this.
- Codebook re-frozen with a verifiable rule: `sed '$d' codebook_v2.md | shasum -a 256` (GNU: `head -n -1 … | sha256sum`) = value in codebook_v2.sha256. Definitions unchanged; polarity token `null` → `stated_null` (pandas reads bare `null` as missing) in Table S1, scripts and codebook.
- §9.1 / S5 / response: fixed N = 120 (119 required, rounded to a multiple of six rule-to-effector rotations); power at 120: C0/C1a 0.903, TOST ±0.30 0.895, C1b omnibus 0.84. Within-participant rotation of the shared lever added to S5.5 (effector-identity confound).
- Pair counts stated as "15 (14 at confidence ≥ 2)"; §7.2 now says the S4 distinguishability judgements are single-coder until the second coder codes them.
- Ref 84 left as Graziano & Webb 2015: CrossRef and OpenAlex both give Graziano as first author for 10.3389/fpsyg.2015.00500.
- NOT done (author decisions): reclassification of Morsella 2009 E3 (interoceptive → motor-conflict) and the abstract sentence that rests on it; length cut to ≤ 13 500; full-text reading of the 54 EXPLICIT/INTERPRETED cells; abstract rewrite.

## v4.3 — interoceptive row (author decision, 24 Sep)
- Morsella, Gray & Krieger 2009 control study (P22-E3) re-coded interoceptive → motor-conflict (autonomic effector) by the first coder. Criteria v2.1 / codebook v2.1 (re-frozen, hash 7dd78645…): interoceptive = content from visceral afferents or autonomic modulation of access; motor-conflict split skeletal / autonomic-effector. Baseline: motor-conflict 8 of 30 (7 + 1), interoceptive 1 of 30 (Garfinkel, contested), 0 in strict scenarios; §7.6 and Table 2 updated; abstract carries no interoceptive count.
- Abstract rewritten (250 words): thesis (commitments concentrate; 22 of 120 cells stated), no "provisional pending second coding" sentence, closing sentence on what the next test needs.

## v4.4 — after the second external audit (24 Sep, evening)
- Coder pack v3.2: codebook §4 no longer reproduces the first coder's row-level S2 decisions (they stay in the deposit criteria); stale 'HOT/HOSS one row' fixed; Table S4 not in the pack. Codebook v2.2 re-frozen; hash rule verifiable.
- Five S1 cells re-coded by the first coder (three where the cell's own note contradicted the code; two after full-text reading); previous code kept. Codes resting on unreachable full texts marked provisional. Totals 21/29/68/2.
- Pair register (55 pairs, four-way relation) replaces distinguishable_from as the basis of 'contested': M8 contested on 2 discriminating pairs of 54 (was '15 distinguishable'); M6 → occupied-not-contested; M4b → single-occupant. Definition of contested rewritten in §7.3; 'only a contested column lets a prediction lose' withdrawn. Table 1 regenerated from S1 + pair register.
- §9 / S5 v2: C0 no longer 'tests P16' — P32/P33 (derived) registered; two confirmatory contrasts with Holm and a conjunctive success rule; session-2-only trial budget (104 presented, 66 usable expected); block scheme, probe, EEG index specification, pilot criteria, autonomic windows, Study 2 hypothesis P34 (derived). N = 120 for both studies.
- Code: agreement.py v2.1 (attribution parser, id sets, vocabularies, grid completeness, UNRESOLVED), reproduce.py v2.1 (statsmodels policy, mixed-sim content check, Table 2 / sensitivity / S3 / pair-register steps), build_table2.py (publication + experiment level), S2 unit_type column.
- Manuscript §11 contradictions fixed: one definition of access; second coding 'scheduled'; abstract/§7.6 zero-vs-imbalance sentence; legacy-code sentence (84 + 12, two departures); 'deposited' → 'will be deposited'. Response: E5 rewritten (status PREPARED), §4 (a), (b), (e) rewritten, (g), (h) added.
- NOT done: length (18 084 words with tables); reading of the 9 closed sources (list in reading_log_20260924.md) — PDFs needed from the authors; the interoceptive-inference query letters.

## v4.5 — after the v4.4 recheck (GPT) and the parallel Claude review
- Protocol arithmetic has one source: `section9_power.py` v2.2 (per-session configuration) → `protocol_numbers.py` (deposited; multiplicity, success-rule powers, retention) → S5 and §9.1. The deposited trial budget now matches the protocol text (session 1: 64 per cell; session 2: 104). Study 2 N = 120 with power at that N. Success rule requires the predicted direction; C0-eq is a secondary TOST outside the family; retention probabilities and a repeat-block rule added to S5.8.
- `reproduce.py` v2.2: `power_mixed_check.csv` no longer hashed (content-checked in step 4); step 4b `protocol_numbers`; `protocol_numbers.json` and the power tables hashed; full run 11 of 11.
- `column_typology_pairs.py`: required pairs derived from S4, 'pair assessment incomplete' class; eight pairs in M3, M7, M4a, M4c added to the register (63 pairs).
- `agreement.py` v2.2: stated_null counter, UNRESOLVED excluded from the binary κ with its own n, later-attribution-only disagreements listed.
- `build_table2.py`: content class derived from raw fields (`effector_type` added to S2) and checked. Publication is the primary unit of Table 2, the abstract and §7.6; experiment-row counts beside it.
- Three distinct recode notes for the integration-pass recodes; `recompute_table1.py` legacy self-test finds the deposited v1.3 file.
- Coder pack v3.3: codebook v2.3 (instructions match the forms; S3 blank; later attribution and own partition coded by coder 2), changelog copy without the row-level decision, README rewritten.
- Manuscript: §7.6 rewritten at publication level; §7.2 counts (57 abstract-only, 27 of 50; 34 register entries, 63 pairs; 16 flagged; "has not begun"); Table 1 legend states the six derived entries in the text, not the caption; abstract 250 words; codebook v2.3 named. Response: R1-8, E5 numbers, §4(a),(e),(h),(i); no stale version, hash or count remains.

## v4.6 — after the v4.5 recheck (GPT) and Claude's third pass
- Response R1-1 rewritten on the pair-register rule; R1-6, E1, §6 counts and pack version corrected; §4(j) on length added.
- Manuscript: 63 pairs everywhere; Table 1 pair row filled for M3, M7, M4a, M4c; M7 'no discriminating pair'; Table 2 caption composition; §7.2 subset sizes 70/50; §7.7 M2 count corrected (PP × M2 NOT_LOCATED). Body trimmed 18 481 → 16 407 words by removing repetition only (trim_log.md); ≤ 13 500 needs content cuts — open.
- S5: S5.16 contradiction removed; S5.8 reserve budget on the feasible grid (112, P ≈ 0.989).
- Code: section9_power.py v2.3, protocol_numbers.py v3.2, agreement.py v2.3 (new second-coder fields compared, 'not compared' when absent); summary regenerated without P16/N = 119 labels; pair_register_notes.md scope note; README_coder2 subset sizes.

## v4.7 — final text pass
- Supplementary Note S6 (new): ConTraSt scheme and limits (from §7.5), full Table 2 scenario list (from §7.6). Body 16 407 → 15 813 words; §8.1–8.3 shortened by about a quarter with every citation kept; §8.4 nested highlight flattened. Response §4(i) version, §4(j) sentence on remaining length. Deposit README lists S6.

## Still with the authors
Send extension request; send proponent letters (record dates); second coding → agreement.py → fill κ; upload deposit_v2 → DOI into 4 places; names, CRediT confirmation, funding, CoI, AI tool; decide on length cuts; confirm Poznanski DOI.
