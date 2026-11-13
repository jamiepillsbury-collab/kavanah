"""Add Kabbalah unit 2 "In practice" (x-kb-practice) to data/src/x-kabbalah.json. RUN ORDER: add_kabbalah1.py, then this.
Lessons: Welcoming the Shabbat bride (L'cha Dodi), Counting the Omer. L'cha Dodi line from data/prayers.json (Metsudah); Leviticus 23:15-16 from sefaria-kabbalah2.json.
L'cha Dodi acrostic (שלמה הלוי) checked 11/13 on Sefaria's Siddur Ashkenaz Lekha Dodi (first letters of the 8 middle stanzas)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {(s["ref"], s["lang"]): s["text"] for s in json.load(open(os.path.join(ROOT, "data/src/sefaria-kabbalah2.json"), encoding="utf-8"))["sources"]}
PR = {p["id"]: p for p in json.load(open(os.path.join(ROOT, "data/prayers.json"), encoding="utf-8"))["prayers"]}
def S(ref, a, b): return " ".join(" ".join(SRC[(ref, "he")]).split()[a:b]).replace("יְהֹוָה", "יְיָ").replace("&thinsp;", " ")
TN = lambda ref: {"type": "torah", "ref": ref}
def K(ref, note=None):  # "Ref (translator)" -> ref + note, so the Sefaria link works
    import re
    m = re.match(r"^(.*?) \((.*)\)$", ref)
    if m and not note: ref, note = m.group(1), m.group(2)
    return {"type": "kabbalah", "ref": ref, **({"note": note} if note else {})}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
def LIT(ref, note=None):
    import re
    m = re.match(r"^(.*?) \((.*)\)$", ref)
    if m and not note: ref, note = m.group(1), m.group(2)
    return {"type": "liturgy", "ref": ref, **({"note": note} if note else {})}
SCH = lambda ref: {"type": "scholarly", "ref": ref, "note": "from memory, not on Sefaria; check"}
def text(ref): return {"kind": "text", "sefaria": ref, "src": TN(ref)}
def term(he, gloss, src): return {"kind": "term", "he": he, "tl": None, "gloss": gloss, "src": src}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}
LD = PR["lcha_dodi_1"]["lines"][0]

P1 = {"id": "x-kb-05", "title": "Welcoming the Shabbat bride", "status": "draft", "related": ["prayer:lcha_dodi_1", "prayer:lcha_dodi_2"],
 "check_note": "Shabbat 119a read on Sefaria 11/13. Acrostic checked on Sefaria's Siddur Ashkenaz Lekha Dodi. Safed history from memory (Scholem): check. CBB practice from the CBB siddur note in data/prayers.json.",
 "cards": [
  {"kind": "hook", "title": "Friday at sunset", "body": "Every Friday night, many congregations sing **L'cha Dodi**: a song welcoming **Shabbat as a bride**. The idea is ancient; the song comes from the Kabbalists.", "src": R("Shabbat 119a")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "The stanzas of L'cha Dodi spell out the name of its author.", "answer": True,
   "why": "Their first letters spell **שְׁלֹמֹה הַלֵּוִי**, Shlomo HaLevi."},
  concept("Go out to greet the queen", "In the Talmud, **Rabbi Chanina** would wrap himself in his cloak at sunset on Friday and say: \"Come and we will go out to greet Shabbat the queen.\" **Rabbi Yannai** would dress and say: \"Enter, O bride. Enter, O bride.\"", R("Shabbat 119a")),
  chk("q1", "greet", "why", "How did Rabbi Chanina welcome Shabbat in Shabbat 119a?", ["He dressed up and went out to greet Shabbat the queen", "He fasted all Friday", "He read the whole Torah portion"],
      "Shabbat as **a royal guest**, met at the door.", ["Not in the Talmud.", "Not in the Talmud."], look_again=2),
  concept("In the fields of Safed", "In 16th-century **Safed**, Kabbalists around Isaac Luria went out to the fields on Friday afternoon, dressed in white, to **greet Shabbat**. One of them, **Shlomo HaLevi Alkabetz**, wrote L'cha Dodi. For Kabbalists, the Shabbat bride is also **the Shechinah**, God's presence, coming home.", SCH("Gershom Scholem, On the Kabbalah and Its Symbolism (1965)")),
  term(LD["he"], "\"" + LD["en"] + "\" The refrain, sung after every stanza.", LIT("Siddur Ashkenaz, Shabbat, Kabbalat Shabbat, Lekha Dodi (Metsudah siddur, 1981)")),
  concept("A name hidden in the song", "Read the **first letter** of each of the eight middle stanzas: ש ל מ ה ה ל ו י, **שְׁלֹמֹה הַלֵּוִי**, Shlomo HaLevi. The poet signed his name inside the song.", LIT("Siddur Ashkenaz, Shabbat, Kabbalat Shabbat, Lekha Dodi (checked on Sefaria)")),
  chk("q2", "acrostic", "pick", "What do the first letters of L'cha Dodi's stanzas spell?", ["Shlomo HaLevi, the poet's name", "Shabbat Shalom", "The name of God"],
      "An **acrostic**: the author's signature.", ["Not this.", "Not this."], look_again=6),
  {"kind": "relevance", "body": "At CBB, everyone **rises and turns to greet the Shabbat bride** before the last stanza.", "links": ["prayer:lcha_dodi_1", "prayer:lcha_dodi_2"]},
  {"kind": "reflect", "prompt": "Rabbi Chanina dressed up and went out to meet Shabbat. What would going out to greet Shabbat look like for you this week?"},
  {"kind": "recap", "points": ["Shabbat 119a: greet Shabbat **the queen**, \"**Enter, O bride**.\"", "Safed: Kabbalists in the fields; **Alkabetz** writes L'cha Dodi.", "The stanzas spell **שְׁלֹמֹה הַלֵּוִי**.", "At CBB: **rise and turn** to greet the bride."]}]}

P2 = {"id": "x-kb-06", "title": "Counting the Omer", "status": "draft", "related": [],
 "check_note": "Menachot 66a, Yevamot 62b, Zohar Emor 34:162 (Soncino), Siddur Sefard Sefirat HaOmer (Metsudah note; Hebrew sefirot lines) read on Sefaria 11/13. CHECK: does CBB count the Omer, and with the sefirot?",
 "cards": [
  {"kind": "hook", "title": "Forty-nine days", "body": "From the second night of Passover to Shavuot, Jews **count** each night: day one, day two, up to forty-nine. Kabbalah turned the counting into a practice of **the inner life**.", "src": TN("Leviticus 23:15-16")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "According to Abaye in the Talmud, what is the mitzvah of counting?", "choices": ["Count both the days and the weeks", "Count only the days", "Count only the weeks", "Count only on Shabbat"], "answer": 0,
   "why": "\"It is a mitzva to count days, and it is also a mitzva to count weeks.\""},
  text("Leviticus 23:15-16"),
  term(S("Leviticus 23:15-16", 0, 2), "\"you shall count off\" (23:15).", TN("Leviticus 23:15")),
  concept("Days and weeks", "**Abaye**: \"It is a mitzva to count days, and it is also a mitzva to count weeks.\" So on day eight, for example, one counts eight days, which is one week and one day. **Ameimar** counted only days, since without the Temple's offering the count is a **remembrance**.", R("Menachot 66a")),
  chk("q1", "count", "why", "Why did Ameimar count only days, not weeks?", ["Without the Temple's offering, the count is only a remembrance", "He forgot the weeks", "Weeks were forbidden"],
      "Abaye counts both; Ameimar keeps it **simpler**.", ["Not the Talmud's reason.", "Not the Talmud's reason."], look_again=4),
  concept("Counting toward Sinai", "A note in the Metsudah siddur explains the counting: like someone awaiting **a dear friend** on a set day, who counts the days in eager anticipation, we count from **freedom** (Passover) to **receiving the Torah** (Shavuot). The **Zohar** adds: just as a woman counts seven days toward purity, Israel counts these days **for purity**.", LIT("Siddur Sefard, Sefirat HaOmer 1 (Metsudah note); Zohar, Emor 34:162")),
  concept("Seven weeks, seven qualities", "Kabbalists give each week one of the **seven lower sefirot**, from Chesed (kindness) to Malchut, and each day a sefirah **within** that week. So day one is חֶסֶד שֶׁבְּחֶסֶד, kindness within kindness, and day forty-nine is Malchut within Malchut. Each night becomes a small **check-up of the soul**.", K("Siddur Sefard, Weekday Maariv, Sefirat HaOmer", "Sefaria Hebrew; order of the sefirot from memory, check")),
  chk("q2", "sefirot", "pick", "In the kabbalistic count, what quality belongs to day one?", ["Kindness within kindness (Chesed within Chesed)", "Kingship within kingship", "Strength within strength"],
      "The count begins with **Chesed**, kindness.", ["That is day forty-nine.", "That is day nine."], look_again=7),
  concept("A season of mourning", "The Talmud says **Rabbi Akiva's** twelve thousand pairs of students all died between Passover and Shavuot, \"because they did not treat each other with respect.\" This is one reason parts of the Omer are kept as **a time of mourning**.", R("Yevamot 62b")),
  {"kind": "reflect", "prompt": "If each week of the Omer focused on one quality, starting with kindness and then strength, which week would you need most this year?"},
  {"kind": "recap", "points": ["\"**You shall count off** seven weeks\" (Leviticus 23:15).", "Menachot 66a: count **days and weeks**.", "From freedom to **Sinai**, counting like waiting for a friend.", "Kabbalah: each day a **sefirah**, starting with **kindness within kindness**.", "Yevamot 62b: Akiva's students and **respect**."]}]}

p = os.path.join(ROOT, "data/src/x-kabbalah.json")
d = json.load(open(p, encoding="utf-8"))
LS = (P1, P2)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
d["units"] = [u for u in d["units"] if u["id"] != "x-kb-practice"] + [{"id": "x-kb-practice", "title": "In practice", "subtitle": "Kabbalah you can live: Shabbat, the Omer", "lessons": list(LS)}]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
