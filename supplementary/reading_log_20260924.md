# Reading log — full-text pass for 8 flagged cells (cells_to_read.csv)

Date: 24 September 2026. Routes tried, in order, for every DOI: fetch_article_fulltext (Unpaywall → Semantic Scholar → PMC → CrossRef TDM → DOI landing page), then OpenAlex OA-location lookup and PubMed E-utilities for abstracts. No mirrors, no scraping, no user-agent spoofing. Where a publisher or repository answered with a bot check (HTTP 403, WAF, proof-of-work challenge) the attempt was stopped and recorded.

## DOIs named in cells_to_read.csv (source_doi / source_locus)

| # | Source | DOI | Reachable | Route | Length read |
|---|---|---|---|---|---|
| 1 | Kelly, Webb, Meier, Arcaro & Graziano 2014, PNAS | 10.1073/pnas.1401201111 | **no (abstract + Significance only)** | PMC record PMC3977229 via fetch tool: metadata + abstract, no XML body (publisher does not permit); PMC PDF endpoint returns a proof-of-work challenge — not attempted | ~1,900 characters (Significance + Abstract) |
| 2 | Graziano & Webb 2015, Front. Psychol. | 10.3389/fpsyg.2015.00500 | **yes** | Unpaywall → Frontiers gold-OA PDF | 11 pages, 70,666 characters (pp. 1–9 text, pp. 10–11 references) |
| 3 | Feinberg & Mallatt 2013, Front. Psychol. | 10.3389/fpsyg.2013.00667 | **yes** | Unpaywall → Frontiers gold-OA PDF | 27 pages, 181,406 characters (pp. 1–19 text, pp. 20–27 references) |
| 4 | Feinberg & Mallatt 2016, *The Ancient Origins of Consciousness* (MIT Press) | 10.7551/mitpress/10714.001.0001 | **no** | closed; Unpaywall/S2/PMC/CrossRef TDM none; DOI landing 403. No open chapter located (OpenAlex lists no OA location) | book blurb only (not used as evidence) |
| 5 | Lau & Rosenthal 2011, TICS | 10.1016/j.tics.2011.05.009 | **no (abstract only)** | closed (Elsevier); abstract via PubMed 21737339 | 887-character abstract |
| 6 | Brown, Lau & LeDoux 2019, TICS | 10.1016/j.tics.2019.06.009 | **no (abstract only)** | hybrid OA at cell.com but the PDF endpoint returned HTTP 403 (bot check) — stopped; abstract via PubMed 31375408 | 975-character abstract |
| 7 | Tallon-Baudry 2022, TICS (Science & Society) | 10.1016/j.tics.2022.09.002 | **no (abstract only)** | bronze OA at cell.com; PDF endpoint 403 (bot check) — stopped; abstract via PubMed 36243671 | 312-character abstract |
| 8 | Park, Correia, Ducorps & Tallon-Baudry 2014, Nat. Neurosci. | 10.1038/nn.3671 | **no (abstract only)** | closed; no OA location in Unpaywall or OpenAlex; abstract via PubMed 24609466 | 1,109-character abstract |
| 9 | Tallon-Baudry, Campana, Park & Babo-Rebelo 2018, Cortex | 10.1016/j.cortex.2017.05.019 | **no (abstract only)** | hybrid OA at sciencedirect.com (domain not on allowlist; not requested — same publisher bot check expected); EPFL Infoscience repository copy (submitted version) — network access granted, but the repository WAF answered 429 'bot suspect activity' twice — stopped; abstract via PubMed 28651745 | 1,126-character abstract |
| 10 | Pezzulo, Rigoli & Friston 2018, TICS | 10.1016/j.tics.2018.01.009 | **yes** | PMC author manuscript (text) | 63,937 characters (full text incl. Boxes 1–3, figure legends, references) |
| 11 | Lamme 2006, TICS | 10.1016/j.tics.2006.09.001 | **no (abstract only)** | closed; abstract via PubMed 16997611 | 833-character abstract |
| 12 | Park & Tallon-Baudry 2014, Phil. Trans. R. Soc. B (named in NSF×M4b source_locus) | 10.1098/rstb.2013.0208 | **no (abstract only)** | PMC record PMC3965163: metadata + abstract, no XML body; PDF behind proof-of-work challenge — not attempted | ~1,400-character abstract |

## Additional §5 primary sources fetched to widen the corpus for negative codes

| Source | DOI | Reachable | Route | Length |
|---|---|---|---|---|
| LeDoux & Brown 2017, PNAS (HOT) | 10.1073/pnas.1619316114 | no (abstract + Significance only) | PMC record PMC5347624, no XML body | ~1,600 characters |
| Lamme 2010, Cogn. Neurosci. (RPT) | 10.1080/17588921003731586 | no (abstract only) | closed; PubMed 24168336 | 1,560-character abstract |
| Lamme & Roelfsema 2000, TINS (RPT) | 10.1016/s0166-2236(00)01657-x | no (abstract only) | closed; PubMed 11074267 | 883-character abstract |
| Babo-Rebelo, Richter & Tallon-Baudry 2016, J. Neurosci. (NSF) | 10.1523/JNEUROSCI.0262-16.2016 | no (abstract only) | PMC record PMC4961773, no XML body | ~2,300-character abstract + significance |
| Azzalini, Rebollo & Tallon-Baudry 2019, TICS (NSF) | 10.1016/j.tics.2019.03.007 | no (abstract only) | hybrid at cell.com (same bot check); PubMed 31047813 | 890-character abstract |
| Graziano, Guterstam, Bio & Wilterson 2019, Cogn. Neuropsychol. (AST) | 10.1080/02643294.2019.1670630 | no (abstract only) | closed; DOI landing 403 | abstract from fetch tool |
| Wilterson et al. 2020, Prog. Neurobiol. (AST) | 10.1016/j.pneurobio.2020.101844 | no (abstract only) | hybrid; landing page requires scraping — stopped | abstract from fetch tool |

## Other checks
- User-granted folders (Documents/речь/Literature, under review, phd_v1, phd_v2, new_mindloom, projects) and the project artifact store were searched for local copies of the unreachable papers: none found.
- api.unpaywall.org and europepmc.org are not on the network allowlist; not requested (the fetch tool already queries Unpaywall internally, and Europe PMC's REST fullTextXML returned HTTP 500 = no full text for the four PMC-record-only papers).

## Tally
- DOIs in cells_to_read.csv: 12 (11 in source_doi + Park & Tallon-Baudry 2014 named in a locus). Full text reached: 3 (Graziano & Webb 2015; Feinberg & Mallatt 2013; Pezzulo et al. 2018). Abstract only: 8. Nothing beyond a blurb: 1 (MIT Press book).
- Cells with at least one full text read: 4 of 8 (AST×M8, FM×M4a, FM×M4c, PP×M2). Cells resting entirely on abstracts: 4 of 8 (HOT×M6, NSF×M6, NSF×M4b, RPT×M5).
