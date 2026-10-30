"""data/src/sefaria-*.json -> data/prayers.json.  Run: python tools/build_prayers.py
Hebrew + English come only from Sefaria (raw file). tl = translit.py. Nothing here is Claude-written text.
Line specs: (src, seg, part). he parts split on ':' and before a closing 'baruch'; en parts split before 'Blessed'.
REFORM holds marked Reform changes (none asserted yet) and CHECK holds questions for Jamie / cantor."""
import json, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from translit import tl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = json.load(open(os.path.join(ROOT, "data/src/sefaria-texts.json"), encoding="utf-8"))
raw2 = json.load(open(os.path.join(ROOT, "data/src/sefaria-shma.json"), encoding="utf-8"))
raw3 = json.load(open(os.path.join(ROOT, "data/src/sefaria-amidah.json"), encoding="utf-8"))
raw4 = json.load(open(os.path.join(ROOT, "data/src/sefaria-after-amidah.json"), encoding="utf-8"))
SRC = {}
for s in raw["sources"] + raw2["sources"] + raw3["sources"] + raw4["sources"]:
    SRC[("BARCHU_HE" if "Maariv, Barchu" in s["ref"] else None) or f'{s["ref"]}|{s["lang"]}'] = s
def key(ref, lang): return SRC.get(f"{ref}|{lang}")
S = {
 "barchu_he": SRC["BARCHU_HE"], "barchu_en": key("Siddur Ashkenaz, Weekday, Shacharit, Blessings of the Shema, Barchu", "en"),
 "torah_he": key("Siddur Sefard, Shabbat Morning Services, Blessings on Torah Reading", "he"),
 "torah_en": key("Siddur Sefard, Shabbat Morning Services, Blessings on Torah Reading", "en"),
 "haft_he": key("Siddur Sefard, Shabbat Morning Services, Haftarah Blessings", "he"),
 "haft_en": key("Siddur Sefard, Shabbat Morning Services, Haftarah Blessings", "en"),
 "cand_he": key("Siddur Sefard, Shabbat Candle Lighting", "he"), "cand_en": key("Siddur Sefard, Shabbat Candle Lighting", "en"),
 "kid_he": key("Siddur Ashkenaz, Shabbat, Shabbat Evening, Kiddush", "he"),
 "kid_en": key("Siddur Sefard, Shabbat Evening Meal, Shabbat Eve Kiddush", "en"), "gen_en": key("Genesis 2:1-3", "en"),
 "motzi_he": key("Siddur Ashkenaz, Berachot, Birkat Hanehenin, Eating, Barachot Rishonot", "he"),
 "sheh_he": key("Siddur Sefard, Blessings, Shehecheyanu", "he"),
 "deut_he": key("Deuteronomy 6:4-9", "he"), "deut_en": key("Deuteronomy 6:4-9", "en"),
 "num_he": key("Numbers 15:40-41", "he"), "num_en": key("Numbers 15:40-41", "en"),
 "bs_he": key("Siddur Ashkenaz, Weekday, Maariv, Blessings of the Shema, Shema (seg 4)", "he"),
 "ao_he": key("Siddur Ashkenaz, Shabbat, Maariv, Blessings of the Shema, Second Blessing before Shema", "he"), "ao_en": key("Siddur Ashkenaz, Shabbat, Maariv, Blessings of the Shema, Second Blessing before Shema", "en"),
 "mc_he": key("Siddur Ashkenaz, Shabbat, Maariv, Blessings of the Shema, First Blessing after Shema (segs 1-2)", "he"), "mc_en": key("Siddur Ashkenaz, Shabbat, Maariv, Blessings of the Shema, First Blessing after Shema (segs 1-2)", "en"),
 "ma_he": key("Siddur Ashkenaz, Shabbat, Maariv, Blessings of the Shema, First Blessing before Shema", "he"), "ma_en": key("Siddur Ashkenaz, Shabbat, Maariv, Blessings of the Shema, First Blessing before Shema", "en"),
 "hk_he": key("Siddur Ashkenaz, Shabbat, Maariv, Blessings of the Shema, Second Blessing after Shema", "he"), "hk_en": key("Siddur Ashkenaz, Shabbat, Maariv, Blessings of the Shema, Second Blessing after Shema", "en"),
 "ex_he": key("Exodus 31:16-17", "he"), "ex_en": key("Exodus 31:16-17", "en"),
 **{f"{k}_{l}": key(f"Siddur Ashkenaz, Shabbat, Maariv, Amidah, {n}", l) for k, n in
    (("av", "Patriarchs"), ("gv", "Divine Might"), ("kh", "Holines of God's Name"), ("ky", "Sanctity of the Day"), ("sr", "Peace")) for l in ("he", "en")},
 **{f"{k}_{l}": key(f"Siddur Ashkenaz, Shabbat, Maariv, {n}", l) for k, n in
    (("vc", "Vay'chulu"), ("me", "Me'ein Sheva"), ("al", "Aleinu")) for l in ("he", "en")},
 "bs_en": key("Siddur Ashkenaz, Weekday, Maariv, Blessings of the Shema, Shema (seg 4)", "en"),
}
NAME = "יְיָ"  # Mishkan T'filah prints the Name as yod-yod (display convention, not a wording change)

