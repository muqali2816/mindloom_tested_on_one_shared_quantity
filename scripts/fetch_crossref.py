"""Fetch CrossRef metadata for a DOI list and cache the fields needed for MDPI references."""
import json, sys, time, urllib.request, urllib.error, urllib.parse, os

src = sys.argv[1] if len(sys.argv) > 1 else "handoff/dois_to_fetch.json"
out = "crossref_cache.json"
cache = json.load(open(out)) if os.path.exists(out) else {}
dois = json.load(open(src))

def pick(msg):
    auth = []
    for a in msg.get("author", []):
        if "family" in a:
            auth.append({"family": a["family"], "given": a.get("given", "")})
        elif "name" in a:
            auth.append({"family": a["name"], "given": ""})
    date = (msg.get("published-print") or msg.get("published-online") or
            msg.get("issued") or {}).get("date-parts", [[None]])[0]
    return {
        "doi": msg.get("DOI", "").lower(),
        "type": msg.get("type"),
        "title": (msg.get("title") or [""])[0],
        "container": (msg.get("container-title") or [""])[0],
        "short_container": (msg.get("short-container-title") or [""])[0],
        "year": date[0] if date else None,
        "volume": msg.get("volume", ""),
        "issue": msg.get("issue", ""),
        "page": msg.get("page", ""),
        "article_number": msg.get("article-number", ""),
        "publisher": msg.get("publisher", ""),
        "publisher_location": msg.get("publisher-location", ""),
        "isbn": (msg.get("ISBN") or [""])[0],
        "authors": auth,
        "editors": [{"family": e.get("family", ""), "given": e.get("given", "")} for e in msg.get("editor", [])],
    }

todo = [d for d in dois if d not in cache]
fail = []
for i, d in enumerate(todo):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(d, safe="")
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=30) as r:
            cache[d] = pick(json.load(r)["message"])
    except Exception as e:
        fail.append((d, str(e)[:80]))
    if i % 25 == 0:
        json.dump(cache, open(out, "w"), ensure_ascii=False)
    time.sleep(0.15)
json.dump(cache, open(out, "w"), ensure_ascii=False)
print(len(cache), "cached |", len(fail), "failed")
for d, e in fail[:20]:
    print("  FAIL", d, e)
