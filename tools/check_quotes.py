"""Check an Explore source file: every "quoted" English phrase must appear in data/src/sefaria-*.json English (else listed for a manual check against Sefaria), and no em/en dashes.
Usage: python3 tools/check_quotes.py data/src/x-stories_jonah.json"""
import glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')).strip().lower()
EN = " ".join(norm(" ".join(s["text"])) for f in glob.glob(os.path.join(ROOT, "data/src/sefaria-*.json")) for s in json.load(open(f, encoding="utf-8"))["sources"] if s.get("lang") == "en" and "text" in s)
def strings(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from strings(v)
    elif isinstance(o, list):
        for v in o: yield from strings(v)
d = json.load(open(sys.argv[1], encoding="utf-8")); ok = other = 0
for s in strings(d):
    if re.search("[–—]", s): print("DASH:", s[:80])
    for q in re.findall(r'"([^"]{3,})"', s):
        q2 = norm(q.replace("**", "")).strip(" .,;:!?")
        if q2 in EN: ok += 1
        else: other += 1; print("CHECK:", q)
print(f"{ok} quotes found in Sefaria English files; {other} to check by hand")
