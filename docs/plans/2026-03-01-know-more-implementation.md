# 3-Tier Know More System — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add 11 expandable "Know More" panels with 3 depth tiers (Plain English, Technical, From the Paper) to key content blocks, plus fix ~11 base text instances of assumed jargon.

**Architecture:** Static HTML approach — all 3 tiers are hidden `<div>`s below each target block, toggled by a single JS function. Reuses existing `.toggle-btn` styling. No new dependencies.

**Tech Stack:** Vanilla HTML/CSS/JS in a single-file page (`index.html`). No build tools.

**File:** `/Users/avinash/AICodeLab/Explainers/AI and Congnition Paper/index.html`

---

## Phase 1: Infrastructure (CSS + JS)

### Task 1: Add Know More CSS classes

**Files:**
- Modify: `index.html` — insert before `</style>` (line ~1821)

**Step 1: Add CSS rules**

Insert these rules before the closing `</style>` tag, after the existing `.crt-condition-banner` rules:

```css
/* ============================================================
   KNOW MORE PANELS
   ============================================================ */
.know-more {
  margin-top: var(--space-md);
  border-top: 1px solid var(--border-light);
  padding-top: var(--space-sm);
}
.know-more-label {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  margin-bottom: var(--space-xs);
}
.know-more-tabs {
  display: inline-flex;
  gap: 0;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 3px;
  margin-bottom: 0;
}
.know-more-tab {
  padding: 0.35rem 0.85rem;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.03em;
  border: none;
  border-radius: calc(var(--radius-md) - 2px);
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  transition: all var(--transition-fast);
}
.know-more-tab:hover {
  color: var(--text-primary);
  background: rgba(255,255,255,0.05);
}
.know-more-tab.active {
  background: var(--accent);
  color: #fff;
}
.know-more-panel {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  transition: max-height 0.4s ease-out, opacity 0.3s ease-out, margin-top 0.3s ease-out;
  margin-top: 0;
}
.know-more-panel.active {
  max-height: 800px;
  opacity: 1;
  margin-top: var(--space-md);
}
.know-more-panel p {
  font-size: 0.88rem;
  line-height: 1.75;
  color: var(--text-secondary);
  max-width: 700px;
}
.know-more-snippet {
  border-left: 3px solid var(--accent);
  padding: 0.8rem 1.2rem;
  background: rgba(218, 165, 32, 0.04);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  font-style: italic;
  font-size: 0.88rem;
  line-height: 1.75;
  color: var(--text-secondary);
  max-width: 700px;
}
.know-more-snippet .snippet-ref {
  display: block;
  margin-top: var(--space-sm);
  font-style: normal;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--text-muted);
}
```

**Step 2: Verify**

Open page in browser, confirm no CSS errors. Know More styles won't be visible yet (no HTML using them).

**Step 3: Commit**

```
git add index.html
git commit -m "style: add Know More panel CSS classes"
```

---

### Task 2: Add Know More JS toggle function

**Files:**
- Modify: `index.html` — insert in the `<script>` block, after the reveal/scroll animation code (~line 3027)

**Step 1: Add the toggle function**

Insert after the scroll-reveal IntersectionObserver code (around line 3027), before the CRT IIFE:

```javascript
/* ============================================================
   KNOW MORE — 3-tier expandable panels
   ============================================================ */
window.KnowMore = {
  toggle: function (id, tier) {
    var container = document.getElementById('km-' + id);
    if (!container) return;
    var tabs = container.querySelectorAll('.know-more-tab');
    var panels = container.querySelectorAll('.know-more-panel');
    var clickedTab = container.querySelector('[data-tier="' + tier + '"]');
    var clickedPanel = document.getElementById('km-' + id + '-' + tier);
    if (!clickedTab || !clickedPanel) return;

    var wasActive = clickedTab.classList.contains('active');

    // Deactivate all
    for (var i = 0; i < tabs.length; i++) tabs[i].classList.remove('active');
    for (var i = 0; i < panels.length; i++) panels[i].classList.remove('active');

    // If clicking a different tab, activate it
    if (!wasActive) {
      clickedTab.classList.add('active');
      clickedPanel.classList.add('active');
    }
  }
};
```

