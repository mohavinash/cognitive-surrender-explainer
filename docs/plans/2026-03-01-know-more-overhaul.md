# Know More System Overhaul — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix all Know More panel issues: height/overlap bugs, math rendering, paper excerpt relevance, and deliberate placement based on principled criteria.

**Architecture:** Single-file HTML edits — CSS fixes, new math styling classes, HTML panel additions/removals, regenerated PDF screenshots, and updated JavaScript. All changes in `index.html` plus new screenshot images in `pdf-highlights/`.

**Tech Stack:** Vanilla CSS (grid-row animation), HTML entities + CSS for math, Python (PyMuPDF/fitz) for PDF screenshot extraction.

---

## Phase 1: Universal CSS Fixes (height, overlap, math styling)

### Task 1: Fix Know More height/overlap bug

**Files:**
- Modify: `index.html:1833-1835` (`.know-more` CSS rule)

**Step 1: Read current CSS to confirm the bug**

Current code at line 1833:
```css
.know-more {
  margin-top: var(--space-xs);
  margin-bottom: calc(-1 * var(--space-sm));
}
```

The `margin-bottom: calc(-1 * var(--space-sm))` creates a negative margin that causes expanded panels to overlap content below them.

**Step 2: Fix the negative margin**

Replace with:
```css
.know-more {
  margin-top: var(--space-sm);
  margin-bottom: var(--space-sm);
}
```

**Step 3: Verify in browser**

Open `index.html` in browser. Expand each Know More panel and confirm:
- Content below pushes down smoothly
- No overlap with sibling elements
- Animation still works (grid-template-rows transition)
- Closing the panel causes content to collapse back

**Step 4: Commit**

```bash
git add index.html
git commit -m "fix: remove negative margin on Know More panels causing overlap"
```

---

### Task 2: Add math styling CSS classes

**Files:**
- Modify: `index.html` — insert new CSS rules before the closing `</style>` tag (before line 1960)

**Step 1: Add math styling rules**

Insert before `.know-more-paper-img` rule (line 1953):

```css
/* Math expression styling for technical tabs */
.know-more-panel .math {
  font-family: 'Times New Roman', 'Georgia', serif;
  font-style: italic;
  letter-spacing: 0.02em;
}
.know-more-panel .math var,
.know-more-panel .math .var {
  font-style: italic;
  font-family: 'Times New Roman', 'Georgia', serif;
}
.know-more-panel .math .num {
  font-style: normal;
}
.know-more-panel .math sub,
.know-more-panel .math sup {
  font-size: 0.75em;
  line-height: 0;
}
.know-more-panel .math-block {
  display: block;
  text-align: center;
  margin: var(--space-sm) 0;
  font-family: 'Times New Roman', 'Georgia', serif;
  font-style: italic;
  font-size: 0.95rem;
  color: var(--text-primary);
  padding: var(--space-sm) var(--space-md);
  background: rgba(218, 165, 32, 0.04);
  border-radius: var(--radius-sm);
}
.know-more-panel .math-block .num {
  font-style: normal;
}
```

**Step 2: Verify CSS loads without errors**

Open browser DevTools, confirm no CSS parse errors. Check that `.math` and `.math-block` classes are available.

**Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add math styling CSS classes for Know More technical tabs"
```

---

## Phase 2: Update Technical Tabs with Proper Math Rendering

### Task 3: Update all existing technical tab content with math markup

**Files:**
- Modify: `index.html` — technical panel content for each of the 8 remaining Know More panels

For each technical tab, wrap statistical expressions in `<span class="math">` and use `<var>` for variables. Key patterns to apply:

- `β = −0.86` → `<span class="math"><var>β</var> = <span class="num">−0.86</span></span>`
- `p < 2.20 × 10⁻¹⁶` → `<span class="math"><var>p</var> &lt; <span class="num">2.20 × 10<sup>−16</sup></span></span>`
- `OR = 16.07` → `<span class="math"><var>OR</var> = <span class="num">16.07</span></span>`
- `Cohen's h = 0.81` → `<span class="math">Cohen's <var>h</var> = <span class="num">0.81</span></span>`
- `95% CI [11.50, 22.46]` → `<span class="math"><span class="num">95%</span> <var>CI</var> [<span class="num">11.50, 22.46</span>]</span>`

**Apply to these panels (one by one, verifying each):**
1. `km-trisystem-technical` (line 2469) — mostly prose, minimal math
2. `km-surrender-technical` (line 2501) — surrender rates (57.7%–87.9%)
3. `km-followrate-technical` (line 2558) — follow rates, Cohen's h, p-values
4. `km-accuracy-technical` (line 2591) — accuracy percentages, scissors gap, Cohen's h
5. `km-individual-technical` (line 2682) — OR values for Trust, NFC, Fluid IQ
6. `km-timepressure-technical` (line 2778) — β, p-values, OR, Cohen's h
7. `km-incentives-technical` (line 2896) — β, OR, CI, override rates
8. `km-synthesis-technical` (line 2983) — OR = 16.07, per-study h values, Hedges' g

**Step 1: Update each panel's technical content**

Work through each panel, wrapping math expressions.

**Step 2: Verify in browser**

Open each Know More → Technical tab and confirm:
- Variables (β, p, h, OR, CI) appear in italic serif
- Numbers appear in normal (upright) style
- Superscripts (exponents like 10⁻¹⁶) render correctly
- Overall readability is improved vs. plain text

**Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add proper math rendering to all Know More technical tabs"
```

