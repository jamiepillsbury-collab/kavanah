"""Write data/src/x-stories_hannah.json: the Hannah unit (x-st-hannah), 4 lessons (1 Samuel 1:1-2:10, the Rosh Hashanah haftarah). Hebrew sliced by word index from sefaria-hannah.json."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-hannah.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ").replace("&thinsp;", " ")
TN = lambda ref: {"type": "tanakh", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
def text(ref): return {"kind": "text", "sefaria": ref, "src": TN(ref)}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
S1 = "I Samuel 1"

H1 = {"id": "x-st-han-01", "title": "Hannah (1): A rival and a husband", "status": "draft", "related": [],
 "check_note": "Bava Batra 16a, Rosh Hashanah 11a, Megillah 31a read on Sefaria 11/12. English: JPS Tanakh Gender-Sensitive. CHECK: Mishkan HaNefesh / CBB read Hannah as the Rosh Hashanah haftarah (and on which day).",
 "cards": [
  {"kind": "hook", "title": "Year after year", "body": "Every year Elkanah and his family go up to **the House of GOD**. His wife Peninnah has children. His wife **Hannah** has none, and every year it hurts again.", "src": TN("I Samuel 1:1-7")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "In one view in the Talmud, Peninnah taunted Hannah for the sake of Heaven.", "answer": True,
   "why": "Rabbi Levi: she upset Hannah \"in order to motivate her to pray.\""},
  text("I Samuel 1:2"),
  term(S("I Samuel 1:2", 12, 15), "\"but Hannah was childless\" (1:2).", TN("I Samuel 1:2")),
  text("I Samuel 1:6-8"),
  term(S("I Samuel 1:6-8", 0, 5), "\"her rival, to make her miserable, would taunt her\" (1:6).", TN("I Samuel 1:6")),
  concept("For the sake of Heaven?", "**Rabbi Levi**: both Satan, who accused Job, and **Peninnah** acted for the sake of Heaven. Peninnah upset Hannah \"in order to motivate her to pray.\" The Talmud adds that when this was taught, Satan came and **kissed the teacher's feet** in gratitude.", R("Bava Batra 16a")),
  chk("q1", "peninnah", "why", "According to Rabbi Levi, why did Peninnah taunt Hannah?", ["To move her to pray", "To make Elkanah send her away", "Out of plain jealousy"],
      "Rabbi Levi reads even the taunting as aimed at **prayer**.", ["Not in the Talmud.", "Rabbi Levi reads her more generously."], look_again=6),
  term(S("I Samuel 1:6-8", 35, 41), "\"Am I not more devoted to you than ten sons?\" (1:8). Elkanah answers her grief with **his love**.", TN("I Samuel 1:8")),
  concept("Remembered on Rosh Hashanah", "The Talmud teaches that on Rosh Hashanah, **Sarah, Rachel and Hannah** were remembered by God and conceived sons. **Rabbi Elazar** links the word **remembered** in Hannah's story (1:19) to the Rosh Hashanah verse \"memorial proclaimed with the blast of a shofar\" (Leviticus 23:24).", R("Rosh Hashanah 11a")),
  chk("q2", "remembered", "pick", "Which women does the Talmud say were remembered on Rosh Hashanah?", ["Sarah, Rachel and Hannah", "Miriam, Deborah and Hannah", "Ruth, Esther and Hannah"],
      "Three women who waited for a child: **Sarah, Rachel and Hannah**.", ["Not this list.", "Not this list."], look_again=9),
  concept("Read on Rosh Hashanah", "So the Talmud names Hannah's story, **1 Samuel 1:1 to 2:10**, as a haftarah for Rosh Hashanah, because she too was blessed with a child on that day.", R("Megillah 31a")),
  {"kind": "reflect", "prompt": "Peninnah's taunts and Elkanah's love both miss what Hannah needs. When have you felt unseen by people close to you?"},
  {"kind": "recap", "points": ["Hannah has **no children**; Peninnah **taunts** her (1:2, 1:6).", "Rabbi Levi: Peninnah meant to **move her to pray**.", "\"**Am I not more devoted to you than ten sons?**\"", "Remembered on **Rosh Hashanah**, read on Rosh Hashanah."]}]}

H2 = {"id": "x-st-han-02", "title": "Hannah (2): Only her lips moved", "status": "draft", "related": ["prayer:avot"],
 "check_note": "Berakhot 31a-b and Zohar Vayigash 10:99 (Soncino) read on Sefaria 11/12.",
 "cards": [
  {"kind": "hook", "title": "The priest is watching", "body": "Hannah rises and prays before GOD. **Eli the priest** watches her mouth, and he gets it wrong.", "src": TN("I Samuel 1:9-13")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Which rule for the Amidah does the Talmud learn from Hannah?", "choices": ["Say the words with your lips, but quietly", "Pray only inside the Temple", "Pray aloud so others can answer amen", "Pray standing on one foot"], "answer": 0,
   "why": "Her lips moved, and **her voice could not be heard** (1:13)."},
  text("I Samuel 1:12-13"),
  term(S("I Samuel 1:12-13", 9, 19), "\"Hannah was praying in her heart; only her lips moved, but her voice could not be heard\" (1:13).", TN("I Samuel 1:13")),
  concept("Laws from one verse", "**Rav Hamnuna** draws laws of prayer from this verse. **In her heart**: focus your heart on your prayer. **Only her lips moved**: say the words with your lips, not only in your mind. **Her voice could not be heard**: do not raise your voice in the Amidah. **Eli thought she was drunk**: a drunk person may not pray.", R("Berakhot 31a")),
  chk("q1", "lips", "why", "What does Rav Hamnuna learn from \"only her lips moved\"?", ["Say the words with your lips, not only in your heart", "Pray as quickly as you can", "Never pray when you are sad"],
      "Prayer is **spoken**, even when it is silent.", ["Not in the Talmud.", "Hannah prays in great sorrow."], look_again=4),
  {"kind": "relevance", "body": "These are the rules for the **Amidah**, the standing prayer, which begins with **Avot**: said quietly, with the lips, and with the heart.", "links": ["prayer:avot"]},
  concept("The voice that cannot be heard", "The **Zohar** says true prayer is \"another voice attached to the voice which is heard.\" So a person should pray with the voice no one else hears, **like Hannah**, whose voice could not be heard.", R("Zohar, Vayigash 10:99")),
  text("I Samuel 1:15"),
  term(S("I Samuel 1:15", 12, 14), "\"I have been pouring out my heart to GOD\" (1:15).", TN("I Samuel 1:15")),
  concept("Not a master here", "On \"Oh no, my lord!\", one sage says Hannah was hinting: in this matter **you are not a master**, and the Divine Spirit is not on you, since you suspect me falsely. **Rabbi Elazar** learns two more rules: someone wrongly suspected should **say so** and clear her name, and someone who suspected wrongly must **make peace and bless**, as Eli does next.", R("Berakhot 31b")),
  text("I Samuel 1:17"),
  chk("q2", "eli", "why", "What does Rabbi Elazar learn from Eli's \"Then go in peace\"?", ["Whoever wrongly suspects someone must make peace and bless them", "Priests are never wrong", "Never pray in a public place"],
      "Eli was wrong, and he **blesses** her.", ["The Talmud says Eli was wrong here.", "Not the Talmud's lesson."], look_again=10),
  {"kind": "reflect", "prompt": "To the priest, Hannah's prayer looked like drunkenness. What does your most honest prayer look like from the outside?"},
  {"kind": "recap", "points": ["\"**Only her lips moved**, but her voice could not be heard\" (1:13).", "Rav Hamnuna: **heart, lips, quiet**, and never drunk.", "Zohar: the **voice no one hears**.", "Eli was wrong, so he **blesses** her (Berakhot 31b)."]}]}

H3 = {"id": "x-st-han-03", "title": "Hannah (3): God of Hosts", "status": "draft", "related": [],
 "check_note": "Berakhot 31b and Zohar Toldot 3:20 (Soncino) read on Sefaria 11/12. Rabbi's-teaching card: the connection is mine; check with Jamie.",
 "cards": [
  {"kind": "hook", "title": "A vow", "body": "Weeping, Hannah makes **a vow**: if God gives her a child, she will give the child back to God.", "src": TN("I Samuel 1:10-11")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "According to the Talmud, Hannah was the first person ever to call God \"Lord of Hosts.\"", "answer": True,
   "why": "Rabbi Elazar: no one, since Creation, until Hannah."},
  text("I Samuel 1:10-11"),
  term(S("I Samuel 1:10-11", 10, 12), "\"O GOD of Hosts\" (1:11).", TN("I Samuel 1:11")),
  concept("The first to say it", "**Rabbi Elazar**: from the day God created the world, no one called God **Lord of Hosts** until Hannah. Her argument: of all the hosts upon hosts You created, is it so hard for You to give me **one son**?", R("Berakhot 31b")),
  chk("q1", "tzevaot", "why", "In Berakhot 31b, why does Hannah call God \"Lord of Hosts\"?", ["Among all the hosts God made, one son should not be hard to give", "It was the Temple's usual name for God", "Eli taught it to her"],
      "**Hosts upon hosts**, and she asks for one child.", ["The Talmud says no one had used it before her.", "Not in the Talmud."], look_again=4),
  term(S("I Samuel 1:10-11", 3, 5), "\"she prayed to GOD\" (1:10). The Hebrew preposition here is unusual: **upon** or **onto** God, and the Talmud notices it.", TN("I Samuel 1:10")),
  concept("Speaking boldly upward", "**Rabbi Elazar**: \"Hannah spoke impertinently toward God on High,\" since the verse says she prayed **onto** God, not to God. He also reads her doubled \"if You will look\" as a dare: if You look now, good; if not, **You will see** anyway, and she tells God how she will hold God to the Torah's own promise.", R("Berakhot 31b")),
  concept("Above the stars", "The **Zohar** reads the same word another way: Hannah's prayer went **above** ordinary fate. Like Isaac's prayer for Rebekah, it rose \"above the planetary influences.\"", R("Zohar, Toldot 3:20")),
  chk("q2", "al", "why", "How does Rabbi Elazar read Hannah praying \"onto\" God?", ["She spoke boldly, even impertinently, toward Heaven", "She prayed on a rooftop", "She prayed on someone else's behalf"],
      "Hannah does not only plead; she **argues**.", ["Not the Talmud's reading.", "She prays for herself."], look_again=7),
  concept("A people growing up", "Your rabbi reads the Torah as a people **growing up**: from a child's hero-God, through a strained and complicated relationship, toward God present in our own choices. Hannah is a grown-up's prayer: no priest needed, her own words, even **arguing with God**. On the same page of Talmud, Rabbi Akiva says, \"The Torah spoke in the language of men.\"", {"type": "reform", "ref": "Teaching from Jamie's rabbi (oral, as Jamie retold it); Berakhot 31b", "note": "connection to Hannah is mine; check with Jamie"}),
  text("I Samuel 1:27-28"),
  term(S("I Samuel 1:27-28", 10, 14), "\"I, in turn, hereby lend him to GOD\" (1:28). **Asked** (שָׁאַלְתִּי, 1:27) and **lent** (הִשְׁאִלְתִּהוּ) come from the same root.", TN("I Samuel 1:27-28")),
  concept("For this boy I prayed", "The Talmud tells a story behind 1:25-27. Young **Samuel** ruled, correctly, that anyone may slaughter an offering, not only a priest. But he ruled **in front of his teacher**, Eli, who said that deserved death. Hannah cried out: \"I am the woman who stood here with you.\" Eli offered to pray for a greater son. She answered: for **this** boy I prayed, and I want no other.", R("Berakhot 31b")),
  {"kind": "reflect", "prompt": "Hannah bargains, dares, and argues with God, and the Talmud learns its rules of prayer from her. Is there something you would only say to God boldly?"},
  {"kind": "recap", "points": ["Hannah is the first to say **Lord of Hosts** (Berakhot 31b).", "She prays **onto** God: boldly, even impertinently.", "Zohar: her prayer rose **above fate**.", "Asked, then **lent** to GOD (1:27-28).", "For **this** boy she prayed (Berakhot 31b)."]}]}

H4 = {"id": "x-st-han-04", "title": "Hannah (4): My heart exults", "status": "draft", "related": ["prayer:gvurot"],
 "check_note": "Megillah 14a and Berakhot 29a read on Sefaria 11/12. CHECK: how Mishkan HaNefesh treats the nine-blessing Musaf (Reform practice may differ).",
 "cards": [
  {"kind": "hook", "title": "A song", "body": "Samuel is born, weaned, and brought to serve at the House of GOD. Then Hannah prays again, this time **a song**.", "src": TN("I Samuel 1:20-2:10")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "The Talmud links the nine blessings of the Rosh Hashanah Musaf Amidah to what?", "choices": ["The nine mentions of God's name in Hannah's prayer", "Nine months of pregnancy", "Nine shofar blasts", "Nine years Hannah waited"], "answer": 0,
   "why": "Rabbi Yitzchak of Kartignin, in Berakhot 29a."},
  text("I Samuel 2:1-2"),
  term(S("I Samuel 2:1-2", 6, 9), "\"I have triumphed through GOD\" (2:1). The Talmud reads the Hebrew image word by word: my **horn** is exalted.", R("I Samuel 2:1; Megillah 14a")),
  concept("A prophetess", "The Talmud counts **seven prophetesses**: Sarah, Miriam, Deborah, Hannah, Abigail, Huldah and Esther. Hannah's proof is the **horn**: she said my horn, not my pitcher. David and Solomon were anointed from a horn and their kingship lasted; Saul and Jehu were anointed from a pitcher and theirs did not. Hannah **foresaw** it.", R("Megillah 14a")),
  chk("q1", "horn", "why", "Why does Megillah 14a call Hannah a prophetess?", ["Her \"horn\" foresaw which anointed kings would last", "She heard angels in Shiloh", "Eli named her one"],
      "**Horn**, not pitcher: her song looks ahead to David.", ["Not in the Talmud.", "Eli misjudged her."], look_again=4),
  concept("No artist like our God", "On \"There is no rock like our God\" (2:2), the Talmud reads **rock** as **artist**. A person paints a form on a wall but cannot give it breath. God forms a child **inside its mother** and gives it breath and a soul. Fitting words from Hannah.", R("Megillah 14a")),
  text("I Samuel 2:6-8"),
  term(S("I Samuel 2:6-8", 0, 3), "\"GOD deals death and gives life\" (2:6).", TN("I Samuel 2:6")),
  {"kind": "relevance", "body": "Every Amidah's **G'vurot** praises God in the same words: מֶלֶךְ מֵמִית וּמְחַיֶּה.", "links": ["prayer:gvurot"]},
  concept("Nine blessings", "**Rabbi Yitzchak of Kartignin**: the nine blessings of the Rosh Hashanah Musaf prayer correspond to the **nine mentions of God's name** in Hannah's prayer. The reason: on Rosh Hashanah, Sarah, Rachel and **Hannah** were remembered.", R("Berakhot 29a")),
  chk("q2", "nine", "pick", "According to Berakhot 29a, why does Hannah's prayer shape the Rosh Hashanah Musaf?", ["She was remembered on Rosh Hashanah", "She wrote the Musaf prayer", "She prayed in the Temple on Yom Kippur"],
      "Remembered on Rosh Hashanah, so her prayer gives the day its **nine blessings**.", ["Not in the Talmud.", "Not in the Talmud."], look_again=10),
  term(S("I Samuel 2:6-8", 11, 17), "\"Raising the poor from the dust, Lifting up the needy from the dunghill\" (2:8). The song turns the world **upside down**, as Hannah's own life was turned.", TN("I Samuel 2:8")),
  {"kind": "reflect", "prompt": "Hannah's song is full of reversals: the poor raised, the mighty brought low. Where have you seen a reversal you once could not imagine?"},
  {"kind": "recap", "points": ["\"**My heart exults in GOD**\" (2:1).", "Megillah 14a: Hannah, **a prophetess**: horn, not pitcher.", "**No artist** like our God.", "\"**GOD deals death and gives life**\": the G'vurot.", "Berakhot 29a: **nine blessings** of Rosh Hashanah Musaf."]}]}

LS = (H1, H2, H3, H4)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "stories", "units": [{"id": "x-st-hannah", "title": "Hannah", "subtitle": "A woman's prayer, and the rules of prayer", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-stories_hannah.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
