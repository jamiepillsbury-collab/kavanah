"""Explore tracks (Imprint-style card lessons): data/src/x-<track>.json -> data/explore.json.
Validates every lesson, fills transliteration (tl) with translit.py, NFC-normalizes Hebrew.
Lesson ids and check "idea" keys are progress keys: never rename or remove them (script warns).
Usage: python tools/build_explore.py            (all data/src/x-*.json -> data/explore.json)
       python tools/build_explore.py --src F --out O   (test with a fixture)
Schema: see PLAN-imprint.md section 2."""
import argparse, glob, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from translit import tl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACKS = [("stories", "Torah stories"), ("history", "Jewish history"), ("kabbalah", "Kabbalah")]
SRC = {"torah", "tanakh", "rabbinic", "apocrypha", "liturgy", "kabbalah", "scholarly", "tradition", "reform"}
KINDS = {"hook", "concept", "term", "text", "timeline", "diagram", "check", "relevance", "reflect", "recap"}
NO_SRC = {"reflect", "recap", "relevance"}
CHECKS = {"pick", "why", "tf", "order"}
errors, warns = [], []
SEF = {}  # (ref, lang) -> source entry, from data/src/sefaria-*.json ("sources" lists)

def load_sefaria():
    for f in glob.glob(os.path.join(ROOT, "data", "src", "sefaria-*.json")):
        d = json.load(open(f, encoding="utf-8"))
        if isinstance(d, dict) and isinstance(d.get("sources"), list):
            for x in d["sources"]:
                if isinstance(x, dict) and "ref" in x and "lang" in x and "text" in x: SEF[(x["ref"], x["lang"])] = x

def clean_he(t):
    t = re.sub(r"\s*\{[פס]\}", "", t).replace("יְהֹוָה", "יְיָ")  # paragraph marks; the Name as elsewhere in the app
    return nfc(t.strip())

def clean_en(t): return re.sub(r",(?=[A-Za-z])", ", ", t).strip()  # Sefaria poetry line breaks lose their space

def err(where, msg): errors.append(f"{where}: {msg}")

def nfc(s): return unicodedata.normalize("NFC", s) if isinstance(s, str) else s

def check_card(c, n, cards, where):
    k = c.get("kind")
    if k not in KINDS: return err(where, f"unknown kind {k!r}")
    for f in ("he",):
        if f in c: c[f] = nfc(c[f])
    if k == "text" and c.get("sefaria"):  # fill from the verified Sefaria file; never hand-typed
        ref = c["sefaria"]; he_s, en_s = SEF.get((ref, "he")), SEF.get((ref, "en"))
        if not (he_s and en_s): return err(where, f"no Sefaria he+en for {ref!r} in data/src/sefaria-*.json")
        c.update(ref=c.get("ref") or ref, he="\n".join(map(clean_he, he_s["text"])), en=" ".join(map(clean_en, en_s["text"])),
                 en_src=en_s["version"], license=en_s["license"], he_src=f'{he_s["version"]} ({he_s["license"]})')
        c.setdefault("src", {"type": "torah", "ref": ref})
    if k not in NO_SRC:
        s_ = c.get("src") or {}
        if s_.get("type") not in SRC: err(where, f"src.type must be one of {sorted(SRC)}")
    if k in ("term", "text"):
        if not c.get("he"): err(where, "needs he")
        if c.get("tl") is None and c.get("he"):
            parts = [tl(x) for x in c["he"].split("\n")]
            c["tl"] = "\n".join(x[0] for x in parts)
            if any(x[1] for x in parts): c["tlf"] = True
    if k == "text" and not (c.get("en_src") and c.get("license") and c.get("ref")):
        err(where, "text card needs ref, en_src and license (Sefaria version)")
    if k in ("concept", "hook") and not c.get("body"): err(where, "needs body")
    if k == "timeline" and not (c.get("when") and c.get("body")): err(where, "needs when + body")
    if k == "diagram" and not c.get("svg"): err(where, "needs svg")
    if k == "recap" and not c.get("points"): err(where, "needs points")
    if k == "reflect" and not c.get("prompt"): err(where, "needs prompt")
    if k == "relevance" and not c.get("body"): err(where, "needs body")
    if k != "check": return
    t = c.get("type")
    if t not in CHECKS: return err(where, f"check type must be one of {sorted(CHECKS)}")
    if not c.get("id"): err(where, "check needs id")
    if not c.get("q"): err(where, "check needs q")
    if not c.get("why"): err(where, "check needs why")
    if not c.get("pretest") and not c.get("idea"): err(where, "check needs idea (unless pretest)")
    if t == "tf":
        if not isinstance(c.get("answer"), bool): return err(where, "tf answer must be true/false")
        c["choices"], c["answer"] = ["True", "False"], 0 if c["answer"] else 1
    if t in ("pick", "why", "tf"):
        ch = c.get("choices") or []
        if len(ch) < 2: err(where, "needs 2+ choices")
        if not isinstance(c.get("answer"), int) or not 0 <= c["answer"] < len(ch): err(where, "answer index out of range")
        ww = c.get("wrong_why")
        if not c.get("pretest"):
            if not isinstance(ww, list) or len(ww) != len(ch): err(where, "wrong_why needs one entry per choice (null for the answer)")
            elif any(not w for i, w in enumerate(ww) if i != c.get("answer")): err(where, "every wrong choice needs a wrong_why")
    if t == "order" and len(c.get("items") or []) < 3: err(where, "order needs 3+ items (in correct order)")
    la = c.get("look_again")
    if la is not None and (not isinstance(la, int) or not 0 <= la < n or cards[la].get("kind") == "check"):
        err(where, "look_again must point to an earlier non-check card")

