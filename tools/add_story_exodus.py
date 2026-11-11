"""Write data/src/x-stories_exodus.json: the Exodus unit (x-st-exodus). Batch 1: lessons 01-04 (birth, bush, hardened heart, the Sea). Hebrew sliced by word index from sefaria-exodus.json."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for f in ("sefaria-exodus.json",) for s in json.load(open(os.path.join(ROOT, "data/src", f), encoding="utf-8"))["sources"]}
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

LS = (X1, X2, X3, X4)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "stories", "units": [{"id": "x-st-exodus", "title": "Exodus", "subtitle": "Moses, from the river to the Sea", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-stories_exodus.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
