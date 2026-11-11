"""Write data/src/x-stories_exodus.json: the Exodus unit (x-st-exodus). Lessons 01-08: birth, bush, hardened heart, the Sea, Sinai, V'shamru, broken tablets, Thirteen Attributes. Hebrew sliced by word index from sefaria-exodus.json."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for f in ("sefaria-exodus.json", "sefaria-exodus2.json") for s in json.load(open(os.path.join(ROOT, "data/src", f), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
TN = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
def text(ref): return {"kind": "text", "sefaria": ref, "src": TN(ref)}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}

X1 = {"id": "x-st-exo-01", "title": "Moses (1): Drawn from the water", "status": "draft", "related": [], "parashah": ["Shemot"],
 "check_note": "Sotah 11b and 12b read on Sefaria 11/11 (William Davidson). English: Contemporary Torah.",
 "cards": [
  {"kind": "hook", "title": "Five women and a baby", "body": "A new Pharaoh orders the **Hebrew midwives** to kill every newborn boy. Before Moses ever speaks a word, his life is saved again and again, **every time by a woman**.", "src": TN("Exodus 1:15-2:10")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "The Torah gives the names of the midwives who defied Pharaoh.", "answer": True,
   "why": "**Shiphrah** and **Puah** (1:15). Pharaoh himself is never named."},
  text("Exodus 1:15-17"),
  term(S("Exodus 1:15-17", 24, 27), "\"The midwives, fearing God\" (1:17). Here, fearing God means **refusing a king's order to kill**.", TN("Exodus 1:17")),
  concept("Who were the midwives?", "In one view in the Talmud, **Shiphrah** was **Jochebed**, Moses' mother, and **Puah** was **Miriam**, his sister. Puah made soothing sounds to the newborns, and Miriam, speaking with divine inspiration, foresaw that her mother would bear a son **who would save the Jewish people**. (Another view: Jochebed and Elisheba, Aaron's wife.)", R("Sotah 11b")),
  chk("q1", "midwives", "why", "In one view in Sotah 11b, who were Shiphrah and Puah?", ["Jochebed and Miriam, Moses' mother and sister", "Two Egyptian women", "Pharaoh's daughters"],
      "Moses' own **mother and sister** were already saving lives before he was born.", ["The Talmud identifies them as Israelite women.", "Not in the Talmud."], look_again=4),
  text("Exodus 2:1-3"),
  text("Exodus 2:5-6"),
  term(S("Exodus 2:5-6", 20, 22), "\"She took pity on it\" (2:6). Pharaoh's own daughter hears a Hebrew baby crying and chooses **compassion over her father's decree**.", TN("Exodus 2:6")),
  concept("Why did she go down to the river?", "Rabbi Yochanan, in the name of Rabbi Shimon bar Yochai: she went down to cleanse herself **from her father's idols**. Her bathing was an **immersion**, the first step of joining the people. Her maidens protested that a king's own household should obey his decree. She saved the child anyway.", R("Sotah 12b")),
  chk("q2", "daughter", "why", "According to Sotah 12b, why did Pharaoh's daughter go down to the river?", ["To cleanse herself of her father's idols", "To look for the baby", "To worship the Nile"],
      "Her bath becomes an **immersion**: she was already turning from her father's world.", ["She found the basket by chance; the Talmud reads her purpose differently.", "The Talmud says the opposite: she left idolatry."], look_again=9),
  text("Exodus 2:10"),
  term(S("Exodus 2:10", 10, 13), "\"I drew him out of the water\" (2:10). The name **Moses** comes from an Egyptian princess.", TN("Exodus 2:10")),
  {"kind": "reflect", "prompt": "Two midwives, a mother, a sister, and Pharaoh's daughter: women save Moses before he can do anything. Who quietly made your own story possible?"},
  {"kind": "recap", "points": ["The midwives **feared God** and let the boys live.", "Sotah 11b: Shiphrah and Puah were **Jochebed and Miriam**.", "Sotah 12b: Pharaoh's daughter was leaving **her father's idols**.", "\"**I drew him out of the water**\": Moses."]}]}

X2 = {"id": "x-st-exo-02", "title": "Moses (2): The bush that was not consumed", "status": "draft", "related": [], "parashah": ["Shemot"],
 "check_note": "Shemot Rabbah 2:2, 2:5 (Sefaria Midrash Rabbah 2022) and Berakhot 9b read 11/11.",
 "cards": [
  {"kind": "hook", "title": "A shepherd in the wilderness", "body": "Moses has fled Egypt. Now he tends his father-in-law's sheep in Midian, far from his people, until something on the mountain **burns and does not burn up**.", "src": TN("Exodus 2:15; 3:1")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Why did God speak from a lowly thorn bush, according to one answer in the Midrash?", "choices": ["No place is empty of God's presence, even a bush", "There were no other trees", "To frighten Moses", "To test Moses' eyesight"], "answer": 0,
   "why": "Rabbi Yehoshua ben Korcha: **no place is empty of the Divine Presence**, even a bush."},
  concept("Tested with a flock", "The Midrash says God tested Moses **with sheep**. A young goat ran off, and Moses followed it until it stopped at a pool to drink. God said: you show such compassion to a flock that belongs to a human being, **you will shepherd My flock, Israel**.", R("Shemot Rabbah 2:2")),
  text("Exodus 3:1-5"),
  term(S("Exodus 3:1-5", 28, 31), "\"yet the bush was not consumed\" (3:2).", TN("Exodus 3:2")),
  concept("Why a thorn bush?", "The Midrash gives many answers. **Rabbi Yehoshua ben Korcha**: \"there is no place that is vacant of the Divine Presence, even a bush.\" **Rabbi Eliezer**: the bush is the lowliest of trees, as Israel was lowly in Egypt. And God speaks from the thorns to say, \"I am party to their suffering.\"", R("Shemot Rabbah 2:5")),
  chk("q1", "bush", "why", "Which is one answer the Midrash gives for why God spoke from a thorn bush?", ["God shares Israel's suffering, speaking from among the thorns", "Thorn bushes were sacred in Egypt", "Moses was afraid of tall trees"],
      "From the thorns, God says: \"**I am party to their suffering.**\"", ["The Midrash doesn't say so.", "The Midrash doesn't say so."], look_again=5),
  term(S("Exodus 3:1-5", 33, 35), "\"I must turn aside to look\" (3:3). Only **when God saw that he had turned aside** does God call his name (3:4).", TN("Exodus 3:3-4")),
  text("Exodus 3:13-14"),
  term(S("Exodus 3:13-14", 22, 25), "God's answer when Moses asks for a name (3:14). The Contemporary Torah leaves it in Hebrew; the Talmud's English renders it \"I will be that I will be.\"", R("Exodus 3:14; Berakhot 9b")),
  concept("I will be with them", "Why the doubled **ehyeh**? God told Moses: tell Israel I was with you in this enslavement, and **I will be with you** in enslavements to come. Moses answered: it is **enough for them to endure** what they suffer now. God agreed: tell them only, \"I will be has sent me.\"", R("Berakhot 9b")),
  chk("q2", "ehyeh", "why", "In Berakhot 9b, why does Moses ask God to shorten the message?", ["Their present suffering is already enough to bear", "The full name was too holy to say", "Pharaoh might overhear it"],
      "Moses protects the people: **today's suffering is enough** without news of future exile.", ["The Talmud's reason is the people's burden.", "The Talmud's reason is the people's burden."], look_again=10),
  {"kind": "reflect", "prompt": "The Midrash says no place is empty of God, even a thorn bush, and Moses sees it only because he turns aside. What might you see if you turned aside today?"},
  {"kind": "recap", "points": ["Moses was chosen for **compassion to a flock** (Shemot Rabbah 2:2).", "The bush **burned and was not consumed**.", "No place is empty of God, **even a bush** (Shemot Rabbah 2:5).", "**Ehyeh**: I will be with them (Berakhot 9b)."]}]}

X3 = {"id": "x-st-exo-03", "title": "Moses (3): A hardened heart", "status": "draft", "related": [], "parashah": ["Vaera"],
 "check_note": "Mishneh Torah, Repentance 6:3 (Touger) read 11/11.",
 "cards": [
  {"kind": "hook", "title": "Refused, again and again", "body": "Moses and Aaron ask Pharaoh to let the people go. Plague after plague falls, and Pharaoh refuses each time. But the Torah describes his refusal **in more than one way**.", "src": TN("Exodus 7-11")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "In the Torah, only God ever hardens Pharaoh's heart.", "answer": False,
   "why": "In the early plagues **Pharaoh hardens his own heart** (8:11). Only later does the Torah say God did it."},
  text("Exodus 7:3"),
  text("Exodus 8:11"),
  term(S("Exodus 8:11", 5, 7), "\"he became stubborn\" (8:11). In Hebrew, Pharaoh does this to **his own heart**: the relief comes, and he chooses not to listen.", TN("Exodus 8:11")),
  chk("q1", "own", "pick", "Who hardens Pharaoh's heart in 8:11?", ["Pharaoh himself", "God", "Moses"],
      "When the relief came, **Pharaoh** made his own heart heavy.", ["Not yet. That comes later (9:12).", "Moses only asks."], look_again=4),
  text("Exodus 9:12"),
  concept("Why would God harden a heart?", "**Maimonides** answers: Pharaoh \"began to sin on his own initiative,\" oppressing Israel in his land. Someone who sins **willfully and greatly** can reach a point where **the way back is held closed**. So God hardened his heart, and he could no longer repent.", R("Mishneh Torah, Repentance 6:3")),
  chk("q2", "heart", "why", "According to Maimonides, why did God harden Pharaoh's heart?", ["Pharaoh first chose evil freely, until the way back closed", "God planned for him to fail from the start", "Moses asked God to"],
      "Pharaoh's own choices came **first**; the hardening was their consequence.", ["Maimonides stresses that Pharaoh began on his own.", "Not in the text."], look_again=7),
  {"kind": "reflect", "prompt": "Pharaoh hardens his own heart before anything is done to it. Is there a refusal in your life that has gotten harder to undo the longer it has gone on?"},
  {"kind": "recap", "points": ["God foretells: **I will harden Pharaoh's heart** (7:3).", "At first **Pharaoh hardens his own heart** (8:11).", "Later **God stiffens it** (9:12).", "Maimonides: willful sin can **close the way back**."]}]}

X4 = {"id": "x-st-exo-04", "title": "Moses (4): At the Sea", "status": "draft", "related": ["prayer:mi_chamocha", "prayer:m_mi_chamocha"], "parashah": ["Beshalach"],
 "check_note": "Sotah 37a and Megillah 10b read 11/11. Friedman: see Genesis (1).",
 "cards": [
  {"kind": "hook", "title": "Trapped", "body": "The Israelites are free, and then trapped: Pharaoh's chariots behind them, **the sea in front**. They cry out to God, and Moses prays.", "src": TN("Exodus 14:10-14")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "According to Rabbi Yehuda in the Talmud, who went into the sea first?", "choices": ["Nahshon, prince of Judah", "Moses", "Aaron", "Miriam"], "answer": 0,
   "why": "Every tribe hung back, until **Nahshon ben Amminadab** jumped in."},
  text("Exodus 14:15-16"),
  term(S("Exodus 14:15-16", 3, 5), "\"Why do you cry out to Me?\" (14:15). God's answer to prayer is: \"Tell the Israelites to go forward.\"", TN("Exodus 14:15")),
  concept("Nahshon", "**Rabbi Yehuda**: no tribe wanted to go into the sea first. Then **Nahshon ben Amminadab**, prince of Judah, jumped in, his tribe after him. Meanwhile Moses kept praying at length, and God told him that **His beloved ones were drowning** while he prolonged his prayer: speak to the people, and lift your rod.", R("Sotah 37a")),
  chk("q1", "nahshon", "why", "In Sotah 37a, why does God interrupt Moses' long prayer?", ["The people were already in the water and needed action", "Moses was praying in the wrong place", "Prayer was forbidden at the Sea"],
      "Nahshon was already **drowning**; it was time to **lift the rod**, not lengthen the prayer.", ["The Talmud's point is urgency.", "The Talmud's point is urgency."], look_again=4),
  text("Exodus 14:21-22"),
  text("Exodus 15:11"),
  {"kind": "relevance", "body": "Every evening and every morning, after the Sh'ma and its blessings, we sing **Mi Chamocha**: these words from the shore of the Sea.", "links": ["prayer:mi_chamocha", "prayer:m_mi_chamocha"]},
  text("Exodus 15:20-21"),
  concept("When not to sing", "**Rabbi Yochanan**: that night, the angels wanted to sing. God stopped them: the Egyptians, **the work of My hands**, are drowning, and you would sing? The Talmud concludes that God **does not rejoice** over the downfall of the wicked.", R("Megillah 10b")),
  chk("q2", "song", "why", "In Megillah 10b, why did God stop the angels from singing?", ["The Egyptians, God's creatures too, were drowning", "Israel hadn't finished crossing", "Only Miriam was allowed to sing"],
      "**The work of My hands** were drowning: even a rescue is not a reason to rejoice in anyone's death.", ["Not the Talmud's reason.", "Not the Talmud's reason."], look_again=10),
  concept("God, openly", "At the Sea, God acts **openly**, for everyone to see. Biblical scholar **Richard Elliott Friedman** traces how this visible presence **fades** across the Bible, until in Esther God is never named. From here on, the people will have to do more of the acting themselves.", {"type": "scholarly", "ref": "Richard Elliott Friedman, The Hidden Face of God (1995)"}),
  {"kind": "reflect", "prompt": "Nahshon steps in before the sea splits; Miriam sings after it closes, and God remembers the drowned. Which is harder for you: stepping in before you're sure, or celebrating without forgetting the cost?"},
  {"kind": "recap", "points": ["\"**Why do you cry out to Me?**\" God says: go forward.", "**Nahshon** went in first (Sotah 37a).", "**Mi Chamocha** comes from the Sea (15:11).", "God **does not rejoice** at the drowning (Megillah 10b)."]}]}

X5 = {"id": "x-st-exo-05", "title": "Moses (5): At the foot of the mountain", "status": "draft", "related": [], "parashah": ["Yitro", "Mishpatim"],
 "check_note": "Shabbat 88a and Shemot Rabbah 29:9 read 11/11.",
 "cards": [
  {"kind": "hook", "title": "Sinai", "body": "Three months out of Egypt, the people camp at the mountain. Thunder, lightning, a cloud, and **the blast of a shofar**. Moses leads them out to meet God.", "src": TN("Exodus 19:16-19")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "According to the Talmud, Israel promised to do the commandments before promising to hear them.", "answer": True,
   "why": "They said \"**We will do**\" before \"**We will hear**,\" and the Talmud calls it the angels' secret."},
  text("Exodus 19:17"),
  term(S("Exodus 19:17", 6, 9), "\"they took their places at the foot of the mountain\" (19:17). The Hebrew can also be read as **under** the mountain, and the Talmud reads it that way.", TN("Exodus 19:17")),
  concept("A mountain held overhead", "**Rabbi Avdimi**: God held the mountain over them **like a tub**: accept the Torah, or this will be your burial. But a covenant accepted under force is weak. **Rava** answers: they **accepted it again, willingly**, in the days of Ahasuerus, as Esther says, \"The Jews ordained, and took upon them\" (Esther 9:27).", R("Shabbat 88a")),
  chk("q1", "tub", "why", "According to Rava in Shabbat 88a, when did Israel accept the Torah freely?", ["In the days of Ahasuerus, in the Purim story", "At the moment of the Ten Commandments", "When Moses died"],
      "At Sinai, under the mountain; in **Esther's** time, by choice. A people grown up enough to choose.", ["The Talmud reads Sinai as under compulsion.", "Not in this passage."], look_again=4),
  text("Exodus 20:2"),
  concept("Silence", "**Rabbi Abbahu** in the name of **Rabbi Yochanan**: when God gave the Torah, no bird sang, no ox lowed, the sea did not stir, the angels did not say \"Holy.\" The entire world was quiet and silent, and **the voice** went out: \"I am the Lord your God.\"", R("Shemot Rabbah 29:9")),
  text("Exodus 24:7"),
  term(S("Exodus 24:7", 10, 12), "Two Hebrew verbs, which the Contemporary Torah renders together as \"we will faithfully do\" (24:7). The Talmud's English hears them one at a time: \"We will do\" and \"We will hear.\"", R("Exodus 24:7; Shabbat 88a")),
  concept("The angels' secret", "**Rabbi Simai**: because Israel put \"We will do\" before \"We will hear,\" **600,000 angels** tied **two crowns** on each person, one for each promise. **Rabbi Elazar**: a heavenly voice asked, \"Who revealed to my children this secret that the ministering angels use?\" Angels **act first, then listen**.", R("Shabbat 88a")),
  chk("q2", "naaseh", "why", "Why does the Talmud call putting \"We will do\" before \"We will hear\" the angels' secret?", ["Angels act on God's word first, and understand after", "Angels never speak", "Only angels heard the Ten Commandments"],
      "Doing first, understanding after: **na'aseh v'nishma**.", ["Not the Talmud's point.", "Not the Talmud's point."], look_again=10),
  {"kind": "reflect", "prompt": "The people promise to do before they understand. Where in your practice has doing come before understanding, and what did the doing teach you?"},
  {"kind": "recap", "points": ["At **the foot of the mountain**, or under it (Shabbat 88a).", "Accepted again, **freely**, in Esther's time (Rava).", "The world fell **silent** for \"I am\" (Shemot Rabbah 29:9).", "**Na'aseh v'nishma**: the angels' secret."]}]}

X6 = {"id": "x-st-exo-06", "title": "Moses (6): V'shamru", "status": "draft", "related": ["prayer:vshamru"], "parashah": ["Ki Tisa"],
 "check_note": "Beitzah 16a read 11/11.",
 "cards": [
  {"kind": "hook", "title": "A pause in the building", "body": "God is giving Moses detailed plans for the **Tabernacle**. Then, before the work begins, the Torah stops for **Shabbat**.", "src": TN("Exodus 31:12-17")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "According to Resh Lakish, what does God give each person on Shabbat eve?", "choices": ["An additional soul", "A double portion of manna", "A new name", "A guardian angel"], "answer": 0,
   "why": "A **neshamah yeteirah**, an additional soul, taken back when Shabbat ends."},
  text("Exodus 31:16-17"),
  {"kind": "relevance", "body": "These are the words of **V'shamru**, which we sing on Shabbat.", "links": ["prayer:vshamru"]},
  term(S("Exodus 31:16-17", 23, 25), "\"[God] ceased from work and was refreshed\" (31:17). The last word, **vayinafash**, shares its root with **nefesh**, soul.", TN("Exodus 31:17")),
  concept("An additional soul", "**Resh Lakish**: God gives a person **an additional soul** on Shabbat eve and takes it back when Shabbat ends. He reads **vayinafash** as **vai, nefesh**: woe for the soul that is lost.", R("Beitzah 16a")),
  chk("q1", "neshamah", "why", "How does Resh Lakish read the word vayinafash?", ["As vai, nefesh: \"woe for the additional soul that is lost\" when Shabbat ends", "As a word for rest, and nothing more", "As a command to sleep"],
      "**Vai, nefesh**: the additional soul leaves as Shabbat goes out.", ["He finds more in the word.", "Not his reading."], look_again=5),
  {"kind": "reflect", "prompt": "Resh Lakish says Shabbat brings you an additional soul, and its leaving is felt. What in you feels larger on Shabbat?"},
  {"kind": "recap", "points": ["The Torah pauses the building **for Shabbat**.", "**V'shamru**: a sign between God and Israel (31:16-17).", "Beitzah 16a: **an additional soul** on Shabbat."]}]}

X7 = {"id": "x-st-exo-07", "title": "Moses (7): Broken tablets", "status": "draft", "related": [], "parashah": ["Ki Tisa"],
 "check_note": "Shabbat 87a and Berakhot 8b read 11/11.",
 "cards": [
  {"kind": "hook", "title": "Forty days", "body": "Moses has been on the mountain forty days. Below, the people lose hope and make **a golden calf**. Moses comes down carrying the tablets.", "src": TN("Exodus 32:1-19")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "According to the Talmud, what was kept in the Ark with the second tablets?", "choices": ["The broken pieces of the first tablets", "The golden calf's ashes", "Moses' staff", "Nothing else"], "answer": 0,
   "why": "**Both** the whole tablets and the **broken** ones (Berakhot 8b)."},
  text("Exodus 32:19"),
  concept("God agreed", "Moses did **three things on his own judgment**, and God agreed with him. One was **breaking the tablets**. His reasoning: if one who has turned from God may not eat even the Passover lamb, one mitzvah, how could a people worshipping a calf receive **the whole Torah**?", R("Shabbat 87a")),
  chk("q1", "agreed", "why", "In Shabbat 87a, how did God respond to Moses breaking the tablets?", ["God agreed with him", "God punished him", "God was silent"],
      "One of three things Moses did **on his own**, and God **agreed**.", ["The Talmud says the opposite.", "The Talmud says God agreed."], look_again=3),
  text("Exodus 34:1"),
  concept("Whole and broken, side by side", "**Both the whole tablets and the broken tablets** were placed in the Ark. So, says **Rabbi Yehoshua ben Levi**, honor an elder who has forgotten their learning through no fault of their own: like the broken tablets, they are still holy.", R("Berakhot 8b")),
  chk("q2", "broken", "why", "What lesson does Berakhot 8b draw from the broken tablets?", ["Honor an elder who has lost their learning; what is broken is still holy", "Broken things should be buried", "Never break a promise"],
      "The broken tablets stayed **in the Ark**, beside the whole ones.", ["The Talmud says they were kept, not buried.", "Not the Talmud's lesson here."], look_again=6),
  {"kind": "reflect", "prompt": "The broken tablets were kept in the Ark beside the whole ones. What broken piece do you carry, and does it still deserve a holy place?"},
  {"kind": "recap", "points": ["Moses **shattered** the tablets (32:19).", "Shabbat 87a: **God agreed** with him.", "Berakhot 8b: **whole and broken** together in the Ark."]}]}

X8 = {"id": "x-st-exo-08", "title": "Moses (8): Thirteen attributes", "status": "draft", "related": [], "parashah": ["Ki Tisa"],
 "check_note": "Rosh Hashanah 17b read 11/11. Liturgy card: CHECK with cantor where Mishkan HaNefesh and CBB use the Thirteen Attributes.",
 "cards": [
  {"kind": "hook", "title": "Show me", "body": "After the calf, Moses asks to see God's presence. God answers: you cannot see My face, but I will **pass before you** and proclaim My name.", "src": TN("Exodus 33:18-23")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "In the Talmud, God appears to Moses wrapped in a tallit, like a prayer leader.", "answer": True,
   "why": "Rabbi Yochanan: \"were it not explicitly written\" it would be impossible to say."},
  text("Exodus 34:6-7"),
  term(S("Exodus 34:6-7", 6, 12), "\"a God compassionate and gracious, slow to anger, abounding in kindness\" (34:6). The opening of the **Thirteen Attributes of Mercy**.", TN("Exodus 34:6")),
  concept("God in a tallit", "**Rabbi Yochanan**: were it not written, it would be impossible to say it. God **wrapped in a tallit like a prayer leader** and showed Moses the order of prayer: whenever Israel sins, let them recite **the thirteen attributes** before Me, and I will forgive them. **Rav Yehuda**: there is a covenant that they **never return empty-handed**.", R("Rosh Hashanah 17b")),
  chk("q1", "tallit", "why", "In Rosh Hashanah 17b, what did God teach Moses?", ["An order of prayer: recite the Thirteen Attributes when Israel sins", "How to build the Ark", "The melody for the shofar"],
      "God as **prayer leader**, teaching the words that bring forgiveness.", ["Not in this passage.", "Not in this passage."], look_again=4),
  concept("Truth, then kindness", "The verse says both \"abounding in **kindness**\" and \"**faithfulness**,\" which the Talmud reads as **truth**, strict justice. **Ilfa**: God begins with justice, but seeing that **the world cannot survive on judgment alone**, turns to kindness.", R("Rosh Hashanah 17b")),
  chk("q2", "kindness", "why", "According to Ilfa, why does kindness win out over strict justice?", ["The world could not survive on judgment alone", "Moses argued for it", "Justice is less important"],
      "Judgment first, then **mercy**, because without it the world could not stand.", ["Not Ilfa's reason.", "Ilfa keeps both."], look_again=6),
  concept("In the prayer book", "These words return in Jewish prayer on **festivals and the High Holy Days**, often as the Ark is opened.", {"type": "tradition", "ref": "Exodus 34:6-7 in festival and High Holy Day liturgy"}),
  {"kind": "reflect", "prompt": "In the Talmud, God gives Moses words to pray when the people have failed. When you have fallen short, what words help you begin again?"},
  {"kind": "recap", "points": ["God **passes before** Moses and proclaims (34:6-7).", "God in **a tallit**, teaching an order of prayer (Rosh Hashanah 17b).", "The Thirteen Attributes **never return empty**.", "Justice first, then **kindness**."]}]}

LS = (X1, X2, X3, X4, X5, X6, X7, X8)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "stories", "units": [{"id": "x-st-exodus", "title": "Exodus", "subtitle": "Moses, from the river to Sinai", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-stories_exodus.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
