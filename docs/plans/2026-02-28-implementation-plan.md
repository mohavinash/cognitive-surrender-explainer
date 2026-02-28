# Cognitive Lab Explainer - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build an interactive single-file HTML explainer for the Shaw & Nave Tri-System Theory paper, with a DocETL pipeline for structured data extraction.

**Architecture:** Two workstreams: (1) DocETL pipeline extracts structured JSON from the PDF via section-based analysis, (2) Single-file HTML frontend consumes that JSON to render an interactive "Cognitive Lab" experience with fully interactive charts, a mini-CRT demo, and animated visualizations.

**Tech Stack:** Python (PyMuPDF for PDF extraction), DocETL (YAML pipeline with Gemini 2.5/3.0 Flash), Vanilla HTML/CSS/JS (single file, SVG charts, IntersectionObserver, requestAnimationFrame).

---

## Phase 1: PDF Pre-processing

### Task 1: Extract text from PDF by logical sections

**Files:**
- Create: `docetl-pipeline/extract_pdf.py`
- Create: `docetl-pipeline/paper_sections.json`

**Step 1: Create the PDF text extraction script**

```python
"""
Extract text from the Shaw & Nave PDF, split into logical sections.
Uses PyMuPDF (fitz) to extract text page-by-page, then groups into
the paper's logical sections.
"""
import fitz  # PyMuPDF
import json
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), '..', 'ssrn-6097646.pdf')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'paper_sections.json')

# Logical sections mapped to page ranges (0-indexed)
# Based on reading the paper structure
SECTIONS = [
    {
        "section_id": "abstract_introduction",
        "title": "Abstract & Introduction",
        "start_page": 0,   # page 1
        "end_page": 6,     # page 7
        "description": "Abstract, introduction, motivation for Tri-System Theory"
    },
    {
        "section_id": "tri_system_theory",
        "title": "Tri-System Theory of Cognition",
        "start_page": 7,   # page 8
        "end_page": 17,    # page 18
        "description": "Dual-process theories, System 3 definition, cognitive surrender concept, Tables 1-2, Figure 1"
    },
    {
        "section_id": "empirical_overview_methods",
        "title": "Empirical Overview & Common Methods",
        "start_page": 18,  # page 19
        "end_page": 20,    # page 21
        "description": "Three studies overview, CRT design, key variables, statistical approach"
    },
    {
        "section_id": "study1",
        "title": "Study 1: System 3 Influences Cognitive Reasoning",
        "start_page": 20,  # page 21
        "end_page": 27,    # page 28
        "description": "N=359, Brain-Only vs AI-Assisted, Figures 2-4, individual differences"
    },
    {
        "section_id": "study2",
        "title": "Study 2: System 3 Buffers the Effects of Time Pressure",
        "start_page": 27,  # page 28
        "end_page": 34,    # page 35
        "description": "N=485, time pressure manipulation, Figures 5-6, thinking profiles"
    },
    {
        "section_id": "study3",
        "title": "Study 3: Incentives and Feedback Reduce Cognitive Surrender",
        "start_page": 34,  # page 35
        "end_page": 41,    # page 42
        "description": "N=450, incentives+feedback, Figures 7-9, per-item confidence"
    },
    {
        "section_id": "general_discussion",
        "title": "General Discussion & Synthesis",
        "start_page": 41,  # page 42
        "end_page": 48,    # page 49
        "description": "Cognitive surrender effect size, Figure 10, individual differences synthesis, cognitive surrender vs offloading"
    },
    {
        "section_id": "implications_conclusion",
        "title": "Implications & Conclusion",
        "start_page": 48,  # page 49
        "end_page": 54,    # page 55 (before references)
        "description": "Theoretical, societal, design/policy implications, limitations, conclusion"
    }
]

PAPER_METADATA = {
    "title": "Thinking\u2014Fast, Slow, and Artificial: How AI is Reshaping Human Reasoning and the Rise of Cognitive Surrender",
    "authors": ["Steven D. Shaw", "Gideon Nave"],
    "affiliation": "The Wharton School of the University of Pennsylvania",
    "version": "v20260111",
    "total_participants": 1372,
    "total_trials": 9593,
    "num_studies": 3
}


def extract_text_by_pages(pdf_path, start_page, end_page):
    """Extract text from a range of pages."""
    doc = fitz.open(pdf_path)
    text_parts = []
    for page_num in range(start_page, min(end_page + 1, len(doc))):
        page = doc[page_num]
        text_parts.append(page.get_text())
    doc.close()
    return "\n".join(text_parts)


def main():
    sections = []
    for section_def in SECTIONS:
        text = extract_text_by_pages(
            PDF_PATH,
            section_def["start_page"],
            section_def["end_page"]
        )
        sections.append({
            "section_id": section_def["section_id"],
            "title": section_def["title"],
            "start_page": section_def["start_page"] + 1,  # 1-indexed for output
            "end_page": section_def["end_page"] + 1,
            "description": section_def["description"],
            "paper_title": PAPER_METADATA["title"],
            "authors": PAPER_METADATA["authors"],
            "text": text
        })

    output = {
        "metadata": PAPER_METADATA,
        "sections": sections
    }

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(sections)} sections to {OUTPUT_PATH}")
    for s in sections:
        print(f"  {s['section_id']}: pages {s['start_page']}-{s['end_page']} ({len(s['text'])} chars)")


if __name__ == "__main__":
    main()
```

