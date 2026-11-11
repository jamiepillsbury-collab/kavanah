"""Write data/src/x-stories_ruth.json: the Ruth unit (x-st-ruth, 4 lessons). Hebrew sliced by word index from data/src/sefaria-ruth.json."""
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
RABBI = {"type": "reform", "ref": "Teaching from Jamie's rabbi (oral, as Jamie retold it); Richard Elliott Friedman, The Hidden Face of God (1995)", "note": "Friedman: check"}

R1 = {"id": "x-st-ruth-01", "title": "Ruth (1): Your people, my people", "status": "draft", "related": [],
 "check_note": "Yevamot 47b and Berakhot 7b read on Sefaria 11/11. English: JPS Tanakh gender-sensitive.",
 "cards": [
  {"kind": "hook", "title": "Three widows on the road", "body": "In Moab, **Naomi** has lost her husband and both sons. She hears that Adonai \"had taken note of the people\" back home, and sets out with her two Moabite daughters-in-law, **Orpah and Ruth** (1:1-6).", "src": TN("Ruth 1:1-6")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "What happens when Naomi tells Ruth to go back to her own people?", "choices": ["Ruth refuses and binds herself to Naomi", "Ruth goes back, like Orpah", "Ruth asks Boaz for advice", "Ruth stays silent"], "answer": 0,
   "why": "Orpah kisses her goodbye; **Ruth clings to her** and refuses to leave (1:14-17)."},
  text("Ruth 1:16-18"),
  term(S("Ruth 1:16-18", 13, 17), "\"your people shall be my people, and your God my God\" (1:16): four Hebrew words that change the history of Israel.", TN("Ruth 1:16")),
  concept("When Naomi stopped arguing", "\"When [Naomi] saw how determined she was to go with her, she ceased to argue with her\" (1:18). **Rabbi Elazar** learns from this how to receive someone who wants to become a Jew: you may test their resolve, but once it is clear, **you stop arguing**.", R("Yevamot 47b")),
  chk("q1", "convert", "why", "What does the Talmud learn from Naomi falling silent (1:18)?", ["Once a person's resolve to join is clear, you stop dissuading them", "Converts should never be questioned", "Naomi didn't want Ruth to come"],
      "Ruth becomes **the model** for choosing to join the Jewish people.", ["Naomi did test her first; the point is when to stop.", "The verse says Naomi saw her determination."], look_again=4),
  concept("What's in the name Ruth?", "**Rabbi Yochanan**: she was called Rut because from her came **David**, who **saturated** (riva) the Holy One with songs and praises.", R("Berakhot 7b")),
  text("Ruth 1:20-21"),
  term(S("Ruth 1:20-21", 5, 8), "\"Call me Mara\" (1:20), bitterness. Naomi says it plainly: \"I went away full, and Adonai has brought me back empty.\" The book lets her say it.", TN("Ruth 1:20-21")),
  chk("q2", "mara", "pick", "What name does Naomi ask to be called?", ["Mara, bitterness", "Ruth", "Orpah"],
      "**Mara**: \"for Shaddai has made my lot very bitter\" (1:20).", ["Ruth is her daughter-in-law.", "Orpah went back to Moab."], look_again=8),
  {"kind": "reflect", "prompt": "In the same scene, Ruth binds herself to a people and a God before anything has gone well, and Naomi names her bitterness out loud. Which voice do you recognize today?"},
  {"kind": "recap", "points": ["\"**Your people shall be my people, and your God my God.**\"", "Yevamot 47b: when resolve is clear, **stop arguing**.", "Berakhot 7b: Ruth, ancestor of David who **saturated God with song**.", "Naomi: \"**Call me Mara.**\""]}]}

