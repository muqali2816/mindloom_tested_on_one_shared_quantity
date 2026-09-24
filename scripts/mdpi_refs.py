"""Convert an author-date manuscript to MDPI numbered citations.

    from mdpi_refs import convert
    new_text, report = convert(md_text, crossref_cache, manual_entries, disambig)

The manuscript's own reference list (Elsevier author-date, one entry per blank-line
paragraph, DOI at the end) is the source of truth for WHICH works are cited. Each entry
is keyed by (first-author surname, year, optional letter). In-text groups such as
"(Mashour et al., 2020; Lamme, 2006)" are replaced by "[n,m]" numbered by first
appearance; the reference list is regenerated in MDPI style from the CrossRef cache.

Ambiguous keys (two entries with the same surname and year and no letter) are resolved
by `disambig`: a list of (regex on the 120 characters before the citation, DOI).
"""
import re
import unicodedata

NARRATIVE = re.compile(r"\b((?:[A-Z][A-Za-z\-]+)(?: et al\.| and [A-Z][A-Za-z\-]+)?)('s)? \(((?:19|20)\d{2})([a-c])?\)")
CITE_GROUP = re.compile(r"\(((?:[^()]*?(?:19|20)\d{2}[a-c]?)(?:;[^()]*?(?:19|20)\d{2}[a-c]?)*)\)")
CITE_ITEM = re.compile(r"^\s*(?:see |e\.g\.,? |cf\. )?([A-Za-z][^,;]+?)(,| et al\.,?| and [^,]+,)?\s*((?:19|20)\d{2})([a-c])?\s*$")
MULTI_YEAR = re.compile(r"^(\s*(?:see |e\.g\.,? |cf\. )?[A-Za-z][^,;]+?(?:,| et al\.,?| and [^,]+,)?\s*(?:19|20)\d{2}[a-c]?)((?:,\s*(?:19|20)\d{2}[a-c]?)+)\s*$")
ENTRY_DOI = re.compile(r"https://doi\.org/(10\.\S+?)\.?$")


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def surname_key(s):
    s = strip_accents(s).lower()
    s = re.sub(r"^(van der|van den|van|de la|de|di|du|la|le|von)\s+", "", s)
    return re.sub(r"[^a-z]", "", s.split()[0]) if s.split() else s


def parse_reflist(reflist):
    """Return list of dicts {key, letter, doi, raw, first_surname, year}."""
    ents = []
    for e in reflist.split("\n\n"):
        e = re.sub(r"\s+", " ", e.strip())
        if not e or e.startswith("#"):
            continue
        m = re.match(r"([^,]+),", e)
        first = m.group(1) if m else e.split()[0]
        ym = re.search(r"\b((?:19|20)\d{2})([a-c])?\.", e)
        year, letter = (ym.group(1), ym.group(2) or "") if ym else ("", "")
        dm = ENTRY_DOI.search(e)
        auth_part = e[:ym.start()] if ym else e
        n_auth = len(re.findall(r"\b[A-Z](?:\.-?[A-Z])*\.,", auth_part)) or 1
        form = "1" if n_auth == 1 else ("2" if n_auth == 2 else "3")
        ents.append(dict(first_surname=first, year=year, letter=letter, form=form,
                         key=(surname_key(first), year, letter),
                         doi=dm.group(1).lower() if dm else "", raw=e))
    return ents


def initials(given):
    parts = re.split(r"[\s\-]+", given.strip())
    out = []
    for p in parts:
        if not p:
            continue
        if "." in p:                               # already "B.J." or "J.-P."
            out.append(p if p.endswith(".") else p + ".")
            continue
        if len(p) <= 2 and p.isupper():          # already initials like "JB"
            out.extend(c + "." for c in p)
        else:
            out.append(p[0] + ".")
    return "".join(out)


def mdpi_authors(auth, max_full=10):
    names = []
    for a in auth:
        fam, giv = a.get("family", ""), a.get("given", "")
        names.append(f"{fam}, {initials(giv)}" if giv else fam)
    if len(names) > max_full:
        return "; ".join(names[:max_full]) + "; et al."
    return "; ".join(names)


def mdpi_entry(rec):
    """MDPI reference string (markdown: journal italic, year bold, volume italic)."""
    a = mdpi_authors(rec.get("authors", []))
    t = rec.get("title", "").rstrip(".")
    y = rec.get("year") or ""
    typ = rec.get("type", "")
    doi = rec.get("doi", "")
    doi_s = f" https://doi.org/{doi}" if doi else ""
    if typ in ("journal-article", "posted-content", "proceedings-article", "peer-review"):
        j = rec.get("container") or rec.get("short_container") or ""
        vol = rec.get("volume", "")
        pages = rec.get("page") or rec.get("article_number") or ""
        pages = pages.replace("-", "–") if pages else ""
        s = f"{a} {t}. *{j}* **{y}**"
        if vol:
            s += f", *{vol}*"
        if pages:
            s += f", {pages}"
        s += "." + doi_s
        if typ == "posted-content":
            s = s.replace(f"*{j}*", f"*{j or 'Preprint'}*")
        return s
    if typ in ("book", "monograph", "edited-book", "reference-book"):
        pub = re.sub(r"(Press|Verlag|Books|Publishers?)(?=[A-Z])", r"\1: ", rec.get("publisher", ""))
        loc = rec.get("publisher_location", "")
        where = f"{pub}: {loc}" if loc else pub
        return f"{a} *{t}*; {where}, {y}.{doi_s}"
    if typ == "book-chapter":
        book = rec.get("container", "")
        eds = mdpi_authors(rec.get("editors", []))
        pub = rec.get("publisher", "")
        pages = (rec.get("page") or "").replace("-", "–")
        s = f"{a} {t}. In *{book}*"
        if eds:
            s += f"; {eds}, Eds."
        s += f"; {pub}, {y}"
        if pages:
            s += f"; pp. {pages}"
        return s + "." + doi_s
    # fallback
    j = rec.get("container", "")
    return f"{a} {t}. *{j}* **{y}**.{doi_s}".replace("**.", "**.")


