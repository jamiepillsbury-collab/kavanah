"""Add/replace the Jacob, Rachel and Leah Explore lessons (x-st-gen-19..21) in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-rachel-leah.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-rachel-leah.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

TN = lambda ref: {"type": "tanakh", "ref": ref}
L19 = {"id": "x-st-gen-19", "title": "Jacob (4): Rachel, Leah and the switch", "parashah": ["Vayetzei"], "status": "draft", "related": ["prayer:avot"],
 "check_note": "My summaries of Rashi on Genesis 29:11 and 29:17, Megillah 13b (cited by Rashi on 29:25), read on Sefaria 11/09.",
 "cards": [
  {"kind": "hook", "title": "Love at the well", "body": "Like his mother Rebekah, Jacob's story turns at **a well**. He sees **Rachel**, rolls the heavy stone off the well by himself, waters her flock, **kisses her and weeps** (29:9-11).", "src": T("Genesis 29:9-11")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Why did Jacob weep when he met Rachel, in one of Rashi's readings?", "choices": ["He foresaw she would not be buried with him", "He was exhausted from the journey", "He missed his father", "He thought she was Leah"], "answer": 0,
   "why": "Rashi gives two reasons; one is that he foresaw **she would not be buried beside him** in Machpelah."},
  text("Genesis 29:9-11"),
  concept("Why he wept", "**Rashi** offers two answers. He foresaw that Rachel **would not be buried with him** in the cave of Machpelah. Or: he came **empty-handed**. His grandfather's servant had brought rings and bracelets for Rebekah; Jacob had nothing.", R("Rashi on Genesis 29:11", "from Bereshit Rabbah 70")),
  text("Genesis 29:16-18"),
  term(S("Genesis 29:16-18", 9, 12), "\"Leah had weak eyes\" (29:17). **Rashi**: tender **from weeping**. People said Rebekah had two sons and Laban two daughters, the older for the older; so Leah cried, afraid she would have to marry **Esau**.", R("Rashi on Genesis 29:17", "from Bereshit Rabbah 70:16")),
  term(S("Genesis 29:20", 5, 11), "Seven years of work, and \"they seemed to him but a few days because of his love for her\" (29:20).", T("Genesis 29:20")),
  chk("q1", "seven", "pick", "How did Jacob's seven years of work feel to him?", ["Like a few days", "Like forever", "Like a punishment"],
      "\"They seemed to him but **a few days** because of his love for her\" (29:20).", ["The verse says the opposite.", "The Torah ties the time to love, not punishment."], look_again=6),
  text("Genesis 29:23-26"),
  concept("Rachel's signs", "How could Jacob not know? The Talmud: Jacob and Rachel had agreed on **secret signs** so he would know her. When Laban planned the switch, Rachel thought her sister would be **put to shame**, and **gave Leah the signs**.", R("Megillah 13b", "cited by Rashi on Genesis 29:25")),
  chk("q2", "signs", "why", "In Megillah 13b, why did Rachel give Leah the secret signs?", ["So her sister would not be shamed", "Because she didn't want to marry Jacob", "Laban forced her to"],
      "Rachel chose **her sister's dignity** over her own wedding night.", ["The Talmud says she loved Jacob; she acted for Leah.", "The Talmud credits Rachel's own choice."], look_again=9),
  {"kind": "relevance", "body": "In the Amidah's first blessing you name both sisters: **Elohei Rachel v'Elohei Leah**, God of Rachel and God of Leah.", "links": ["prayer:avot"]},
  {"kind": "reflect", "prompt": "Laban says: \"It is not the practice in our place to marry off the younger before the older\" (29:26). Jacob once took his older brother's place. What do you make of the echo?"},
  {"kind": "recap", "points": ["Jacob meets Rachel **at a well**, and weeps (Rashi: two reasons).", "Leah's eyes were tender **from weeping** (Rashi 29:17).", "Seven years were **like a few days**.", "Rachel gave Leah **the signs**, to spare her shame (Megillah 13b).", "Both sisters are in the Amidah: **Elohei Rachel v'Elohei Leah**."]}]}

L20 = {"id": "x-st-gen-20", "title": "Jacob (5): Leah's thanks, Rachel's longing", "parashah": ["Vayetzei"], "status": "draft", "related": ["prayer:m_modim"],
 "check_note": "My summaries of Berakhot 7b and Rashi on Genesis 30:22, read on Sefaria 11/09. The root link odeh / Yehudah / Modim is a plain fact of Hebrew.",
 "cards": [
  {"kind": "hook", "title": "Two sisters, two kinds of pain", "body": "**Leah** has children but is **unloved**. **Rachel** is loved but has **no children** (29:31). The Torah tells both sides.", "src": T("Genesis 29:31")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "The Talmud says Leah was the first person ever to thank God.", "answer": True,
   "why": "**Berakhot 7b**: from the day God created the world, no one thanked God until Leah."},
  text("Genesis 29:31"),
  text("Genesis 29:35"),
  term(S("Genesis 29:35", 5, 8), "\"This time I will praise Adonai\" (29:35), and she names her fourth son **Yehudah**, Judah. **Berakhot 7b**: from the day the world was created, **no one thanked God until Leah**.", R("Berakhot 7b")),
  concept("One root, three words", "Leah's **odeh**, I will praise or thank, shares its root with **Yehudah**, Judah, the name behind the word **Jew**, and with **Modim** in the Amidah (\"We are thankful to You,\" in the Metsudah translation).", T("Genesis 29:35")),
  chk("q1", "leah-thanks", "why", "Why does Berakhot 7b single out Leah?", ["She was the first person to thank God", "She was the oldest of the matriarchs", "She named all twelve tribes"],
      "\"This time I will praise Adonai\": the Talmud calls it **the first thanks** since creation.", ["Age isn't the Talmud's point here.", "She named her own sons, not all twelve."], look_again=4),
  text("Genesis 30:1-2"),
  concept("Two cries", "Rachel: \"Give me children, or I shall die.\" Jacob, angry: \"Can I take the place of God, who has denied you fruit of the womb?\" (30:1-2). The Torah keeps **both** voices, the pain and the anger, without smoothing them over.", T("Genesis 30:1-2")),
  text("Genesis 30:22-24"),
  concept("God remembered Rachel", "**Rashi**: God remembered to Rachel's merit that she **gave her sister the signs**, and her fear that, being childless, she might be divorced and fall to **Esau**.", R("Rashi on Genesis 30:22")),
  chk("q2", "remembered", "why", "According to Rashi, what did God remember about Rachel?", ["That she gave Leah the signs", "That she was Jacob's favorite", "That she had prayed the longest"],
      "Her kindness to her sister, years before, is **remembered** now.", ["Rashi doesn't make favoritism the reason.", "Rashi names a different merit."], look_again=10),
  {"kind": "relevance", "body": "When you bow at **Modim**, \"We are thankful to You\" (Metsudah), you use **Leah's word**.", "links": ["prayer:m_modim"]},
  {"kind": "recap", "points": ["Leah unloved, Rachel childless: **two kinds of pain**.", "\"**This time I will praise Adonai**\": the first thanks (Berakhot 7b).", "Odeh, **Yehudah**, **Modim**: one root.", "Rachel's cry and Jacob's anger, both kept.", "God remembered Rachel's **kindness to her sister** (Rashi 30:22)."]}]}

L21 = {"id": "x-st-gen-21", "title": "Jacob (6): Rachel weeping for her children", "parashah": ["Vayishlach"], "status": "draft", "related": [],
 "check_note": "My summaries of Rashi on Genesis 48:7 and Megillah 31a, read on Sefaria 11/09. CBB's Rosh Hashanah haftarah not checked. Ben-oni left untranslated (the Contemporary Torah doesn't translate it).",
 "cards": [
  {"kind": "hook", "title": "A grave by the road", "body": "On the journey home, **Rachel dies giving birth** to her second son. Jacob buries her **by the road** to Ephrath, now Bethlehem, not in the family cave (35:16-20).", "src": T("Genesis 35:16-20")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Where does the Torah say Rachel was buried?", "choices": ["On the road to Ephrath, now Bethlehem", "In the cave of Machpelah", "In Haran", "In Beth-el"], "answer": 0,
   "why": "**On the road** (35:19), and Jacob set up a pillar over her grave."},
  text("Genesis 35:16-20"),
  term(S("Genesis 35:16-20", 28, 32), "Dying, Rachel names her son **Ben-oni**; his father calls him **Benjamin** (35:18).", T("Genesis 35:18")),
  concept("Why by the road?", "Years later Jacob explains to Joseph. **Rashi**: God told him to bury her there, so that when her children were **led into exile** along that road, Rachel would come out of her grave and **weep and plead** for them.", R("Rashi on Genesis 48:7")),
  chk("q1", "road", "why", "In Rashi's reading, why was Rachel buried on the road?", ["So she could weep for her children going into exile", "Because there was no time to reach Machpelah", "Because Laban demanded it"],
      "She would be **there, on their road**, to plead for them.", ["The verse itself gives no reason; Rashi gives God's.", "Laban has no part in this."], look_again=4),
  {**text("Jeremiah 31:15-16"), "src": TN("Jeremiah 31:15-16")},
  term(S("Jeremiah 31:15-16", 3, 12), "\"A cry is heard in Ramah... Rachel weeping for her children. She refuses to be comforted\" (Jeremiah 31:15). God doesn't scold her. God answers: \"Restrain your voice from weeping... They shall return from the enemy's land\" (31:16).", TN("Jeremiah 31:15-16")),
  chk("q2", "jeremiah", "pick", "In Jeremiah 31, how does God answer Rachel's weeping?", ["With a promise that her children will return", "By telling her to stop grieving", "By staying silent"],
      "\"**They shall return** from the enemy's land.\"", ["God says to restrain her tears, but because of the promise that follows.", "God answers her directly."], look_again=7),
  {"kind": "relevance", "body": "The Talmud has **Jeremiah 31**, the chapter with Rachel's weeping, as a **Rosh Hashanah haftarah** (Megillah 31a). Check what CBB reads.", "links": []},
  {"kind": "reflect", "prompt": "Rachel refuses to be comforted, and God answers with hope instead of correction. What does that say to you about grief? It's fine to skip this one."},
  {"kind": "recap", "points": ["Rachel dies **on the road**, giving birth to Benjamin.", "Rashi: buried there to **weep for her children** in exile.", "**A cry is heard in Ramah**: Rachel refuses comfort (Jeremiah 31:15).", "God's answer: **they shall return**.", "Jeremiah 31 is a **Rosh Hashanah** haftarah (Megillah 31a)."]}]}
for L in (L19, L20, L21):
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
ids = [L["id"] for L in (L19, L20, L21)]
u["lessons"] = [l for l in u["lessons"] if l["id"] not in ids] + [L19, L20, L21]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in (L19, L20, L21)])
