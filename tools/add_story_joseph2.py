"""Add/replace the Joseph lessons 2, 7, 8 (x-st-gen-29..31); also orders the Joseph lessons in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-joseph2.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-joseph2.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

L29 = {"id": "x-st-gen-29", "title": "Joseph (2): Judah and Tamar", "parashah": ["Vayeshev"], "status": "draft", "related": [],
 "check_note": "Sotah 10b read on Sefaria 11/11. 'Haker na' in 37:32 and 38:25: same Hebrew words, checked in the Masorah text.",
 "cards": [
  {"kind": "hook", "title": "A detour to Judah", "body": "In the middle of Joseph's story, the Torah turns to **Judah**. His widowed daughter-in-law **Tamar** is denied the marriage she was promised. When she is found pregnant and condemned, she quietly sends Judah his own **seal, cord and staff** (38:24-25).", "src": T("Genesis 38:24-25")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "Tamar publicly names Judah as the father.", "answer": False,
   "why": "She only sends a message: \"Examine these: whose seal and cord and staff are these?\" (38:25). Judah must decide whether to speak."},
  text("Genesis 38:25-26"),
  concept("Better a furnace than shaming another", "The Talmud learns from Tamar: she was ready to be **burned** rather than **humiliate Judah in public**. So it is better to throw yourself into a fiery furnace than to shame another person publicly.", R("Sotah 10b")),
  chk("q1", "shame", "why", "What does Sotah 10b learn from Tamar?", ["Never shame another person in public, even at great cost", "Always defend yourself first", "Keep evidence secret"],
      "Tamar risked her life **rather than shame Judah**.", ["She did the opposite, protecting Judah's dignity.", "She sent the evidence, but privately."], look_again=3),
  term(S("Genesis 38:25-26", 21, 23), "\"She is more in the right than I\" (38:26). **Judah's first admission** of wrong, long before he offers himself in Benjamin's place.", T("Genesis 38:26")),
  term(S("Genesis 38:25-26", 12, 13), "\"Examine these\" (38:25). In Hebrew it is the very phrase the brothers used when they showed Jacob Joseph's bloodied tunic (37:32). The deceiver is now the one asked **to recognize**.", T("Genesis 37:32, 38:25")),
  chk("q2", "haker", "why", "Why does Tamar's \"examine these\" echo chapter 37?", ["The brothers said the same words to Jacob about Joseph's tunic", "Joseph said it to Pharaoh", "It is the name of Judah's son"],
      "The words that deceived Jacob now confront Judah.", ["Not those words in Pharaoh's court.", "His sons are Er, Onan and Shelah."], look_again=6),
  {"kind": "reflect", "prompt": "Tamar chose not to shame Judah, and Judah chose to tell the truth. Which of those two choices is harder for you?"},
  {"kind": "recap", "points": ["Tamar sends Judah his **seal, cord and staff**, privately.", "Sotah 10b: **better a furnace** than shaming someone in public.", "\"**She is more in the right than I**\": Judah's first teshuvah.", "\"Examine these\": the words of the tunic, **returned**."]}]}

L30 = {"id": "x-st-gen-30", "title": "Joseph (7): Going down to Egypt", "parashah": ["Vayigash"], "status": "draft", "related": [],
 "check_note": "Megillah 29a read on Sefaria 11/11.",
 "cards": [
  {"kind": "hook", "title": "A night vision on the way", "body": "Joseph is alive. Old Jacob sets out for Egypt, and at night God speaks to him one last time: \"Jacob! Jacob!\" (46:1-2).", "src": T("Genesis 46:1-2")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "What does God promise Jacob about going down to Egypt?", "choices": ["\"I Myself will go down with you\"", "\"You will never see Joseph\"", "\"Stay where you are\"", "\"Egypt will make you a king\""], "answer": 0,
   "why": "\"**I Myself will go down with you** to Egypt, and I Myself will also bring you back\" (46:4)."},
  text("Genesis 46:2-4"),
  concept("The Shechinah in exile", "**Rabbi Shimon bar Yochai**: see how beloved Israel is: **wherever they were exiled, the Divine Presence went with them**. To Egypt, to Babylonia, and beyond. God doesn't stay home while the people suffer.", R("Megillah 29a")),
  chk("q1", "shechinah", "why", "What does Megillah 29a teach about exile?", ["The Divine Presence goes into exile with the people", "Exile means God has left", "Only Egypt counts as exile"],
      "\"**I Myself will go down with you**\": the Shechinah shares every exile.", ["Megillah 29a teaches the opposite.", "It names Egypt, Babylonia and more."], look_again=3),
  text("Genesis 47:9"),
  concept("Few and hard", "Pharaoh asks Jacob his age. Jacob answers: \"Few and hard have been the years of my life\" (47:9). A brother who wanted him dead, a deceiving uncle, Rachel lost on the road, a son lost for more than twenty years. The Torah lets the patriarch **say it plainly**.", T("Genesis 47:9")),
  {"kind": "reflect", "prompt": "Jacob calls his years few and hard, and still God goes down with him. Where have you felt accompanied in a hard place? It's fine to skip this one."},
  {"kind": "recap", "points": ["\"**I Myself will go down with you.**\"", "Megillah 29a: **the Shechinah goes into exile** with the people.", "Jacob: \"**Few and hard** have been the years of my life.\""]}]}

L31 = {"id": "x-st-gen-31", "title": "Joseph (8): Blessings and bones", "parashah": ["Vayechi"], "status": "draft", "related": ["prayer:shma"],
 "check_note": "Pesachim 56a and Sotah 13a read on Sefaria 11/11.",
 "cards": [
  {"kind": "hook", "title": "The last blessings", "body": "Before he dies, Jacob blesses **Joseph's sons**, then gathers **his own twelve** (48-49). Then Joseph, too, grows old.", "src": T("Genesis 48-50")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "In the Talmud's story, the line \"Blessed be the name of His glorious kingdom\" first came from Jacob.", "answer": True,
   "why": "**Pesachim 56a**: Jacob said it on his deathbed, answering his sons' Sh'ma."},
  text("Genesis 48:20"),
  concept("Ephraim before Manasseh", "Jacob crosses his hands and puts **the younger before the older** (48:20), one more time in Genesis. His words are still how parents bless their sons on Friday night: \"God make you like Ephraim and Manasseh.\"", {"type": "tradition", "ref": "Genesis 48:20"}),
  text("Genesis 49:1-2"),
  concept("Sh'ma, our father Israel", "Jacob wants to reveal **the end of days**, but the Divine Presence leaves him. He fears one of his sons is unfit, as Ishmael and Esau were. His sons answer: **\"Hear, Israel\"** (their father's name) **\"the Lord is our God, the Lord is One.\"** Jacob answers: **\"Blessed be the name of His glorious kingdom for ever and ever.\"**", R("Pesachim 56a")),
  chk("q1", "shma", "why", "In Pesachim 56a, why do Jacob's sons say \"Hear, Israel\"?", ["To reassure their father, Israel, that they all share his one God", "To start a prayer service", "To ask him to bless them"],
      "As there is one God in their father's heart, so there is in theirs. Jacob answers with **Baruch shem**.", ["The setting is a deathbed, not a service.", "They reassure him; he already blessed them."], look_again=5),
  text("Genesis 50:24-25"),
  concept("Carry up my bones", "Joseph makes his brothers swear: \"you shall carry up my bones from here\" (50:25). Generations later, while all Israel gathered **Egypt's riches** at the Exodus, **Moses** busied himself with **Joseph's coffin**. The Talmud: see how beloved mitzvot are to Moses.", R("Sotah 13a")),
  chk("q2", "bones", "why", "What was Moses doing, according to Sotah 13a, while the people took Egypt's riches?", ["Carrying Joseph's coffin", "Counting the people", "Writing the Torah"],
      "**Keeping the oath** to Joseph: a mitzvah over treasure.", ["The Talmud highlights the coffin.", "Not at that moment."], look_again=8),
  {"kind": "relevance", "body": "Every time you say **Sh'ma Yisrael** and the quiet **Baruch shem k'vod malchuto**, you echo Jacob's sons and Jacob's answer.", "links": ["prayer:shma"]},
  {"kind": "recap", "points": ["\"**God make you like Ephraim and Manasseh.**\"", "Pesachim 56a: Jacob's sons say **Sh'ma**, Jacob answers **Baruch shem**.", "\"**Carry up my bones.**\"", "Sotah 13a: Moses chose **the coffin over the treasure**."]}]}
LS = (L29, L30, L31)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
ids = [L["id"] for L in LS]
rest = [l for l in u["lessons"] if l["id"] not in ids]
new = {L["id"]: L for L in LS}
order = []
for l in rest:
    order.append(l)
    if l["id"] == "x-st-gen-24": order.append(new["x-st-gen-29"])
    if l["id"] == "x-st-gen-28": order += [new["x-st-gen-30"], new["x-st-gen-31"]]
u["lessons"] = order
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