R2 = {"id": "x-st-ruth-02", "title": "Ruth (2): Under whose wings", "status": "draft", "related": [],
 "check_note": "Mishnah Berakhot 9:5 read on Sefaria 11/11. The kanaf link between 2:12 and 3:9 is in the Hebrew text itself.",
 "cards": [
  {"kind": "hook", "title": "A field of strangers", "body": "Ruth goes out to **glean** behind the reapers, and happens to come to the field of **Boaz**, a relative of Naomi's husband (2:1-3).", "src": TN("Ruth 2:1-3")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "The Mishnah learns from Boaz to greet people with God's name.", "answer": True,
   "why": "**Mishnah Berakhot 9:5**, from Boaz's \"Adonai be with you!\" (2:4)."},
  text("Ruth 2:4"),
  concept("A blessing for hello", "Boaz greets his workers, \"Adonai be with you!\" and they answer, \"Adonai bless you!\" The **Mishnah**: from this the Sages instituted that people **greet one another using God's name**.", R("Mishnah Berakhot 9:5")),
  text("Ruth 2:12"),
  term(S("Ruth 2:12", 12, 13), "\"under whose wings you have sought refuge\" (2:12). Boaz prays that **God** will shelter Ruth, the stranger in his field.", TN("Ruth 2:12")),
  text("Ruth 3:9-10"),
  term(S("Ruth 3:9-10", 6, 9), "\"Spread your robe over your handmaid\" (3:9). In Hebrew, \"robe\" here is **kanaf**, the very word for God's **wings** in 2:12. Boaz prayed for God to shelter Ruth; now Ruth asks **Boaz** to be that shelter.", TN("Ruth 2:12, 3:9")),
  chk("q1", "kanaf", "why", "What links Boaz's blessing (2:12) to Ruth's request (3:9)?", ["The same Hebrew word, kanaf: wings, or the corner of a robe", "Both mention Naomi", "Both happen at the city gate"],
      "God's **wings** and Boaz's **robe** are one word. Boaz becomes **the answer to his own prayer**.", ["Naomi isn't named in either verse.", "2:12 is in the field and 3:9 at the threshing floor."], look_again=7),
  term(S("Ruth 3:9-10", 17, 21), "\"Your latest deed of loyalty is greater than the first\" (3:10). The Hebrew word for loyalty is **chesed**.", TN("Ruth 3:10")),
  {"kind": "reflect", "prompt": "Boaz becomes the answer to his own prayer. Is there a prayer of yours that you could help answer?"},
  {"kind": "recap", "points": ["Boaz's \"Adonai be with you\": greeting with God's name (Mishnah Berakhot 9:5).", "\"**Under whose wings** you have sought refuge.\"", "\"**Spread your robe**\": the same word, kanaf.", "Boaz becomes **the answer to his own prayer**.", "**Chesed**, loyalty, greater the second time."]}]}

R3 = {"id": "x-st-ruth-03", "title": "Ruth (3): Where is God in Ruth?", "status": "draft", "related": [],
 "check_note": "Count of the narrator's statements about God from the full JPS text of Ruth on Sefaria (1:6, 4:13). Ruth Rabbah 2:14 and Chullin 139b read on Sefaria 11/11. Esther 5:4 initials checked by script on the Masorah text.",
 "cards": [
  {"kind": "hook", "title": "God's name, God's hand", "body": "People in Ruth say God's name often: in blessings, in oaths, in Naomi's grief. But the **narrator** says God **did** something only **twice**: gave the people food (1:6) and let Ruth conceive (4:13). Everything else that saves anyone is **a human act**.", "src": TN("Ruth 1:6, 4:13")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "How many times does the narrator of Ruth say God acted?", "choices": ["Twice", "Never", "In every chapter", "Once"], "answer": 0,
   "why": "**Twice**: 1:6 and 4:13. The rest is human loyalty, generosity and courage."},
  text("Ruth 1:6"),
  text("Ruth 4:13"),
  concept("Written to teach chesed", "**Rabbi Ze'eira**: this scroll contains no laws of purity or impurity, nothing forbidden or permitted. Why was it written? **To teach how great the reward is for those who do chesed**, acts of loving-kindness.", R("Ruth Rabbah 2:14")),
  chk("q1", "chesed", "why", "According to Rabbi Ze'eira, why was the Book of Ruth written?", ["To teach the reward of loving-kindness", "To teach the laws of gleaning", "To record the history of Moab"],
      "No laws at all: **chesed** is the whole point.", ["He says the scroll has no laws in it.", "That's not his answer."], look_again=4),
  concept("The hidden face", "Ruth's neighbor in the Writings goes further: the Book of **Esther never names God at all**. The Talmud asks where Esther is hinted at in the Torah, and answers with God's warning, \"I will hide My face\" (Deuteronomy 31:18): **haster astir** sounds like **Esther**.", R("Chullin 139b")),
  term(S("Esther 5:4", 4, 8), "\"let Your Majesty and Haman come today\" (Esther 5:4). Read only the **first letters** of these four Hebrew words: yod, heh, vav, heh, the **four-letter Name**. God is in the story, hidden inside an ordinary sentence.", TN("Esther 5:4")),
  chk("q2", "hidden", "why", "What is hidden in the first letters of four words in Esther 5:4?", ["The four-letter Name of God", "Esther's Hebrew name", "The word chesed"],
      "Yod, heh, vav, heh: **God's Name**, hidden in a dinner invitation.", ["Esther's Hebrew name, Hadassah, isn't there.", "Chesed isn't spelled there."], look_again=7),
  concept("A people growing up", "A teaching from your rabbi: the Torah can be read as a people **growing up spiritually**. First, God is a child's hero who fixes everything. Then the relationship becomes strained and complicated. In maturity, God is no longer a hand moving events, but a love that becomes **present when we make great moral choices**. Ruth is that last stage: God's shelter arrives as Boaz's robe, and God's chesed as Ruth's. The Bible scholar **Richard Elliott Friedman** traces a similar arc: God's visible presence fades across the Bible until Esther, where God is never named.", RABBI),
  {"kind": "reflect", "prompt": "If God is present in the moments when people choose chesed, where did you meet God this week?"},
  {"kind": "recap", "points": ["The narrator says God acted **twice**; everything else is **human chesed**.", "Ruth Rabbah 2:14: written **to teach the reward of chesed**.", "Esther: God **never named**, the Name **hidden** in Esther 5:4 (Chullin 139b).", "Your rabbi: a people growing up, God present **in our moral choices**."]}]}

