"""Add/replace the Joseph Explore lessons (x-st-gen-24..28) in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-joseph.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-joseph.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

SC = lambda ref: {"type": "scholarly", "ref": ref}
L24 = {"id": "x-st-gen-24", "title": "Joseph (1): The tunic, the dreams and the pit", "parashah": ["Vayeshev"], "status": "draft", "related": [],
 "check_note": "My summaries of Rashi on Genesis 37:15, 37:24 and 37:35 (read on Sefaria 11/11). 'Coat of many colours' is the King James rendering.",
 "cards": [
  {"kind": "hook", "title": "The favorite son", "body": "\"Israel loved Joseph best of all his sons\" and gave him **an ornamented tunic**. His brothers **hated him**, and then Joseph told them **his dreams** (37:3-7).", "src": T("Genesis 37:3-7")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "\"The pit was empty; there was no water in it\" (37:24). According to Rashi, what was in it?", "choices": ["Snakes and scorpions", "Grain", "Water after all", "Nothing at all"], "answer": 0,
   "why": "Why add \"no water\" if it was empty? **Rashi**: no water, but **snakes and scorpions**."},
  text("Genesis 37:3-4"),
  term(S("Genesis 37:3-4", 9, 11), "\"an ornamented tunic\" (37:3). The rare Hebrew word for its decoration has been translated many ways; the King James Bible made it the famous \"coat of many colours.\"", SC("Genesis 37:3; King James Version")),
  text("Genesis 37:5-7"),
  concept("The man in the field", "On his way to his brothers, \"a man came upon him wandering in the fields\" (37:15). An ordinary stranger? **Rashi**: this was **the angel Gabriel**.", R("Rashi on Genesis 37:15", "from Bereshit Rabbah 84:14 and Tanchuma")),
  term(S("Genesis 37:15-17", 10, 13), "\"I am looking for my brothers\" (37:16): said by the boy his brothers hate, on his way to find them.", T("Genesis 37:16")),
  chk("q1", "gabriel", "why", "Who does Rashi say the \"man\" in the field was?", ["The angel Gabriel", "One of Joseph's brothers", "A local shepherd"],
      "**Gabriel**: a hidden messenger who keeps the story moving.", ["The brothers were already gone to Dothan.", "That's the plain reading; Rashi brings the midrash."], look_again=5),
  text("Genesis 37:23-24"),
  concept("Empty, but not empty", "\"The pit was **empty**; there was **no water** in it.\" Why say both? **Rashi**, from the Talmud: there was no water, but there were **snakes and scorpions**.", R("Rashi on Genesis 37:24", "from Shabbat 22a")),
  text("Genesis 37:34-35"),
  concept("He refused to be comforted", "Jacob mourns and **refuses to be comforted** (37:35). **Rashi**: no one can be comforted over someone **still alive** who is thought dead. It is decreed that the dead are slowly forgotten from the heart, but not the living. Joseph is alive.", R("Rashi on Genesis 37:35", "from Bereshit Rabbah 84:20")),
  chk("q2", "comfort", "why", "Why, in Rashi's reading, could Jacob not be comforted?", ["Joseph was still alive", "His sons didn't try", "He blamed himself for the tunic"],
      "Comfort comes for **the dead**, who fade from the heart. Joseph was **alive**.", ["\"All his sons and daughters sought to comfort him\" (37:35).", "Rashi gives a different reason."], look_again=11),
  {"kind": "recap", "points": ["A favorite son, **an ornamented tunic**, and dreams.", "Rashi: the man in the field was **Gabriel**.", "\"**I am looking for my brothers.**\"", "The pit: no water, but **snakes and scorpions** (Rashi).", "Jacob **refuses comfort**: Joseph is alive (Rashi 37:35)."]}]}

L25 = {"id": "x-st-gen-25", "title": "Joseph (3): Adonai was with Joseph", "parashah": ["Vayeshev"], "status": "draft", "related": [],
 "check_note": "My summaries of Rashi on Genesis 39:3 (from Tanchuma) and Sotah 36b (cited by Rashi on 39:11), read on Sefaria 11/11.",
 "cards": [
  {"kind": "hook", "title": "A slave in Egypt", "body": "Sold by his brothers, Joseph becomes a slave in the house of Potiphar, an Egyptian official. Yet the Torah says, \"Adonai was with Joseph\" (39:2).", "src": T("Genesis 39:1-2")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "Joseph's Egyptian master could tell that God was with him.", "answer": True,
   "why": "\"His master saw that Adonai was with him\" (39:3). Rashi explains **how** he could see it."},
  text("Genesis 39:2-3"),
  concept("God's name in his mouth", "How could an Egyptian **see** that God was with Joseph? **Rashi**: the name of God was **always on his lips**. God's presence showed in how Joseph spoke and acted.", R("Rashi on Genesis 39:3", "from Midrash Tanchuma, Vayeshev 8")),
  chk("q1", "name", "why", "According to Rashi, how did Potiphar see that God was with Joseph?", ["God's name was always on Joseph's lips", "Joseph performed miracles", "Joseph told him about his dreams"],
      "Not miracles: **Joseph's own speech** made God visible.", ["The Torah describes no miracles here.", "The dreams aren't part of Rashi's answer."], look_again=3),
  text("Genesis 39:8-9"),
  concept("His father's face", "Potiphar's wife tries again and again to seduce Joseph. The Talmud: at the moment of greatest temptation, **his father's image appeared to him in the window**, and reminded him of **his place among his brothers**. Joseph fled.", R("Sotah 36b", "cited by Rashi on Genesis 39:11")),
  chk("q2", "father", "why", "In Sotah 36b, what helped Joseph resist?", ["His father's image appeared to him", "A servant walked in", "He was afraid of Potiphar"],
      "**Jacob's face**, and the memory of who Joseph was meant to be.", ["The Talmud's answer is more inward than that.", "His own words (39:9) are about loyalty and sin, not fear."], look_again=6),
  text("Genesis 40:8"),
  term(S("Genesis 40:8", 10, 13), "\"Surely God can interpret!\" (40:8). In prison, Joseph gives the credit away before he even hears the dreams.", T("Genesis 40:8")),
  {"kind": "reflect", "prompt": "Joseph is a slave, then a prisoner, and still the Torah says God was with him. In this story, where does God's presence actually show up?"},
  {"kind": "recap", "points": ["\"**Adonai was with Joseph**,\" even as a slave.", "Rashi: God's name was **always on his lips**.", "Sotah 36b: **his father's face** in the window.", "\"**Surely God can interpret!**\""]}]}

L26 = {"id": "x-st-gen-26", "title": "Joseph (4): Pharaoh's dreams", "parashah": ["Miketz"], "status": "draft", "related": [],
 "check_note": "Torah text only, plus the custom of blessing children with Ephraim and Manasseh (Genesis 48:20).",
 "cards": [
  {"kind": "hook", "title": "From prison to palace", "body": "Pharaoh dreams of **seven fat cows and seven lean ones**, and no one can explain it. Joseph is brought **straight from prison** (41:1-15).", "src": T("Genesis 41:1-15")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Pharaoh says Joseph can interpret any dream. What does Joseph answer?", "choices": ["\"Not I! God will see to Pharaoh's welfare.\"", "\"Yes, it is my gift.\"", "\"Only if you free me.\"", "He says nothing."], "answer": 0,
   "why": "\"**Not I!**\" (41:16). Again Joseph points away from himself."},
  text("Genesis 41:15-16"),
  term(S("Genesis 41:15-16", 20, 25), "\"Not I! God will see to Pharaoh's welfare\" (41:16). Before he names God, Joseph answers in **a single Hebrew word**.", T("Genesis 41:16")),
  text("Genesis 41:51-52"),
  concept("Two names", "Joseph names his sons **Manasseh**, \"God has made me forget completely my hardship,\" and **Ephraim**, \"God has made me fertile in the land of my affliction\" (41:51-52). Jacob later blesses them, and Jewish parents still bless their sons on Friday night to be like **Ephraim and Manasseh** (48:20).", {"type": "tradition", "ref": "Genesis 41:51-52, 48:20"}),
  chk("q1", "names", "pick", "What does the name Ephraim say?", ["God made me fertile in the land of my affliction", "God made me forget my father's house", "God made me ruler over Egypt"],
      "**Ephraim**: fruitful **in the land of affliction** (41:52).", ["That's Manasseh's name.", "Neither name says that."], look_again=5),
  {"kind": "reflect", "prompt": "Ephraim: \"fertile in the land of my affliction.\" Has anything grown for you in a hard place? It's fine to skip this one."},
  {"kind": "recap", "points": ["Joseph goes **from prison to Pharaoh**.", "\"**Not I!** God will see to Pharaoh's welfare.\"", "**Manasseh** and **Ephraim**: forgetting hardship, and growing in it.", "Children are still blessed **to be like Ephraim and Manasseh**."]}]}

L27 = {"id": "x-st-gen-27", "title": "Joseph (5): The brothers and Judah", "parashah": ["Miketz", "Vayigash"], "status": "draft", "related": [],
 "check_note": "Rambam, Mishneh Torah, Repentance 2:1 (Touger translation on Sefaria), read 11/11. The observation that Genesis 37 records no plea from Joseph is from the text itself.",
 "cards": [
  {"kind": "hook", "title": "Bowing to a stranger", "body": "Famine drives Joseph's brothers to Egypt. They **bow** to the governor, as in Joseph's dream. Joseph recognizes them; **they do not recognize him** (42:6-8).", "src": T("Genesis 42:6-8")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "When the brothers come to Egypt, they recognize Joseph.", "answer": False,
   "why": "Joseph **recognized them**, but **they did not recognize him** (42:8)."},
  text("Genesis 42:21"),
  concept("We looked on at his anguish", "Years later, the brothers say they **watched his anguish** and ignored him **as he pleaded** (42:21). Chapter 37 never mentions Joseph pleading. We hear his cry only now, **through their guilt**.", T("Genesis 37:23-28, 42:21")),
  chk("q1", "guilt", "why", "What do we first learn in 42:21 that chapter 37 didn't tell us?", ["Joseph pleaded with his brothers from the pit", "Joseph had a third dream", "Reuben sold Joseph"],
      "The plea is told **only in memory**, when the brothers' guilt surfaces.", ["There's no third dream.", "Reuben wanted to save him (37:22)."], look_again=3),
  text("Genesis 44:33-34"),
  concept("Complete teshuvah", "Long ago, **Judah** proposed selling Joseph (37:26-27). Now Joseph tests them with Benjamin, Rachel's other son, and Judah offers to **stay as a slave in his place** (44:33). **Rambam**: complete teshuvah is when you face **the same situation** again and choose differently, not out of fear or weakness.", R("Mishneh Torah, Repentance 2:1")),
  chk("q2", "teshuvah", "why", "Why is Judah's offer a model of complete teshuvah, in Rambam's terms?", ["He faces the same situation and chooses differently", "He apologizes in words", "He gives a large gift"],
      "Same test, a brother at risk, and **this time he protects him**.", ["Rambam asks for more than words.", "Gifts aren't the measure here."], look_again=6),
  {"kind": "recap", "points": ["The brothers **bow**, and don't recognize Joseph.", "Joseph's plea from the pit is heard **only in their guilt** (42:21).", "**Judah** offers himself for Benjamin.", "Rambam: complete teshuvah is choosing differently **in the same situation**."]}]}

L28 = {"id": "x-st-gen-28", "title": "Joseph (6): I am Joseph", "parashah": ["Vayigash", "Vayechi"], "status": "draft", "related": [],
 "check_note": "My summaries of Bereshit Rabbah 93:10 and Zohar, Miketz 11:182 (Soncino translation on Sefaria), read 11/11.",
 "cards": [
  {"kind": "hook", "title": "He could no longer hold back", "body": "Judah's plea breaks Joseph open. He sends everyone else out and says: \"I am Joseph. Is my father still well?\" (45:1-3).", "src": T("Genesis 45:1-3")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "After \"I am Joseph,\" what does Joseph ask first?", "choices": ["\"Is my father still well?\"", "\"Why did you sell me?\"", "\"Where is Benjamin?\"", "\"Do you remember my dreams?\""], "answer": 0,
   "why": "His first question is about **his father** (45:3)."},
  text("Genesis 45:3-5"),
  concept("The day of rebuke", "\"His brothers could not answer him.\" **Abba Kohen Bardela**: woe to us on **the day of rebuke**. Joseph was the youngest, and his brothers **could not withstand his rebuke**. How much more, when **God** comes to rebuke each person **according to who they are**.", R("Bereshit Rabbah 93:10")),
  chk("q1", "rebuke", "why", "What does Abba Kohen Bardela learn from the brothers' silence?", ["If they couldn't face Joseph, how much harder to face God's judgment", "The brothers had forgotten Hebrew", "Joseph spoke too softly"],
      "\"I am Joseph\" was rebuke enough. **The day of judgment** will be harder.", ["The midrash isn't about language.", "The midrash reads the silence as shame, not mishearing."], look_again=3),
  text("Genesis 50:19-20"),
  term(S("Genesis 50:19-20", 8, 15), "\"although you intended me harm, God intended it for good\" (50:20). After Jacob dies, the brothers fear revenge. Joseph answers: \"Have no fear! Am I a substitute for God?\"", T("Genesis 50:19-20")),
  concept("Not repaying evil", "The **Zohar** holds up \"Joseph the righteous\" as the model of one who **does not repay evil**: when his brothers fell into his hands, he told himself, \"wait for the Lord, and he will save thee\" (Proverbs 20:22).", {"type": "kabbalah", "ref": "Zohar, Miketz 11:182"}),
  chk("q2", "zohar", "why", "Why does the Zohar call Joseph \"the righteous\" here?", ["He had his brothers in his power and did not repay evil", "He interpreted dreams", "He became ruler of Egypt"],
      "Power over those who hurt him, and **he chose not to use it**.", ["The Zohar's point here is restraint, not dreams.", "Power alone isn't righteousness; how he used it is."], look_again=7),
  {"kind": "reflect", "prompt": "Joseph says God meant it for good, but it's Joseph who chooses to forgive. Where do you see God in that choice?"},
  {"kind": "recap", "points": ["\"**I am Joseph.** Is my father still well?\"", "Bereshit Rabbah 93:10: **the day of rebuke**.", "\"You intended me harm, **God intended it for good**.\"", "Zohar: Joseph the righteous **did not repay evil**."]}]}
LS = (L24, L25, L26, L27, L28)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
ids = [L["id"] for L in LS]
u["lessons"] = [l for l in u["lessons"] if l["id"] not in ids] + list(LS)
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
