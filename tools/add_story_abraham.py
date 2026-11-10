"""Add/replace the Abraham and Sarah Explore lessons (x-st-gen-10, -11) in data/src/x-stories.json.
Term Hebrew is sliced by word index from data/src/sefaria-abraham.json (never typed). Then run build_explore.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-abraham.json"), encoding="utf-8"))["sources"]}
def S(ref, line, a, b): return " ".join(SRC[(ref, "he")][line].split()[a:b]).replace("יְהֹוָה", "יְיָ")
def text(ref): return {"kind": "text", "sefaria": ref}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
T = lambda ref: {"type": "torah", "ref": ref}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}

L10 = {"id": "x-st-gen-10", "title": "Abraham and Sarah (1): Go forth", "parashah": ["Lech Lecha"], "status": "draft", "related": ["prayer:avot"],
 "check_note": "My summaries of Rashi on Genesis 12:1 and 12:5, Bereshit Rabbah 39:1, Berakhot 13a and Pesachim 117b (all read on Sefaria 11/09). Building 'lit up' vs 'on fire': translations differ.",
 "cards": [
  {"kind": "hook", "title": "Go, without a map", "body": "God's first words to **Abram** are a command: **leave** your land, your birthplace and your father's house, for \"the land that **I will show you**\" (12:1). No destination is named.", "src": T("Genesis 12:1")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "Why does the Torah say God chose Abram?", "choices": ["It never says", "He won an argument with his father", "He was the oldest son", "He had built an altar"], "answer": 0,
   "why": "The Torah **gives no reason**. The midrash fills the gap, as you'll see."},
  text("Genesis 12:1-3"),
  term(S("Genesis 12:1-3", 0, 3, 4), "Literally \"go, to you.\" Why the extra word? **Rashi**: go **for your own benefit and your own good**.", R("Rashi on Genesis 12:1")),
  term(S("Genesis 12:1-3", 1, 6, 8), "\"and you shall be a blessing\" (12:2). Not only blessed: **a blessing for others**. The next verse widens it to all the families of the earth.", T("Genesis 12:2-3")),
  concept("The lit-up building", "**Rabbi Yitzchak**'s parable: a traveler sees a building **lit up** (some translate: on fire) and wonders, does this place have **no one in charge**? The owner looks out: **I am the owner.** So Abraham looked at the world and asked, and God answered him.", R("Bereshit Rabbah 39:1")),
  chk("q1", "parable", "why", "In the parable, what does the traveler do before the owner speaks?", ["He asks whether the building has an owner", "He puts out the fire", "He walks past without looking"],
      "He **asks the question**: does this place have someone in charge? Then the owner answers.", ["Nothing in the parable has him fight the fire: he wonders and asks.", "The point is that he **stops and asks**."], look_again=5),
  concept("The souls they made", "Abram and Sarai set out with \"the persons that they had acquired in Haran\" (12:5). **Rashi** quotes a midrash: these are people they brought **under the wings of the Shechinah**. **Abraham taught the men and Sarah taught the women**, and the Torah counts it as if they had made them. (Rashi adds the plain sense: their servants.)", R("Rashi on Genesis 12:5", "from Bereshit Rabbah 39:14")),
  text("Genesis 15:1"),
  term(S("Genesis 15:1", 0, 10, 13), "\"I am a shield to you\" (15:1). The Amidah's first blessing ends **Magen Avraham**, shield of Abraham. The Talmud reads 12:2's \"you shall be a blessing\" as that very ending: **the blessing concludes with you**.", R("Pesachim 117b")),
  term(S("Genesis 17:5", 0, 8, 10), "\"father of a multitude of nations\" (17:5): Abram becomes **Abraham**, and Sarai becomes **Sarah** (17:15). The Talmud: Abram was a father to Aram, Abraham to the whole world. Sarai, \"my princess,\" was a princess to her own people; Sarah, to everyone.", R("Berakhot 13a")),
  chk("q2", "names", "why", "In Berakhot 13a, what do the new names mean?", ["Their role grows from one people to the whole world", "They were given new names to hide from enemies", "The names honor Abram's father"],
      "Abram, father to **Aram**, becomes Abraham, father to **all**; Sarai, princess to **her people**, becomes Sarah, princess to **all**.", ["Nothing in the text points to hiding.", "Terach is not part of this explanation."], look_again=10),
  {"kind": "relevance", "body": "In the Amidah you already know: **Elohei Avraham ... Elohei Sarah**, and the ending **magein Avraham v'ezrat Sarah**. The shield of 15:1 and the blessing of 12:2 are in that line.", "links": ["prayer:avot"]},
  {"kind": "reflect", "prompt": "Abram left before he knew where he was going. When have you started something before you knew where it led?"},
  {"kind": "recap", "points": ["**Lech l'cha**: go, with no destination named; Rashi: for your own good.", "**Veh'yeh b'rachah**: be a blessing for others.", "Midrash: the **lit-up building** and its owner.", "Rashi: Abraham taught the men, **Sarah the women**.", "**Magen Avraham** (15:1, Pesachim 117b) and the new names (Berakhot 13a)."]}]}

L11 = {"id": "x-st-gen-11", "title": "Abraham and Sarah (2): The tent and the laughter", "parashah": ["Vayera"], "status": "draft", "related": ["prayer:avot"],
 "check_note": "My summaries of Shabbat 127a, Rashi on Genesis 18:13, Bava Metzia 87a, Megillah 31a, Rosh Hashanah 11a (read on Sefaria 11/09). Which Torah reading CBB uses on Rosh Hashanah: not checked.",
 "cards": [
  {"kind": "hook", "title": "A hot afternoon", "body": "Abraham sits at the **entrance of his tent** in the heat of the day (18:1). He looks up, sees **three strangers**, and **runs** to greet them.", "src": T("Genesis 18:1-2")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "When they arrive, the Torah tells us the three visitors are angels.", "answer": False,
   "why": "The Hebrew calls them **anashim**, men (\"three figures\" in this translation). Abraham greets them as travelers."},
  text("Genesis 18:1-5"),
  concept("Guests before God", "The chapter opens with **God appearing** to Abraham, then the guests arrive. **Rav**: welcoming guests is **greater than receiving the Divine Presence**, since Abraham asked God to wait (\"do not go on past your servant,\" 18:3) while he ran to them.", R("Shabbat 127a")),
  term(S("Genesis 18:1-5", 2, 6, 10), "\"do not go on past your servant\" (18:3). Said to the guests, or, as Rav reads it, **to God**.", R("Shabbat 127a")),
  chk("q1", "guests", "why", "Why does Rav say hospitality is greater than receiving the Divine Presence?", ["Abraham asked God to wait while he served his guests", "The guests were really God", "Abraham never saw God that day"],
      "Rav reads 18:3 as Abraham **asking God to wait** while he ran to the strangers.", ["Rav's point is the opposite: God and the guests are different, and the guests came first.", "The chapter begins with God appearing to him (18:1)."], look_again=3),
  text("Genesis 18:10-12"),
  concept("Changed for peace", "Sarah laughs: \"with **my husband** so old?\" (18:12). Reporting it to Abraham, God quotes her as \"old as **I** am\" (18:13). **Rashi**: the words were changed **for the sake of peace** between them. The Talmud: peace is so great that even God altered the truth for it.", R("Rashi on Genesis 18:13; Bava Metzia 87a")),
  chk("q2", "peace", "why", "What did God change when telling Abraham about Sarah's laugh?", ["\"With my husband so old\" became \"old as I am\"", "God left out that she laughed", "God said she was asleep"],
      "Sarah's words about **Abraham's** age became words about **her own**, to keep peace in the home.", ["God does mention the laugh: \"Why did Sarah laugh?\" (18:13).", "Nothing like that is in the text."], look_again=7),
  text("Genesis 18:23-25"),
  term(S("Genesis 18:23-25", 2, 13, 18), "\"Shall not the Judge of all the earth deal justly?\" (18:25). Abraham **argues with God** for strangers in Sodom. Noah, told of the flood, said nothing.", T("Genesis 18:25")),
  chk("q3", "argue", "pick", "What does Abraham do when God tells him about Sodom?", ["He argues for the innocent", "He stays silent, like Noah", "He leaves to warn Lot"],
      "He **steps forward and argues**: will You sweep away the innocent with the guilty? (18:23)", ["That was Noah. Abraham speaks up.", "The Torah shows him arguing with God, not traveling."], look_again=10),
  term(S("Genesis 21:6", 0, 2, 6), "\"God has brought me laughter\" (21:6). Her son is named **Yitzchak**, Isaac, from the same root: laughter.", T("Genesis 21:3-6")),
  {"kind": "relevance", "body": "The Talmud teaches that **Sarah was remembered on Rosh Hashanah** (Rosh Hashanah 11a), and gives Genesis 21, \"Adonai took note of Sarah,\" as a Rosh Hashanah Torah reading (Megillah 31a). Check what your congregation reads.", "links": []},
  {"kind": "recap", "points": ["Abraham **runs** to three strangers in the heat (18:1-2).", "Rav: guests **before** the Divine Presence (Shabbat 127a).", "Sarah's laugh, retold **for peace** (Rashi 18:13, Bava Metzia 87a).", "**\"Shall not the Judge of all the earth deal justly?\"** Abraham argues.", "**Yitzchak**: God brought Sarah laughter."]}]}

for L in (L10, L11):  # a check takes the source of the card it points back to (pretest: the hook)
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
u = [x for x in d["units"] if x["id"] == "x-st-gen"][0]
u["lessons"] = [l for l in u["lessons"] if l["id"] not in ("x-st-gen-10", "x-st-gen-11")] + [L10, L11]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [l["id"] for l in u["lessons"]][-3:])