def build(srcs, out):
    load_sefaria()
    tracks = {tid: {"id": tid, "title": title, "units": []} for tid, title in TRACKS}
    pnames = set(json.load(open(os.path.join(ROOT, "data", "parashah.json"), encoding="utf-8"))["names"])
    lesson_ids = set()
    for path in srcs:
        d = json.load(open(path, encoding="utf-8"))
        tid = d.get("track")
        if tid not in tracks: err(path, f"track must be one of {list(tracks)}"); continue
        for u in d.get("units", []):
            if not (u.get("id") and u.get("title")): err(path, "unit needs id + title")
            for l in u.get("lessons", []):
                w = f"{path}:{l.get('id')}"
                if not (l.get("id") and l.get("title")): err(w, "lesson needs id + title"); continue
                if l["id"] in lesson_ids: err(w, "duplicate lesson id")
                lesson_ids.add(l["id"])
                l.setdefault("status", "draft"); l.setdefault("related", []); l.setdefault("parashah", []); l.setdefault("season", None)
                if l["status"] not in ("draft", "reviewed"): err(w, "status must be draft or reviewed")
                for p in l["parashah"]:
                    if p not in pnames: err(w, f"unknown parashah {p!r} (use the names in data/parashah.json)")
                cards = l.get("cards") or []
                if not cards or cards[-1].get("kind") != "recap": err(w, "last card must be a recap")
                ids = [c.get("id") for c in cards if c.get("kind") == "check"]
                if len(ids) != len(set(ids)): err(w, "duplicate check id")
                for n, c in enumerate(cards): check_card(c, n, cards, f"{w} card {n}")
            tracks[tid]["units"].append(u)
    # progress keys must stay stable
    if os.path.exists(out):
        try:
            old = json.load(open(out, encoding="utf-8"))
            for t in old["tracks"]:
                for u in t["units"]:
                    for l in u["lessons"]:
                        if l["id"] not in lesson_ids: warns.append(f"lesson id {l['id']} disappeared (its progress is orphaned)")
        except Exception as e: warns.append(f"couldn't compare with old {out}: {e}")
    for w in warns: print("WARN", w)
    if errors:
        for e in errors: print("ERROR", e)
        sys.exit(1)
    json.dump({"tracks": list(tracks.values())}, open(out, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print(f"{out}: {len(lesson_ids)} lessons")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", nargs="*")
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "explore.json"))
    a = ap.parse_args()
    build(a.src if a.src is not None else sorted(glob.glob(os.path.join(ROOT, "data", "src", "x-*.json"))), a.out)