R4 = {"id": "x-st-ruth-04", "title": "Ruth (4): A son for Naomi", "status": "draft", "related": [],
 "check_note": "Bava Batra 91b read on Sefaria 11/11.",
 "cards": [
  {"kind": "hook", "title": "Full again", "body": "Boaz marries Ruth, and she bears a son. The neighbors don't say \"a son is born to Ruth.\" They say: \"**A son is born to Naomi!**\" (4:13-17).", "src": TN("Ruth 4:13-17")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Who do the neighbors say the baby is born to?", "choices": ["Naomi", "Ruth", "Boaz", "Orpah"], "answer": 0,
   "why": "\"**A son is born to Naomi!**\" (4:17)."},
  text("Ruth 4:17"),
  concept("Empty, then full", "In chapter 1 Naomi said, \"I went away full, and Adonai has brought me back empty\" (1:21). Now a child is placed in her lap, and the women name him **Obed**, father of Jesse, **father of David**. Her emptiness is filled through Ruth's loyalty.", TN("Ruth 1:21, 4:16-17")),
  chk("q1", "naomi", "why", "Why do the neighbors call Ruth's son Naomi's?", ["Naomi, who came back empty, is made full again", "Naomi adopted him legally", "Ruth had left"],
      "The story ends where Naomi's grief began, **reversed**.", ["The text speaks of joy, not law.", "Ruth is still there; she is the one who gave Naomi this."], look_again=3),
  concept("Ruth saw Solomon", "The Talmud says **Ruth the Moabite lived to see the kingship of Solomon**: the stranger who chose to belong saw her great-great-grandson on the throne.", R("Bava Batra 91b")),
  chk("q2", "solomon", "pick", "According to Bava Batra 91b, whose reign did Ruth live to see?", ["Solomon's", "Saul's", "Moses'"],
      "**Solomon**, son of David, her great-great-grandson.", ["Saul was not of her line.", "Moses lived long before Ruth."], look_again=5),
  {"kind": "reflect", "prompt": "The line of David begins with a woman who chose to belong. What does that say to you about who belongs?"},
  {"kind": "recap", "points": ["\"**A son is born to Naomi!**\"", "Naomi, **empty**, is made **full** again.", "Obed, Jesse, **David**.", "Bava Batra 91b: Ruth **saw Solomon's kingship**."]}]}

