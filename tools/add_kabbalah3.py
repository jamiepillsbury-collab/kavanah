"""Add Kabbalah unit 3 "Prayer and meditation" (x-kb-prayer) to data/src/x-kabbalah.json. RUN ORDER: add_kabbalah1.py, add_kabbalah2.py, then this.
Lessons x-kb-07..10. Connects to Jamie's Neshamah app (claude/neshamah-mission-principles.md: breath first; nefesh/ruach/neshamah; sleep care; low load on bad days; safety: eyes open allowed, no breath holds, stop anytime).
Bible text from sefaria-kabbalah3.json (Genesis 2:7 from sefaria-creation.json). "Try it" practice wording is mine, built on the named source."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for f in ("sefaria-kabbalah3.json", "sefaria-creation.json") for s in json.load(open(os.path.join(ROOT, "data/src", f), encoding="utf-8"))["sources"] if "text" in s}
PR = {p["id"]: p for p in json.load(open(os.path.join(ROOT, "data/prayers.json"), encoding="utf-8"))["prayers"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ").replace("&thinsp;", " ")
def ty(t):
    def f(ref, note=None):
        m = re.match(r"^(.*?) \((.*)\)$", ref)
        if m and not note: ref, note = m.group(1), m.group(2)
        return {"type": t, "ref": ref, **({"note": note} if note else {})}
    return f
TN, TK, K, R, LIT = ty("torah"), ty("tanakh"), ty("kabbalah"), ty("rabbinic"), ty("liturgy")
SCH = lambda ref: {"type": "scholarly", "ref": ref, "note": "from memory, not on Sefaria; check"}
NESH = {"type": "reform", "ref": "Neshamah app: Mission and principles (Jamie's own app)", "note": "project doc claude/neshamah-mission-principles.md"}
def text(ref, src): return {"kind": "text", "sefaria": ref, "src": src}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def tryit(body, src): return {"kind": "concept", "title": "Try it", "body": body + " Eyes open or closed, as you like. Never hold your breath. Stop whenever you want.", "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
AO = [l for l in PR["c_adon_olam"]["lines"] if "אַפְקִיד" in l["he"]][0]

M1 = {"id": "x-kb-07", "title": "Every breath praises", "status": "draft", "related": [],
 "check_note": "Bereshit Rabbah 14:9 (Sefaria Midrash Rabbah 2022) read 11/13. Neshamah card from the project doc. Practice wording is mine.",
 "cards": [
  {"kind": "hook", "title": "Breath first", "body": "Jewish prayer and Jewish meditation start in the same place: **the breath**. The first human becomes alive when God breathes into him.", "src": TN("Genesis 2:7")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "A midrash reads \"Let every soul praise God\" as \"Let every breath praise God.\"", "answer": True,
   "why": "נְשָׁמָה, soul, and נְשִׁימָה, breath, sound almost alike."},
  text("Genesis 2:7", TN("Genesis 2:7")),
  term(S("Genesis 2:7", 6, 10), "\"blowing into his nostrils the breath of life\" (Genesis 2:7). The word for breath here, נִשְׁמַת, is the word **neshamah**, soul.", TN("Genesis 2:7")),
  text("Psalms 150:6", TK("Psalms 150:6")),
  concept("Every breath", "**Rabbi Levi** in the name of **Rabbi Chanina**: \"For each and every breath that a person takes, he must laud the Creator.\" Read the psalm's כׇּל הַנְּשָׁמָה, every soul, as every **breath**.", R("Bereshit Rabbah 14:9")),
  chk("q1", "breath", "why", "How does Bereshit Rabbah 14:9 read \"Let every soul praise God\"?", ["Praise God for every single breath", "Only souls in heaven praise God", "Praise God once a day"],
      "Soul and breath: **neshamah, neshimah**.", ["Not the Midrash's reading.", "The Midrash says every breath."], look_again=5),
  concept("Five names for the soul", "The same Midrash gives the soul **five names**: **nefesh**, life, linked to the blood; **ruach**, wind, which rises and falls; **neshamah**, breath and understanding; **chayah**, living; and **yechidah**, the one-and-only.", R("Bereshit Rabbah 14:9")),
  concept("Your Neshamah app", "Your app **Neshamah** is built on this: its first principle is **breath**. God breathed life into the first human; nefesh, ruach and neshamah are all words of breath; and the gate to wellness is breath. Kabbalah and Neshamah begin at the same door.", NESH),
  chk("q2", "five", "pick", "According to Bereshit Rabbah 14:9, how many names does the soul have?", ["Five", "Three", "Ten"],
      "Nefesh, ruach, neshamah, chayah, **yechidah**.", ["There are five.", "That is the sefirot."], look_again=7),
  tryit("Breathe in slowly through your nose. As you breathe out, silently say one word of thanks. Do this for three breaths.", R("Bereshit Rabbah 14:9", "practice wording is mine")),
  {"kind": "reflect", "prompt": "If every breath can be praise, what changes about an ordinary breath you take today?"},
  {"kind": "recap", "points": ["God breathed **the breath of life** (Genesis 2:7).", "\"**For each and every breath** that a person takes, he must laud the Creator.\"", "Five names: **nefesh, ruach, neshamah, chayah, yechidah**.", "Neshamah, your app: **breath first**."]}]}

M2 = {"id": "x-kb-08", "title": "Waiting an hour", "status": "draft", "related": [],
 "check_note": "Mishnah Berakhot 5:1, Berakhot 32b, 28b and Tzava'at HaRivash 63, 137 (Markel 2020) read on Sefaria 11/13. Lurianic kavanot summary from memory: check.",
 "cards": [
  {"kind": "hook", "title": "Arriving before praying", "body": "The rabbis knew you can't jump into prayer cold. The earliest Jewish meditation we know of is simply **waiting before prayer**.", "src": R("Mishnah Berakhot 5:1")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "According to the Mishnah, how long did the early pious wait before praying?", "choices": ["An hour", "A minute", "A whole day", "Until sunset"], "answer": 0,
   "why": "And the Talmud adds an hour **after**, too."},
  concept("Focusing the heart", "The early pious would **wait an hour** before praying, \"so that they would focus their hearts toward their Father in Heaven.\" Once standing in prayer, they would not interrupt, even for a king's greeting.", R("Mishnah Berakhot 5:1")),
  concept("And an hour after", "**Rabbi Yehoshua ben Levi**: wait an hour **after** praying too, as it says, \"the upright will sit before You\" (Psalm 140:14). A teaching adds the hour before from \"Happy are those who dwell in Your House\" (Psalm 84:5).", R("Berakhot 32b")),
  chk("q1", "after", "why", "Why does Berakhot 32b say to wait after praying as well?", ["To stay and sit in God's presence once prayer ends", "To make sure no one interrupted", "To count the prayers"],
      "Prayer has **a doorway in and a doorway out**.", ["Not the Talmud's reason.", "Not the Talmud's reason."], look_again=3),
  concept("Know before whom you stand", "**Rabbi Eliezer's** advice to his students: \"when you pray, know before Whom you stand.\"", R("Berakhot 28b")),
  concept("Letters full of light", "The Kabbalists of Safed prayed with **kavanot**, detailed meditations on divine names inside each word. Hasidism made it simpler and closer: the Baal Shem Tov taught that \"every letter you utter contains worlds, souls, and Godliness.\"", K("Tzava'at HaRivash 137 (trans. Amiram and Yehudah Shimon Markel, 2020); Lurianic kavanot from memory, check")),
  chk("q2", "letters", "pick", "According to the Baal Shem Tov's teaching, what does every letter of prayer contain?", ["Worlds, souls, and Godliness", "Only sound", "A number"],
      "Each letter as **a vessel of light**.", ["Not the teaching.", "Not this teaching."], look_again=6),
  concept("On a hard day", "The same book: if your mind is **diminished**, it is better to pray **from the book** than from memory; seeing the words and letters helps you pray with more intention. Like Neshamah's **bad-day** design: lower the load, and let the page carry you.", K("Tzava'at HaRivash 63 (trans. Amiram and Yehudah Shimon Markel, 2020)")),
  tryit("Before you pray, sit for one minute. Feel your feet and the chair, and let three slow breaths go out longer than they come in. Begin when you are ready. Afterward, sit for one more breath before you get up.", R("Mishnah Berakhot 5:1; Berakhot 32b", "practice wording is mine")),
  {"kind": "reflect", "prompt": "The pious waited an hour; most of us rush in. What would a one-minute doorway into your prayer, or your day, look like?"},
  {"kind": "recap", "points": ["Wait before praying to **focus the heart** (Mishnah Berakhot 5:1).", "Sit a while **after**, too (Berakhot 32b).", "\"**Know before Whom you stand**\" (Berakhot 28b).", "Every letter holds **light**; on hard days, **pray from the book**."]}]}

M3 = {"id": "x-kb-09", "title": "Entrusting the soul", "status": "draft", "related": ["prayer:c_adon_olam"],
 "check_note": "Bereshit Rabbah 14:9 and Berakhot 60b read on Sefaria 11/13. Adon Olam line from data/prayers.json. Practice wording is mine.",
 "cards": [
  {"kind": "hook", "title": "Night and morning", "body": "Jewish tradition treats **sleep** as a kind of letting go: the soul is entrusted to God at night and **returned** in the morning.", "src": R("Bereshit Rabbah 14:9")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "In the Midrash, the soul rises during sleep and draws life from above.", "answer": True,
   "why": "Rabbi Meir's teaching in Bereshit Rabbah 14:9."},
  concept("The soul at night", "**Rabbi Meir**: the neshamah fills the whole body, and when a person sleeps, \"it ascends upward and draws life for him from above.\" Sleep is not only rest; it is **renewal**.", R("Bereshit Rabbah 14:9")),
  text("Psalms 31:6", TK("Psalms 31:6")),
  term(S("Psalms 31:6", 0, 3), "\"Into Your hand I entrust my spirit\" (31:6).", TK("Psalms 31:6")),
  {"kind": "relevance", "body": "**Adon Olam** ends with the same words: " + AO["he"] + ", \"" + AO["en"] + "\"", "links": ["prayer:c_adon_olam"]},
  concept("Pure, and returned", "On waking, the Talmud teaches a blessing: \"My God, the soul You have placed within me is pure.\" You formed it, **breathed** it into me, and guard it; blessed are You **who restores souls**.", R("Berakhot 60b")),
  chk("q1", "pure", "pick", "What does the morning blessing in Berakhot 60b say about the soul?", ["It is pure", "It is tired", "It is borrowed from the angels"],
      "Each morning begins with a **pure** soul, breathed in again.", ["Not in the blessing.", "Not in the blessing."], look_again=6),
  concept("Neshamah's sleep principle", "This is why Neshamah treats **sleep care as breath care**: the neshamah is entrusted to God each night and returned each morning.", NESH),
  chk("q2", "night", "why", "According to Rabbi Meir, what does the neshamah do while we sleep?", ["Rises and draws life from above", "Stays still and waits", "Leaves for good"],
      "Sleep as **renewal**.", ["Not Rabbi Meir's teaching.", "It returns in the morning."], look_again=2),
  tryit("At night, lying down, breathe out slowly and think: into Your hand I entrust my spirit. In the morning, before getting up, take one breath and think: the soul You gave me is pure.", R("Psalms 31:6; Berakhot 60b", "practice wording is mine")),
  {"kind": "reflect", "prompt": "What would it feel like to hand the day over at night, instead of carrying it to sleep with you?"},
  {"kind": "recap", "points": ["Rabbi Meir: in sleep the soul **draws life from above**.", "\"**Into Your hand I entrust my spirit**\": Psalm 31:6 and Adon Olam.", "Morning: \"the soul You have placed within me **is pure**.\"", "Neshamah: **sleep care is breath care**."]}]}

M4 = {"id": "x-kb-10", "title": "Talking alone with God", "status": "draft", "related": [],
 "check_note": "Likutei Moharan II 25 (Mykoff, Breslov Research), Ketubot 111b, Tzava'at HaRivash 49 read on Sefaria 11/13. Abulafia/Kaplan card from memory: check. Practice wording is mine.",
 "cards": [
  {"kind": "hook", "title": "In your own words", "body": "Alongside the prayer book, Jewish mystics teach a practice with no script at all: **hitbodedut**, being alone with God.", "src": K("Likutei Moharan, Part II 25:1 (trans. Moshe Mykoff)")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "In what language did Rebbe Nachman of Breslov say to speak with God in hitbodedut?", "choices": ["Your own everyday language", "Only Hebrew", "Aramaic", "No words at all"], "answer": 0,
   "why": "The heart is drawn to **your native tongue**."},
  concept("Hitbodedut", "**Rebbe Nachman of Breslov**: \"Hitbodedut is the highest asset and greater than everything.\" Set aside time, in a room or out in a field, and **speak your piece** with your Maker.", K("Likutei Moharan, Part II 25:1 (trans. Moshe Mykoff)")),
  concept("Your own language", "Speak in **the language you normally use**, he says, because the heart is drawn to it and moved by it. Tell God **everything in your heart**, each person according to their level.", K("Likutei Moharan, Part II 25:1 (trans. Moshe Mykoff)")),
  chk("q1", "language", "why", "Why does Rebbe Nachman say to use your everyday language?", ["The heart is moved most by the language you know", "Hebrew is forbidden for private prayer", "God does not understand Hebrew"],
      "Prayer as **real conversation**.", ["He does not forbid Hebrew.", "Not his reason."], look_again=3),
  concept("Hannah, again", "The Talmud learned its laws of prayer from **Hannah**, who prayed in her heart, in her own words, without a priest.", R("Berakhot 31a")),
  text("Deuteronomy 4:4", TN("Deuteronomy 4:4")),
  term(S("Deuteronomy 4:4", 0, 3), "\"while you, who held fast to your God\" (4:4). From this word comes **devekut**, clinging to God.", TN("Deuteronomy 4:4")),
  concept("Can we cling to God?", "The Talmud asks: is it possible to cling to the Divine Presence? God is \"a devouring fire\" (Deuteronomy 4:24). Its answer is **social**: support and stay close to those who live by Torah. The **Baal Shem Tov** taught devekut **in everything**, even in ordinary conversation.", R("Ketubot 111b; Tzava'at HaRivash 49")),
  chk("q2", "devekut", "why", "How does Ketubot 111b answer whether a person can cling to God?", ["By staying close to and supporting people who live by Torah", "By climbing a mountain", "It is impossible in every way"],
      "Devekut as **closeness to good people**.", ["Not the Talmud's answer.", "The Talmud finds a way."], look_again=8),
  concept("Letters and breath", "The 13th-century Kabbalist **Abraham Abulafia** taught meditation on the **letters of divine names**, paced with the breath. These were intense practices, traditionally learned **with a teacher**. Neshamah keeps breathing gentle, **never holding the breath**.", SCH("Aryeh Kaplan, Meditation and Kabbalah (1982); Moshe Idel, The Mystical Experience in Abraham Abulafia (1988)")),
  tryit("Sit or walk somewhere quiet for five minutes. Speak to God, out loud or in a whisper, in plain English, about whatever is true today. If no words come, just breathe and say: here I am.", K("Likutei Moharan, Part II 25:1", "practice wording is mine")),
  {"kind": "reflect", "prompt": "If you spoke to God for five minutes in your own words, what would you say first?"},
  {"kind": "recap", "points": ["Rebbe Nachman: **hitbodedut**, alone with God.", "In **your own language**, everything in your heart.", "**Devekut**: clinging (Deuteronomy 4:4), through people and everyday life.", "Abulafia's letters and breath: **gentle**, with a teacher."]}]}

p = os.path.join(ROOT, "data/src/x-kabbalah.json")
d = json.load(open(p, encoding="utf-8"))
LS = (M1, M2, M3, M4)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
d["units"] = [u for u in d["units"] if u["id"] != "x-kb-prayer"] + [{"id": "x-kb-prayer", "title": "Prayer and meditation", "subtitle": "Breath, stillness, sleep, and your own words", "lessons": list(LS)}]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
