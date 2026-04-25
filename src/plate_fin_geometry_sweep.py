"""Preliminary aluminum plate-fin geometry sweep for ENGG 114 Project B.

This script performs a first-pass parameter sweep only; it does not choose a
final design.
"""

from __future__ import annotations

import csv
from pathlib import Path

from heatsink_model import (
    ALLOWABLE_TOTAL_THERMAL_RESISTANCE_C_PER_W,
    AMBIENT_AIR_C,
    CHIP_LENGTH_M,
    CHIP_WIDTH_M,
    DERATED_TARGET_C,
    FAILURE_LIMIT_C,
    HEAT_LOAD_W,
    base_conduction_resistance,
    chip_temperature_c,
    contact_resistance,
    convection_resistance,
    effective_area,
    rectangular_fin_efficiency,
)

# Material and interface assumptions.
K_ALUMINUM_W_PER_MK = 205.0  # [W/(m*K)]
INTERFACE_THICKNESS_M = 0.0001  # [m]
INTERFACE_CONDUCTIVITY_W_PER_MK = 3.0  # [W/(m*K)]

# Fixed first-pass assumptions.
BASE_LENGTH_M = 0.0508  # [m]
BASE_WIDTH_M = 0.0508  # [m]
FIN_SPAN_WIDTH_M = 0.0508  # [m]
H_W_PER_M2K = 65.0  # [W/(m^2*K)]

# Sweep ranges.
NUM_FINS_RANGE = range(8, 31)  # 8..30
FIN_HEIGHT_VALUES_M = [0.015 + 0.005 * i for i in range(8)]  # 0.015..0.050
FIN_THICKNESS_VALUES_M = [0.001 + 0.0005 * i for i in range(5)]  # 0.001..0.003
BASE_THICKNESS_VALUES_M = [0.003 + 0.001 * i for i in range(4)]  # 0.003..0.006


def _is_physically_packable(num_fins: int, fin_thickness_m: float, base_width_m: float) -> bool:
    """Basic manufacturability screen: total fin footprint must fit base width."""
    return num_fins * fin_thickness_m < base_width_m


def run_sweep() -> list[dict[str, float | int | bool]]:
    """Evaluate all geometry combinations and return row dictionaries."""
    chip_area_m2 = CHIP_LENGTH_M * CHIP_WIDTH_M
    contact_r = contact_resistance(INTERFACE_THICKNESS_M, INTERFACE_CONDUCTIVITY_W_PER_MK, chip_area_m2)
    base_top_area_m2 = BASE_LENGTH_M * BASE_WIDTH_M

    rows: list[dict[str, float | int | bool]] = []

    for num_fins in NUM_FINS_RANGE:
        for fin_height_m in FIN_HEIGHT_VALUES_M:
            for fin_thickness_m in FIN_THICKNESS_VALUES_M:
                if not _is_physically_packable(num_fins, fin_thickness_m, BASE_WIDTH_M):
                    continue

                for base_thickness_m in BASE_THICKNESS_VALUES_M:
                    r_base = base_conduction_resistance(base_thickness_m, K_ALUMINUM_W_PER_MK, chip_area_m2)

                    eta_fin = rectangular_fin_efficiency(
                        h_w_per_m2k=H_W_PER_M2K,
                        fin_conductivity_w_per_mk=K_ALUMINUM_W_PER_MK,
                        fin_thickness_m=fin_thickness_m,
                        fin_length_m=fin_height_m,
                    )

                    fin_footprint_area_m2 = num_fins * fin_thickness_m * FIN_SPAN_WIDTH_M
                    base_exposed_area_m2 = base_top_area_m2 - fin_footprint_area_m2
                    if base_exposed_area_m2 < 0.0:
                        continue

                    a_eff_m2 = effective_area(
                        num_fins=num_fins,
                        fin_length_m=fin_height_m,
                        fin_width_m=FIN_SPAN_WIDTH_M,
                        fin_efficiency=eta_fin,
                        base_exposed_area_m2=base_exposed_area_m2,
                    )

                    r_conv = convection_resistance(H_W_PER_M2K, a_eff_m2)
                    r_total = r_base + contact_r + r_conv
                    t_chip_c = chip_temperature_c(AMBIENT_AIR_C, HEAT_LOAD_W, r_total)

                    pass_r_total = r_total <= ALLOWABLE_TOTAL_THERMAL_RESISTANCE_C_PER_W
                    pass_derated = t_chip_c <= DERATED_TARGET_C
                    pass_failure = t_chip_c <= FAILURE_LIMIT_C

                    rows.append(
                        {
                            "num_fins": num_fins,
                            "fin_height_m": fin_height_m,
                            "fin_thickness_m": fin_thickness_m,
                            "base_thickness_m": base_thickness_m,
                            "h_W_per_m2K": H_W_PER_M2K,
                            "eta_fin": eta_fin,
                            "base_exposed_area_m2": base_exposed_area_m2,
                            "A_eff_m2": a_eff_m2,
                            "R_base_K_per_W": r_base,
                            "R_contact_K_per_W": contact_r,
                            "R_conv_K_per_W": r_conv,
                            "R_total_K_per_W": r_total,
                            "T_chip_C": t_chip_c,
                            "Pass_R_total": pass_r_total,
                            "Pass_derated_70C": pass_derated,
                            "Pass_failure_85C": pass_failure,
                        }
                    )

    return rows


