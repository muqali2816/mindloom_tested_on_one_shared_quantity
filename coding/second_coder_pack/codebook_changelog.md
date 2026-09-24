# Codebook changelog

| Date | Version | Change | Cells to re-code |
|---|---|---|---|
| 2026-09-24 | 2.0 | Frozen: 12 accounts (HOT/HOSS split), 10 domains (M4 → M4a/M4b/M4c), code scheme v2 (EXPLICIT/INTERPRETED/NOT_LOCATED/NOT_APPLICABLE/UNRESOLVED + polarity), S2 unit = experiment, attribution split by-authors / later / coder. | — (freeze) |
| 2026-09-24 | 2.0 (re-frozen) | Polarity token `null` → `stated_null` (pandas reads bare `null` as missing); footer hash rule made verifiable (`head -n -1 | sha256sum`). Definitions unchanged; second coder has not started, so no re-coding. | — |
| 2026-09-24 | 2.1 | S2 content classes sharpened before the second coder starts: interoceptive = content from visceral afferents (or autonomic modulation of access); motor-conflict split into skeletal / autonomic-effector. Morsella et al. 2009 control study re-coded by the first coder from interoceptive to motor-conflict (autonomic effector). No S1 change. | — (freeze; coder 2 not started) |
| 2026-09-24 | 2.2 | Blind copy: first-coder row-level S2 decisions removed from §4 (kept in the deposit criteria file); stale 'HOT/HOSS coded as one row' label corrected; Table S4 removed from the file list. No definition changed. | — (freeze; coder 2 not started) |
| 2026-09-24 | 2.2 (final freeze) | Column-class paragraph now states the pair-register rule (discriminating / incompatible pairs), replacing the distinguishable_from rule. Hash re-issued; nothing sent to the second coder before this freeze. | — |
