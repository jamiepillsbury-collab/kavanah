"""Rule-based transliteration of pointed Hebrew (Mishkan T'filah style).
Usage: from translit import tl; text, flagged = tl("בָּרוּךְ אַתָּה")
CLI:   python translit.py "עִבְרִית"
Style: ch = chet/chaf, tz = tzadi, tsere = ei, vocal sh'va = ', silent alef/ayin.
flagged=True when a vowel the rules can't settle is present (kamatz katan?, sh'va after long vowel).
Keep this file in tools/. Never hand-edit generated output; fix the rules or EXCEPT instead."""
import re, sys, unicodedata

SHEVA, HATAF_PATAH, HATAF_SEGOL, HATAF_QAMATS = "ְֱֲֳ"
HIRIQ, TSERE, SEGOL, PATAH, QAMATS, HOLAM, HOLAM_HASER_VAV, QUBUTS = "ִֵֶַָֹֺֻ"
DAGESH, SHIN_DOT, SIN_DOT, QAMATS_QATAN = "ׇּׁׂ"
VOWELS = {SHEVA: "", HATAF_PATAH: "a", HATAF_SEGOL: "e", HATAF_QAMATS: "o", HIRIQ: "i", TSERE: "ei", SEGOL: "e",
          PATAH: "a", QAMATS: "a", HOLAM: "o", HOLAM_HASER_VAV: "o", QUBUTS: "u", QAMATS_QATAN: "o"}
LONG = {QAMATS, TSERE, HOLAM, HOLAM_HASER_VAV}
CONS = {"א": "", "ב": "v", "ג": "g", "ד": "d", "ה": "h", "ו": "v", "ז": "z", "ח": "ch", "ט": "t", "י": "y",
        "כ": "ch", "ך": "ch", "ל": "l", "מ": "m", "ם": "m", "נ": "n", "ן": "n", "ס": "s", "ע": "", "פ": "f",
        "ף": "f", "צ": "tz", "ץ": "tz", "ק": "k", "ר": "r", "ש": "sh", "ת": "t"}
FIN = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}
HARD = {"ב": "b", "כ": "k", "ך": "k", "פ": "p", "ף": "p"}
# Whole-word exceptions (pointed form without cantillation -> transliteration). Add as needed.
EXCEPT = {"יְיָ": "Adonai", "יהוה": "Adonai", "יְהוָה": "Adonai", "יִשְׂרָאֵל": "Yisrael", "כָּל": "kol", "כׇּל": "kol",
          "וְכָל": "v'chol", "בְּכָל": "b'chol", "לְכָל": "l'chol", "כָל": "chol", "יְרוּשָׁלַיִם": "Y'rushalayim",
          "צָהֳרַיִם": "tzohorayim", "חׇכְמָה": "chochmah", "חָכְמָה": "chochmah", "שָׁלוֹם": "shalom",
          "מִצְוֹתָיו": "mitzvotav", "מֹשֶׁה": "Moshe", "בְּחָכְמָה": "b'chochmah", "מִצְוֹת": "mitzvot", "בְּמִצְוֹתָיו": "b'mitzvotav", "קָדְשֵׁנוּ": "kid'shanu",
          "קִדְּשָׁנוּ": "kid'shanu", "אֱלֹהֵינוּ": "Eloheinu", "יְהֹוָה": "Adonai", "אֲדֹנָי": "Adonai"}

# Added 2026-10-28 for blessings (Mishkan T'filah style; kamatz katan words resolved by hand)
EXCEPT.update({"בָּרְכוּ": "Bar'chu", "הַמְבֹרָךְ": "ham'vorach", "קָדְשׁוֹ": "kodsho", "קָדְשְׁךָ": "kodsh'cha",
    "וַיְהִי": "vay'hi", "וַיְכֻלּוּ": "vay'chulu", "וַיְכַל": "vay'chal", "וַיְבָרֶךְ": "vay'varech", "וַיְקַדֵּשׁ": "vay'kadeish",
    "וּבְמשֶׁה": "uv'Moshe", "וּבְמֹשֶׁה": "uv'Moshe", "וּבְיִשְׂרָאֵל": "uv'Yisrael", "מִצְרָיִם": "Mitzrayim", "הַתּוֹרָה": "haTorah",
    "בַּתּוֹרָה": "baTorah", "הַשַּׁבָּת": "haShabbat"})


def _letters(word):
    """Split a word into [letter, set(points)]."""
    out = []
    for ch in word:
        if "א" <= ch <= "ת": out.append([ch, set()])
        elif out and "ְ" <= ch <= "ׇ": out[-1][1].add(ch)
    return out

def _vowel(pts):
    for v in VOWELS:
        if v in pts: return v
    return None

def sep(out):
    """Separator before a voiced alef/ayin: none after a vocal sh'va, '-' after a vowel, ' after a closed syllable."""
    last = out[-1] if out else ""
    if not last or last.endswith("'"): return ""
    return "-" if last[-1] in "aeiou" else "'"