**Step 2: Run extraction**

Run: `cd docetl-pipeline && python extract_pdf.py`
Expected: `paper_sections.json` created with 8 sections.

**Step 3: Commit**

```bash
git add docetl-pipeline/extract_pdf.py docetl-pipeline/paper_sections.json
git commit -m "feat: add PDF text extraction script and extracted sections"
```

---

### Task 2: Extract figures from PDF as images

**Files:**
- Create: `docetl-pipeline/extract_figures.py`
- Create: `figures/` directory with PNG images

**Step 1: Create figure extraction script**

```python
"""
Extract figures from the PDF as high-resolution PNG images.
Uses PyMuPDF to identify and extract images from specific pages.
"""
import fitz
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), '..', 'ssrn-6097646.pdf')
FIGURES_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')

# Figure locations (0-indexed pages)
FIGURES = [
    {"number": 1, "page": 13, "title": "Tri-System Theory of Cognition"},
    {"number": 2, "page": 22, "title": "Participants adopt System 3 answers"},
    {"number": 3, "page": 23, "title": "System 3 facilitates cognitive surrender"},
    {"number": 4, "page": 26, "title": "Individual differences moderate System 3 reasoning"},
    {"number": 5, "page": 31, "title": "Time pressure reduces accuracy across trial types"},
    {"number": 6, "page": 32, "title": "System 3 can avert time pressure performance declines"},
    {"number": 7, "page": 37, "title": "Incentives and feedback reduce cognitive surrender to faulty System 3"},
    {"number": 8, "page": 39, "title": "Incentives and feedback increase accuracy, but cognitive surrender persists"},
    {"number": 9, "page": 40, "title": "Incentives and feedback improve System 3 calibration in AI-Users"},
    {"number": 10, "page": 42, "title": "Cognitive surrender as a function of System 3 usage across three studies"},
]


def extract_figure_as_screenshot(pdf_path, page_num, output_path, dpi=200):
    """Render a full page as a high-res PNG."""
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    pix.save(output_path)
    doc.close()


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)

    for fig in FIGURES:
        output_path = os.path.join(FIGURES_DIR, f"figure_{fig['number']}.png")
        extract_figure_as_screenshot(PDF_PATH, fig["page"], output_path)
        print(f"Figure {fig['number']}: {fig['title']} -> {output_path}")

    print(f"\nExtracted {len(FIGURES)} figures to {FIGURES_DIR}/")


if __name__ == "__main__":
    main()
```

**Step 2: Run extraction**

Run: `cd docetl-pipeline && python extract_figures.py`
Expected: 10 PNG files in `figures/` directory.

**Step 3: Commit**

```bash
git add docetl-pipeline/extract_figures.py figures/
git commit -m "feat: extract all 10 figures from PDF as PNG images"
```

---

## Phase 2: DocETL Pipeline

### Task 3: Create DocETL pipeline configuration

**Files:**
- Create: `docetl-pipeline/pipeline.yaml`

**Step 1: Write the pipeline YAML**

