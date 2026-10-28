#!/usr/bin/env python3
"""Generate data/alefbet.json: letters, vowels, and syllable drills.
Run from the app folder:  python tools/gen_alefbet.py
Pronunciation: modern Israeli/Sephardi, as used in Reform congregations.
Transliteration follows Mishkan T'filah style (ch, tz, ' for vocal sheva).
"""
import json, random, os

DAG, SHIN, SIN = "ּ", "ׁ", "ׂ"

# id, char, name, sound, translit, note, look-alike group
LETTERS = [
    ("alef", "א", "Alef", "silent", "", "Carries a vowel; makes no sound itself.", None),
    ("bet", "ב" + DAG, "Bet", "b", "b", "Dot inside (dagesh) = b.", "bk"),
    ("vet", "ב", "Vet", "v", "v", "No dot = v.", "bk"),
    ("gimel", "ג", "Gimel", "g", "g", "Hard g, as in 'go'.", "gn"),
    ("dalet", "ד", "Dalet", "d", "d", "Corner sticks out at top right.", "dr"),
    ("he", "ה", "Hei", "h", "h", "Gap at top left; often silent at word end.", "hct"),
    ("vav", "ו", "Vav", "v", "v", "Also a vowel carrier (o, u).", "vzn"),
    ("zayin", "ז", "Zayin", "z", "z", "Head sticks out both sides.", "vzn"),
    ("chet", "ח", "Chet", "ch", "ch", "Throaty ch, as in 'Bach'. No gap at top.", "hct"),
    ("tet", "ט", "Tet", "t", "t", "Curls in at top left.", "tm"),
    ("yod", "י", "Yod", "y", "y", "Smallest letter; floats high.", None),
    ("kaf", "כ" + DAG, "Kaf", "k", "k", "Dot inside = k.", "bk"),
    ("khaf", "כ", "Chaf", "ch", "ch", "No dot = ch. Rounded back.", "bk"),
    ("khaf-sofit", "ך", "Chaf sofit", "ch", "ch", "Final form: only at word end.", "vzn"),
    ("lamed", "ל", "Lamed", "l", "l", "Only letter that rises above the line.", None),
    ("mem", "מ", "Mem", "m", "m", "Small gap at bottom left.", "tm"),
    ("mem-sofit", "ם", "Mem sofit", "m", "m", "Final form: closed box.", "sm"),
    ("nun", "נ", "Nun", "n", "n", "Narrow, with a flat base.", "gn"),
    ("nun-sofit", "ן", "Nun sofit", "n", "n", "Final form: long, drops below the line.", "vzn"),
    ("samekh", "ס", "Samech", "s", "s", "Round, closed.", "sm"),
    ("ayin", "ע", "Ayin", "silent", "", "Carries a vowel; silent in most Reform pronunciation.", "at"),
    ("pe", "פ" + DAG, "Pei", "p", "p", "Dot inside = p.", "pf"),
    ("fe", "פ", "Fei", "f", "f", "No dot = f.", "pf"),
    ("fe-sofit", "ף", "Fei sofit", "f", "f", "Final form: drops below the line.", "pf"),
    ("tzadi", "צ", "Tzadi", "tz", "tz", "tz, as in 'cats'.", "at"),
    ("tzadi-sofit", "ץ", "Tzadi sofit", "tz", "tz", "Final form: drops below the line.", "at"),
    ("kuf", "ק", "Kuf", "k", "k", "Leg drops below the line.", None),
    ("resh", "ר", "Resh", "r", "r", "Rounded corner (compare Dalet).", "dr"),
    ("shin", "ש" + SHIN, "Shin", "sh", "sh", "Dot on the right = sh.", "ss"),
    ("sin", "ש" + SIN, "Sin", "s", "s", "Dot on the left = s.", "ss"),
    ("tav", "ת", "Tav", "t", "t", "Foot at bottom left.", "hct"),
]
LETTER_LESSONS = [
    ("Letters 1", ["alef", "bet", "vet", "gimel", "dalet"]),
    ("Letters 2", ["he", "vav", "zayin", "chet", "tet"]),
    ("Letters 3", ["yod", "kaf", "khaf", "khaf-sofit", "lamed"]),
    ("Letters 4", ["mem", "mem-sofit", "nun", "nun-sofit", "samekh"]),
    ("Letters 5", ["ayin", "pe", "fe", "fe-sofit", "tzadi", "tzadi-sofit"]),
    ("Letters 6", ["kuf", "resh", "shin", "sin", "tav"]),
]

