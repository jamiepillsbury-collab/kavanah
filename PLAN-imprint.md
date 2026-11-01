# PLAN: Imprint-style tracks + trope (draft 2026-11-01, not built)

Tracks: Torah stories, Jewish history, Kabbalah (swipe-card explainers), and Trope / b'nai mitzvah prep (Duolingo-style, like the prayer units).

## Decisions (Jamie, 11/01)
- Explore tab: yes. Start with Genesis.
- No set portion. App should know the weekly parashah and offer it that week.
- CBB: traditional Ashkenazi trope; some liturgy and melodies are its own. No cantor recordings for now, so trope audio slots stay empty (Jamie may record herself later).
- Jamie is the only reviewer. So every claim needs a source she can tap and check, and she can flag a card.
- Learning design must rest on adult-learning research, not app marketing. (Imprint's "How Imprint Works" page names retrieval practice and visuals but cites no studies.)

## 0. Learning design and research basis
Each rule below changes what the app does.
1. Narrative first. Every lesson opens with a story or a person, and ideas sit inside it. Narrative text is recalled and understood better than expository text (Mar, Li, Nguyen & Ta, 2021, meta-analysis, Psychonomic Bulletin & Review). History lessons follow people and places; Kabbalah lessons follow Safed, the Zohar's circle, and so on.
2. Relevance to her own life (andragogy: need to know, problem-centered, draws on experience; Knowles, Holton & Swanson, The Adult Learner). Each lesson has a "Where you meet this" card: a prayer she already says in the app, a holiday, this week's parashah, a CBB practice.
3. Reflection (Mezirow, 1991; Kolb, 1984). Optional "Your turn" card with one open prompt; her note is saved on the phone, never graded, shown again on replay.
4. A guess before the lesson (pretesting effect; Richland, Kornell & Kao, 2009). The first card asks one prediction question. Wrong guesses are expected and cost nothing.
5. Retrieval and spacing (Roediger & Karpicke, 2006; Adesope, Trevisan & Sundararajan, 2017; Cepeda et al., 2006; Dunlosky et al., 2013). Checks inside lessons, then the existing fade/review system brings them back days later.
6. Learning from errors (Metcalfe, 2017, Annual Review of Psychology; Butler, Godbole & Marsh, 2013; Hattie & Timperley, 2007). After a wrong answer: (a) her answer and the right one side by side; (b) why the right one is right AND why hers was tempting (each wrong choice has its own "why"); (c) "Look again" opens the card that teaches it; (d) later the same idea comes back in a different form (another question type), so she rebuilds it instead of remembering a letter. Optional confidence tap ("sure / unsure"): confident errors are corrected best (hypercorrection; Butterfield & Metcalfe, 2001), so they come back first.
7. "To revisit" list (Practice tab and each lesson's end): every miss with her answer, the right answer and the why, until she gets it right twice on separate days.
8. Multimedia rules (Mayer, Multimedia Learning): one idea per card (segmenting), key words highlighted (signaling), no decorative extras (coherence), key terms before the story uses them (pretraining), plain conversational voice (personalization).
9. Self-explanation (Chi et al., 1994; Dunlosky et al., 2013): some checks ask "why" (pick the best reason), not only "what".
10. Interleaving similar things (Kornell & Bjork, 2008): Practice mixes look-alike ideas and trope marks so she learns to tell them apart.
Citations are from my knowledge, not checked online; Jamie, confirm any you want to rely on.

## 1. Card format, lesson flow, fit with the app

Lesson = 6 to 10 cards, swiped left/right, about 3 to 5 minutes. Card kinds:
- hook: the opening scene or question, plus a prediction check (rule 4).
- concept: title, 1 to 3 short sentences, optional diagram.
- relevance: "Where you meet this" (rule 2), with links into the app.
- reflect: optional open prompt, private note (rule 3).
- term: Hebrew term (with nikkud), translit (translit.py), short meaning.
- text: a short Hebrew/English excerpt from Sefaria with ref, version and license (same rules as prayers).
- timeline: date or era + event; consecutive timeline cards draw as one strip.
- diagram: generated SVG (timeline, map outline, family tree, sefirot tree). Code-drawn only.
- check: one quick question after every 2 to 3 cards. Types: pick one, pick the reason, true/false, put in order, match term to meaning. Each idea has 2+ question forms. Error handling as in rule 6. Never blocks; misses come back at the end and go on the To revisit list.
- recap: 3 bullet takeaways + key terms.
Every card shows a source chip (see schema) and can be tapped for "Where this comes from" (exact ref, Sefaria link where there is one). A "Flag this card" button saves her doubts; Settings lists flagged cards (like questions.html). Lessons are marked draft until she marks them reviewed. Illustration slot (image: null) on any card for art Jamie adds later; no copied or fake art.

Fit with the app:
- New 4th tab "Explore" (Learn / Explore / Practice / Settings), with chips for Stories, History, Kabbalah. Trope lives in Learn as normal units (it is a skill, like letters).
- Progress: check questions are items in state.items (ids like x-hist-03-q2) and use the existing mastery/fade system, Review card and Practice. Reading a card is stored as seen (no score). Lesson tile = % of its checks mastered; lessons always open and replayable.
- Practice tab: adds check questions to the mix, fading first. Explore items never mix into Hebrew drills unless they are term cards.
- Links both ways: a prayer's about card can link "Story behind this" (Mi Chamocha -> Sea of Reeds; L'cha Dodi -> Safed; Sh'ma -> Moses' farewell), and a story card can link to the prayer lesson.

## 2. Data schema

Authored source: data/src/x-<track>.json (one file per track). tools/build_explore.py validates it, adds translit, checks every check question has a valid answer and every card has a source, and writes data/explore.json. Ids are append-only, as with words.json.

```json
{
  "track": "stories",
  "units": [{
    "id": "x-st-gen",
    "title": "Genesis",
    "lessons": [{
      "id": "x-st-gen-01",
      "title": "Creation",
      "related": ["prayer:kabbalat"],
      "season": null,
      "cards": [
        {"kind": "concept", "title": "Seven days", "body": "...",
         "src": {"type": "torah", "ref": "Genesis 1:1-2:3"}},
        {"kind": "text", "ref": "Genesis 1:1", "he": "...", "en": "...",
         "en_src": "The Contemporary Torah", "license": "CC-BY-NC",
         "src": {"type": "torah", "ref": "Genesis 1:1"}},
        {"kind": "term", "he": "...", "tl": null, "gloss": "...",
         "src": {"type": "torah", "ref": "Genesis 2:2"}},
        {"kind": "check", "id": "q1", "idea": "rest-day", "q": "...", "type": "pick",
         "choices": ["...", "...", "..."], "answer": 0, "why": "...",
         "wrong_why": [null, "...", "..."], "look_again": 0,
         "src": {"type": "torah", "ref": "Genesis 1"}},
        {"kind": "relevance", "body": "...", "links": ["prayer:kiddush"]}
      ],
      "parashah": ["Bereshit"],
      "status": "draft",
      "check_note": "Anything for Jamie to confirm"
    }]
  }]
}
```
src.type (shown as the chip): torah, tanakh, rabbinic (Talmud/Midrash), apocrypha (Maccabees), liturgy, kabbalah (Zohar, Luria...), scholarly (academic history/archaeology), tradition (traditional account), reform (Reform teaching or practice). Optional src.note for a citation (book, author). idea = the concept a check tests; mastery and To revisit go by idea, so different question forms count toward the same idea. look_again = index of the card that teaches it. Saved on the phone: state.missed (idea, her answer, date), state.notes (reflections), state.flags. Where scholars and tradition differ, the lesson uses two cards, one of each type, side by side. Fields: tl null = filled by translit.py; season = holiday key (e.g. "hanukkah") to surface the lesson in the weeks before.

Trope data (separate, in prayers-style data): verse lines keep a new field he_t (Hebrew WITH cantillation, from Sefaria, not stripped), plus he (current stripped form) and audio slots per verse and per trope phrase. data/trope.json lists each trope mark: id, name, Unicode mark, family, position (above/below), audio: null.

## 3. Units (titles only)

Torah stories
1. Genesis: Creation; Garden of Eden; Cain and Abel; Noah; Tower of Babel; Abraham and Sarah; Hagar and Ishmael; The Binding of Isaac; Rebecca at the well; Jacob and Esau; Jacob's ladder and the wrestling; Rachel and Leah; Joseph and his brothers; Joseph in Egypt
2. Exodus: Moses' birth and the midwives; The burning bush; The plagues; The first Passover; Crossing the sea (Miriam's song); Manna and Shabbat; Sinai and the Ten Commandments; The golden calf; Building the Mishkan
3. Leviticus: Offerings and the priests; The Yom Kippur ritual; "You shall be holy"
4. Numbers: The spies; Korach; Miriam's well and the rock; Balaam; The daughters of Tzelophechad
5. Deuteronomy: Moses' farewell; The Sh'ma in context; The death of Moses
6. Holiday scrolls and haftarot: Hannah (Rosh Hashanah); Jonah (Yom Kippur); Ecclesiastes (Sukkot); Song of Songs (Passover); Ruth (Shavuot); Lamentations (Tisha B'Av); Esther (Purim)
7. Judges, kings and prophets: Joshua and Jericho; Deborah; Samson; Samuel and Saul; David and Goliath; David and Bathsheba; Solomon and the Temple; Elijah; Isaiah; Jeremiah; Ezekiel's dry bones; Daniel
8. After the Bible: Hanukkah (1 and 2 Maccabees, Talmud Shabbat 21b); Hillel and Shammai; Honi the circle-maker; Yochanan ben Zakkai and Yavneh; Rabbi Akiva; The oven of Akhnai; Beruriah

Jewish history
1. Beginnings: The ancestors (tradition and scholarship); Israel in Canaan; The kingdoms of Israel and Judah
2. Exile and return: Assyria and the lost tribes; Babylon and the first exile; The return and the Second Temple
3. Greeks and Romans: Hellenism; The Maccabees and Hasmoneans; Herod and Rome; The Temple destroyed; Bar Kokhba
4. The rabbis: From Temple to synagogue; Mishnah; The Talmuds; The Geonim
5. Medieval worlds: Jews under Islam; The golden age of Spain; Rashi and Ashkenaz; Maimonides; The Crusades and expulsions; 1492
6. Early modern: The Sephardi diaspora; Safed and Luria; Shabbetai Tzvi; Hasidim and their opponents
7. Modern Europe: Enlightenment and emancipation; The birth of Reform; Orthodox and Conservative responses; Pogroms and migration
8. America: Early American Jews; Reform in America (Pittsburgh Platform to today); The great immigration; Women rabbis
9. 20th century: Zionism; The Holocaust; The State of Israel; Soviet Jewry; Jews of the Middle East and North Africa; Ethiopian Jews
10. Jews today: Movements and diversity; Israel and the diaspora

Kabbalah
1. What Kabbalah is: Mysticism in Judaism; Sefer Yetzirah and the Bahir; The Zohar; How scholars study it
2. God beyond and within: Ein Sof; Shechinah
3. The sefirot: The tree; Keter, Chochmah, Binah; Chesed, G'vurah, Tiferet; Netzach, Hod, Y'sod; Malchut
4. The Lurianic story: Tzimtzum; The breaking of the vessels; Tikkun (Luria's meaning and the Reform meaning)
5. Soul and practice: Levels of soul (nefesh, ruach, n'shamah); Kavanah in prayer; Kabbalat Shabbat and Safed; Devekut and the Hasidim
6. Kabbalah and Reform: Rejection, rediscovery, and use today

Trope / b'nai mitzvah prep (Learn tab)
1. What trope is: Signs and melodies; Torah, haftarah and scroll melodies
2. The marks: Sof pasuk and silluk; Etnachta; Mercha and tipcha; Munach and zakef katon; Zakef gadol; Revia; Pashta and kadma; Tevir and darga; Geresh and gershayim; Rarer marks
3. Reading the scroll: Letters without vowels; Torah scroll script; Reading from a tikkun
4. Chanting: Phrase families with audio; Practice verses
5. The aliyah: Torah blessings (built); Haftarah blessings after; The Torah service
6. Your portion (if Jamie picks one): verse by verse, trope shown, then hidden; record and compare
7. D'var Torah: How to build one (structure only)

## Weekly parashah
data/parashah.json: one row per Shabbat (Diaspora schedule, which a US Reform congregation follows), date -> parashah name(s), joined portions included, about 5 years ahead. Generated by a tools/ script from Hebcal's free JSON (CC-BY; fetched in the browser pane since shells are blocked), hash-checked, stored in the app so it works offline. Each Torah-stories lesson lists its parashah. During the week, Learn and Explore show "This week: Parashat ..." with the matching story lesson; later also the opening verses with trope. Note: Mishkan T'filah congregations sometimes read a different section of the portion; the card says so.

## 4. Placement and build order

Placement: Learn keeps letters -> words -> prayers; Trope units come after the Torah service prayer unit and after "reading without vowels". Explore runs beside everything, no prerequisites. Holiday lessons (season key) show a card on Learn in the weeks before the holiday.

Suggested build order (one session each, clean checkpoints):
1. DONE 11/01 (v19). Engine: Explore tab, card renderer (swipe, chips, checks, error flow, To revisit, flags, notes), schema, build_explore.py, progress wiring. Test with one pilot lesson.
2. Weekly parashah table + "This week" card (the Genesis portions are being read now).
3. Pilot: one Genesis lesson; Jamie reviews tone, length and the error flow before more.
4. Rest of Genesis, then Exodus (most tied to prayers). Hanukkah lesson before Dec 4.
5. Kabbalah units 1 to 4 (ties to Kabbalat Shabbat already built).
6. Prayer track continues: Torah service, reading without vowels.
7. Trope units 1 to 3 (marks need he_t data; small Sefaria fetch).
8. History, two units at a time.
9. Trope 4 to 6 when recordings exist (Jamie's own or the cantor's).

Content production: original explanations, drafted per lesson in the fixed schema (Sonnet sub-agent for bulk drafts, main model for Kabbalah and contested history), validated by script, every lesson reviewed by Jamie. Quotes only from Sefaria with license.

## Content drafting (decided 11/01)
- All lesson content drafted by the main model (Jamie's choice: rewriting/checking Sonnet drafts would cost about as much). Scripts still pull verses and validate; no sub-agents for content.
- Pilot = Creation; it sets tone and length for the rest. Ask Jamie before writing each batch.