def write_csv(rows: list[dict[str, float | int | bool]]) -> Path:
    out_path = Path("outputs/tables/plate_fin_geometry_sweep.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "num_fins",
        "fin_height_m",
        "fin_thickness_m",
        "base_thickness_m",
        "h_W_per_m2K",
        "eta_fin",
        "base_exposed_area_m2",
        "A_eff_m2",
        "R_base_K_per_W",
        "R_contact_K_per_W",
        "R_conv_K_per_W",
        "R_total_K_per_W",
        "T_chip_C",
        "Pass_R_total",
        "Pass_derated_70C",
        "Pass_failure_85C",
    ]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return out_path


def write_passing_csv(rows: list[dict[str, float | int | bool]]) -> Path:
    """Write only geometries that pass all criteria."""
    out_path = Path("outputs/tables/plate_fin_passing_geometries.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    passing_rows = [
        r
        for r in rows
        if bool(r["Pass_R_total"]) and bool(r["Pass_derated_70C"]) and bool(r["Pass_failure_85C"])
    ]

    fieldnames = [
        "num_fins",
        "fin_height_m",
        "fin_thickness_m",
        "base_thickness_m",
        "h_W_per_m2K",
        "eta_fin",
        "base_exposed_area_m2",
        "A_eff_m2",
        "R_base_K_per_W",
        "R_contact_K_per_W",
        "R_conv_K_per_W",
        "R_total_K_per_W",
        "T_chip_C",
        "Pass_R_total",
        "Pass_derated_70C",
        "Pass_failure_85C",
    ]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(passing_rows)

    return out_path


def print_summary(rows: list[dict[str, float | int | bool]]) -> None:
    print("Plate-fin geometry sweep (preliminary; not final design)")
    print(
        f"Q={HEAT_LOAD_W:.1f} W | Ambient={AMBIENT_AIR_C:.1f} C | "
        f"R_allow={ALLOWABLE_TOTAL_THERMAL_RESISTANCE_C_PER_W:.2f} C/W"
    )
    print(f"Chip={CHIP_LENGTH_M:.4f} m x {CHIP_WIDTH_M:.4f} m | h={H_W_PER_M2K:.1f} W/m^2K")

    passing = [
        r
        for r in rows
        if bool(r["Pass_R_total"]) and bool(r["Pass_derated_70C"]) and bool(r["Pass_failure_85C"])
    ]
    print(f"Evaluated combinations: {len(rows)}")
    print(f"Passing all criteria: {len(passing)}")

    top = sorted(rows, key=lambda r: float(r["R_total_K_per_W"]))[:10]
    print("\nTop 10 lowest R_total candidates:")
    print(
        f"{'fins':>4} {'h_fin(m)':>8} {'t_fin(m)':>8} {'t_base(m)':>9} {'A_eff':>8} "
        f"{'R_total':>8} {'T_chip':>8} {'R<=0.45':>8} {'T<=70':>6} {'T<=85':>6}"
    )
    for r in top:
        print(
            f"{int(r['num_fins']):4d} "
            f"{float(r['fin_height_m']):8.3f} "
            f"{float(r['fin_thickness_m']):8.4f} "
            f"{float(r['base_thickness_m']):9.4f} "
            f"{float(r['A_eff_m2']):8.4f} "
            f"{float(r['R_total_K_per_W']):8.4f} "
            f"{float(r['T_chip_C']):8.2f} "
            f"{str(r['Pass_R_total']):>8} "
            f"{str(r['Pass_derated_70C']):>6} "
            f"{str(r['Pass_failure_85C']):>6}"
        )


if __name__ == "__main__":
    result_rows = run_sweep()
    csv_path = write_csv(result_rows)
    passing_csv_path = write_passing_csv(result_rows)
    print_summary(result_rows)
    print(f"\nWrote CSV: {csv_path}")
    print(f"Wrote passing CSV: {passing_csv_path}")
