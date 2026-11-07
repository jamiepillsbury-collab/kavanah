"""Compare each prayers.json line (translit) with the CBB siddur Mashiv HaRuach transliteration.
Input: sources/cbb_txt/pNNN.txt (pdftotext -layout per page; PDF page = book page). Hebrew there is images, so only translit is compared.
Output: sources/cbb_compare.txt. A line with low coverage is probably not printed at CBB (or worded differently)."""
import json, re, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(t):
    t = t.lower().replace("’", "").replace("'", "").replace("‘", "").replace("-", "").replace("kh", "ch").replace("ey", "ei")
    return [w for w in re.findall(r"[a-z]+", t)]
pages = {int(re.search(r"p(\d+)", f).group(1)): norm(open(f, encoding="utf-8", errors="replace").read())
         for f in glob.glob(os.path.join(ROOT, "sources", "cbb_txt", "p*.txt"))}
bags = {n: set(w) for n, w in pages.items()}
out = []
for p in json.load(open(os.path.join(ROOT, "data", "prayers.json"), encoding="utf-8"))["prayers"]:
    out.append(f"\n## {p['id']} ({p['title']})")
    for i, l in enumerate(p["lines"]):
        ws = [w for w in norm(l["tl"]) if len(w) > 2] or norm(l["tl"])
        best = max(bags, key=lambda n: sum(w in bags[n] for w in ws))
        cov = sum(w in bags[best] for w in ws) / max(1, len(ws))
        miss = [w for w in ws if w not in bags[best]]
        out.append(f"{'OK ' if cov >= .75 else ('?? ' if cov >= .45 else 'NO ')} L{i+1} p{best} {cov:.0%}  {l['tl'][:70]}" + (f"   missing: {' '.join(miss[:8])}" if miss and cov < 1 else ""))
open(os.path.join(ROOT, "sources", "cbb_compare.txt"), "w", encoding="utf-8").write("\n".join(out))
