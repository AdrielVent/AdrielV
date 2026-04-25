# SolidWorks / FreeCAD / Onshape Modeling Steps (Exact Sequence)

> **Design status:** Preliminary concept only. Do not treat as final release geometry until test/manufacturing review is complete.

## Target Geometry
- Base: 50.8 mm × 50.8 mm × 3.0 mm
- Fins: 17 fins, 25.0 mm height, 1.0 mm thickness, 50.8 mm span
- Fin spacing (gap): 2.112 mm
- Equivalent pattern pitch: 3.112 mm

---

## Step-by-Step

### 1) Make base
1. Start a new part file.
2. Set units to **mm**.
3. Sketch a rectangle on Top (or equivalent) plane: **50.8 mm × 50.8 mm**.
4. Extrude the sketch by **3.0 mm** to create the base block.

### 2) Create one fin
1. Select the **top face of the base**.
2. Start a sketch and draw one rectangular fin profile:
   - Fin length/span along base length: **50.8 mm**
   - Fin thickness across base width: **1.0 mm**
3. Constrain/locate fin so it is fully on the base top face.
4. Extrude the fin profile upward by **25.0 mm**.

### 3) Linear pattern to 17 fins
1. Select the fin feature.
2. Use **Linear Pattern** (or equivalent pattern tool).
3. Pattern direction: across base width (perpendicular to fin span).
4. Set **instances = 17** (total fins).
5. Set pattern spacing as **pitch = 3.112 mm**.

### 4) Set spacing/pitch correctly
1. Confirm the tool interprets spacing as **center-to-center pitch**.
2. Verify:
   - fin thickness = 1.0 mm
   - gap spacing = 2.112 mm
   - therefore pitch = 1.0 + 2.112 = **3.112 mm**
3. If your CAD tool patterns by gap instead of pitch, set gap directly to **2.112 mm**.

### 5) Verify total width equals 50.8 mm
Use this check after patterning:

- Total array width = `N*f_t + (N-1)*s`
- `= 17*(1.0) + 16*(2.112)`
- `= 17.0 + 33.792`
- `= 50.792 mm` (rounding-compatible with 50.8 mm target)

Final checks:
1. Measure overall model width across fin array and base: should be **≈ 50.8 mm**.
2. Ensure no fin body extends outside base boundary.
3. Regenerate/rebuild model and confirm no feature warnings/errors.

---

## Recommended CAD Parameter Names
- `BASE_L = 50.8 mm`
- `BASE_W = 50.8 mm`
- `BASE_T = 3.0 mm`
- `N_FINS = 17`
- `FIN_H = 25.0 mm`
- `FIN_T = 1.0 mm`
- `FIN_SPAN = 50.8 mm`
- `FIN_GAP = 2.112 mm`
- `FIN_PITCH = 3.112 mm`

Using named parameters makes revision control and drawing updates much easier.
