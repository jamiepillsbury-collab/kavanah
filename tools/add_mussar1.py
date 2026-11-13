"""Write data/src/x-mussar.json: Mussar track (added 11/13), unit 1 "Beginning a practice" (x-mu-start), lessons x-mu-01..04.
English from Sefaria: Pirkei Avot (Kulp), Mesillat Yesharim (Sebag), Orchot Tzadikim (Cohen), Mishneh Torah (Touger), Talmud (Davidson). Mussar-movement history from memory, flagged. No Hebrew text cards (Bible verses not used)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = lambda ref, note=None: {"type": "mussar", "ref": ref, **({"note": note} if note else {})}
R = lambda ref, note=None: {"type": "rabbinic", "ref": ref, **({"note": note} if note else {})}
SCH = lambda ref: {"type": "scholarly", "ref": ref, "note": "from memory, not on Sefaria; check"}
def concept(title, body, src): return {"kind": "concept", "title": title, "body": body, "src": src}
def chk(cid, idea, typ, q, choices, why, wrong, **kw):
    return {"kind": "check", "id": cid, "idea": idea, "type": typ, "q": q, "choices": choices, "answer": 0, "why": why, "wrong_why": [None] + wrong, **kw}

U1 = {"id": "x-mu-01", "title": "What is Mussar?", "status": "draft", "related": [],
 "check_note": "Pirkei Avot 4:1 (Kulp) and Mesillat Yesharim Intro + 1:1 (Sebag) read on Sefaria 11/13. Movement history from memory: check.",
 "cards": [
  {"kind": "hook", "title": "Working on yourself", "body": "**Mussar** is the Jewish practice of working on your character, one trait at a time: patience, humility, generosity, honesty. The traits are called **middot**.", "src": SCH("Mussar movement: Rabbi Israel Salanter (19th c.); Alan Morinis, Everyday Holiness (2007)")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "According to Ben Zoma, who is rich?", "choices": ["One who rejoices in their lot", "One who owns the most land", "One who never spends", "One who has many children"], "answer": 0,
   "why": "Each of Ben Zoma's answers turns a measure of status into **a trait of character**."},
  concept("Four questions", "**Ben Zoma** asks: who is wise? One who **learns from every person**. Who is mighty? One who **masters their own impulses**. Who is rich? \"He who rejoices in his lot.\" Who is honored? One who **honors others**.", R("Pirkei Avot 4:1", "trans. Joshua Kulp")),
  chk("q1", "benzoma", "why", "What do Ben Zoma's four answers have in common?", ["Each turns an outward status into an inner trait", "Each is about money", "Each is about Torah study only"],
      "Wisdom, strength, wealth and honor, **found inside**.", ["Only one is about money.", "Not this."], look_again=2),
  concept("Nothing new", "Moshe Chaim Luzzatto opens his classic **Mesillat Yesharim**, The Path of the Just, by saying he wrote it not to teach new things but \"to remind them of what they already know.\" Mussar is less about learning and more about **practice**.", M("Mesillat Yesharim, Introduction 1", "trans. Yosef Sebag")),
  concept("Your obligation in your world", "Luzzatto's first chapter: the root of a good life is to clarify, and truly take in, **what is your obligation in your world**, and to what you should direct your effort all your days.", M("Mesillat Yesharim 1:1", "trans. Yosef Sebag")),
  chk("q2", "remind", "pick", "Why did Luzzatto say he wrote Mesillat Yesharim?", ["To remind people of what they already know", "To reveal new secrets", "To replace the Talmud"],
      "Mussar **reminds**; the work is in living it.", ["He says the opposite.", "Not his aim."], look_again=4),
  concept("A movement", "In 19th-century Lithuania, **Rabbi Israel Salanter** started the **Mussar movement**: daily study of texts like Mesillat Yesharim, often slowly and with feeling, and honest work on one's traits. In recent decades Mussar groups have spread across Jewish communities, including **Reform**.", SCH("Immanuel Etkes, Rabbi Israel Salanter and the Mussar Movement (1993); Alan Morinis, Everyday Holiness (2007)")),
  {"kind": "reflect", "prompt": "Luzzatto says Mussar reminds us of what we already know. What do you already know you should be doing, but are not yet doing?"},
  {"kind": "recap", "points": ["**Mussar**: working on your **middot**, your traits.", "Ben Zoma: wisdom, strength, wealth, honor, **inside**.", "Mesillat Yesharim: a **reminder**, not a secret.", "Salanter's **movement**, now in many communities."]}]}

U2 = {"id": "x-mu-02", "title": "The middle path", "status": "draft", "related": [],
 "check_note": "Orchot Tzadikim Introduction (Cohen) and Mishneh Torah, Human Dispositions 1:4, 2:2 (Touger) read on Sefaria 11/13.",
 "cards": [
  {"kind": "hook", "title": "Not good or bad", "body": "Mussar doesn't sort traits into good and bad. Most traits have **a right amount**, and the work is finding it.", "src": R("Mishneh Torah, Human Dispositions 1:4", "trans. Eliyahu Touger")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "Maimonides says the cure for an extreme trait is to lean toward the opposite extreme for a while.", "answer": True,
   "why": "Then you return to **the middle path**."},
  concept("Sickness of the soul", "**Orchot Tzadikim**: bad traits are **a sickness of the soul**. Just as a sick person tastes the bitter as sweet, a sick soul loves what harms it. The remedy: go to \"the healers of souls,\" teachers who help restore the good path.", M("Orchot Tzadikim, Introduction", "trans. Seymour J. Cohen")),
  concept("Husk and flour", "The same book explains each trait's **good and bad sides**, so that, since a person has choice, they \"may throw aside the husk and take the fine flour.\"", M("Orchot Tzadikim, Introduction", "trans. Seymour J. Cohen")),
  chk("q1", "sickness", "pick", "How does Orchot Tzadikim describe bad traits?", ["As a sickness of the soul", "As a punishment", "As something that cannot change"],
      "And sickness can be **healed**.", ["Not its image.", "The book says traits can be healed."], look_again=2),
  concept("The middle path", "**Maimonides**: for each trait, the straight path is **the midpoint**, equally distant from both extremes. Not stingy, not wasteful; not furious, not numb.", R("Mishneh Torah, Human Dispositions 1:4", "trans. Eliyahu Touger")),
  concept("Leaning the other way", "How to heal an extreme? A very angry person trains himself, for a long time, not to react even when insulted, until the anger is uprooted. Anyone who has swayed to one extreme should \"move in the direction of the opposite extreme\" for a while, then come back to **the middle**.", R("Mishneh Torah, Human Dispositions 2:2", "trans. Eliyahu Touger")),
  chk("q2", "lean", "why", "According to Maimonides, why lean toward the opposite extreme?", ["To pull a trait back to the middle", "To stay there forever", "To punish yourself"],
      "The opposite extreme is **a temporary correction**.", ["He says to return to the middle.", "Not his reason."], look_again=6),
  {"kind": "reflect", "prompt": "Pick one trait where you lean too far one way, too much or too little. What would leaning the other way for a month look like?"},
  {"kind": "recap", "points": ["Orchot Tzadikim: bad traits are **a sickness of the soul**.", "**Husk and fine flour**: every trait has two sides.", "Maimonides: the **middle path**.", "Heal an extreme by **leaning the other way** for a while."]}]}

U3 = {"id": "x-mu-03", "title": "The daily accounting", "status": "draft", "related": [],
 "check_note": "Bava Batra 78b and Mesillat Yesharim 3 (Sebag) read on Sefaria 11/13. Cheshbon HaNefesh / Franklin card from memory: check (Lefin's text not on Sefaria in English).",
 "cards": [
  {"kind": "hook", "title": "Keeping accounts", "body": "Businesses keep accounts. Mussar asks you to keep **accounts of the soul**: cheshbon ha-nefesh.", "src": R("Bava Batra 78b")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "pick", "q": "In Bava Batra 78b, who are the moshlim of Numbers 21:27?", "choices": ["People who rule over their own impulses", "Kings and judges", "The rich", "Priests"], "answer": 0,
   "why": "Rabbi Yochanan reads a verse about rulers as a verse about **self-mastery**."},
  concept("Come to Heshbon", "**Rabbi Yochanan** reads a verse (Numbers 21:27) as a pun. The moshlim, the verse's storytellers, become people who **rule over their impulses**, and \"Come to Heshbon\" means: come, let us make an **accounting**, cheshbon. What does a good deed cost, and what does it bring? What does a wrong bring, and what does it cost?", R("Bava Batra 78b")),
  chk("q1", "heshbon", "why", "How does Rabbi Yochanan read \"Come to Heshbon\"?", ["Come, let us make an accounting of our deeds", "Travel to the city of Heshbon", "Count the stars"],
      "**Heshbon** sounds like **cheshbon**, an account.", ["He reads it as a pun.", "Not this."], look_again=2),
  concept("Two investigations", "Luzzatto: \"He who wants to watch over himself must investigate two matters.\" First, what is **truly good** and truly harmful. Second, whether **his own actions** fall on the good side or the bad.", M("Mesillat Yesharim 3:1-3", "trans. Yosef Sebag")),
  concept("Before and after", "**Before** acting: weigh the act first. **Afterward**: bring your deeds to mind, weigh them, keep and strengthen the good, and where you find something wrong, work out **a strategy** to turn away from it.", M("Mesillat Yesharim 3:5-6", "trans. Yosef Sebag")),
  chk("q2", "review", "pick", "According to Mesillat Yesharim, what should you do with deeds already done?", ["Review them, keep the good, plan how to change the bad", "Forget them", "Confess them publicly"],
      "A daily review with **a plan**, not just regret.", ["He says to review them.", "Not in this chapter."], look_again=5),
  concept("A chart and a week", "In 1812, **Menachem Mendel Lefin** published **Cheshbon HaNefesh**: thirteen traits, one in focus each week, checked off on a daily chart. He adapted the method from **Benjamin Franklin's** autobiography.", SCH("Menachem Mendel Lefin, Cheshbon HaNefesh (1812)")),
  {"kind": "reflect", "prompt": "Tonight before sleep, review the day: one moment you would keep, and one you would change. What are they today?"},
  {"kind": "recap", "points": ["Bava Batra 78b: those who **rule themselves** make an **accounting**.", "Mesillat Yesharim 3: know the good; **check your deeds**.", "Weigh **before** acting; review and plan **after**.", "Lefin: one trait a week, **a daily chart**."]}]}

U4 = {"id": "x-mu-04", "title": "A ladder for the soul", "status": "draft", "related": [],
 "check_note": "Avodah Zarah 20b and Mesillat Yesharim Introduction 40-42 (Sebag) read on Sefaria 11/13. Rabbi's-teaching card: the connection is mine; check with Jamie.",
 "cards": [
  {"kind": "hook", "title": "One rung at a time", "body": "The Talmud describes character as **a ladder**: each quality leads to the next. Mesillat Yesharim is built on it.", "src": R("Avodah Zarah 20b")},
  {"kind": "check", "id": "pre", "pretest": True, "type": "tf", "q": "Mesillat Yesharim is organized around a ladder taught by Rabbi Pinchas ben Yair.", "answer": True,
   "why": "Luzzatto quotes it in his introduction and gives each rung its own chapters."},
  concept("The ladder", "**Rabbi Pinchas ben Yair**: \"Torah study leads to care in the performance of mitzvot.\" Care leads to **diligence**; diligence to cleanliness of the soul; then abstention from evil, purity, **piety**, **humility**, fear of sin, **holiness**, the Divine Spirit, and at last the resurrection of the dead.", R("Avodah Zarah 20b")),
  {"kind": "check", "id": "q1", "idea": "ladder", "type": "order", "q": "Put these rungs of Rabbi Pinchas ben Yair's ladder in order.", "items": ["Torah study", "Care", "Diligence", "Humility", "Holiness"],
   "why": "Study, then care, diligence, and up through humility to **holiness**.", "src": R("Avodah Zarah 20b"), "look_again": 2},
  concept("A path, not a leap", "Luzzatto builds **Mesillat Yesharim** on this teaching: \"Torah brings to watchfulness; Watchfulness brings to Zeal\", and so on, one rung per section. No one starts at holiness; you start with **watchfulness**, paying attention.", M("Mesillat Yesharim, Introduction 40-42", "trans. Yosef Sebag")),
  chk("q2", "first", "pick", "In Mesillat Yesharim, what is the first quality Torah study brings?", ["Watchfulness", "Holiness", "Humility"],
      "First, **pay attention**.", ["Holiness is near the top.", "Humility comes later."], look_again=4),
  concept("Growing up", "Your rabbi reads the Torah as a people **growing up**, from a God who acts for us toward a God present in **our own choices**. Mussar is that adult work done one person at a time: no miracle, just **steady practice**, rung by rung.", {"type": "reform", "ref": "Teaching from Jamie's rabbi (oral, as Jamie retold it)", "note": "connection to Mussar is mine; check with Jamie"}),
  {"kind": "reflect", "prompt": "Which rung are you standing on right now, and what would one step up look like in your week?"},
  {"kind": "recap", "points": ["Avodah Zarah 20b: a **ladder** from study to holiness.", "Mesillat Yesharim: built on that ladder.", "Start with **watchfulness**.", "Mussar: steady practice, **rung by rung**."]}]}

LS = (U1, U2, U3, U4)
for L in LS:
    for c in L["cards"]:
        if c["kind"] == "check" and "src" not in c: c["src"] = L["cards"][c.get("look_again", 0)]["src"]
out = {"track": "mussar", "units": [{"id": "x-mu-start", "title": "Beginning a practice", "subtitle": "Traits, balance, a daily accounting, and a ladder", "lessons": list(LS)}]}
json.dump(out, open(os.path.join(ROOT, "data/src/x-mussar.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", [len(L["cards"]) for L in LS])
