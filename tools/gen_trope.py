"""Build data/trope.json (trope marks + trope Learn units) from data/src/sefaria-trope.json.
Run: python3 tools/gen_trope.py   (no network). All lesson wording is original; every card names its source.
Mark names: Ashkenazi. Melodies: none (audio null) until Jamie adds recordings."""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = json.load(open(os.path.join(ROOT, "data/src/sefaria-trope.json"), encoding="utf-8"))
VERSES = {}
for s in SRC["sources"]:
    m = re.match(r"Genesis (\d+):(\d+)(?:-(\d+))?$", s["ref"])
    c, a = int(m[1]), int(m[2])
    for k, (t, p) in enumerate(zip(s["he_t"], s["he"])):
        VERSES[f"Genesis {c}:{a+k}"] = {"he_t": re.sub(" {2,}", " ", t), "he": p}
LIC = "Hebrew: Miqra according to the Masorah (Sefaria, CC-BY-SA)"
JAC = "Joshua R. Jacobson, Chanting the Hebrew Bible (JPS, 2002)"

# id: (name, codepoint(s), role, position, family, note)
MARKS = {
 "sof_pasuk": ("Sof pasuk (silluk)", "ֽ׃", "ruler", "below the stressed syllable of the last word, then two dots after the word", "end", "Ends every verse. Silluk looks like the meteg, a small vertical line; the two dots after the word make it certain."),
 "etnachta": ("Etnachta", "֑", "ruler", "below", "etnachta", "The main pause inside a verse: it splits most verses in two."),
 "tipcha": ("Tipcha", "֖", "ruler", "below", "mercha-tipcha", "Usually comes just before etnachta or sof pasuk."),
 "mercha": ("Mercha", "֥", "connector", "below", "mercha-tipcha", "Often leads into tipcha, or into silluk at the end of a verse."),
 "munach": ("Munach", "֣", "connector", "below", "munach-zakef", None),
 "zakef_katon": ("Zakef katon", "֔", "ruler", "above", "munach-zakef", None),
 "zakef_gadol": ("Zakef gadol", "֕", "ruler", "above", "zakef-gadol", None),
 "revia": ("Revia", "֗", "ruler", "above", "revia", None),
 "pashta": ("Pashta", "֙", "ruler", "above, on the last letter of the word", "pashta-kadma", None),
 "kadma": ("Kadma", "֨", "connector", "above, on the stressed syllable", "pashta-kadma", None),
 "mahpach": ("Mahpach", "֤", "connector", "below", "pashta-kadma", None),
 "yetiv": ("Yetiv", "֚", "ruler", "below, before the first letter", "pashta-kadma", None),
 "tevir": ("Tevir", "֛", "ruler", "below", "tevir-darga", None),
 "darga": ("Darga", "֧", "connector", "below", "tevir-darga", None),
 "geresh": ("Geresh", "֜", "ruler", "above", "geresh", None),
 "gershayim": ("Gershayim", "֞", "ruler", "above", "geresh", None),
 "segol": ("Segol", "֒", "ruler", "above, on the last letter", "rare", None),
 "zarka": ("Zarka", "֮", "ruler", "above, on the last letter", "rare", None),
 "telisha_gedola": ("Telisha gedola", "֠", "ruler", "above, on the first letter", "rare", None),
 "telisha_ketana": ("Telisha ketana", "֩", "connector", "above, on the last letter", "rare", None),
 "pazer": ("Pazer", "֡", "ruler", "above", "rare", None),
 "shalshelet": ("Shalshelet", "֓", "ruler", "above", "rare", None),
}
LOOK = {  # shapes easy to confuse; pashta/kadma share a shape, so never offered against each other
 "sof_pasuk": ["etnachta", "tipcha", "mercha"], "etnachta": ["munach", "mahpach", "yetiv"],
 "tipcha": ["mercha", "darga", "tevir"], "mercha": ["tipcha", "darga", "munach"],
 "munach": ["mahpach", "etnachta", "mercha"], "mahpach": ["munach", "etnachta", "yetiv"],
 "zakef_katon": ["zakef_gadol", "revia", "segol"], "zakef_gadol": ["zakef_katon", "revia", "shalshelet"],
 "revia": ["zakef_katon", "segol", "geresh"], "pashta": ["geresh", "telisha_ketana", "zarka"],
 "kadma": ["geresh", "telisha_gedola", "gershayim"], "yetiv": ["mahpach", "munach", "etnachta"],
 "tevir": ["darga", "tipcha", "mercha"], "darga": ["tevir", "mercha", "munach"],
 "geresh": ["gershayim", "pashta", "telisha_gedola"], "gershayim": ["geresh", "kadma", "zakef_katon"],
 "segol": ["revia", "zakef_katon", "gershayim"], "zarka": ["pashta", "telisha_ketana", "segol"],
 "telisha_gedola": ["telisha_ketana", "geresh", "kadma"], "telisha_ketana": ["telisha_gedola", "pashta", "zarka"],
 "pazer": ["shalshelet", "gershayim", "geresh"], "shalshelet": ["pazer", "zakef_gadol", "revia"],
}
SAME = {"pashta": ["kadma"], "kadma": ["pashta"]}