def clean_he(t):
    t = re.sub(r"^[^ְ-ׇ]*?:\s*(?=\S*[ְ-ׇ])", "", t)  # unpointed instruction prefix
    t = t.replace("‑", "").replace("יְהֹוָה", NAME).replace("יְהוָה", NAME).replace("יְיָ", NAME).replace("אֱלֹהֵינוּ", "אֱלֹהֵינוּ")
    t = t.replace("(", "").replace(")", "")
    t = re.sub(r"([א-ת])([֑-ׇ]*?)\u05BA", lambda m: m[0] if m[1] == "ו" else m[1] + m[2] + "\u05B9", t)  # holam haser (Metsudah) -> holam, except on vav
    t = re.sub(r"\.\s+(?=\S)(?!בָּרוּךְ)", ", ", t)  # mid-line periods read as commas
    return re.sub(r"\s+", " ", t).strip(" :.,")
def clean_en(t):
    t = re.sub(r"^(The [^:]{0,60}(says|repeats|responds)[^:]*|Recite (quietly|aloud)|\(When reciting Kiddush on wine\))\s*:?\s*", "", t)
    t = re.sub(r"\s*Recite aloud:\s*$", "", t)
    for a, b in (("יהוה", "Adonai"), ("Adonoy", "Adonai"), ("the Lord", "Adonai"), ("Shabbos", "Shabbat")): t = t.replace(a, b)
    t = re.sub(r"\s+", " ", t.replace("(", "").replace(")", "")).strip()
    return t[:1].upper() + t[1:]
def he_parts(t): return [p for p in re.split(r":\s*|[.]\s*(?=בָּרוּךְ)", t) if re.search(r"[ְ-ׇ]", p)]
def en_parts(t): return [p for p in re.split(r"(?<=\.)\s+(?=Blessed)", t) if p.strip()]
def sents(t): return [x for x in re.split(r"(?<=[.”])\s+(?=[“A-Z\[])", t) if x.strip()]
def get(spec, lang):
    if spec is None: return None
    if isinstance(spec, list): return " ".join(get(s, lang) for s in spec)
    src, seg, part = spec
    t = S[src]["text"][seg]
    if part == "s0": return clean_en(t.split(". ")[0]) + "."
    if isinstance(part, tuple) and part[0] == "w":  # Hebrew: colon-part k, words a..b
        return " ".join(he_parts(clean_he(t))[part[1]].split()[part[2]:part[3] + 1]).strip(" ,")
    if isinstance(part, tuple) and part[0] == "cut":  # English: from start text to end text (inclusive)
        a = t.index(part[1]); b = t.index(part[2], a) + len(part[2]); return clean_en(t[a:b]).rstrip(";,")
    if isinstance(part, tuple): return clean_en(" ".join(sents(t)[part[0]:part[1] + 1]))  # English sentences i..j
    if lang == "he": t = clean_he(t); return clean_he(he_parts(t)[part]) if part is not None else t
    t = clean_en(t); return clean_en(en_parts(t)[part]) if part is not None else t