**Step 2: Verify**

Open page, run `KnowMore.toggle` in console — should not error.

**Step 3: Commit**

```
git add index.html
git commit -m "feat: add Know More JS toggle function"
```

---

## Phase 2: Know More Panels (11 blocks)

Each task adds the HTML for one Know More panel below its target block. The pattern is identical each time — a `<div id="km-{id}" class="know-more">` containing the label, 3 tabs, and 3 panels.

### Task 3: Know More — Tri-System Diagram (Theory)

**Files:**
- Modify: `index.html` — insert after the system comparison table closing `</div>` (~line 2312), before the pull quote

**Step 1: Add HTML**

```html
<div id="km-trisystem" class="know-more reveal">
  <div class="know-more-label">Know More</div>
  <div class="know-more-tabs">
    <button class="know-more-tab" data-tier="simple" onclick="KnowMore.toggle('trisystem','simple')">Plain English</button>
    <button class="know-more-tab" data-tier="technical" onclick="KnowMore.toggle('trisystem','technical')">Technical</button>
    <button class="know-more-tab" data-tier="paper" onclick="KnowMore.toggle('trisystem','paper')">From the Paper</button>
  </div>
  <div id="km-trisystem-simple" class="know-more-panel">
    <p>Psychologists have long described two ways humans think. <strong>System 1</strong> is fast and automatic — it's the gut reaction that makes you flinch at a loud noise or blurt out "10 cents" to a trick math question. <strong>System 2</strong> is slow and effortful — it's what you engage when you stop, re-read the question, and work through the algebra. This framework, developed by Daniel Kahneman (who won a Nobel Prize for it), has shaped decades of research on decision-making.</p>
    <p>Shaw &amp; Nave's contribution is arguing that AI has become a <strong>third system</strong> — not a tool like a calculator, but something you think <em>with</em>, the way you think with your own intuition. The critical question their paper investigates: when you consult AI, do you actually evaluate its answer with System 2, or do you just accept it and move on?</p>
  </div>
  <div id="km-trisystem-technical" class="know-more-panel">
    <p>The paper extends Kahneman's (2011) dual-process framework by introducing System 3 as a formally distinct cognitive system with four defining properties: (1) <strong>External</strong> — resides outside the biological nervous system; (2) <strong>Automated</strong> — executes via statistical/algorithmic processes; (3) <strong>Data-driven</strong> — based on large-scale training corpora; (4) <strong>Dynamic</strong> — responds to human and environmental inputs in real-time. Table 1 (p. 10) compares System 3 against Systems 1 and 2 across eight dimensions: origin, speed, effort, accuracy, affect, ethics, justification, and locus. The authors propose six canonical cognitive routes (Table 2, p. 14) including <em>cognitive offloading</em> (S1/S2 → S3 → S2 → Response) and <em>cognitive surrender</em> (S1 brief → S3 → Response), where the key distinction is whether System 2 evaluates System 3's output.</p>
  </div>
  <div id="km-trisystem-paper" class="know-more-panel">
    <div class="know-more-snippet">
      "System 3 is not merely a tool that supports cognition but an active participant in cognitive processes… it functions not just as a tool or extension but as a co-agent in reasoning, often delivering outputs with epistemic authority."
      <span class="snippet-ref">— Shaw &amp; Nave, 2025 (pp. 8–9)</span>
    </div>
  </div>
</div>
```

**Step 2: Verify in browser** — tabs appear, all 3 tiers toggle correctly, collapse on re-click.

**Step 3: Commit**

```
git add index.html
git commit -m "feat: add Know More panel for Tri-System diagram"
```

---

### Task 4: Know More — Cognitive Surrender Quote (Theory)

**Files:**
- Modify: `index.html` — insert after the existing pull quote div (~line 2318)

**Content:**

