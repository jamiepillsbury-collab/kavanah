"""Write data/src/x-stories_deborah.json: the Deborah unit (x-st-deborah), 4 lessons (Judges 4-5). Hebrew sliced by word index from sefaria-deborah.json. Judges 5:7's English on Sefaria carries a footnote remnant, so 5:7 is used only as a term card."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-deborah.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ").replace("&thinsp;", " ")
TN = lambda ref: {"type": "tanakh", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
def text(ref): return {"kind": "text", "sefaria": ref, "src": TN(ref)}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}

D1 = {"id": "x-st-deb-01", "title": "Deborah (1): Under the palm tree", "status": "draft", "related": [],
 "check_note": "Megillah 14a-b, Esther Rabbah 5:4 and Zohar Vayikra 47:328 (Soncino) read on Sefaria 11/12. English: JPS Tanakh Gender-Sensitive.",
 "cards": [
  {"kind": "hook", "title": "A prophet who leads", "body": "Israel is oppressed by a Canaanite king. Its leader at that time is a woman: **Deborah**, prophet and judge.", "src": TN("Judges 4:1-5")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "According to the Talmud, why is Deborah called \"wife of Lappidoth\"?", "choices": ["She made wicks for the Sanctuary", "Her husband was a general", "She lived by a lighthouse", "She wove the Temple curtains"], "answer": 0,
   "why": "לַפִּידוֹת means **flames**: \"a woman of flames.\""},
  text("Judges 4:4-5"),
  term(S("Judges 4:4-5", 0, 5), "\"Deborah, wife of Lappidoth, was a prophet\" (4:4).", TN("Judges 4:4")),
  concept("A woman of flames", "The Talmud counts **seven prophetesses**: Sarah, Miriam, **Deborah**, Hannah, Abigail, Huldah and Esther. Why \"wife of Lappidoth\"? Because she made **wicks for the Sanctuary**, and from the flames, לַפִּידוֹת, she was called a woman of flames.", R("Megillah 14a")),
  chk("q1", "lappidot", "why", "Why does the Talmud call Deborah \"a woman of flames\"?", ["She made the Sanctuary's wicks", "She fought with torches", "She had red hair"],
      "Before she lit up Israel as a judge, she made **light for the Sanctuary**.", ["Not in the Talmud.", "Not in the Talmud."], look_again=4),
  term(S("Judges 4:4-5", 10, 13), "\"She used to sit under the Palm of Deborah\" (4:5).", TN("Judges 4:5")),
  concept("Why under a palm tree?", "**Rabbi Shimon ben Avshalom**: she judged **out in the open**, visible to all, so she would never be alone behind closed doors with the men who came to her. Or: a palm tree has **one heart**, a single trunk, and so did Israel in her generation, one heart turned to their Father in Heaven.", R("Megillah 14a")),
  chk("q2", "palm", "why", "In Megillah 14a, what is one reason Deborah judged under a palm tree?", ["To judge in the open, visible to everyone", "For the shade only", "Because it was sacred to Baal"],
      "Justice **in plain sight**.", ["The Talmud gives a deeper reason.", "Not in the Talmud."], look_again=7),
  concept("How the rabbis saw her", "The Bible simply names Deborah prophet and judge. Later readers argued. **Esther Rabbah**: when Israel was crushed, who was fitting for the moment? **Deborah**. **Rav Nachman** calls her haughty, because she sent for Barak instead of going to him. The **Zohar** goes further: \"Woe to the generation which could only find a female to be its judge!\"", R("Esther Rabbah 5:4; Megillah 14b; Zohar, Vayikra 47:328")),
  chk("q3", "views", "pick", "Which source says Deborah was the one \"fitting\" for her moment?", ["Esther Rabbah 5:4", "Megillah 14b", "The Zohar"],
      "Rabbinic voices **disagree** about her; Esther Rabbah praises her.", ["Rav Nachman calls her haughty.", "The Zohar laments a woman judge."], look_again=9),
  {"kind": "reflect", "prompt": "The Bible calls Deborah a prophet and leader; later readers argued about her. When have you seen someone's leadership doubted for who they were rather than what they did?"},
  {"kind": "recap", "points": ["Deborah: **prophet and judge** (4:4).", "Megillah 14a: **a woman of flames**, wicks for the Sanctuary.", "Judging **under the palm**, in the open; one heart.", "Rabbinic views **differ**: fitting, haughty, or a sign of a weak generation."]}]}

D2 = {"id": "x-st-deb-02", "title": "Deborah (2): Barak and Jael", "status": "draft", "related": [],
 "check_note": "Nazir 23b read on Sefaria 11/12 (its sexual reading of 5:27 left out).",
 "cards": [
  {"kind": "hook", "title": "Not without you", "body": "Deborah tells **Barak** to lead ten thousand men against **Sisera**, the Canaanite general. Barak has one condition.", "src": TN("Judges 4:6-8")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "Barak would not go to battle unless Deborah came with him.", "answer": True,
   "why": "\"If you will go with me, I will go; if not, I will not go\" (4:8)."},
  text("Judges 4:8-9"),
  term(S("Judges 4:8-9", 24, 29), "\"GOD will deliver Sisera into the hands of a woman\" (4:9). Which woman? Not Deborah, as it turns out.", TN("Judges 4:9")),
  chk("q1", "hand", "pick", "Into whose hands does Deborah say Sisera will fall?", ["A woman's", "Barak's", "The king's"],
      "**A woman's** hand, and the story will name her.", ["Barak gets no glory here (4:9).", "Not in the text."], look_again=3),
  concept("Jael", "Sisera's army is routed and he flees on foot to the tent of **Jael**, wife of Heber the Kenite. She invites him in, gives him milk, and covers him. When he sleeps, she takes a tent pin and a mallet.", TN("Judges 4:17-22")),
  text("Judges 4:21"),
  text("Judges 5:24"),
  concept("For the sake of Heaven", "**Rav Nachman bar Yitzchak**: a transgression done **for the sake of Heaven** is equal to a mitzvah done not for its own sake. His proof is Jael: \"Most blessed of women in tents.\" Who are the women in the tent? **Sarah, Rebecca, Rachel and Leah**. Jael, who did what she had to do to stop Sisera, is ranked with the matriarchs.", R("Nazir 23b")),
  chk("q2", "jael", "why", "In Nazir 23b, who are the \"women in tents\" Jael is blessed above?", ["Sarah, Rebecca, Rachel and Leah", "Deborah and Miriam", "The women of Sisera's household"],
      "Jael is ranked with **the matriarchs**.", ["Not the Talmud's list.", "Not the Talmud's list."], look_again=8),
  {"kind": "reflect", "prompt": "Barak would not go alone, and the victory went to two women. Who do you need beside you to do something hard?"},
  {"kind": "recap", "points": ["Barak: \"**If you will go with me, I will go**\" (4:8).", "Sisera falls **into the hands of a woman** (4:9).", "**Jael** and the tent pin (4:21).", "Nazir 23b: blessed with **the matriarchs**."]}]}

D3 = {"id": "x-st-deb-03", "title": "Deborah (3): Awake, sing", "status": "draft", "related": ["prayer:lcha_dodi_2"],
 "check_note": "Pesachim 66b read on Sefaria 11/12. L'cha Dodi line from data/prayers.json.",
 "cards": [
  {"kind": "hook", "title": "A victory song", "body": "After the battle, **Deborah and Barak sing**.", "src": TN("Judges 5:1")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "According to Pesachim 66b, why did Deborah's prophecy leave her for a time?", "choices": ["She praised herself", "She went to war", "She doubted God", "Barak insulted her"], "answer": 0,
   "why": "Rav: **haughtiness** drives away prophecy."},
  text("Judges 5:1-3"),
  term(S("Judges 5:1-3", 18, 24), "\"I will sing, will sing to GOD\" (5:3).", TN("Judges 5:3")),
  term(S("Judges 5:7", 4, 10), "\"Arose, O mother, in Israel!\" (5:7). The JPS reads the verb as said **to** Deborah. The Talmud reads it as Deborah speaking of herself: **until I arose**.", R("Judges 5:7; Pesachim 66b")),
  concept("A mother in Israel", "**Rav Yehuda** in the name of **Rav**: whoever acts haughtily, if a sage, loses wisdom; if a prophet, **loses prophecy**. From Deborah: \"until I, Deborah, arose, I arose a mother in Israel.\" For praising herself, her prophecy left her, so later she had to be told, \"Awake, awake, Deborah.\"", R("Pesachim 66b")),
  chk("q1", "haughty", "why", "How does Pesachim 66b explain \"Awake, awake, Deborah\"?", ["Her prophecy had left her after she praised herself", "She had fallen asleep after the battle", "Barak was calling her"],
      "Pride **dimmed** her prophecy; the song **wakes** it.", ["Not the Talmud's reading.", "Not the Talmud's reading."], look_again=5),
  text("Judges 5:12"),
  term(S("Judges 5:12", 0, 6), "\"Awake, awake, O Deborah! Awake, awake, strike up the chant!\" (5:12).", TN("Judges 5:12")),
  {"kind": "relevance", "body": "Every Friday night, **L'cha Dodi** borrows Deborah's words: עוּרִי עוּרִי שִׁיר דַּבֵּרִי.", "links": ["prayer:lcha_dodi_2"]},
  {"kind": "reflect", "prompt": "Deborah calls herself \"a mother in Israel,\" and the Talmud warns against self-praise. How do you tell healthy pride from too much?"},
  {"kind": "recap", "points": ["Deborah and Barak **sing** (5:1-3).", "\"Arose, O mother, in Israel\": **you** arose, or **I** arose?", "Pesachim 66b: self-praise, and **prophecy leaves**.", "\"**Awake, awake**\": in L'cha Dodi every Shabbat."]}]}

D4 = {"id": "x-st-deb-04", "title": "Deborah (4): Sisera's mother", "status": "draft", "related": [],
 "check_note": "Rosh Hashanah 33b and Megillah 10b read on Sefaria (33b on 11/12).",
 "cards": [
  {"kind": "hook", "title": "At the window", "body": "Deborah's song does not end with the victors. It ends in the enemy's house, with **Sisera's mother**, waiting at the window.", "src": TN("Judges 5:28-30")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "The Talmud learns the sound of the shofar's teruah from the crying of Sisera's mother.", "answer": True,
   "why": "Rosh Hashanah 33b defines the sound by her **wailing**."},
  text("Judges 5:28"),
  term(S("Judges 5:28", 0, 6), "\"Through the window peered Sisera’s mother\" (5:28). Her crying is וַתְּיַבֵּב.", TN("Judges 5:28")),
  concept("The sound of the shofar", "The Torah calls Rosh Hashanah **a day of teruah**, and the Aramaic translation calls it a day of **yevava**. What is yevava? The Talmud answers from this verse: Sisera's mother **wailed**, וַתְּיַבֵּב. One view hears **moaning sighs** (shevarim), another **whimpers** (teruot). The shofar's sounds are measured by **an enemy mother's cry**.", R("Rosh Hashanah 33b")),
  chk("q1", "shofar", "why", "In Rosh Hashanah 33b, how does the Talmud define the shofar's sound?", ["By the crying of Sisera's mother", "By Deborah's song", "By the trumpets of Barak's army"],
      "The shofar sounds like **a mother's crying**.", ["Not the Talmud's source.", "Not the Talmud's source."], look_again=4),
  concept("Not rejoicing", "Compare the Sea: when the Egyptians drowned, God stopped the angels from singing, because they too were **the work of My hands**.", R("Megillah 10b")),
  text("Judges 5:31"),
  term(S("Judges 5:31", 8, 12), "\"And the land was tranquil forty years\" (5:31).", TN("Judges 5:31")),
  chk("q2", "forty", "pick", "How does the story of Deborah end?", ["The land was tranquil forty years", "Deborah becomes queen", "Sisera escapes"],
      "**Forty years** of quiet (5:31).", ["Not in the text.", "Jael ends Sisera's flight (4:21)."], look_again=8),
  {"kind": "reflect", "prompt": "The song ends with a mother waiting for a son who will not come home, and the shofar still carries her cry. Can you hold victory and grief at the same time?"},
  {"kind": "recap", "points": ["The song ends with **Sisera's mother** at the window (5:28).", "Rosh Hashanah 33b: the shofar's sound is **her cry**.", "Megillah 10b: God does not rejoice when enemies drown.", "**Forty years** of quiet (5:31)."]}]}

LS = (D1, D2, D3, D4)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "stories", "units": [{"id": "x-st-deborah", "title": "Deborah", "subtitle": "A prophet, a general, a tent pin, and a song", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-stories_deborah.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
