# Codebook changelog

| Date | Version | Change | Cells to re-code |
|---|---|---|---|
| 2026-09-24 | 2.0 | Frozen: 12 accounts (HOT/HOSS split), 10 domains (M4 → M4a/M4b/M4c), code scheme v2 (EXPLICIT/INTERPRETED/NOT_LOCATED/NOT_APPLICABLE/UNRESOLVED + polarity), S2 unit = experiment, attribution split by-authors / later / coder. | — (freeze) |
| 2026-09-24 | 2.0 (re-frozen) | Polarity token `null` → `stated_null` (pandas reads bare `null` as missing); footer hash rule made verifiable (`head -n -1 | sha256sum`). Definitions unchanged; second coder has not started, so no re-coding. | — |
