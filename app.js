/* Kavanah — lesson engine. Plain JS, no build step. Data in data/*.json, progress in localStorage. */
(() => {
  "use strict";
  const KEY = "kavanah.v1";
  const DATA_FILES = ["data/alefbet.json", "data/words.json"];
  const $ = (s, el = document) => el.querySelector(s);
  const view = $("#view");
  const h = (tag, attrs = {}, ...kids) => {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
      else if (k === "html") el.innerHTML = v;
      else el.setAttribute(k, v === true ? "" : v);
    }
    for (const kid of kids.flat()) if (kid != null && kid !== false) el.append(kid);
    return el;
  };
  const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  // ---------- state ----------
  let course = { units: [], items: {} };
  let prayers = {}; // data/prayers.json by id
  let state = { items: {}, settings: { hints: "auto", rate: 0.8 } };
  const load = () => { try { const s = JSON.parse(localStorage.getItem(KEY)); if (s && s.items) state = { ...state, ...s, settings: { ...state.settings, ...s.settings } }; } catch (e) {} };
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} };
  const rec = (id) => state.items[id] || null;
  // Memory fades: an item at level m holds for 2^(m-1) days, then drops one level per further interval.
  const DAY = 864e5;
  const mastery = (id) => {
    const r = rec(id);
    if (!r) return 0;
    let m = r.m, t = (Date.now() - r.last) / DAY;
    while (m > 0 && t >= 2 ** (m - 1)) { t -= 2 ** (m - 1); m--; }
    return m;
  };
  const isDue = (id) => rec(id) && mastery(id) < rec(id).m;
  const mark = (id, ok) => {
    const cur = mastery(id);
    const r = state.items[id] || (state.items[id] = { m: 0, right: 0, wrong: 0, last: 0 });
    r.m = ok ? Math.min(5, cur + 1) : Math.max(0, cur - 1);
    ok ? r.right++ : r.wrong++;
    r.last = state.lastActive = Date.now();
    save();
  };
  // ---------- sound: recording if present, else the phone's Hebrew voice ----------
  let heVoice = null, allVoices = [];
  const pickVoice = () => {
    if (!("speechSynthesis" in window)) return;
    const vs = speechSynthesis.getVoices();
    allVoices = vs;
    const isHe = (v) => /^(he|iw|heb)([-_]|$)/i.test(v.lang) || /hebrew|עברית/i.test(v.name);
    heVoice = vs.find((v) => isHe(v) && v.localService) || vs.find(isHe) || null;
  };
  const canHear = (it) => !!(it && (it.audio || (heVoice && it.say)));
  const speak = (it, done) => {
    const fin = () => { if (done) { const d = done; done = null; d(); } };
    if (!it) return fin();
    if (it.audio) { const a = new Audio(it.audio); a.onended = a.onerror = fin; a.play().catch(fin); return; }
    if (!heVoice || !it.say) return fin();
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(it.say);
    u.voice = heVoice; u.lang = heVoice.lang; u.rate = state.settings.rate || 0.8;
    u.onend = u.onerror = fin;
    speechSynthesis.speak(u);
  };
  const speakBtn = (it, big) => canHear(it)
    ? h("button", { class: "speaker" + (big ? " lg" : ""), "aria-label": "Play sound", onclick: (e) => { e.stopPropagation(); speak(it); } }, "🔊")
    : null;
  // what an item sounds like, for keeping same-sounding choices apart (בַ/וַ, patach/kamatz)
  const soundKey = (x) => { const t = course.items[x]; return t.kind === "letter" ? t.name : t.kind === "vowel" ? t.sound : t.tr; };

  // banner that explains anything that can't happen yet; actions = [{label, fn}]
  const toast = (msg, actions = []) => {
    document.querySelector(".toast")?.remove(); clearTimeout(toast.t);
    const t = h("div", { class: "toast", role: "status" }, h("span", {}, msg),
      ...actions.filter(Boolean).map((a) => h("button", { onclick: () => { t.remove(); a.fn(); } }, a.label)),
      h("button", { class: "x", "aria-label": "Close", onclick: () => t.remove() }, "✕"));
    document.body.append(t); toast.t = setTimeout(() => t.remove(), 9000);
  };
  const lessonPct = (l) => l.items.reduce((s, id) => s + Math.min(mastery(id), 3) / 3, 0) / l.items.length;
  const allLessons = () => course.units.flatMap((u) => u.lessons);

  // ---------- questions ----------
  const label = (it, mode) => {
    if (!it.name) return it.tr;
    return `${it.name} · ${it.sound}`;
  };
  const hintFor = (it, mode) => {
    if (it.kind === "syllable") return it.hint;
    if (it.kind === "word") return mode === "hear" ? it.tr : glossText(it);
    if (it.kind === "letter" && mode === "find") return it.note;
    if (mode === "hear") return it.name ? `${it.name} · ${it.sound}` : it.tr;
    return `${it.name} · ${it.sound}`;
  };
  const glossText = (it) => (it.gloss ? `${it.gloss.def} (${it.gloss.root})` : "No dictionary entry yet");
  const heWords = (s) => s.replace(/[,.;:]/g, "").split(/\s+/).filter(Boolean);
  // hint visibility: "show" | "faint" | "hidden"
  const hintLevel = (id) => {
    const s = state.settings.hints;
    if (s === "always") return "show";
    if (s === "never") return "hidden";
    const m = mastery(id);
    return m < 1 ? "show" : m < 2 ? "faint" : "hidden";
  };
  const distractors = (id, mode, lessonIds) => {
    const it = course.items[id];
    const same = (x) => course.items[x].kind === it.kind;
    const key = (x) => (mode === "read" ? label(course.items[x], mode) : course.items[x].he);
    const pools = [
      it.group ? Object.keys(course.items).filter((x) => same(x) && course.items[x].group === it.group) : [],
      lessonIds.filter(same),
      Object.keys(course.items).filter(same),
    ];
    // in find/hear, also never offer a second choice that sounds the same as another
    const seen = new Set([key(id)]), heard = new Set([soundKey(id)]), out = [];
    for (const pool of pools) for (const x of shuffle(pool)) {
      if (out.length >= 3) break;
      const k = key(x), sk = soundKey(x);
      if (seen.has(k) || (mode !== "read" && heard.has(sk))) continue;
      seen.add(k); heard.add(sk); out.push(x);
    }
    return out;
  };

  // ---------- tracing (print letters, stroke by stroke; never graded) ----------
  let strokes = null; // data/strokes.json, loaded at boot
  const SHAPE = { "א": "alef", "ב": "bet", "ג": "gimel", "ד": "dalet", "ה": "he", "ו": "vav", "ז": "zayin", "ח": "chet", "ט": "tet", "י": "yod",
    "כ": "kaf", "ך": "kaf_sofit", "ל": "lamed", "מ": "mem", "ם": "mem_sofit", "נ": "nun", "ן": "nun_sofit", "ס": "samekh", "ע": "ayin",
    "פ": "pe", "ף": "pe_sofit", "צ": "tzadi", "ץ": "tzadi_sofit", "ק": "kuf", "ר": "resh", "ש": "shin", "ת": "tav" };
  const traceStrokes = (it) => {
    const key = strokes && it.kind === "letter" && SHAPE[it.he[0]];
    if (!key || !strokes.letters[key]) return null;
    const out = strokes.letters[key].map((s) => ({ d: s.d }));
    const dot = (x, y) => out.push({ d: `M${x} ${y} L${x + 0.5} ${y + 0.5}`, dot: true });
    if (it.he.includes("ּ")) dot(52, 55);  // dagesh
    if (it.he.includes("ׁ")) dot(76, 9);   // shin dot (right)
    if (it.he.includes("ׂ")) dot(26, 9);   // sin dot (left)
    return out;
  };
  const canTrace = (it) => !!traceStrokes(it);
  const SVGNS = "http://www.w3.org/2000/svg";
  const s = (tag, attrs = {}) => { const el = document.createElementNS(SVGNS, tag); for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v); return el; };

  function renderTrace(it, bar, next) {
    const list = traceStrokes(it);
    const svg = s("svg", { viewBox: "0 0 100 100", class: "trace", "aria-label": `Trace ${it.name}` });
    const defs = s("defs");
    const mk = s("marker", { id: "arw", viewBox: "0 0 10 10", refX: "5", refY: "5", markerWidth: "4", markerHeight: "4", orient: "auto-start-reverse" });
    mk.append(s("path", { d: "M0 0 L10 5 L0 10 z", class: "t-arrow" }));
    defs.append(mk); svg.append(defs);
    svg.append(s("line", { x1: 50, y1: 2, x2: 50, y2: 98, class: "t-cross" }), s("line", { x1: 2, y1: 50, x2: 98, y2: 50, class: "t-cross" }),
      s("line", { x1: 8, y1: 80, x2: 92, y2: 80, class: "t-base" }));
    for (const st of list) svg.append(s("path", { d: st.d, class: "t-ghost" + (st.dot ? " dot" : "") }));
    const layer = s("g"); svg.append(layer);
    const status = h("p", { class: "sub t-status" }, "Start at the dot and follow the dashes.");
    let k = 0, guide, ink, startDot, pts, len, prog, active;
    const TOL = 13, LOST = 24;
    const setup = () => {
      layer.querySelectorAll(".t-guide,.t-start,.t-ink").forEach((e) => e.remove());
      if (k >= list.length) return finish();
      const st = list[k];
      guide = s("path", { d: st.d, class: "t-guide", "marker-end": st.dot ? "" : "url(#arw)" });
      ink = s("path", { d: st.d, class: "t-ink" + (st.dot ? " dot" : "") });
      layer.append(guide, ink);
      len = guide.getTotalLength();
      pts = []; for (let d = 0; d <= len; d += 2) pts.push(guide.getPointAtLength(d)); pts.push(guide.getPointAtLength(len));
      const p0 = pts[0];
      startDot = s("circle", { cx: p0.x, cy: p0.y, r: st.dot ? 5 : 4.5, class: "t-start" }); layer.append(startDot);
      prog = 0; active = false; paint();
      status.textContent = st.dot ? "Tap the dot." : k ? `Stroke ${k + 1} of ${list.length}.` : "Start at the dot and follow the dashes.";
    };
    const paint = () => { ink.style.strokeDasharray = `${(prog / (pts.length - 1)) * len} ${len + 10}`; };
    const at = (e) => { const p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY; return p.matrixTransform(svg.getScreenCTM().inverse()); };
    const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
    const strokeDone = () => { prog = pts.length - 1; paint(); ink.classList.add("done"); guide.remove(); startDot.remove();
      layer.parentNode.insertBefore(s("path", { d: list[k].d, class: "t-solid" + (list[k].dot ? " dot" : "") }), layer); k++; setTimeout(setup, 120); };
    svg.addEventListener("pointerdown", (e) => {
      if (k >= list.length) return;
      const p = at(e);
      if (dist(p, pts[0]) > TOL + 4) { status.textContent = "Begin at the dot."; return; }
      if (list[k].dot) return strokeDone();
      svg.setPointerCapture(e.pointerId); active = true; e.preventDefault();
    });
    svg.addEventListener("pointermove", (e) => {
      if (!active) return;
      const p = at(e);
      // advance along the path while the finger stays close; allow small skips ahead
      let best = -1;
      for (let j = prog; j < Math.min(pts.length, prog + 8); j++) if (dist(p, pts[j]) < TOL) best = j;
      if (best > prog) { prog = best; paint(); }
      else if (dist(p, pts[prog]) > LOST && dist(p, pts[Math.min(prog + 4, pts.length - 1)]) > LOST) {
        active = false; prog = 0; paint(); status.textContent = "Off the path — start again from the dot.";
      }
      if (prog >= pts.length - 2) { active = false; strokeDone(); }
    });
    const up = () => { if (!active) return; active = false; if (prog >= (pts.length - 1) * 0.88) strokeDone(); else { prog = 0; paint(); status.textContent = "Keep going to the arrow. Start again from the dot."; } };
    svg.addEventListener("pointerup", up); svg.addEventListener("pointercancel", up);
    const showMe = h("button", { class: "secondary small", onclick: () => {
      if (k >= list.length || list[k].dot) return;
      const demo = s("path", { d: list[k].d, class: "t-demo" }); layer.append(demo);
      demo.style.strokeDasharray = demo.style.strokeDashoffset = len;
      requestAnimationFrame(() => { demo.style.transition = `stroke-dashoffset ${0.4 + len / 120}s linear`; demo.style.strokeDashoffset = 0; });
      setTimeout(() => demo.remove(), 900 + len * 9);
    } }, "Show me");
    const finish = () => {
      svg.classList.add("complete"); status.textContent = "";
      bar.className = "checkbar good";
      bar.replaceChildren(h("div", { class: "fb-row" }, h("b", {}, "Nicely written."), speakBtn(it)), h("button", { class: "primary", onclick: next }, "Continue"));
      speak(it);
    };
    view.append(h("div", { class: "card trace-card" },
      h("div", { class: "t-head" }, h("span", { class: "he-in", lang: "he" }, it.he), h("span", {}, `${it.name} · ${it.sound}`), speakBtn(it)),
      h("p", { class: "prompt-label" }, "Trace the letter"), svg, status, showMe), bar);
    bar.append(h("button", { class: "secondary", onclick: next }, "Skip"));
    setup();
  }

  // ---------- write from memory: blank pad, reveal the letter any time, compare at the end (never graded) ----------
  function renderWrite(it, bar, next) {
    const list = traceStrokes(it);
    const svg = s("svg", { viewBox: "0 0 100 100", class: "trace", "aria-label": `Write ${it.name}` });
    svg.append(s("line", { x1: 50, y1: 2, x2: 50, y2: 98, class: "t-cross" }), s("line", { x1: 2, y1: 50, x2: 98, y2: 50, class: "t-cross" }),
      s("line", { x1: 8, y1: 80, x2: 92, y2: 80, class: "t-base" }));
    const answer = s("g", { class: "w-answer" }); answer.style.display = "none";
    for (const st of list) answer.append(s("path", { d: st.d, class: "t-solid" + (st.dot ? " dot" : "") }));
    const inkG = s("g"); svg.append(answer, inkG);
    const status = h("p", { class: "sub t-status" }, "Write it from memory. Stuck? Tap Show the letter.");
    let cur = null;
    const at = (e) => { const p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY; return p.matrixTransform(svg.getScreenCTM().inverse()); };
    svg.addEventListener("pointerdown", (e) => { const p = at(e); cur = s("path", { d: `M${p.x.toFixed(1)} ${p.y.toFixed(1)} l0.1 0.1`, class: "w-ink" }); inkG.append(cur); svg.setPointerCapture(e.pointerId); e.preventDefault(); });
    svg.addEventListener("pointermove", (e) => { if (!cur) return; const p = at(e); cur.setAttribute("d", cur.getAttribute("d") + ` L${p.x.toFixed(1)} ${p.y.toFixed(1)}`); });
    const up = () => { if (cur) { cur = null; done.disabled = false; } };
    svg.addEventListener("pointerup", up); svg.addEventListener("pointercancel", up);
    const peek = h("button", { class: "secondary small", onclick: () => { answer.style.display = ""; status.textContent = "Here it is. Write over it, or Clear and try again."; } }, "Show the letter");
    const clear = h("button", { class: "secondary small", onclick: () => { inkG.replaceChildren(); done.disabled = true; } }, "Clear");
    const done = h("button", { class: "primary", disabled: true, onclick: () => {
      answer.style.display = ""; status.textContent = "";
      bar.className = "checkbar good";
      bar.replaceChildren(h("div", { class: "fb-row" }, h("b", {}, "Compare yours with the print form."), speakBtn(it)),
        h("div", { class: "fb-ans" }, "Not graded. Close is good."), h("button", { class: "primary", onclick: next }, "Continue"));
      speak(it);
    } }, "Done");
    view.append(h("div", { class: "card trace-card" },
      h("div", { class: "t-head" }, h("span", {}, `Write ${it.name} (${it.sound || "silent"})`), speakBtn(it)),
      h("p", { class: "prompt-label" }, "From memory"), svg, status, h("div", { class: "row-btns" }, peek, clear)), bar);
    bar.append(h("button", { class: "secondary", onclick: next }, "Skip"), done);
  }

  // ---------- speaking: record yourself, compare by ear with the model (never graded) ----------
  const canRecord = () => state.settings.speak !== false && !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.MediaRecorder);
  let mine = null; // object URL of the latest take; kept in memory only, never saved
  const dropTake = () => { if (mine) URL.revokeObjectURL(mine); mine = null; };
  function renderSay(it, bar, next, id) {
    dropTake();
    let recorder = null, timer = null;
    const status = h("p", { class: "sub" }, canHear(it) ? "Listen, then record yourself saying it. Compare by ear; nothing is scored." : "Record yourself saying it, then play it back. (No model sound for this one yet.)");
    const playMine = (done) => { if (!mine) return done && done(); const a = new Audio(mine); a.onended = a.onerror = () => done && done(); a.play().catch(() => done && done()); };
    const mineBtn = h("button", { class: "secondary small", disabled: true, onclick: () => playMine() }, "▶ Mine");
    const bothBtn = h("button", { class: "secondary small", disabled: true, hidden: !canHear(it), onclick: () => speak(it, () => setTimeout(() => playMine(), 350)) }, "▶ Both");
    const recBtn = h("button", { class: "rec", "aria-label": "Record" }, h("span", { class: "rec-dot" }), h("span", { class: "rec-txt" }, "Record"));
    const stop = () => { clearTimeout(timer); if (recorder && recorder.state === "recording") recorder.stop(); };
    recBtn.addEventListener("click", async () => {
      if (recorder && recorder.state === "recording") return stop();
      speechSynthesis && speechSynthesis.cancel && speechSynthesis.cancel();
      let stream;
      try { stream = await navigator.mediaDevices.getUserMedia({ audio: true }); }
      catch (e) { status.textContent = "The microphone isn't available (permission may be off). You can still say it aloud and compare with the model."; return; }
      const chunks = [];
      recorder = new MediaRecorder(stream);
      recorder.ondataavailable = (e) => e.data.size && chunks.push(e.data);
      recorder.onstop = () => {
        stream.getTracks().forEach((t) => t.stop());
        recBtn.classList.remove("on"); recBtn.querySelector(".rec-txt").textContent = "Record again";
        dropTake(); mine = URL.createObjectURL(new Blob(chunks, { type: recorder.mimeType || "audio/webm" }));
        mineBtn.disabled = bothBtn.disabled = false;
        status.textContent = canHear(it) ? "Play them side by side. Record again as often as you like." : "Play it back. Record again as often as you like.";
        cont.textContent = "Continue";
        canHear(it) ? speak(it, () => setTimeout(() => playMine(), 350)) : playMine();
      };
      recorder.start();
      recBtn.classList.add("on"); recBtn.querySelector(".rec-txt").textContent = "Stop";
      status.textContent = "Recording… tap Stop when done.";
      timer = setTimeout(stop, 5000);
    });
    const cont = h("button", { class: "primary", onclick: () => { stop(); dropTake(); next(); } }, "Skip");
    view.append(h("div", { class: "card say-card" },
      h("p", { class: "prompt-label" }, it.kind === "letter" ? "Say the letter's name" : "Say it aloud"),
      h("div", { class: "big", lang: "he" }, it.he),
      speakBtn(it, true),
      hintBlock(id, it.name ? `${it.name} · ${it.sound}` : it.tr),
      recBtn, status, h("div", { class: "say-row" }, mineBtn, bothBtn)), bar);
    bar.append(cont);
    speak(it);
  }

  // ---------- lesson runner ----------
  let run = null;
  function buildLesson(lesson) {
    if (lesson.prayer) return buildPrayerLesson(lesson);
    const steps = [], second = [];
    const syls = lesson.items.filter((id) => course.items[id].kind === "syllable");
    for (const id of lesson.items) {
      const it = course.items[id];
      if (it.kind === "syllable") { steps.push({ id, mode: "read" }); continue; }
      if (!rec(id) || mastery(id) === 0) { // re-teach forgotten items, then trace new/forgotten letters
        steps.push({ id, mode: "intro" });
        if (canTrace(it)) steps.push({ id, mode: "trace" });
      }
      steps.push({ id, mode: "read" });
      if ((!rec(id) || mastery(id) === 0) && it.kind !== "letter" && canRecord() && canHear(it)) steps.push({ id, mode: "say" });
      const hear = canHear(it) && Math.random() < 0.5;
      second.push({ id, mode: hear ? "hear" : it.kind === "letter" || it.kind === "word" ? "find" : "read" });
    }
    shuffle(syls).slice(0, 5).forEach((id, n) => second.push({ id, mode: n % 2 && canHear(course.items[id]) ? "hear" : "find" }));
    const sayable = syls.filter((x) => canHear(course.items[x]));
    if (canRecord() && sayable.length) second.push({ id: shuffle(sayable)[0], mode: "say" });
    shuffle(lesson.items.filter((x) => course.items[x].kind === "word")).slice(0, lesson.drill ? 4 : 2).forEach((id) => second.push({ id, mode: "type" }));
    // write from memory (no stencil) for up to 2 letters of this lesson
    shuffle(lesson.items.filter((x) => course.items[x].kind === "letter" && canTrace(course.items[x]))).slice(0, 2).forEach((id) => second.push({ id, mode: "write" }));
    return steps.concat(shuffle(second));
  }
  function buildPractice(n = 12) {
    const seen = Object.keys(state.items).filter((id) => course.items[id]);
    const pick = seen.sort((a, b) => isDue(b) - isDue(a) || mastery(a) - mastery(b) || rec(a).last - rec(b).last).slice(0, n);
    const out = shuffle(pick).map((id) => {
      const it = course.items[id], r = Math.random();
      if (it.kind === "line") return { id, mode: r < 0.5 ? "order" : "fill" };
      if (it.kind === "word" && r > 0.85) return { id, mode: "type" };
      if (canHear(it) && r < 0.3) return { id, mode: "hear" };
      return { id, mode: it.kind === "vowel" || r < 0.65 ? "read" : "find" };
    });
    const sayId = pick.find((id) => !["letter", "line"].includes(course.items[id].kind) && canHear(course.items[id]));
    if (canRecord() && sayId && out.length > 4) out.splice(1 + Math.floor(Math.random() * (out.length - 1)), 0, { id: sayId, mode: "say" });
    shuffle(pick.filter((id) => course.items[id].kind === "letter" && canTrace(course.items[id]))).slice(0, 2)
      .forEach((id) => out.splice(Math.floor(Math.random() * (out.length + 1)), 0, { id, mode: "write" }));
    return out;
  }
  function startRun(title, steps, lessonIds) {
    run = { title, steps, i: 0, lessonIds, right: 0, wrong: 0, touched: new Set() };
    document.body.classList.add("in-lesson");
    $("#back").hidden = false; $("#back").textContent = "✕"; $("#back").setAttribute("aria-label", "Quit lesson");
    history.pushState({ lesson: true }, "");
    renderStep();
  }
  function endRun() {
    run = null; dropTake();
    document.body.classList.remove("in-lesson");
    $("#back").hidden = true;
    showTab(currentTab);
  }

  function hintBlock(id, text, quiz, btnLabel = "Show hint") {
    const lvl = quiz ? (state.settings.hints === "always" ? "show" : "hidden") : hintLevel(id);
    const box = h("div", { class: "hint" + (lvl === "faint" ? " faint" : "") });
    const reveal = () => { box.textContent = text; box.classList.remove("faint"); };
    if (lvl === "hidden") box.append(h("button", { onclick: reveal }, btnLabel));
    else box.textContent = text;
    return box;
  }
  const ansText = (it) => (it.name ? `${it.name} · ${it.sound}` : it.tr);

  function renderStep() {
    const { steps, i } = run;
    $("#title").textContent = run.title;
    if (i >= steps.length) return renderDone();
    const step = steps[i], it = course.items[step.id];
    const bar = h("div", { class: "checkbar" });
    const next = () => { run.i++; renderStep(); };
    const btn = (text, onclick, disabled) => h("button", { class: "primary", onclick, disabled }, text);
    view.replaceChildren(h("div", { class: "progress" }, h("i", { style: `width:${(i / steps.length) * 100}%` })));

    if (step.mode === "intro" && it.kind === "word") { view.append(wordCard(it, step.id), bar); bar.append(btn("Continue", next)); speak(it); return; }
    if (step.mode === "about") return renderAbout(it, bar, next);
    if (step.mode === "line") return renderLine(it, bar, next, step.id);
    if (step.mode === "order") return renderOrder(it, bar, next, step);
    if (step.mode === "fill") return renderFill(it, bar, next, step);
    if (step.mode === "type") return renderType(it, bar, next, step);
    if (step.mode === "intro") {
      view.append(h("div", { class: "card" },
        h("p", { class: "prompt-label" }, it.kind === "letter" ? (rec(step.id) ? "Refresher" : "New letter") : (rec(step.id) ? "Refresher" : "New vowel")),
        h("div", { class: "big", lang: "he" }, it.he),
        h("div", { class: "name" }, it.name),
        h("div", {}, "Sound: ", h("b", {}, it.sound)),
        h("div", { class: "note" }, it.note),
        it.flag ? h("div", { class: "flag" }, "Note: " + it.flag) : null,
        speakBtn(it, true)), bar);
      bar.append(btn("Continue", next));
      speak(it);
      return;
    }

    if (step.mode === "trace") return renderTrace(it, bar, next);
    if (step.mode === "say") return renderSay(it, bar, next, step.id);
    if (step.mode === "write") return renderWrite(it, bar, next);

    const heChoices = step.mode !== "read"; // find & hear: choose the Hebrew
    const keyOf = (x) => (heChoices ? course.items[x].he : label(course.items[x], step.mode));
    const answerKey = keyOf(step.id);
    const opts = shuffle([step.id, ...distractors(step.id, step.mode, run.lessonIds)]);
    let picked = null;
    const grade = () => {
      const ok = keyOf(picked) === answerKey;
      for (const b of view.querySelectorAll(".opt")) {
        b.disabled = true;
        if (b.dataset.key === answerKey) b.classList.add("right");
        else if (b.classList.contains("sel")) b.classList.add("wrong");
      }
      if (!run.touched.has(i)) {
        run.touched.add(i);
        mark(step.id, ok);
        ok ? run.right++ : run.wrong++;
        if (!ok && (step.retries || 0) < 2) steps.push({ ...step, retries: (step.retries || 0) + 1 });
      }
      bar.className = "checkbar " + (ok ? "good" : "bad");
      bar.replaceChildren(
        h("div", { class: "fb-row" }, h("b", {}, ok ? "Yes." : "Not quite."), speakBtn(it)),
        h("div", { class: "fb-ans" }, ok ? "" : "Answer: ", h("span", { class: "he-in", lang: "he" }, it.he), " ", ansText(it)),
        ...(!ok && it.kind === "letter" && it.note ? [h("div", { class: "note" }, it.note)] : []),
        ...(it.kind === "word" && it.gloss ? [h("div", { class: "note" }, glossText(it))] : []),
        btn("Continue", next));
      bar.querySelector(".primary").focus();
    };
    const check = btn("Check", grade, true);
    bar.append(check);

    let q, promptMain;
    if (step.mode === "hear") {
      q = it.kind === "letter" ? "Which letter is this?" : "Which one did you hear?";
      promptMain = h("button", { class: "speaker xl", "aria-label": "Play again", onclick: () => speak(it) }, "🔊");
    } else if (step.mode === "find") {
      q = it.kind === "syllable" || it.kind === "word" ? "Which reads like this?" : "Which letter is this?";
      promptMain = h("div", { class: "big mid" }, !it.name ? it.tr : `${it.name} (${it.sound})`);
    } else {
      q = it.kind === "syllable" || it.kind === "word" ? "What sound does this make?" : it.kind === "vowel" ? "What sound is this vowel?" : "Which letter is this?";
      promptMain = h("div", { class: "big" + (it.kind === "word" ? " word" : ""), lang: "he" }, it.he);
    }
    view.append(
      h("div", { class: "card" },
        h("p", { class: "prompt-label" }, q), promptMain,
        step.mode === "read" ? speakBtn(it) : null,
        hintBlock(step.id, hintFor(it, step.mode), true)),
      h("div", { class: "opts" }, opts.map((x) => {
        const key = keyOf(x);
        const b = h("button", { class: "opt" + (heChoices ? " he" : ""), lang: heChoices ? "he" : null, "data-key": key }, key);
        b.addEventListener("click", () => {
          picked = x;
          for (const o of view.querySelectorAll(".opt")) o.classList.toggle("sel", o === b);
          check.disabled = false;
        });
        return b;
      })),
      bar);
    if (step.mode === "hear") speak(it);
  }

  // ---------- words & blessings ----------
  function addPrayers(pd) {
    const lessons = pd.prayers.slice().sort((a, b) => (a.seq ?? a.order) - (b.seq ?? b.order)).map((p) => {
      prayers[p.id] = p;
      const items = p.lines.map((l, n) => {
        const id = `p-${p.id}-${n}`;
        course.items[id] = { kind: "line", he: l.he, tr: l.tl, tlf: l.tlf, en: l.en, en_src: l.en_src, en_license: l.en_license, reform: l.reform || [],
          prayer: p.id, n, say: l.he.replace(/יְיָ/g, "אֲדֹנָי"), audio: null };
        return id;
      });
      return { id: `pr-${p.id}`, title: p.title, subtitle: p.about, prayer: p.id, unit: p.unit || "blessings", items };
    });
    const UNITS = [["blessings", "Blessings", "Line by line, then word order and missing words"],
                   ["shma", "Sh'ma and its blessings", "Shabbat evening, Ma'ariv Aravim to V'shamru"],
                   ["amidah", "Amidah", "Shabbat evening, Avot v'Imahot to Shalom Rav"]];
    for (const [u, title, subtitle] of UNITS) {
      const ls = lessons.filter((l) => l.unit === u);
      if (ls.length) course.units.push({ id: u === "blessings" ? "u-blessings" : `u-${u}`, title, subtitle, tiles: false, lessons: ls });
    }
  }
  function buildPrayerLesson(lesson) {
    const steps = [{ id: lesson.items[0], mode: "about" }], second = [];
    for (const id of lesson.items) {
      steps.push({ id, mode: "line" });
      const n = heWords(course.items[id].he).length;
      if (n >= 3) second.push({ id, mode: "order" });
      if (n >= 2) second.push({ id, mode: "fill" });
    }
    return steps.concat(shuffle(second));
  }
  const flagNote = (it) => (it.tlf ? h("div", { class: "flag" }, "Transliteration to check with your cantor.") : null);
  function wordCard(it, id) {
    return h("div", { class: "card" },
      h("p", { class: "prompt-label" }, rec(id) ? "Refresher" : "New word"),
      h("div", { class: "big word", lang: "he" }, it.he),
      h("div", { class: "name" }, it.tr),
      it.gloss ? h("div", { class: "note" }, "Dictionary: ", h("span", { lang: "he" }, it.gloss.root), " ", it.gloss.def, h("small", { class: "src" }, " · BDB via Sefaria")) : null,
      it.note ? h("div", { class: "note" }, it.note) : null,
      it.prayers && it.prayers.length ? h("small", { class: "src" }, "In: " + it.prayers.map((p) => (prayers[p] ? prayers[p].title : p)).join(", ")) : null,
      flagNote(it), speakBtn(it, true));
  }
  function renderAbout(it, bar, next) {
    const p = prayers[it.prayer];
    view.append(h("div", { class: "card" },
      h("p", { class: "prompt-label" }, p.unit === "blessings" ? "Blessing" : "Prayer"),
      h("div", { class: "name" }, p.title), h("div", { class: "note" }, p.about),
      p.audio ? h("button", { class: "secondary", onclick: () => new Audio(p.audio).play().catch(() => toast("Couldn't play the recording.")) }, "▶ Hear it chanted")
        : h("small", { class: "src" }, "Chanting recording: not added yet."),
      h("small", { class: "src" }, "Hebrew: " + p.he_src),
      p.check && p.check.length ? h("div", { class: "flag" }, "To check against your siddur:", h("ul", {}, p.check.map((c) => h("li", {}, c)))) : null), bar);
    bar.append(h("button", { class: "primary", onclick: next }, "Start"));
  }
  function renderLine(it, bar, next, id) {
    const p = prayers[it.prayer];
    view.append(h("div", { class: "card" },
      h("p", { class: "prompt-label" }, `${p.title} · line ${it.n + 1} of ${p.lines.length}`),
      h("div", { class: "line-he", lang: "he", dir: "rtl" }, it.he),
      speakBtn(it, true),
      hintBlock(id, it.tr, false, "Show transliteration"),
      hintBlock(id, it.en || "No Sefaria translation for this line yet.", false, "Show translation"),
      it.en_src ? h("small", { class: "src" }, `English: ${it.en_src} (${it.en_license})`) : null,
      it.reform && it.reform.length ? h("div", { class: "flag" }, "Reform wording (Mishkan T'filah), to confirm: " + it.reform.join(" ")) : null,
      flagNote(it)), bar);
    bar.append(h("button", { class: "primary", onclick: next }, "Continue"));
  }
  function quizBar(step, ok, it, bar, next, extra) {
    if (!run.touched.has(run.i)) {
      run.touched.add(run.i); mark(step.id, ok); ok ? run.right++ : run.wrong++;
      if (!ok && (step.retries || 0) < 2) run.steps.push({ ...step, retries: (step.retries || 0) + 1 });
    }
    bar.className = "checkbar " + (ok ? "good" : "bad");
    bar.replaceChildren(h("div", { class: "fb-row" }, h("b", {}, ok ? "Yes." : "Not quite."), speakBtn(it)),
      ...extra.filter(Boolean), h("button", { class: "primary", onclick: next }, "Continue"));
    bar.querySelector(".primary").focus();
  }
  function renderOrder(it, bar, next, step) {
    const all = heWords(it.he);
    let a = 0, b = all.length;
    if (all.length > 7) { a = step.a != null ? step.a : Math.floor(Math.random() * (all.length - 5)); b = Math.min(all.length, a + 6); step.a = a; }
    const target = all.slice(a, b), bank = shuffle(target.map((w, k) => ({ w, k }))), placed = [];
    const ansBox = h("div", { class: "chips answer", lang: "he", dir: "rtl" }), bankBox = h("div", { class: "chips", lang: "he", dir: "rtl" });
    const check = h("button", { class: "primary", disabled: true, onclick: () => {
      const ok = placed.map((x) => x.w).join(" ") === target.join(" ");
      for (const c of view.querySelectorAll(".chip")) c.disabled = true;
      quizBar(step, ok, it, bar, next, [h("div", { class: "fb-ans" }, ok ? "" : "In order: ", h("span", { class: "he-in", lang: "he" }, target.join(" "))), h("div", { class: "note" }, it.tr)]);
    } }, "Check");
    const draw = () => {
      ansBox.replaceChildren(...placed.map((x) => h("button", { class: "chip", onclick: () => { placed.splice(placed.indexOf(x), 1); draw(); } }, x.w)));
      bankBox.replaceChildren(...bank.filter((x) => !placed.includes(x)).map((x) => h("button", { class: "chip", onclick: () => { placed.push(x); draw(); } }, x.w)));
      check.disabled = placed.length !== target.length;
    };
    draw();
    const part = a > 0 || b < all.length;
    view.append(h("div", { class: "card" },
      h("p", { class: "prompt-label" }, part ? "Put this part in order" : "Put the words in order"),
      part ? h("div", { class: "line-he ctx", lang: "he", dir: "rtl" }, [...all.slice(0, a), "[ … ]", ...all.slice(b)].join(" ")) : null,
      ansBox, hintBlock(step.id, it.tr, true, "Show transliteration")), bankBox, bar);
    bar.append(check);
  }
  function renderFill(it, bar, next, step) {
    const all = heWords(it.he);
    const k = step.k != null ? step.k : Math.floor(Math.random() * all.length); step.k = k;
    const ans = all[k];
    const pool = [...new Set(Object.values(course.items).filter((x) => x.kind === "word").map((x) => x.he))].filter((w) => w !== ans && !all.includes(w));
    const opts = shuffle([ans, ...shuffle(pool).slice(0, 3)]);
    let picked = null;
    const check = h("button", { class: "primary", disabled: true, onclick: () => {
      const ok = picked === ans;
      for (const o of view.querySelectorAll(".opt")) { o.disabled = true; if (o.dataset.key === ans) o.classList.add("right"); else if (o.classList.contains("sel")) o.classList.add("wrong"); }
      quizBar(step, ok, it, bar, next, [h("div", { class: "fb-ans" }, h("span", { class: "he-in", lang: "he" }, it.he)), h("div", { class: "note" }, it.tr)]);
    } }, "Check");
    view.append(h("div", { class: "card" },
      h("p", { class: "prompt-label" }, "Which word is missing?"),
      h("div", { class: "line-he", lang: "he", dir: "rtl" }, ...all.flatMap((w, j) => [j === k ? h("span", { class: "blank" }, "＿＿＿") : w, " "])),
      hintBlock(step.id, it.tr, true, "Show transliteration")),
      h("div", { class: "opts" }, opts.map((w) => {
        const b = h("button", { class: "opt he", lang: "he", "data-key": w }, w);
        b.addEventListener("click", () => { picked = w; for (const o of view.querySelectorAll(".opt")) o.classList.toggle("sel", o === b); check.disabled = false; });
        return b;
      })), bar);
    bar.append(check);
  }
  // lenient (sh'va ' may be typed as e): case, accents, apostrophes, hyphens, spaces, kh/ch, ts/tz, ei/e, doubled letters, final h
  const normTr = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/kh/g, "ch").replace(/x/g, "ch")
    .replace(/ts/g, "tz").replace(/ei/g, "e").replace(/[^a-z]/g, "").replace(/(.)\1+/g, "$1").replace(/h$/, "");
  function renderType(it, bar, next, step) {
    const inp = h("input", { class: "type-in", type: "text", autocomplete: "off", autocapitalize: "off", spellcheck: "false", placeholder: "Type how it sounds", "aria-label": "How it sounds" });
    const check = h("button", { class: "primary", disabled: true, onclick: () => {
      const v = normTr(inp.value), ok = v === normTr(it.tr) || v === normTr(it.tr.replace(/'/g, "e")); inp.disabled = true;
      quizBar(step, ok, it, bar, next, [h("div", { class: "fb-ans" }, ok ? `${it.tr}` : `Answer: ${it.tr}`), it.gloss ? h("div", { class: "note" }, glossText(it)) : null]);
    } }, "Check");
    inp.addEventListener("input", () => { check.disabled = !inp.value.trim(); });
    inp.addEventListener("keydown", (e) => { if (e.key === "Enter" && !check.disabled) check.click(); });
    view.append(h("div", { class: "card" }, h("p", { class: "prompt-label" }, "Type the sound"),
      h("div", { class: "big word", lang: "he" }, it.he), speakBtn(it), hintBlock(step.id, glossText(it), true, "Show meaning"), inp), bar);
    bar.append(check); inp.focus();
  }

  function renderDone() {
    const total = run.right + run.wrong;
    view.replaceChildren(
      h("div", { class: "progress" }, h("i", { style: "width:100%" })),
      h("div", { class: "card" },
        h("p", { class: "prompt-label" }, "Session complete"),
        h("div", { class: "big mid" }, `${run.right} / ${total}`),
        h("div", { class: "note" }, run.wrong ? "Missed items were repeated and will come back in Practice." : "Every answer on the first try.")),
      h("button", { class: "primary", onclick: () => history.back() }, "Done"));
  }

  // ---------- tabs ----------
  let currentTab = "learn";
  function showTab(tab) {
    currentTab = tab;
    for (const b of document.querySelectorAll(".tabs button")) b.classList.toggle("on", b.dataset.tab === tab);
    $("#title").textContent = { learn: "Kavanah", practice: "Practice", settings: "Settings" }[tab];
    ({ learn: renderLearn, practice: renderPractice, settings: renderSettings })[tab]();
    window.scrollTo(0, 0);
  }

  let gapDays = 0; // days since last session, measured at launch
  function reviewCard() {
    const seen = Object.keys(state.items).filter((id) => course.items[id]);
    const due = seen.filter(isDue).length;
    if (!seen.length) return null;
    if (gapDays >= 5) return h("div", { class: "card welcome" },
      h("div", { class: "name" }, "Welcome back"),
      h("p", { class: "note" }, `It's been ${Math.round(gapDays)} days. A short refresher will show what's still there and bring back what faded. Anything forgotten gets re-taught, not marked down.`),
      h("button", { class: "primary", onclick: () => { gapDays = 0; startRun("Refresher", buildPractice(15), seen); } }, "Start refresher"),
      h("button", { class: "secondary", onclick: () => { gapDays = 0; renderLearn(); } }, "Not now"));
    if (due) return h("button", { class: "lesson next", onclick: () => startRun("Review", buildPractice(Math.min(15, Math.max(8, due))), seen) },
      h("span", { class: "he" }, "↺"),
      h("span", { class: "meta" }, "Review", h("small", {}, `${due} item${due > 1 ? "s" : ""} fading — a quick pass keeps them`)));
    return null;
  }
  function tileGrid(u) {
    const ids = u.lessons.flatMap((l) => l.items).filter((id) => course.items[id].kind !== "syllable");
    return h("div", { class: "tiles" }, ids.map((id) => {
      const it = course.items[id], pct = Math.min(mastery(id), 3) / 3;
      const t = h("button", { class: "tile" + (isDue(id) ? " fading" : "") + (rec(id) ? "" : " new"), "aria-label": `${it.name}, ${it.sound}` },
        h("span", { class: "he", lang: "he" }, it.he),
        h("small", {}, it.kind === "letter" ? (it.tr || "silent") : it.tr === "'" ? "sh'va" : it.tr),
        h("div", { class: "bar" }, h("i", { style: `width:${Math.round(pct * 100)}%` })));
      t.addEventListener("click", () => {
        t.classList.remove("ping"); void t.offsetWidth; t.classList.add("ping");
        const les = allLessons().find((l) => l.items.includes(id));
        const practice = les ? { label: rec(id) ? "Practice this" : "Learn this", fn: () => startRun(les.title, buildLesson(les), les.items) } : null;
        if (canHear(it)) { speak(it); toast(`${it.name}${it.kind === "letter" ? " · " + (it.sound || "silent") : ""}`, [practice]); }
        else toast("No sound: this phone has no Hebrew voice installed yet. It takes about 2 minutes to add.", [{ label: "Show me how", fn: () => showTab("settings") }, practice]);
      });
      return t;
    }));
  }
  function renderLearn() {
    const next = allLessons().find((l) => lessonPct(l) < 0.67);
    const started = Object.keys(state.items).length > 0;
    const go = next
      ? h("button", { class: "primary cta", onclick: () => startRun(next.title, buildLesson(next), next.items) },
          started ? `Continue: ${next.title}` : "Learn the letters")
      : null;
    const noVoice = !heVoice && !Object.values(course.items).some((x) => x.audio)
      ? h("div", { class: "card notice" }, h("b", {}, "Sound is off: no Hebrew voice on this phone."),
          h("p", { class: "sub" }, "Without it, letters can't be heard and speaking practice is skipped. Adding it takes about 2 minutes."),
          h("button", { class: "secondary", onclick: () => showTab("settings") }, "Show me how")) : null;
    view.replaceChildren(reviewCard() || "", go || "", ...course.units.map((u) => h("section", {},
      h("h2", {}, u.title), h("p", { class: "sub" }, u.subtitle + (u.tiles === false ? "" : " · tap a tile to hear it or practice it. Gray = not learned yet.")),
      u.tiles === false ? "" : tileGrid(u),
      h("details", { class: "lessons", open: next && u.lessons.includes(next) },
        h("summary", {}, `Lessons (${u.lessons.length})`),
        u.lessons.map((l) => {
          const pct = lessonPct(l);
          const preview = l.prayer ? heWords(course.items[l.items[0]].he).slice(0, 2).join(" ") : l.items.filter((id) => course.items[id].kind !== "syllable").slice(0, 3).map((id) => course.items[id].he.replace("◌", "")).join(" ");
          return h("button", { class: "lesson" + (l === next ? " next" : ""), onclick: () => startRun(l.title, buildLesson(l), l.items) },
            h("span", { class: "he", lang: "he" }, preview),
            h("span", { class: "meta" }, l.subtitle ? `${l.title} · ${l.subtitle}` : l.title, h("small", {}, pct >= 0.99 ? "Mastered · tap to replay" : l === next ? "Up next" : l.items.some(isDue) ? "Fading · tap to refresh" : pct > 0 ? "Tap to replay" : `${l.items.length} items`),
              h("div", { class: "bar" }, h("i", { style: `width:${Math.round(pct * 100)}%` }))));
        })))), noVoice || "");
  }

  function renderPractice() {
    const ids = Object.keys(course.items).filter((id) => course.items[id].kind !== "syllable");
    const seen = Object.keys(state.items).filter((id) => course.items[id]);
    const strong = seen.filter((id) => mastery(id) >= 3).length;
    const due = seen.filter(isDue).length;
    view.replaceChildren(
      h("div", { class: "stats" },
        h("div", { class: "stat" }, h("b", {}, seen.length), h("small", {}, "practiced")),
        h("div", { class: "stat" }, h("b", {}, strong), h("small", {}, "solid")),
        h("div", { class: "stat" }, h("b", {}, due), h("small", {}, "fading"))),
      seen.length
        ? h("button", { class: "primary", onclick: () => startRun("Practice", buildPractice(), seen) }, due ? "Practice (fading items first)" : "Practice weakest items")
        : h("p", { class: "sub" }, "Practice opens once you've started a lesson."));
  }

  function renderSettings() {
    const sel = h("select", { id: "hints", onchange: (e) => { state.settings.hints = e.target.value; save(); } },
      [["auto", "Fade as I learn"], ["always", "Always show"], ["never", "Hidden (tap to show)"]].map(([v, t]) =>
        h("option", { value: v, selected: state.settings.hints === v }, t)));
    const file = h("input", { type: "file", accept: "application/json", hidden: true, onchange: async (e) => {
      try { const s = JSON.parse(await e.target.files[0].text()); if (s.items) { state = s; save(); showTab("settings"); } } catch (err) { msg.textContent = "That file couldn't be read."; }
    } });
    const msg = h("p", { class: "sub" });
    let armed = false;
    const reset = h("button", { class: "secondary", onclick: () => {
      if (!armed) { armed = true; reset.textContent = "Tap again to erase all progress"; return; }
      state = { items: {}, settings: state.settings }; save(); showTab("settings");
    } }, "Reset progress");
    view.replaceChildren(
      h("div", { class: "row" }, h("label", { for: "hints" }, "Transliteration hints"), sel),
      h("p", { class: "sub" }, "Hints are always one tap away. Revealing one never counts against you."),
      h("h2", {}, "Sound"),
      h("p", { class: "sub" }, heVoice ? `Hebrew voice: ${heVoice.name}. Your own recordings, once added, replace it item by item.`
        : "No Hebrew voice found. Samsung: Settings › General management › Text-to-speech › Preferred engine = Speech Recognition and Synthesis from Google, then its gear › Install voice data › Hebrew. Then Settings › Apps › Chrome › Force stop, and reopen this app."),
      h("p", { class: "sub" }, `Voices this browser can see: ${allVoices.length}` + (allVoices.length ? ` (${[...new Set(allVoices.map((v) => v.lang))].slice(0, 12).join(", ")}${allVoices.length > 12 ? ", …" : ""})` : "")),
      h("div", { class: "row" }, h("label", { for: "rate" }, "Speaking speed"),
        h("select", { id: "rate", onchange: (e) => { state.settings.rate = +e.target.value; save(); } },
          [[0.6, "Slow"], [0.8, "Relaxed"], [1, "Normal"]].map(([v, t]) => h("option", { value: v, selected: (state.settings.rate || 0.8) === v }, t)))),
      h("button", { class: "secondary", onclick: () => speak({ say: "שָׁלוֹם" }) }, "Test voice (shalom)"),
      h("div", { class: "row" }, h("label", { for: "speak" }, "Speaking practice"),
        h("select", { id: "speak", onchange: (e) => { state.settings.speak = e.target.value === "on"; save(); } },
          [["on", "On"], ["off", "Off"]].map(([v, t]) => h("option", { value: v, selected: (state.settings.speak !== false) === (v === "on") }, t)))),
      h("p", { class: "sub" }, "Record yourself and compare with the model by ear. Nothing is scored, and recordings are never saved."),
      h("h2", {}, "Your progress"),
      h("p", { class: "sub" }, "Saved on this device. Export a backup before clearing browser data or switching phones."),
      h("button", { class: "secondary", onclick: () => {
        const url = URL.createObjectURL(new Blob([JSON.stringify(state)], { type: "application/json" }));
        h("a", { href: url, download: `kavanah-progress-${new Date().toISOString().slice(0, 10)}.json` }).click();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
      } }, "Export backup"),
      h("button", { class: "secondary", onclick: () => file.click() }, "Import backup"), file,
      reset, msg,
      h("h2", {}, "About"),
      h("p", { class: "sub" }, `Version ${self.APP_VERSION || "?"}. If this doesn't match the latest, close and reopen the app.`),
      h("p", { class: "sub" }, "Breathing, sleep and soundscapes live in ", h("a", { href: "https://neshamah.netlify.app/", target: "_blank", rel: "noopener" }, "Neshamah"), "."),
      h("p", { class: "sub" }, "Open wording questions for your rabbi or cantor: ", h("a", { href: "questions.html", target: "_blank", rel: "noopener" }, "printable list"), "."));
  }

  // ---------- boot ----------
  $("#tabs").addEventListener("click", (e) => { const t = e.target.closest("button"); if (t) showTab(t.dataset.tab); });
  $("#back").addEventListener("click", () => history.back());
  window.addEventListener("popstate", () => { if (run) endRun(); });

  async function boot() {
    load();
    try { navigator.storage && navigator.storage.persist && navigator.storage.persist(); } catch (e) {}
    pickVoice();
    if ("speechSynthesis" in window) speechSynthesis.addEventListener("voiceschanged", () => { const had = heVoice; pickVoice(); if (!had && heVoice && !run) showTab(currentTab); });
    if (state.lastActive) gapDays = (Date.now() - state.lastActive) / DAY;
    for (const f of DATA_FILES) {
      const d = await (await fetch(f)).json();
      course.units.push(...d.units);
      Object.assign(course.items, d.items);
    }
    try { addPrayers(await (await fetch("data/prayers.json")).json()); } catch (e) { console.warn("prayers", e); }
    try { strokes = await (await fetch("data/strokes.json")).json(); } catch (e) { strokes = null; }
    showTab("learn");
  }
  boot().catch((e) => { view.textContent = "Couldn't load lessons. " + e.message; });
  if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js", { updateViaCache: "none" }).catch(() => {});
})();
