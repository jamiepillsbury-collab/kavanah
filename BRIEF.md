# Hebrew Prayer App — Brief

Duolingo-style, mobile-first app for Jamie's own learning: Hebrew reading, prayers & blessings, meaning, chanting, then advanced liturgy (Shabbat, Torah service, holidays).

## Tradition & sources
- Reform. Daily/Shabbat: Mishkan T'filah selection and order. High Holy Days: Mishkan HaNefesh. A CBB Mashiv HaRuach PDF, if provided, takes priority.
- Hebrew base text from Sefaria (traditional), adapted to Mishkan T'filah wording; every Reform change marked in the data. Full nikkud, stored as JSON.
- No Claude-written translations or transliterations (changed 2026-10-28). English from Sefaria in Jamie's order: Contemporary Torah; Psalms JPS gender-sensitive; siddur Sim Shalom > Community > Birnbaum > Metsudah. Credit the version and license on every text. Transliteration = tools/translit.py run on the Sefaria Hebrew (Mishkan T'filah style); lines it flags get checked by Jamie or her cantor.
- Flag anything uncertain (vowels, wording, Reform vs. traditional) for Jamie/cantor. Jamie verifies each prayer against her Mishkan T'filah before it's final.

## Learning design
- Adult, respectful, mastery-based tone. Learning, not grading.
- Transliteration + translation shown first, fading with mastery; always uncoverable by tap, no penalty.
- Chanting audio: empty slots for Jamie's recordings. No fake melodies.

## Tech
- Plain HTML/CSS/JS, progress in device storage. Target: Android Chrome.
- Installable, offline-capable PWA hosted on GitHub Pages. Code lives in this folder.
- No Prayer & Meditation tab (decided 2026-10-28): Neshamah covers that; Settings links to it.
- Every script lives in tools/ (never only in the cloud). Version lives only in version.js. Deploy with git (GitHub Desktop) to GitHub Pages.
- Lessons from Neshamah: project doc claude/hebrew-app-lessons-from-neshamah.md.

## Working rules
Read PROGRESS.md + BRIEF.md each session; update PROGRESS.md at end. Small phases, clean checkpoints. Bulk content via Sonnet/Haiku sub-agents and scripts. Ask before anything large.

## Letters course direction (Jamie, 2026-10-15)
Model on Duolingo's Hebrew *letters* section (which Jamie loved; not its word lessons). Keep: finger tracing/writing, hearing the sound, practicing reading, writing and saying each sound, then letters combining, vowels, and finally reading without nikkud.
Fix what failed: after a long break she forgot most of it and Duolingo had no way back in. So: memory decays over time, a "welcome back" refresher after gaps, any lesson can be replayed anytime, and review never runs out.

### Duolingo screens Jamie shared (2026-10-15): exercise types to emulate
- **Letter grid home**: tile per letter/sound (letter, translit, progress bar) + one big "Learn the letters" button. Tiles include vowel-letters (וּ u, וֹ o). Tap tile = hear it.
- **Trace**: small letter + translit + speaker at top; big canvas with guide cross; letter traced stroke by stroke, each stroke shown as dashed path with start-arrow circle and end arrowhead; finished letter shown solid, "Great job".
- **What sound does this make?**: big card with letter+vowel combo (e.g. וֹי "oi") and speaker button; 3 translit choices; bottom feedback bar + Continue.
- **Select the characters for "jon"**: translit prompt, 4 real short WORDS in Hebrew as choices (not just syllables).
- **Hard exercise: type the sound**: vowelled word (e.g. פְּזוֹרָה), free-text translit box, Check. Needs lenient matching (ch/kh, tz/ts, apostrophes, doubled letters).
- Pattern: select then Check; feedback bar at bottom; progress bar at top; X to quit.
- Skip for prayer focus: geresh letters (ג׳ j, ז׳ zh, צ׳ ch), modern-only sounds.

## Scope expansion (Jamie, 2026-11-01)
Goal: everything a young Jew learns for bar/bat mitzvah, Duolingo-style. Plus two new tracks in the style of the Imprint app (short visual explainer cards, illustrated concepts, swipe-through lessons, quick check questions):
- **Jewish history**: biblical and ancient history through to modern.
- **Torah stories**: the Five Books, plus the other stories central to tradition and holidays: Ruth (Shavuot), Esther (Purim), Jonah (Yom Kippur), Hannah (Rosh Hashanah haftarah), prophets, and post-biblical ones like Hanukkah (Books of Maccabees, Talmud). Label each story's source.
- **Kabbalah**: core ideas (Ein Sof, sefirot, tzimtzum, tikkun olam, etc.), framed for a Reform learner.
Open: bar/bat mitzvah prep traditionally includes Torah/haftarah trope (cantillation), which the app currently strips; decide if/when to add it. History/Kabbalah explanations are original writing; cite sources and mark scholarly vs traditional accounts.
