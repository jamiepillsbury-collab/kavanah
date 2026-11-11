"""Add Jamie's two framing teachings (with published parallels) to existing Explore lessons. Idempotent: matches by card title.
Inserted right before a lesson's 'relevance' (or 'recap') card, so no look_again index shifts."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEA = {"kind": "concept", "title": "Two questions, one cup of tea",
 "body": "A teaching from your rabbi, a scientist before he was a rabbi: a husband sees his wife is ill and makes her tea. **Why did the water boil?** Because heat was applied: that's true. And because **he loves her**: without that, the water never boils either. Two true answers to two different questions, not a contest. Rabbi Jonathan Sacks put it this way: \"Science takes things apart to see how they work\"; religion puts them together to see **what they mean**.",
 "src": {"type": "reform", "ref": "Teaching from Jamie's rabbi (oral, as Jamie retold it); Jonathan Sacks, The Great Partnership (2011)", "note": "check page"}}
GROW = {"kind": "concept", "title": "A people growing up",
 "body": "A teaching from your rabbi: read the Torah as a people **growing up spiritually**. Early on, God is like a child's picture of a parent, a hero who fixes everything. Later the relationship gets strained and complicated. In maturity, God is felt less as a hand moving things and more as the love present **when we act rightly**. Rambam made a related point: people can't move **suddenly from one extreme to the other**, so the Torah meets them where they are. The Talmud: \"The Torah spoke in the language of men.\"",
 "src": {"type": "reform", "ref": "Teaching from Jamie's rabbi (oral, as Jamie retold it); Guide for the Perplexed 3:32; Berakhot 31b; Richard Elliott Friedman, The Hidden Face of God (1995)", "note": "Rambam and Berakhot read on Sefaria 11/11; Friedman: check"}}
ADD = {"x-st-gen-01": [GROW, TEA]}
p = os.path.join(ROOT, "data/src/x-stories.json")
d = json.load(open(p, encoding="utf-8"))
for u in d["units"]:
    for l in u["lessons"]:
        if l["id"] not in ADD: continue
        cards = [c for c in l["cards"] if c.get("title") not in {x["title"] for x in ADD[l["id"]]}]
        at = next(i for i, c in enumerate(cards) if c["kind"] in ("relevance", "recap"))
        l["cards"] = cards[:at] + ADD[l["id"]] + cards[at:]
        print(l["id"], len(l["cards"]))
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
