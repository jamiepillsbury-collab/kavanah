"""Add/replace the Jacob's ladder Explore lesson (x-st-gen-18) in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-ladder.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-ladder.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

L = {"id": "x-st-gen-18", "title": "Jacob (3): The ladder", "parashah": ["Vayetzei"], "status": "draft", "related": ["prayer:maariv_aravim", "prayer:hashkiveinu"],
 "check_note": "My summaries of Berakhot 26b, Rashi on Genesis 28:11, 28:12 and 28:16, Bereshit Rabbah 68:9 (read on Sefaria 11/09).",
 "cards": [
  {"kind": "hook", "title": "A night on the road", "body": "Jacob is **running from Esau**. At sunset he stops, puts a **stone** under his head, and sleeps in the open. Then he **dreams** (28:10-12).", "src": T("Genesis 28:10-12")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "In Jacob's dream, which way do the angels move first?", "choices": ["Up, then down", "Down, then up", "Only down", "They stand still"], "answer": 0,
   "why": "\"**Going up and down**\" (28:12): up first. Rashi asks why."},
  text("Genesis 28:10-11"),
  term(S("Genesis 28:10-11", 6, 8), "**Vayifga bamakom**, \"he came upon a certain place\" (28:11). The Talmud reads **pegiah**, encountering, as **prayer**: Jacob began **Ma'ariv**, the evening prayer. With Abraham's morning prayer and Isaac's afternoon prayer, that makes **three daily prayers**.", R("Berakhot 26b")),
  chk("q1", "maariv", "pick", "According to Berakhot 26b, which prayer did Jacob begin?", ["Ma'ariv, the evening prayer", "Shacharit, the morning prayer", "Minchah, the afternoon prayer"],
      "The sun had set (28:11): Jacob's prayer is the **evening** one.", ["The Talmud credits Abraham with the morning.", "That was Isaac's, toward evening in the field."], look_again=3),
  concept("The stones that argued", "Jacob takes \"one of the stones\" (28:11), but in the morning he lifts \"**the** stone\" (28:18). **Rashi** quotes a midrash: he set several stones around his head, and they argued over who would hold the righteous man's head, so God **made them one**.", R("Rashi on Genesis 28:11", "from Bereshit Rabbah 68:11")),
  text("Genesis 28:12-13"),
  concept("Up first, then down", "Why do the angels go **up** before they come down? **Rashi**: the angels who had escorted Jacob in the Land could not leave it, so they **went up**; angels for the journey abroad **came down** to accompany him.", R("Rashi on Genesis 28:12", "from Bereshit Rabbah 68:12")),
  chk("q2", "angels", "why", "Why, in Rashi's reading, do the angels go up first?", ["The Land's escort leaves and a new escort comes down", "They were bringing Jacob's prayers to heaven", "The ladder only went one way"],
      "One group of escorts **goes up**, another **comes down** to travel with him.", ["That's a lovely idea, but not Rashi's here.", "The verse says they went both ways."], look_again=7),
  term(S("Genesis 28:15", 0, 6), "**V'hinei anochi imach ush'marticha b'chol asher teilech**, \"I am with you: I will protect you **wherever you go**\" (28:15). God's promise to a man alone, at night, on the road.", T("Genesis 28:15")),
  text("Genesis 28:16-17"),
  term(S("Genesis 28:16-17", 4, 12), "**Achen yesh Adonai bamakom hazeh v'anochi lo yadati**, \"Surely Adonai is present in this place, and I did not know it!\" (28:16). **Rashi**: had I known, I would not have slept in so holy a place.", R("Rashi on Genesis 28:16")),
  concept("God, the Place", "The word **makom**, place, appears again and again in this story. The Rabbis call God **HaMakom**, the Place. **Bereshit Rabbah**: God is the place of the world, but the world is **not God's place**: the world is held in God, not the other way around.", R("Bereshit Rabbah 68:9")),
  chk("q3", "makom", "why", "What does Bereshit Rabbah 68:9 mean by calling God \"the Place\"?", ["The world exists within God, not God within the world", "God lives only in Beth-el", "God is found only in holy buildings"],
      "**God is the place of the world**; the world does not contain God.", ["The midrash says the opposite: no place contains God.", "The point is that God is everywhere, holding the world."], look_again=12),
  {"kind": "relevance", "body": "Friday night you pray **Ma'ariv Aravim**, \"who brings on the evening,\" and **Hashkiveinu**, \"help us lie down in peace.\" The Talmud traces the evening prayer to **Jacob's night** in this place.", "links": ["prayer:maariv_aravim", "prayer:hashkiveinu"]},
  {"kind": "recap", "points": ["**Vayifga bamakom**: Jacob begins **Ma'ariv** (Berakhot 26b).", "The stones argued, and God **made them one** (Rashi 28:11).", "Angels **up, then down**: a change of escort (Rashi 28:12).", "\"**I am with you** wherever you go\" (28:15).", "\"Surely Adonai is in this place\"; **HaMakom**, God as the Place (Bereshit Rabbah 68:9)."]}]}
for c in L["cards"]:
    if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
u["lessons"] = [l for l in u["lessons"] if l["id"] != L["id"]] + [L]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(L["cards"]))