def example(ch):
    for ref, v in VERSES.items():
        for n, w in enumerate(v["he_t"].split(" ")):
            if ch[0] in w: return {"ref": ref, "w": n, "word": w}
    return None

items = {}
for k, (name, ch, role, pos, fam, note) in MARKS.items():
    items["tm-" + k] = {"kind": "mark", "name": name, "ch": ch, "he": "◌" + ch, "role": role, "pos": pos, "family": fam,
        "note": note, "look": ["tm-" + x for x in LOOK[k]], "same": ["tm-" + x for x in SAME.get(k, [])],
        "ex": example(ch), "audio": None, "src": JAC + " ⚑ page to check; Unicode encoding as in Sefaria's Masorah text"}

def V(ref, **kw):
    return {"ref": ref, **VERSES[ref], **kw}

n_et = sum("֑" in v["he_t"] for v in VERSES.values())
no_et = [r for r, v in VERSES.items() if "֑" not in v["he_t"]]

def card(text, src, label=None, verse=None, chip=False): return {"t": "card", "label": label, "text": text, "src": src, "verse": verse, "chip": chip}
def mc(qid, q, opts, a, why, src):
    items["tq-" + qid] = {"kind": "tq", "q": q, "opts": opts, "a": a, "why": why, "src": src, "he": ""}
    return {"t": "q", "id": "tq-" + qid}