The pipeline has 6 stages:
1. `extract_narrative` (Map, Gemini 2.5 Flash) - concepts, definitions, quotes per section
2. `extract_statistics` (Map, Gemini 2.5 Flash) - all statistical values per section
3. `extract_figure_data` (Map, Gemini 2.5 Flash) - chart data for interactive recreation
4. `compile_narrative` (Reduce, Gemini 3.0 Flash) - plain-language compilation
5. `compile_chart_data` (Reduce, Gemini 3.0 Flash) - structured chart JSON
6. `generate_explainer_content` (Map, Gemini 3.0 Flash) - 8 blog sections + CRT demo

Key prompts must be carefully designed for:
- Extracting exact statistical values (means, SEs, CIs, p-values, ORs, effect sizes)
- Extracting figure data with bar heights, labels, and error bars for chart recreation
- Generating plain-language explanations for a general audience
- Creating the CRT demo question content

**Step 2: Run the pipeline**

Run: `cd docetl-pipeline && docetl run pipeline.yaml`
Expected: `output/paper_analysis.json` with all structured data.

**Step 3: Commit**

```bash
git add docetl-pipeline/pipeline.yaml docetl-pipeline/output/
git commit -m "feat: add DocETL pipeline and run analysis"
```

---

### Task 4: Validate and supplement extracted data

**Files:**
- Modify: `docetl-pipeline/output/paper_analysis.json` (manual corrections if needed)

**Step 1: Cross-check extracted chart data against paper**

Verify these key data points from the paper:
- Figure 2: Follow rates 93%/80%, Override rates 7%/20%
- Figure 3: Accuracy Brain-Only 45.8%, AI-Accurate 71.0%, AI-Faulty 31.5%
- Cohen's h = 0.81 (Study 1), 0.86 (S2), 0.78 (S3), weighted 0.82
- OR = 16.07 for cognitive surrender effect across studies
- Individual differences: Trust amplifies, NFC/Fluid IQ protect

**Step 2: Fix any extraction errors in the JSON**

**Step 3: Commit**

```bash
git add docetl-pipeline/output/paper_analysis.json
git commit -m "fix: validate and correct extracted chart data"
```

---

## Phase 3: Frontend Implementation

### Task 5: HTML scaffold with CSS design system

**Files:**
- Create: `index.html`

**Step 1: Build the HTML skeleton with full CSS design system**

