"""Add/replace the Rebekah Explore lesson (x-st-gen-15) in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-rebekah.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-rebekah.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

L = {"id": "x-st-gen-15", "title": "Abraham and Sarah (6): Rebekah at the well", "parashah": ["Chayei Sara"], "status": "draft", "related": ["prayer:avot"],
 "check_note": "My summaries of Rashi on Genesis 24:14, 24:57 and 24:67, Berakhot 26b (read on Sefaria 11/09). Ten camels: Genesis 24:10.",
 "cards": [
  {"kind": "hook", "title": "A test of kindness", "body": "Abraham sends his servant to find a wife for Isaac. At a well, the servant prays for a sign: the young woman who offers water **to him and to his camels** (24:12-14).", "src": T("Genesis 24:12-14")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "What sign does the servant ask God for?", "choices": ["A woman who offers water to him and his camels", "A woman from Abraham's family", "The most beautiful woman at the well", "A woman who knows Abraham's name"], "answer": 0,
   "why": "The sign is **kindness beyond what's asked**: water for a stranger, and for his camels too."},
  text("Genesis 24:12-14"),
  term(S("Genesis 24:12-14", 8, 9), "**Va'aseh chesed**, \"deal graciously\" (24:12). **Chesed**, loving-kindness, is this chapter's key word: the servant asks God for chesed, and looks for a woman who shows it. **Rashi**: if she is fitting, \"I'll know You have shown kindness to my master.\"", R("Rashi on Genesis 24:14")),
  text("Genesis 24:17-20"),
  concept("She ran", "Count Rebekah's verbs: she **hurries**, lowers her jar, gives him drink, empties it, **runs** back to the well, and draws for **all** his camels (24:18-20). He had ten camels (24:10). She does far more than she was asked.", T("Genesis 24:10, 24:18-20")),
  chk("q1", "chesed", "why", "What made Rebekah the answer to the servant's prayer?", ["She offered water to his camels too, without being asked", "She was related to Abraham", "She asked who his master was"],
      "His sign was **chesed beyond the request**, and she gave it, running back again and again.", ["She was family, but that wasn't the sign he prayed for.", "She didn't ask; she simply helped."], look_again=5),
  text("Genesis 24:57-58"),
  term(S("Genesis 24:57-58", 13, 14), "**Elech**, \"I will\" (24:58): one word. Her family says \"let us call the girl and ask her.\" **Rashi**: from here we learn that a woman is not married **without her own consent**.", R("Rashi on Genesis 24:57", "from Bereshit Rabbah 60:12")),
  chk("q2", "consent", "why", "What does Rashi learn from \"let us call the girl and ask her\"?", ["A woman is not married without her consent", "Brothers decide for their sisters", "A bride must travel the same day"],
      "Asking Rebekah teaches that **her own yes** is required.", ["The verse teaches the opposite: they ask her.", "The timing isn't Rashi's point."], look_again=8),
  term(S("Genesis 24:63-64", 2, 4), "**Lasuach basadeh**, Isaac went out \"walking in the field\" toward evening (24:63). **Lasuach** can also mean to converse, so the Talmud reads it as **prayer**: Abraham began the morning prayer, and **Isaac began Minchah**, the afternoon prayer.", R("Berakhot 26b")),
  chk("q3", "minchah", "pick", "According to Berakhot 26b, which prayer did Isaac begin?", ["Minchah, the afternoon prayer", "Shacharit, the morning prayer", "Ma'ariv, the evening prayer"],
      "From \"lasuach basadeh **toward evening**\": Isaac's prayer is the afternoon one.", ["The Talmud credits Abraham with the morning prayer.", "That isn't Isaac's; the verse says toward evening."], look_again=10),
  concept("Comfort after his mother", "Isaac brings Rebekah into **his mother Sarah's tent**, loves her, and is comforted after his mother (24:67). **Rashi** quotes a midrash: in Sarah's lifetime a **lamp burned** from one Shabbat eve to the next, there was **blessing in the dough** and a **cloud** over the tent. They stopped when she died, and **returned with Rebekah**.", R("Rashi on Genesis 24:67", "from Bereshit Rabbah 60:16")),
  {"kind": "relevance", "body": "In the Amidah's first blessing you say **Elohei Rivkah**, God of Rebekah, right after Elohei Sarah. And every **Minchah** is, in the Talmud's reading, Isaac's walk in the field.", "links": ["prayer:avot"]},
  {"kind": "recap", "points": ["The sign: **chesed beyond the request** (24:14).", "Rebekah **runs** to water ten camels.", "**Elech**, \"I will\": Rashi, no marriage **without her consent**.", "**Lasuach basadeh**: Isaac begins **Minchah** (Berakhot 26b).", "Sarah's lamp, dough and cloud **return with Rebekah** (Rashi 24:67)."]}]}
for c in L["cards"]:
    if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
u["lessons"] = [l for l in u["lessons"] if l["id"] != L["id"]] + [L]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(L["cards"]))