L1 = [
 card("Look closely at a printed Torah verse. Besides the vowels, small marks sit above and below the words. These are the te'amim, the accents. In English and Yiddish they are usually called trope.", f"Genesis 1:1. {LIC}. Names: {JAC} ⚑", "Trope", V("Genesis 1:1")),
 card("The same verse with the trope taken out. The letters and vowels are exactly the same. The trope adds a layer on top.", f"Genesis 1:1. {LIC}", None, V("Genesis 1:1", plain=True)),
 card("The marks do three jobs. They show which syllable is stressed. They group words into phrases, like commas and periods. And each mark stands for a short tune.", JAC + " ⚑"),
 card("The Talmud finds the te'amim already in Ezra's public Torah reading. It reads the words \"and caused them to understand the reading\" (Nehemiah 8:8) as the cantillation that makes the verses clear.", "Talmud Nedarim 37b (William Davidson translation on Sefaria)"),
 card("The written marks came later. Scholars called the Masoretes, working mostly in Tiberias, added vowels and te'amim to the text between about the 7th and 10th centuries CE. The Aleppo Codex, about 930 CE, is the best-known example.", JAC + " ⚑ (scholarly dating)"),
 card("Chanting is part of learning, not decoration. The Talmud criticizes reading Torah without a melody. One reason it gives: the tune helps you remember what you learned.", "Talmud Megillah 32a (William Davidson translation on Sefaria)"),
 card("A mark is not a single note. It names a short tune, and the tune depends on the book and the community. This app teaches each mark's name, shape and job. Melodies come only from real recordings, like your cantor's.", JAC + " ⚑", None, None, True),
 mc("t1-what", "What is trope?", ["The vowel dots under the letters", "Marks that show stress, phrasing and a short tune", "The scribe's crowns on the scroll letters"], 1,
    "Vowels are a separate system. Trope marks sit alongside them and do three jobs.", JAC + " ⚑"),
 mc("t1-neh", "Which verse does the Talmud read as including the te'amim?", ["Nehemiah 8:8", "Genesis 1:1", "Psalm 150:6"], 0,
    "Nehemiah 8:8 describes Ezra's reading; Nedarim 37b takes \"caused them to understand\" as the cantillation.", "Talmud Nedarim 37b"),
 mc("t1-meg", "In Megillah 32a, what is one benefit of chanting?", ["It makes the reading shorter", "It helps you remember what you learned", "It replaces the vowels"], 1,
    "The Gemara explains that the tune helps the learner remember.", "Talmud Megillah 32a"),
]
L2 = [
 card("The same marks are sung to different melodies, depending on what is read. Ashkenazi tradition has separate melodies for the Torah, the Haftarah, Esther, Lamentations, and the other three scrolls (Ruth, Song of Songs, Ecclesiastes). The Torah also has a special melody for the High Holy Days.", JAC + " ⚑", "Melodies"),
 card("The Haftarah is the reading from the Prophets after the Torah reading on Shabbat and festivals. Same marks as the Torah, a different tune. Its blessings are in this app's Torah service unit.", JAC + " ⚑"),
 card("Esther is chanted on Purim and Lamentations (Eicha) on Tisha B'Av, each with its own melody.", JAC + " ⚑"),
 card("Communities differ too. Ashkenazi, Sephardi, Yemenite and other communities sing different tunes, and some marks have different names. This app uses the Ashkenazi names.", JAC + " ⚑"),
 card("Three books, Psalms, Proverbs and Job, use a different set of marks. This course covers the system used in the other 21 books of the Tanakh.", JAC + " ⚑"),
 card("So you learn each mark once: its name, its shape and its job. Its tune is a second layer, learned once per melody from a recording.", JAC + " ⚑", None, None, True),
 mc("t2-haf", "Is the Haftarah chanted to the Torah melody?", ["Yes: same marks, same tune", "Same marks, a different tune", "The Haftarah has no trope"], 1,
    "The Prophets use the same marks as the Torah, sung to the Haftarah melody.", JAC + " ⚑"),
 mc("t2-purim", "Which book has its own melody for Purim?", ["Esther", "Ruth", "Jonah"], 0, "Esther is read on Purim with its own melody.", JAC + " ⚑"),
 mc("t2-comm", "What differs between Ashkenazi and Sephardi reading?", ["The tunes, and some mark names", "The Hebrew words of the Torah", "Nothing"], 0,
    "The text is shared. The tunes and some names of the marks differ.", JAC + " ⚑"),
]
L3 = [
 card("Trope marks come in two kinds. Disjunctive marks (mafsikim) mark a pause; they are often called kings or rulers. Conjunctive marks (m'shartim, \"servants\") join a word to the next one.", JAC + " ⚑", "Two kinds"),
 card("Every verse ends with sof pasuk, \"end of verse\": a short line called silluk under the stressed syllable of the last word, then two dots after it.", f"Genesis 1:1. {LIC}", None, V("Genesis 1:1", hi="׃")),
 card(f"Most verses split into two halves at etnachta, the strongest pause inside a verse. Here the first half is the first three words. Of the {len(VERSES)} Genesis verses in this app, {n_et} have an etnachta.",
      f"Genesis 1:1. {LIC}. Count: this app's verses ({', '.join(no_et)} has none)", None, V("Genesis 1:1", split=True)),
 card("Each half is divided again by smaller rulers, and connectors lead into them. A verse works like a sentence with commas inside its two halves.", JAC + " ⚑", None, V("Genesis 1:27", split=True)),
 card("Tipcha is a ruler that usually comes just before etnachta or sof pasuk. Mercha is a connector that often leads into tipcha. In this verse's second half: mercha, tipcha, mercha, then sof pasuk.", f"Genesis 1:1. {LIC}. {JAC} ⚑", None, V("Genesis 1:1", hi="֥֖")),
 {"t": "drill", "marks": ["tm-sof_pasuk", "tm-etnachta", "tm-tipcha", "tm-mercha"]},
 mc("t3-et", "What does etnachta do?", ["Splits the verse into two halves", "Ends the verse", "Joins a word to the next"], 0, "Etnachta is the main pause inside the verse.", JAC + " ⚑"),
 mc("t3-mer", "Is mercha a ruler or a connector?", ["A ruler: it marks a pause", "A connector: it leads into the next word"], 1, "Mercha is a conjunctive mark, often leading into tipcha.", JAC + " ⚑"),
]
def lesson(lid, title, sub, icon, steps):
    ids = [s["id"] for s in steps if s["t"] == "q"] + [m for s in steps if s["t"] == "drill" for m in s["marks"]]
    return {"id": lid, "title": title, "subtitle": sub, "icon": icon, "trope": True, "items": ids, "steps": steps}
units = [{"id": "u-trope1", "title": "Trope 1: What trope is", "subtitle": "Cantillation marks: what they are, why there are many melodies, rulers and connectors", "tiles": False,
  "lessons": [lesson("tr-1", "Signs, not notes", "what the marks are", "◌֑", L1),
              lesson("tr-2", "One set of marks, many melodies", "Torah, Haftarah, scrolls", "◌֖", L2),
              lesson("tr-3", "Rulers and connectors", "sof pasuk, etnachta, tipcha, mercha", "◌֥", L3)]}]
for u in units:
    for l in u["lessons"]:
        for i in l["items"]: assert i in items, i
out = {"note": "Built by tools/gen_trope.py. Do not edit by hand.", "units": units, "items": items}
json.dump(out, open(os.path.join(ROOT, "data/trope.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("marks", len(MARKS), "items", len(items), "etnachta", n_et, "/", len(VERSES), no_et)
print({k: (v["ex"] or {}).get("ref") for k, v in items.items() if v["kind"] == "mark"})
