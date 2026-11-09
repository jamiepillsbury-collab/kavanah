"""Add/replace the Machpelah Explore lesson (x-st-gen-14) in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-machpelah.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-machpelah.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

L = {"id": "x-st-gen-14", "title": "Abraham and Sarah (5): Sarah's life and the cave of Machpelah", "parashah": ["Chayei Sara"], "status": "draft", "related": [],
 "check_note": "My summaries of Rashi on Genesis 23:1, 23:2 and 23:4, Bava Metzia 87a, Bereshit Rabbah 79:7 (read on Sefaria 11/09).",
 "cards": [
  {"kind": "hook", "title": "A portion called \"Life\"", "body": "This Torah portion is called **Chayei Sarah**, \"the life of Sarah,\" yet it opens with **her death** (23:1-2). Abraham comes **to mourn her and to weep for her**, then rises to find her a resting place.", "src": T("Genesis 23:1-2")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "How did Abraham get the cave of Machpelah?", "choices": ["He paid full price for it", "It was a gift he accepted", "He inherited it", "He took it in a war"], "answer": 0,
   "why": "Ephron offers it as a gift, but Abraham **insists on paying** 400 shekels of silver (23:16)."},
  text("Genesis 23:1-2"),
  term(S("Genesis 23:1-2", 9, 12), "**Sh'nei chayei Sarah**, \"the years of Sarah's life\" (23:1). The verse counts 100 years, 20 years and 7 years separately. **Rashi**: \"years\" is repeated to show that **all her years were equally good**.", R("Rashi on Genesis 23:1", "from Bereshit Rabbah 58:1")),
  concept("Why here?", "Sarah's death comes right after the binding of Isaac. **Rashi** quotes a midrash: when she heard that her son had been readied as an offering and nearly sacrificed, the shock was too much, and **she died**.", R("Rashi on Genesis 23:2", "from Pirkei DeRabbi Eliezer 32")),
  chk("q1", "years", "why", "Why does Rashi say the verse repeats the word \"years\"?", ["To show all her years were equally good", "To show she lived longer than Abraham", "Because the number was uncertain"],
      "The repetition tells us **every stage of her life was good**.", ["Rashi says nothing about comparing their ages.", "Rashi reads it as praise, not doubt."], look_again=3),
  text("Genesis 23:3-4"),
  term(S("Genesis 23:3-4", 8, 11), "**Ger v'toshav anochi imachem**, \"I am a resident alien among you\" (23:4): an outsider who has settled down. **Rashi** adds a midrash: if you sell, I'm a stranger and will pay; if not, I'll claim it as a resident, **by right**.", R("Rashi on Genesis 23:4")),
  chk("q2", "ger-toshav", "why", "What do the two words ger and toshav describe?", ["An outsider who has settled down", "A king and a servant", "A buyer and a seller"],
      "**Ger**, stranger, from another land; **toshav**, resident, settled among them. Abraham is both.", ["Neither word means king or servant.", "The words describe Abraham alone."], look_again=7),
  text("Genesis 23:10-11"),
  concept("Say little, do much", "Ephron offers the field as a **gift**, in front of everyone (23:11). Then he names a price, 400 shekels: \"what is that between you and me?\" (23:15). **Rabbi Elazar**: the righteous **say little and do much**, like Abraham running to his guests; the wicked **say much and don't do even a little**, like Ephron.", R("Bava Metzia 87a")),
  concept("Paid in full", "Abraham **weighs out the silver** in public (23:16) and buries Sarah in the cave of Machpelah (23:19). A midrash: Machpelah is one of **three places** no one can call stolen, because they were bought: the cave of Machpelah, the Temple site and Joseph's tomb.", R("Bereshit Rabbah 79:7")),
  chk("q3", "paid", "why", "Why does the midrash stress that Machpelah was paid for?", ["So no one can say it was stolen", "Because gifts were forbidden", "Because Ephron was poor"],
      "It's one of three places **bought outright**, so no one can claim it was taken.", ["Ephron did offer a gift; Abraham chose to pay.", "Nothing in the text says Ephron was poor."], look_again=11),
  {"kind": "reflect", "prompt": "Abraham mourns, and then rises to do what has to be done (23:3). What helps you move between grieving and doing? It's fine to skip this one."},
  {"kind": "recap", "points": ["**Chayei Sarah**, the life of Sarah, opens with her death.", "Rashi: **all her years were equally good**.", "**Ger v'toshav**: an outsider who has settled down.", "Bava Metzia 87a: **say little, do much** (Abraham, not Ephron).", "Machpelah was **paid for**, never taken (Bereshit Rabbah 79:7)."]}]}
for c in L["cards"]:
    if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
u["lessons"] = [l for l in u["lessons"] if l["id"] != L["id"]] + [L]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(L["cards"]))