# id, mark (combining or suffix), name, sound, translit, note, flag
V = "◌"  # dotted circle placeholder
VOWELS = [
    ("patach", "ַ", "Patach", "a (father)", "a", "Line under the letter.", None),
    ("kamatz", "ָ", "Kamatz", "a (father)", "a", "T-shape under the letter.",
     "Sometimes read 'o' (kamatz katan); flagged per word later."),
    ("segol", "ֶ", "Segol", "e (bed)", "e", "Three dots in a triangle.", None),
    ("tzere", "ֵ", "Tzere", "e (they)", "e", "Two dots side by side.",
     "Before yod, Mishkan T'filah transliterates as 'ei' (e.g. Eloheinu)."),
    ("hiriq", "ִ", "Chirik", "i (ski)", "i", "One dot below.", None),
    ("hiriq-yod", "ִי", "Chirik yod", "i (ski)", "i", "Dot below, then yod.", None),
    ("holam", "ֹ", "Cholam", "o (go)", "o", "Dot above, top left.", None),
    ("holam-vav", "וֹ", "Cholam vav", "o (go)", "o", "Vav with a dot on top.", None),
    ("kubutz", "ֻ", "Kubutz", "u (flute)", "u", "Three diagonal dots below.", None),
    ("shuruk", "וּ", "Shuruk", "u (flute)", "u", "Vav with a dot in its middle.", None),
    ("sheva", "ְ", "Sh'va", "silent or quick e", "'", "Two dots stacked.",
     "Vocal vs. silent sh'va varies; Mishkan T'filah marks vocal with an apostrophe."),
    ("hataf-patach", "ֲ", "Chataf patach", "short a", "a", "Sh'va + patach.", None),
    ("hataf-segol", "ֱ", "Chataf segol", "short e", "e", "Sh'va + segol.", None),
    ("hataf-kamatz", "ֳ", "Chataf kamatz", "short o", "o", "Sh'va + kamatz.", None),
]
VOWEL_LESSONS = [
    ("Vowels: a", ["patach", "kamatz"]),
    ("Vowels: e", ["segol", "tzere"]),
    ("Vowels: i", ["hiriq", "hiriq-yod"]),
    ("Vowels: o", ["holam", "holam-vav"]),
    ("Vowels: u", ["kubutz", "shuruk"]),
    ("Sh'va & short vowels", ["sheva", "hataf-patach", "hataf-segol", "hataf-kamatz"]),
]
# consonants allowed to carry syllable vowels (no finals; hataf only on gutturals)
SYL_LETTERS = ["alef", "bet", "vet", "gimel", "dalet", "he", "vav", "zayin", "chet", "tet",
               "yod", "kaf", "khaf", "lamed", "mem", "nun", "samekh", "ayin", "pe", "fe",
               "tzadi", "kuf", "resh", "shin", "sin", "tav"]
GUTTURALS = ["alef", "he", "chet", "ayin"]
SUFFIX_VOWELS = {"hiriq-yod", "holam-vav", "shuruk"}

