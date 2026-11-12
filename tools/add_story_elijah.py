"""Write data/src/x-stories_elijah.json: the Elijah unit (x-st-elijah), 4 lessons (1 Kings 17-19, 2 Kings 2, Malachi 3). Hebrew sliced by word index from sefaria-elijah.json."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-elijah.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ").replace("&thinsp;", " ")
TN = lambda ref: {"type": "tanakh", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
def text(ref): return {"kind": "text", "sefaria": ref, "src": TN(ref)}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
PRE = "Pirkei DeRabbi Eliezer 29"

E1 = {"id": "x-st-eli-01", "title": "Elijah (1): The key to the rain", "status": "draft", "related": [],
 "check_note": "Sanhedrin 113a and Chullin 5a read on Sefaria 11/12. English: JPS Tanakh Gender-Sensitive.",
 "cards": [
  {"kind": "hook", "title": "No dew, no rain", "body": "**Elijah** appears with no introduction and makes King **Ahab** an oath: no rain until Elijah says so.", "src": TN("I Kings 17:1")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "In the Talmud, which key did God take back from Elijah in exchange for another?", "choices": ["The key of rain, for the key of reviving the dead", "The key of the Temple, for the key of heaven", "The key of birth, for the key of rain", "None; Elijah kept every key"], "answer": 0,
   "why": "Three keys are not handed to an agent; Elijah could hold only one at a time."},
  text("I Kings 17:1"),
  term(S("I Kings 17:1", 12, 20), "\"there will be no dew or rain except at my bidding\" (17:1).", TN("I Kings 17:1")),
  concept("Why Elijah swore", "The Talmud sets the scene in a house of mourning. **Ahab** mocks Elijah: Moses warned that if Israel served other gods, the heavens would close and there would be no rain. Yet Ahab has set up an idol on every furrow, and the rain is so plentiful he can hardly get out to worship them. **Immediately** Elijah swears, prays, and is given **the key to the rain**.", R("Sanhedrin 113a")),
  text("I Kings 17:6"),
  concept("Ravens", "Where did the ravens get bread and meat? **Rav**: from **Ahab's own slaughterhouse**. Were they really ravens? **Ravina**: yes, actual ravens, not two men who happened to be named Oreb.", R("Chullin 5a; Sanhedrin 113a")),
  chk("q1", "ravens", "pick", "According to Rav, where did the ravens bring Elijah's meat from?", ["Ahab's slaughterhouse", "The Temple altar", "The widow's kitchen"],
      "The king who hunted Elijah **fed him**, without knowing it.", ["Not in the Talmud.", "He meets the widow later."], look_again=6),
  text("I Kings 17:14-16"),
  concept("Three keys", "The stream dries up. The Talmud says God saw the world suffering while Elijah **was not moved by it**, so God sent him to a widow in Zarephath. When her son fell ill, Elijah asked for **the key to reviving the dead**. Heaven answered: three keys are not given to an agent, birth, rain and resurrection. People will say the student holds two keys and the Master one. **Give back the rain**, and take this key. A Galilean compared Elijah to a man who **slammed his door and lost his key**.", R("Sanhedrin 113a")),
  chk("q2", "keys", "why", "Why, in Sanhedrin 113a, did Elijah have to give back the key to the rain?", ["To receive the key to reviving the widow's son", "Ahab stole it", "The drought had ended by itself"],
      "Compassion for one child **unlocks the rain** for everyone.", ["Not in the Talmud.", "Elijah had to give the key back for rain to fall."], look_again=9),
  text("I Kings 17:24"),
  {"kind": "reflect", "prompt": "In the Talmud, Elijah held the key to the rain but was slow to feel the people's suffering. When has being right made it harder for you to be kind?"},
  {"kind": "recap", "points": ["Elijah swears: **no dew or rain** (17:1).", "Sanhedrin 113a: provoked by **Ahab's mockery**, he is given **the key**.", "Rav: the ravens brought meat from **Ahab's** slaughterhouse.", "**Three keys**: rain is given back for the widow's son."]}]}

E2 = {"id": "x-st-eli-02", "title": "Elijah (2): Fire on Mount Carmel", "status": "draft", "related": [],
 "check_note": "Berakhot 6b and 9b read on Sefaria 11/12. Neilah card: CHECK wording in Mishkan HaNefesh and CBB practice.",
 "cards": [
  {"kind": "hook", "title": "A contest", "body": "Elijah gathers all the people, and the prophets of Baal, on **Mount Carmel**. Two altars, two bulls, and one question: who answers with fire?", "src": TN("I Kings 18:19-24")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Which daily prayer does the Talmud connect to Elijah's answer on Mount Carmel?", "choices": ["Minchah, the afternoon prayer", "Shacharit, the morning prayer", "Ma'ariv, the evening prayer", "Musaf"], "answer": 0,
   "why": "He was answered at the time of **the minchah offering** (18:36)."},
  text("I Kings 18:21"),
  term(S("I Kings 18:21", 4, 9), "\"How long will you keep hopping between two opinions?\" (18:21). The verb shares its letters with **פֶּסַח**, Passover.", TN("I Kings 18:21")),
  text("I Kings 18:36-37"),
  concept("Answered at Minchah", "**Rav Huna**: always be careful with **the afternoon prayer**, because Elijah was answered only at the afternoon prayer. The verse begins: when it was time to present the **minchah**, the grain offering.", R("Berakhot 6b")),
  chk("q1", "minchah", "why", "Why does Rav Huna say to be careful with the afternoon prayer?", ["Elijah was answered at the afternoon prayer", "It is the longest prayer", "Moses wrote it"],
      "At **Minchah**, fire came down.", ["It is the shortest of the three.", "Not in the Talmud."], look_again=5),
  term(S("I Kings 18:36-37", 25, 28), "\"Answer me, O ETERNAL One, answer me\" (18:37).", TN("I Kings 18:37")),
  concept("Answer me, twice", "**Rabbi Abbahu**: why say \"answer me\" twice? The first: answer me with **fire** from heaven. The second: answer me so the people **will not say it was sorcery**. Elijah adds, \"You have turned their hearts backward\": the God who turned their hearts can **turn them back**.", R("Berakhot 9b")),
  chk("q2", "twice", "why", "According to Rabbi Abbahu, what was Elijah's second \"answer me\" for?", ["That the people would not dismiss the fire as sorcery", "That it would rain", "That Ahab would die"],
      "A miracle is not enough; **hearts** have to turn too.", ["Rain comes later.", "Not in the Talmud."], look_again=8),
  text("I Kings 18:38-39"),
  term(S("I Kings 18:38-39", 15, 21), "\"the ETERNAL One alone is God, the ETERNAL One alone is God!\" (18:39).", TN("I Kings 18:39")),
  concept("At the close of Yom Kippur", "The people's cry from Carmel is called out again at the very end of **Yom Kippur**, as **Neilah** closes.", {"type": "tradition", "ref": "1 Kings 18:39 in the Neilah service", "note": "CHECK: Mishkan HaNefesh wording and CBB practice"}),
  {"kind": "reflect", "prompt": "Elijah asked the people how long they would keep hopping between two opinions. Where are you still hopping?"},
  {"kind": "recap", "points": ["\"**Hopping between two opinions**\" (18:21).", "Berakhot 6b: answered at **Minchah**.", "Berakhot 9b: answer me twice: **fire**, and **hearts**.", "\"**The ETERNAL One alone is God**\" (18:39), again at Neilah."]}]}

E3 = {"id": "x-st-eli-03", "title": "Elijah (3): A soft murmuring sound", "status": "draft", "related": [],
 "check_note": "Pirkei DeRabbi Eliezer 29 (Friedlander) read on Sefaria 11/12. Rabbi's-teaching card: the connection is mine; check with Jamie.",
 "cards": [
  {"kind": "hook", "title": "Enough", "body": "After Carmel, Queen **Jezebel** seeks Elijah's life. The prophet who called down fire runs into the wilderness, sits under a bush, and **asks to die**.", "src": R("I Kings 19:1-4; Pirkei DeRabbi Eliezer 29")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "According to the Midrash, Elijah attends every brit milah.", "answer": True,
   "why": "Pirkei d'Rabbi Eliezer 29: so the Sages set a **seat of honor** for him."},
  text("I Kings 19:4"),
  term(S("I Kings 19:4", 14, 22), "\"take my life, for I am no better than my predecessors\" (19:4).", TN("I Kings 19:4")),
  text("I Kings 19:11-12"),
  term(S("I Kings 19:11-12", 35, 38), "\"a soft murmuring sound\" (19:12). GOD was not in the wind, not in the earthquake, not in the fire.", TN("I Kings 19:11-12")),
  chk("q1", "voice", "pick", "After the wind, the earthquake and the fire, how does God come to Elijah?", ["In a soft murmuring sound", "In the fire", "In the earthquake"],
      "Not in the noise: in **a soft murmuring sound**.", ["God was not in the fire.", "God was not in the earthquake."], look_again=5),
  text("I Kings 19:13-14"),
  concept("Always zealous", "In **Pirkei d'Rabbi Eliezer**, Elijah's complaint is about the **covenant of circumcision**, which the northern kingdom had abandoned. God answers: \"Thou art always zealous.\" Then: by your life, Israel will not perform this covenant **until you see it with your own eyes**. So the Sages set **a seat of honor** at every brit for Elijah, called the Messenger of the Covenant (Malachi 3:1).", R(PRE)),
  chk("q2", "covenant", "why", "In Pirkei d'Rabbi Eliezer 29, why is Elijah present at every brit?", ["He said Israel had abandoned the covenant, so he must witness them keeping it", "He was the first mohel", "He asked to be invited"],
      "The accuser becomes **the witness** to Israel's faithfulness.", ["Not in the Midrash.", "Not in the Midrash."], look_again=8),
  concept("God in the quiet", "Your rabbi reads the Torah as a people **growing up**: from a child's hero-God who fixes everything, toward God present in quieter ways. Elijah lives both stages in two chapters. On Carmel, God answers with **fire**. At Horeb, God is not in the wind, the earthquake or the fire, but in **a soft murmuring sound**.", {"type": "reform", "ref": "Teaching from Jamie's rabbi (oral, as Jamie retold it); I Kings 18-19", "note": "connection to Elijah is mine; check with Jamie"}),
  {"kind": "reflect", "prompt": "God was not in the fire, but in a soft murmuring sound. Where do you hear that quiet voice?"},
  {"kind": "recap", "points": ["\"**Enough!**\" Elijah asks to die (19:4).", "Not in wind, earthquake or fire: **a soft murmuring sound** (19:12).", "Pirkei d'Rabbi Eliezer 29: \"**always zealous**\", so Elijah witnesses every brit.", "Your rabbi: from fire to **quiet**."]}]}

E4 = {"id": "x-st-eli-04", "title": "Elijah (4): The one who comes back", "status": "draft", "related": [],
 "check_note": "Bava Metzia 59b and Sanhedrin 98a read on Sefaria 11/12. Seder/Havdalah card: CHECK CBB and Mishkan T'filah practice.",
 "cards": [
  {"kind": "hook", "title": "A chariot of fire", "body": "Elijah does not die. Walking and talking with his student **Elisha**, he is taken up to heaven in a whirlwind.", "src": TN("II Kings 2:11")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "In the Talmud, how did God react when the Sages overruled a voice from heaven?", "choices": ["God smiled: \"My children have triumphed over Me\"", "God sent a flood", "God took back the Torah", "God was silent forever"], "answer": 0,
   "why": "Elijah reports it to Rabbi Natan in Bava Metzia 59b."},
  text("II Kings 2:11"),
  term(S("II Kings 2:11", 6, 9), "\"a fiery chariot with fiery horses\" (2:11).", TN("II Kings 2:11")),
  text("Malachi 3:23-24"),
  term(S("Malachi 3:23-24", 13, 19), "\"He shall reconcile parents with children and children with their parents\" (3:24). The prophets' last words promise that **Elijah comes back**.", TN("Malachi 3:24")),
  concept("My children have triumphed", "In a famous dispute, a heavenly voice sides with Rabbi Eliezer. **Rabbi Yehoshua** stands and says, \"It is not in heaven\": the Torah was given at Sinai, and now the majority decides. Years later, **Rabbi Natan** meets Elijah and asks what God did at that moment. Elijah: God **smiled** and said, \"My children have triumphed over Me.\"", R("Bava Metzia 59b")),
  chk("q1", "smiled", "why", "In Bava Metzia 59b, how does God respond to being overruled?", ["With a smile and pride in the children", "With anger", "By changing the law"],
      "Like a parent whose children have **grown up**.", ["Elijah says God smiled.", "The majority's ruling stands."], look_again=6),
  concept("Today, if you listen", "**Rabbi Yehoshua ben Levi** meets Elijah and asks when the Messiah will come. Go ask him, says Elijah: he sits at the gate of Rome **among the sick poor**, changing his bandages one at a time so he is always ready. The Messiah tells him, \"Today.\" When he does not come, Elijah explains: \"today, if you will listen to his voice\" (Psalms 95:7).", R("Sanhedrin 98a")),
  chk("q2", "today", "why", "In Sanhedrin 98a, what did the Messiah's \"today\" mean?", ["Today, if you will listen to his voice", "Exactly that day", "Never"],
      "The coming depends on **us listening**.", ["He did not come that day.", "Elijah reads it as a condition, not a refusal."], look_again=8),
  concept("A cup and a song", "Elijah is still expected: a cup is poured for him and the door opened at the **Passover seder**, and as Shabbat ends, **Havdalah** sings of אֵלִיָּהוּ הַנָּבִיא.", {"type": "tradition", "ref": "Passover seder; Havdalah", "note": "CHECK: CBB and Mishkan T'filah practice"}),
  {"kind": "reflect", "prompt": "Elijah returns to turn parents' hearts toward children and children's toward parents. Whose heart would you like turned toward yours, or yours toward theirs?"},
  {"kind": "recap", "points": ["A **fiery chariot**: Elijah does not die (2:11).", "Malachi: he will come back to **reconcile** parents and children.", "Bava Metzia 59b: God smiles, \"**My children have triumphed over Me**.\"", "Sanhedrin 98a: \"**today, if you will listen**.\"", "A cup at the seder, a song at Havdalah."]}]}

LS = (E1, E2, E3, E4)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "stories", "units": [{"id": "x-st-elijah", "title": "Elijah", "subtitle": "The prophet who did not die", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-stories_elijah.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
