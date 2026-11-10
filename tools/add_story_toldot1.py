"""Add/replace the Jacob and Esau (1) Explore lesson (x-st-gen-16) in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-toldot.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-toldot.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

L = {"id": "x-st-gen-16", "title": "Jacob and Esau (1): Twins and the birthright", "parashah": ["Toldot"], "status": "draft", "related": ["prayer:m_mah_tovu"],
 "check_note": "My summaries of Rashi on Genesis 25:22, 25:27 and 25:30 (with Bereshit Rabbah 63 and Bava Batra 16b), read on Sefaria 11/09. Note the Contemporary Torah renders yoshev ohalim as 'raising livestock'.",
 "cards": [
  {"kind": "hook", "title": "Two in one womb", "body": "Rebekah's twins **struggle inside her** (25:22). She asks the question people in pain ask, **why?**, and then goes **to inquire of God**.", "src": T("Genesis 25:21-23")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "Rebekah keeps her distress to herself.", "answer": False,
   "why": "She speaks it aloud and **goes to inquire of Adonai** (25:22), and God answers her."},
  text("Genesis 25:21-23"),
  term(S("Genesis 25:21-23", 19, 22), "\"why do I exist?\" (25:22). Rebekah doesn't stop at the question: she goes **lidrosh**, to seek out God.", T("Genesis 25:22")),
  concept("Running to the doors", "**Rashi** reads \"struggled\" as **running**: whenever Rebekah passed a house of Torah study, **Jacob** strained to come out; whenever she passed a pagan temple, **Esau** did. He also gives the plain reading: the twins **fought** with each other.", R("Rashi on Genesis 25:22", "from Bereshit Rabbah 63:6")),
  chk("q1", "struggle", "why", "In Rashi's midrash, why did the twins move inside Rebekah?", ["Each was drawn to a different kind of place", "They were hungry", "They wanted to be born first"],
      "Jacob toward **houses of study**, Esau toward **pagan temples**: two paths from the start.", ["Hunger isn't part of this midrash.", "Rashi's midrash here is about where each was drawn, not birth order."], look_again=4),
  text("Genesis 25:27-28"),
  term(S("Genesis 25:27-28", 10, 14), ": this translation says \"a mild man, raising livestock\"; word for word, \"a **whole** man, **dwelling in tents**.\" **Rashi**: tam means his heart matched his mouth, not clever at deceiving; the tents are the study tents of **Shem and Ever**.", R("Rashi on Genesis 25:27")),
  chk("q2", "tam", "why", "What does Rashi say tam means?", ["His words matched his thoughts", "He was physically weak", "He was the younger twin"],
      "**Tam**: whole, straightforward. What was in his heart was in his mouth.", ["Tam isn't about strength.", "Tam describes character, not birth order."], look_again=7),
  text("Genesis 25:29-31"),
  concept("A mourner's meal", "Why was Jacob cooking lentils? **Rashi**: **Abraham died that day**, and Jacob was preparing the first meal for the mourners. Lentils are **round like a wheel**, because mourning is a wheel that comes around to everyone.", R("Rashi on Genesis 25:30", "from Bava Batra 16b")),
  text("Genesis 25:32-34"),
  term(S("Genesis 25:32-34", 29, 32), "\"thus did Esau spurn the birthright\" (25:34). The Torah's own verdict comes after a rush of verbs: **he ate, drank, rose and went**.", T("Genesis 25:34")),
  chk("q3", "spurn", "pick", "Whom does the last line of the story judge?", ["Esau, for spurning the birthright", "Jacob, for driving a hard bargain", "Isaac, for loving Esau more"],
      "The verse names **Esau**: he \"spurn[ed] the birthright.\"", ["The Torah doesn't comment on Jacob here, though readers have long argued about him.", "Isaac isn't in this scene."], look_again=12),
  {"kind": "relevance", "body": "Jacob is the one who **dwells in tents**. Every Shabbat morning you open with **Mah tovu ohalecha Yaakov**, \"how good are your tents, Jacob\" (Numbers 24:5).", "links": ["prayer:m_mah_tovu"]},
  {"kind": "recap", "points": ["**Lamah zeh anochi**: Rebekah's why becomes a search for God.", "Rashi: the twins ran toward **study houses** and **temples**.", "**Ish tam**: heart and mouth matched (Rashi 25:27).", "The lentils: **a mourner's meal** for Abraham (Rashi 25:30).", "**Vayivez Esav**: the Torah's verdict on the sale."]}]}
for c in L["cards"]:
    if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
u["lessons"] = [l for l in u["lessons"] if l["id"] != L["id"]] + [L]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(L["cards"]))
