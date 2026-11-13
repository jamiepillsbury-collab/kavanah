"""Write data/src/x-kabbalah.json: Kabbalah track, unit 1 "Foundations" (x-kb-foundations), 4 lessons: Ein Sof, tzimtzum, the ten sefirot, Shechinah/broken vessels/tikkun.
Kabbalistic English from Sefaria (Etz Chaim, Sefer Yetzirah, Pardes Rimonim: Sefaria Community Translation; Tikkunei Zohar: David Solomon 2024). Bible text sliced from sefaria-kabbalah1.json. Scholarly history (Scholem) is cited from memory and flagged, per Jamie 11/13."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-kabbalah1.json"), encoding="utf-8"))["sources"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ").replace("&thinsp;", " ")
TN = lambda ref: {"type": "tanakh", "ref": ref}
def K(ref, note=None):  # "Ref (translator)" -> ref + note, so the Sefaria link works
    import re
    m = re.match(r"^(.*?) \((.*)\)$", ref)
    if m and not note: ref, note = m.group(1), m.group(2)
    return {"type": "kabbalah", "ref": ref, **({"note": note} if note else {})}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
SCH = lambda ref: {"type": "scholarly", "ref": ref, "note": "from memory, not on Sefaria; check"}
def text(ref): return {"kind": "text", "sefaria": ref, "src": TN(ref)}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
ETZ = "Etz Chaim 1:2 (Sefaria Community Translation)"

Q1 = {"id": "x-kb-01", "title": "Ein Sof: Without end", "status": "draft", "related": [],
 "check_note": "Etz Chaim 1:1 (Community Translation) and Tikkunei Zohar 17a (Solomon 2024) read on Sefaria 11/13. Scholem card from memory: check.",
 "cards": [
  {"kind": "hook", "title": "Beyond every name", "body": "**Kabbalah**, Jewish mysticism, starts with a God beyond anything we can picture or name. Kabbalists call this **Ein Sof**: without end.", "src": K("Etz Chaim 1:1 (Sefaria Community Translation)")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "In Kabbalah, Ein Sof can be fully understood through careful thought.", "answer": False,
   "why": "Etz Chaim: Ein Sof cannot be grasped \"neither by thought nor by reflection.\""},
  concept("Without end", "Isaac Luria's teaching, as written down in **Etz Chaim**, begins with the highest light, **Ein Sof**: \"it cannot be grasped in any way, neither by thought nor by reflection.\" It has **no beginning and no end**, and comes before everything that was ever created.", K("Etz Chaim 1:1 (Sefaria Community Translation)")),
  concept("One, but not in number", "A famous kabbalistic prayer opens with Elijah speaking: **Master of the Worlds**, You are One, but not one the way a number is one. You are high above all, hidden beyond all that is hidden: \"no thought apprehends You at all.\"", K("Tikkunei Zohar 17a (trans. David Solomon, 2024)")),
  chk("q1", "one", "pick", "In Tikkunei Zohar 17a, what can no thought do?", ["Grasp God", "Count the stars", "Reach the angels"],
      "God is **beyond thought**: One, but not a number among numbers.", ["Not the text's point.", "Not the text's point."], look_again=3),
  text("Isaiah 6:3"),
  term(S("Isaiah 6:3", 8, 11), "\"Whose presence fills all the earth!\" (6:3). Etz Chaim says the same of the light of Ein Sof: before creation, it **filled all of existence**.", K("Isaiah 6:3; Etz Chaim 1:2")),
  concept("Where Kabbalah comes from", "The **Zohar** presents itself as the teachings of **Rabbi Shimon bar Yochai** and his companions (2nd century). The scholar **Gershom Scholem** argued it was written in 13th-century **Spain**, largely by **Moses de León**. Three centuries later, **Isaac Luria** taught in Safed; his student **Chaim Vital** recorded his teaching in **Etz Chaim**.", SCH("Gershom Scholem, Major Trends in Jewish Mysticism (1941)")),
  chk("q2", "zohar", "pick", "Which scholar argued that the Zohar was written in 13th-century Spain?", ["Gershom Scholem", "Rashi", "Maimonides"],
      "**Scholem**, the founder of the modern study of Kabbalah.", ["Rashi lived before the Zohar appeared.", "Maimonides died before the Zohar appeared."], look_again=7),
  concept("A God beyond pictures", "Your rabbi reads the Torah as a people **growing up**: from a child's picture of God as a hero, toward a God found in our choices. Kabbalah's **Ein Sof** pushes the same way: every picture of God is too small, so the old pictures have to be let go.", {"type": "reform", "ref": "Teaching from Jamie's rabbi (oral, as Jamie retold it); Etz Chaim 1:1", "note": "connection to Kabbalah is mine; check with Jamie"}),
  {"kind": "reflect", "prompt": "Ein Sof is beyond every name and picture. Which picture of God from childhood have you outgrown, and what, if anything, took its place?"},
  {"kind": "recap", "points": ["**Ein Sof**: without end, beyond thought (Etz Chaim).", "One, **but not in number** (Tikkunei Zohar).", "Ein Sof's light **filled all of existence**.", "Zohar: attributed to Shimon bar Yochai; Scholem: **13th-century Spain**."]}]}

Q2 = {"id": "x-kb-02", "title": "Tzimtzum: Making room", "status": "draft", "related": [],
 "check_note": "Etz Chaim 1:2 (Community Translation) read on Sefaria 11/13.",
 "cards": [
  {"kind": "hook", "title": "Where is there room?", "body": "If God's light fills everything, where is there room for **a world**? Isaac Luria's answer is one of Kabbalah's boldest ideas.", "src": K(ETZ)},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "In Luria's teaching, what did Ein Sof do first to make room for the worlds?", "choices": ["Contracted itself, leaving an empty space", "Spoke ten words", "Built a palace of light", "Split into two"], "answer": 0,
   "why": "**Tzimtzum**: contraction."},
  concept("A light that filled everything", "Before anything was created, \"there was a simple supernal light that filled all of existence.\" There was **no empty space** at all: only one equal light without beginning or end, the light of Ein Sof.", K(ETZ)),
  concept("Contraction", "When God willed to create, God **contracted** at the center point. The light withdrew to the sides, and an **empty space** was left, perfectly round, equal on every side. Kabbalists call this **tzimtzum**.", K(ETZ)),
  chk("q1", "tzimtzum", "pick", "What is tzimtzum?", ["God's contraction, leaving room for creation", "A kind of prayer shawl", "The breaking of the tablets"],
      "God **withdraws**, so something else can be.", ["Not this.", "Not this."], look_again=3),
  concept("A line of light", "Into the empty space, a single **straight line** of light reaches down from Ein Sof, \"like a thin tube.\" Through it, light reaches the worlds. It cannot pour in from every side: then everything would melt back into **the light of Ein Sof**, as it was at first.", K(ETZ)),
  chk("q2", "kav", "why", "In Etz Chaim, why does light enter the empty space by one thin line, not from every side?", ["Otherwise the worlds would dissolve back into Ein Sof", "The space was too small", "Light can only travel in lines"],
      "Too much light, and **there would be no world**.", ["Not the text's reason.", "Not the text's reason."], look_again=5),
  concept("Why create at all?", "Etz Chaim gives a reason: God wanted to be known as **merciful and gracious**. But if no one exists to receive mercy, \"how can He be called merciful?\" Creation makes room for **someone to receive kindness**.", K(ETZ)),
  chk("q3", "why", "pick", "According to Etz Chaim, why did God create the worlds?", ["So there would be someone to receive God's mercy", "Because God was lonely", "To defeat the angels"],
      "Mercy needs **someone to receive it**.", ["Not the text's reason.", "Not the text's reason."], look_again=7),
  {"kind": "reflect", "prompt": "Tzimtzum is God stepping back so that something else can exist. Where might you need to step back to make room for someone?"},
  {"kind": "recap", "points": ["First, light **filled all of existence**.", "**Tzimtzum**: contraction, leaving an empty space.", "A thin **line of light** reaches the worlds.", "Why? So **mercy** has someone to receive it."]}]}

Q3 = {"id": "x-kb-03", "title": "The ten sefirot", "status": "draft", "related": ["prayer:t_lcha"],
 "check_note": "Sefer Yetzirah 1:4, Pardes Rimonim 1:1 (Community Translation), Tikkunei Zohar 17a, Etz Chaim 1:2 read on Sefaria 11/13. Full list of ten names from memory: check.",
 "cards": [
  {"kind": "hook", "title": "How the hidden is known", "body": "If Ein Sof is beyond all thought, how is God known at all? Kabbalah answers: through **ten sefirot**, ten ways God's light reaches the world.", "src": K("Tikkunei Zohar 17a (trans. David Solomon, 2024)")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "Sefer Yetzirah insists there are exactly ten sefirot.", "answer": True,
   "why": "\"Ten and not nine, ten and not eleven.\""},
  concept("Ten and not nine", "The ancient **Sefer Yetzirah**, the Book of Formation, says: \"Ten and not nine, ten and not eleven.\" Centuries later **Moses Cordovero** writes that all who study this wisdom agree the number is **ten**, and notes that Sefer Yetzirah is traditionally attributed to **Abraham**.", K("Sefer Yetzirah 1:4; Pardes Rimonim 1:1 (Sefaria Community Translation)")),
  concept("Constructs to direct worlds", "In the prayer of Elijah: You produced ten constructs, which we call **the ten sefirot**, to guide hidden worlds and revealed ones. You **bind and unite** them, and because You are within them, whoever separates one from another is as though they separated **You**.", K("Tikkunei Zohar 17a (trans. David Solomon, 2024)")),
  chk("q1", "unity", "why", "In Tikkunei Zohar 17a, why must the ten sefirot not be separated?", ["God is within them, so splitting them splits God's unity", "They would fall from heaven", "There would be only nine"],
      "Ten qualities, **one God**.", ["Not the text's reason.", "Not the text's reason."], look_again=3),
  text("I Chronicles 29:11"),
  term(S("I Chronicles 29:11", 2, 7), "\"greatness, might, splendor, triumph, and majesty\" (29:11). Kabbalists use these words as names of sefirot; Etz Chaim names **Gevurah, Tiferet, Netzach and Hod**.", K("I Chronicles 29:11; Etz Chaim 1:2")),
  {"kind": "relevance", "body": "These are the words of **L'cha Adonai**, sung as the Torah is carried back to the Ark.", "links": ["prayer:t_lcha"]},
  concept("The ten", "The usual list, from top to bottom: **Keter** (crown), **Chochmah** (wisdom), **Binah** (understanding), **Chesed** (kindness), **Gevurah** (strength), **Tiferet** (beauty), **Netzach** (endurance), **Hod** (splendor), **Yesod** (foundation), **Malchut** (kingship, also called **Shechinah**). Etz Chaim shows them in **three lines**, right, left and center.", SCH("Standard kabbalistic list; Gershom Scholem, Kabbalah (1974); Etz Chaim 1:2 for the three lines")),
  chk("q2", "lcha", "pick", "Which verse, sung at the Torah service, gives several sefirot their names?", ["1 Chronicles 29:11", "Genesis 1:1", "Psalm 23:1"],
      "**L'cha Adonai hag'dulah**: greatness, might, splendor...", ["Not this verse.", "Not this verse."], look_again=5),
  {"kind": "reflect", "prompt": "Tikkunei Zohar warns against separating the sefirot, like kindness from strength. Which two of your own qualities do you find hardest to hold together?"},
  {"kind": "recap", "points": ["\"**Ten and not nine**, ten and not eleven\" (Sefer Yetzirah).", "Ten constructs, **bound in one** (Tikkunei Zohar).", "Names from **1 Chronicles 29:11**: sung in L'cha Adonai.", "Keter to Malchut, in **three lines**."]}]}

Q4 = {"id": "x-kb-04", "title": "Shechinah, broken vessels, and repair", "status": "draft", "related": [],
 "check_note": "Megillah 29a, Mishnah Gittin 4:2 and Etz Chaim 9:2 read on Sefaria 11/13. Broken-vessels summary and modern use of tikkun olam from memory (Scholem): check. Aleinu wording: CHECK Mishkan T'filah.",
 "cards": [
  {"kind": "hook", "title": "God in exile", "body": "Kabbalah speaks of the **Shechinah**, God's presence dwelling in the world, as close to us, and sometimes in exile with us.", "src": R("Megillah 29a")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "In the Talmud, the Divine Presence went into exile with Israel.", "answer": True,
   "why": "Rabbi Shimon bar Yochai, in Megillah 29a."},
  concept("The Shechinah went with them", "**Rabbi Shimon bar Yochai**: see how beloved Israel is. Wherever they were exiled, **the Divine Presence went with them**: to Egypt, to Babylonia. And when they are redeemed, the Divine Presence will return **with them**.", R("Megillah 29a")),
  chk("q1", "exile", "why", "According to Megillah 29a, where was the Divine Presence when Israel was exiled?", ["In exile with them", "Left behind in Jerusalem", "Gone up to heaven"],
      "God **goes into exile** with the people.", ["The Talmud says the Presence went with them.", "Not this teaching."], look_again=2),
  concept("Broken vessels", "Luria taught that the first vessels made to hold God's light **could not hold it**, and broke. Etz Chaim describes \"seven kings\" who descended, and from what was left of them the **klipot**, husks, were formed, with **lights** still caught inside. As scholars summarize it, every good act **frees a spark** and helps repair what broke.", SCH("Etz Chaim 9:2 (Sefaria Community Translation); Gershom Scholem, Major Trends in Jewish Mysticism (1941)")),
  chk("q2", "sparks", "pick", "In Luria's picture, what is caught inside the husks (klipot)?", ["Light from the broken vessels", "The tablets of Sinai", "The souls of angels"],
      "**Sparks of light**, waiting to be raised.", ["Not in this teaching.", "Not in this teaching."], look_again=4),
  concept("For the betterment of the world", "The phrase **tikkun olam** is old. In the Mishnah, **Rabban Gamliel the Elder** makes rules about divorce documents \"for the betterment of the world\": legal fixes that keep society **fair and working**.", R("Mishnah Gittin 4:2")),
  concept("Tikkun olam today", "Many prayer books' **Aleinu** hopes to **repair the world** under God's sovereignty. Kabbalah gave the idea a cosmic meaning, and modern Reform Judaism made **tikkun olam** a call to **social justice**: repair, one act at a time.", {"type": "reform", "ref": "Aleinu (second paragraph); Reform usage of tikkun olam", "note": "CHECK: Mishkan T'filah Aleinu wording; history from memory"}),
  chk("q3", "tikkun", "pick", "In the Mishnah, what does \"for the betterment of the world\" refer to?", ["Practical rules that keep society fair", "Raising mystical sparks", "Building the Temple"],
      "Tikkun olam begins as **law** for a fair society.", ["That meaning comes later, from Kabbalah.", "Not in this Mishnah."], look_again=6),
  {"kind": "reflect", "prompt": "Luria pictures a broken world with light hidden in every piece. Where have you found light inside something broken?"},
  {"kind": "recap", "points": ["Megillah 29a: **the Shechinah goes into exile** with Israel.", "Luria: **vessels broke**; sparks are caught in husks.", "Mishnah Gittin: tikkun olam as **fair law**.", "Today: **repair**, one act at a time."]}]}

LS = (Q1, Q2, Q3, Q4)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "kabbalah", "units": [{"id": "x-kb-foundations", "title": "Foundations", "subtitle": "Ein Sof, tzimtzum, the sefirot, and repair", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-kabbalah.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
