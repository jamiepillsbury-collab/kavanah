"""Write data/src/x-history.json: Jewish history units 1-2 (x-hi-begin, x-hi-exile), 6 lessons. Hebrew sliced by word index from sefaria-history1.json.
Scholarly facts (dates, inscriptions, deportation numbers) are from memory and flagged in each lesson's check_note. look_again is given as a card title or sefaria ref and resolved to an index at the end."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-history1.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b):
    w = " ".join(SRC[(ref, "he")]).split()[a:b]
    return " ".join(x for x in w if x not in ("׀", "{פ}", "{ס}")).replace("יְהֹוָה", "יְיָ")
TN = lambda ref: {"type": "torah" if ref.startswith("Deut") else "tanakh", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
SCH = lambda ref, note="From memory; check.": {"type": "scholarly", "ref": ref, "note": note}
TRAD = lambda ref, note=None: {"type": "tradition", "ref": ref, **({"note": note} if note else {})}
REF = lambda ref, note=None: {"type": "reform", "ref": ref, **({"note": note} if note else {})}
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

H1 = {"id": "x-hi-01", "title": "The ancestors", "status": "draft", "related": ["prayer:avot"],
 "check_note": "Bereshit Rabbah 38:13 read on Sefaria 11/14. Seder Olam date for Abraham, the camel finding and the scholarly dating are from memory: check.",
 "cards": [
  hook("A family story in one sentence", "When an Israelite farmer brought the first fruits to the sanctuary, they told the whole family history in a single line, beginning with a wanderer.", TN("Deuteronomy 26:5")),
  pre("What does the Bible say Abraham's father Terah did?", ["Worshiped other gods", "Served as a priest of the one God", "Ruled as king of Ur", "Kept sheep in Egypt"],
      "Joshua says the ancestors \"lived beyond the Euphrates and worshiped other gods.\""),
  text("Deuteronomy 26:5"),
  term(S("Deuteronomy 26:5", 6, 9), "\"My father was a fugitive Aramean\" (26:5). The Passover Haggadah builds its telling of the Exodus on these three words.", TN("Deuteronomy 26:5")),
  text("Joshua 24:2-3"),
  concept("The idol shop", "The midrash fills in Joshua's hint. **Terah sold idols.** One day he left young Abraham to mind the shop. A customer came in; Abraham asked his age. Sixty, said the man. Abraham answered: a man of sixty, bowing down to something made **yesterday**? The man left, ashamed. The story ends with Abraham smashing the idols.", R("Bereshit Rabbah 38:13")),
  chk("q1", "idols", "why", "In Bereshit Rabbah 38:13, why is the idol buyer ashamed?", ["Abraham shows him he is older than the god he is buying", "Abraham charges him too much", "Terah catches him stealing"],
      "A grown man bowing to a thing **a day old**: Abraham's first argument is a question.", ["Not in the midrash.", "Not in the midrash."], "The idol shop"),
  tl("Tradition: 1812 BCE", "Seder Olam, a 2nd-century chronology, puts Abraham's birth in year **1948** from Creation.", R("Seder Olam Rabbah 1", "1656 years to the Flood (read on Sefaria) + 292 to Abraham; check.")),
  tl("Scholars: c. 900-500 BCE", "Most scholars date the **writing** of the ancestor stories to these centuries, from older oral traditions.", SCH("e.g., Finkelstein & Silberman, The Bible Unearthed (2001)")),
  concept("What historians can say", "No inscription or dig has found **Abraham, Sarah, Isaac or Jacob**. Some details fit an early age (names, travel from Mesopotamia to Canaan). Others fit a later one: **domesticated camels** in Canaan date to about 1000 BCE, centuries after the traditional date. Many scholars read Genesis as a people's **memory of its origins**, written down long after.", SCH("Camel bones: Sapir-Hen & Ben-Yosef, Tel Aviv 40 (2013)")),
  chk("q2", "evidence", "pick", "What have archaeologists found about Abraham?", ["No inscription or find that names him", "His tomb with an inscription", "A letter he wrote in Ur"],
      "The ancestors are known **only from the Bible** and later tradition.", ["The tomb at Hebron is a tradition, not an inscription.", "No such letter exists."], "What historians can say"),
  concept("Two questions", "**Did it happen?** and **What does it mean?** are different questions. History works on the first; the tradition answers the second through the story. This track keeps both, side by side, and labels each card: Tradition, Scholars, Reform.", REF("Reform approach to text and history", "e.g., CCAR Centenary Perspective (1976); check.")),
  rel("In every Amidah you name the ancestors: Elohei Avraham, Elohei Sarah. The Genesis lessons tell their stories.", ["prayer:avot", "lesson:x-st-gen-10"]),
  refl("Your family has its own one-sentence story of where you came from. What is it, and which part do you know is true?"),
  recap("\"**My father was a fugitive Aramean**\" (Deut 26:5).", "Joshua 24:2: the ancestors **worshiped other gods**.", "Midrash: Abraham in **Terah's idol shop**.", "No inscription names the ancestors; scholars date the **writing** much later.")]}

H2 = {"id": "x-hi-02", "title": "Israel in Canaan", "status": "draft", "related": [],
 "check_note": "Jerusalem Talmud Sheviit 6:1 and Bava Batra 14b read on Sefaria 11/14. Merneptah Stele date, village survey and Deuteronomistic History are from memory: check.",
 "cards": [
  hook("After Moses", "The book of **Joshua** tells of a fast conquest. The book of **Judges** tells of a slow, messy settling in, tribe by tribe, with many Canaanites still in the land.", TN("Joshua 11:23; Judges 1:27-33")),
  pre("Where does the name Israel first appear outside the Bible?", ["On an Egyptian victory stone", "On a Babylonian clay tablet", "In a Greek history book", "On a Roman coin"],
      "The **Merneptah Stele**, about 1208 BCE."),
  concept("Three letters", "Rabbi Shmuel bar Nachman: before crossing the Jordan, **Joshua sent three messages**. Whoever wants to leave, leave. Whoever wants to make peace, make peace. Whoever wants to fight, fight. The Girgashites left, and went to Africa.", R("Jerusalem Talmud Sheviit 6:1")),
  chk("q1", "letters", "pick", "In the Jerusalem Talmud, what three choices did Joshua offer the peoples of Canaan?", ["Leave, make peace, or fight", "Convert, pay tax, or leave", "Fight, flee, or hide"],
      "The rabbis gave Joshua's wars **a way out**.", ["Not the Talmud's list.", "Not the Talmud's list."], "Three letters"),
  text("Judges 21:25"),
  term(S("Judges 21:25", 0, 5), "\"In those days there was no king in Israel\" (21:25). Judges ends with this line, and it points ahead to the kings.", TN("Judges 21:25")),
  tl("c. 1208 BCE", "Pharaoh **Merneptah** boasts that Israel is wiped out: the first mention of Israel outside the Bible.", SCH("Merneptah Stele, Egyptian Museum, Cairo")),
  tl("c. 1200-1000 BCE", "Hundreds of **small new villages** appear in the hill country of Canaan: the age of the Judges.", SCH("Hill-country surveys, e.g., Finkelstein (1988)")),
  concept("The stone and the villages", "On the stele, Israel is written with the sign for **a people**, not a city: a group, already in Canaan. The new hill villages share simple **four-room houses**, and their bones show **no pigs**. Many scholars think most early Israelites grew up **inside Canaan**; others argue a smaller group did come out of Egypt, carrying the Exodus story with them.", SCH("e.g., Dever, Who Were the Early Israelites? (2003)")),
  chk("q2", "stele", "why", "On the Merneptah Stele, Israel is marked as a people rather than a city. What does that suggest?", ["Israel was a group living in Canaan, not yet a city-state", "Israel was still in Egypt", "Israel was a kingdom with a capital"],
      "A people **in the land** by about 1208 BCE.", ["The stele places Israel in Canaan.", "Kings come later."], "The stone and the villages"),
  concept("Who wrote these books?", "**Tradition**: Joshua wrote his own book and the last eight verses of the Torah; Samuel wrote Judges and Ruth (Bava Batra 14b). **Scholars**: Joshua through Kings form one long history, edited around the 7th and 6th centuries BCE, judging each age by Deuteronomy's laws.", R("Bava Batra 14b; scholars: Noth, the Deuteronomistic History (1943), check")),
  text("Joshua 24:15"),
  term(S("Joshua 24:15", 25, 29), "\"I and my household will serve GOD\" (24:15). Joshua's last speech asks the people to **choose this day**.", TN("Joshua 24:15")),
  rel("Deborah judged Israel in these years. Her story is in the Torah stories track.", ["lesson:x-st-deb-01"]),
  refl("Joshua asks a people to choose, again, what they will serve. What would you say you choose, this year?"),
  recap("Joshua: fast conquest; Judges: **slow settling**.", "Talmud: Joshua's **three letters**: leave, make peace, or fight.", "**Merneptah Stele**, about 1208 BCE: Israel, a people in Canaan.", "\"**There was no king in Israel**\" (Judges 21:25).")]}

H3 = {"id": "x-hi-03", "title": "The two kingdoms", "status": "draft", "related": [],
 "check_note": "Sanhedrin 102a read on Sefaria 11/14. Tel Dan and Mesha stelae details and dates are from memory: check.",
 "cards": [
  hook("Lighten our load", "After Solomon dies, the northern tribes ask his son **Rehoboam** to lighten the heavy work his father put on them. He answers that he will make it heavier.", TN("1 Kings 12:1-14")),
  pre("What did Jeroboam, the first king of the north, set up in Bethel and Dan?", ["Two golden calves", "Two temples to Baal", "Two Torah scrolls", "Two watchtowers"],
      "\"So the king took counsel and made two golden calves\" (1 Kings 12:28)."),
  tl("c. 1000 BCE", "**David** rules from Jerusalem; then Solomon builds the Temple.", SCH("Conventional date")),
  tl("c. 930 BCE", "The kingdom splits: **Israel** in the north, **Judah** in the south, with Jerusalem.", SCH("Conventional date")),
  text("1 Kings 12:16"),
  term(S("1 Kings 12:16", 18, 20), "\"To your tents, O Israel!\" The north walks away from David's house.", TN("1 Kings 12:16")),
  text("1 Kings 12:28-29"),
  concept("Why the calves?", "Jeroboam's fear was simple: if his people kept going up to **Jerusalem** to worship, their hearts would go back to Judah's king. So he built **his own shrines** at the edges of his land. The book of Kings blames every later northern king for this.", TN("1 Kings 12:26-30")),
  concept("God grabs his garment", "Rabbi Abba: God took hold of Jeroboam by his garment and said, **Repent**, and you and I and the son of Yishai will walk together in the Garden of Eden. Jeroboam asked, \"Who will walk in the lead?\" \"The son of Yishai will walk in the lead.\" Jeroboam: \"If so, I do not wish to repent.\"", R("Sanhedrin 102a")),
  chk("q1", "jeroboam", "why", "In Sanhedrin 102a, why does Jeroboam refuse to repent?", ["David would walk ahead of him", "He did not believe in the Garden of Eden", "The prophets had insulted him"],
      "Pride: he would rather **lose Eden than walk second**.", ["Not in the Talmud.", "Not in the Talmud."], "God grabs his garment"),
  concept("The House of David in stone", "In **1993**, at Tel Dan in the far north, archaeologists found part of a 9th-century BCE stone. In Aramaic, a king of Aram boasts of killing the king of Israel and a king of the **House of David**: the first mention of David outside the Bible. Another stone, the **Mesha Stele**, names Israel's king Omri. How large David's kingdom was is still argued.", SCH("Tel Dan Stele (Israel Museum); Mesha Stele (Louvre)")),
  chk("q2", "teldan", "pick", "What does the Tel Dan Stele show?", ["David's dynasty was known outside the Bible", "Solomon's Temple plan", "That David never existed"],
      "\"**House of David**\" in a 9th-century enemy's inscription.", ["No plan of the Temple has been found.", "It shows the opposite."], "The House of David in stone"),
  text("2 Samuel 7:16"),
  rel("Elijah's stories happen in the northern kingdom, under Omri's son Ahab. David's own stories are in their unit.", ["lesson:x-st-eli-01", "lesson:x-st-dav-01"]),
  refl("Rehoboam could have lightened the load and kept the kingdom whole. When has a small act of listening, or not listening, changed things for you?"),
  recap("Rehoboam's answer, and \"**To your tents, O Israel!**\"", "Two kingdoms: **Israel** (north) and **Judah** (south), about 930 BCE.", "Jeroboam's **golden calves** at Bethel and Dan.", "Sanhedrin 102a: \"**Who will walk in the lead?**\"", "Tel Dan: the **House of David** in stone.")]}

H4 = {"id": "x-hi-04", "title": "Assyria and the lost tribes", "status": "draft", "related": ["prayer:m_ahavah_rabbah"],
 "check_note": "Mishnah Sanhedrin 10:3 read on Sefaria 11/14. Sargon's deportation number, Sennacherib's prism, Jerusalem's growth and the Sambatyon sources are from memory: check.",
 "cards": [
  hook("Samaria falls", "Assyria, the great power of its day, besieges **Samaria**, capital of the northern kingdom, for three years.", TN("2 Kings 17:5-6")),
  pre("According to Rabbi Akiva in the Mishnah, will the ten lost tribes return?", ["No, they will not return", "Yes, with the Messiah", "They already came back with Ezra", "Only two of them will"],
      "Rabbi Akiva says no; Rabbi Eliezer disagrees."),
  tl("722 BCE", "Assyria conquers **Samaria**. The northern kingdom ends.", SCH("Conventional date (722 or 720 BCE)")),
  tl("701 BCE", "Assyria's king **Sennacherib** besieges Jerusalem. The city survives; Judah goes on.", SCH("2 Kings 18-19; Sennacherib's prism")),
  text("2 Kings 17:6"),
  concept("What Assyria did", "Assyria moved conquered peoples around to break them. Its king **Sargon II** claims he carried off about **27,000** people from Samaria, and the Bible says Assyria settled other peoples in their place. Many northerners also **fled south**: Jerusalem grew several times over in these years.", SCH("Sargon II's annals; Jerusalem's growth: e.g., Broshi (1974)")),
  chk("q1", "deport", "pick", "What did Assyria do with the people of Samaria?", ["Deported many and settled other peoples in their place", "Left them all in place", "Sent them to Egypt"],
      "**Exile and resettlement** were Assyria's tools.", ["The Bible and Assyria's records say otherwise.", "They went east, to Assyria and Media."], "What Assyria did"),
  concept("Will they come back?", "The Mishnah records a debate. **Rabbi Akiva**: the ten tribes will not return, as it says, \"As it is this day\": as a day passes and never comes back. **Rabbi Eliezer** reads the same words the other way: as a day grows dark and then **brightens again**, so it will be for them.", R("Mishnah Sanhedrin 10:3")),
  chk("q2", "akiva", "why", "How does Rabbi Eliezer read \"as it is this day\"?", ["A day darkens and then brightens: they will return", "A day passes forever: they are gone", "They will return on one special day"],
      "Same verse, **two readings**: an ending, or a night before morning.", ["That is Rabbi Akiva's reading.", "Not in the Mishnah."], "Will they come back?"),
  concept("The search", "The lost tribes became legend: beyond the river **Sambatyon**, which rests on Shabbat, they live on. Travelers like **Eldad HaDani** (9th century) claimed to come from them. Communities from Ethiopia to India have been linked to a lost tribe.", TRAD("Sambatyon: Sanhedrin 65b; Eldad HaDani", "From memory; check.")),
  text("Isaiah 11:12"),
  rel("Each morning in Ahavah Rabbah you pray to be brought \"from the four corners of the earth,\" Isaiah's words. And Jonah's Nineveh was Assyria's great city.", ["prayer:m_ahavah_rabbah", "lesson:x-st-jon-01"]),
  refl("Rabbi Akiva saw an ending; Rabbi Eliezer saw a night before morning. Which way do you tend to read your own losses?"),
  recap("**722 BCE**: Assyria ends the northern kingdom.", "Exile and **resettlement**; many flee south to Judah.", "Rabbi Akiva: gone like a day; Rabbi Eliezer: **morning comes**.", "Isaiah: gathered \"**from the four corners of the earth**.\"")]}

H5 = {"id": "x-hi-05", "title": "By the rivers of Babylon", "status": "draft", "related": ["prayer:t_etz"],
 "check_note": "Mishnah Taanit 4:6, Yoma 9b and Pesachim 87b read on Sefaria 11/14. Dates, the Al-Yahudu tablets and the scholarly view of exile and Torah are from memory: check. Does CBB read Lamentations on Tisha B'Av?",
 "cards": [
  hook("The city burns", "Babylon's king **Nebuchadnezzar** takes Jerusalem, burns the Temple, and carries Judah's leaders away.", TN("2 Kings 25:8-11")),
  pre("What did the prophet Jeremiah tell the exiles in Babylon to do?", ["Build houses, plant gardens, and pray for the city", "Escape at once", "Refuse to speak Babylonian", "Fast until the Temple was rebuilt"],
      "\"Build houses and live in them, plant gardens and eat their fruit\" (Jer 29:5)."),
  tl("597 BCE", "First exile: King **Jehoiachin** and Jerusalem's elite are taken to Babylon.", SCH("Babylonian Chronicle")),
  tl("586 BCE", "Jerusalem falls. The **First Temple** is destroyed.", SCH("Conventional date (586 or 587 BCE)")),
  term(S("Lamentations 1:1", 0, 5), "\"Alas! Lonely sits the city\" (Lam 1:1). The book of Lamentations, read on **Tisha B'Av**, opens with this word, Eichah.", TN("Lamentations 1:1")),
  text("Psalms 137:1"),
  text("Psalms 137:5-6"),
  concept("Why was it destroyed?", "The Mishnah lists five disasters on the **Ninth of Av**, among them both Temples destroyed. The Talmud asks why. The First: idolatry, sexual sins and bloodshed. The Second, in an age of Torah and kindness? \"**Wanton hatred**,\" which the Talmud weighs as equal to all three.", R("Mishnah Taanit 4:6; Yoma 9b")),
  chk("q1", "hatred", "why", "In Yoma 9b, why was the Second Temple destroyed?", ["Wanton hatred between people", "Idolatry", "A failure to bring sacrifices"],
      "Not ritual failure but **how people treated each other**.", ["The Talmud gives that for the First Temple.", "Not the Talmud's answer."], "Why was it destroyed?"),
  text("Jeremiah 29:5-7"),
  term(S("Jeremiah 29:5-7", 23, 26), "\"Seek the welfare of the city\" (29:7). From here come Jewish prayers for the country where Jews live.", TN("Jeremiah 29:7")),
  chk("q2", "jeremiah", "pick", "What does Jeremiah tell the exiles to seek?", ["The welfare of the city they were exiled to", "Revenge on Babylon", "A quick way home"],
      "Live **fully** where you are, and pray for it.", ["Psalm 137 has anger; Jeremiah does not counsel it.", "He says the exile will be long."], "Jeremiah 29:5-7"),
  concept("Exile as seed", "Rabbi Elazar: God exiled Israel among the nations \"**only so that converts would join them**\": as a farmer sows a little grain to harvest much more.", R("Pesachim 87b")),
  concept("A people without a Temple", "Clay tablets from Babylonia (the **Al-Yahudu** tablets) record Judean families farming in a village called **Judah-town**, giving their children Hebrew names. Many scholars think that in exile, without Temple or king, Judeans gathered around **texts and prayer**, and much of the Torah took its final shape.", SCH("Al-Yahudu tablets: Pearce & Wunsch (2014)")),
  rel("When the Torah returns to the ark, you sing Hashiveinu, from the last chapter of Lamentations: bring us back to You.", ["prayer:t_etz"]),
  refl("Jeremiah says: build, plant, pray for the place you are, even if it is not home. Where in your life are you being asked to do that?"),
  recap("**586 BCE**: the First Temple falls.", "Lamentations and Psalm 137: \"**If I forget you, O Jerusalem**.\"", "Yoma 9b: the Second Temple fell for **wanton hatred**.", "Jeremiah: \"**seek the welfare of the city**.\"", "In exile, a people of **text and prayer**.")]}

H6 = {"id": "x-hi-06", "title": "Return and the Second Temple", "status": "draft", "related": ["prayer:torah_before"],
 "check_note": "Bava Kamma 82a (incl. the wilderness origin of Monday/Thursday reading) and Sanhedrin 21b read on Sefaria 11/14. Cyrus Cylinder, 515 BCE and Ezra's dates are from memory: check.",
 "cards": [
  hook("A new empire", "In **539 BCE**, Persia's king **Cyrus** takes Babylon. Soon after, he lets the Judeans go home.", TN("Ezra 1:1")),
  pre("According to the Talmud, what changed about the Torah scroll in Ezra's time?", ["Its script, to the square letters", "Its language, to Greek", "Its length", "The order of its books"],
      "Sanhedrin 21b: the Torah was given again in **Ashurit script**, the square letters you learned."),
  tl("539 BCE", "**Cyrus** conquers Babylon and lets exiles return.", SCH("Cyrus Cylinder (British Museum)")),
  tl("515 BCE", "The **Second Temple** is finished in Jerusalem.", SCH("Ezra 6:15; conventional date")),
  tl("c. 450 BCE", "**Ezra** the scribe and **Nehemiah** the governor rebuild community and walls.", SCH("Dates debated")),
  text("Ezra 1:2-3"),
  concept("Cyrus in his own words", "Cyrus left his own clay **cylinder**: he says he returned peoples and their gods to their homes. It never names Judeans, but it fits Ezra's story. And many Judeans **stayed** in Babylon, which later became the great center of the Talmud.", SCH("Cyrus Cylinder (British Museum)")),
  chk("q1", "cyrus", "pick", "Did all the exiles go back to Judah?", ["No, many stayed in Babylon", "Yes, every one", "No, they all went to Egypt"],
      "Return and **diaspora** began together.", ["Many stayed; Babylon's community lasted for centuries.", "Not in the sources."], "Cyrus in his own words"),
  text("Nehemiah 8:2-3"),
  text("Nehemiah 8:8"),
  concept("Ezra's ordinances", "The Talmud lists ten rules Ezra made. Among them: read the Torah on **Shabbat afternoon**. The Monday and Thursday readings were older, from the wilderness, so Israel would not go \"three days without hearing the Torah.\" Ezra set the form still used: **three people** read, at least **ten verses**.", R("Bava Kamma 82a")),
  chk("q2", "ordinances", "pick", "What does the Talmud say Ezra added to Torah reading?", ["A reading on Shabbat afternoon, with three readers", "The first Monday and Thursday readings", "Reading only on festivals"],
      "Ezra **added and shaped**; the weekday readings were older.", ["The Talmud says those go back to the wilderness.", "Not in the Talmud."], "Ezra's ordinances"),
  concept("New letters", "Mar Zutra: the Torah was first given in **Ivrit** script (the old Hebrew letters). In Ezra's days it was given again in \"**Ashurit script**,\" the square letters still used today. Rabbi Yosei: Ezra was worthy that the Torah could have been given through him, had Moses not come first.", R("Sanhedrin 21b")),
  chk("q3", "script", "why", "Why does the Talmud link Ezra to the square Hebrew letters?", ["The Torah was given again in Ashurit script in his days", "He invented Hebrew", "He wrote the first siddur"],
      "The letters you are learning carry **Ezra's** name in tradition.", ["Hebrew is older; the script changed.", "Siddurs came much later."], "New letters"),
  rel("Every Torah reading you hear goes back to Ezra's square: a scroll read aloud and explained. Esther's story is set among the Jews who stayed in Persia.", ["prayer:torah_before", "lesson:x-st-esther-01"]),
  refl("Ezra read \"from the first light until midday\" to everyone who could understand. What would you want read aloud, and explained, to your whole community?"),
  recap("**539 BCE**: Cyrus lets exiles return; many stay.", "**515 BCE**: the Second Temple.", "Ezra reads the Torah aloud, \"**translating it and giving the sense**.\"", "Ezra adds **Shabbat afternoon** and sets **three readers, ten verses**.", "Sanhedrin 21b: **Ashurit script**, the square letters.")]}

U1, U2 = (H1, H2, H3), (H4, H5, H6)
for L in U1 + U2:
    cs = L["cards"]
    for c in cs:
        if c["kind"] == "check" and "look_again" in c:
            k = c["look_again"]
            c["look_again"] = next(i for i, x in enumerate(cs) if x.get("title") == k or x.get("sefaria") == k)
            c["src"] = cs[c["look_again"]]["src"]
        elif c["kind"] == "check": c["src"] = cs[0]["src"]
out = {"track": "history", "units": [
    {"id": "x-hi-begin", "title": "Beginnings", "subtitle": "Ancestors, Canaan and the two kingdoms", "lessons": list(U1)},
    {"id": "x-hi-exile", "title": "Exile and return", "subtitle": "Assyria, Babylon and the Second Temple", "lessons": list(U2)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-history.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in U1 + U2])
