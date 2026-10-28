"""data/src/sefaria-texts.json -> data/prayers.json.  Run: python tools/build_prayers.py
Hebrew + English come only from Sefaria (raw file). tl = translit.py. Nothing here is Claude-written text.
Line specs: (src, seg, part). he parts split on ':' and before a closing 'baruch'; en parts split before 'Blessed'.
REFORM holds marked Reform changes (none asserted yet) and CHECK holds questions for Jamie / cantor."""
import json, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from translit import tl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = json.load(open(os.path.join(ROOT, "data/src/sefaria-texts.json"), encoding="utf-8"))
SRC = {}
for s in raw["sources"]:
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
}
NAME = "יְיָ"  # Mishkan T'filah prints the Name as yod-yod (display convention, not a wording change)

def clean_he(t):
    t = re.sub(r"^[^ְ-ׇ]*?:\s*(?=\S*[ְ-ׇ])", "", t)  # unpointed instruction prefix
    t = t.replace("‑", "").replace("יְהֹוָה", NAME).replace("יְהוָה", NAME).replace("יְיָ", NAME).replace("אֱלֹהֵינוּ", "אֱלֹהֵינוּ")
    t = t.replace("(", "").replace(")", "")
    t = re.sub(r"\.\s+(?=\S)(?!בָּרוּךְ)", ", ", t)  # mid-line periods read as commas
    return re.sub(r"\s+", " ", t).strip(" :.,")
def clean_en(t):
    t = re.sub(r"^(The [^:]{0,60}(says|repeats|responds)[^:]*|Recite (quietly|aloud)|\(When reciting Kiddush on wine\))\s*:?\s*", "", t)
    t = re.sub(r"\s*Recite aloud:\s*$", "", t)
    for a, b in (("Adonoy", "Adonai"), ("the Lord", "Adonai"), ("Shabbos", "Shabbat")): t = t.replace(a, b)
    return re.sub(r"\s+", " ", t.replace("(", "").replace(")", "")).strip()
def he_parts(t): return [p for p in re.split(r":\s*|[.]\s*(?=בָּרוּךְ)", t) if re.search(r"[ְ-ׇ]", p)]
def en_parts(t): return [p for p in re.split(r"(?<=\.)\s+(?=Blessed)", t) if p.strip()]
def get(spec, lang):
    if spec is None: return None
    if isinstance(spec, list): return " ".join(get(s, lang) for s in spec)
    src, seg, part = spec
    t = S[src]["text"][seg]
    if part == "s0": return clean_en(t.split(". ")[0]) + "."
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
]
# Marked Reform changes vs the traditional base (Mishkan T'filah). Add {"line": i, "change": "..."} here once confirmed.
REFORM = {}
CHECK = {
 "candles": ["Mishkan T'filah wording: confirm 'l'hadlik ner shel Shabbat' matches your siddur."],
 "torah_before": ["Mishkan T'filah: 'mikol ha-amim' or 'im kol ha-amim'? (line 3)"],
 "kiddush": ["Does Mishkan T'filah include 'Vay'hi erev vay'hi voker' and 'Savri maranan'?",
             "Mishkan T'filah wording of 'ki vanu vacharta v'otanu kidashta mikol ha-amim'?",
             "Line 1 English joins two Metsudah pieces; Genesis lines use Contemporary Torah."],
 "hamotzi": ["No Sefaria English found for this text."],
 "shehecheyanu": ["No Sefaria English found for this text."],
}

out = {"generated_by": "tools/build_prayers.py", "source_fetched": raw["fetched"], "prayers": []}
for order, (pid, title, about, lines) in enumerate(PRAYERS):
    pl = []
    for i, (hs, es) in enumerate(lines):
        he = get(hs, "he"); t, f = tl(he)
        src = None if es is None else (es[0] if isinstance(es, tuple) else es[0][0])
        pl.append({"he": he, "tl": t, "tlf": f, "en": get(es, "en"),
                   "en_src": S[src]["version"] if src else None, "en_license": S[src]["license"] if src else None,
                   "reform": [r["change"] for r in REFORM.get(pid, []) if r["line"] == i], "verify": True})
    hs0 = lines[0][0] if isinstance(lines[0][0], tuple) else lines[0][0][0]
    out["prayers"].append({"id": pid, "title": title, "about": about, "order": order, "audio": None,
        "he_src": f'{S[hs0[0]]["ref"]} ({S[hs0[0]]["version"]}, {S[hs0[0]]["license"]})',
        "check": CHECK.get(pid, []), "lines": pl})
json.dump(out, open(os.path.join(ROOT, "data/prayers.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for p in out["prayers"]:
    print(p["id"])
    for l in p["lines"]: print("  ", ("F " if l["tlf"] else "  ") + l["tl"], "|", (l["en"] or "-")[:70])