---

## Phase 3: Remove Redundant Know More Panels

### Task 4: Remove km-scissors, km-implications, km-vulnerability

**Files:**
- Modify: `index.html`
  - Remove lines 3067-3091 (`km-scissors`)
  - Remove lines 3193-3217 (`km-implications`)
  - Remove lines 3288-3312 (`km-vulnerability`)

**Step 1: Remove km-scissors (lines 3067-3091)**

This panel is redundant with km-synthesis. The dose-response chart already explains the scissors effect visually.

**Step 2: Remove km-implications (lines 3193-3217)**

The implications section is design recommendations, not empirical findings. The explainer text already covers them adequately.

**Step 3: Remove km-vulnerability (lines 3288-3312)**

This overlaps with km-individual (same Trust/NFC/Fluid IQ moderators). The vulnerability profile section in the explainer is already clear.

**Step 4: Verify removal doesn't break JavaScript**

Open browser console, expand/close remaining Know More panels, confirm no JS errors. The KnowMore.open() and KnowMore.toggle() functions use getElementById which gracefully returns null for missing elements.

**Step 5: Commit**

```bash
git add index.html
git commit -m "refactor: remove 3 redundant Know More panels (scissors, implications, vulnerability)"
```

---

## Phase 4: Add Missing Critical Know More Panels

### Task 5: Add km-cognitiveRoutes panel after Cognitive Routes section

**Files:**
- Modify: `index.html` — insert after the cognitive routes section (after line ~2410)

The Cognitive Routes section (Table 2 equivalent) presents the 6 canonical pathways through the triadic system. This is a foundational concept that deserves a Know More panel.

**Step 1: Insert the Know More panel HTML**

Insert after the cognitive routes cards container (after the route-description div, around line 2410):

```html
<div id="km-cognitiveRoutes" class="know-more reveal">
  <button class="know-more-trigger" onclick="KnowMore.open('cognitiveRoutes')">Know more <span class="km-arrow">+</span></button>
  <div class="know-more-body"><div class="know-more-body-inner"><div class="know-more-card">
    <div class="know-more-tabs">
    <button class="know-more-tab" data-tier="simple" onclick="KnowMore.toggle('cognitiveRoutes','simple')">Plain English</button>
    <button class="know-more-tab" data-tier="technical" onclick="KnowMore.toggle('cognitiveRoutes','technical')">Technical</button>
    <button class="know-more-tab" data-tier="paper" onclick="KnowMore.toggle('cognitiveRoutes','paper')">From the Paper</button>
  </div>
  <div id="km-cognitiveRoutes-simple" class="know-more-panel">
    <div class="know-more-panel-inner">
    <p>Think of these six routes as the different paths your mind can take when solving a problem. <strong>Intuition</strong> is your gut reaction — no AI involved. <strong>Deliberation</strong> is when you slow down and think carefully — also no AI. <strong>Cognitive offloading</strong> is the healthy version of using AI: you ask it for help but you still check the answer with your own reasoning. <strong>Cognitive surrender</strong> is when you skip that checking step and just go with whatever the AI says. <strong>Autopilot</strong> is the extreme — you don't even think before handing the question to AI. The paper's key finding is that most AI users follow the surrender path, not the offloading path.</p>
    </div>
  </div>
  <div id="km-cognitiveRoutes-technical" class="know-more-panel">
    <div class="know-more-panel-inner">
    <p>Table 2 (p. 16) formalises six canonical routes through the triadic cognitive system. The critical distinction is the <em>cognitive locus</em> — which system ultimately governs the response. In cognitive offloading (locus: System 2), the user delegates to System 3 but retains evaluative oversight: <span class="math">Stimulus → S1/S2 → S3 (assist) → S2 → Response</span>. In cognitive surrender (locus: System 3), System 2 is bypassed: <span class="math">Stimulus → S1 (brief) → S3 → Response</span>. Empirically, on chat-engaged faulty trials across all three studies, <span class="math"><span class="num">73.2%</span></span> of responses reflected surrender vs. <span class="math"><span class="num">19.7%</span></span> offloading — a nearly 4:1 ratio favouring the path of least cognitive resistance.</p>
    </div>
  </div>
  <div id="km-cognitiveRoutes-paper" class="know-more-panel">
    <div class="know-more-panel-inner">
    <img src="pdf-highlights/km_cognitiveRoutes.png" alt="Paper excerpt: Table 2 — Canonical routes of cognition under Tri-System Theory (Shaw &amp; Nave, 2025, p. 16)" class="know-more-paper-img" loading="lazy">
      <span class="snippet-ref">&mdash; Shaw &amp; Nave, 2025, Table 2 (p. 16)</span>
  </div>
  </div></div></div>
</div>
```

