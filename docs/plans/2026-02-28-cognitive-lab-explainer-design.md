# Cognitive Lab Explainer: "Thinking - Fast, Slow, and Artificial"

## Overview

Interactive single-file HTML explainer for the Shaw & Nave (2026) Wharton research paper on Tri-System Theory and Cognitive Surrender. Framed as a "Cognitive Lab" where readers experience the research before learning the findings.

**Paper**: "Thinking - Fast, Slow, and Artificial: How AI is Reshaping Human Reasoning and the Rise of Cognitive Surrender" by Steven D. Shaw & Gideon Nave, Wharton School, UPenn.

**Target Audience**: General public / non-academic readers.

**Reference Pattern**: Kejriwal Acquittal Explainer (single-file HTML, scroll-based narrative, interactive elements).

---

## Two Parallel Workstreams

### Workstream 1: DocETL Pipeline

**Pre-processing**: Extract text + figures from PDF using Python (PyMuPDF).

**Input**: `paper_sections.json` - 8 logical sections:
1. Abstract + Introduction (pages 1-7)
2. Tri-System Theory framework (pages 8-18)
3. Empirical Overview + Methods (pages 19-21)
4. Study 1: System 3 Influences Reasoning (pages 21-27)
5. Study 2: Time Pressure (pages 28-34)
6. Study 3: Incentives & Feedback (pages 35-41)
7. General Discussion + Synthesis (pages 41-48)
8. Implications + Conclusion (pages 48-55)

**Pipeline stages**:

| Stage | Operation | Model | Purpose |
|-------|-----------|-------|---------|
| 1 | extract_narrative | Gemini 2.5 Flash | Key concepts, definitions, analogies, quotes per section |
| 2 | extract_statistics | Gemini 2.5 Flash | All p-values, ORs, CIs, means, SEs, effect sizes per study |
| 3 | extract_figure_data | Gemini 2.5 Flash | Bar heights, labels, error bars, annotations for each figure |
| 4 | compile_narrative | Gemini 3.0 Flash | Plain-language explanations, executive summary, key takeaways |
| 5 | compile_chart_data | Gemini 3.0 Flash | Structured JSON for every interactive chart |
| 6 | generate_explainer_content | Gemini 3.0 Flash | 8 blog sections, CRT demo content, implications |

**Output**: `paper_analysis.json` with structured data for all interactive elements.

### Workstream 2: Interactive Frontend

Single-file HTML with embedded CSS + JS. No external dependencies.

---

## Aesthetic Direction: "Cognitive Lab"

