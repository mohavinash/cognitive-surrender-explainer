# Design: 3-Tier Know More System

## Overview

Add a 3-tier "Know More" expandable panel to ~11 key content blocks across the explainer. Each panel offers three depth levels: Plain English, Technical, and From the Paper. Hidden by default; user-activated via tabbed toggle.

## Decisions

- **Approach:** Static content tabs (Approach A) — all content hardcoded in HTML as hidden divs, toggled by JS. Matches existing single-file architecture.
- **Scope:** ~11 key finding blocks (not all 53 content blocks).
- **UI Pattern:** Tabbed panel below content, reusing existing toggle-group/toggle-btn styling.
- **Base text fixes:** Separate pass to remove assumed knowledge from existing section intros.

## UI Component

### Structure
```
[Content block: chart, stat, or card]

  Know More  [Plain English]  [Technical]  [From the Paper]

┌─────────────────────────────────────────────┐
│  (Selected tier content, smooth expand)      │
└─────────────────────────────────────────────┘
```

### Behavior
- Collapsed by default. No content visible until user clicks a tab.
- Clicking a tab expands the panel with that tier's content.
- Clicking a different tab swaps content in-place.
- Clicking the active tab again collapses the panel entirely.
- Smooth max-height transition (same pattern as Kejriwal blog accused cards).

### CSS Classes
- `.know-more` — container wrapper
- `.know-more-tabs` — tab bar (reuses `.toggle-group` / `.toggle-btn` patterns)
- `.know-more-panel` — content area (hidden by default, animated expand)
- `.know-more-panel--active` — visible state
- `.know-more-snippet` — "From the Paper" tier styling (left-border accent, italic, page ref)

### JS
- `toggleKnowMore(id, tier)` — single function, toggles active tab + panel visibility.
- Exported on `window.KnowMore` or similar.

## Target Blocks (11)

| # | Section | Block | Rationale |
|---|---------|-------|-----------|
| 1 | Theory | Tri-System diagram | Core framework needs context |
| 2 | Theory | "Cognitive surrender" pull quote | Central concept definition |
| 3 | Study 1 | 79.8% key stat | Headline finding |
| 4 | Study 1 | Accuracy chart | The scissors pattern |
| 5 | Study 1 | Individual differences cards | Moderators need explanation |
| 6 | Study 2 | 12.1% stat + buffer/cost cards | Time pressure amplification |
| 7 | Study 3 | 2x override stat + helped/persisted | Incentives as partial remedy |
| 8 | Big Picture | 16x effect + confidence/surrender | Cross-study synthesis |
| 9 | Big Picture | Scissors effect chart | Dose-response relationship |
| 10 | Implications | 4 implication cards | Practical takeaways |
| 11 | Implications | Vulnerability bars | Who's at risk |

## Content Tone per Tier

### Plain English
Accessible language. Uses technical terms but doesn't assume you already know them. Not patronising — respects the reader while providing context.

Example (Tri-System diagram):
> Psychologists have long described two ways humans think: fast gut reactions (System 1) and slow, careful reasoning (System 2). This paper argues AI has become a third system — not inside your head, but one you think with. The key question: when you ask AI for an answer, do you evaluate what it says, or just accept it?

### Technical
Full stats, methodology, effect sizes, confidence intervals, moderator analysis. For someone comfortable reading research.

Example (79.8% stat):
> On chat-engaged faulty AI trials, 79.8% of responses followed the AI's incorrect suggestion (Study 1, N=238 AI-Assisted). Follow rate for accurate trials was 92.7%. Cohen's h = 0.83 (large effect). Not moderated by trial position — no learning effect across 7 CRT items. Trust in AI increased surrender (OR = 3.47); Fluid IQ (OR = 0.23) and Need for Cognition (OR = 0.65) were protective.

### From the Paper
Verbatim quote with page reference. Distinctive styling (left-border accent, italic).

Example:
> "cognitive surrender is an uncritical abdication of reasoning itself. It reflects not merely the use of external assistance, but a relinquishing of cognitive control."
> — Shaw & Nave, 2025 (p. 15)

## Base Text Fixes

Separate pass to fix ~5-8 instances of assumed knowledge:

1. "Beyond Kahneman's dual-process model" → explain what dual-process theory is before going beyond it
2. "Cohen's h" references → brief inline explanation of what it measures
3. "Hedges' g = 0.54" → inline context
4. "OR = 0.36" / odds ratios in vulnerability bars → explain what odds ratios mean
5. Any other naked jargon that assumes prior knowledge

Principle: Don't shy away from technical terms, but don't assume the reader already knows them.

## Verification

1. All 11 Know More panels collapsed by default
2. Each tab shows correct tier content
3. Clicking active tab collapses panel
4. "From the Paper" tier has distinctive quote styling
5. Base text fixes don't break existing layout
6. Mobile responsive (tabs stack or scroll horizontally)
7. No JS errors