def word_tl(word):
    clean = "".join(c for c in word if not ("֑" <= c <= "֯") and c not in "ֽ׀׃")
    if clean in EXCEPT: return EXCEPT[clean], False
    for k in ("כָל", "כׇל", "כָּל", "כׇּל"):  # prefixed kol
        if clean.endswith(k) and len(clean) > len(k):
            head, _ = word_tl(clean[:-len(k)] + "ד")
            return head[:-1] + ("kol" if "\u05bc" in k else "chol"), False
    L = _letters(clean)
    n, out, flag = len(L), [], False
    i = 0
    prev_v = None  # vowel point of the previous consonant (None = none yet / word start)
    while i < n:
        c, p = L[i]
        nxt = L[i + 1] if i + 1 < n else None
        v = _vowel(p)
        # vav as vowel letter: shuruk / holam male
        if c == "ו" and v in (None, HOLAM) and (DAGESH in p or HOLAM in p) and (i == 0 or _vowel(L[i - 1][1]) is None):
            out.append("u" if DAGESH in p and HOLAM not in p else "o")
            prev_v = QAMATS if HOLAM in p else QUBUTS
            i += 1; continue
        if c == "ו" and HOLAM in p and i > 0 and _vowel(L[i-1][1]) is None:
            out.append("o"); prev_v = HOLAM; i += 1; continue
        # silent yod after hiriq/tsere/segol (vowel letter)
        if c == "י" and v is None and DAGESH not in p and prev_v in (HIRIQ, TSERE, SEGOL):
            i += 1; continue
        # silent he at end / mater; he with mappiq is pronounced
        if c == "ה" and v is None and DAGESH not in p and i == n - 1:
            if prev_v in (QAMATS, SEGOL): out.append("h")
            i += 1; continue
        # alef/ayin before a vowel-vav (ha-olam); else silent alef
        if c in "אע" and v is None and i > 0 and nxt and nxt[0] == "ו" and (DAGESH in nxt[1] or HOLAM in nxt[1]):
            out.append(sep(out)); i += 1; continue
        if c == "א" and v is None:
            i += 1; continue
        cons = CONS[c]
        if c in HARD and DAGESH in p: cons = HARD[c]
        if c == "ש": cons = "s" if SIN_DOT in p else "sh"
        if c in "אע" and v == SHEVA:
            prev_v = v; i += 1; continue
        if c in "אע" and v is not None and i > 0:
            cons = sep(out)
        # furtive patach on final chet/ayin/he-mappiq: vowel before consonant
        if i == n - 1 and v == PATAH and c in "חעה":
            out.append("a" + cons); i += 1; continue
        # yod after patach/qamats without vowel: diphthong ai (or 'av' for -ָיו)
        if c == "י" and v is None and i == n - 1 and prev_v in (QUBUTS, None):
            out.append("i"); i += 1; continue
        if c == "י" and v is None and DAGESH not in p and prev_v in (PATAH, QAMATS) and not (nxt and nxt[0] == "ו" and (DAGESH in nxt[1] or HOLAM in nxt[1])):
            if nxt and nxt[0] == "ו" and not nxt[1] and i + 1 == n - 1: out.append("v"); i += 2; continue
            out.append("i"); i += 1; continue
        vs = VOWELS.get(v, "") if v else ""
        if v == QAMATS and nxt and _vowel(nxt[1]) == SHEVA and i > 0:
            flag = True  # possible kamatz katan
        if v == SHEVA:
            vocal = (i == 0) or (prev_v == SHEVA and i > 1)
            if i == n - 1 or (nxt and _vowel(nxt[1]) == SHEVA and i + 1 == n - 1): vocal = False
            if prev_v in LONG and i > 0 and nxt is not None: flag = True
            if i > 0 and nxt and FIN.get(nxt[0], nxt[0]) == FIN.get(c, c): vocal = True  # hal'lu
            if i > 0 and DAGESH in p and prev_v not in (None, SHEVA): vocal = True  # dagesh forte
            if i == 1 and L[0][0] == "ו" and DAGESH in L[0][1] and not _vowel(L[0][1]): vocal = True  # uv'chol
            vs = "'" if vocal and nxt is not None else ""
        out.append(cons + vs)
        prev_v = v
        i += 1
    s = "".join(out)
    s = re.sub(r"'+", "'", s).replace("''", "'")
    if s.endswith("'"): s = s[:-1]
    return s, flag

def tl(text):
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[֑-ֽ֯׀]", "", text)  # cantillation, meteg, paseq
    text = text.replace("־", " ").replace("׃", ".")
    flagged, parts = False, []
    for tok in re.split(r"(\s+|-|[,.;:!?\"()])", text):
        if re.search(r"[א-ת]", tok or ""):
            w, f = word_tl(tok); parts.append(w); flagged |= f
        else:
            parts.append(tok or "")
    s = re.sub(r"\beloh", "Eloh", "".join(parts).strip()).replace("shabat", "Shabbat")
    return (s[:1].upper() + s[1:]), flagged

if __name__ == "__main__":
    for a in sys.argv[1:]: print(*tl(a))
