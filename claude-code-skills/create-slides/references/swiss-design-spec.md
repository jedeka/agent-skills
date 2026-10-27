# Swiss-Informed Technical Presentation Design System

## 1. Global Visual Language

Design for a **technical research presentation**, not a poster.

The visual language is Swiss-inspired: precise grid, strong typographic hierarchy, asymmetric composition, restrained color, consistent alignment, and high information density.

Prioritize **clarity, hierarchy, technical legibility, and structural consistency** over decorative minimalism.

Do not intentionally create large empty areas merely for aesthetic effect. Whitespace should separate, group, and frame information.

Use a white or very light background, near-black primary text, gray secondary text, and a restrained accent color.

Avoid gradients, glassmorphism, excessive rounded cards, heavy shadows, decorative geometry, glowing effects, 3D styling, and generic futuristic AI aesthetics.

---

# 2. Canvas and Grid

Use a 16:9 widescreen canvas.

Use a **12-column underlying grid** with consistent outer margins and gutters.

Default horizontal margin: approximately 0.55–0.65 in.

Default gutter: approximately 0.15–0.20 in.

All major objects should align to the grid or to another deliberate alignment reference.

Maintain a consistent vertical rhythm across slides.

The grid is structural and should usually remain invisible.

---

# 3. Typography

### Primary Typeface

Preferred: **Inter**

Alternatives: Helvetica Neue, Neue Haas Grotesk, IBM Plex Sans, Aptos.

Use one primary sans-serif family throughout the deck.

Optional monospace: IBM Plex Mono or JetBrains Mono for code, identifiers, tensor dimensions, and technical metadata.

### Type Hierarchy

* Main title: 32–40 pt, semibold/bold
* Section title: 40–56 pt, semibold/bold
* Slide title: 28–36 pt, semibold/bold
* Large key statement: 30–44 pt, semibold/bold
* Body text: 19–23 pt, regular
* Secondary text: 16–19 pt
* Caption: 13–16 pt
* Metadata/footer: 10–12 pt
* Equations: 23–30 pt

Use sentence case by default.

Use uppercase only for small labels, metadata, and navigation markers.

Left alignment is the default.

Avoid excessive bolding, italics, decorative typography, and multiple typefaces.

---

# 4. Color System

### Base

* Background: `#FFFFFF`
* Primary text: `#111111`
* Secondary text: `#666666`
* Tertiary text: `#929292`
* Divider: `#D9D9D9`
* Panel background: `#F4F4F2`

### Accents

* Primary accent: `#D93838`
* Secondary blue: `#315EF5`
* Positive green: `#198754`
* Warning amber: `#C78A00`

Use color sparingly.

The default visual structure should be primarily black, white, and gray.

Accent colors must have stable semantic meaning. Do not change the meaning of a color between slides.

Do not use red merely because the design is Swiss-inspired.

---

# 5. Main Title Slide

Use a strong asymmetrical composition with substantial but controlled visual presence.

Place the title primarily on the left side of the grid.

Use a small metadata label above or near the title.

The title should be the largest textual element.

Use a concise subtitle beneath it.

Author, affiliation, event, and date should be visually subordinate.

A restrained visual element, diagram, image, or geometric structure may occupy the opposite side, but it must remain secondary to the title.

Do not center all elements by default.

Do not fill the slide with decorative graphics.

---

# 6. Section Title Slide

Use a strong typographic composition with very few elements.

Display a small section number or metadata label.

Make the section title large and visually dominant.

Optional subtitle may explain the section in one short line.

Use asymmetry and whitespace for separation, but do not create excessive empty space.

The slide should feel like a transition within the same visual system, not a completely different design.

---

# 7. Standard Main Content Slide

Use a clear title at the top-left.

Place the principal content directly beneath it.

Use one dominant visual or conceptual object.

Supporting text, annotations, and metadata should be visually subordinate.

Maintain strong alignment between title, content, and footer.

Avoid multiple competing focal points.

---

# 8. Two-Column Text + Visual

Divide the slide into approximately **4–5 columns + 7–8 columns**.

Use the larger region for the technically important visual.

Use the smaller region for explanation, labels, equations, or concise supporting text.

Keep both columns aligned to the same top and bottom structure.

Do not give equal visual weight to unequal information.

Prefer asymmetrical column widths.

---

# 9. Two-Column Text + Images

Use one text region and one image region.

The image should be large enough to inspect without zooming.

Prefer one strong image or a small, coherent image group over many small images.

Align image edges to the grid.

Use short captions directly associated with the image.

Do not surround every image with decorative borders or cards.

When comparing images, use consistent dimensions and alignment.

---

# 10. Full-Width Image / Figure Slide

Allow the figure to occupy most of the slide.

Keep the title compact and visually subordinate to the figure.

Use a short caption or annotation to identify the important interpretation.

Do not shrink a technically important figure merely to create decorative margins.

The figure itself should be the dominant visual object.

---

# 11. Architecture / Pipeline Slide