**Step 2: Generate PDF screenshot**

Use Python to extract page 16 from the PDF (Table 2 — "Canonical routes of cognition under Tri-System Theory"):

```python
import fitz
doc = fitz.open("ssrn-6097646.pdf")
page = doc[15]  # page 16, 0-indexed
clip = fitz.Rect(50, 40, 560, 520)  # Table 2 area
pix = page.get_pixmap(clip=clip, dpi=200)
pix.save("pdf-highlights/km_cognitiveRoutes.png")
```

Adjust clip coordinates to capture Table 2 cleanly.

**Step 3: Verify panel renders correctly**

Open browser, navigate to Cognitive Routes section, click "Know more", verify all 3 tabs work.

**Step 4: Commit**

```bash
git add index.html pdf-highlights/km_cognitiveRoutes.png
git commit -m "feat: add Know More panel for Cognitive Routes (Table 2)"
```

---

### Task 6: Add km-confidence panel after confidence inflation callout

**Files:**
- Modify: `index.html` — insert after the confidence inflation callout (after line ~2631)

The confidence inflation finding is one of the paper's most striking results: AI makes people more confident even when 50% of AI answers are wrong. Currently has no Know More panel.

**Step 1: Insert the Know More panel HTML**

Insert after the confidence inflation callout div (after line ~2631):

```html
<div id="km-confidence" class="know-more reveal">
  <button class="know-more-trigger" onclick="KnowMore.open('confidence')">Know more <span class="km-arrow">+</span></button>
  <div class="know-more-body"><div class="know-more-body-inner"><div class="know-more-card">
    <div class="know-more-tabs">
    <button class="know-more-tab" data-tier="simple" onclick="KnowMore.toggle('confidence','simple')">Plain English</button>
    <button class="know-more-tab" data-tier="technical" onclick="KnowMore.toggle('confidence','technical')">Technical</button>
    <button class="know-more-tab" data-tier="paper" onclick="KnowMore.toggle('confidence','paper')">From the Paper</button>
  </div>
  <div id="km-confidence-simple" class="know-more-panel">
    <div class="know-more-panel-inner">
    <p>Here's what's perhaps most unsettling: using AI didn't just change people's answers — it changed how <em>sure</em> they felt. Participants who used the AI chatbot rated their confidence at 77 out of 100, compared to 65 for those working alone. That 12-point boost sounds reasonable — except that roughly half the AI's answers were deliberately wrong. People felt smarter and more confident while their actual performance was being dragged down by faulty AI. Even more troubling: confidence didn't drop as people encountered more wrong answers. Their brains didn't recalibrate. The mere act of consulting AI — regardless of its accuracy — made them feel like they knew what they were doing.</p>
    </div>
  </div>
  <div id="km-confidence-technical" class="know-more-panel">
    <div class="know-more-panel-inner">
    <p>Study 1: Global confidence was significantly higher in AI-Assisted (<span class="math"><var>M</var> = <span class="num">77.0%</span></span>, <span class="math"><var>SE</var> = <span class="num">1.30%</span></span>, <span class="math"><span class="num">95%</span> <var>CI</var> [<span class="num">74.4, 79.6</span>]</span>) than Brain-Only (<span class="math"><var>M</var> = <span class="num">65.3%</span></span>, <span class="math"><var>SE</var> = <span class="num">2.21%</span></span>, <span class="math"><span class="num">95%</span> <var>CI</var> [<span class="num">61.0, 69.6</span>]</span>); <span class="math"><var>t</var>(<span class="num">202.91</span>) = <span class="num">4.57</span></span>, <span class="math"><var>p</var> = <span class="num">8.55 × 10<sup>−6</sup></span></span>; <span class="math">Hedges' <var>g</var> = <span class="num">0.54</span></span>, <span class="math"><span class="num">95%</span> <var>CI</var> [<span class="num">0.32, 0.77</span>]</span> — a medium effect. Critically, within the AI-Assisted condition, confidence did not significantly decline as the number of faulty trials increased (<span class="math"><var>β</var> = <span class="num">−1.14</span></span>, <span class="math"><var>SE</var> = <span class="num">0.89</span></span>, <span class="math"><var>t</var> = <span class="num">−1.28</span></span>, <span class="math"><span class="num">95%</span> <var>CI</var> [<span class="num">−2.88, 0.61</span>]</span>, <span class="math"><var>p</var> = <span class="num">0.202</span></span>). Study 3 per-item data confirmed: AI-assisted trial confidence (<span class="math"><var>M</var> = <span class="num">82.2%</span></span>) exceeded brain-only (<span class="math"><var>M</var> = <span class="num">77.5%</span></span>) regardless of AI accuracy (<span class="math"><var>p</var> = <span class="num">6.86 × 10<sup>−7</sup></span></span>).</p>
    </div>
  </div>
  <div id="km-confidence-paper" class="know-more-panel">
    <div class="know-more-panel-inner">
    <img src="pdf-highlights/km_confidence.png" alt="Paper excerpt: Confidence inflation despite faulty AI (Shaw &amp; Nave, 2025, p. 25)" class="know-more-paper-img" loading="lazy">
      <span class="snippet-ref">&mdash; Shaw &amp; Nave, 2025 (p. 25)</span>
  </div>
  </div></div></div>
</div>
```