R5 = {"id": "x-st-ruth-05", "title": "Ruth (3): The night at the threshing floor", "status": "draft", "related": [],
 "check_note": "Sanhedrin 19b read on Sefaria 11/11. Eshet chayil: Ruth 3:11 and Proverbs 31:10.",
 "cards": [
  {"kind": "hook", "title": "Naomi's plan", "body": "Naomi, who once said she came back empty, now makes a plan: \"Daughter, I must seek a home for you, where you may be happy\" (3:1). She sends Ruth to the threshing floor, at night, to Boaz (3:1-4).", "src": TN("Ruth 3:1-4")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "Boaz calls Ruth an eshet chayil, the phrase that opens the poem in Proverbs 31.", "answer": True,
   "why": "**Eshet chayil** (3:11), the same words as Proverbs 31:10."},
  text("Ruth 3:1"),
  text("Ruth 3:8"),
  concept("Stronger than Joseph", "At midnight Boaz wakes to find a woman at his feet, and he acts with complete honor. **Rabbi Yochanan**: what Joseph is praised for, resisting temptation, was for Boaz **a small thing**, his humility. (And Palti son of Laish, he adds, was greater still.)", R("Sanhedrin 19b")),
  chk("q1", "restraint", "why", "How does Rabbi Yochanan compare Boaz to Joseph?", ["What was Joseph's great strength was a small thing for Boaz", "Boaz was weaker than Joseph", "They never faced the same test"],
      "Joseph's **power** is Boaz's **humility**: the same restraint, held more lightly.", ["He says the opposite.", "He compares them precisely because they did."], look_again=4),
  text("Ruth 3:11"),
  term(S("Ruth 3:11", 11, 14), "\"what a fine woman you are\" (3:11). The Hebrew is **eshet chayil**, the words that open the poem of Proverbs 31 (31:10), which many families sing at the Friday night table.", {"type": "tradition", "ref": "Ruth 3:11; Proverbs 31:10"}),
  chk("q2", "chayil", "pick", "What Hebrew phrase does Boaz use for Ruth in 3:11?", ["Eshet chayil", "Go'el", "Peloni almoni"],
      "**Eshet chayil**, a woman of valor.", ["Go'el, redeemer, is Boaz's role.", "That's the unnamed relative in chapter 4."], look_again=7),
  {"kind": "recap", "points": ["Naomi: \"**I must seek a home for you.**\"", "Midnight at the threshing floor: Boaz acts with honor.", "Sanhedrin 19b: Joseph's strength was **Boaz's humility**.", "Ruth, an **eshet chayil**."]}]}

R6 = {"id": "x-st-ruth-06", "title": "Ruth (4): At the city gate", "status": "draft", "related": [],
 "check_note": "Ruth Rabbah 7:7 read on Sefaria 11/11.",
 "cards": [
  {"kind": "hook", "title": "So-and-so", "body": "Boaz goes to the town gate, where business was done in public, and calls over the relative who has the first right to redeem: \"Come over and sit down here, **So-and-so**!\" (4:1). The book never gives his name.", "src": TN("Ruth 4:1")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "What is the closer redeemer's name in the Book of Ruth?", "choices": ["He has none: he is only \"So-and-so\"", "Elimelech", "Obed", "Mahlon"], "answer": 0,
   "why": "**Peloni almoni**, So-and-so (4:1)."},
  text("Ruth 4:1"),
  concept("The man with no name", "Why no name? In the midrash, **Rabbi Yehoshua** says Peloni Almoni really was his name. **Rabbi Shmuel bar Nachman**: he was **mute from matters of Torah**. Afraid that marrying Ruth had doomed Naomi's sons, he refused her.", R("Ruth Rabbah 7:7")),
  chk("q1", "noname", "why", "What does Rabbi Shmuel bar Nachman say about the unnamed redeemer?", ["He was mute from matters of Torah, and refused Ruth out of fear", "He was a stranger to Bethlehem", "He was Boaz's brother"],
      "**Mute in matters of Torah**: afraid of what happened to Naomi's sons, he walked away from Ruth.", ["He was a relative of Elimelech.", "The midrash doesn't say that."], look_again=3),
  text("Ruth 4:7"),
  concept("The sandal", "To seal the deal, one man **takes off a sandal** and hands it to the other (4:7-8). The book stops to explain the custom, as if writing for readers who had forgotten it.", TN("Ruth 4:7-8")),
  text("Ruth 4:11"),
  term(S("Ruth 4:11", 10, 17), "\"like Rachel and Leah, both of whom built up the House of Israel!\" (4:11). The elders bless Ruth, a woman from Moab, by **the two sisters** you met in Genesis.", TN("Ruth 4:11")),
  chk("q2", "rachel-leah", "pick", "Which two women do the elders name when they bless Ruth?", ["Rachel and Leah", "Sarah and Rebekah", "Naomi and Orpah"],
      "\"**Like Rachel and Leah**, both of whom built up the House of Israel.\"", ["They're matriarchs too, but not the ones named here.", "Naomi and Orpah are in Ruth's own story."], look_again=8),
  {"kind": "recap", "points": ["\"**So-and-so**\": the redeemer without a name.", "Ruth Rabbah 7:7: \"mute from matters of Torah,\" he **refused Ruth**.", "A **sandal** seals the deal.", "The elders bless Ruth: **like Rachel and Leah**."]}]}

for L, t in ((R1, "Ruth (1)"), (R2, "Ruth (2)"), (R4, "Ruth (5)"), (R3, "Ruth (6)")):
    L["title"] = t + L["title"][L["title"].index(":"):]
LS = (R1, R2, R5, R6, R4, R3)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "stories", "units": [{"id": "x-st-ruth", "title": "Ruth", "subtitle": "The scroll of chesed: choosing, sheltering, and a God found in human kindness", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-stories_ruth.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