# "say": Hebrew text the phone's Hebrew voice (speechSynthesis) reads aloud. A recording in "audio" overrides it.
# Letters say their name; vowels are said on alef. Some names are respelled phonetically (vet, chaf) so the voice
# doesn't read them as bet/kaf. FLAG: TTS may still blur b/v, k/ch, p/f -- check by ear; record replacements if wrong.
SAY_LETTER = {
    "alef": "אָלֶף", "bet": "בֵּית", "vet": "וֵית", "gimel": "גִּימֶל", "dalet": "דָּלֶת", "he": "הֵא",
    "vav": "וָו", "zayin": "זַיִן", "chet": "חֵית", "tet": "טֵית", "yod": "יוֹד", "kaf": "כַּף",
    "khaf": "חָף", "khaf-sofit": "חָף סוֹפִית", "lamed": "לָמֶד", "mem": "מֵם", "mem-sofit": "מֵם סוֹפִית",
    "nun": "נוּן", "nun-sofit": "נוּן סוֹפִית", "samekh": "סָמֶךְ", "ayin": "עַיִן", "pe": "פֵּא",
    "fe": "פֵא", "fe-sofit": "פֵא סוֹפִית", "tzadi": "צָדִי", "tzadi-sofit": "צָדִי סוֹפִית",
    "kuf": "קוֹף", "resh": "רֵישׁ", "shin": "שִׁין", "sin": "שִׂין", "tav": "תָּו",
}
SAY_VOWEL = {"patach": "אַ", "kamatz": "אָ", "segol": "אֶ", "tzere": "אֵ", "hiriq": "אִ", "hiriq-yod": "אִי",
             "holam": "אֹ", "holam-vav": "אוֹ", "kubutz": "אֻ", "shuruk": "אוּ", "sheva": None,
             "hataf-patach": "אֲ", "hataf-segol": "אֱ", "hataf-kamatz": "אֳ"}
# Syllables the voice is likely to misread (no-dagesh v/ch/f, sh'va) get no voice until recorded.
NO_SAY_LETTERS = {"vet", "khaf", "fe"}

def main():
    random.seed(18)
    items, units = {}, []
    L = {r[0]: r for r in LETTERS}
    for lid, ch, name, sound, tr, note, grp in LETTERS:
        items["l-" + lid] = dict(kind="letter", he=ch, name=name, sound=sound, tr=tr,
                                 note=note, group=grp, say=SAY_LETTER[lid], audio=None)
    for vid, mark, name, sound, tr, note, flag in VOWELS:
        disp = V + mark if vid not in SUFFIX_VOWELS else V + mark
        items["v-" + vid] = dict(kind="vowel", he=disp, name=name, sound=sound, tr=tr,
                                 note=note, flag=flag, say=SAY_VOWEL[vid], audio=None)

    units.append(dict(id="u-letters", title="The Alef-Bet",
                      subtitle="Letters, final forms, and dot-pairs",
                      lessons=[dict(id=f"letters-{i+1}", title=t, items=["l-" + x for x in ids])
                               for i, (t, ids) in enumerate(LETTER_LESSONS)]))

    vlessons = []
    for i, (t, vids) in enumerate(VOWEL_LESSONS):
        ids = ["v-" + v for v in vids]
        syls = []
        for vid in vids:
            pool = GUTTURALS if vid.startswith("hataf") else [x for x in SYL_LETTERS if not (vid == "sheva" and x in GUTTURALS)]
            picks = random.sample(pool, min(4, len(pool)))
            vrow = next(r for r in VOWELS if r[0] == vid)
            for lid in picks:
                _, ch, lname, _, ltr, _, _ = L[lid]
                if (vid == "holam" and lid in ("shin", "sin", "vav")) or (vid == "holam-vav" and lid == "vav"):
                    continue  # holam merges with shin/sin dot / vav; avoid ambiguity
                he = ch + vrow[1]
                tr = ltr + vrow[4]
                sid = f"s-{vid}-{lid}"
                items[sid] = dict(kind="syllable", he=he, tr=tr,
                                  hint=f"{ch} {lname} ({ltr or 'silent'}) + {vrow[2]} ({vrow[4]})",
                                  say=None if (lid in NO_SAY_LETTERS or vid == "sheva") else he,
                                  audio=None)
                syls.append(sid)
        vlessons.append(dict(id=f"vowels-{i+1}", title=t, items=ids + syls))
    units.append(dict(id="u-vowels", title="Vowels (Nikkud)",
                      subtitle="Reading letters with vowels", lessons=vlessons))

    out = dict(version=1, generated_by="tools/gen_alefbet.py", units=units, items=items)
    path = os.path.join(os.path.dirname(__file__), "..", "data", "alefbet.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"{len(items)} items, {sum(len(u['lessons']) for u in units)} lessons -> {path}")

if __name__ == "__main__":
    main()
