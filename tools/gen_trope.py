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

# ---------- Unit 2: the marks, one lesson per family ----------
C = {k: v[1][0] for k, v in MARKS.items()}
def cnt(k): return sum(t["he_t"].count(C[k]) for t in VERSES.values())
def seq(a, b):
    for ref, v in VERSES.items():
        w = v["he_t"].split(" ")
        for i in range(len(w) - 1):
            if C[a] in w[i] and C[b] in w[i + 1]: return ref
def seqn(a, b): return sum(1 for v in VERSES.values() for w in [v["he_t"].split(" ")] for i in range(len(w) - 1) if C[a] in w[i] and C[b] in w[i + 1])
N = len(VERSES)
def count_src(): return f"Count: this app's {N} Genesis verses (Masorah text on Sefaria)"
def drill(new, review): return {"t": "drill", "marks": ["tm-" + x for x in new + review]}
rulers = sorted([k for k, v in MARKS.items() if v[2] == "ruler" and k != "sof_pasuk"], key=cnt, reverse=True)
U2 = []
U2.append(lesson("tr2-1", "Munach and zakef katon", "a medium pause", "◌֔", [
 card("Zakef katon is a ruler written above the word: two dots, one over the other. Its pause is smaller than etnachta's. Each half of a verse is often split again at a zakef katon.", JAC + " ⚑", "Zakef katon"),
 card(f"Munach is a connector written below the word, shaped like a corner. It often leads into zakef katon: in this app's verses that pair comes {seqn('munach','zakef_katon')} times.", f"{seq('munach','zakef_katon')}. {LIC}. {count_src()}", None, V(seq("munach", "zakef_katon"), hi=C["munach"] + C["zakef_katon"])),
 card(f"Among the rulers inside a verse, only tipcha is more common here than zakef katon ({cnt('tipcha')} and {cnt('zakef_katon')} times).", count_src()),
 drill(["munach", "zakef_katon"], ["etnachta", "tipcha"]),
 mc("t2-1a", "Where is zakef katon written?", ["Above the word", "Below the word"], 0, "Zakef katon's two dots sit above the word.", JAC + " ⚑"),
 mc("t2-1b", "Which connector often leads into zakef katon?", ["Munach", "Tipcha", "Etnachta"], 0, "Munach. Tipcha and etnachta are rulers, not connectors.", JAC + " ⚑")]))
U2.append(lesson("tr2-2", "Zakef gadol", "zakef standing alone", "◌֕", [
 card("Zakef gadol is a ruler above the word: the two dots of zakef katon with a short vertical line beside them. It stands in for zakef katon when no connector comes before it.", JAC + " ⚑", "Zakef gadol"),
 card(f"It is rare: {cnt('zakef_gadol')} times in this app's verses. In every one, the word before it has no connector.", f"Genesis 2:9. {LIC}. {count_src()}", None, V("Genesis 2:9", hi=C["zakef_gadol"])),
 drill(["zakef_gadol"], ["zakef_katon", "munach"]),
 mc("t2-2a", "When does zakef gadol appear instead of zakef katon?", ["When no connector comes before it", "At the end of a verse", "On every first word"], 0, "Zakef gadol is the form of zakef used without a connector before it.", JAC + " ⚑")]))
U2.append(lesson("tr2-3", "Revia", "a smaller pause", "◌֗", [
 card("Revia is a ruler written above the word as a single diamond-shaped dot. Its pause is smaller than zakef katon's.", JAC + " ⚑", "Revia"),
 card(f"Munach leads into revia too ({seqn('munach','revia')} times in this app's verses). The same connector can serve different rulers.", f"{seq('munach','revia')}. {LIC}. {count_src()}", None, V(seq("munach", "revia"), hi=C["munach"] + C["revia"])),
 drill(["revia"], ["zakef_katon", "zakef_gadol", "munach"]),
 mc("t2-3a", "How is revia written?", ["One diamond-shaped dot above", "Two dots above", "A corner shape below"], 0, "Two dots above is zakef katon; the corner below is munach.", JAC + " ⚑")]))
U2.append(lesson("tr2-4", "Mahpach and pashta", "the pause before zakef", "◌֙", [
 card("Pashta is a ruler written above the last letter of the word, slanting to the left. It often comes right before zakef katon.", f"{JAC} ⚑. {seqn('pashta','zakef_katon')} times in this app's verses", "Pashta"),
 card(f"When the stress is not on the last syllable, pashta is written twice: once over the stressed syllable and once on the last letter. That happens {sum(t['he_t'].count(C['pashta']*1) and sum(w.count(C['pashta'])>1 for w in t['he_t'].split(' ')) for t in VERSES.values())} times in this app's verses.", JAC + " ⚑. " + count_src()),
 card(f"Mahpach is a connector written below the word, shaped like a sideways V. It often leads into pashta ({seqn('mahpach','pashta')} times here).", f"{seq('mahpach','pashta')}. {LIC}. {count_src()}", None, V(seq("mahpach", "pashta"), hi=C["mahpach"] + C["pashta"])),
 drill(["mahpach", "pashta"], ["munach", "zakef_katon"]),
 mc("t2-4a", "Where does pashta sit?", ["On the last letter of the word", "Under the first letter", "Over the stressed syllable only"], 0, "Pashta goes on the last letter, and on the stressed syllable too when that isn't last.", JAC + " ⚑"),
 mc("t2-4b", "Mahpach or munach: which is shaped like a sideways V?", ["Mahpach", "Munach"], 0, "Munach is the corner shape.", JAC + " ⚑")]))
