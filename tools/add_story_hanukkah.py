"""Write data/src/x-stories_hanukkah.json: the Hanukkah unit (x-st-hanukkah), 4 lessons going deeper than the overview x-st-hol-02. Hebrew sliced by word index from sefaria-hanukkah.json (+ Zechariah 4:6 from sefaria-holidays.json). 1 Maccabees is paraphrased/quoted from Brenton's Septuagint on Sefaria (no vocalized Hebrew there, so no text cards)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for f in ("sefaria-hanukkah.json", "sefaria-holidays.json") for s in json.load(open(os.path.join(ROOT, "data/src", f), encoding="utf-8"))["sources"] if "text" in s}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ").replace("&thinsp;", " ")
TN = lambda ref: {"type": "torah", "ref": ref}
TK = lambda ref: {"type": "tanakh", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
A = lambda ref: {"type": "apocrypha", "ref": ref, "note": "Brenton's Septuagint, on Sefaria"}
def text(ref, src=None): return {"kind": "text", "sefaria": ref, "src": src or TK(ref)}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}

K1 = {"id": "x-st-hnk-01", "title": "Hanukkah (1): Darkness and decrees", "status": "draft", "related": [],
 "check_note": "Bereshit Rabbah 2:4, Yoma 85b and 1 Maccabees 2:32-48 (Brenton) read on Sefaria 11/12. Overview lesson: x-st-hol-02.",
 "cards": [
  {"kind": "hook", "title": "A choice on Shabbat", "body": "The king has outlawed Shabbat and the Torah. Faithful Jews hide in caves in the wilderness, and the soldiers come for them **on Shabbat**.", "src": A("1 Maccabees 1:41-61; 2:29-38")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "In 1 Maccabees, Mattathias and his followers decided to fight back even on Shabbat.", "answer": True,
   "why": "After a thousand people died refusing to fight on Shabbat, they decided to defend themselves."},
  text("Genesis 1:2", TN("Genesis 1:2")),
  term(S("Genesis 1:2", 4, 7), "\"with darkness over the surface of the deep\" (Genesis 1:2).", TN("Genesis 1:2")),
  concept("Greece is darkness", "**Resh Lakish** reads the second verse of the Torah as the story of four empires. **Darkness** is the Greek kingdom, \"which darkened Israel’s eyes with their edicts,\" forcing Jews to write on the horn of a bull that they had **no portion in the God of Israel**. And the spirit of God hovering over the water? The spirit of the Messiah, which comes **by the merit of repentance**.", R("Bereshit Rabbah 2:4")),
  chk("q1", "darkness", "why", "In Bereshit Rabbah 2:4, why is the Greek kingdom called \"darkness\"?", ["It darkened Israel's eyes with its decrees", "It ruled only at night", "Its armies wore black"],
      "Decrees meant to cut Israel off from **its God**.", ["Not the Midrash's reason.", "Not the Midrash's reason."], look_again=4),
  concept("A thousand in the caves", "Soldiers surrounded the caves on Shabbat and offered life in exchange for obeying the king. The people refused to come out or **profane the Sabbath**. They did not even throw a stone. They said, \"Let us die all in our innocency,\" and about **a thousand** people died, with their wives and children.", A("1 Maccabees 2:32-38")),
  concept("We will fight", "**Mattathias** and his friends mourned them. If we all do as our brothers did, they said, we will be **wiped off the earth**. So they decided: whoever attacks us on Shabbat, **we will fight**, rather than all die like those in the caves.", A("1 Maccabees 2:39-41")),
  chk("q2", "shabbat", "why", "Why did Mattathias decide to fight on Shabbat?", ["Otherwise the enemy could destroy them all on the Sabbath", "Shabbat had been cancelled", "A prophet commanded it"],
      "Keeping Shabbat required **staying alive** to keep it.", ["The Torah's Shabbat still stood; the king's ban did not cancel it.", "1 Maccabees describes a decision by the people."], look_again=7),
  concept("Live by them", "The Talmud later makes this a principle. **Rabbi Shimon ben Menasya**: break one Shabbat for a person, so he will keep many Shabbatot. **Shmuel**: the Torah says these are laws a person shall \"live by\" (Leviticus 18:5), \"and not that he should die by them.\"", R("Yoma 85b")),
  chk("q3", "live", "why", "What does Shmuel learn from \"live by them\"?", ["Saving a life comes before keeping a commandment", "Live in the Land of Israel", "Only the living may study Torah"],
      "Mitzvot are for **life**: when a life is at stake, it comes first.", ["Not Shmuel's teaching.", "Not Shmuel's teaching."], look_again=9),
  {"kind": "reflect", "prompt": "The people in the caves died faithful; Mattathias chose to live and fight. When has keeping what matters most meant bending a rule?"},
  {"kind": "recap", "points": ["Bereshit Rabbah 2:4: Greece is the **darkness** of Genesis 1:2.", "A thousand died in the caves rather than **profane Shabbat**.", "Mattathias: we will **fight**, even on Shabbat.", "Yoma 85b: \"**live by them**,\" not die by them."]}]}

K2 = {"id": "x-st-hnk-02", "title": "Hanukkah (2): Eight days", "status": "draft", "related": [],
 "check_note": "1 Maccabees 4:52-59 (Brenton), Shabbat 21b, Bamidbar Rabbah 15:6 and Megillah 31a read on Sefaria 11/12.",
 "cards": [
  {"kind": "hook", "title": "The same day", "body": "Judah's fighters take back the Temple, build a new altar, and dedicate it **on the very day** it had been defiled.", "src": A("1 Maccabees 4:36-59")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Which story of Hanukkah appears in 1 Maccabees?", "choices": ["Eight days of dedicating the altar, with no jar of oil", "A jar of oil that lasted eight days", "Both stories", "Neither story"], "answer": 0,
   "why": "The jar of oil first appears centuries later, **in the Talmud**."},
  concept("Dedication of the altar", "They dedicated the altar with songs, harps and cymbals, and \"kept the dedication of the altar eight days.\" Then **Judah** and his brothers ordained that these days be kept **every year**, eight days from the **25th of Kislev**.", A("1 Maccabees 4:52-59")),
  chk("q1", "dedication", "pick", "According to 1 Maccabees, what did the first eight days celebrate?", ["The dedication of the new altar", "A jar of oil", "The death of Antiochus"],
      "**Hanukkah**: dedication.", ["That story comes later, in the Talmud.", "Not in this passage."], look_again=2),
  concept("What is Hanukkah?", "The Talmud asks, and quotes an older source: when the Greeks entered the Temple they defiled the oil. The Hasmoneans found **one jar** still sealed by **the High Priest**, enough for one day. \"A miracle occurred and they lit the candelabrum from it eight days.\" The next year the Sages made these days a festival of **Hallel and thanksgiving**.", R("Shabbat 21b")),
  chk("q2", "cruse", "why", "In Shabbat 21b, how did they know the jar of oil was pure?", ["It still had the High Priest's seal", "A prophet told them", "It was buried under the altar"],
      "One jar the Greeks had not touched: **sealed by the High Priest**.", ["Not in the Talmud.", "Not in the Talmud."], look_again=4),
  text("Numbers 8:2", TN("Numbers 8:2")),
  term(S("Numbers 8:2", 4, 6), "\"When you mount the lamps\" (8:2).", TN("Numbers 8:2")),
  concept("Aaron's lamps", "On Hanukkah the Torah reading is the **princes' gifts for dedicating the altar** (Numbers 7). The Midrash notices that every tribe's prince brought a gift, except Levi's: **Aaron**, who worried it was his fault. God answered: you are meant for something greater. The offerings last only while the Temple stands, \"But the candles, forever.\"", R("Bamidbar Rabbah 15:6; Megillah 31a")),
  chk("q3", "lamps", "why", "In Bamidbar Rabbah 15:6, why is Aaron's task greater than the princes' gifts?", ["Offerings end with the Temple, but the lamps last forever", "Aaron's gift was larger", "Aaron was older"],
      "**The candles, forever**: a light that outlasts the Temple.", ["Aaron brought no gift with the princes.", "Not the Midrash's reason."], look_again=8),
  {"kind": "reflect", "prompt": "Hanukkah means dedication, and the altar was rededicated on the very day it had been defiled. What in your life could use rededicating?"},
  {"kind": "recap", "points": ["1 Maccabees: **eight days** dedicating the altar, from 25 Kislev.", "Shabbat 21b: **one sealed jar**, eight days of light.", "Bamidbar Rabbah 15:6: \"**the candles, forever**.\""]}]}

K3 = {"id": "x-st-hnk-03", "title": "Hanukkah (3): Adding light", "status": "draft", "related": [],
 "check_note": "Shabbat 21b, 22a and 23a read on Sefaria 11/12.",
 "cards": [
  {"kind": "hook", "title": "How many lights?", "body": "The Talmud asks how to light for Hanukkah, and the two great schools, **Beit Shammai** and **Beit Hillel**, disagree.", "src": R("Shabbat 21b")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Which school said to light one light the first night and add one each night?", "choices": ["Beit Hillel", "Beit Shammai", "Rabbi Akiva", "The Hasmoneans"], "answer": 0,
   "why": "Beit Shammai started with eight and went **down**; Beit Hillel started with one and went **up**."},
  concept("One light, or more", "The basic mitzvah: **one light** each night for a whole household. Those who take extra care light **one for each person**. Those who take even more care change the number each night: **Beit Shammai** start with eight and go down; **Beit Hillel** start with one and go up.", R("Shabbat 21b")),
  concept("Why up, why down", "Two elders in Sidon each explained their practice. One: the lights match the **bulls of Sukkot**, which went down day by day. The other: \"One elevates to a higher level in matters of sanctity and one does not downgrade.\"", R("Shabbat 21b")),
  chk("q1", "increase", "why", "What reason is given for Beit Hillel's adding a light each night?", ["In holiness, you go up, not down", "There was more oil each day", "Hillel liked even numbers"],
      "**Go up in holiness.**", ["Not in the Talmud.", "Not in the Talmud."], look_again=3),
  concept("For all to see", "Put the Hanukkah lamp **outside the door**, so everyone can see it; upstairs, in a window facing the street. In a time of danger, the table is enough. And **Rav**: do not count money by its light, so that **mitzvot do not become cheap** in your eyes.", R("Shabbat 21b; Shabbat 22a")),
  chk("q2", "outside", "pick", "Where does the Talmud say to place the Hanukkah lamp?", ["Outside the door, where everyone can see it", "Hidden in a back room", "On the roof, above twenty cubits"],
      "The point is that the light is **seen**.", ["Only in a time of danger is it brought inside.", "Above twenty cubits, people do not look up to see it (22a)."], look_again=5),
  concept("They too were in that miracle", "**Rabbi Yehoshua ben Levi**: women are obligated to light, \"as they too were included in that miracle.\"", R("Shabbat 23a")),
  text("Deuteronomy 17:11", TN("Deuteronomy 17:11")),
  concept("Where did God command us?", "The blessing says God **commanded us** to light, but Hanukkah is not in the Torah. So where? **Rav Avya**: from this verse, \"you must not deviate from the verdict that they announce to you.\" Following the Sages' rulings is itself a mitzvah. **Rav Nechemya**: from \"Ask your father, and he will declare unto you\" (Deuteronomy 32:7).", R("Shabbat 23a")),
  chk("q3", "commanded", "why", "How can the Hanukkah blessing say God \"commanded us\" to light?", ["The Torah commands us to follow the Sages' rulings", "Hanukkah is hidden in Genesis", "Moses lit the first Hanukkah lamp"],
      "A rabbinic mitzvah rests on **the Torah's trust in its teachers**.", ["Not in the Talmud.", "Not in the Talmud."], look_again=9),
  {"kind": "reflect", "prompt": "Beit Hillel adds one light each night. What small practice could you grow, a little at a time?"},
  {"kind": "recap", "points": ["One light, a light per person, or **a changing number**.", "Beit Hillel: **go up** in holiness (Shabbat 21b).", "Light it **where it can be seen**.", "Women too: \"**they too were included in that miracle**.\"", "\"Commanded us\": through **Deuteronomy 17:11**."]}]}

K4 = {"id": "x-st-hnk-04", "title": "Hanukkah (4): Not by might", "status": "draft", "related": [],
 "check_note": "Megillah 31a and Shabbat 23b read on Sefaria 11/12. Rabbi's-teaching card: the connection is mine; check with Jamie.",
 "cards": [
  {"kind": "hook", "title": "The prophet's lampstand", "body": "On Shabbat of Hanukkah, the haftarah is a prophet's vision of **a golden lampstand**.", "src": R("Megillah 31a")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "The Talmud names Zechariah's vision of the lamps as the haftarah for Shabbat of Hanukkah.", "answer": True,
   "why": "Megillah 31a: \"the lamps of Zechariah\" (Zechariah 2:14 to 4:7)."},
  text("Zechariah 2:14"),
  text("Zechariah 4:2-3"),
  term(S("Zechariah 4:2-3", 8, 10), "\"a lampstand all of gold\" (4:2).", TK("Zechariah 4:2")),
  concept("Two Shabbatot", "On each day of Hanukkah the Torah reading comes from the **princes' dedication gifts** (Numbers 7). The haftarah is **the lamps of Zechariah**. If Hanukkah has two Shabbatot, the second reads **the lamps of Solomon** in the Temple (1 Kings 7:40-50).", R("Megillah 31a")),
  chk("q1", "haftarah", "pick", "What is the haftarah for a second Shabbat of Hanukkah?", ["The lamps of Solomon's Temple", "The book of Jonah", "The Song of Hannah"],
      "Two Shabbatot, **two sets of lamps**.", ["Jonah is read on Yom Kippur.", "Hannah is read on Rosh Hashanah."], look_again=5),
  term(S("Zechariah 4:6", 8, 17), "\"Not by might, nor by power, but by My spirit\" (4:6).", TK("Zechariah 4:6")),
  concept("Lights that teach", "**Rav Huna**: whoever regularly lights for **Shabbat and Hanukkah** will have children who are Torah scholars, who spread the light of Torah. Passing the house of **Rabbi Avin the carpenter**, who lit many lights, Rav Huna said: two great men will come from here. And two of his sons became great rabbis.", R("Shabbat 23b")),
  chk("q2", "scholars", "why", "According to Rav Huna, what comes to someone who regularly lights for Shabbat and Hanukkah?", ["Children who become Torah scholars", "Wealth", "A long life"],
      "Physical light, passed on as **the light of Torah**.", ["Not Rav Huna's promise.", "Not Rav Huna's promise."], look_again=8),
  concept("From the sword to the lamp", "1 Maccabees tells of **battles** and an altar. The Talmud tells of **a jar of oil**. The haftarah says **not by might, nor by power**. Your rabbi reads the tradition as a people **growing up**, from a God who fights our battles toward God present in what we do. Hanukkah shows it: the tradition chose to remember **the light** more than the war.", {"type": "reform", "ref": "Teaching from Jamie's rabbi (oral, as Jamie retold it); 1 Maccabees 4; Shabbat 21b; Zechariah 4:6", "note": "connection to Hanukkah is mine; check with Jamie"}),
  {"kind": "reflect", "prompt": "Not by might, nor by power. Where has a quiet, steady light done more than force could?"},
  {"kind": "recap", "points": ["Haftarah: **the lamps of Zechariah** (Megillah 31a).", "\"**Not by might, nor by power, but by My spirit**\" (4:6).", "Shabbat 23b: lights at home, **light of Torah** in the children.", "From the sword **to the lamp**."]}]}

LS = (K1, K2, K3, K4)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "stories", "units": [{"id": "x-st-hanukkah", "title": "Hanukkah", "subtitle": "Darkness, dedication, and adding light", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-stories_hanukkah.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
