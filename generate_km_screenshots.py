"""Generate PDF screenshots for all 10 Know More panels."""
import fitz
import os

doc = fitz.open("ssrn-6097646.pdf")

# Define clips: (page_0indexed, rect, output_filename, description)
# Page dimensions are ~612 x 792 points (US Letter)
clips = [
    # km-trisystem: Table 1 — Cognitive affordances and tradeoffs (p.12)
    (11, fitz.Rect(50, 35, 560, 520), "pdf-highlights/km_trisystem.png",
     "Table 1: System comparison"),

    # km-cognitiveRoutes: Table 2 — Canonical routes (p.16)
    (15, fitz.Rect(50, 35, 560, 760), "pdf-highlights/km_cognitiveRoutes.png",
     "Table 2: Canonical routes"),

    # km-surrender: Cognitive Surrender definition (p.17)
    (16, fitz.Rect(50, 35, 560, 500), "pdf-highlights/km_surrender.png",
     "Cognitive Surrender definition"),

    # km-followrate: Figure 2 — Follow/Override rates (p.23)
    (22, fitz.Rect(50, 35, 560, 700), "pdf-highlights/km_followrate.png",
     "Figure 2: Follow/Override rates"),

    # km-accuracy: Figure 3 — Accuracy by condition (p.24)
    (23, fitz.Rect(50, 35, 560, 650), "pdf-highlights/km_accuracy.png",
     "Figure 3: Accuracy by condition"),

    # km-confidence: Confidence paragraph (p.25)
    (24, fitz.Rect(50, 35, 560, 330), "pdf-highlights/km_confidence.png",
     "Confidence inflation results"),

    # km-individual: Figure 4 — Individual differences (p.26)
    (25, fitz.Rect(50, 35, 560, 650), "pdf-highlights/km_individual.png",
     "Figure 4: Individual differences"),

    # km-timepressure: Figure 5 — Time pressure accuracy (p.30)
    (29, fitz.Rect(50, 35, 560, 700), "pdf-highlights/km_timepressure.png",
     "Figure 5: Time pressure accuracy"),

    # km-incentives: Figure 7 — Incentives follow/override (p.35)
    (34, fitz.Rect(50, 35, 560, 700), "pdf-highlights/km_incentives.png",
     "Figure 7: Incentives follow/override"),

    # km-synthesis: Figure 10 — Dose-response curves (p.43)
    (42, fitz.Rect(50, 35, 560, 760), "pdf-highlights/km_synthesis.png",
     "Figure 10: Dose-response curves"),
]

os.makedirs("pdf-highlights", exist_ok=True)

for page_idx, rect, output_path, desc in clips:
    page = doc[page_idx]
    pix = page.get_pixmap(clip=rect, dpi=200)
    pix.save(output_path)
    print(f"Saved: {output_path} (page {page_idx + 1}) — {desc}")

# Clean up removed panel screenshots
removed = [
    "pdf-highlights/km_scissors.png",
    "pdf-highlights/km_implications.png",
    "pdf-highlights/km_vulnerability.png",
]
for path in removed:
    if os.path.exists(path):
        os.remove(path)
        print(f"Removed: {path}")

doc.close()
print("\nDone! Generated 10 screenshots, removed 3 obsolete ones.")