**Step 2: Generate PDF screenshot**

Use Python to extract the confidence results paragraph from page 25:

```python
import fitz
doc = fitz.open("ssrn-6097646.pdf")
page = doc[24]  # page 25, 0-indexed
clip = fitz.Rect(50, 40, 560, 290)  # Confidence section
pix = page.get_pixmap(clip=clip, dpi=200)
pix.save("pdf-highlights/km_confidence.png")
```

Adjust clip coordinates to capture the "Confidence" paragraph cleanly.

**Step 3: Verify panel renders correctly**

Open browser, navigate to Study 1 section, find confidence inflation callout, click "Know more", verify all 3 tabs work.

**Step 4: Commit**

```bash
git add index.html pdf-highlights/km_confidence.png
git commit -m "feat: add Know More panel for confidence inflation finding"
```

---

## Phase 5: Regenerate All "From the Paper" Screenshots

### Task 7: Generate correct PDF screenshots for all 10 Know More panels

**Files:**
- Create/replace: `pdf-highlights/km_*.png` (10 files)

**Screenshot generation script** (`generate_km_screenshots.py`):

```python
import fitz

doc = fitz.open("ssrn-6097646.pdf")

# Define clips: (page_0indexed, rect, output_filename)
# Rects need to be tuned per page to capture the right content
clips = [
    # km-trisystem: Table 1 + "Reframing" paragraph (p.12-13)
    (12, fitz.Rect(50, 35, 560, 560), "pdf-highlights/km_trisystem.png"),

    # km-surrender: "We define cognitive surrender as..." (p.17)
    (16, fitz.Rect(50, 40, 560, 350), "pdf-highlights/km_surrender.png"),

    # km-cognitiveRoutes: Table 2 (p.16)
    (15, fitz.Rect(50, 40, 560, 520), "pdf-highlights/km_cognitiveRoutes.png"),

    # km-followrate: Figure 2 + "Chat Use & AI Adoption" (p.23)
    (22, fitz.Rect(50, 35, 560, 560), "pdf-highlights/km_followrate.png"),

    # km-accuracy: Figure 3 (p.24)
    (23, fitz.Rect(50, 35, 560, 510), "pdf-highlights/km_accuracy.png"),

    # km-confidence: "Confidence" paragraph (p.25)
    (24, fitz.Rect(50, 40, 560, 290), "pdf-highlights/km_confidence.png"),

    # km-individual: Figure 4 (p.26)
    (25, fitz.Rect(50, 35, 560, 480), "pdf-highlights/km_individual.png"),

    # km-timepressure: Figure 5 (p.31)
    (30, fitz.Rect(50, 35, 560, 560), "pdf-highlights/km_timepressure.png"),

    # km-incentives: Figure 7 (p.37)
    (36, fitz.Rect(50, 35, 560, 560), "pdf-highlights/km_incentives.png"),

    # km-synthesis: "Cognitive Surrender Effect Size" + Figure 10 (p.42-43)
    (42, fitz.Rect(50, 35, 560, 560), "pdf-highlights/km_synthesis.png"),
]

for page_idx, rect, output_path in clips:
    page = doc[page_idx]
    pix = page.get_pixmap(clip=rect, dpi=200)
    pix.save(output_path)
    print(f"Saved: {output_path} (page {page_idx + 1})")

doc.close()
```

