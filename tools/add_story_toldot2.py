"""Add/replace the Jacob and Esau (2) Explore lesson (x-st-gen-17) in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-blessing.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-blessing.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

L = {"id": "x-st-gen-17", "title": "Jacob and Esau (2): The stolen blessing", "parashah": ["Toldot"], "status": "draft", "related": [],
 "check_note": "My summaries of Rashi on Genesis 27:1, 27:19 and 27:22 (from Midrash Tanchuma) and Bereshit Rabbah 67:4, read on Sefaria 11/09.",
 "cards": [
  {"kind": "hook", "title": "One blessing, two brothers", "body": "Isaac is old and **cannot see**. He plans to bless **Esau**. Rebekah overhears, and sends **Jacob** in to take the blessing in disguise (27:1-17).", "src": T("Genesis 27:1-17")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "When Isaac asks \"Which of my sons are you?\", what does Jacob answer?", "choices": ["\"I am Esau, your firstborn\"", "\"I am Jacob\"", "He says nothing", "\"Your younger son\""], "answer": 0,
   "why": "\"**I am Esau, your first-born**\" (27:19). Rashi works hard with those words, as you'll see."},
  text("Genesis 27:1-4"),
  concept("Why was Isaac blind?", "**Rashi** gives two midrashim: the **smoke** of the incense Esau's wives offered to idols dimmed his eyes; or, at the binding of Isaac, the **angels wept** and their tears fell into his eyes.", R("Rashi on Genesis 27:1", "from Midrash Tanchuma, Toldot 8")),
  text("Genesis 27:11-13"),
  text("Genesis 27:18-20"),
  concept("A lie, or not quite?", "\"Anochi Esav b'chorecha,\" I am Esau your firstborn. **Rashi** splits the sentence: \"**I am** the one bringing you food\" and \"**Esau is** your firstborn.\" He reads the words so Jacob doesn't tell an outright lie.", R("Rashi on Genesis 27:19")),
  chk("q1", "anochi", "why", "How does Rashi read Jacob's \"I am Esau your firstborn\"?", ["As two statements: \"I am the one bringing food\" and \"Esau is your firstborn\"", "As a plain lie the Torah approves", "As a mistranslation"],
      "Rashi **divides the sentence**, so each half is true.", ["Rashi tries to avoid that conclusion.", "Rashi reads the Hebrew as it stands."], look_again=6),
  term(S("Genesis 27:22", 6, 12), "\"the voice is the voice of Jacob, yet the hands are the hands of Esau\" (27:22). **Rashi**: Jacob's voice was **gentle**, \"Arise, I pray thee\"; Esau would speak **harshly**, \"Let my father arise\" (27:31).", R("Rashi on Genesis 27:22", "from Midrash Tanchuma, Toldot 11")),
  chk("q2", "voice", "why", "According to Rashi, what gave Jacob's voice away?", ["He spoke gently and politely", "His voice was higher", "He spoke Hebrew, Esau Aramaic"],
      "Jacob said **\"please\"**; Esau's way of speaking was harsh.", ["Rashi is about manner, not pitch.", "Rashi says nothing about languages here."], look_again=8),
  text("Genesis 27:33-34"),
  term(S("Genesis 27:38", 3, 7), "\"Have you but one blessing, Father?\" (27:38). Then **Esau wept aloud**. The Torah lets us hear the pain of the brother who lost.", T("Genesis 27:38")),
  concept("The cry comes back", "**Rabbi Chanina**: Jacob caused Esau **one great and bitter cry**. It was repaid generations later in Shushan, when **Mordecai** cried out \"a loud and bitter cry\" (Esther 4:1). God is patient, the midrash says, but the debt is remembered.", R("Bereshit Rabbah 67:4")),
  chk("q3", "cry", "why", "In Bereshit Rabbah 67:4, how was Esau's cry repaid?", ["By Mordecai's bitter cry in Shushan", "Jacob was never held to account", "Esau later took the blessing back"],
      "The same words, **a great and bitter cry**, come back in the Book of Esther.", ["The midrash says the opposite: God collects, patiently.", "Nothing in the Torah says Esau took it back."], look_again=12),
  {"kind": "reflect", "prompt": "Jacob is our ancestor, yet the Torah makes us hear Esau's sobbing. Why might it tell the story this way?"},
  {"kind": "recap", "points": ["Isaac, blind, plans to bless **Esau**; Rebekah sends **Jacob**.", "Rashi on 27:19: \"**I am** (bringing food); **Esau is** your firstborn.\"", "**The voice is Jacob's**: gentle, \"please\" (Rashi 27:22).", "\"**Have you but one blessing?**\" Esau weeps.", "Bereshit Rabbah 67:4: the cry returns as **Mordecai's**."]}]}
for c in L["cards"]:
    if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
u["lessons"] = [l for l in u["lessons"] if l["id"] != L["id"]] + [L]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(L["cards"]))