# (he spec, en spec) per line. None = Sefaria has no English for this text yet.
PRAYERS = [
 ("hamotzi", "HaMotzi", "Blessing over bread", [(("motzi_he", 1, None), None)]),
 ("candles", "Shabbat candles", "Blessing for lighting Shabbat candles", [(("cand_he", 2, None), ("cand_en", 2, None))]),
 ("shehecheyanu", "Shehecheyanu", "Blessing for new and special moments", [(("sheh_he", 2, None), None)]),
 ("barchu", "Barchu", "Call to prayer and response", [(("barchu_he", 0, None), ("barchu_en", 0, None)), (("barchu_he", 1, None), ("barchu_en", 1, None))]),
 ("torah_before", "Torah blessing (before)", "Blessing before a Torah reading", [
   (("torah_he", 1, None), ("torah_en", 1, None)), (("torah_he", 2, None), ("torah_en", 2, None)),
   (("torah_he", 4, 0), ("torah_en", 4, 0)), (("torah_he", 4, 1), ("torah_en", 4, 1))]),
 ("torah_after", "Torah blessing (after)", "Blessing after a Torah reading", [(("torah_he", 6, 0), ("torah_en", 6, 0)), (("torah_he", 6, 1), ("torah_en", 6, 1))]),
 ("kiddush", "Kiddush (Shabbat evening)", "Sanctifying Shabbat over wine", [
   ([("kid_he", 1, None), ("kid_he", 3, 0)], [("kid_en", 3, None), ("kid_en", 4, "s0")]),
   (("kid_he", 3, 1), ("gen_en", 0, None)), (("kid_he", 3, 2), ("gen_en", 1, None)), (("kid_he", 3, 3), ("gen_en", 2, None)),
   (("kid_he", 4, None), ("kid_en", 5, None)), (("kid_he", 5, None), ("kid_en", 6, None)),
   (("kid_he", 6, 0), ("kid_en", 7, 0)), (("kid_he", 6, 1), ("kid_en", 7, 1))]),
 ("haftarah_before", "Haftarah blessing (before)", "Blessing before the reading from the Prophets", [(("haft_he", 1, 0), ("haft_en", 1, 0)), (("haft_he", 1, 1), ("haft_en", 1, 1))]),
 ("shma", "Sh'ma", "Hear, O Israel: the declaration of faith", [
   (("deut_he", 0, None), ("deut_en", 0, None)), (("bs_he", 0, None), ("bs_en", 0, None))]),
 ("vahavta", "V'ahavta", "You shall love: Deuteronomy 6:5-9 and Numbers 15:40-41", [
   *[(("deut_he", i, None), ("deut_en", i, None)) for i in range(1, 6)],
   (("num_he", 0, None), ("num_en", 0, None)), (("num_he", 1, None), ("num_en", 1, None))]),
 ("ahavat_olam", "Ahavat Olam", "Eternal love: the blessing before the Sh'ma (evening)", [
   (("ao_he", 0, i), ("ao_en", 0, se)) for i, se in enumerate([(0, 1), (2, 2), (3, 3), (4, 4), (5, 5)])]),
 ("mi_chamocha", "Mi Chamocha", "Who is like You: from the blessing after the Sh'ma (evening)", [
   (("mc_he", 0, 0), ("mc_en", 0, (0, 0))), (("mc_he", 0, 1), ("mc_en", 0, (1, 1))),
   (("mc_he", 1, 0), ("mc_en", 1, (0, 0))), (("mc_he", 1, 1), ("mc_en", 1, (1, 1))), (("mc_he", 1, 2), ("mc_en", 1, (2, 2)))]),
 ("maariv_aravim", "Ma'ariv Aravim", "Who brings on evening: the first blessing before the Sh'ma", [
   (("ma_he", 0, ("w", 0, 0, 12)), ("ma_en", 0, ("cut", "Blessed are You", "gates (of heaven)"))),
   (("ma_he", 0, ("w", 0, 13, 22)), ("ma_en", 0, ("cut", "and with understanding", "to His will."))),
   (("ma_he", 0, ("w", 1, 0, 9)), ("ma_en", 0, ("cut", "He creates day", "from before light"))),
   (("ma_he", 0, ("w", 1, 10, 21)), ("ma_en", 0, ("cut", "He causes day", "is His Name."))),
   (("ma_he", 0, ("w", 2, 0, 7)), ("ma_en", 0, ("cut", "The Almighty", "ever and ever."))),
   (("ma_he", 0, ("w", 3, 0, 4)), ("ma_en", 0, ("cut", "Blessed are You, Adonoy, Who", "evening.")))]),
 ("hashkiveinu", "Hashkiveinu", "Lay us down in peace: the evening prayer for protection", [
   (("hk_he", 0, ("w", 0, 0, 6)), ("hk_en", 0, ("cut", "Adonoy our God", "again to life"))),
   (("hk_he", 0, ("w", 0, 7, 17)), ("hk_en", 0, ("cut", "Spread over us", "Name’s sake."))),
   (("hk_he", 0, ("w", 0, 18, 26)), ("hk_en", 0, ("cut", "Shield us", "sorrow."))),
   (("hk_he", 0, ("w", 0, 27, 33)), ("hk_en", 0, ("cut", "Remove the adversary", "Your wings."))),
   (("hk_he", 0, ("w", 0, 34, 44)), ("hk_en", 0, ("cut", "For, Almighty, You", "merciful King."))),
   (("hk_he", 0, ("w", 0, 45, 52)), ("hk_en", 0, ("cut", "Guard our going", "now forever."))),
   (("hk_he", 0, ("w", 1, 0, 3)), ("hk_en", 0, ("cut", "And spread over us", "Your peace."))),
   (("hk_he", 0, ("w", 2, 0, 12)), ("hk_en", 0, ("cut", "Blessed are You", "Jerusalem.")))]),
 ("vshamru", "V'shamru", "Keeping Shabbat: Exodus 31:16-17", [
   (("ex_he", 0, None), ("ex_en", 0, None)), (("ex_he", 1, None), ("ex_en", 1, None))]),
 ("avot", "Avot v'Imahot", "Our ancestors: the first blessing of the Amidah", [
   (("av_he", 0, None), ("av_en", 0, None)),
   (("av_he", 1, ("w", 0, 0, 5)), ("av_en", 1, ("cut", "Blessed are You", "God of our fathers"))),
   (("av_he", 1, ("w", 0, 6, 11)), ("av_en", 1, ("cut", "God of Abraham", "God of Jacob"))),
   (("av_he", 1, ("w", 0, 12, 22)), ("av_en", 1, ("cut", "the Almighty, the Great", "possesses everything"))),
   (("av_he", 1, ("w", 0, 23, 32)), ("av_en", 1, ("cut", "Who remembers", "with love."))),
   (("av_he", 3, 0), ("av_en", 3, ("cut", "King, Helper", "Shield."))),
   (("av_he", 3, 1), ("av_en", 3, ("cut", "Blessed are You", "Abraham.")))]),
 ("gvurot", "G'vurot", "God's power: the second blessing of the Amidah", [
   (("gv_he", 0, None), ("gv_en", 0, None)),
   (("gv_he", 1, 0), ("gv_en", 1, ("cut", "Causer of the wind", "to fall."))),
   (("gv_he", 1, 1), ("gv_en", 1, ("cut", "He causes the dew", "descend."))),
   (("gv_he", 2, ("w", 0, 0, 6)), ("gv_en", 2, ("cut", "Sustainer", "great mercy"))),
   (("gv_he", 2, ("w", 0, 7, 16)), ("gv_en", 2, ("cut", "Supporter", "the dust."))),
   (("gv_he", 2, ("w", 0, 17, 28)), ("gv_en", 2, ("cut", "Who is like You", "sprout forth."))),
   (("gv_he", 4, 0), ("gv_en", 4, ("cut", "And You are faithful", "to life."))),
   (("gv_he", 4, 1), ("gv_en", 4, ("cut", "Blessed are You", "the dead.")))]),
 ("kdushat_hashem", "K'dushat HaShem", "God's holiness: the third blessing of the Amidah (evening)", [
   (("kh_he", 0, 0), ("kh_en", 0, ("cut", "You are holy", "forever."))),
   (("kh_he", 0, 1), ("kh_en", 0, ("cut", "Blessed are You", "the Holy One.")))]),
 ("kdushat_hayom", "K'dushat HaYom", "The holiness of Shabbat: R'tzei vimnuchateinu (evening)", [
   (("ky_he", 2, ("w", 0, 0, 4)), ("ky_en", 2, ("cut", "Our God", "with our rest"))),
   (("ky_he", 2, ("w", 0, 5, 11)), ("ky_en", 2, ("cut", "sanctify us", "Your goodness"))),
   (("ky_he", 2, ("w", 0, 12, 17)), ("ky_en", 2, ("cut", "and gladden us", "in truth."))),
   (("ky_he", 2, ("w", 0, 18, 24)), ("ky_en", 2, ("cut", "And give us", "holy Shabbos"))),
   (("ky_he", 2, ("w", 0, 25, 29)), ("ky_en", 2, ("cut", "and may Israel", "Your Name."))),
   (("ky_he", 2, 1), ("ky_en", 2, ("cut", "Blessed are You Adonoy, Sanctifier", "Shabbos.")))]),
 ("shalom_rav", "Shalom Rav", "Abundant peace: the last blessing of the Amidah (evening)", [
   (("sr_he", 0, ("w", 0, 0, 6)), ("sr_en", 0, ("cut", "Bestow", "forever."))),
   (("sr_he", 0, ("w", 0, 7, 12)), ("sr_en", 0, ("cut", "For You are King", "all peace."))),
   (("sr_he", 0, ("w", 0, 13, 20)), ("sr_en", 0, ("cut", "And may it be good", "Your peace."))),
   (("sr_he", 2, None), ("sr_en", 2, None))]),
 ("vaychulu", "Vay'chulu", "Genesis 2:1-3: heaven and earth completed, and the seventh day", [
   (("vc_he", 1, 0), ("vc_en", 1, ("cut", "And the heavens", "all their hosts."))),
   (("vc_he", 1, 1), ("vc_en", 1, ("cut", "And God completed", "He had done."))),
   (("vc_he", 1, 2), ("vc_en", 1, ("cut", "And God blessed", "created to do.")))]),
 ("magen_avot", "Magen Avot", "The Amidah in brief, said together after it (from Me'ein Sheva)", [
   (("me_he", 3, ("w", 0, 0, 5)), ("me_en", 3, ("cut", "Shield of", "His utterance"))),
   ([("me_he", 3, ("w", 0, 6, 7)), ("me_he", 3, ("w", 0, 10, 21))],
    [("me_en", 3, ("cut", "the Almighty, the Holy One", "the Holy One")), ("me_en", 3, ("cut", "Who has no peer", "grant them rest."))]),
   (("me_he", 3, ("w", 0, 22, 32)), ("me_en", 3, ("cut", "Before Him", "the blessings."))),
   (("me_he", 3, 1), ("me_en", 3, ("cut", "Almighty of thanksgiving", "creation.")))]),
 ("aleinu", "Aleinu", "Our duty to praise: the closing prayer", [
   (("al_he", 0, ("w", 0, 0, 7)), ("al_en", 0, ("cut", "It is our obligation", "beginning"))),
   (("al_he", 0, ("w", 0, 8, 15)), ("al_en", 0, ("cut", "that He has not made us", "families of the earth"))),
   (("al_he", 0, ("w", 0, 16, 22)), ("al_en", 0, ("cut", "that He has not assigned", "multitudes."))),
   (("al_he", 0, ("w", 1, 0, 19)), ("al_en", 0, ("cut", "But we bow", "blessed is He"))),
   (("al_he", 0, ("w", 1, 20, 32)), ("al_en", 0, ("cut", "Who spreads", "loftiest heights."))),
   (("al_he", 0, ("w", 1, 33, 42)), ("al_en", 0, ("cut", "He is our God", "His Torah"))),
   (("al_he", 0, ("w", 1, 43, 58)), ("al_en", 0, ("cut", "And You shall know", "nothing else."))),
   (("al_he", 1, 2), ("al_en", 1, ("cut", "And it is said", "His Name One.")))]),
]
# Marked Reform changes vs the traditional base (Mishkan T'filah wording). "sub" = (traditional Hebrew, Reform Hebrew) applied to that line.
# Added words: names from Genesis (Sefaria, Miqra al pi ha-Masorah), g'ulah Lev 25:24, ezrat Judg 5:23, hakol from this blessing. Not sourced: imoteinu, imahot.
# English stays the traditional Metsudah translation (no Claude-written English), so it lacks these additions.
IMOT = ("וֵאלֹהֵי אֲבוֹתֵינוּ", "וֵאלֹהֵי אֲבוֹתֵינוּ וְאִמּוֹתֵינוּ")
REFORM = {
 "avot": [{"line": 1, "change": "Adds v'imoteinu (and our mothers).", "sub": IMOT},
          {"line": 2, "change": "Adds Elohei Sarah, Elohei Rivkah, Elohei Rachel v'Elohei Leah.", "sub": ("וֵאלֹהֵי יַעֲקֹב", "וֵאלֹהֵי יַעֲקֹב אֱלֹהֵי שָׂרָה אֱלֹהֵי רִבְקָה אֱלֹהֵי רָחֵל וֵאלֹהֵי לֵאָה")},
          {"line": 4, "change": "Adds v'imahot (and mothers).", "sub": ("חַסְדֵי אָבוֹת", "חַסְדֵי אָבוֹת וְאִמָּהוֹת")},
          {"line": 4, "change": "G'ulah (redemption) instead of go'el (a redeemer).", "sub": ("גוֹאֵל", "גְאֻלָּה")},
          {"line": 6, "change": "Adds v'ezrat Sarah (and Sarah's help).", "sub": ("מָגֵן אַבְרָהָם", "מָגֵן אַבְרָהָם וְעֶזְרַת שָׂרָה")}],
 "gvurot": [{"line": 0, "change": "M'chayeih hakol (gives life to all) instead of m'chayeh meitim (revives the dead).", "sub": ("מְחַיֶּה מֵתִים", "מְחַיֵּה הַכֹּל")},
            {"line": 3, "change": "M'chayeih hakol instead of m'chayeih meitim.", "sub": ("מְחַיֵּה מֵתִים", "מְחַיֵּה הַכֹּל")},
            {"line": 6, "change": "L'hachayot hakol instead of l'hachayot meitim.", "sub": ("לְהַחֲיוֹת מֵתִים", "לְהַחֲיוֹת הַכֹּל")},
            {"line": 7, "change": "M'chayeih hakol instead of m'chayeih hameitim.", "sub": ("מְחַיֵּה הַמֵּתִים", "מְחַיֵּה הַכֹּל")}],
 "kdushat_hayom": [{"line": 0, "change": "Adds v'imoteinu (and our mothers).", "sub": IMOT}],
 "magen_avot": [{"line": 0, "change": "Adds v'imahot: Magen avot v'imahot (shield of fathers and mothers).", "sub": ("מָגֵן אָבוֹת", "מָגֵן אָבוֹת וְאִמָּהוֹת")},
                {"line": 0, "change": "M'chayeih hakol instead of m'chayeih meitim.", "sub": ("מְחַיֵּה מֵתִים", "מְחַיֵּה הַכֹּל")}],
 "aleinu": [{"line": 3, "change": "Leaves out 'shehem mishtachavim lahevel varik umitpal'lim el el lo yoshia' (many traditional Ashkenazi siddurim also omit it).",
             "sub": ("שֶׁהֵם מִשְׁתַּחֲוִים לָהֶבֶל וָרִיק וּמִתְפַּלְּלִים אֶל אֵל לֹא יוֹשִׁיעַ, ", "")}],
}
UNIT = {"vaychulu": "concluding", "magen_avot": "concluding", "aleinu": "concluding", **{k: "amidah" for k in ("avot", "gvurot", "kdushat_hashem", "kdushat_hayom", "shalom_rav")}, "maariv_aravim": "shma", "hashkiveinu": "shma", "vshamru": "shma", "shma": "shma", "vahavta": "shma", "ahavat_olam": "shma", "mi_chamocha": "shma"}
SEQ = {"maariv_aravim": 7.2, "ahavat_olam": 7.5}  # display order (Mishkan T'filah); "order" stays append-only so words.json ids stay stable  # app groups lessons into units by this
CHECK = {
 "candles": ["Mishkan T'filah wording: confirm 'l'hadlik ner shel Shabbat' matches your siddur."],
 "torah_before": ["Mishkan T'filah: 'mikol ha-amim' or 'im kol ha-amim'? (line 3)"],
 "kiddush": ["Does Mishkan T'filah include 'Vay'hi erev vay'hi voker' and 'Savri maranan'?",
             "Mishkan T'filah wording of 'ki vanu vacharta v'otanu kidashta mikol ha-amim'?",
             "Line 1 English joins two Metsudah pieces; Genesis lines use Contemporary Torah."],
 "shma": ["Hebrew line 1: Deuteronomy 6:4 (Miqra according to the Masorah, CC-BY-SA). Line 2 from the Metsudah siddur.",
          "Baruch shem: does CBB say it aloud or quietly? (Mishkan T'filah prints it in smaller type.)"],
 "vahavta": ["Mishkan T'filah goes from Deut 6:9 straight to 'L'ma'an tizk'ru' (Num 15:40-41), skipping Deut 11:13-21 and Num 15:37-39. Confirm, then mark as a Reform change.",
             "Hebrew is the Torah text: kamatz katan printed as its own sign in b'chol (it reads 'o'). English: Contemporary Torah (CC-BY-NC)."],
 "ahavat_olam": ["Evening (Ma'ariv) text, Metsudah siddur. Confirm Mishkan T'filah wording, esp. 'v'ahavat'cha al tasir mimenu l'olamim'.",
                 "Line 1 English joins two Metsudah sentences."],
 "mi_chamocha": ["Starts at 'Mi chamocha'; the Emet ve-emunah lines before it are not included yet (Mishkan T'filah shortens them).",
                 "Confirm Mishkan T'filah has 'V'ne-emar: ki fadah...' before the closing blessing."],
 "maariv_aravim": ["Evening text, Metsudah siddur. Confirm Mishkan T'filah wording."],
 "hashkiveinu": ["Shabbat evening form (ends 'haporeis sukat shalom'). Does Mishkan T'filah keep 'v'haseir mei-aleinu oyeiv, dever v'cherev v'ra-av v'yagon' and 'v'haseir satan'?",
                 "Line 1 English: Metsudah has no period after 'to life'."],
 "vshamru": ["Torah text (Exodus 31:16-17). English: Contemporary Torah (CC-BY-NC)."],
 "avot": ["Hebrew base: Metsudah siddur (traditional). Reform wording added from Mishkan T'filah as I know it; please check each marked line, and the vowels of v'imoteinu and v'imahot (no Sefaria source for those two words).",
          "English is the traditional Metsudah translation, so it doesn't mention the matriarchs. Add your own if you like.",
          "The Ten Days of Repentance insert (Zochreinu) is left out."],
 "gvurot": ["Mishkan T'filah prints m'chayeih hakol with m'chayeih meitim as an option. Which does CBB say?",
            "Lines 2-3 are seasonal: mashiv haruach (winter) or morid hatal (summer). Does CBB say morid hatal year-round, or switch?",
            "English is Metsudah's 'Resurrector of the dead'; it doesn't match hakol."],
 "kdushat_hashem": ["Evening form (no K'dushah). Ten Days ending (hamelech hakadosh) left out."],
 "kdushat_hayom": ["Only R'tzei vimnuchateinu is here. Does Mishkan T'filah's Shabbat evening K'dushat HaYom also have Atah kidashta, Vay'chulu, or Yism'chu?"],
 "shalom_rav": ["Does Mishkan T'filah's Shalom Rav add 'v'al kol yoshvei teiveil' (and all who live on earth)?",
                "Ten Days insert (B'sefer chayim) left out. Ending: ham'vareich et amo Yisrael bashalom."],
 "vaychulu": ["Torah text (Genesis 2:1-3), as printed in the Metsudah siddur. Mishkan T'filah also has it in the Kiddush; same wording?",
              "Does CBB say Vay'chulu after the Amidah, or only in Kiddush?"],
 "magen_avot": ["Only the Magen Avot paragraph of Me'ein Sheva is here (not the opening 'Baruch atah... koneih shamayim va-aretz' or the closing R'tzei). Does Mishkan T'filah print more?",
                "Ten Days word (hamelech hakadosh) left out.",
                "English is Metsudah's 'Resurrector of the dead' and 'fathers'; it doesn't match hakol or v'imahot."],
 "aleinu": ["Does Mishkan T'filah offer the alternative first paragraph ('shenatan lanu torat emet, v'chayei olam nata b'tocheinu') in place of 'shelo asanu k'goyei ha-aratzot...'? Which does CBB sing?",
            "The second paragraph (Al kein n'kaveh) is left out; only its closing V'ne-emar line is here. Does Mishkan T'filah or CBB include Al kein?",
            "'Hu Eloheinu ein od... v'yadata hayom' (lines 6-7) kept from the traditional text. Confirm Mishkan T'filah prints them."],
 "hamotzi": ["No Sefaria English found for this text."],
 "shehecheyanu": ["No Sefaria English found for this text."],
}

