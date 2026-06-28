/* =====================================================================
   slides.js — slide engine controller
   ---------------------------------------------------------------------
   Features:
     * one-slide-at-a-time deck with smooth transitions
     * reveal-style fragments (.frag) advanced with the same arrow keys
     * "Under the hood" panels: click to expand math/mechanism in place;
       a global depth toggle ('m') flips every panel on the deck
     * overview grid ('o'), help ('?'), progress bar, counter, deep links (#3)
     * KaTeX auto-render of $...$ and \[...\]
   The deck is fully keyboard- and click-driven; no build step required.
   ===================================================================== */
(function () {
  "use strict";

  function el(tag, cls) { const n = document.createElement(tag); if (cls) n.className = cls; return n; }

  const deck = document.querySelector(".deck");
  const stage = document.querySelector(".stage");
  const slides = Array.from(document.querySelectorAll(".slide"));
  let idx = 0;

  /* ---------- build chrome ---------- */
  const progress = el("div", "progress");
  document.body.appendChild(progress);

  const meta = window.DECK_META || {};
  const hud = el("div", "hud");
  hud.innerHTML = `
    <a class="brand" href="../index.html" title="All lectures"><span class="dot"></span><span class="full">${meta.course || "LLM in Finance"}</span></a>
    <button class="navbtn" id="prev" title="Previous (←)">‹</button>
    <button class="navbtn" id="next" title="Next (→)">›</button>
    <span class="counter" id="counter">1 / ${slides.length}</span>
    <div class="spacer"></div>
    <button class="btn" id="depth" title="Toggle technical depth (m)">⚙ <span>Under the hood</span></button>
    <button class="btn" id="overview" title="Overview (o)">▦ Overview</button>
    <button class="btn" id="fsbtn" title="Fullscreen (f)">⛶ <span>Fullscreen</span></button>
    <button class="btn" id="helpbtn" title="Help (?)">?</button>`;
  document.body.appendChild(hud);

  /* overview grid */
  const ovGrid = el("div", "overview-grid");
  slides.forEach((s, i) => {
    const card = el("div", "ov-card" + (s.classList.contains("section-slide") ? " is-section" : ""));
    const t = s.querySelector("h1,h2");
    const tag = s.classList.contains("title-slide") ? "Title"
      : s.classList.contains("section-slide") ? "Section" : "Slide " + i;
    card.innerHTML = `<div class="ov-n">${tag}</div><div class="ov-t">${t ? t.textContent : ""}</div>`;
    card.addEventListener("click", () => { go(i); toggleOverview(false); });
    ovGrid.appendChild(card);
  });
  document.body.appendChild(ovGrid);

  /* help overlay */
  const help = el("div", "help");
  help.innerHTML = `<div class="card">
    <h3>Navigation</h3>
    <table>
      <tr><td><kbd>→</kbd><kbd>Space</kbd></td><td>Next step / slide</td></tr>
      <tr><td><kbd>←</kbd></td><td>Previous</td></tr>
      <tr><td><kbd>m</kbd></td><td>Show / hide all "under the hood" math</td></tr>
      <tr><td><kbd>o</kbd></td><td>Slide overview</td></tr>
      <tr><td><kbd>f</kbd></td><td>Fullscreen</td></tr>
      <tr><td><kbd>Home</kbd><kbd>End</kbd></td><td>First / last slide</td></tr>
      <tr><td><kbd>?</kbd></td><td>This help</td></tr>
    </table>
    <p class="small" style="margin-bottom:0">Tip: the warm <b style="color:#B48228">◆ bigger picture</b> boxes are the intuition;
    the blue <b style="color:#0E4B8C">⚙ under the hood</b> panels hold the math — click any to expand.</p>
  </div>`;
  help.addEventListener("click", () => help.classList.remove("show"));
  document.body.appendChild(help);

  /* ---------- under-the-hood panels: build from <aside class="underhood"> ---------- */
  document.querySelectorAll("aside.underhood").forEach((node) => {
    const title = node.getAttribute("data-title") || "The mechanism";
    const inner = node.innerHTML;
    node.innerHTML = "";
    const btn = el("button", "uh-toggle");
    btn.innerHTML = `<span class="gear">⚙</span><span class="chev">▸</span><span>Under the hood — ${title}</span>`;
    const body = el("div", "uh-body");
    const wrap = el("div", "uh-inner");
    wrap.innerHTML = `<span class="uh-tag">under the hood</span>` + inner +
      `<div><button class="uh-back">‹ back to the big picture</button></div>`;
    body.appendChild(wrap);
    node.appendChild(btn); node.appendChild(body);
    btn.addEventListener("click", () => node.classList.toggle("open"));
    wrap.querySelector(".uh-back").addEventListener("click", () => {
      node.classList.remove("open");
      node.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  });

  /* ---------- fragments per slide ---------- */
  function frags(s) { return Array.from(s.querySelectorAll(".frag")); }
  function shownFrags(s) { return frags(s).filter(f => f.classList.contains("in")).length; }
  function showAllFrags(s) { frags(s).forEach(f => f.classList.add("in")); }
  function hideAllFrags(s) { frags(s).forEach(f => f.classList.remove("in")); }

  /* ---------- navigation ----------
     render() only positions slides; it never touches fragment state.
     next()/prev() reveal fragments progressively; any *jump* (go) reveals
     the whole slide so it never lands on a blank, all-fragment slide. */
  function render() {
    slides.forEach((s, i) => {
      s.classList.toggle("current", i === idx);
      s.classList.toggle("prev", i < idx);
    });
    progress.style.width = (slides.length <= 1 ? 100 : (idx / (slides.length - 1)) * 100) + "%";
    document.getElementById("counter").textContent = (idx) + " / " + (slides.length - 1);
    location.hash = idx ? "#" + idx : "";
    slides[idx].scrollTop = 0;
  }

  function go(i) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    if (i === idx) return;
    idx = i; render();
    showAllFrags(slides[idx]);   // jumps land fully revealed
  }

  function next() {
    const cur = slides[idx];
    const fr = frags(cur);
    const shown = shownFrags(cur);
    if (shown < fr.length) { fr[shown].classList.add("in"); return; }
    if (idx < slides.length - 1) { idx++; render(); hideAllFrags(slides[idx]); }
  }
  function prev() {
    const cur = slides[idx];
    const shown = shownFrags(cur);
    if (shown > 0) { frags(cur)[shown - 1].classList.remove("in"); return; }
    if (idx > 0) { idx--; render(); showAllFrags(slides[idx]); }
  }

  /* ---------- depth toggle ---------- */
  let depthOn = false;
  function setDepth(on) {
    depthOn = on;
    document.body.classList.toggle("depth-tech", on);
    document.querySelectorAll("aside.underhood").forEach(n => n.classList.toggle("open", on));
    document.getElementById("depth").classList.toggle("active", on);
  }

  /* ---------- overview ---------- */
  let ovOn = false;
  function toggleOverview(force) {
    ovOn = (force === undefined) ? !ovOn : force;
    document.body.classList.toggle("overview", ovOn);
  }

  /* ---------- events ---------- */
  document.getElementById("next").addEventListener("click", next);
  document.getElementById("prev").addEventListener("click", prev);
  document.getElementById("depth").addEventListener("click", () => setDepth(!depthOn));
  document.getElementById("overview").addEventListener("click", () => toggleOverview());
  document.getElementById("helpbtn").addEventListener("click", () => help.classList.toggle("show"));
  document.getElementById("fsbtn").addEventListener("click", toggleFs);
  document.addEventListener("fullscreenchange", () => {
    const b = document.getElementById("fsbtn");
    const on = !!document.fullscreenElement;
    b.classList.toggle("active", on);
    b.querySelector("span").textContent = on ? "Exit full" : "Fullscreen";
    b.title = on ? "Exit fullscreen (f)" : "Fullscreen (f)";
  });

  document.addEventListener("keydown", (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    switch (e.key) {
      case "ArrowRight": case " ": case "PageDown": e.preventDefault(); next(); break;
      case "ArrowLeft": case "PageUp": e.preventDefault(); prev(); break;
      case "ArrowDown": e.preventDefault(); go(idx + 1); break;
      case "ArrowUp": e.preventDefault(); go(idx - 1); break;
      case "Home": go(0); break;
      case "End": go(slides.length - 1); break;
      case "m": case "M": setDepth(!depthOn); break;
      case "o": case "O": toggleOverview(); break;
      case "f": case "F": toggleFs(); break;
      case "?": help.classList.toggle("show"); break;
      case "Escape": toggleOverview(false); help.classList.remove("show"); break;
    }
  });

  // swipe (touch)
  let tx = 0;
  deck.addEventListener("touchstart", e => tx = e.touches[0].clientX, { passive: true });
  deck.addEventListener("touchend", e => {
    const dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 50) (dx < 0 ? next() : prev());
  }, { passive: true });

  function toggleFs() {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
    else document.exitFullscreen?.();
  }

  /* ---------- KaTeX ---------- */
  function typeset() {
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "\\[", right: "\\]", display: true },
          { left: "$", right: "$", display: false },
          { left: "\\(", right: "\\)", display: false },
        ],
        throwOnError: false,
        macros: { "\\R": "\\mathbb{R}", "\\E": "\\mathbb{E}", "\\1": "\\mathbb{1}" },
      });
    }
  }

  /* ---------- init ---------- */
  function init() {
    const h = parseInt(location.hash.replace("#", ""), 10);
    if (!isNaN(h) && h >= 0 && h < slides.length) idx = h;
    render();
    if (idx > 0) showAllFrags(slides[idx]);   // deep-link lands fully revealed
    typeset();
  }
  if (window.renderMathInElement) init();
  else window.addEventListener("load", init);
})();