- **Plain English:** Cognitive surrender is what happens when you stop thinking for yourself and just go with whatever the AI says — not because you evaluated its answer and found it convincing, but because you didn't evaluate it at all. It's the difference between using a GPS while still paying attention to where you're going versus blindly following turn-by-turn directions into a lake. The paper found this isn't rare or irrational — it's the default behaviour for most people most of the time when AI is available.
- **Technical:** The authors define cognitive surrender as distinct from cognitive offloading (Risko & Gilbert, 2016) along two axes: (1) the presence/absence of System 2 evaluation of System 3 output, and (2) the retention/abdication of metacognitive monitoring. Operationally, surrender is measured as following AI-Faulty advice — accepting an incorrect AI suggestion without override. Across three studies, surrender rates on chat-engaged faulty trials ranged from 57.7% (Study 3, Incentives+Feedback) to 87.9% (Study 2, Time Pressure). Manifestation indicators include low override rates, shorter justification text, and inflated confidence.
- **Paper snippet:** "In cases of cognitive surrender, the user does not just follow System 3: they stop deliberative thinking altogether… cognitive surrender represents a deeper abdication of critical evaluation, where the user relinquishes cognitive control and adopts the AI's judgment as their own." — Shaw & Nave, 2025 (pp. 14–15)

**Step: Add HTML, verify, commit.**

```
git commit -m "feat: add Know More panel for cognitive surrender definition"
```

---

### Task 5: Know More — 79.8% Key Stat (Study 1)

**Files:**
- Modify: `index.html` — insert after the 79.8% `.study-key-finding` div (~line 2349)

**Content:**

- **Plain English:** In this experiment, people answered 7 reasoning puzzles — classic brain teasers designed to have a tempting wrong answer. Some participants could ask an AI chatbot for help. What the participants didn't know: the AI was rigged. On some questions it gave the correct answer; on others, it confidently gave the wrong one. The result: nearly 4 out of 5 times someone asked the AI and got a wrong answer, they submitted that wrong answer anyway. They didn't just get it wrong — they performed worse than people who had no AI at all.
- **Technical:** N = 238 AI-Assisted participants answered 7 CRT (Cognitive Reflection Test) items. AI accuracy was manipulated within-subjects via hidden seed prompts: 4 items received accurate AI responses, 3 received faulty (confidently incorrect) responses. On chat-engaged faulty trials, 79.8% of responses followed the AI's incorrect suggestion. Follow rate on accurate trials was 92.7%. The AI-Accurate vs. AI-Faulty accuracy contrast was −39.5 percentage points (Cohen's h = 0.81, p < 2.20 × 10⁻¹⁶). Chat engagement was similar across trial types (54.4% accurate, 52.8% faulty), suggesting participants did not selectively avoid faulty items.
- **Paper snippet:** "participants achieved higher accuracy when System 3 is correct and succumb to lower accuracy when System 3 is faulty, illustrating cognitive surrender." — Shaw & Nave, 2025 (p. 20)

**Step: Add HTML, verify, commit.**

```
git commit -m "feat: add Know More panel for Study 1 key stat"
```

---

### Task 6: Know More — Accuracy Chart (Study 1)

**Files:**
- Modify: `index.html` — insert after the `#chart-s1-accuracy` SVG container and its caption (~line 2358)

**Content:**

