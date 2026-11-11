"""Add/replace the Jacob wrestles / meets Esau Explore lessons (x-st-gen-22, -23) in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-israel.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-israel.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

L22 = {"id": "x-st-gen-22", "title": "Jacob (7): Wrestling until dawn", "parashah": ["Vayishlach"], "status": "draft", "related": ["prayer:shma"],
 "check_note": "My summaries of Rashi on Genesis 32:8, 32:11, 32:25 and 32:29 (read on Sefaria 11/10).",
 "cards": [
  {"kind": "hook", "title": "Alone at night", "body": "Twenty years after the stolen blessing, Jacob is about to meet **Esau** again. He is afraid. He prays, sends everyone across the river, and is **left alone**. A figure wrestles with him **until dawn** (32:8-25).", "src": T("Genesis 32:8-25")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "What new name does Jacob receive that night?", "choices": ["Israel", "Abraham", "Judah", "Peniel"], "answer": 0,
   "why": "**Israel**, \"for you have striven with beings divine and human, and have prevailed\" (32:29)."},
  concept("Two fears", "\"Jacob was greatly frightened; in his anxiety...\" (32:8). Why two words? **Rashi**: he was afraid **he would be killed**, and distressed that **he might have to kill** someone.", R("Rashi on Genesis 32:8", "from Bereshit Rabbah 76:2")),
  text("Genesis 32:10-11"),
  term(S("Genesis 32:10-11", 16, 20), "\"I am unworthy of all the kindness that You have so steadfastly shown Your servant\" (32:11). **Rashi**: my merits are **diminished** by all the kindness You have already shown me.", R("Rashi on Genesis 32:11")),
  chk("q1", "fear", "why", "In Rashi's reading of 32:8, what was Jacob's second fear?", ["That he might have to kill someone", "That Esau would take his flocks", "That Rachel would leave him"],
      "Afraid of **being killed**, and distressed at the thought of **killing**.", ["Rashi says nothing about the flocks here.", "Rachel isn't part of Rashi's reading."], look_again=2),
  text("Genesis 32:25-27"),
  concept("Who was the figure?", "The Torah says only **\"a figure\"** (in Hebrew, a man). **Rashi**: the Rabbis explained he was **Esau's guardian angel**. By morning Jacob says he has seen **a divine being face to face** (32:31).", R("Rashi on Genesis 32:25", "from Bereshit Rabbah 77:3")),
  term(S("Genesis 32:25-27", 27, 31), "\"I will not let you go, unless you bless me\" (32:27). Wounded at the hip, Jacob **holds on**.", T("Genesis 32:27")),
  text("Genesis 32:28-30"),
  term(S("Genesis 32:28-30", 11, 17), "\"...but Israel, for you have striven with beings divine and human, and have prevailed\" (32:29). **Rashi**: no longer will it be said that the blessings came to you **by supplanting**, but by **noble conduct**, in the open.", R("Rashi on Genesis 32:29")),
  chk("q2", "israel", "why", "According to Rashi, what does the change from Jacob to Israel mean?", ["His blessings now come openly, not by supplanting", "He has become a king", "He is forbidden to use the name Jacob"],
      "**Yaakov** echoes the heel and supplanting; **Yisrael**, striving and prevailing in the open.", ["Rashi doesn't speak of kingship.", "The Torah keeps calling him Jacob too; Rashi's point is how his blessings are earned."], look_again=10),
  concept("Limping into the sunrise", "Jacob names the place **Peniel**: \"I have seen a divine being face to face, yet my life has been preserved.\" Then \"the sun rose upon him\" as he passed, **limping on his hip** (32:31-32).", T("Genesis 32:31-32")),
  {"kind": "relevance", "body": "Every time you say **Sh'ma Yisrael**, you use the name Jacob earned that night.", "links": ["prayer:shma"]},
  {"kind": "reflect", "prompt": "Jacob won't let go until he's blessed, and walks away limping. Is there a struggle you've come through changed? It's fine to skip this one."},
  {"kind": "recap", "points": ["Rashi 32:8: afraid **to be killed**, and **to kill**.", "\"**I am unworthy** of all the kindness\" (32:11).", "A figure, Rashi: **Esau's guardian angel**.", "\"**I will not let you go, unless you bless me.**\"", "**Israel**: blessings won in the open (Rashi 32:29); Jacob limps into the sunrise."]}]}

L23 = {"id": "x-st-gen-23", "title": "Jacob (8): Esau runs to meet him", "parashah": ["Vayishlach"], "status": "draft", "related": [],
 "check_note": "My summaries of Rashi on Genesis 33:4 (from Bereshit Rabbah 78:8 and Sifrei Bamidbar 69), read on Sefaria 11/10. The dots over vayishakehu are in Sefaria's Masorah text.",
 "cards": [
  {"kind": "hook", "title": "Four hundred men", "body": "Jacob sees **Esau coming with four hundred men**. He places his family in rows, **Rachel and Joseph last**, walks ahead, and **bows to the ground seven times** (33:1-3).", "src": T("Genesis 33:1-3")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "When they meet, Esau attacks Jacob.", "answer": False,
   "why": "\"Esau **ran** to greet him. He **embraced** him and, falling on his neck, he **kissed** him; and **they wept**\" (33:4)."},
  text("Genesis 33:1-4"),
  term(S("Genesis 33:1-4", 43, 44), "\"he kissed him\" (33:4). In the Masoretic text this word carries **dots over its letters**. **Rashi**: the sages disagreed. Some say Esau **did not kiss him wholeheartedly**. **Rabbi Shimon bar Yochai**: Esau hated Jacob, but at that moment his **pity was truly aroused**, and he kissed him **with his whole heart**.", R("Rashi on Genesis 33:4", "from Sifrei Bamidbar 69")),
  chk("q1", "dots", "why", "What does Rabbi Shimon bar Yochai learn from the dots over \"he kissed him\"?", ["At that moment Esau kissed him with his whole heart", "Esau's kiss was fake", "The word should be erased"],
      "Despite the old hatred, **in that moment** Esau's pity was real.", ["That's the other opinion Rashi reports.", "No one suggests erasing it; the dots invite interpretation."], look_again=3),
  concept("Why he embraced him", "**Rashi**: Esau's pity was aroused when he saw Jacob **bowing to the ground so many times**. Seven bows, and a twenty-year grudge gives way.", R("Rashi on Genesis 33:4", "from Bereshit Rabbah 78:8")),
  text("Genesis 33:10"),
  term(S("Genesis 33:10", 12, 17), "\"to see your face is like seeing the face of God\" (33:10). The night before, Jacob saw a divine being **face to face** (32:31). Now he sees God in **his brother's face**.", T("Genesis 32:31, 33:10")),
  chk("q2", "face", "pick", "What does Jacob tell Esau seeing his face is like?", ["Seeing the face of God", "Seeing their father again", "Looking in a mirror"],
      "\"To see your face is like **seeing the face of God**\" (33:10).", ["Isaac isn't mentioned here.", "Not in the text."], look_again=7),
  {"kind": "reflect", "prompt": "Twenty years after the stolen blessing, Esau runs to his brother. What do you think made this meeting possible?"},
  {"kind": "recap", "points": ["Jacob bows **seven times**; Esau **runs** to him.", "Dots over \"he kissed him\": Rabbi Shimon bar Yochai, **with his whole heart** (Rashi 33:4).", "Esau's pity was aroused by Jacob's bowing.", "\"To see your face is like seeing **the face of God**.\""]}]}
for L in (L22, L23):
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
ids = [L["id"] for L in (L22, L23)]
u["lessons"] = [l for l in u["lessons"] if l["id"] not in ids] + [L22, L23]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in (L22, L23)])
