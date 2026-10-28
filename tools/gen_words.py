"""data/prayers.json + data/src/lexicon-bdb.tsv -> data/words.json ("Prayer words" unit).
Order: SEED words, then new words in prayer order. Glosses only from Sefaria's BDB lexicon (REJECT = wrong matches, blanked).
Run: python tools/gen_words.py"""
import json, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from translit import word_tl
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, "data/prayers.json"), encoding="utf-8"))
LEX = {}
for ln in open(os.path.join(ROOT, "data/src/lexicon-bdb.tsv"), encoding="utf-8"):
    if ln.startswith("#") or not ln.strip(): continue
    w, root, d = ln.rstrip("\n").split("\t"); LEX[w] = (root, d)
SEED = "בָּרוּךְ אַתָּה יְיָ אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם אֲשֶׁר קִדְּשָׁנוּ בְּמִצְוֹתָיו וְצִוָּנוּ".split()
# Lexicon hits that matched the wrong word (homograph or wrong root): no gloss rather than a wrong one.
REJECT = {"נֵר", "בָּנוּ", "בָנוּ", "בוֹ", "כִּי", "הוּא", "בָּרָא", "וְקִיְּמָנוּ", "וְכָל", "צְבָאָם", "הָאָרֶץ"}
USELESS = re.compile(r"^(n f|n m|adj|prep|\(.*\))$")
SAY = {"יְיָ": "אֲדֹנָי"}  # what the phone voice reads
NOTE = {"יְיָ": "Written יְיָ, read Adonai."}
PER = 6

def words(he): return [w for w in re.split(r"[\s־,.;:]+", he) if re.search(r"[א-ת]", w)]
def tr(w):
    s = word_tl(w)[0]
    s = re.sub(r"^eloh", "Eloh", s).replace("shabat", "Shabbat")
    return s, word_tl(w)[1]

order, where, freq = [], {}, {}
for w in SEED: order.append(w)
for p in sorted(P["prayers"], key=lambda p: p["order"]):
    for l in p["lines"]:
        for w in words(l["he"]):
            freq[w] = freq.get(w, 0) + 1
            where.setdefault(w, [])
            if p["id"] not in where[w]: where[w].append(p["id"])
            if w not in order: order.append(w)

items, ids = {}, []
for i, w in enumerate(order):
    t, flag = tr(w)
    g = LEX.get(w)
    gloss = None if (not g or w in REJECT or USELESS.match(g[1])) else {"root": g[0], "def": g[1], "src": "BDB (Sefaria lexicon)"}
    iid = f"w-{i+1:03d}"; ids.append(iid)
    items[iid] = {"kind": "word", "he": w, "tr": t, "tlf": flag, "say": SAY.get(w, w), "gloss": gloss,
                  "note": NOTE.get(w), "freq": freq.get(w, 0), "prayers": where.get(w, []), "audio": None}
titles = {p["id"]: p["title"] for p in P["prayers"]}
lessons = []
for n in range(0, len(ids), PER):
    chunk = ids[n:n + PER]
    porder = {p["id"]: p["order"] for p in P["prayers"]}
    firsts = [items[i]["prayers"][0] for i in chunk if items[i]["prayers"]]
    first = max(firsts, key=porder.get) if firsts else None  # the prayer this lesson completes
    lessons.append({"id": f"words-{n // PER + 1}", "title": f"Words {n // PER + 1}",
                    "subtitle": f"Toward {titles[first]}" if first else "", "items": chunk})
out = {"version": 1, "generated_by": "tools/gen_words.py",
       "units": [{"id": "u-words", "title": "Prayer words", "subtitle": "The words of the blessings, most common first", "lessons": lessons, "tiles": False}],
       "items": items}
json.dump(out, open(os.path.join(ROOT, "data/words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(items), "words,", len(lessons), "lessons,", sum(1 for x in items.values() if x["gloss"]), "with gloss,",
      sum(1 for x in items.values() if x["tlf"]), "translit flagged")
for l in lessons[:4]: print(l["title"], l["subtitle"], " ".join(items[i]["tr"] for i in l["items"]))
