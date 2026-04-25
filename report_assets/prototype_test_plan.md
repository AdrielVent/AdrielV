# Prototype Validation Plan — Preliminary Plate-Fin Heat Sink

> **Design under test (DUT):** Preliminary aluminum plate-fin heat sink, 50.8 mm × 50.8 mm footprint, 3 mm base, 17 fins, 25 mm fin height, 1 mm fin thickness, 2.1125 mm fin spacing.  
> **Prediction reference:** T_chip ≈ 65.51 °C at 100 W (model estimate; to be validated experimentally).

## 1) Test Objective

Validate whether the selected preliminary heat sink geometry can keep the chip-proxy/base interface temperature at or below the derated limit under controlled 100 W loading.

Primary objective:
- Verify **measured base/chip proxy temperature ≤ 70 °C at 100 W** under controlled airflow and measured ambient.

Secondary objectives:
- Quantify thermal margin to 70 °C and 85 °C limits.
- Compare measured vs modeled performance and identify model bias for later refinement.

---

## 2) Required Equipment

- Programmable DC power supply (or electronic load + supply) capable of stable 100 W operation.
- Resistive cartridge heater / flat heater block assembly (chip proxy heat source).
- Calibrated power measurement (voltage + current, or power analyzer).
- Heat spreader/heater block fixture sized for 50.8 mm class interface.
- Thermal interface material (TIM) and controlled clamping fixture.
- Thermocouples (Type K or equivalent), data logger/DAQ, and optional RTD for ambient reference.
- Airflow source (fan/blower) with speed control (PWM/voltage controller).
- Airflow measurement device (anemometer or flow bench), optional differential pressure gauge.
- IR camera (optional) for surface gradient checks.
- Insulation/guarding materials for reducing unintended heat losses.

---

## 3) Heater Block Setup (100 W Chip Simulation)

1. Machine/prepare heater contact face to mate with DUT base contact area.
2. Apply TIM consistently (document type, method, and amount).
3. Clamp DUT to heater block using repeatable torque/load.
4. Energize heater to **100 W electrical input** (record V and I continuously).
5. Hold fan setting fixed for each run; do not adjust during a steady-state segment.
6. Allow sufficient warm-up until steady-state criterion is satisfied.

Notes:
- Record exact fixture stack-up (heater block, TIM, clamp, heat sink orientation).
- If possible, characterize heater losses separately to improve net-heat accuracy.

---

## 4) Thermocouple Locations

Minimum recommended channel set:

- **TC1 (chip proxy / heater near interface):** closest practical location to heat source centerline.
- **TC2 (base center, sink side):** top of base directly above heat source center.
- **TC3 (base edge):** on base near perimeter to capture spreading gradient.
- **TC4 (fin root):** at base-fin junction near center rows.
- **TC5 (fin tip):** near top of representative center fin.
- **TC6 (inlet ambient air):** upstream of fan and DUT.
- **TC7 (local ambient near DUT):** near heat sink inlet plane (shielded from direct radiant bias).

If available, add additional fin-tip channels for spatial repeatability.

---

## 5) Fan / Airflow Control

- Use fixed fan speed setpoints (e.g., low/medium/high) for separate test runs.
- Measure and log airflow metric per run:
  - inlet velocity at standardized points **or**
  - volumetric flow from calibrated setup.
- Record fan command value, measured RPM (if available), and supply voltage/current.
- Maintain consistent ducting/orientation between runs.

---

## 6) Ambient Temperature Measurement

- Ambient reference should be near **25 °C** target condition.
- Use at least one upstream ambient sensor and one local ambient sensor near DUT.
- If ambient differs from 25 °C, compare using **temperature rise**:
  - \\(\Delta T = T_{chip-proxy} - T_{ambient}\\)
- Report both absolute temperatures and ambient-corrected deltas.

---

## 7) Steady-State Criterion

Steady-state is reached when:
- temperature change at chip-proxy/base reference location is **< 0.5 °C over 5 minutes**.

Recommended implementation:
- log data at 1–2 s intervals,
- evaluate rolling 5-minute slope,
- only compute pass/fail metrics from data after criterion is met.

---

## 8) Pass / Fail Criteria

A run is considered **PASS** only if all of the following are true:

1. **Measured base/chip proxy temperature ≤ 70 °C at 100 W**.
2. Ambient is near 25 °C **or** results are interpreted with delta-T correction.
3. Steady-state criterion satisfied: **< 0.5 °C change over 5 minutes**.

Recommended reporting extras (not primary pass criterion):
- Margin to 70 °C and 85 °C thresholds.
- Estimated effective thermal resistance from measured data.

---

## 9) Data Table Template

| Run ID | Date/Time | Heater Power (W) | Ambient Inlet (°C) | Local Ambient (°C) | TC1 Chip Proxy (°C) | TC2 Base Center (°C) | TC4 Fin Root (°C) | TC5 Fin Tip (°C) | Fan Setting | Airflow Metric | Steady-State Met? | dT over 5 min (°C) | Pass/Fail |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---:|---|
| Example-01 | YYYY-MM-DD hh:mm | 100.0 | 25.1 | 25.4 | 66.2 | 64.8 | 60.5 | 51.0 | Medium | 2.8 m/s avg | Yes | 0.22 | Pass |

Suggested derived columns for analysis:
- \(\Delta T_{chip-amb} = T_{chip-proxy} - T_{ambient}\)
- \(R_{th,meas} = \Delta T_{chip-amb} / Q\)

---

## 10) Uncertainty / Error Sources

- Thermocouple calibration uncertainty and channel-to-channel offset.
- Thermocouple attachment quality (contact resistance, adhesive effects).
- Heater electrical power uncertainty (meter accuracy, wiring losses).
- Unknown parasitic heat paths (fixture conduction, radiation, wiring).
- TIM thickness variability and clamp load inconsistency.
- Airflow nonuniformity or drift (fan RPM fluctuations).
- Ambient drift during run.
- Sensor placement variation between repeat tests.

Mitigation:
- Calibrate sensors, standardize assembly torque/TIM procedure, run repeated trials, and report confidence intervals.

---

## 11) Safety Precautions

- Use thermal gloves when handling heated hardware.
- Guard exposed hot surfaces and heater leads.
- Verify electrical insulation and grounding before energizing.
- Do not exceed component current/temperature ratings.
- Keep fan guards in place and secure loose cables away from blades.
- Use emergency shutoff procedure for runaway temperature or smoke/odor events.
- Allow full cool-down before rework or disassembly.

---

## Deliverables from Prototype Phase

- Raw logged temperature/power/airflow data.
- Process notes (TIM method, torque, orientation, ambient conditions).
- Pass/fail summary per run.
- Model-to-test comparison plot and recommended model updates.