Give the architecture the majority of the available area.

Organize components according to natural computational or conceptual flow.

Use alignment, spacing, and directional connectors to show relationships.

Use stable semantic colors for different entities or modalities.

Prefer flat 2D forms.

Avoid excessive boxes, rounded rectangles, shadows, gradients, and decorative icons.

Labels should be concise and readable.

The reader should be able to understand the major flow without reading a paragraph.

---

# 12. Equation-Focused Slide

Treat equations as primary visual objects rather than inline text.

Use one major equation or a small coherent group of equations.

Give equations sufficient size and surrounding space for inspection.

Use nearby annotations to define important variables or interpret the equation.

Maintain strong typographic contrast between formal mathematics and explanatory prose.

Do not compress equations into tiny text.

---

# 13. Chart / Results Slide

Make the chart the primary visual object.

Use restrained monochrome styling with one or two semantic accents.

Highlight the scientifically important method, comparison, or result.

Keep axes, units, labels, and necessary experimental context.

Use subtle gridlines only when useful.

Avoid 3D charts, excessive colors, decorative effects, and unnecessary legends.

Directly label important values when doing so improves readability.

---

# 14. Table Slide

Treat the table as a typographic information structure rather than a spreadsheet.

Use whitespace, alignment, and typography instead of heavy cell borders.

Emphasize the most important row, column, or comparison using weight or a restrained accent.

Keep numerical precision appropriate to the evidence.

Avoid dense tables copied directly from papers without redesign.

All essential values must remain readable at presentation distance.

---

# 15. Image Comparison Slide

Use consistent image dimensions and alignment.

Arrange images according to the intended comparison rather than decorative symmetry.

Use concise labels above or below each image.

If highlighting a difference, use one restrained visual marker such as an outline, annotation, or accent.

Avoid decorative frames.

---

# 16. Text-Dominant Slide

Use strong typographic hierarchy rather than large paragraphs.

Break information into short conceptual units.

Use bold or accent treatment only for the most important terms.

Keep line lengths moderate.

Do not turn the slide into a document page.

Prefer a few substantial statements over many fragmented bullets.

---

# 17. Key Number / Large Statistic Slide

Use one dominant numerical result.

Display the number large enough to be immediately visible.

Place the metric, unit, and comparison close to the number.

Use a short explanatory statement beneath or beside it.

The number should communicate something meaningful; do not enlarge arbitrary statistics merely for visual impact.

---

# 18. Comparison Slide

Use a clear visual axis of comparison.

Align competing methods, conditions, or alternatives consistently.

Make the intended difference immediately visible through position, scale, typography, or one restrained accent.

Avoid giving every alternative identical visual emphasis when one is the focal method.

---

# 19. Quote / Statement Slide

Use a large, concise statement as the dominant element.

Attribute the statement using smaller secondary typography.

Use very little decoration.

Prefer left alignment and asymmetric positioning.

Do not use quotation slides frequently.

---

# 20. Summary / Closing Slide

Use a small label or section marker.

Present a small number of concise statements with strong hierarchy.

Do not introduce substantial new information.

Use spacing, alignment, and typography to make the hierarchy obvious.

A final statement may be larger than the supporting points.

---

# 21. Footer and Navigation

Use a small, consistent footer across ordinary slides.

Recommended contents:

* author or lab
* optional short presentation identifier
* slide number

Use restrained typography around 10–12 pt.

Section numbers or small labels may appear near the title.

Navigation should be visible but never compete with the main content.

---

# 22. Shapes and Lines

Prefer simple geometric forms.

Default to sharp or minimally rounded corners.

Use thin rules and dividers.

Avoid shadows unless they serve a genuine structural purpose.

Do not place information inside cards unless grouping genuinely improves comprehension.

---

# 23. Spacing

Use spacing systematically.

Related elements should be close.

Unrelated elements should have visibly larger separation.

Maintain consistent spacing increments wherever practical.

Do not distribute objects evenly merely because the slide contains empty space.

Spacing should communicate hierarchy and relationships.

---

# 24. Visual Density

Target **moderate-to-high useful information density**.

A technically complex slide may occupy most of the available canvas.

Do not reduce content solely to preserve minimalist aesthetics.

Do not overcrowd the slide with multiple unrelated focal points.

The goal is:

**high signal, high structure, low decorative noise.**

---

# 25. Consistency Rules

Across all slides, preserve:

* typography
* margins
* grid
* spacing rhythm
* footer
* alignment behavior
* color semantics
* diagram language
* chart language

Individual layouts may vary substantially.

Consistency should come from the **design system**, not from making every slide look identical.

---

# 26. Absolute Priorities

When visual decisions conflict, prioritize in this order:

1. technical readability
2. information hierarchy
3. structural alignment
4. semantic consistency
5. visual elegance
6. decorative aesthetics

Never sacrifice technical comprehension for stylistic purity.

The presentation should feel:

**precise, intelligent, technical, editorial, restrained, and deliberately composed.**
