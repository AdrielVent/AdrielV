# CAD Drawing Checklist — Preliminary Aluminum Plate-Fin Heat Sink

> **Design status:** Preliminary concept only (not final until prototype/test/manufacturing review).

## Selected Geometry (for all CAD/drawing checks)

- **Base**
  - Length: **50.8 mm**
  - Width: **50.8 mm**
  - Thickness: **3.0 mm**
- **Fins**
  - Number of fins: **17**
  - Fin height: **25.0 mm** (from top face of base)
  - Fin thickness: **1.0 mm**
  - Fin span: **50.8 mm**
  - Fin spacing (gap between adjacent fins): **2.112 mm**

---

## 1) 3D Model Build Steps (Checklist)

- [ ] Set document units to **MMGS** (mm, g, s) or equivalent.
- [ ] Create base solid: 50.8 × 50.8 × 3.0 mm.
- [ ] Create one fin feature on base top face:
  - [ ] thickness = 1.0 mm
  - [ ] height = 25.0 mm
  - [ ] span = 50.8 mm
- [ ] Linear pattern the fin to get **17 total fins**.
- [ ] Pattern direction is across base width.
- [ ] Set spacing correctly: **2.112 mm gap** between fins (or equivalent pitch setup).
- [ ] Verify no fin extends outside base envelope.
- [ ] Confirm final overall body is watertight/valid (no self-intersections).

---

## 2) Required 2D Drawing Views

Include these views on the fabrication drawing:

- [ ] **Top view**
- [ ] **Front view**
- [ ] **Right side view**
- [ ] **Isometric view** (for visual clarity)
- [ ] **Section view through fins** (to clearly show fin thickness, spacing, and base thickness)

---

## 3) Required Dimensions to Label

### Base
- [ ] Base length = 50.8 mm
- [ ] Base width = 50.8 mm
- [ ] Base thickness = 3.0 mm

### Fin array
- [ ] Number of fins = 17 (note callout)
- [ ] Fin thickness = 1.0 mm
- [ ] Fin height = 25.0 mm
- [ ] Fin span/length = 50.8 mm
- [ ] Fin spacing (clear gap) = 2.112 mm
- [ ] Pattern pitch (if used) = 3.112 mm (1.0 + 2.112)
- [ ] Total array width check (fins + gaps) = 50.8 mm

### Recommended dimensioning practice
- [ ] Dimension from datums/baselines, not chain-dimensioning entire array.
- [ ] Keep repeated fin data in one place via note + pattern callout.

---

## 4) Manufacturing Notes (Suggested)

- [ ] Process placeholder note (e.g., “Manufacturing method TBD: CNC/skived/extruded profile + finish machining”).
- [ ] Deburr all sharp edges unless otherwise specified.
- [ ] Remove burrs/chips from fin channels.
- [ ] Do not damage fin tips/edges during handling.
- [ ] Maintain fin straightness and parallelism across array.

---

## 5) Tolerance Suggestions (Preliminary)

> Confirm with manufacturing capability before release.

- [ ] General linear tolerance (unless noted): **±0.10 mm**
- [ ] Base thickness: **±0.05 mm**
- [ ] Fin thickness: **±0.05 mm**
- [ ] Fin spacing (critical airflow feature): **±0.05 mm**
- [ ] Flatness of chip-contact face: **0.05 mm** (or tighter if required by interface spec)
- [ ] Perpendicularity of fins to base: **0.1 mm/25 mm** guideline

---

## 6) Material Callout

- [ ] Material: **Aluminum alloy** (project preliminary assumption: thermal conductivity basis ~205 W/m·K).
- [ ] If known, specify exact grade (e.g., 6061-T6 / 1050 / 1100) in title block or notes.

---

## 7) Surface / Interface Note for Chip Contact Face

- [ ] Identify base bottom (chip-contact face) as functional thermal interface surface.
- [ ] Add surface finish requirement (example): **Ra ≤ 1.6 µm** (confirm with thermal interface requirements).
- [ ] Add flatness requirement for contact face.
- [ ] Note: apply thermal interface material during assembly per thermal design procedure.

---

## 8) Drawing Title Block Items

- [ ] Part name: *Preliminary Plate-Fin Heat Sink*
- [ ] Part number / drawing number
- [ ] Revision
- [ ] Units (mm)
- [ ] Scale
- [ ] Material
- [ ] Mass (reference): **0.079196 kg** (preliminary)
- [ ] Drawn by / checked by / date
- [ ] Sheet number and total sheets
- [ ] Projection method symbol (1st or 3rd angle)

---

## 9) Common Drawing Mistakes to Avoid

- [ ] Mixing mm and m in callouts.
- [ ] Confusing **spacing** (gap) with **pitch**.
- [ ] Omitting fin count and assuming symmetry implies count.
- [ ] Missing section view, making fin geometry ambiguous.
- [ ] Over-dimensioning the fin array with redundant chained dimensions.
- [ ] Forgetting to specify contact-face requirements (flatness/finish).
- [ ] No revision/date updates after geometry edits.
- [ ] Leaving material unspecified or inconsistent with thermal assumptions.

