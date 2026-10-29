"""data/prayers.json -> questions.html: every open CHECK, printable, for Jamie's rabbi/cantor.  Run: python tools/questions.py"""
import json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, "data/prayers.json"), encoding="utf-8"))
UNIT = {"blessings": "Blessings", "shma": "Shabbat evening: the Sh'ma and its blessings", "amidah": "Shabbat evening: the Amidah"}
rows, n = [], 0
for u in UNIT:
    ps = [p for p in sorted(P["prayers"], key=lambda p: p["seq"]) if p["unit"] == u and p["check"]]
    if not ps: continue
    rows.append(f"<h2>{html.escape(UNIT[u])}</h2>")
    for p in ps:
        rows.append(f'<h3>{html.escape(p["title"])}</h3><p class="src">Hebrew: {html.escape(p["he_src"])}</p><ol start="{n + 1}">')
        for q in p["check"]: rows.append(f"<li>{html.escape(q)}<div class=ans></div></li>"); n += 1
        rows.append("</ol>")
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Questions for the rabbi</title><style>
body{{font:16px/1.5 system-ui,sans-serif;max-width:720px;margin:0 auto;padding:16px;background:#fff;color:#222}}
h1{{font-size:1.4em}} h2{{font-size:1.15em;margin-top:1.6em;border-bottom:1px solid #ccc}} h3{{margin:1em 0 .2em}}
.src{{color:#666;font-size:.85em;margin:0}} li{{margin:.5em 0}} .ans{{border-bottom:1px dotted #aaa;height:1.6em}}
@media print{{.ans{{height:2.2em}}}}</style></head><body>
<h1>Kavanah: questions for the rabbi</h1>
<p>Open questions about wording and practice, compared with Mishkan T'filah. Generated from the app data ({n} questions). Space under each for notes.</p>
{"".join(rows)}</body></html>"""
open(os.path.join(ROOT, "questions.html"), "w", encoding="utf-8").write(page)
print(n, "questions -> questions.html")
