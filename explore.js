/* Kavanah Explore: Imprint-style card lessons (Torah stories, history, Kabbalah).
   Data: data/explore.json (built by tools/build_explore.py). Progress: one state.items entry per idea ("x:<lesson>:<idea>"),
   so ideas fade and come back like letters. state.missed = To revisit list, state.notes = reflections,
   state.flags = cards Jamie doubts, state.reviewed = lessons she has checked, state.xseen = furthest card reached. */
self.KavanahExplore = (api) => {
  "use strict";
  const { h, $, view, toast, shuffle, mark, mastery, isDue, rec, save, DAY } = api;
  const S = () => api.state();
  const bag = (k) => S()[k] || (S()[k] = {});
  let data = { tracks: [] }, track = "stories", xr = null;
  const lessons = {}, ideaChecks = {}; // lesson id -> lesson; idea key -> [{l, c}]
  const SRC = { torah: "Torah", tanakh: "Tanakh", rabbinic: "Rabbinic", apocrypha: "Apocrypha", liturgy: "Liturgy",
    kabbalah: "Kabbalah", scholarly: "Scholars", tradition: "Tradition", reform: "Reform" };
  const SEFARIA = new Set(["torah", "tanakh", "rabbinic", "apocrypha", "liturgy", "kabbalah"]);
  const key = (lid, idea) => `x:${lid}:${idea}`;
  const ideasOf = (l) => [...new Set(l.cards.filter((c) => c.kind === "check" && !c.pretest).map((c) => c.idea))];
  const pct = (l) => { const ids = ideasOf(l); return ids.length ? ids.reduce((s, i) => s + Math.min(mastery(key(l.id, i)), 3) / 3, 0) / ids.length : 0; };
  const today = () => Math.floor(Date.now() / DAY);
  // **word** = signaled key word (bold); no HTML from data except diagram svg
  const rich = (s) => (s || "").split(/\*\*(.+?)\*\*/).map((t, i) => (i % 2 ? h("b", {}, t) : t));
  const he = (t, cls = "line-he") => h("div", { class: cls, lang: "he", dir: "rtl" }, t);

  async function load() {
    try { data = await (await fetch("data/explore.json")).json(); } catch (e) { data = { tracks: [] }; }
    for (const t of data.tracks) for (const u of t.units) for (const l of u.lessons) {
      l.track = t.id; l.unit = u.title; lessons[l.id] = l;
      l.cards.forEach((c, n) => { c.n = n; if (c.kind === "check" && !c.pretest) (ideaChecks[key(l.id, c.idea)] ||= []).push({ l, c }); });
    }
  }

  // ---------- small parts ----------
  function srcChip(c) {
    if (!c.src) return null;
    const s = c.src, box = h("div", { class: "src-more", hidden: true },
      s.ref ? h("div", {}, "Reference: ", s.ref) : null,
      s.note ? h("div", {}, s.note) : null,
      SEFARIA.has(s.type) && s.ref ? h("a", { href: "https://www.sefaria.org/" + encodeURI(s.ref.replace(/ /g, "_")), target: "_blank", rel: "noopener" }, "Read it on Sefaria") : null);
    const b = h("button", { class: "srcchip t-" + s.type, onclick: () => { box.hidden = !box.hidden; } }, SRC[s.type] + (s.ref ? " · " + s.ref : ""));
    return h("div", { class: "srcwrap" }, b, box);
  }
  function flagBtn(l, c) {
    const k = `${l.id}#${c.n}`, flags = bag("flags");
    const ta = h("textarea", { rows: 2, placeholder: "What looks wrong or unclear? (optional)" });
    const panel = h("div", { class: "flagpanel", hidden: true }, ta,
      h("div", { class: "row-btns" },
        h("button", { class: "secondary sm", onclick: () => { flags[k] = { note: ta.value.trim(), at: Date.now(), lesson: l.title, card: c.title || c.q || c.kind }; save(); panel.hidden = true; b.textContent = "⚑ Flagged"; toast("Flagged. The list is in Settings."); } }, "Save flag"),
        h("button", { class: "secondary sm", onclick: () => { delete flags[k]; save(); panel.hidden = true; b.textContent = "⚑ Flag"; } }, "Remove")));
    const b = h("button", { class: "flagbtn", onclick: () => { ta.value = flags[k]?.note || ""; panel.hidden = !panel.hidden; } }, flags[k] ? "⚑ Flagged" : "⚑ Flag");
    return h("div", {}, b, panel);
  }
  const foot = (l, c) => h("div", { class: "xfoot" }, srcChip(c) || h("span"), l ? flagBtn(l, c) : null);

  // ---------- content cards ----------
  function cardBody(l, c) {
    switch (c.kind) {
      case "hook": case "concept":
        return [c.title ? h("div", { class: "name" }, c.title) : null, h("p", { class: "xbody" }, rich(c.body))];
      case "term":
        return [h("p", { class: "prompt-label" }, "Key term"), he(c.he, "big word"), c.tl ? h("div", { class: "name" }, c.tl) : null,
          h("p", { class: "xbody" }, rich(c.gloss)), c.tlf ? h("div", { class: "flag" }, "Transliteration to check.") : null];
      case "text":
        return [h("p", { class: "prompt-label" }, c.ref), he(c.he), c.tl ? h("div", { class: "hint" }, c.tl) : null,
          h("p", { class: "xbody" }, c.en), h("small", { class: "src" }, `English: ${c.en_src} (${c.license})`)];
      case "timeline": {
        const pts = l.cards.filter((x) => x.kind === "timeline");
        return [h("ol", { class: "tl-strip" }, pts.map((x) => h("li", { class: x === c ? "on" : "" }, h("b", {}, x.when), h("span", {}, x === c ? rich(x.body) : x.body))))];
      }
      case "diagram": { const d = h("div", { class: "diagram", html: c.svg }); return [c.title ? h("div", { class: "name" }, c.title) : null, d, c.body ? h("p", { class: "xbody" }, rich(c.body)) : null]; }
      case "relevance":
        return [h("p", { class: "prompt-label" }, "Where you meet this"), h("p", { class: "xbody" }, rich(c.body)),
          ...(c.links || []).map((ln) => h("button", { class: "secondary", onclick: () => follow(ln) }, linkLabel(ln)))];
      case "reflect": {
        const k = `${l.id}#${c.n}`, notes = bag("notes");
        const ta = h("textarea", { rows: 4, placeholder: "Only you see this. Skip it if you like." });
        ta.value = notes[k]?.text || "";
        ta.addEventListener("input", () => { notes[k] = { text: ta.value, at: Date.now() }; save(); });
        return [h("p", { class: "prompt-label" }, "Your turn"), h("p", { class: "xbody" }, rich(c.prompt)), ta];
      }
      case "recap": return recapBody(l, c);
      case "summary": return c.body;
    }
    return [h("p", {}, "Unknown card.")];
  }
  const linkLabel = (ln) => { const [t, id] = ln.split(":"); return t === "prayer" ? `Open the prayer: ${api.prayerTitle(id) || id}` : t === "lesson" ? `Open lesson: ${lessons[id]?.title || id}` : ln; };
  function follow(ln) {
    const [t, id] = ln.split(":");
    if (t === "prayer") { if (!api.prayerTitle(id)) return toast("That prayer isn't in the app yet."); end(true); api.openPrayer(id); }
    else if (t === "lesson") { if (!lessons[id]) return toast("That lesson isn't written yet."); end(true); start(lessons[id]); }
  }
  function recapBody(l, c) {
    const pre = l.cards.filter((x) => x.pretest && xr && xr.pre[x.n] != null);
    const missedHere = Object.keys(bag("missed")).filter((k) => k.startsWith(`x:${l.id}:`)).length;
    const reviewed = bag("reviewed");
    const rb = h("button", { class: "secondary", onclick: () => {
      reviewed[l.id] ? delete reviewed[l.id] : (reviewed[l.id] = Date.now()); save();
      rb.textContent = reviewed[l.id] ? "Reviewed ✓ (tap to undo)" : "Mark this lesson reviewed"; } },
      reviewed[l.id] ? "Reviewed ✓ (tap to undo)" : "Mark this lesson reviewed");
    return [h("p", { class: "prompt-label" }, "Takeaways"), h("ul", { class: "xlist" }, c.points.map((p) => h("li", {}, rich(p)))),
      ...pre.map((x) => h("div", { class: "note pre" }, h("b", {}, "Your first guess: "), x.choices[xr.pre[x.n]], h("br"), h("b", {}, "Answer: "), x.choices[x.answer], ". ", x.why)),
      missedHere ? h("div", { class: "note" }, `${missedHere} idea${missedHere > 1 ? "s" : ""} from this lesson on your To revisit list (Practice tab). They come back in new forms until you get each right on two different days.`) : null,
      l.check_note ? h("div", { class: "flag" }, "To confirm: " + l.check_note) : null,
      h("div", { class: "flag" }, "Accuracy: tap any card's source to check it; flag anything doubtful."), rb];
  }

  // ---------- checks ----------
  function renderCheck(entry, bar, done) {
    const c = entry.c, l = entry.l;
    const isOrder = c.type === "order";
    const order = isOrder ? null : (c.type === "tf" ? [0, 1] : shuffle(c.choices.map((_, i) => i)));
    let picked = null, placed = [], sure = false;
    const check = h("button", { class: "primary", disabled: true, onclick: () => grade(false) }, "Check");
    const sureBtn = h("button", { class: "chip sure", "aria-pressed": "false", onclick: () => { sure = !sure; sureBtn.classList.toggle("on", sure); sureBtn.setAttribute("aria-pressed", sure); } }, "I'm sure");
    const dunno = h("button", { class: "linkbtn", onclick: () => grade(true) }, "I don't know, show me");
    let opts, ansRow, pool;
    if (isOrder) {
      let items = shuffle(c.items); while (items.join() === c.items.join()) items = shuffle(c.items);
      ansRow = h("div", { class: "chips answer xorder" }); pool = h("div", { class: "chips xorder" });
      const draw = () => {
        ansRow.replaceChildren(...placed.map((t, i) => h("button", { class: "chip", onclick: () => { placed.splice(i, 1); draw(); } }, `${i + 1}. ${t}`)));
        pool.replaceChildren(...items.filter((t) => !placed.includes(t)).map((t) => h("button", { class: "chip", onclick: () => { placed.push(t); draw(); } }, t)));
        check.disabled = placed.length !== items.length;
      };
      draw();
    } else {
      opts = h("div", { class: "xopts" }, order.map((i) => {
        const b = h("button", { class: "opt xopt", "data-i": i }, c.choices[i]);
        b.addEventListener("click", () => { picked = i; for (const o of opts.children) o.classList.toggle("sel", o === b); check.disabled = false; });
        return b;
      }));
    }
    const label = c.pretest ? "First, a guess" : entry.retry ? "Try it again, a new way" : c.type === "why" ? "Pick the best reason" : c.type === "order" ? "Put in order" : "Quick check";
    view.append(h("div", { class: "card xcard" }, h("p", { class: "prompt-label" }, label), h("p", { class: "xq" }, rich(c.q)),
      isOrder ? [ansRow, pool] : opts, c.pretest ? h("p", { class: "sub" }, "Guessing before you learn helps it stick. Nothing rides on it.") : null, foot(l, c)), bar);
    bar.replaceChildren(c.pretest ? "" : h("div", { class: "row-btns" }, sureBtn, dunno), check);

    function grade(gaveUp) {
      const ok = !gaveUp && (isOrder ? placed.join("\u0001") === c.items.join("\u0001") : picked === c.answer);
      if (opts) for (const o of opts.children) { o.disabled = true; const i = +o.dataset.i; if (i === c.answer) o.classList.add("right"); else if (i === picked) o.classList.add("wrong"); }
      if (pool) for (const b of view.querySelectorAll(".xorder .chip")) b.disabled = true;
      const right = isOrder ? c.items.map((t, i) => `${i + 1}. ${t}`).join("  ") : c.choices[c.answer];
      if (c.pretest) {
        xr.pre[c.n] = gaveUp ? null : picked;
        bar.className = "checkbar"; bar.replaceChildren(h("div", { class: "fb-row" }, h("b", {}, "Noted.")), h("div", { class: "note" }, "The lesson answers this. Your guess comes back at the end."), h("button", { class: "primary", onclick: done }, "Continue"));
        return;
      }
      if (!entry.graded) { entry.graded = true; record(entry, ok, gaveUp, sure); }
      const yours = gaveUp ? null : isOrder ? placed.map((t, i) => `${i + 1}. ${t}`).join("  ") : c.choices[picked];
      const tempting = !gaveUp && !isOrder && c.wrong_why ? c.wrong_why[picked] : null;
      bar.className = "checkbar " + (ok ? "good" : "bad");
      bar.replaceChildren(...[
        h("div", { class: "fb-row" }, h("b", {}, ok ? "Yes." : gaveUp ? "Here it is." : sure ? "Not quite, and worth a second look." : "Not quite.")),
        !ok && yours ? h("div", { class: "fb-ans" }, h("b", {}, "You said: "), yours, tempting ? h("div", { class: "note" }, "Why it's tempting: ", tempting) : null) : null,
        h("div", { class: "fb-ans" }, ok ? "" : h("b", {}, "Answer: "), ok ? "" : right, h("div", { class: "note" }, rich(c.why))),
        !ok ? h("div", { class: "note" }, "It's on your To revisit list and comes back later in a different form.") : null,
        h("div", { class: "row-btns" },
          !ok && c.look_again != null ? h("button", { class: "secondary", onclick: () => lookAgain(l, l.cards[c.look_again]) }, "Look again") : null,
          h("button", { class: "primary", onclick: done }, "Continue"))].filter(Boolean));
      bar.querySelector(".primary").focus();
    }
  }
  function record(entry, ok, gaveUp, sure) {
    const c = entry.c, k = key(entry.l.id, c.idea), missed = bag("missed");
    mark(k, ok);
    ok ? xr.right++ : xr.wrong++;
    if (!ok) {
      missed[k] = { lesson: entry.l.id, cid: c.id, sure: !!sure && !gaveUp, at: Date.now(), fixed: [] };
      if (!xr.retried.has(k)) { xr.retried.add(k); queueRetry(k, c.id); }
    } else if (missed[k]) {
      const f = missed[k].fixed; if (!f.includes(today())) f.push(today());
      missed[k].cid = c.id;
      if (f.length >= 2) delete missed[k];
    }
    save();
  }
  // another question form for the same idea, if there is one
  function altForm(k, avoidId) {
    const forms = ideaChecks[k] || [];
    const others = forms.filter((f) => f.c.id !== avoidId);
    return (others.length ? shuffle(others) : forms)[0];
  }
  function queueRetry(k, cid) {
    const f = altForm(k, cid); if (!f) return;
    const q = xr.queue, at = q.length && ["recap", "summary"].includes(q[q.length - 1].c.kind) ? q.length - 1 : q.length;
    q.splice(Math.max(at, xr.i + 1), 0, { l: f.l, c: f.c, retry: true });
  }
  function lookAgain(l, c) {
    const ov = h("div", { class: "overlay" }, h("div", { class: "card xcard" }, h("p", { class: "prompt-label" }, "Look again"), ...cardBody(l, c), foot(null, c)),
      h("button", { class: "primary", onclick: () => ov.remove() }, "Back"));
    document.body.append(ov);
  }

  // ---------- runs ----------
  function begin(title, queue) {
    xr = { title, queue, i: 0, pre: {}, right: 0, wrong: 0, retried: new Set() };
    document.body.classList.add("in-lesson");
    $("#back").hidden = false; $("#back").textContent = "✕"; $("#back").setAttribute("aria-label", "Quit lesson");
    history.pushState({ lesson: true }, "");
    step();
  }
  function start(l) { begin(l.title, l.cards.map((c) => ({ l, c }))); }
  function startReview(keys, title) {
    const q = shuffle(keys).map((k) => { const m = bag("missed")[k]; const f = altForm(k, m && m.cid); return f && { l: f.l, c: f.c, retry: !!m }; }).filter(Boolean);
    if (!q.length) return toast("Nothing to review yet.");
    q.push({ l: null, c: { kind: "summary", n: -1, body: null } });
    begin(title, q);
  }
  function step() {
    const { queue, i } = xr;
    $("#title").textContent = xr.title;
    if (i >= queue.length) return history.back();
    const e = queue[i], c = e.c, l = e.l;
    if (l) { const seen = bag("xseen"); seen[l.id] = Math.max(seen[l.id] || 0, c.n + 1); }
    const bar = h("div", { class: "checkbar" });
    const next = () => { xr.i++; step(); };
    const prev = () => { if (xr.i > 0) { xr.i--; step(); } };
    view.replaceChildren(h("div", { class: "progress" }, h("i", { style: `width:${(i / queue.length) * 100}%` })));
    window.scrollTo(0, 0);
    if (c.kind === "check") return renderCheck(e, bar, next);
    if (c.kind === "summary") c.body = [h("p", { class: "prompt-label" }, "Review done"), h("div", { class: "big mid" }, `${xr.right} / ${xr.right + xr.wrong}`),
      h("p", { class: "note" }, xr.wrong ? "Missed ideas stay on your To revisit list and come back in new forms." : "All of them held.")];
    const card = h("div", { class: "card xcard" }, l ? h("p", { class: "kicker" }, `${l.unit} · ${c.n + 1} of ${l.cards.length}`) : null, ...cardBody(l, c), l ? foot(l, c) : null);
    swipe(card, next, prev);
    view.append(card, bar);
    const last = i === queue.length - 1;
    bar.append(h("div", { class: "row-btns" },
      i > 0 && queue[i - 1].c.kind !== "check" ? h("button", { class: "secondary", onclick: prev }, "Back") : null,
      h("button", { class: "primary", onclick: last ? () => history.back() : next }, last ? "Done" : "Next")));
    save();
  }
  function swipe(el, next, prev) {
    let x0 = null, y0 = 0;
    el.addEventListener("pointerdown", (e) => { if (e.target.closest("button,a,textarea")) return; x0 = e.clientX; y0 = e.clientY; });
    el.addEventListener("pointerup", (e) => {
      if (x0 == null) return; const dx = e.clientX - x0, dy = e.clientY - y0; x0 = null;
      if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) (dx < 0 ? next : prev)();
    });
  }
  function end(silent) {
    xr = null; document.querySelector(".overlay")?.remove();
    document.body.classList.remove("in-lesson"); $("#back").hidden = true;
    if (!silent) api.showTab("explore");
  }

  // ---------- tab views ----------
  const allKeys = () => Object.keys(ideaChecks);
  const dueKeys = () => allKeys().filter((k) => rec(k) && isDue(k));
  const missedKeys = () => { const m = bag("missed"); return Object.keys(m).filter((k) => ideaChecks[k]).sort((a, b) => m[b].sure - m[a].sure || m[a].at - m[b].at); };
  function reviewBlock() {
    const due = dueKeys(), miss = missedKeys();
    if (!due.length && !miss.length) return null;
    return h("div", { class: "card notice xreview" },
      h("div", { class: "name" }, "Ideas to bring back"),
      h("p", { class: "note" }, [due.length ? `${due.length} fading` : "", miss.length ? `${miss.length} to revisit` : ""].filter(Boolean).join(" · ")),
      h("button", { class: "primary", onclick: () => startReview([...new Set([...miss, ...due])].slice(0, 10), "Idea review") }, "Review ideas"),
      miss.length ? h("button", { class: "secondary", onclick: revisitList }, "See what I missed") : null);
  }
  function render() {
    const t = data.tracks.find((x) => x.id === track) || { units: [] };
    const reviewed = bag("reviewed"), seen = bag("xseen");
    const seg = h("div", { class: "seg" }, data.tracks.map((x) => h("button", { class: x.id === track ? "on" : "", onclick: () => { track = x.id; render(); } }, ({ stories: "Stories", history: "History", kabbalah: "Kabbalah" })[x.id] || x.title)));
    const empty = { stories: "Coming next: Genesis, starting with Creation.", history: "Not written yet. Planned after the Torah stories.", kabbalah: "Not written yet. Planned after Genesis and Exodus." }[track];
    view.replaceChildren(seg, reviewBlock() || "",
      ...(t.units.length ? t.units.map((u) => h("section", {}, h("h2", {}, u.title), u.subtitle ? h("p", { class: "sub" }, u.subtitle) : null,
        u.lessons.map((l, n) => {
          const p = pct(l), fading = ideasOf(l).some((i) => isDue(key(l.id, i)));
          const status = (reviewed[l.id] || l.status === "reviewed") ? "Reviewed" : "Draft";
          const prog = p >= 0.99 ? "Mastered · tap to replay" : fading ? "Fading · tap to refresh" : seen[l.id] ? `Card ${Math.min(seen[l.id], l.cards.length)} of ${l.cards.length}` : `${l.cards.length} cards`;
          return h("button", { class: "lesson", onclick: () => start(l) }, h("span", { class: "he num" }, n + 1),
            h("span", { class: "meta" }, l.title, h("small", {}, `${prog} · ${status}`), h("div", { class: "bar" }, h("i", { style: `width:${Math.round(p * 100)}%` }))));
        }))) : [h("div", { class: "card notice" }, h("p", { class: "note" }, empty))]));
  }
  function revisitList() {
    const m = bag("missed"); window.scrollTo(0, 0);
    $("#title").textContent = "To revisit";
    view.replaceChildren(h("p", { class: "sub" }, "Each idea leaves this list once you get it right on two different days. Ones you were sure about come first."),
      h("button", { class: "primary", onclick: () => startReview(missedKeys().slice(0, 10), "To revisit") }, "Practice these"),
      ...missedKeys().map((k) => {
        const r = m[k], f = (ideaChecks[k].find((x) => x.c.id === r.cid) || ideaChecks[k][0]), c = f.c, l = f.l;
        return h("div", { class: "card revisit" }, h("small", { class: "src" }, `${l.title}${r.sure ? " · you were sure" : ""}${r.fixed.length ? " · right once, once more to go" : ""}`),
          h("p", { class: "xq" }, rich(c.q)), h("div", { class: "note" }, h("b", {}, "Answer: "), c.type === "order" ? c.items.join(" → ") : c.choices[c.answer], ". ", rich(c.why)),
          c.look_again != null ? h("button", { class: "secondary sm", onclick: () => lookAgain(l, l.cards[c.look_again]) }, "Look again") : null);
      }),
      h("button", { class: "secondary", onclick: () => api.showTab(api.currentTab()) }, "Back"));
  }
  function practiceBlock() {
    if (!allKeys().length) return null;
    const seen = allKeys().filter((k) => rec(k));
    return h("section", {}, h("h2", {}, "Ideas (Explore)"),
      h("p", { class: "sub" }, `${seen.length} practiced · ${dueKeys().length} fading · ${missedKeys().length} to revisit`),
      seen.length ? h("button", { class: "secondary", onclick: () => startReview([...new Set([...missedKeys(), ...dueKeys(), ...shuffle(seen)])].slice(0, 10), "Idea review") }, "Review ideas") : null,
      missedKeys().length ? h("button", { class: "secondary", onclick: revisitList }, "See what I missed") : null);
  }
  function settingsBlock() {
    const flags = bag("flags"), ks = Object.keys(flags);
    return h("section", {}, h("h2", {}, "Flagged cards"),
      h("p", { class: "sub" }, ks.length ? "Cards you marked as doubtful. Bring these to your next session with Claude or your rabbi." : "None yet. Use ⚑ Flag on any Explore card you doubt."),
      ks.map((k) => h("div", { class: "row" }, h("label", {}, `${flags[k].lesson}: ${flags[k].card}`, flags[k].note ? h("small", { class: "src" }, flags[k].note) : null),
        h("button", { class: "secondary sm", onclick: () => { delete flags[k]; save(); api.showTab("settings"); } }, "Remove"))));
  }
  return { load, render, active: () => !!xr, end, practiceBlock, settingsBlock };
};
