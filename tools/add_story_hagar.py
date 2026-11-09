"""Add/replace the Hagar and Ishmael Explore lesson (x-st-gen-12) in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-hagar.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-hagar.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

L = {"id": "x-st-gen-12", "title": "Abraham and Sarah (3): Hagar and Ishmael", "parashah": ["Lech Lecha", "Vayera"], "status": "draft", "related": [],
 "check_note": "My summaries of Ramban on Genesis 16:6, Rashi on Genesis 16:13 and 21:17 (read on Sefaria 11/09). 'First angel in the Torah' = first occurrence of mal'ach (16:7).",
 "cards": [
  {"kind": "hook", "title": "The first to meet an angel", "body": "The first person in the Torah to meet **a messenger of God** is not Abraham or Sarah. It is **Hagar**, Sarah's Egyptian slave, alone by a spring in the wilderness (16:7).", "src": T("Genesis 16:7")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Who is the first person in the Torah to meet an angel?", "choices": ["Hagar", "Abraham", "Sarah", "Noah"], "answer": 0,
   "why": "**Hagar** (16:7). The word mal'ach, messenger or angel, appears here for the first time."},
  text("Genesis 16:1-2"),
  concept("Ramban doesn't excuse Sarah", "Abram tells Sarai, \"Deal with her as you think right,\" and Sarai **treats Hagar harshly** until she runs away (16:6). **Ramban** (13th-century Spain): Sarah **did wrong** by this, and **Abraham did wrong** by allowing it. God heard Hagar's suffering.", R("Ramban on Genesis 16:6")),
  chk("q1", "ramban", "why", "How does Ramban judge Sarah's treatment of Hagar?", ["As a wrong, by Sarah and by Abraham", "As fair, since Hagar was her servant", "He says nothing about it"],
      "He calls it a **transgression** by Sarah, and by Abraham for allowing it.", ["Ramban says the opposite: it was wrong.", "He comments directly on 16:6."], look_again=3),
  text("Genesis 16:7-8"),
  term(S("Genesis 16:13", 4, 7), "**Atah El Ro'i**, \"You are El-roi,\" a God of seeing (16:13). Hagar names God from her own experience. Her son's name, **Yishmael**, means \"God hears\": \"for Adonai has paid heed to your suffering\" (16:11). **Rashi**: the One who sees the humiliation people suffer at others' hands.", R("Rashi on Genesis 16:13", "from Bereshit Rabbah 45:10")),
  chk("q2", "names", "why", "What do the names El-roi and Yishmael say about God?", ["God sees and God hears", "God rules and God judges", "God creates and God rests"],
      "**El-roi**: God who sees. **Yishmael**: God hears, heeding Hagar's suffering.", ["Those aren't in either name.", "Those belong to the creation story, not to Hagar."], look_again=6),
  term(S("Genesis 21:9-10", 6, 7), "**M'tzachek**, \"playing\" (21:9). Years later Sarah sees Ishmael **m'tzachek** and demands that Hagar and her son be sent away. It's the same root as **Yitzchak** and Sarah's laughter. The Torah doesn't say what kind of playing it was.", T("Genesis 21:9-10")),
  text("Genesis 21:17"),
  concept("Where he is", "\"God has heeded the cry of the boy **where he is**\" (21:17). **Rashi**: he is judged by **what he is doing now**, not by what his descendants might do later. Rashi also notes that God heard **the boy's own voice**: a sick person's own prayer is accepted more readily than others' prayers for him.", R("Rashi on Genesis 21:17", "from Rosh Hashanah 16b and Bereshit Rabbah 53:14")),
  chk("q3", "now", "why", "In Rashi's reading of \"where he is,\" how is Ishmael judged?", ["By what he is doing now", "By what his descendants will do", "By what his mother did"],
      "**As he is now.** The future doesn't decide the present.", ["Rashi rejects exactly that: the angels raised it, and God answered, what is he now?", "Hagar's actions aren't the basis here."], look_again=10),
  concept("Together at the end", "Many years later, when Abraham dies, **\"his sons Isaac and Ishmael buried him\"** in the cave of Machpelah (25:9). The brothers who were separated stand together at their father's grave.", T("Genesis 25:9")),
  {"kind": "reflect", "prompt": "Hagar names God from her own experience: El-roi, the God who sees. What name would come from yours?"},
  {"kind": "recap", "points": ["**Hagar** is the first person in the Torah to meet an angel (16:7).", "Ramban: Sarah and Abraham **did wrong** by her (16:6).", "**El-roi**, God who sees; **Yishmael**, God hears.", "Rashi on 21:17: judged **as he is now**; a person's own prayer is heard.", "Isaac and Ishmael **bury Abraham together** (25:9)."]}]}
for c in L["cards"]:
    if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
u["lessons"] = [l for l in u["lessons"] if l["id"] != L["id"]] + [L]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(L["cards"]))
