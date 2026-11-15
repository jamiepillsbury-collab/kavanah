"""Write data/src/x-history_rome.json: Jewish history unit 3 'Greeks and Romans' (x-hi-rome), 5 lessons. Hebrew sliced by word index from sefaria-history2.json.
Scholarly facts are from memory and flagged in each check_note. look_again = a card title or sefaria ref, resolved to an index at the end."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-history2.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b):
    w = " ".join(SRC[(ref, "he")]).split()[a:b]
    return " ".join(x for x in w if x not in ("׀", "{פ}", "{ס}")).replace("יְהֹוָה", "יְיָ")
TN = lambda ref: {"type": "torah" if ref.split()[0] in ("Genesis", "Leviticus", "Numbers") else "tanakh", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
SCH = lambda ref, note="From memory; check.": {"type": "scholarly", "ref": ref, "note": note}
AP = lambda ref, note="Brenton's Septuagint (English) on Sefaria": {"type": "apocrypha", "ref": ref, "note": note}
def text(ref): return {"kind": "text", "sefaria": ref, "src": TN(ref)}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def tl(when, body, src): return {"kind": "timeline", "when": when, "body": body, "src": src}
def hook(title, body, src): return {"kind": "hook", "title": title, "body": body, "src": src}
def pre(q, choices, why): return {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": q, "choices": choices, "answer": 0, "why": why}
def chk(cid, idea, typ, q, choices, why, wrong, look):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, "look_again": look}
def rel(body, links): return {"kind": "relevance", "body": body, "links": links}
def refl(p): return {"kind": "reflect", "prompt": p}
def recap(*p): return {"kind": "recap", "points": list(p)}

H7 = {"id": "x-hi-07", "title": "The Greeks arrive", "status": "draft", "related": [],
 "check_note": "Yoma 69a, Avot 1:2 (Mishnah Yomit), Megillah 9a-b read on Sefaria 11/14. Dates, Josephus's parallel, the gymnasium (2 Maccabees 4) and Septuagint dating are from memory: check.",
 "cards": [
  hook("A new world power", "In **332 BCE**, Alexander of Macedon sweeps through the Persian empire. Judea, a small temple-state around Jerusalem, now lives in a **Greek** world.", SCH("Alexander's conquests")),
  pre("In the Talmud's story, what did Alexander do when he met the High Priest Shimon HaTzaddik?", ["Got down from his chariot and bowed to him", "Arrested him", "Asked to become a Jew", "Ignored him"],
      "Yoma 69a: the conqueror **bows**."),
  concept("The king bows", "The Samaritans won Alexander's permission to destroy the Temple. **Shimon HaTzaddik** put on the high priest's garments and walked all night, with Jerusalem's leaders carrying torches. At dawn the two camps met. Alexander **got down from his chariot and bowed**. Asked why, he said this man's face went before him to victory in every battle. Josephus tells a similar story; most historians doubt it happened.", R("Yoma 69a", "Josephus, Antiquities 11: from memory; check.")),
  chk("q1", "alexander", "why", "In Yoma 69a, why does Alexander bow to Shimon HaTzaddik?", ["He had seen his face going before him to victory", "He was afraid of the Jewish army", "Shimon paid him tribute"],
      "The story makes the **priest**, not the conqueror, the greater power.", ["Not in the Talmud.", "Not in the Talmud."], "The king bows"),
  concept("Three things", "The Mishnah remembers the same Shimon as a teacher: \"the world stands upon three things\": the **Torah**, the **Temple service**, and **acts of piety**.", R("Pirkei Avot 1:2", "English: Mishnah Yomit")),
  tl("332 BCE", "**Alexander** takes the land; after his death his generals split the empire.", SCH("Conventional date")),
  tl("c. 301-200 BCE", "The **Ptolemies** of Egypt rule Judea. Alexandria becomes a great Jewish city.", SCH("Conventional dates")),
  tl("200 BCE", "The **Seleucids** of Syria take Judea from Egypt.", SCH("Battle of Panium")),
  concept("Becoming Greek", "Greek was now the language of trade, law and learning. Jews took Greek names: **Jason**, **Alexander**. In Jerusalem some built a **gymnasium**; others saw Greek ways as a threat to the covenant. That split will matter in the next lesson.", SCH("Gymnasium: 2 Maccabees 4")),
  concept("Seventy-two elders", "King **Ptolemy** gathered seventy-two elders, put each in a separate room, and told each to translate the Torah. God put wisdom in every heart, and **all seventy-two wrote the same**. Scholars call this Greek Torah the **Septuagint**, made in Alexandria in the 3rd century BCE for Jews who no longer read Hebrew.", R("Megillah 9a; scholars: Letter of Aristeas, Septuagint", "Dating from memory; check.")),
  chk("q2", "septuagint", "pick", "Who, in tradition, translated the Torah into Greek?", ["Seventy-two elders, each in a separate room", "Alexander's scribes", "Ezra"],
      "The **Septuagint** (Greek for seventy).", ["Not in the sources.", "Ezra is linked to the square script, not Greek."], "Seventy-two elders"),
  text("Genesis 9:27"),
  term(S("Genesis 9:27", 0, 5), "\"May God enlarge Japheth, And let him dwell in the tents of Shem\" (9:27). Greece descends from Japheth, through Javan.", TN("Genesis 9:27")),
  concept("Japheth's beauty", "Rabban Shimon ben Gamliel allows a Torah scroll in **Greek**. His proof is this verse: Greek, the language of Japheth's son Javan, may live **in the tents of Shem**, where Torah is studied.", R("Megillah 9b")),
  chk("q3", "japheth", "why", "How does Megillah 9b use Genesis 9:27?", ["To allow Torah in Greek, Japheth's language, in Shem's tents", "To ban Greek books", "To explain the flood"],
      "A **welcome**, within limits, to Greek culture.", ["It does the opposite.", "Not the Talmud's use."], "Japheth's beauty"),
  rel("Next comes the clash with Greek rule that Hanukkah remembers. Its stories are in the Hanukkah unit.", ["lesson:x-st-hnk-01"]),
  refl("Jews have always borrowed from the cultures around them. What from your own world has deepened your Judaism?"),
  recap("**332 BCE**: Alexander; Judea in a Greek world.", "Yoma 69a: the conqueror **bows** to the high priest.", "Avot 1:2: Torah, Temple service, **acts of piety**.", "Megillah 9a: **seventy-two elders**, one translation.", "Megillah 9b: Japheth's language **in Shem's tents**.")]}

H8 = {"id": "x-hi-08", "title": "The Hasmonean kings", "status": "draft", "related": [],
 "check_note": "1 Maccabees 14 (Brenton), Kiddushin 66a read on Sefaria 11/14. Dates, the three parties (Josephus) and the scholarly reading of why the rabbis stress the oil are from memory: check.",
 "cards": [
  hook("From rebels to rulers", "The **Maccabees** won back the Temple in 164 BCE. Then Judah's brothers did something larger: they built a **Jewish state**, independent for the first time since Babylon.", AP("1 Maccabees 13-14")),
  pre("In 1 Maccabees 14, what did the people make Simon the Hasmonean?", ["Governor and high priest, until a faithful prophet arose", "King of Judea and Egypt", "An exile", "A judge for one year"],
      "Ruler and high priest, **with a condition**."),
  tl("167-164 BCE", "The **revolt**; the Temple rededicated: Hanukkah.", SCH("Conventional dates")),
  tl("140 BCE", "**Simon** becomes high priest and ruler: the Hasmonean state.", SCH("Conventional date")),
  tl("104-76 BCE", "**Alexander Yannai**, king and high priest, conquers widely.", SCH("Conventional dates")),
  tl("63 BCE", "Rome's general **Pompey** takes Jerusalem. Independence ends.", SCH("Conventional date")),
  concept("Until a faithful prophet", "The Jews and priests agreed that Simon would be their \"governor and high priest for ever, until there should arise a faithful prophet.\" The Hasmoneans were **priests**, not of David's line. The word **until** leaves room for God to say otherwise.", AP("1 Maccabees 14:41")),
  chk("q1", "simon", "why", "Why does the decree for Simon say \"until there should arise a faithful prophet\"?", ["His rule was not from David's line, so it stayed open to God's word", "He was too young to rule", "Rome demanded it"],
      "A priestly ruler, **provisional** in the eyes of tradition.", ["Not in the text.", "Rome is a friend here, not a master."], "Until a faithful prophet"),
  concept("Three parties", "Under the Hasmoneans, Jews divided. **Pharisees**: teachers of the oral tradition, ancestors of the rabbis. **Sadducees**: the priestly elite, holding to the written Torah. **Essenes**: a strict, separate group; many scholars link them to the **Dead Sea Scrolls** at Qumran.", SCH("Josephus, Antiquities 13 and 18")),
  concept("The king and the sages", "King **Yannai** came home from conquering sixty cities and threw a feast for the sages. A troublemaker, Elazar ben Po'ira, turned him against them, and the sages were killed. The world was empty of Torah until **Shimon ben Shatach** \"restored the Torah to its former glory.\"", R("Kiddushin 66a")),
  chk("q2", "yannai", "pick", "In Kiddushin 66a, who restored the Torah after Yannai killed the sages?", ["Shimon ben Shatach", "Judah Maccabee", "Hillel"],
      "The rabbis' hero here is a **sage**, not a king.", ["Judah lived before Yannai.", "Hillel came a generation later."], "The king and the sages"),
  concept("Why the oil?", "The Talmud remembers Hanukkah by a **jar of oil**, not by battles, and reads Zechariah: \"Not by might.\" Many scholars think the rabbis played down the Hasmonean kings after their rule turned harsh and later revolts failed. The **books of Maccabees** were not kept in the Jewish Bible.", R("Shabbat 21b; Megillah 31a", "Scholarly reading from memory; check.")),
  chk("q3", "oil", "why", "Why might the rabbis have stressed the oil over the Hasmonean victory?", ["The Hasmonean kings had become harsh rulers", "The battles never happened", "The oil story is in 1 Maccabees"],
      "Memory **chooses** what to tell.", ["1 Maccabees records the battles.", "The oil story is in the Talmud, not 1 Maccabees."], "Why the oil?"),
  rel("The Hanukkah unit tells the story from the inside: the oil, the lights, and \"Not by might.\"", ["lesson:x-st-hnk-02", "lesson:x-st-hnk-04"]),
  refl("The Maccabees fought for freedom; their grandchildren ruled harshly. What helps a movement stay true to why it began?"),
  recap("**140 BCE**: Simon, ruler and high priest \"**until... a faithful prophet**.\"", "**Pharisees, Sadducees, Essenes**.", "Kiddushin 66a: Yannai and the sages; **Shimon ben Shatach**.", "**63 BCE**: Rome. The rabbis remember the **oil**.")]}

H9 = {"id": "x-hi-09", "title": "Herod and Rome", "status": "draft", "related": [],
 "check_note": "Bava Batra 3b-4a and Shabbat 31a read on Sefaria 11/14. Herod's dates, Idumean origin, the Western Wall and Hillel's dates are from memory: check.",
 "cards": [
  hook("Rome's king", "In **37 BCE**, with Roman troops behind him, **Herod** takes Jerusalem. Rome's Senate has named him King of Judea.", SCH("Josephus, Antiquities 14")),
  pre("What does the Talmud say about Herod's rebuilt Temple?", ["Whoever has not seen it has never seen a beautiful building", "It was smaller than Solomon's", "It was never finished", "It was made of cedar"],
      "Bava Batra 4a."),
  tl("37-4 BCE", "**Herod** reigns as Rome's client king.", SCH("Conventional dates")),
  tl("c. 20 BCE", "Herod begins **rebuilding the Temple** and its vast platform.", SCH("Conventional date")),
  tl("c. 30 BCE-10 CE", "**Hillel** and **Shammai** teach in Jerusalem.", SCH("Traditional dates, approximate")),
  concept("A slave in the house", "The Talmud: \"Herod was a slave in the house of the Hasmoneans.\" He killed his masters and took the throne, then killed the sages, sparing only **Bava ben Buta**, whom he blinded. Later Bava advised him to make amends by **rebuilding the Temple**. Historians: Herod was an **Idumean**, son of a Hasmonean official, and a brilliant, brutal ruler.", R("Bava Batra 3b-4a", "Idumean origin: Josephus; check.")),
  chk("q1", "herod", "pick", "In Bava Batra 3b, how did Herod come to rebuild the Temple?", ["Bava ben Buta advised it as amends", "Rome ordered it", "The prophets demanded it"],
      "The Talmud turns a tyrant's project into **repentance**.", ["Not the Talmud's account.", "Not the Talmud's account."], "A slave in the house"),
  concept("The beautiful building", "The sages say whoever has not seen Herod's building \"has never seen a beautiful building.\" Rows of white and green marble; he thought to cover it in gold and was told to leave it. The **Western Wall** is part of the retaining wall Herod built around the Temple Mount.", R("Bava Batra 4a", "Western Wall: archaeology; check.")),
  chk("q2", "kotel", "pick", "What is the Western Wall?", ["Part of the retaining wall Herod built around the Temple Mount", "A wall of Solomon's Temple", "The wall of the Holy of Holies"],
      "Herod's **platform wall**, still standing.", ["Solomon's Temple was gone by Herod's time.", "The Temple itself was destroyed."], "The beautiful building"),
  concept("On one foot", "A non-Jew asked to learn the whole Torah standing on one foot. **Shammai** pushed him away with a builder's measuring stick. **Hillel** taught him: \"That which is hateful to you do not do to another\"; the rest is commentary, now go and learn it.", R("Shabbat 31a")),
  text("Leviticus 19:18"),
  term(S("Leviticus 19:18", 4, 7), "\"Love your fellow [Israelite] as yourself\" (19:18). Hillel's rule says the same thing from the other side.", TN("Leviticus 19:18")),
  chk("q3", "hillel", "why", "How did Hillel answer the man who wanted the Torah on one foot?", ["What is hateful to you, do not do to another; go and learn the rest", "He sent him away", "He told him to memorize the Ten Commandments"],
      "A summary **and** an invitation to study.", ["That was Shammai.", "Not in the Talmud."], "On one foot"),
  rel("The houses of Hillel and Shammai argue all through the Mishnah, even about how to light Hanukkah candles.", ["lesson:x-st-hnk-03"]),
  refl("Herod built beauty and spilled blood; Hillel built a way of life with a sentence. Which kind of building lasts longer, and why?"),
  recap("**37 BCE**: Herod, Rome's king.", "Bava Batra 3b: \"**a slave in the house of the Hasmoneans**.\"", "The **beautiful building**; the Western Wall.", "Hillel: \"**That which is hateful to you do not do to another**.\"")]}

H10 = {"id": "x-hi-10", "title": "The Temple falls", "status": "draft", "related": ["prayer:m_rtzeh"],
 "check_note": "Gittin 55b-56b and Avot D'Rabbi Natan 4:5 read on Sefaria 11/14. Gittin 56a's line on Rabbi Zekharya's humility, the coffin escape, dates, Masada, Arch of Titus and the Reform R'tzeh change are from memory: check.",
 "cards": [
  hook("A feast and an insult", "The Talmud tells the fall of Jerusalem as a story about one party. A host sends for his friend **Kamtza**; the servant brings his enemy **Bar Kamtza** instead. The host throws him out, in front of the sages, who say nothing.", R("Gittin 55b-56a")),
  pre("What did Rabban Yochanan ben Zakkai ask from the Roman general?", ["Yavne and its sages", "Jerusalem's walls", "Gold for the Temple", "Safe passage to Babylon"],
      "\"Give me Yavne and its Sages\" (Gittin 56b)."),
  tl("66 CE", "Judea **revolts** against Rome.", SCH("Josephus, The Jewish War")),
  tl("70 CE", "Rome burns Jerusalem and the **Second Temple**: by tradition on the Ninth of Av.", SCH("Conventional date")),
  tl("73-74 CE", "**Masada**, the last fortress, falls.", SCH("Josephus; date debated")),
  concept("Silence at the feast", "\"Jerusalem was destroyed on account of Kamtza and bar Kamtza.\" Shamed, Bar Kamtza tells Rome the Jews are rebelling, and sends a calf with a hidden blemish as the emperor's offering. **Rabbi Zekharya ben Avkolas** blocks both sacrificing it and killing the informer. Rome comes. The Talmud blames Zekharya's **excess humility**.", R("Gittin 55b-56a")),
  chk("q1", "kamtza", "why", "In the Talmud's telling, what began the road to destruction?", ["Public humiliation, and sages who stayed silent", "A lost battle", "A failed harvest"],
      "Not armies first, but **how people treated one another**.", ["The Talmud starts at the feast.", "Not in the story."], "Silence at the feast"),
  concept("Give me Yavne", "Rabban **Yochanan ben Zakkai** had his students carry him out of the besieged city in a coffin. Before the Roman general he asked: \"Give me Yavne and its Sages,\" and doctors for a starving rabbi. Later voices asked why he did not ask to save **Jerusalem**. His answer became a new Judaism: of study, prayer and law.", R("Gittin 56a-b", "Coffin: from memory; check.")),
  chk("q2", "yavne", "pick", "What did Yochanan ben Zakkai save?", ["Yavne and its sages", "The Temple vessels", "Jerusalem"],
      "A **school**, not a city.", ["Rome took the vessels.", "The Talmud asks why he did not ask for it."], "Give me Yavne"),
  concept("Another atonement", "Leaving Jerusalem, Rabbi Yehoshua saw the ruins and cried: woe to us, the place where Israel's sins were atoned! Rabban Yochanan: do not grieve; we have another atonement as strong: \"the practice of lovingkindness.\"", R("Avot D'Rabbi Natan 4:5")),
  text("Hosea 6:6"),
  term(S("Hosea 6:6", 0, 4), "\"For I desire goodness, not sacrifice\" (6:6), Yochanan ben Zakkai's proof.", TN("Hosea 6:6")),
  concept("What Rome left", "In Rome, the **Arch of Titus** still shows soldiers carrying the Temple's **menorah**. Rome struck coins: **Judaea Capta**, Judea captured. The historian Josephus, a Jewish general who went over to Rome, saw it all.", SCH("Arch of Titus; Judaea Capta coins; Josephus")),
  rel("Prayer took the place of offerings. Reform siddurim also drop the plea to restore the sacrifices; check how R'tzeh reads in Mishkan T'filah.", ["prayer:m_rtzeh"]),
  refl("Yochanan ben Zakkai saved a school instead of a city. What would you carry out of a burning house, if not the house?"),
  recap("Gittin 55b: \"**Jerusalem was destroyed on account of Kamtza and bar Kamtza**.\"", "**70 CE**: the Second Temple falls.", "\"**Give me Yavne and its Sages**.\"", "Kindness as atonement: \"**I desire goodness, not sacrifice**.\"")]}

H11 = {"id": "x-hi-11", "title": "Bar Kokhba", "status": "draft", "related": ["prayer:shma"],
 "check_note": "Jerusalem Talmud Taanit 4:5 (Guggenheimer) and Berakhot 61b read on Sefaria 11/14. Dates, Aelia Capitolina, the Cave of Letters, and Akiva's last word 'echad' (61b, later in the passage) are from memory: check.",
 "cards": [
  hook("A star from Jacob", "In **132 CE**, sixty years after the Temple fell, Judea rises against Rome again. Its leader is **Shimon bar Kosiba**, and the greatest sage of the age believes in him.", SCH("Revolt under Hadrian")),
  pre("What did Rabbi Akiva call Bar Kokhba?", ["The King Messiah", "A false prophet", "A Roman spy", "The high priest"],
      "\"This is King Messias\" (Jerusalem Talmud Taanit 4:5)."),
  tl("132-135 CE", "The **Bar Kokhba revolt**: for three years, a free Judea.", SCH("Conventional dates")),
  tl("135 CE", "**Betar** falls. Jerusalem becomes a Roman city, **Aelia Capitolina**, closed to Jews.", SCH("Conventional date")),
  text("Numbers 24:17"),
  term(S("Numbers 24:17", 6, 9), "\"A star rises from Jacob\" (24:17). Kokhav, star, becomes his nickname: **Bar Kokhba**, son of a star.", TN("Numbers 24:17")),
  concept("Star or liar?", "Rabbi Shimon bar Yochai: Akiva taught that \"a star out of Jacob\" meant **Koziba**, and seeing him said, this is the King Messiah. **Rabbi Yochanan ben Torta** answered: \"Grass will grow from your jaws,\" and David's son still will not have come. Later the rabbis called him **Bar Koziba**, son of a lie.", R("Jerusalem Talmud Taanit 4:5")),
  chk("q1", "messiah", "pick", "How did Rabbi Yochanan ben Torta answer Akiva?", ["You will be long dead before the Messiah comes", "You are right; he is the Messiah", "Let us wait and see"],
      "Even the rabbis **disagreed** about him.", ["That was Akiva's view.", "Not his answer."], "Star or liar?"),
  concept("His own letters", "In **1960-61**, in caves near the Dead Sea, archaeologists found letters signed by **Shimon bar Kosiba** himself, giving orders to his commanders. One asks that the **four species** be brought for Sukkot.", SCH("Cave of Letters, Nahal Hever (Yadin)")),
  chk("q2", "letters", "pick", "What did the Cave of Letters reveal?", ["Letters from Bar Kokhba himself, under his real name", "His tomb", "A Roman account of his victory"],
      "His real name: **Bar Kosiba**.", ["No tomb has been found.", "The letters are his own."], "His own letters"),
  concept("With all your soul", "After the revolt, Rome banned teaching Torah. Akiva taught anyway, and was executed. As they tore his flesh, he recited the Sh'ma. His students asked: even now? He said: \"All my days I have been troubled by the verse: With all your soul.\" Now he could fulfill it. He died on the word **echad**, one.", R("Berakhot 61b")),
  chk("q3", "akiva", "why", "Why did Akiva say the Sh'ma as he died?", ["He could finally love God \"with all your soul\"", "It was the hour for evening prayer only", "Rome required it"],
      "His death became a teaching about **the Sh'ma**.", ["It was time for the Sh'ma, but that is not his reason.", "Not in the story."], "With all your soul"),
  rel("Each time you say the Sh'ma, \"with all your soul\" carries Akiva's story. On Tisha B'Av, Jews mourn Betar too.", ["prayer:shma", "lesson:x-kb-06"]),
  refl("Akiva backed a leader who failed, and is still the rabbis' hero. What do you make of a great person's great mistake?"),
  recap("**132-135 CE**: Bar Kokhba's revolt; Betar falls.", "Akiva: \"**A star rises from Jacob**\"; ben Torta: \"**Grass will grow from your jaws**.\"", "The **Cave of Letters**: Shimon bar Kosiba.", "Berakhot 61b: Akiva and the Sh'ma, **with all your soul**.")]}

LS = (H7, H8, H9, H10, H11)
for L in LS:
    cs = L["cards"]
    for c in cs:
        if c["kind"] == "check" and "look_again" in c:
            k = c["look_again"]
            c["look_again"] = next(i for i, x in enumerate(cs) if x.get("title") == k or x.get("sefaria") == k)
            c["src"] = cs[c["look_again"]]["src"]
        elif c["kind"] == "check": c["src"] = cs[0]["src"]
out = {"track": "history", "units": [{"id": "x-hi-rome", "title": "Greeks and Romans", "subtitle": "From Alexander to Bar Kokhba", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-history_rome.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
