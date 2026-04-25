# ENGG 114 Project B — Report Asset Map and Outline

This outline maps current project artifacts to report sections and identifies missing items still to create.

---

## 1. Executive Summary

**What to write**
- One-page summary of objective, constraints, selected preliminary concept, and key performance outcome.
- State that current selection is preliminary pending prototype validation.

**File/assets to insert**
- `report_assets/selected_plate_fin_design.md`
- `outputs/tables/selected_plate_fin_design.csv`

**Calculation/table/plot support**
- Predicted `R_total`, `T_chip`, and margins to 70 °C / 85 °C / 0.45 °C/W from selected design table.

**Still needs to be created**
- Final executive summary figure (one compact “design snapshot” graphic).
- Final wording after prototype test results are available.

---

## 2. Problem Definition and Specifications

**What to write**
- Project statement and thermal requirements:
  - chip size 50.8 mm × 50.8 mm,
  - heat load 100 W,
  - ambient 25 °C,
  - derated target 70 °C,
  - failure 85 °C,
  - allowable thermal resistance 0.45 °C/W.

**File/assets to insert**
- `src/heatsink_model.py` (constants section)
- `report_assets/assumption_audit_table.md`

**Calculation/table/plot support**
- Table of design targets and constraints.
- Assumption traceability table for baseline values.

**Still needs to be created**
- Final requirement verification matrix (Req ID → evidence).

---

## 3. Existing Cooling Solutions

**What to write**
- Short literature/market scan of relevant CPU cooling approaches (plate-fin, pin-fin, vapor chamber, active blower options).
- Why plate-fin forced convection is chosen for first-pass analysis.

**File/assets to insert**
- *(No direct file currently in repo dedicated to this section.)*

**Calculation/table/plot support**
- Comparative qualitative table (complexity, cost, manufacturability, expected thermal performance).

**Still needs to be created**
- A sourced comparison table with citations.
- Optional benchmark figure from datasheets/literature.

---

## 4. Thermal Resistance Model

**What to write**
- Derivation and equations used for conduction, contact, convection, fin efficiency, and temperature prediction.
- Modeling assumptions and validity limits.

**File/assets to insert**
- `src/heatsink_model.py`
- `report_assets/assumption_audit_table.md`

**Calculation/table/plot support**
- Equation summary table:
  - `R_base = L/(kA)`
  - `R_contact = t/(kA)`
  - fin efficiency relation
  - `R_conv = 1/(h*A_eff)`
  - `T_chip = T_ambient + Q*R_total`

**Still needs to be created**
- A clean equation figure for report formatting.
- Model validation subsection (to be filled after prototype data).

---

## 5. Concept Generation and Screening

**What to write**
- Describe preliminary concepts, assumptions, and screening logic.
- Explain required effective area vs assumed area and pass/fail criteria.

**File/assets to insert**
- `src/concept_compare.py`
- `outputs/tables/concept_comparison.csv`

**Calculation/table/plot support**
- Concept comparison table with:
  - `A_eff_required` vs `A_eff_assumed`
  - `area_margin_percent`
  - `R_total` and `T_chip` pass/fail.

**Still needs to be created**
- Small bar chart: area margin by concept.
- Short rationale text for concept down-selection.

---

## 6. Parametric Geometry Sweep

**What to write**
- Sweep setup, variable ranges, constraints (including spacing filter), and interpretation of results.
- Explain why many geometries pass and how screening narrows options.

**File/assets to insert**
- `src/plate_fin_geometry_sweep.py`
- `outputs/tables/plate_fin_geometry_sweep.csv`
- `outputs/tables/plate_fin_passing_geometries.csv`

**Calculation/table/plot support**
- Distribution table/summary of passing vs total cases.
- Candidate ranking table (e.g., by `R_total`, by mass).

**Still needs to be created**
- Plots:
  - `R_total` vs mass scatter,
  - `T_chip` vs spacing,
  - Pareto front (mass vs thermal resistance).

---

## 7. Selected Preliminary Design

**What to write**
- Selected geometry details, thermal predictions, and quantified margins.
- Justification for selecting this candidate over alternatives.

**File/assets to insert**
- `report_assets/selected_plate_fin_design.md`
- `outputs/tables/selected_plate_fin_design.csv`
- `outputs/tables/plate_fin_passing_geometries.csv` (for ranking context)

**Calculation/table/plot support**
- Final selected design table (geometry + performance + margins).
- Optional short comparison table: selected design vs next-best alternatives.

**Still needs to be created**
- Decision matrix (thermal margin, mass, manufacturability, risk).

---

## 8. CAD Drawing Package

**What to write**
- CAD modeling process, drawing standards, and manufacturing-ready view/dimension requirements.

**File/assets to insert**
- `report_assets/solidworks_modeling_steps.md`
- `report_assets/cad_drawing_checklist.md`

**Calculation/table/plot support**
- Geometry conformance checks (fin count, spacing/pitch, total width).

**Still needs to be created**
- Actual CAD screenshots/figures.
- Final 2D drawing PDF with title block and tolerances.

---

## 9. BOM

**What to write**
- Preliminary bill of materials for prototype build (heat sink part, fan, heater block, TIM, fasteners, test sensors).

**File/assets to insert**
- `report_assets/selected_plate_fin_design.md` (mass/reference geometry)
- `report_assets/prototype_test_plan.md` (instrumentation hints)

**Calculation/table/plot support**
- Cost and lead-time table.
- Mass and material summary.

**Still needs to be created**
- `report_assets/preliminary_bom.csv` or markdown BOM table with part numbers, qty, unit cost, vendor.

---

## 10. Prototype Test Plan

**What to write**
- Experimental validation method, pass/fail criteria, data collection process, and uncertainty handling.

**File/assets to insert**
- `report_assets/prototype_test_plan.md`
- `report_assets/assumption_audit_table.md`

**Calculation/table/plot support**
- Test matrix and data template from prototype plan.
- Planned computed metrics: `ΔT`, measured effective `R_th`.

**Still needs to be created**
- As-built test logs and plots after running prototype tests.
- Repeatability statistics (multiple trials).

---

## 11. Conclusion

**What to write**
- Summarize current findings, confidence level, and next actions to reach final design release.
- Clearly distinguish modeled preliminary status from validated status.

**File/assets to insert**
- `report_assets/selected_plate_fin_design.md`
- `report_assets/prototype_test_plan.md`

**Calculation/table/plot support**
- Final summary table of predicted performance and required validation gates.

**Still needs to be created**
- Post-test conclusion update with measured results.

---

## 12. Appendix: Python Code and Full Sweep Data

**What to write**
- Reproducibility appendix with script descriptions and output file references.

**File/assets to insert**
- `src/heatsink_model.py`
- `src/concept_compare.py`
- `src/plate_fin_geometry_sweep.py`
- `outputs/tables/concept_comparison.csv`
- `outputs/tables/plate_fin_geometry_sweep.csv`
- `outputs/tables/plate_fin_passing_geometries.csv`
- `outputs/tables/selected_plate_fin_design.csv`

**Calculation/table/plot support**
- File manifest table and run commands.

**Still needs to be created**
- Optional reproducibility script/Makefile (`run_all.sh`) that regenerates all tables.
- Optional compressed archive for large CSV appendices.

---

## Suggested Final Report Build Order

1. Freeze specs + assumptions.  
2. Finalize thermal model/equations section.  
3. Insert concept screen + sweep figures.  
4. Lock selected preliminary design section.  
5. Add CAD package and BOM.  
6. Execute prototype tests and update conclusion with measured data.  