- **Background**: Dark slate/charcoal (#0f172a) with subtle dot-grid texture
- **System colors**: Blue (#3B82F6) for System 2, Amber (#F59E0B) for System 1, Coral (#EF4444) for System 3/AI
- **Typography**: Distinctive serif display font + clean sans-serif body
- **Accents**: Monospace for data callouts, glowing borders on interactive elements
- **Motion**: Scroll-reveal, animated chart growth, pathway highlighting
- **Tone**: Scientific editorial meets interactive dashboard

---

## Frontend Sections (8)

### 1. HERO (100vh)
- Title + authors + hook: "What happens to your thinking when AI thinks for you?"
- Animated 3-node visualization (Systems 1/2/3) as background
- Scroll indicator

### 2. THE CRT EXPERIENCE ("Try It Yourself")
- 2-3 CRT questions from the adapted test
- Text input for answer
- "Ask AI" button triggers simulated chatbot (sometimes correct, sometimes wrong)
- After completion: reveal results, map to study data
- Bridge: "You just experienced the experiment. Here's what 1,372 people did..."

### 3. THE BIG IDEA: TRI-SYSTEM THEORY
- Interactive SVG diagram (Figure 1): clickable System 1/2/3 nodes
- Animated pathways: Intuition, Deliberation, Cognitive Offloading, Cognitive Surrender, Autopilot
- Brain boundary visual divider
- Table 1 as interactive 3-column card layout (System comparison)
- Table 2 cognitive routes as clickable flow paths

### 4. STUDY 1: THE SURRENDER EFFECT
- Interactive bar charts (Figures 2 & 3)
- Toggle: Follow/Override rates vs Accuracy by Condition
- Key stat callouts: "93% followed AI when correct, 80% followed when wrong"
- Effect size meter (Cohen's h = 0.81)
- Figure 4: Individual differences faceted chart (Trust, NFC, Fluid IQ)

### 5. STUDY 2: UNDER PRESSURE
- Interactive Figures 5 & 6
- Toggle: Control vs Time Pressure
- Thinking Profiles comparison: Independents vs AI-Users
- Key finding: AI buffers time pressure costs when accurate, but surrender persists

### 6. STUDY 3: CAN WE FIX IT?
- Interactive Figures 7, 8 & 9
- Toggle: Control vs Incentives+Feedback
- Override rates visualization (20% -> 42% on faulty AI)
- Key finding: partially malleable, gap persists

### 7. THE DOSE-RESPONSE CURVE
- Interactive Figure 10 recreation
- Draggable slider: System 3 Usage 0% -> 100%
- Two diverging curves (AI-Accurate rises, AI-Faulty falls)
- Condition toggle overlay
- Key stat: OR = 16.07

### 8. WHAT THIS MEANS
- Implication cards: Society, AI Design, Policy, Vulnerability profiles
- Who's most susceptible (high trust, low NFC, low fluid IQ)
- Concluding paper quote
- Footer with paper citation and methodology note

---

## Global Interactive Elements

- Reading progress bar (top, 3px)
- Scroll-triggered reveal animations
- Responsive design (mobile-first, breakpoints at 680px, 420px)
- `prefers-reduced-motion` support
- No external dependencies (vanilla JS, SVG charts)

---

## Key Data Points for Charts

### Figure 2 (Follow/Override):
- AI-Accurate: Follow 93%, Override 7%
- AI-Faulty: Follow 80%, Override 20%

### Figure 3 (Accuracy):
- Brain-Only: 45.8%, AI-Accurate: 71.0%, AI-Faulty: 31.5%
- Deltas: +25pp (accurate), -14pp (faulty), 40pp gap

### Figure 4 (Individual Differences):
- Trust in AI: amplifies vulnerability to faulty AI
- NFC: protective against faulty AI
- Fluid IQ: protective against faulty AI

### Figure 5 (Time Pressure):
- Brain-Only: Control 46.9%, Time Pressure 32.6%
- AI-Accurate: Control ~80%, TP ~71%
- AI-Faulty: Control ~20%, TP ~12%

### Figure 7 (Incentives Override):
- Control AI-Faulty override: 20%
- Incentives+Feedback AI-Faulty override: 42.3%

### Figure 8 (Incentives Accuracy):
- Brain-Only: Control ~42%, I+F ~64%
- AI-Accurate: Control ~68%, I+F ~81%
- AI-Faulty: Control ~31%, I+F ~46%

### Figure 10 (Dose-Response):
- 0% usage: ~50% accuracy (Brain-Only baseline)
- 100% usage AI-Accurate: ~92-95%
- 100% usage AI-Faulty: ~5-18%

---

## CRT Demo Questions (from paper's adapted CRT-7)

Classic CRT-style questions where intuitive answer is wrong:
1. Bat and ball variant: "A laptop and a case cost $110 in total. The laptop costs $100 more than the case. How much does the case cost?"
   - Intuitive (wrong): $10
   - Correct: $5

2. Machine variant: "If 5 machines take 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?"
   - Intuitive (wrong): 100 minutes
   - Correct: 5 minutes

3. Lily pad variant: "In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how long would it take to cover half the lake?"
   - Intuitive (wrong): 24 days
   - Correct: 47 days

---

## Technical Decisions

- **Single HTML file**: All CSS + JS embedded (matching Kejriwal pattern)
- **Charts**: Vanilla JS with SVG (no D3 or Chart.js dependency)
- **Animations**: CSS transitions + IntersectionObserver + requestAnimationFrame
- **Images**: Figure screenshots from PDF with lazy loading
- **Performance**: Passive scroll listeners, will-change hints, lazy image loading