def convert(text, cache, manual=None, disambig=None, ref_heading="## References"):
    manual = manual or {}          # key -> MDPI string, for entries without DOI
    disambig = disambig or []
    body, reflist = text.split(ref_heading, 1)
    ents = parse_reflist(reflist)
    by_key = {}
    for e in ents:
        by_key.setdefault(e["key"], []).append(e)
    order, numbers = [], {}      # doi/raw -> number
    unresolved, ambiguous = [], []

    def resolve(item, ctx):
        m = CITE_ITEM.match(item)
        if not m:
            return None
        sep = (m.group(2) or ",").strip()
        form = "1" if sep == "," else ("3" if sep.startswith("et al") else "2")
        cands = by_key.get((surname_key(m.group(1)), m.group(3), m.group(4) or ""))
        if not cands:
            cands = by_key.get((surname_key(m.group(1)), m.group(3), ""))
        if cands and len(cands) > 1:
            byform = [c for c in cands if c["form"] == form]
            if byform:
                cands = byform
        if not cands:
            unresolved.append(item.strip())
            return None
        if len(cands) > 1:
            for pat, doi in disambig:
                if re.search(pat, ctx) and any(c["doi"] == doi for c in cands):
                    return next(c for c in cands if c["doi"] == doi)
            ambiguous.append((item.strip(), ctx[-80:]))
            return cands[0]
        return cands[0]

    def number_of(e):
        k = e["doi"] or e["raw"]
        if k not in numbers:
            order.append(e)
            numbers[k] = len(order)
        return numbers[k]

    def repl(m):
        items = []
        for x in m.group(1).split(";"):
            if not x.strip():
                continue
            my = MULTI_YEAR.match(x)
            if my:
                head = my.group(1)
                stem = re.sub(r"(?:19|20)\d{2}[a-c]?\s*$", "", head)
                items.append(head)
                items.extend(stem + y.strip() for y in my.group(2).strip(",").split(","))
            else:
                items.append(x)
        ctx = body[max(0, m.start() - 120):m.start()]
        nums, keep = [], []
        for it in items:
            e = resolve(it, ctx)
            if e is None:
                keep.append(it.strip())
            else:
                nums.append(number_of(e))
        if not nums:
            return m.group(0)
        nums = sorted(set(nums))
        # compress runs: 1,2,3 -> 1–3
        runs, start, prev = [], nums[0], nums[0]
        for n in nums[1:] + [None]:
            if n is not None and n == prev + 1:
                prev = n
                continue
            runs.append(f"{start}–{prev}" if prev - start >= 2 else (f"{start},{prev}" if prev != start else f"{start}"))
            if n is not None:
                start = prev = n
        s = "[" + ",".join(runs) + "]"
        if keep:
            s += " (" + "; ".join(keep) + ")"
        return s

    def repl_narr(m):
        name, poss, yr, letter = m.group(1), m.group(2) or "", m.group(3), m.group(4) or ""
        sep = " et al.," if name.endswith("et al.") else (" and X," if " and " in name else ",")
        surname = name.replace(" et al.", "").split(" and ")[0]
        item = f"{surname}{sep} {yr}{letter}" if sep != " and X," else f"{name}, {yr}{letter}"
        e = resolve(item, body[max(0, m.start() - 120):m.start()])
        if e is None:
            return m.group(0)
        return f"{name}{poss} [{number_of(e)}]"

    # single left-to-right pass over both citation forms so numbering follows position
    events = [(m.start(), m.end(), "g", m) for m in CITE_GROUP.finditer(body)]
    events += [(m.start(), m.end(), "n", m) for m in NARRATIVE.finditer(body)]
    events.sort(key=lambda t: t[0])
    out, pos = [], 0
    for s, e_, kind, m in events:
        if s < pos:
            continue
        out.append(body[pos:s])
        out.append(repl(m) if kind == "g" else repl_narr(m))
        pos = e_
    out.append(body[pos:])
    new_body = "".join(out)
    lines = []
    for i, e in enumerate(order, 1):
        rec = cache.get(e["doi"]) if e["doi"] else None
        if e["key"] in manual:
            s = manual[e["key"]]
        elif e["doi"] in manual:
            s = manual[e["doi"]]
        elif rec and rec.get("authors"):
            s = mdpi_entry(rec)
        else:
            s = e["raw"] + "  ⟵ NO STRUCTURED RECORD"
        lines.append(f"{i}. {s}")
    uncited = [e for e in ents if (e["doi"] or e["raw"]) not in numbers]
    report = dict(n_cited=len(order), n_entries=len(ents), uncited=[e["raw"][:80] for e in uncited],
                  unresolved=sorted(set(unresolved)), ambiguous=ambiguous)
    return new_body + ref_heading + "\n\n" + "\n".join(lines) + "\n", report
