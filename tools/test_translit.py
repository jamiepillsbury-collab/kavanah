"""Regression test: compare translit.py against he/tl pairs in a JS/JSON data file.
python test_translit.py ../../neshmah-site/prayers.js [max_diffs]"""
import json, re, sys
from translit import tl
src = open(sys.argv[1], encoding="utf-8").read()
pairs = []
def walk(o):
    if isinstance(o, dict):
        if isinstance(o.get("he"), str) and isinstance(o.get("tl"), str): pairs.append((o["he"], o["tl"]))
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
for m in re.finditer(r"=\s*(\{.*?\}|\[.*?\]);\s*(?=\n(?:var|const|let|/\*|$)|\Z)", src, re.S):
    try: walk(json.loads(m.group(1)))
    except Exception: pass
norm = lambda s: re.sub(r"[^a-z' ]", "", s.lower().replace("-", " ").replace("\u2019","'")).split()
canon = lambda s: re.sub(r"[^a-z]", "", s.lower())
ok = 0; diffs = []
for he, want in pairs:
    got, _ = tl(he)
    if norm(got) == norm(want): ok += 1
    elif canon(got) == canon(want): diffs.append(("SPACING/APOS: "+want, got))
    else:
        for g, w in zip(norm(got), norm(want)):
            if g != w: diffs.append((w, g))
print(f"{ok}/{len(pairs)} lines match")
from collections import Counter
for (w, g), c in Counter(diffs).most_common(int(sys.argv[2]) if len(sys.argv) > 2 else 40):
    print(c, "want", w, "| got", g)