out = {"generated_by": "tools/build_prayers.py", "source_fetched": raw["fetched"], "prayers": []}
for order, (pid, title, about, lines) in enumerate(PRAYERS):
    pl = []
    for i, (hs, es) in enumerate(lines):
        he = get(hs, "he"); rf = [r for r in REFORM.get(pid, []) if r["line"] == i]
        for r in rf:
            assert he.count(r["sub"][0]) == 1, (pid, i, r["sub"][0]); he = he.replace(*r["sub"])
        t, f = tl(he)
        src = None if es is None else (es[0] if isinstance(es, tuple) else es[0][0])
        pl.append({"he": he, "tl": t, "tlf": f, "en": get(es, "en"),
                   "en_src": S[src]["version"] if src else None, "en_license": S[src]["license"] if src else None,
                   "reform": [r["change"] for r in rf], "verify": True})
    hs0 = lines[0][0] if isinstance(lines[0][0], tuple) else lines[0][0][0]
    out["prayers"].append({"id": pid, "title": title, "about": about, "order": order, "audio": None,
        "he_src": f'{S[hs0[0]]["ref"]} ({S[hs0[0]]["version"]}, {S[hs0[0]]["license"]})',
        "unit": UNIT.get(pid, "blessings"), "seq": SEQ.get(pid, order), "check": CHECK.get(pid, []) + [f'Line {r["line"] + 1}, Reform change: {r["change"]} Confirm against Mishkan T\'filah.' for r in REFORM.get(pid, [])], "lines": pl})
json.dump(out, open(os.path.join(ROOT, "data/prayers.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for p in out["prayers"]:
    print(p["id"])
    for l in p["lines"]: print("  ", ("F " if l["tlf"] else "  ") + l["tl"], "|", (l["en"] or "-")[:70])