**Step 1: Run the screenshot generation script**

```bash
python generate_km_screenshots.py
```

**Step 2: Visually verify each screenshot**

Open each generated PNG and confirm it captures the correct content:
- `km_trisystem.png` → Table 1 (Cognitive affordances and tradeoffs)
- `km_surrender.png` → Cognitive surrender definition paragraph
- `km_cognitiveRoutes.png` → Table 2 (Canonical routes of cognition)
- `km_followrate.png` → Figure 2 (Follow/Override rates chart)
- `km_accuracy.png` → Figure 3 (Accuracy by condition chart)
- `km_confidence.png` → Confidence results paragraph
- `km_individual.png` → Figure 4 (Individual differences chart)
- `km_timepressure.png` → Figure 5 (Time pressure accuracy chart)
- `km_incentives.png` → Figure 7 (Incentives follow/override chart)
- `km_synthesis.png` → Figure 10 (Dose-response curves)

**Step 3: Adjust clip rectangles if any screenshot is off**

Re-run script with adjusted coordinates for any misaligned captures.

**Step 4: Update page references in HTML**

Verify each `<span class="snippet-ref">` matches the actual page shown in the screenshot:
- km-trisystem: p. 13
- km-surrender: p. 17
- km-cognitiveRoutes: p. 16
- km-followrate: p. 23
- km-accuracy: p. 24
- km-confidence: p. 25
- km-individual: p. 26
- km-timepressure: p. 31
- km-incentives: p. 37
- km-synthesis: p. 43

**Step 5: Commit**

```bash
git add pdf-highlights/km_*.png index.html
git commit -m "fix: regenerate all Know More paper screenshots from correct pages"
```

---

## Phase 6: Final Verification

### Task 8: End-to-end verification of all 10 Know More panels

**Step 1: Open index.html in browser**

**Step 2: For each Know More panel, verify:**

| Check | What to look for |
|-------|-----------------|
| Opens/closes smoothly | Grid-row animation works, no jump |
| No overlap | Content below pushes down when open |
| Plain English tab | Clear, jargon-free explanation |
| Technical tab | Math variables in italic serif, numbers upright, exponents render |
| From the Paper tab | Screenshot shows correct page, reference matches |
| Tab switching | All 3 tabs activate correctly, deactivate others |

**Step 3: Verify removed panels are gone**

Ctrl+F for "km-scissors", "km-implications", "km-vulnerability" — should not appear in HTML.

**Step 4: Verify no JavaScript errors**

Open browser console, navigate through entire page, expand/close all panels. No errors should appear.

**Step 5: Mobile responsive check**

Resize browser to 420px width. Know More panels should:
- Tabs wrap correctly
- Text remains readable
- Screenshots scale properly

**Step 6: Final commit**

```bash
git add -A
git commit -m "chore: final verification pass for Know More overhaul"
```

---

## Summary of Changes

| Action | Panel | Rationale |
|--------|-------|-----------|
| FIX | All panels | Remove negative margin causing overlap |
| FIX | All technical tabs | Add proper math rendering |
| KEEP | km-trisystem | Core theoretical claim |
| KEEP | km-surrender | Core theoretical claim |
| ADD | km-cognitiveRoutes | Core theoretical claim (Table 2) |
| KEEP | km-followrate | Key empirical finding |
| KEEP | km-accuracy | Key empirical finding + counterintuitive |
| ADD | km-confidence | Key empirical finding + counterintuitive |
| KEEP | km-individual | Key empirical finding + statistical depth |
| KEEP | km-timepressure | Key empirical finding + counterintuitive |
| KEEP | km-incentives | Key empirical finding + counterintuitive |
| KEEP | km-synthesis | Key empirical finding + statistical depth |
| REMOVE | km-scissors | Redundant with synthesis + visual chart |
| REMOVE | km-implications | Not empirical findings, already in explainer |
| REMOVE | km-vulnerability | Overlaps with individual differences |
| REGEN | All "From Paper" screenshots | Correct pages with verified references |

**Final count: 10 Know More panels (was 11, removed 3, added 2)**
