"""Write data/src/x-stories_jonah.json: the Jonah unit (x-st-jonah), 4 lessons built around the holiday overview x-st-hol-03. Hebrew sliced by word index from sefaria-jonah.json (+ Exodus 34:6-7 from sefaria-exodus2.json)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for f in ("sefaria-jonah.json", "sefaria-exodus2.json") for s in json.load(open(os.path.join(ROOT, "data/src", f), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
TN = lambda ref: {"type": "tanakh", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
def text(ref): return {"kind": "text", "sefaria": ref, "src": TN(ref)}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
MEKH = "Mekhilta DeRabbi Yishmael, Tractate Pischa 1"

J1 = {"id": "x-st-jon-01", "title": "Jonah (1): Running away", "status": "draft", "related": [],
 "check_note": "Mekhilta Pischa 1 (Silverstein), Nedarim 38a, Pirkei DeRabbi Eliezer 10 (Friedlander), Zohar Vayakhel 7:81-83 (Soncino) read on Sefaria 11/12. English: JPS Tanakh Gender-Sensitive. Overview lesson: x-st-hol-03.",
 "cards": [
  {"kind": "hook", "title": "A prophet who says no", "body": "God tells **Jonah** to go to **Nineveh**, that great city, and proclaim judgment upon it. Jonah gets up, and heads the other way: **down to the sea**.", "src": TN("Jonah 1:1-3")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "According to one Midrash, why did Jonah run?", "choices": ["He knew Nineveh would repent, and Israel would look worse by comparison", "He was afraid the Assyrians would kill him", "He did not believe God had really spoken", "He wanted to see Tarshish"], "answer": 0,
   "why": "The Mekhilta says Jonah knew that \"the gentiles are close to repentance.\""},
  text("Jonah 1:1-3"),
  term(S("Jonah 1:1-3", 17, 21), "\"started out to flee to Tarshish from GOD’s service\" (1:3). The Midrash asks whether anyone can flee from God at all, and answers with Psalm 139: wherever you go, God is there.", TN("Jonah 1:3")),
  concept("Why he ran", "The **Mekhilta** says Jonah meant to leave the Land of Israel, where, in its view, the Divine Presence reveals itself. His reason: \"the gentiles are close to repentance.\" If Nineveh turned at once, Israel, which had not turned, would look guilty by comparison. God's answer: **I have many messengers like you**, and God sends the wind.", R(MEKH)),
  chk("q1", "flee", "why", "In the Mekhilta, why did Jonah flee?", ["He was protecting Israel: Nineveh would repent quickly and make Israel look worse", "He was afraid of the sailors", "He wanted to be a merchant"],
      "Jonah ran **for Israel's sake**, not out of fear for himself.", ["The sailors come later, and the Midrash's reason is Israel.", "Not in the Midrash."], look_again=4),
  concept("Paid in full", "**Rabbi Yochanan**: \"He paid the cost of the entire ship.\" **Pirkei d'Rabbi Eliezer** adds that the ship was two days away, and God sent a storm to bring it back to Jaffa, **to test Jonah**. Jonah took it as a sign his escape would succeed, and in his joy he paid his fare in advance.", R("Nedarim 38a; Pirkei DeRabbi Eliezer 10")),
  text("Jonah 1:5-6"),
  term(S("Jonah 1:5-6", 12, 18), "\"Jonah, meanwhile, had gone down into the hold of the vessel where he lay down and fell asleep\" (1:5). Down to Jaffa, down into the ship, down into the hold: the verb **went down**, יָרַד, keeps returning (1:3, 1:5).", TN("Jonah 1:3-5")),
  text("Jonah 1:9"),
  concept("A soul on a ship", "The **Zohar** reads the story as \"the whole of a man’s career in this world.\" Jonah going down into the ship is **the soul coming down into a body**. The storm is the judgment that follows a person, and the captain who wakes Jonah is the good inner voice: it is no time to sleep, **return to your Master**.", R("Zohar, Vayakhel 7:81-83")),
  chk("q2", "soul", "why", "In the Zohar's reading, what does Jonah going down into the ship stand for?", ["The soul coming down into a body in this world", "Israel going into exile", "A merchant's journey"],
      "The ship is life in this world, and Jonah is **the soul** in it.", ["Not the Zohar's reading here.", "Not the Zohar's reading here."], look_again=10),
  text("Jonah 1:12"),
  concept("Ready to give his life", "**Rabbi Yochanan** (in the Mekhilta): Jonah boarded the ship **only to cast himself into the sea**. Moses offered his life for Israel (\"blot me out of Your book\"), and so did David. Jonah, too, gave his life for his people.", R(MEKH)),
  {"kind": "reflect", "prompt": "Jonah runs, sleeps through the storm, and then offers his own life for the sailors. Is there something you know is yours to do that you have been sailing away from?"},
  {"kind": "recap", "points": ["Jonah flees **toward Tarshish** (1:3).", "Mekhilta: he ran **for Israel's sake**, knowing Nineveh would repent.", "**Down**, down, down: Jaffa, the ship, the hold.", "Zohar: Jonah is **the soul** on the ship of this world.", "\"**Heave me overboard**\": ready to give his life."]}]}

J2 = {"id": "x-st-jon-02", "title": "Jonah (2): Inside the fish", "status": "draft", "related": ["prayer:gvurot"],
 "check_note": "Pirkei DeRabbi Eliezer 10 (Friedlander) and Zohar Vayakhel 7:88-92 (Soncino) read on Sefaria 11/12. G'vurot wording from data/prayers.json.",
 "cards": [
  {"kind": "hook", "title": "Three days down", "body": "The sailors throw Jonah into the sea, and the storm stops. Jonah sinks, and is **swallowed**.", "src": TN("Jonah 1:15-2:1")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "The book of Jonah says Jonah was swallowed by a whale.", "answer": False,
   "why": "The text says **a huge fish**, דָּג גָּדוֹל. No species is named."},
  text("Jonah 2:1-2"),
  term(S("Jonah 2:1-2", 2, 4), "\"a huge fish\" (2:1). Notice who **provided** it: GOD.", TN("Jonah 2:1")),
  concept("Prepared from Creation", "**Rabbi Tarfon**: this fish was appointed **from the six days of Creation** to swallow Jonah. He entered its mouth as a person enters a great synagogue, and its two eyes were \"like windows of glass giving light to Jonah.\" **Rabbi Meir**: a pearl hung inside the fish, shining like the noon sun, and showed him **everything in the sea**.", R("Pirkei DeRabbi Eliezer 10")),
  chk("q1", "fish", "pick", "In Pirkei d'Rabbi Eliezer, when was Jonah's fish appointed?", ["During the six days of Creation", "On the morning of the storm", "After Jonah prayed"],
      "The rescue was **prepared before the running began**.", ["Earlier: Rabbi Tarfon says from Creation.", "Earlier: Rabbi Tarfon says from Creation."], look_again=4),
  concept("Under the Temple", "In the same Midrash, the fish shows Jonah the path Israel took **through the Reed Sea**, the pillars of the earth, and at last the **Foundation Stone beneath the Temple**. There the sons of Korah stand praying. They tell him: you are standing beneath God's Temple; pray, and you will be answered. So Jonah asks the fish to stop, and **begins to pray**.", R("Pirkei DeRabbi Eliezer 10")),
  term(S("Jonah 2:1-2", 14, 20), "\"Jonah prayed to the ETERNAL his God from the belly of the fish\" (2:2). On the ship, the sailors cried out and Jonah slept (1:5-6). Now **Jonah prays**.", TN("Jonah 1:5-6; 2:2")),
  chk("q2", "temple", "why", "In Pirkei d'Rabbi Eliezer, why is Jonah told to pray where he is?", ["He is beneath the Temple, where prayer is answered", "The fish is about to die", "The sailors asked him to"],
      "Even at the bottom of the sea, Jonah is **beneath the Temple**.", ["Not the Midrash's reason.", "The sailors are back on the ship."], look_again=6),
  {"kind": "relevance", "body": "In this Midrash Jonah prays to God as the One who kills and the One who makes alive. Every Amidah praises God in the same way in the **G'vurot**: מֶלֶךְ מֵמִית וּמְחַיֶּה.", "links": ["prayer:gvurot"]},
  concept("The fish is the grave", "The **Zohar** continues its reading: the fish that swallowed Jonah **is the grave**, and its belly is the belly of Sheol, the underworld (2:3). The three days and nights are a person's first days in the grave. When God speaks to the fish and it **spews Jonah out upon dry land**, the Zohar reads it as the day God will **awaken the dead**.", R("Zohar, Vayakhel 7:88-92")),
  text("Jonah 2:11"),
  {"kind": "reflect", "prompt": "Jonah prays only after he has gone as far down as anyone can go. What has a low place taught you about prayer?"},
  {"kind": "recap", "points": ["God **provided a huge fish** (2:1).", "Pirkei d'Rabbi Eliezer: prepared **from Creation**, lit by **a pearl**.", "Beneath **the Temple**, Jonah prays.", "G'vurot: God who **kills and gives life**.", "Zohar: the fish is **the grave**, dry land is **life again**."]}]}

J3 = {"id": "x-st-jon-03", "title": "Jonah (3): What God saw", "status": "draft", "related": [],
 "check_note": "Taanit 16a, Jerusalem Talmud Taanit 2:1 (Guggenheimer), Megillah 31a read on Sefaria 11/12. Reform Yom Kippur afternoon practice: see x-st-hol-03 note.",
 "cards": [
  {"kind": "hook", "title": "Sackcloth, and something more", "body": "Jonah's five words reach the king. He leaves his throne, puts on **sackcloth**, and decrees a fast for every person and every animal in Nineveh.", "src": TN("Jonah 3:4-9")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "On a public fast day, what does the Talmud say an elder reminds the people about Nineveh?", "choices": ["God saw their deeds, not their sackcloth and fasting", "Their fast lasted forty days", "Only the king repented", "Their prayers were in Hebrew"], "answer": 0,
   "why": "The verse says God saw **what they did** (3:10)."},
  text("Jonah 3:8"),
  term(S("Jonah 3:8", 11, 14), "\"from the injustice of which they are guilty\" (3:8). The king names not only evil ways but the injustice in their own hands.", TN("Jonah 3:8")),
  concept("Tear down the building", "**Shmuel**: the king of Nineveh proclaimed that even someone who **stole a beam** and built it into a house must **tear down the whole building** and return the beam. The Talmud notes that the Sages require only money in such a case; Nineveh went further, to remove every trace of what was stolen.", R("Taanit 16a")),
  chk("q1", "beam", "why", "In Taanit 16a, what did Nineveh's king require of someone who had built a stolen beam into a house?", ["Tear the building down and return the beam", "Pay a fine to the king", "Fast for forty days"],
      "Repair, not just regret: **give back what you took**.", ["Shmuel says they went further than money.", "Not in Shmuel's teaching."], look_again=4),
  text("Jonah 3:10"),
  concept("Deeds, not sackcloth", "On a public fast, the Talmud has an elder say: \"it is not sackcloth and fasting that cause atonement for our sins.\" **Repentance and good deeds** do. The verse does not say God saw their sackcloth and their fasting; it says **God saw what they did**.", R("Taanit 16a")),
  chk("q2", "deeds", "pick", "According to Taanit 16a, what brings atonement?", ["Repentance and good deeds", "Sackcloth and fasting", "Ashes on the ark"],
      "God saw **their deeds** (3:10).", ["The elder says these are not what atones.", "A sign of mourning, not what atones."], look_again=7),
  concept("Was it real?", "The two Talmuds read Nineveh differently. In the Babylonian Talmud, the people separate the animals from their young and plead: even if we are not worthy, **these animals have not sinned**. In the Jerusalem Talmud, **Resh Lakish** says \"the people of Nineveh repented in trickery\": the separated animals were crying so God would give in. **Rabbi Yochanan** adds that they returned what was in their hands, **but not what was locked in their chests**.", R("Taanit 16a; Jerusalem Talmud Taanit 2:1")),
  chk("q3", "trickery", "why", "How does Resh Lakish judge Nineveh's repentance in the Jerusalem Talmud?", ["As partly a trick, to pressure God", "As perfect", "As something that never happened"],
      "Even a famous repentance can be **only partly honest**. The Babylonian Talmud reads the same scene as a sincere plea.", ["The Babylonian Talmud is kinder; Resh Lakish is not.", "He agrees they did something; he doubts their motive."], look_again=9),
  concept("Why on Yom Kippur", "The Talmud says Jonah is read on **Yom Kippur afternoon**, as the haftarah, the book \"which mentions the repentance of the people of Nineveh.\"", R("Megillah 31a")),
  {"kind": "reflect", "prompt": "The Talmud says God looked past the sackcloth to the deeds, and one rabbi still doubts what was hidden in the chests. What would a change in your deeds, not only your words, look like this year?"},
  {"kind": "recap", "points": ["**Turn back** from evil ways and **injustice** (3:8).", "Shmuel: return even **a beam in the wall**.", "Taanit 16a: **deeds**, not sackcloth, bring atonement.", "Resh Lakish: Nineveh's repentance was **partly a trick**.", "Jonah is read on **Yom Kippur afternoon** (Megillah 31a)."]}]}

J4 = {"id": "x-st-jon-04", "title": "Jonah (4): The plant and the question", "status": "draft", "related": [],
 "check_note": "Pirkei DeRabbi Eliezer 43 and Mekhilta Pischa 1 read on Sefaria 11/12. Word comparison Exodus 34:6 vs Jonah 4:2 checked by script on the Masorah text.",
 "cards": [
  {"kind": "hook", "title": "Angry enough to die", "body": "Nineveh is spared. Jonah, who saved a ship of strangers with his own life, is **furious**, and asks God to take his life.", "src": TN("Jonah 4:1-3")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "When Jonah quotes God's attributes from Exodus 34, he quotes them word for word.", "answer": False,
   "why": "He drops **faithfulness** and adds **renouncing punishment**, the very thing he is angry about."},
  text("Jonah 4:2"),
  term(S("Jonah 4:2", 17, 24), "\"a compassionate and gracious God, slow to anger, abounding in kindness, renouncing punishment\" (4:2).", TN("Jonah 4:2")),
  concept("Words from Sinai, changed", "At Sinai God proclaimed: \"a God compassionate and gracious, slow to anger, abounding in kindness and faithfulness\" (Exodus 34:6). In Hebrew, Jonah's list **stops before faithfulness**, וֶאֱמֶת, and ends instead with **renouncing punishment**. He even reverses the first pair: Exodus has רַחוּם וְחַנּוּן; Jonah has חַנּוּן וְרַחוּם.", {"type": "tanakh", "ref": "Exodus 34:6; Jonah 4:2"}),
  chk("q1", "emet", "pick", "Which attribute from Exodus 34:6 is missing from Jonah's list?", ["Faithfulness", "Kindness", "Slow to anger"],
      "Jonah keeps the mercy and leaves out **faithfulness**.", ["Kindness is there: וְרַב־חֶסֶד.", "Slow to anger is there."], look_again=4),
  text("Jonah 4:10-11"),
  term(S("Jonah 4:10-11", 14, 20), "\"And should not I care about Nineveh, that great city\" (4:11). The book ends on God's question.", TN("Jonah 4:11")),
  concept("The king was Pharaoh", "**Pirkei d'Rabbi Eliezer** opens with \"Know thou the power of repentance.\" Its example: **Pharaoh**, who defied God by asking who the Lord was, and at the Sea turned with the words of **Mi Chamocha**. God saved him, and he went on to **rule in Nineveh**. When Jonah came, he rose from his throne and put on sackcloth. Infants cried for their mothers, and by the merit of **4,123 children**, more than twelve hundred thousand people were saved (4:11).", R("Pirkei DeRabbi Eliezer 43")),
  chk("q2", "pharaoh", "pick", "In Pirkei d'Rabbi Eliezer 43, who was the king of Nineveh?", ["Pharaoh, who had turned at the Sea", "Jonah's father", "Ahasuerus"],
      "The king who once defied God became the king who led a city in repentance.", ["Not in the Midrash.", "Ahasuerus is the king of the Esther story."], look_again=8),
  concept("The son and the Father", "The **Mekhilta**: \"Jonah claimed the honor of the son, but not the honor of the Father.\" He defended Israel's honor, but not God's. So, it says, God spoke to Jonah a second time, **but not a third**.", R(MEKH)),
  concept("A question, not a command", "God does not force Jonah. God teaches with **a plant, a worm and a question**, and the book stops before Jonah answers. This fits your rabbi's teaching of a people **growing up**: God present less as a hand that compels and more in the choices we make. The answer to God's question is left to the reader.", {"type": "reform", "ref": "Jonah 4:6-11; teaching from Jamie's rabbi (oral, as Jamie retold it)", "note": "connection is mine; check with Jamie"}),
  {"kind": "reflect", "prompt": "Jonah wanted justice for Nineveh; God asked him to care. Who is it hardest for you to wish well?"},
  {"kind": "recap", "points": ["Jonah quotes Sinai, but **drops faithfulness** (4:2).", "\"**Should not I care** about Nineveh?\" (4:11).", "Pirkei d'Rabbi Eliezer: the king was **Pharaoh**, saved by **the children**.", "Mekhilta: the honor of **the son**, not **the Father**.", "A question, not a command: **the reader answers**."]}]}

LS = (J1, J2, J3, J4)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "stories", "units": [{"id": "x-st-jonah", "title": "Jonah", "subtitle": "The prophet who ran, and the city that turned", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-stories_jonah.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