- **Plain English:** This chart shows three bars. The gold bar (45.8%) is how people scored without any AI — just their own thinking. The blue bar (71%) is how they scored when the AI gave them the right answer — a big boost. The red bar (31.5%) is how they scored when the AI gave them a wrong answer — worse than having no AI at all. That last bar is the key finding. AI didn't just fail to help; it actively dragged performance below what people would have achieved on their own. The researchers call the gap between the blue and red bars the "scissors effect" — the more you rely on AI, the more your fate depends on whether the AI happens to be right.
- **Technical:** CRT accuracy by trial type (Study 1, N = 359): Brain-Only M = 45.8%; AI-Accurate M = 71.0% (+25.2pp, p < .001); AI-Faulty M = 31.5% (−14.3pp vs. Brain-Only, p < .001). The scissors gap (AI-Accurate minus AI-Faulty) = 39.5pp (Cohen's h = 0.83). Error bars show 95% CIs. Brain-Only baseline includes n = 121 participants with no AI access plus probe trials from AI-Assisted participants. The accuracy boost from accurate AI (+25.2pp) is nearly twice the accuracy cost of faulty AI (−14.3pp), but the faulty AI result is more consequential because participants don't know which trials are faulty.
- **Paper snippet:** "When AI gave correct suggestions, accuracy soared to 71%. But when AI was wrong, people followed it off a cliff — performing worse than without any AI at all." — Shaw & Nave, 2025 (p. 21)

**Step: Add HTML, verify, commit.**

```
git commit -m "feat: add Know More panel for Study 1 accuracy chart"
```

---

### Task 7: Know More — Individual Differences (Study 1)

**Files:**
- Modify: `index.html` — insert after the `.grid-3col` individual differences cards (~line 2418)

**Content:**

- **Plain English:** Not everyone surrendered equally. The study measured three traits in each participant. <strong>Trust in AI</strong>: people who reported higher trust in AI systems were significantly more likely to follow wrong AI answers — they gave the AI the benefit of the doubt even when it was wrong. <strong>Need for Cognition</strong>: this is a psychological scale measuring how much someone enjoys thinking through hard problems (as opposed to preferring shortcuts). People who scored higher were nearly twice as likely to catch the AI's mistakes. <strong>Fluid intelligence</strong>: this measures raw reasoning ability — the kind tested by pattern-recognition puzzles, not learned knowledge. Higher scores nearly doubled the odds of overriding faulty AI. In short: your willingness to think and your ability to reason both protect you, while blind trust in AI makes you vulnerable.
- **Technical:** Three individual-difference moderators were assessed via validated scales. (1) Trust in AI (Jian et al., 2000): Higher trust predicted more System 3 engagement (OR = 1.24, p = .047) and lower override rates on faulty trials (OR = 0.36, p < .001), meaning 64% less likely to resist faulty AI per SD increase. (2) Need for Cognition (Cacioppo et al., 1984): Reduced System 3 usage (OR = 0.65, p = .003) and increased override (OR = 1.86, p < .001). (3) Fluid Intelligence (ICAR-16 matrix reasoning): Higher scores predicted greater override (OR = 1.96, p < .001). These effects held when controlling for the other two variables in a combined model (Figure 4, p. 22).
- **Paper snippet:** "Trust in AI amplified vulnerability; Need for Cognition and Fluid IQ protected against it… Higher fluid intelligence nearly doubled the odds of resisting faulty AI." — Shaw & Nave, 2025 (pp. 21–22)

**Step: Add HTML, verify, commit.**

```
git commit -m "feat: add Know More panel for individual differences"
```

---

### Task 8: Know More — Study 2 (Time Pressure)

**Files:**
- Modify: `index.html` — insert after the Study 2 effect meter (~line 2488)

**Content:**

- **Plain English:** Study 2 asked: what happens when you're under time pressure? With a 30-second countdown per question, people had less time to think carefully — which is exactly when you'd expect them to lean on AI more. The result was a double-edged sword. When the AI was right, time-pressured participants held up reasonably well (71.3% accuracy). But when the AI was wrong, time-pressured participants hit rock bottom — just 12.1% accuracy, far below anyone else in the study. Time pressure didn't change whether people surrendered; it made the consequences of surrendering more extreme.
- **Technical:** Study 2 (N = 485): 2 × 2 between-subjects (Time Pressure: 30s countdown vs. Control: unlimited) × within-subjects (AI Accuracy). Time pressure reduced accuracy across the board (β = −0.86, p = 1.59 × 10⁻⁸), but critically, no Time Pressure × Trial Type interaction emerged (β = −0.02, p = 0.937). This means cognitive surrender was equally strong under both conditions — time pressure lowered the baseline without differentially affecting the surrender effect. AI-Users under time pressure: AI-Accurate 71.3%, AI-Faulty 12.1% (Cohen's h = 0.86, largest of all 3 studies). Thinking profile analysis: AI-Users showed OR = 40.9 for Trial Type effect (p < 2.20 × 10⁻¹⁶).
- **Paper snippet:** "time pressure reduced performance, suppressed System 2 engagement, and shifted participants toward either System 1 (intuitive) or System 3 (artificial)… the low-friction path to defer to external cognition becomes attractive." — Shaw & Nave, 2025 (pp. 28, 42)

**Step: Add HTML, verify, commit.**

```
git commit -m "feat: add Know More panel for Study 2"
```

---

### Task 9: Know More — Study 3 (Incentives)

**Files:**
- Modify: `index.html` — insert after the Study 3 effect meter (~line 2580)

**Content:**

- **Plain English:** Study 3 tested the obvious fix: what if you pay people to get the right answer and tell them immediately whether they were right or wrong? The results were encouraging but incomplete. Override rates on wrong AI answers more than doubled — from 20% to 42.3%. People were clearly trying harder. But here's the catch: even with money on the line and instant feedback, the majority of participants still followed wrong AI answers more often than not. Financial motivation helped, but it wasn't enough to overcome the pull of cognitive surrender. The problem isn't laziness — it's something more structural about how we interact with confident AI outputs.
- **Technical:** Study 3 (N = 450): Between-subjects Incentives + Feedback (n = 238) vs. Control (n = 212). Incentives: $0.20/correct + $20 lottery. Feedback: item-level correct/incorrect post-response. Key results: Override rates on faulty trials increased from 20.0% to 42.3% (β = 1.44, p = 6.30 × 10⁻⁹, OR = 4.25). Follow rates on accurate trials also increased (87.6% → 92.2%, OR = 1.94), suggesting better calibration overall. However, the AI-Accurate vs. AI-Faulty accuracy gap remained large: 44pp under Incentives+Feedback vs. 50pp under Control. Cohen's h = 0.78 (still "large"). Per-item confidence data showed AI-assisted trial confidence (82.2%) exceeded brain-only trial confidence (77.5%) regardless of AI accuracy.
- **Paper snippet:** "cognitive surrender persists. Participants rewarded for accuracy and given immediate item-level feedback were significantly more accurate, particularly in cases when AI recommendations may have led them astray… the accuracy gap between Trial Types remained large, at ~44 percentage points." — Shaw & Nave, 2025 (pp. 36–37)

**Step: Add HTML, verify, commit.**

```
git commit -m "feat: add Know More panel for Study 3"
```

---

### Task 10: Know More — 16x Effect + Synthesis Cards (Big Picture)

**Files:**
- Modify: `index.html` — insert after the Confidence Inflation / Surrender vs. Offloading cards (~line 2641)

**Content:**

- **Plain English:** Across all three studies — 1,372 people and 9,593 individual trial responses — the pattern held. When the AI was right, people were <strong>16 times more likely</strong> to answer correctly than when the AI was wrong. Not 16% more likely — 16 <em>times</em>. That's a staggering dependency. It means the quality of your thinking has become almost entirely a function of the quality of your AI. The paper also found a troubling side effect: AI access made people more confident in their answers — by nearly 12 percentage points — even though roughly half the AI answers were wrong. People felt smarter while getting worse results.
- **Technical:** Trial-level meta-analytic synthesis across Studies 1–3 (N = 1,372; 9,593 trials): OR for correct responding (AI-Accurate vs. AI-Faulty) = 16.07 (95% CI [11.50, 22.46], p < 2.20 × 10⁻¹⁶). Per-study Cohen's h values: Study 1 = 0.83, Study 2 = 0.86, Study 3 = 0.78; trial-weighted h = 0.82 (all "large" by conventional thresholds). Situational manipulations shifted absolute performance levels but did not eliminate the surrender effect: Time Pressure OR = 14.28, Incentives + Feedback OR = 11.05. Confidence inflation: AI-Assisted M = 77.0% vs. Brain-Only M = 65.3% (Hedges' g = 0.54, a "medium" effect size indicating AI access inflated self-reported confidence by roughly half a standard deviation). Confidence did not decline as faulty trials accumulated (β = −1.14, p = 0.202).
- **Paper snippet:** "Correct responding was over 16 times greater when System 3 was correct… illustrating the promises of superintelligence and exposing a structural vulnerability of cognitive surrender." — Shaw & Nave, 2025 (p. 39)

**Step: Add HTML, verify, commit.**

```
git commit -m "feat: add Know More panel for Big Picture synthesis"
```

---

### Task 11: Know More — Scissors Effect Chart (Big Picture)

**Files:**
- Modify: `index.html` — insert after the dose-response legend/instructions (~line 2712)

**Content:**

- **Plain English:** This interactive chart shows what happens as people rely more on AI. Move the slider from left (0% AI use) to right (100% AI use). The blue line (AI-Accurate) goes up — more AI use means higher accuracy when AI is right. The red line (AI-Faulty) goes down — more AI use means lower accuracy when AI is wrong. They diverge like scissors opening. At zero AI use, everyone performs the same (the brain-only baseline). At 100% AI use, your performance is entirely determined by whether the AI happened to be right. The gap between the lines is the cost of cognitive surrender — and it gets wider the more you depend on AI.
- **Technical:** Dose-response curves estimated from trial-level data. At 0% System 3 usage, both curves converge at the Brain-Only baseline (~46%). At 100% usage, AI-Accurate accuracy reaches ~71% while AI-Faulty drops to ~31% (Study 1). The gap widens monotonically with AI reliance. Study 2 (Time Pressure) shows steeper divergence: AI-Faulty drops to ~12% at high usage under time constraints. Study 3 (Incentives + Feedback) shows a compressed gap (~44pp vs. ~50pp in Control) but the scissors pattern persists. This is not a threshold effect — it's continuous and proportional to AI dependency.
- **Paper snippet:** "When AI provided correct suggestions, they experienced enhanced accuracy, but when it was faulty, they performed significantly worse than the Brain-Only group — a pattern we refer to as the scissors effect." — Shaw & Nave, 2025 (p. 21)

**Step: Add HTML, verify, commit.**

```
git commit -m "feat: add Know More panel for scissors effect chart"
```

---

### Task 12: Know More — Implications Cards

**Files:**
- Modify: `index.html` — insert after the 4 implication cards grid (~line 2812)

**Content:**

- **Plain English:** The paper draws four sets of implications. For <strong>individuals</strong>: reasoning is like a muscle — if you always let AI do the thinking, your own skills may weaken over time. Deliberately solving problems without AI might be as important as physical exercise. For <strong>education</strong>: if students use AI on assignments, exams end up measuring how well they prompt AI rather than whether they actually understand the material. Assessment design needs to catch up. For <strong>AI designers</strong>: the current design of most AI tools — instant, confident, frictionless answers — is exactly what promotes surrender. Adding deliberate friction (like asking "what do you think first?") could shift users from surrender to genuine collaboration. For <strong>society</strong>: if cognitive surrender is the default, then the quality of AI outputs has outsized influence on collective decision-making — in medicine, law, policy, and democracy itself.
- **Technical:** The authors propose a design framework for "calibrated collaboration" (pp. 44–45): (1) Customisable autonomy modes allowing users to set AI involvement level; (2) Adaptive nudging — flagging uncertainty, contradiction, and domain-specific cautions; (3) Transparency and reliability indicators — confidence scores, uncertainty flags, grounded vs. probabilistic vs. uncertain signals; (4) Dynamic cognitive demand adjustment — requiring user reasoning before revealing AI output. The educational implications connect to Bloom's taxonomy: AI tools that provide answers target lower-order cognition (remember/understand), while tools that scaffold reasoning could target higher-order cognition (analyze/evaluate/create).
- **Paper snippet:** "Rather than fully automating choices, effective AI design may encourage calibrated collaboration, where System 3 enhances and collaborates with internal cognition… understanding and indicating the reliability of AI recommendations may help individuals strategically regulate System 3 usage." — Shaw & Nave, 2025 (pp. 44–45)

**Step: Add HTML, verify, commit.**

```
git commit -m "feat: add Know More panel for implications"
```

---

### Task 13: Know More — Vulnerability Bars

**Files:**
- Modify: `index.html` — insert after the vulnerability bars section (~line 2880)

**Content:**

- **Plain English:** These four bars show the traits that predict who surrenders to AI and who resists. <strong>Trust in AI</strong> (red bar): people who reported trusting AI systems were the most vulnerable — 64% less likely to override a wrong AI answer. Trust isn't bad in itself, but uncalibrated trust is. <strong>Need for Cognition</strong> (amber bar): this measures how much you enjoy effortful thinking — puzzling through hard problems rather than looking for the quick answer. Scoring higher nearly doubled your odds of catching AI mistakes. <strong>Fluid intelligence</strong> (purple bar): this measures raw reasoning ability — pattern recognition and logical inference, not learned facts. Higher scores nearly doubled resistance to faulty AI. <strong>Incentives + Feedback</strong> (green bar): paying people for correct answers and giving them immediate feedback helped — override rates doubled — but even highly motivated people still surrendered on the majority of faulty trials.
- **Technical:** Logistic regression results from Study 1 (confirmed in Studies 2–3). Trust in AI (Jian et al., 2000): OR = 0.36 for overriding faulty AI (i.e., each SD increase in trust reduced override odds by 64%). Need for Cognition (Cacioppo et al., 1984, 18-item NFC scale): OR = 1.86 for override (each SD increase nearly doubled override odds). Fluid Intelligence (ICAR-16 matrix reasoning subset): OR = 1.96 for override. All three held in a combined model controlling for each other. Study 3 Incentives + Feedback: override OR = 4.25 (p = 6.30 × 10⁻⁹), but absolute surrender rate remained >50% on faulty trials even with incentives, suggesting motivational interventions are necessary but insufficient.
- **Paper snippet:** "Trust in AI amplified vulnerability… Higher fluid intelligence nearly doubled the odds of resisting faulty AI… cognitive surrender persists. Even with incentives and feedback, the fundamental vulnerability to faulty AI remains a structural feature of human-AI interaction." — Shaw & Nave, 2025 (pp. 21–22, 37)

**Step: Add HTML, verify, commit.**

```
git commit -m "feat: add Know More panel for vulnerability factors"
```

---

## Phase 3: Base Text Fixes

### Task 14: Fix assumed jargon in base text

**Files:**
- Modify: `index.html` — ~11 targeted edits across the page

**Step 1: Fix each instance**

1. **Line ~2157** — "Beyond Kahneman's dual-process model"
   - Change to: "Psychologists have long used a two-system model of thinking — fast intuition (System 1) and slow deliberation (System 2), a framework developed by Nobel laureate Daniel Kahneman. Shaw & Nave propose that AI introduces a third cognitive system — and with it, new pathways for both insight and surrender."

2. **Line ~2370** — "Cohen's h measures how much AI accuracy matters"
   - Change to: "Cohen's h is a statistical measure of how far apart two rates are — in this case, how differently people perform when AI is right vs. wrong. Anything above 0.8 is considered a 'large' effect, meaning the gap is substantial and unlikely due to chance."

3. **Line ~2381** — "(Hedges' g = 0.54)"
   - Change to: "(Hedges' g = 0.54 — a 'medium' effect size, meaning AI access shifted confidence by roughly half a standard deviation)"

4. **Line ~2399** — "OR = 0.36, meaning 64% less likely to resist faulty AI"
   - Change to: "The odds ratio (OR) was 0.36 — meaning for each standard-deviation increase in AI trust, people were 64% less likely to override faulty AI advice."

5. **Line ~2407** — "OR = 1.86, nearly doubling odds of overriding faulty AI"
   - Change to: "OR = 1.86 — meaning each standard-deviation increase in enjoyment of thinking nearly doubled the odds of catching and overriding AI mistakes."

6. **Line ~2415** — "OR = 1.96, nearly doubling odds of catching AI errors"
   - Change to: "OR = 1.96 — meaning each standard-deviation increase in reasoning ability nearly doubled the odds of resisting faulty AI."

7. **Line ~2613** — "(OR = 16.07, 95% CI [11.50, 22.46], p < 2.20 × 10⁻¹⁶)"
   - Change to: "(the odds ratio was 16.07, with a 95% confidence interval of 11.50 to 22.46 — meaning this result is extremely robust and statistically overwhelming)"

8. **Line ~2625** — "(Hedges' g = 0.54)"
   - Change to: "(Hedges' g = 0.54, a medium-sized effect)"

9. **Line ~2404** — "Need for Cognition" heading area
   - Add after the `<h4>`: a subtitle or modify the `<p>` to read: "Need for Cognition measures how much someone enjoys effortful thinking. Higher NFC → less surrender."

10. **Line ~2412** — "Fluid Intelligence" heading area
    - Add context: "Fluid intelligence measures raw reasoning ability — pattern recognition and logic, independent of learned knowledge. Higher IQ → less surrender."

11. **CRT references** — Check lines ~3343, ~3688 for any "CRT" without context. These are in JS comments/data so lower priority, but if "CRT" appears in user-visible text without "Cognitive Reflection Test", expand it.

**Step 2: Read the file to verify exact current text before editing**

Always `Read` the target lines before making edits — line numbers may have shifted from earlier tasks.

**Step 3: Verify**

Open page, check each edited section reads naturally. No layout breaks.

**Step 4: Commit**

```
git add index.html
git commit -m "fix: remove assumed jargon from base text, add inline context for technical terms"
```

---

## Phase 4: Verification + Ship

### Task 15: Full verification pass

**Step 1: Start local server**

```bash
cd "/Users/avinash/AICodeLab/Explainers/AI and Congnition Paper"
python3 -c "import http.server, os; os.chdir('.'); http.server.HTTPServer(('',8770), http.server.SimpleHTTPRequestHandler).serve_forever()"
```

**Step 2: Test all 11 Know More panels**

For each of the 11 panels:
- [ ] Panel is collapsed by default (no content visible)
- [ ] Clicking "Plain English" shows tier 1 content
- [ ] Clicking "Technical" swaps to tier 2
- [ ] Clicking "From the Paper" swaps to tier 3 (with left-border accent styling)
- [ ] Clicking the active tab collapses the panel
- [ ] Smooth expand/collapse animation

**Step 3: Test base text fixes**

- [ ] Theory section intro no longer assumes Kahneman knowledge
- [ ] Cohen's h explanation is clear
- [ ] Hedges' g has context
- [ ] Odds ratios have inline explanation
- [ ] Need for Cognition and Fluid Intelligence are defined

**Step 4: Test existing features still work**

- [ ] CRT experiment gate (participate / skip / undo skip)
- [ ] A/B assignment (Brain-Only / AI-Assisted)
- [ ] All charts render (Study 1, 2, 3, Big Picture)
- [ ] Condition toggles work (Control / Time Pressure, Control / Incentives)
- [ ] Dose-response slider works
- [ ] Route selector in Theory section works
- [ ] Scroll-reveal animations fire
- [ ] No JS console errors

**Step 5: Test mobile responsiveness**

Resize browser to 375px width:
- [ ] Know More tabs wrap or scroll horizontally
- [ ] Panel content doesn't overflow
- [ ] Base text fixes render cleanly

**Step 6: Commit and push**

```bash
git add index.html
git commit -m "feat: complete 3-tier Know More system with 11 panels + base text clarity fixes"
git push origin main
```

---

## Summary

| Phase | Tasks | What |
|-------|-------|------|
| 1 | Tasks 1–2 | CSS classes + JS toggle function |
| 2 | Tasks 3–13 | 11 Know More panel HTML blocks |
| 3 | Task 14 | ~11 base text jargon fixes |
| 4 | Task 15 | Full verification + push |

**Total: 15 tasks across 4 phases.**