Create the single-file HTML with:
- CSS variables for the "Cognitive Lab" theme
- Dark slate background (#0f172a) with dot-grid texture
- System colors: Blue (#3B82F6), Amber (#F59E0B), Coral (#EF4444)
- Typography: Distinctive serif + sans-serif pairing via Google Fonts
- Responsive breakpoints (680px, 420px)
- All 8 section containers (empty content)
- Reading progress bar
- Scroll-reveal animation system (IntersectionObserver)
- `prefers-reduced-motion` support

**Step 2: Verify in browser**

Open `index.html` in browser. Should see dark themed page with section placeholders.

**Step 3: Commit**

```bash
git add index.html
git commit -m "feat: HTML scaffold with Cognitive Lab CSS design system"
```

---

### Task 6: Hero section + global navigation

**Files:**
- Modify: `index.html`

**Step 1: Build the hero section**

- Full viewport (100vh) dark hero
- Animated 3-node System visualization (SVG with CSS animations)
- Title, authors, hook line
- Table of contents with smooth-scroll links
- Scroll indicator (bouncing arrow)

**Step 2: Add reading progress bar**

- Fixed 3px bar at top
- Scales based on scroll position
- Uses passive scroll listener

**Step 3: Verify and commit**

```bash
git add index.html
git commit -m "feat: hero section with animated systems visualization"
```

---

### Task 7: Mini-CRT interactive demo (Section 2)

**Files:**
- Modify: `index.html`

**Step 1: Build the CRT question interface**

- 3 CRT questions (bat-and-ball, machine, lily-pad variants)
- Text input for each answer
- "Ask AI" button that shows a simulated chatbot response
- AI sometimes gives correct answer, sometimes gives intuitive (wrong) answer
- Question state machine: unanswered -> answered -> revealed

**Step 2: Build the results reveal**

- After all 3 questions answered, show results panel
- For each: whether user was correct, whether they followed AI, whether AI was right
- Map results to study percentages: "93% of people did what you did on this one"
- Animated count-up for the mapping stats
- Bridge text: "You just experienced the experiment..."

**Step 3: Verify interaction flow and commit**

```bash
git add index.html
git commit -m "feat: interactive mini-CRT demo with simulated AI chatbot"
```

---

### Task 8: Tri-System Theory interactive diagram (Section 3)

**Files:**
- Modify: `index.html`

**Step 1: Build the interactive SVG diagram (Figure 1)**

- SVG-based flow diagram matching the paper's Figure 1
- 3 clickable system nodes with distinct colors
- Internal (in vivo) zone above brain boundary
- External (in silico) zone below brain boundary
- Animated connection paths between systems
- Click a system to highlight its pathways and show description

**Step 2: Build cognitive routes explorer (Table 2)**

- 5 clickable route cards: Intuition, Deliberation, Offloading, Surrender, Autopilot
- Clicking a route highlights that path in the diagram above
- Shows the route formula (e.g., "Stimulus -> System 1 (brief) -> System 3 -> Response")
- Description panel with plain-language explanation

**Step 3: Build System comparison table (Table 1)**

- 3-column interactive card layout (System 1 / System 2 / System 3)
- Rows: Origin, Speed, Effort, Accuracy, Emotion, Ethics, Justification
- Hover/click to highlight differences across systems
- Each card uses its system color

**Step 4: Verify and commit**

```bash
git add index.html
git commit -m "feat: interactive Tri-System diagram, routes explorer, comparison table"
```

---

### Task 9: Study 1 interactive charts (Section 4)

**Files:**
- Modify: `index.html`

**Step 1: Build SVG bar chart engine**

Create a reusable vanilla JS function for animated bar charts:
- `createBarChart(container, data, options)`
- Supports grouped bars, error bars, statistical annotations
- Hover shows exact value + SE + CI + p-value
- Animated bar growth on scroll-into-view
- Responsive sizing

**Step 2: Build Figure 2 (Follow/Override rates)**

- Grouped bars: AI-Accurate vs AI-Faulty
- Light bars = Follow AI, Dark bars = Override
- Values: 93/7 (Accurate), 80/20 (Faulty)
- Delta annotation: 13%, z = 3.87***
- Hover for full stats

**Step 3: Build Figure 3 (Accuracy by condition)**

- 3 bars: Brain-Only (46%), AI-Accurate (71%), AI-Faulty (31%)
- Delta annotations between bars (+25%, -14%, 40% gap)
- z-scores and significance stars
- Color: gold for brain-only, blue for accurate, coral for faulty

**Step 4: Build Cohen's h effect size meter**

- Visual gauge/meter showing h = 0.81
- Scale: 0 (none) to 1.0+ (huge)
- Reference markers: 0.2 small, 0.5 medium, 0.8 large
- Animated fill on scroll

**Step 5: Build Figure 4 (Individual differences)**

- 3-panel faceted chart: Trust in AI, NFC, Fluid IQ
- Each panel: grouped bars by Trial Type (Brain-Only, AI-Accurate, AI-Faulty)
- Split by median (Low vs High)
- Significance stars on AI-Faulty contrasts

**Step 6: Verify and commit**

```bash
git add index.html
git commit -m "feat: Study 1 interactive charts with hover stats"
```

---

### Task 10: Study 2 interactive charts (Section 5)

**Files:**
- Modify: `index.html`

**Step 1: Build Figure 5 (Time pressure x trial type x thinking profile)**

- 3-panel chart: Brain-Only, AI-Accurate, AI-Faulty
- Each panel: Control vs Time Pressure bars
- Split by: Brain-Only probe, Independents, AI-Users
- Significance annotations

**Step 2: Build Figure 6 (System 3 averts time pressure)**

- 2-panel chart: Control vs Time Pressure
- Bars: Brain-Only, Independents, AI-Users
- Each bar split by AI-Accurate / AI-Faulty
- Toggle between panels

**Step 3: Add condition toggle**

- Button group: Control / Time Pressure
- Clicking toggles animated bar transitions between conditions
- Smooth height transitions (0.4s ease)

**Step 4: Verify and commit**

```bash
git add index.html
git commit -m "feat: Study 2 interactive charts with condition toggles"
```

---

### Task 11: Study 3 interactive charts (Section 6)

**Files:**
- Modify: `index.html`

**Step 1: Build Figure 7 (Follow/Override under Incentives+Feedback)**

- 2-panel: Control vs Incentives+Feedback
- Grouped bars: AI-Accurate and AI-Faulty
- Follow (light) vs Override (dark)
- Delta annotations showing the jump in override rates

**Step 2: Build Figure 8 (Accuracy under Incentives+Feedback)**

- 3 grouped bars: Brain-Only, AI-Accurate, AI-Faulty
- Control (light) vs Incentives+Feedback (dark)
- All significance annotations

**Step 3: Build Figure 9 (Thinking profiles under Incentives+Feedback)**

- 2-panel: Control vs Incentives+Feedback
- Bars per thinking profile: Brain-Only, Independents, AI-Users
- AI-Accurate (dark) vs AI-Faulty (light) per profile

**Step 4: Verify and commit**

```bash
git add index.html
git commit -m "feat: Study 3 interactive charts with incentive toggles"
```

---

### Task 12: Dose-response curve explorer (Section 7)

**Files:**
- Modify: `index.html`

**Step 1: Build the interactive dose-response visualization (Figure 10)**

- SVG canvas with two curves: AI-Accurate and AI-Faulty
- X-axis: System 3 Usage (0% to 100%)
- Y-axis: Estimated Accuracy (0% to 100%)
- Shaded confidence interval bands
- 3 condition overlays: Control, Time Pressure, Incentives+Feedback

**Step 2: Add interactive slider**

- Draggable slider on x-axis
- As user drags, vertical line follows
- Readout shows: "At X% AI usage: Y% accuracy (accurate) / Z% accuracy (faulty)"
- The "scissors" effect becomes viscerally obvious

**Step 3: Add condition toggle buttons**

- Toggle which condition curves are visible
- Animated fade in/out of curves
- Brain-Only anchor points at 0% usage

**Step 4: Verify and commit**

```bash
git add index.html
git commit -m "feat: interactive dose-response curve explorer with slider"
```

---

### Task 13: Implications section (Section 8) + Footer

**Files:**
- Modify: `index.html`

**Step 1: Build implication cards**

- 4 cards: Society, AI Design, Policy, Vulnerability
- Each with icon, title, brief description, key data point
- Hover animation (subtle lift + glow)

**Step 2: Build vulnerability profile**

- Visual showing who's most susceptible:
  - High Trust in AI -> more surrender
  - Low NFC -> more surrender
  - Low Fluid IQ -> more surrender
- Animated indicator bars

**Step 3: Build conclusion + footer**

- Concluding quote from paper
- Citation block with paper details
- "Built with" metadata
- Footer links

**Step 4: Verify and commit**

```bash
git add index.html
git commit -m "feat: implications section with cards and vulnerability profile"
```

---

## Phase 4: Polish & Deploy

### Task 14: Animation polish and mobile responsiveness

**Files:**
- Modify: `index.html`

**Step 1: Tune all scroll-reveal animations**

- Stagger timings for each section
- Ensure smooth 60fps on mobile
- Test and tune IntersectionObserver thresholds

**Step 2: Mobile responsive testing**

- Test at 320px, 375px, 414px, 768px, 1024px
- Fix any layout breaks
- Ensure charts resize properly
- Touch interaction for sliders and toggles

**Step 3: Accessibility pass**

- Keyboard navigation for all interactive elements
- ARIA labels on charts
- Screen reader text for data visualizations
- Reduced motion support verified

**Step 4: Commit**

```bash
git add index.html
git commit -m "fix: animation polish, mobile responsiveness, accessibility"
```

---

### Task 15: Final review and deploy

**Files:**
- Modify: `index.html` (any final fixes)

**Step 1: Cross-check all data accuracy**

Verify every number in the explainer against the paper.

**Step 2: Performance check**

- Lighthouse audit
- Ensure lazy loading works
- Check total page weight

**Step 3: Deploy to GitHub Pages**

```bash
git add -A
git commit -m "feat: complete Cognitive Lab explainer"
git push origin main
# Enable GitHub Pages in repo settings (main branch, root)
```

**Step 4: Verify live site**

Open: `https://mohavinash.github.io/cognitive-surrender-explainer/`

---

## Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 1. PDF Pre-processing | 1-2 | Extract text + figures from PDF |
| 2. DocETL Pipeline | 3-4 | Run analysis pipeline, validate data |
| 3. Frontend | 5-13 | Build all 8 sections with interactive elements |
| 4. Polish & Deploy | 14-15 | Responsive, accessible, deployed |

**Total: 15 tasks across 4 phases.**
