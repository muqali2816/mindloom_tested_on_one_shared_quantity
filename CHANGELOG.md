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

## Still with the authors
Send extension request; send proponent letters (record dates); second coding → agreement.py → fill κ; upload deposit_v2 → DOI into 4 places; names, CRediT confirmation, funding, CoI, AI tool; decide on length cuts; confirm Poznanski DOI.
