"""Write data/src/x-stories_david.json: the David unit (x-st-david), 4 lessons (1-2 Samuel, Psalms). Hebrew sliced by word index from sefaria-david.json."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-david.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ").replace("&thinsp;", " ")
TN = lambda ref: {"type": "tanakh", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
def text(ref): return {"kind": "text", "sefaria": ref, "src": TN(ref)}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}

V1 = {"id": "x-st-dav-01", "title": "David (1): The youngest son", "status": "draft", "related": [],
 "check_note": "Shemot Rabbah 2:2 (Sefaria Midrash Rabbah 2022) and Megillah 14a read on Sefaria. English: JPS Tanakh Gender-Sensitive.",
 "cards": [
  {"kind": "hook", "title": "Not the tall one", "body": "God sends **Samuel** to the house of **Jesse** in Bethlehem to anoint a new king. Samuel sees the eldest son and is sure: this must be the one.", "src": TN("I Samuel 16:1-6")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "In the Midrash, how did God test David before making him king?", "choices": ["By how he shepherded his sheep", "By a battle", "By a riddle", "By a long fast"], "answer": 0,
   "why": "He fed each animal **according to its ability**."},
  text("I Samuel 16:7"),
  term(S("I Samuel 16:7", 18, 21), "\"GOD sees into the heart\" (16:7).", TN("I Samuel 16:7")),
  text("I Samuel 16:11-13"),
  term(S("I Samuel 16:11-13", 6, 9), "\"There is still the youngest\" (16:11). He is out **tending the flock**.", TN("I Samuel 16:11")),
  concept("A shepherd for each", "God tested David **with sheep**. He let the small ones out first to graze the **soft grass**, then the old ones on the middling grass, then the strong ones on the tough grass. God said: \"One who knows how to herd the flocks, each according to its ability, will come and herd My people.\"", R("Shemot Rabbah 2:2")),
  chk("q1", "shepherd", "why", "In Shemot Rabbah 2:2, what made David fit to lead Israel?", ["He cared for each sheep according to its needs", "He was the strongest brother", "He could play the harp"],
      "Leadership as **care for each one** by what they can bear.", ["The eldest looked strongest, and was passed over.", "Not the Midrash's reason."], look_again=6),
  term(S("I Samuel 16:11-13", 37, 39), "\"the horn of oil\" (16:13). The Talmud notes that kings anointed from **a horn**, like David, kept their kingship, as Hannah's song foresaw.", R("I Samuel 16:13; Megillah 14a")),
  {"kind": "reflect", "prompt": "Samuel looked at height; God looked at the heart. What do people miss when they look at you, and what might you be missing in others?"},
  {"kind": "recap", "points": ["\"**GOD sees into the heart**\" (16:7).", "**The youngest**, out with the flock (16:11).", "Shemot Rabbah 2:2: tested by shepherding **each according to its ability**.", "Anointed from **a horn** (16:13)."]}]}

V2 = {"id": "x-st-dav-02", "title": "David (2): David and Goliath", "status": "draft", "related": ["prayer:shma"],
 "check_note": "Sotah 42b read on Sefaria 11/13 (its sexual readings of Goliath's mother omitted).",
 "cards": [
  {"kind": "hook", "title": "Forty days", "body": "The Philistine champion **Goliath** comes out every morning and evening, for forty days, and dares Israel to send a man to fight him.", "src": TN("I Samuel 17:1-16")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "In the Talmud, Goliath came out morning and evening to stop Israel from saying the Sh'ma.", "answer": True,
   "why": "Rabbi Yochanan, in Sotah 42b."},
  concept("Morning and evening", "**Rabbi Yochanan**: Goliath came out **morning and evening** to keep Israel from reciting the Sh'ma at its proper times. And his **forty days** match the forty days the Torah was given: he wanted to do away with it.", R("Sotah 42b")),
  chk("q1", "shma", "why", "According to Rabbi Yochanan, why did Goliath taunt Israel morning and evening?", ["To stop them from saying the Sh'ma on time", "Because the sun was in his eyes at noon", "To change guards"],
      "The battle was also over **the Sh'ma**.", ["Not in the Talmud.", "Not in the Talmud."], look_again=2),
  {"kind": "relevance", "body": "The **Sh'ma**, said morning and evening, is what the Talmud says Goliath tried to stop.", "links": ["prayer:shma"]},
  text("I Samuel 17:45"),
  term(S("I Samuel 17:45", 9, 14), "\"but I come against you in the name of GOD of Hosts\" (17:45).", TN("I Samuel 17:45")),
  concept("The one who kissed, the one who cleaved", "The Talmud identifies Goliath's mother with **Orpah**, Naomi's other daughter-in-law. **Rabbi Yitzchak**: God said, the children of the one who **kissed** Naomi goodbye will fall into the hands of the children of the one who **cleaved** to her. David descends from **Ruth**. **Rava**: for the four tears Orpah shed for her mother-in-law, she merited four mighty sons.", R("Sotah 42b")),
  chk("q2", "orpah", "why", "In Sotah 42b, how are David and Goliath connected?", ["David descends from Ruth, Goliath from Orpah", "They were cousins in Bethlehem", "Goliath was David's teacher"],
      "Ruth **cleaved**; Orpah **kissed** and left (Ruth 1:14).", ["Not in the Talmud.", "Not in the Talmud."], look_again=7),
  concept("His own words", "**Rabbi Meir**: three times Goliath's own mouth foretold his fall. He said \"let him come down to me,\" placing himself below; he spoke of losing before he spoke of winning; and he asked, \"Am I a dog, that you come to me with staves?\"", R("Sotah 42b")),
  {"kind": "reflect", "prompt": "David faced Goliath with a sling and a Name. What giant are you facing with what you already have?"},
  {"kind": "recap", "points": ["Sotah 42b: Goliath came morning and evening to stop **the Sh'ma**.", "\"**I come against you in the name of GOD**\" (17:45).", "Orpah **kissed**, Ruth **cleaved**: Goliath and David.", "Goliath's **own words** foretold his fall."]}]}

V3 = {"id": "x-st-dav-03", "title": "David (3): That man is you", "status": "draft", "related": ["prayer:avot"],
 "check_note": "Avodah Zarah 4b-5a and Shabbat 56a read on Sefaria 11/13.",
 "cards": [
  {"kind": "hook", "title": "A king who takes", "body": "David takes **Bathsheba**, wife of Uriah, and arranges for Uriah to die in battle. Then God sends the prophet **Nathan**.", "src": TN("II Samuel 11-12")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "According to the Talmud, what can any individual who has sinned learn from David?", "choices": ["That one can repent", "That kings are above the law", "That some sins stay hidden", "That prophets are always believed"], "answer": 0,
   "why": "Avodah Zarah 5a: go to David, and learn **that one can repent**."},
  concept("The poor man's lamb", "Nathan tells the king a story: a rich man with many flocks took a poor man's **only lamb**, which he had raised like a daughter, to feed a guest. David is furious: the rich man deserves to die.", TN("II Samuel 12:1-6")),
  text("II Samuel 12:7"),
  term(S("II Samuel 12:7", 3, 5), "\"That man is you!\" (12:7).", TN("II Samuel 12:7")),
  text("II Samuel 12:13"),
  term(S("II Samuel 12:13", 3, 5), "\"I stand guilty before GOD!\" (12:13). In Hebrew, **two words**.", TN("II Samuel 12:13")),
  concept("The teacher of repentance", "**Rabbi Yochanan** in the name of **Rabbi Shimon bar Yochai**: David was not the kind of person to do this, nor was Israel the kind of people to make the golden calf. It happened so that if **an individual** sins, he is told: go to David, and **learn that one can repent**; and if **a community** sins, go to the people of the calf. David's \"last words\" (II Samuel 23:1) are read as: David, who **raised up the yoke of repentance**.", R("Avodah Zarah 4b-5a")),
  chk("q1", "teshuvah", "why", "In Avodah Zarah 5a, why is David's story held up to an individual who sinned?", ["To show that one can repent", "To show that kings can do as they like", "To warn against marriage"],
      "David as **the teacher of teshuvah**.", ["Nathan's rebuke says the opposite.", "Not the Talmud's lesson."], look_again=7),
  concept("Did David sin?", "Not every rabbi agreed. **Rabbi Shmuel bar Nachmani** in **Rabbi Yonatan's** name: \"Anyone who says that David sinned with Bathsheba is nothing other than mistaken,\" reading that soldiers gave their wives a conditional divorce before battle. But **Rav** says David's one sin was **the matter of Uriah** (1 Kings 15:5), and Nathan's words in the text are plain.", R("Shabbat 56a")),
  text("Psalms 51:1-2"),
  text("Psalms 51:12"),
  {"kind": "relevance", "body": "Every Amidah opens with a verse from this psalm: אֲדֹנָי שְׂפָתַי תִּפְתָּח (Psalm 51:17).", "links": ["prayer:avot"]},
  chk("q2", "psalm51", "pick", "Which psalm's heading places it after Nathan confronted David?", ["Psalm 51", "Psalm 23", "Psalm 92"],
      "Psalm 51, whose 17th verse **opens the Amidah**.", ["Not by its heading.", "Psalm 92 is for Shabbat."], look_again=10),
  {"kind": "reflect", "prompt": "David's confession is two words. What makes them so hard to say?"},
  {"kind": "recap", "points": ["Nathan's parable: \"**That man is you!**\" (12:7).", "\"**I stand guilty before GOD**\": two words (12:13).", "Avodah Zarah 5a: David teaches **that one can repent**.", "Shabbat 56a: some rabbis defend him; Rav does not.", "Psalm 51: \"**Fashion a pure heart for me**\", and the Amidah's first words."]}]}

V4 = {"id": "x-st-dav-04", "title": "David (4): The sweet singer", "status": "draft", "related": [],
 "check_note": "Berakhot 3b and 10a read on Sefaria 11/13.",
 "cards": [
  {"kind": "hook", "title": "Songs of a king", "body": "David is a shepherd, a soldier, a king, and above all remembered as **a singer**.", "src": TN("II Samuel 23:1")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "In the Talmud, a lyre over David's bed played by itself at midnight.", "answer": True,
   "why": "The north wind came at midnight and played it (Berakhot 3b)."},
  text("II Samuel 23:1"),
  term(S("II Samuel 23:1", 14, 17), "\"The favorite of the songs of Israel\" (23:1).", TN("II Samuel 23:1")),
  text("Psalms 119:62"),
  concept("The lyre at midnight", "A **lyre** hung over David's bed. At midnight the **north wind** blew and it played by itself, and David rose and **studied Torah until dawn**. At dawn the Sages came: the people need food. David answered, \"Go and sustain one another.\"", R("Berakhot 3b")),
  chk("q1", "lyre", "pick", "In Berakhot 3b, how did David know it was midnight?", ["The north wind played the lyre over his bed", "A servant woke him", "The stars told him"],
      "The wind **played the lyre**, and David rose.", ["Not in the Talmud.", "Not in the Talmud."], look_again=5),
  text("Psalms 103:1"),
  concept("Five times, O my soul", "David says \"Bless the Lord, O my soul\" **five times**. One answer: once for each world he lived in, from his mother's womb to his last day. Another: the soul is like God in five ways. As God **fills the world**, the soul fills the body; God **sees and is not seen**, and so does the soul; God sustains the world, the soul the body; God is **pure**, the soul is pure; God dwells in **an innermost chamber**, and so does the soul. So let the soul praise God.", R("Berakhot 10a")),
  chk("q2", "soul", "why", "In Berakhot 10a, why should the soul be the one to praise God?", ["It shares five qualities with God", "It is the oldest part of us", "The body cannot speak"],
      "Like praising like: **the soul** to **its source**.", ["Not the Talmud's reason.", "Not the Talmud's reason."], look_again=8),
  {"kind": "reflect", "prompt": "The Talmud says David sang a song for each stage of his life. What would your soul bless God for at this stage of yours?"},
  {"kind": "recap", "points": ["\"**The favorite of the songs of Israel**\" (23:1).", "Berakhot 3b: **the lyre at midnight**; \"sustain one another.\"", "\"**Bless GOD, O my soul**\" (Psalm 103:1).", "Berakhot 10a: the soul is like God **in five ways**."]}]}

LS = (V1, V2, V3, V4)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "stories", "units": [{"id": "x-st-david", "title": "David", "subtitle": "Shepherd, warrior, sinner, singer", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-stories_david.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
