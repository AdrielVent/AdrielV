"""Preliminary concept screening for ENGG 114 heat sink options.

This script intentionally uses preliminary assumptions only; it does not select
final design dimensions.
"""

from __future__ import annotations

import csv
import math
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
)

# Critical correction: use official project heat load (100 W).
CHIP_POWER_W = HEAT_LOAD_W

# Shared preliminary contact-interface assumptions.
THERMAL_INTERFACE_THICKNESS_M = 0.0001  # [m]
THERMAL_INTERFACE_CONDUCTIVITY_W_PER_MK = 3.0  # [W/(m*K)]

# Preliminary concept-screening assumptions only (not final dimensions).
CONCEPTS = [
    {
        "name": "Concept A (dense fins, forced air)",
        "base_thickness_m": 0.0040,  # [m]
        "base_conductivity_w_per_mk": 205.0,  # [W/(m*K)] aluminum-ish
        "h_w_per_m2k": 65.0,  # [W/(m^2*K)]
        "a_eff_m2": 0.0250,  # [m^2]
    },
    {
        "name": "Concept B (moderate fins)",
        "base_thickness_m": 0.0050,  # [m]
        "base_conductivity_w_per_mk": 205.0,  # [W/(m*K)]
        "h_w_per_m2k": 52.0,  # [W/(m^2*K)]
        "a_eff_m2": 0.0210,  # [m^2]
    },
    {
        "name": "Concept C (coarser fins)",
        "base_thickness_m": 0.0060,  # [m]
        "base_conductivity_w_per_mk": 205.0,  # [W/(m*K)]
        "h_w_per_m2k": 43.0,  # [W/(m^2*K)]
        "a_eff_m2": 0.0180,  # [m^2]
    },
]


def evaluate_concepts() -> list[dict[str, float | str | bool]]:
    """Evaluate each preliminary concept and return result rows."""
    chip_contact_area_m2 = CHIP_LENGTH_M * CHIP_WIDTH_M
    r_contact = contact_resistance(
        THERMAL_INTERFACE_THICKNESS_M,
        THERMAL_INTERFACE_CONDUCTIVITY_W_PER_MK,
        chip_contact_area_m2,
    )

    rows: list[dict[str, float | str | bool]] = []
    for concept in CONCEPTS:
        h_w_per_m2k = concept["h_w_per_m2k"]
        a_eff_assumed_m2 = concept["a_eff_m2"]
        r_base = base_conduction_resistance(
            concept["base_thickness_m"],
            concept["base_conductivity_w_per_mk"],
            chip_contact_area_m2,
        )
        r_conv_assumed = convection_resistance(h_w_per_m2k, a_eff_assumed_m2)
        r_total_assumed = r_base + r_contact + r_conv_assumed
        t_chip_assumed_c = chip_temperature_c(AMBIENT_AIR_C, CHIP_POWER_W, r_total_assumed)

        r_conv_required = ALLOWABLE_TOTAL_THERMAL_RESISTANCE_C_PER_W - r_base - r_contact
        if r_conv_required > 0.0:
            a_eff_required_m2 = 1.0 / (h_w_per_m2k * r_conv_required)
            area_margin_percent = 100.0 * (a_eff_assumed_m2 - a_eff_required_m2) / a_eff_required_m2
            has_enough_area = a_eff_assumed_m2 >= a_eff_required_m2
        else:
            # Base + contact already exceed allowed thermal resistance.
            a_eff_required_m2 = math.inf
            area_margin_percent = -math.inf
            has_enough_area = False

        rows.append(
            {
                "Concept": concept["name"],
                "h_W_per_m2K": h_w_per_m2k,
                "A_eff_assumed_m2": a_eff_assumed_m2,
                "A_eff_required_m2": a_eff_required_m2,
                "area_margin_percent": area_margin_percent,
                "R_base_K_per_W": r_base,
                "R_contact_K_per_W": r_contact,
                "R_conv_assumed_K_per_W": r_conv_assumed,
                "R_total_assumed_K_per_W": r_total_assumed,
                "T_chip_assumed_C": t_chip_assumed_c,
                "Has_enough_area": has_enough_area,
                "Pass_R_total": r_total_assumed <= ALLOWABLE_TOTAL_THERMAL_RESISTANCE_C_PER_W,
                "Pass_derated_70C": t_chip_assumed_c <= DERATED_TARGET_C,
                "Pass_failure_85C": t_chip_assumed_c <= FAILURE_LIMIT_C,
            }
        )

    return rows


def write_csv(rows: list[dict[str, float | str | bool]]) -> Path:
    """Write concept comparison table to outputs/tables/concept_comparison.csv."""
    out_path = Path("outputs/tables/concept_comparison.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "Concept",
        "h_W_per_m2K",
        "A_eff_assumed_m2",
        "A_eff_required_m2",
        "area_margin_percent",
        "R_base_K_per_W",
        "R_contact_K_per_W",
        "R_conv_assumed_K_per_W",
        "R_total_assumed_K_per_W",
        "T_chip_assumed_C",
        "Pass_R_total",
        "Pass_derated_70C",
        "Pass_failure_85C",
    ]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return out_path


def print_table(rows: list[dict[str, float | str | bool]]) -> None:
    """Print a compact terminal table for quick screening."""
    print("Preliminary concept screening (not final dimensions)")
    print(f"Ambient: {AMBIENT_AIR_C:.1f} C | Chip power: {CHIP_POWER_W:.1f} W")
    print(f"R_allow = {ALLOWABLE_TOTAL_THERMAL_RESISTANCE_C_PER_W:.2f} C/W")
    print("-" * 148)
    print(
        f"{'Concept':34} {'h':>7} {'A_req':>10} {'A_assumed':>10} {'Area OK?':>8} {'Margin%':>9} "
        f"{'R_total':>9} {'T_chip(C)':>10} {'R<=0.45':>9} {'T<=70':>8} {'T<=85':>8}"
    )
    print("-" * 148)

    for row in rows:
        a_req = float(row["A_eff_required_m2"])
        a_req_str = f"{a_req:10.4f}" if math.isfinite(a_req) else f"{'inf':>10}"
        margin = float(row["area_margin_percent"])
        margin_str = f"{margin:9.1f}" if math.isfinite(margin) else f"{'-inf':>9}"
        print(
            f"{str(row['Concept'])[:34]:34} "
            f"{float(row['h_W_per_m2K']):7.1f} "
            f"{a_req_str} "
            f"{float(row['A_eff_assumed_m2']):10.4f} "
            f"{str(row['Has_enough_area']):>8} "
            f"{margin_str} "
            f"{float(row['R_total_assumed_K_per_W']):9.4f} "
            f"{float(row['T_chip_assumed_C']):10.2f} "
            f"{str(row['Pass_R_total']):>9} "
            f"{str(row['Pass_derated_70C']):>8} "
            f"{str(row['Pass_failure_85C']):>8}"
        )


if __name__ == "__main__":
    result_rows = evaluate_concepts()
    csv_path = write_csv(result_rows)
    print_table(result_rows)
    print(f"\nWrote CSV: {csv_path}")
