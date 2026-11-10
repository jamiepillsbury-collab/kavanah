"""Add/replace the Akedah Explore lesson (x-st-gen-13) in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-akedah.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-akedah.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

L = {"id": "x-st-gen-13", "title": "Abraham and Sarah (4): The binding of Isaac", "parashah": ["Vayera"], "status": "draft", "related": [],
 "check_note": "My summaries of Rashi on Genesis 22:2 and 22:6 (from Sanhedrin 89b), Rosh Hashanah 16a, Megillah 31a, Ibn Ezra on Genesis 22:19 (read on Sefaria 11/09). CBB's Rosh Hashanah reading not checked.",
 "cards": [
  {"kind": "hook", "title": "Here I am", "body": "It is one of the hardest stories in the Torah. Through it runs one word: **hineni**, here I am. Abraham says it to **God** (22:1), to **Isaac** (22:7) and to the **angel** (22:11).", "src": T("Genesis 22:1-11")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "How many times does Abraham answer \"hineni\" in this chapter?", "choices": ["Three", "Once", "Twice", "Never"], "answer": 0,
   "why": "**Three times**: to God, to Isaac, and to the angel who stops him."},
  text("Genesis 22:1-2"),
  concept("Your son, your only one", "Why does God name Isaac so slowly? **Rashi** retells a Talmudic dialogue: God: \"Your son.\" Abraham: \"I have two sons.\" God: \"Your only one.\" Abraham: \"Each is the only son of his mother.\" God: \"Whom you love.\" Abraham: \"I love them both.\" God: \"Isaac.\"", R("Rashi on Genesis 22:2", "from Sanhedrin 89b")),
  term(S("Genesis 22:1-2", 11, 12), "Here I am. Not a place but **readiness**: I'm listening, I'm present. The same word answers God, a son and an angel.", T("Genesis 22:1, 22:7, 22:11")),
  text("Genesis 22:6-8"),
  term(S("Genesis 22:6-8", 11, 14), "\"the two walked off together\" (22:6), said again in 22:8. **Rashi**: Abraham, who knew what was coming, walked with the same willingness as Isaac, who did not.", R("Rashi on Genesis 22:6")),
  term(S("Genesis 22:6-8", 32, 36), "\"It is God who will see to the sheep\" (22:8): Abraham's answer to Isaac's question. The same verb, **to see**, names the place afterward: **Adonai yireh** (22:14).", T("Genesis 22:8, 22:14")),
  text("Genesis 22:11-12"),
  concept("The ram and the shofar", "Abraham looks up and sees **a ram caught by its horns** (22:13), and offers it instead of his son. **Rabbi Abbahu**: that's why the Rosh Hashanah shofar is a **ram's horn**. God says: blow it before Me, and I will **remember the binding of Isaac**.", R("Rosh Hashanah 16a")),
  chk("q2", "shofar", "pick", "According to Rosh Hashanah 16a, why is the shofar a ram's horn?", ["To recall the ram offered instead of Isaac", "Rams were the only animals with horns", "Abraham blew it on the mountain"],
      "God says: sound a ram's horn, and **I will remember the binding of Isaac** for you.", ["Other animals have horns too; the Talmud gives a different reason.", "The Torah doesn't say Abraham blew a horn."], look_again=9),
  concept("Where is Isaac?", "At the end, \"**Abraham** then returned to his servants\" (22:19). Isaac isn't mentioned. **Ibn Ezra** (12th-century Spain): he was there, in his father's care. Those who claim Isaac was actually slaughtered and revived, he says, **contradict the text**.", R("Ibn Ezra on Genesis 22:19")),
  chk("q3", "isaac-missing", "why", "How does Ibn Ezra explain why Isaac isn't named in 22:19?", ["He was there, in Abraham's care", "He had been slaughtered and revived", "He had gone off on his own"],
      "He reads Isaac as **present and safe**, and rejects the idea that he died.", ["Ibn Ezra rejects that reading as contradicting Scripture.", "That isn't Ibn Ezra's explanation."], look_again=11),
  {"kind": "relevance", "body": "The Talmud has this chapter read on the **second day of Rosh Hashanah**, to recall the binding on the day of judgment (Megillah 31a), and the **shofar** recalls it every year. Many congregations read it on Rosh Hashanah; check what CBB reads.", "links": []},
  {"kind": "reflect", "prompt": "Hineni means being fully present. Where in your life right now would you like to be able to say hineni?"},
  {"kind": "recap", "points": ["**Hineni**: here I am, said to God, Isaac and the angel.", "Rashi: \"your son... your only one... whom you love... Isaac.\"", "**The two walked together** (Rashi 22:6).", "The ram's horn: **the shofar remembers the binding** (Rosh Hashanah 16a).", "Ibn Ezra: Isaac was there, **safe**, at the end."]}]}
for c in L["cards"]:
    if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
u["lessons"] = [l for l in u["lessons"] if l["id"] != L["id"]] + [L]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(L["cards"]))
