"""Write data/src/x-stories_esther.json: the Esther unit (x-st-esther, 4 lessons). Hebrew sliced by word index from the Sefaria files."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for f in ("sefaria-ruth.json", "sefaria-ruth-esther.json") for s in json.load(open(os.path.join(ROOT, "data/src", f), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
TN = lambda ref: {"type": "tanakh", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
def text(ref): return {"kind": "text", "sefaria": ref, "src": TN(ref)}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}

E1 = {"id": "x-st-esther-01", "title": "Esther (1): Hidden", "status": "draft", "related": [],
 "check_note": "Megillah 13a and Chullin 139b read on Sefaria 11/11. English: JPS Tanakh gender-sensitive.",
 "cards": [
  {"kind": "hook", "title": "A book without God's name", "body": "The Book of Esther **never names God**, not once. Its heroine hides too: a Jewish orphan in the Persian king's palace who keeps her people **secret** (2:7-10).", "src": TN("Esther 2:7-10")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "God's name appears in the Book of Esther.", "answer": False,
   "why": "Not once. The Rabbis found God **hidden** in the book instead."},
  text("Esther 2:7"),
  text("Esther 2:10"),
  concept("Why \"Esther\"?", "Her Hebrew name was **Hadassah**. Why call her Esther? **Rabbi Yehuda**: because she **concealed** (masteret) the truth about herself, as the verse says, she did not reveal her people.", R("Megillah 13a")),
  chk("q1", "name", "why", "According to Rabbi Yehuda, why was Hadassah called Esther?", ["Because she concealed who she was", "Because it means star", "Because the king chose it"],
      "**Esther** sounds like **masteret**, concealing: she hid her people (2:10).", ["That's another opinion in the same passage, not Rabbi Yehuda's.", "The Talmud doesn't say so."], look_again=4),
  concept("Hidden in the Torah", "The Talmud asks: where is Esther hinted at in the Torah? In God's warning, \"**I will hide My face**\" (Deuteronomy 31:18). In Hebrew, **haster astir**: \"Esther\" is hidden inside \"I will hide.\"", R("Chullin 139b")),
  chk("q2", "hester", "why", "How does Chullin 139b find Esther in the Torah?", ["In the words \"I will hide My face\" (haster astir)", "In Esther's genealogy in Genesis", "It says she isn't hinted at"],
      "**Haster astir**: God's hidden face, and Esther's name.", ["She has no genealogy in the Torah.", "The Talmud finds a hint."], look_again=6),
  {"kind": "reflect", "prompt": "Esther hides who she is, and God is hidden in her book. When have you had to hide part of yourself, and what did it cost?"},
  {"kind": "recap", "points": ["Esther **never names God**.", "Hadassah, called **Esther** because she **concealed** (Megillah 13a).", "\"**I will hide My face**\": haster astir (Chullin 139b)."]}]}

E2 = {"id": "x-st-esther-02", "title": "Esther (2): Mordecai would not bow", "status": "draft", "related": [],
 "check_note": "Megillah 13b read on Sefaria 11/11.",
 "cards": [
  {"kind": "hook", "title": "One man standing", "body": "Every courtier at the palace gate **bows to Haman**, by royal order. **Mordecai** does not (3:2). Haman's fury turns into a plan to destroy all the Jews.", "src": TN("Esther 3:2-6")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Why was Haman glad when the lot fell on the month of Adar, according to the Talmud?", "choices": ["Moses died in Adar, so it seemed an unlucky month for the Jews", "Adar was the king's birthday", "It was the shortest month", "It was harvest time"], "answer": 0,
   "why": "He knew Moses died in Adar. He didn't know Moses was also **born** in Adar."},
  text("Esther 3:2"),
  term(S("Esther 3:2", 10, 15), "\"but Mordecai would not kneel or bow low\" (3:2). One man refuses, and the whole story turns on it.", TN("Esther 3:2")),
  concept("The lot in Adar", "Haman casts **pur**, a lot, for the date (3:7). It falls on **Adar**, and he rejoices: Moses died in Adar, a month of calamity for the Jews. **But he did not know** that Moses was also **born** in Adar.", R("Megillah 13b")),
  chk("q1", "adar", "why", "What did Haman not know about Adar, according to Megillah 13b?", ["Moses was also born in Adar", "Adar has two months in some years", "The king was born in Adar"],
      "A month of loss is also a month of birth: the turn is already hidden in the date.", ["That's true of the calendar, but not the Talmud's point.", "The Talmud speaks of Moses."], look_again=4),
  {"kind": "reflect", "prompt": "Mordecai would not bow, and Haman saw only the death in Adar, not the birth. Where might a hard date or season hold something you can't see yet?"},
  {"kind": "recap", "points": ["Everyone bows; **Mordecai will not**.", "Pur, the lot, falls on **Adar**.", "Megillah 13b: Moses **died and was born** in Adar."]}]}

E3 = {"id": "x-st-esther-03", "title": "Esther (3): For just such a crisis", "status": "draft", "related": [],
 "check_note": "Esther 5:4 initials checked by script on the Masorah text. Makom as a name of God: Bereshit Rabbah 68:9 (read 11/09, see the Jacob's ladder lesson).",
 "cards": [
  {"kind": "hook", "title": "Who knows?", "body": "Esther hesitates: going to the king unbidden can mean death. Mordecai answers with the book's most famous words (4:13-14).", "src": TN("Esther 4:13-14")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "What does Mordecai say might be the reason Esther became queen?", "choices": ["\"For just such a crisis\"", "Her beauty", "The king's whim", "To punish Haman"], "answer": 0,
   "why": "\"**Perhaps you have attained to royal position for just such a crisis**\" (4:14)."},
  text("Esther 4:13-14"),
  term(S("Esther 4:13-14", 18, 20), "\"from another quarter\" (4:14). In Hebrew, **mimakom acher**, from another **place**. **Makom**, place, is also a name the Rabbis gave to God: God is the place of the world. In a book that never names God, Mordecai speaks of help from \"another place.\"", {"type": "rabbinic", "ref": "Esther 4:14; Bereshit Rabbah 68:9"}),
  text("Esther 4:16"),
  concept("If I perish, I perish", "Esther asks all the Jews of Shushan to **fast for her three days**, and she and her maids will fast too. Then: \"I shall go to the king, though it is contrary to the law; and if I am to perish, I shall perish!\" (4:16). The orphan who hid becomes **the one who acts**.", TN("Esther 4:16")),
  chk("q1", "act", "why", "What changes in Esther in 4:16?", ["She chooses to risk her life and act", "She reveals that she is Persian", "She leaves the palace"],
      "From hiding to acting: \"**If I am to perish, I shall perish.**\"", ["She is Jewish, and soon reveals it.", "She goes toward the king, not away."], look_again=5),
  term(S("Esther 5:4", 4, 8), "\"let Your Majesty and Haman come today\" (5:4). Esther's invitation, and the **first letters** of these four Hebrew words: yod, heh, vav, heh, **the four-letter Name**. God is present at the very moment Esther acts.", TN("Esther 5:4")),
  chk("q2", "name", "why", "Where is God's Name hidden in Esther 5:4?", ["In the first letters of four words of Esther's invitation", "In the king's name", "In Mordecai's speech"],
      "Yod, heh, vav, heh: hidden **in the words of Esther's own brave act**.", ["Not in Ahasuerus's name.", "This verse is Esther speaking."], look_again=7),
  {"kind": "reflect", "prompt": "God's Name appears, hidden, in the words Esther speaks when she finally acts. Is there a moment you are being asked to act \"for just such a crisis\"?"},
  {"kind": "recap", "points": ["\"**Who knows**, perhaps you have attained to royal position for just such a crisis.\"", "**Mimakom acher**: help from \"another place\", and Makom is a name for God.", "\"**If I am to perish, I shall perish.**\"", "The Name hidden in **Esther's invitation** (5:4)."]}]}

E4 = {"id": "x-st-esther-04", "title": "Esther (4): Turned upside down", "status": "draft", "related": [],
 "check_note": "Tikkunei Zohar 57b read on Sefaria 11/11.",
 "cards": [
  {"kind": "hook", "title": "The day it flipped", "body": "On the very day the Jews' enemies expected to destroy them, \"**the opposite happened**\" (9:1). Grief becomes celebration, and Purim is born.", "src": TN("Esther 9:1")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Besides feasting, what does Esther 9:22 tell people to do on Purim?", "choices": ["Send gifts to one another and presents to the poor", "Fast all day", "Stay home", "Read the Torah twice"], "answer": 0,
   "why": "\"Sending gifts to one another and **presents to the poor**\" (9:22)."},
  text("Esther 9:1"),
  term(S("Esther 9:1", 21, 23), "\"the opposite happened\" (9:1). In Hebrew, **v'nahafoch hu**, from the verb for turning over. Purim celebrations still quote it.", {"type": "tradition", "ref": "Esther 9:1"}),
  text("Esther 9:22"),
  concept("Joy that includes the poor", "The holiday is fixed as \"days of feasting and merrymaking,\" with gifts to one another **and presents to the poor** (9:22). Purim's joy isn't complete until it reaches **those who have least**.", TN("Esther 9:22")),
  concept("A day like Purim", "The mystical **Tikkunei Zohar** hears **Purim** inside the name of the Day of Atonement, **Yom haKiPURIM**: the holiest fast and the most joyful feast are linked, and the day is destined to **change affliction into delight**.", {"type": "kabbalah", "ref": "Tikkunei Zohar 57b"}),
  chk("q1", "kippurim", "why", "How does the Tikkunei Zohar connect Purim and Yom Kippur?", ["It hears Purim in the name Yom haKippurim", "Both are fasts", "Both are in Adar"],
      "**Yom haKiPURIM**: the fast and the feast share a name, and both turn affliction into delight.", ["Purim is a feast, not a fast.", "Yom Kippur is in Tishrei."], look_again=6),
  {"kind": "reflect", "prompt": "In Ruth and Esther, God's hand is hidden and people act: Ruth's loyalty, Boaz's generosity, Esther's courage. Where is something in your life waiting to be turned around?"},
  {"kind": "recap", "points": ["**V'nahafoch hu**: the day turned upside down.", "Purim joy includes **presents to the poor**.", "Tikkunei Zohar: Purim is heard in **Yom haKippurim**."]}]}
LS = (E1, E2, E3, E4)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "stories", "units": [{"id": "x-st-esther", "title": "Esther", "subtitle": "The hidden face of God, and a woman who stops hiding", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-stories_esther.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