U2.append(lesson("tr2-5", "Yetiv", "pashta's short stand-in", "◌֚", [
 card("Yetiv is a ruler written below the word, before its first letter. It takes pashta's place on some short words with no connector before them.", JAC + " ⚑", "Yetiv"),
 card(f"Yetiv looks a lot like mahpach. The difference is where it sits: yetiv comes before the first letter. It appears {cnt('yetiv')} times in this app's verses.", f"{seq('yetiv','zakef_katon')}. {LIC}. {count_src()}", None, V(seq("yetiv", "zakef_katon"), hi=C["yetiv"])),
 drill(["yetiv"], ["mahpach", "pashta", "munach"]),
 mc("t2-5a", "Yetiv and mahpach look alike. How do you tell them apart?", ["Yetiv sits before the first letter", "Yetiv is above the word", "Yetiv is always the last word"], 0, "Yetiv is placed before the word's first letter.", JAC + " ⚑")]))
U2.append(lesson("tr2-6", "Darga and tevir", "the pause before tipcha", "◌֛", [
 card(f"Tevir is a ruler written below the word. It often comes before tipcha ({seqn('tevir','tipcha')} times in this app's verses).", f"{JAC} ⚑. {count_src()}", "Tevir"),
 card(f"Darga is a connector below the word, shaped like a zigzag. It often leads into tevir ({seqn('darga','tevir')} times here). Mercha can lead into tevir too ({seqn('mercha','tevir')} times).", f"{seq('darga','tevir')}. {LIC}. {count_src()}", None, V(seq("darga", "tevir"), hi=C["darga"] + C["tevir"])),
 drill(["darga", "tevir"], ["mercha", "tipcha"]),
 mc("t2-6a", "Which ruler does tevir often come before?", ["Tipcha", "Zakef katon", "Revia"], 0, "Tevir usually precedes tipcha.", JAC + " ⚑. " + count_src()),
 mc("t2-6b", "Is darga a ruler or a connector?", ["A connector", "A ruler"], 0, "Darga is a connector; it leads into tevir.", JAC + " ⚑")]))
U2.append(lesson("tr2-7", "Kadma, geresh, gershayim", "kadma v'azla", "◌֜", [
 card("Geresh is a ruler written above the word, one slanted stroke. Gershayim is the same with two strokes. Both mark small pauses, and geresh often comes before revia.", f"{JAC} ⚑. {seqn('geresh','revia')} geresh-revia pairs in this app's verses", "Geresh"),
 card("Kadma is a connector with the same shape as pashta, but it sits over the stressed syllable, not the last letter. Kadma before geresh is a pair called kadma v'azla.", f"{seq('kadma','geresh')}. {LIC}. {JAC} ⚑", None, V(seq("kadma", "geresh"), hi=C["kadma"] + C["geresh"])),
 drill(["kadma", "geresh", "gershayim"], ["revia", "pashta"]),
 mc("t2-7a", "Kadma and pashta look the same. What tells them apart?", ["Where they sit: pashta on the last letter, kadma on the stressed syllable", "Kadma is below the word", "Pashta has two strokes"], 0, "Same shape, different position. Two strokes is gershayim.", JAC + " ⚑"),
 mc("t2-7b", "What is the pair kadma v'azla?", ["Kadma followed by geresh", "Two kadmas in a row", "Kadma followed by sof pasuk"], 0, "In this pair the geresh is called azla.", JAC + " ⚑")]))
U2.append(lesson("tr2-8", "Rarer marks", "segol, zarka, telishas, pazer, shalshelet", "◌֒", [
 card(f"These marks appear less often than the ones so far (together {sum(cnt(k) for k in ['segol','zarka','telisha_gedola','telisha_ketana','pazer','shalshelet'])} times in this app's verses). Learn their shapes now; the tunes come later.", count_src(), "Rarer marks"),
 card(f"Segol is a ruler of three dots above the last letter. Zarka, a zigzag above the last letter, often comes before it, as here.", f"{seq('zarka','segol')}. {LIC}. {JAC} ⚑", None, V(seq("zarka", "segol"), hi=C["zarka"] + C["segol"])),
 card("Telisha gedola is a ruler above the first letter of the word. Telisha ketana has a similar shape but is a connector, above the last letter. Pazer is a ruler above the word.", JAC + " ⚑"),
 card("Shalshelet, a zigzag above the word, is the rarest: it appears only four times in the Torah (Genesis 19:16, 24:12, 39:8 and Leviticus 8:23).", JAC + " ⚑"),
 drill(["segol", "zarka", "telisha_gedola", "telisha_ketana", "pazer", "shalshelet"], []),
 mc("t2-8a", "How many times does shalshelet appear in the Torah?", ["Four", "About forty", "Once"], 0, "Genesis 19:16, 24:12, 39:8 and Leviticus 8:23.", JAC + " ⚑"),
 mc("t2-8b", "Telisha gedola and telisha ketana: which is the connector?", ["Telisha ketana", "Telisha gedola"], 0, "Ketana (small) connects; gedola (big) is a ruler.", JAC + " ⚑")]))
units.append({"id": "u-trope2", "title": "Trope 2: The marks", "subtitle": "One lesson per family: shape, ruler or connector, and the marks it pairs with", "tiles": False, "lessons": U2})
for u in units:
    for l in u["lessons"]:
        for i in l["items"]: assert i in items, i
out = {"note": "Built by tools/gen_trope.py. Do not edit by hand.", "units": units, "items": items}
json.dump(out, open(os.path.join(ROOT, "data/trope.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("marks", len(MARKS), "items", len(items), "etnachta", n_et, "/", len(VERSES), no_et)
print({k: (v["ex"] or {}).get("ref") for k, v in items.items() if v["kind"] == "mark"})
