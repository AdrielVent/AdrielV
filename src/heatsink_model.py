"""Heat sink thermal model helpers for ENGG 114 Project B.

All calculations use SI units only.
Project target constants are provided for convenience, but geometric design
variables are intentionally left unspecified.
"""

from __future__ import annotations

import math

# Project target (fixed by assignment).
CHIP_LENGTH_M = 50.8e-3  # [m]
CHIP_WIDTH_M = 50.8e-3  # [m]
HEAT_LOAD_W = 100.0  # [W]
AMBIENT_AIR_C = 25.0  # [degC]
FAILURE_LIMIT_C = 85.0  # [degC]
DERATED_TARGET_C = 70.0  # [degC]
ALLOWABLE_TOTAL_THERMAL_RESISTANCE_C_PER_W = 0.45  # [degC/W]


def _require_positive(value: float, name: str) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0. Received {value}.")


def _require_non_negative(value: float, name: str) -> None:
    if value < 0.0:
        raise ValueError(f"{name} must be >= 0. Received {value}.")


def base_conduction_resistance(length_m: float, conductivity_w_per_mk: float, area_m2: float) -> float:
    """Compute base conduction thermal resistance: R = L/(kA).

    Args:
        length_m: Conduction path length, L [m].
        conductivity_w_per_mk: Material thermal conductivity, k [W/(m*K)].
        area_m2: Cross-sectional area normal to heat flow, A [m^2].
    """
    _require_positive(length_m, "length_m")
    _require_positive(conductivity_w_per_mk, "conductivity_w_per_mk")
    _require_positive(area_m2, "area_m2")
    return length_m / (conductivity_w_per_mk * area_m2)


def contact_resistance(thickness_m: float, conductivity_w_per_mk: float, area_m2: float) -> float:
    """Compute contact/interface thermal resistance: R = t/(kA).

    Args:
        thickness_m: Interface thickness, t [m].
        conductivity_w_per_mk: Interface conductivity, k [W/(m*K)].
        area_m2: Contact area, A [m^2].
    """
    _require_non_negative(thickness_m, "thickness_m")
    _require_positive(conductivity_w_per_mk, "conductivity_w_per_mk")
    _require_positive(area_m2, "area_m2")
    return thickness_m / (conductivity_w_per_mk * area_m2)


def hydraulic_diameter(flow_area_m2: float, wetted_perimeter_m: float) -> float:
    """Compute hydraulic diameter: D_h = 4*A_flow/P_wetted.

    Args:
        flow_area_m2: Flow cross-sectional area, A_flow [m^2].
        wetted_perimeter_m: Wetted perimeter, P_wetted [m].
    """
    _require_positive(flow_area_m2, "flow_area_m2")
    _require_positive(wetted_perimeter_m, "wetted_perimeter_m")
    return 4.0 * flow_area_m2 / wetted_perimeter_m


def reynolds_number(
    density_kg_per_m3: float,
    velocity_m_per_s: float,
    hydraulic_diameter_m: float,
    dynamic_viscosity_pa_s: float,
) -> float:
    """Compute Reynolds number: Re = rho*v*D_h/mu.

    Args:
        density_kg_per_m3: Fluid density, rho [kg/m^3].
        velocity_m_per_s: Bulk flow velocity, v [m/s].
        hydraulic_diameter_m: Hydraulic diameter, D_h [m].
        dynamic_viscosity_pa_s: Dynamic viscosity, mu [Pa*s].
    """
    _require_positive(density_kg_per_m3, "density_kg_per_m3")
    _require_non_negative(velocity_m_per_s, "velocity_m_per_s")
    _require_positive(hydraulic_diameter_m, "hydraulic_diameter_m")
    _require_positive(dynamic_viscosity_pa_s, "dynamic_viscosity_pa_s")
    return density_kg_per_m3 * velocity_m_per_s * hydraulic_diameter_m / dynamic_viscosity_pa_s


def nusselt_number(reynolds: float, prandtl: float, regime: str = "auto") -> float:
    """Compute Nusselt number.

    Laminar placeholder for parallel plates at constant heat flux: Nu = 7.54.
    Turbulent relation (Dittus-Boelter form): Nu = 0.023*Re^0.8*Pr^0.4.

    Args:
        reynolds: Reynolds number, Re [-].
        prandtl: Prandtl number, Pr [-].
        regime: "laminar", "turbulent", or "auto".
    """
    _require_non_negative(reynolds, "reynolds")
    _require_positive(prandtl, "prandtl")

    if regime not in {"auto", "laminar", "turbulent"}:
        raise ValueError("regime must be one of: 'auto', 'laminar', 'turbulent'.")

    selected = regime
    if regime == "auto":
        selected = "laminar" if reynolds < 2300.0 else "turbulent"

    if selected == "laminar":
        return 7.54

    # Turbulent correlation is not physically meaningful at Re <= 0.
    _require_positive(reynolds, "reynolds")
    return 0.023 * (reynolds ** 0.8) * (prandtl ** 0.4)


def convection_coefficient(nusselt: float, air_conductivity_w_per_mk: float, hydraulic_diameter_m: float) -> float:
    """Compute convection coefficient: h = Nu*k_air/D_h.

    Args:
        nusselt: Nusselt number, Nu [-].
        air_conductivity_w_per_mk: Air thermal conductivity, k_air [W/(m*K)].
        hydraulic_diameter_m: Hydraulic diameter, D_h [m].
    """
    _require_non_negative(nusselt, "nusselt")
    _require_positive(air_conductivity_w_per_mk, "air_conductivity_w_per_mk")
    _require_positive(hydraulic_diameter_m, "hydraulic_diameter_m")
    return nusselt * air_conductivity_w_per_mk / hydraulic_diameter_m


def rectangular_fin_efficiency(
    h_w_per_m2k: float,
    fin_conductivity_w_per_mk: float,
    fin_thickness_m: float,
    fin_length_m: float,
) -> float:
    """Compute rectangular fin efficiency.

    m = sqrt(2h/(k_fin*t_fin))
    L_c = L_fin + t_fin/2
    eta_f = tanh(m*L_c)/(m*L_c)

    Args:
        h_w_per_m2k: Convection coefficient, h [W/(m^2*K)].
        fin_conductivity_w_per_mk: Fin conductivity, k_fin [W/(m*K)].
        fin_thickness_m: Fin thickness, t_fin [m].
        fin_length_m: Fin length/height from base, L_fin [m].
    """
    _require_positive(h_w_per_m2k, "h_w_per_m2k")
    _require_positive(fin_conductivity_w_per_mk, "fin_conductivity_w_per_mk")
    _require_positive(fin_thickness_m, "fin_thickness_m")
    _require_positive(fin_length_m, "fin_length_m")

    m = math.sqrt(2.0 * h_w_per_m2k / (fin_conductivity_w_per_mk * fin_thickness_m))
    corrected_length_m = fin_length_m + fin_thickness_m / 2.0
    argument = m * corrected_length_m

    _require_positive(argument, "m*L_c")
    return math.tanh(argument) / argument


def effective_area(
    num_fins: int,
    fin_length_m: float,
    fin_width_m: float,
    fin_efficiency: float,
    base_exposed_area_m2: float,
) -> float:
    """Compute effective convection area.

    A_eff = N_fins*(2*L_fin*w_fin)*eta_f + A_base_exposed

    Args:
        num_fins: Number of fins, N_fins [-].
        fin_length_m: Fin length/height, L_fin [m].
        fin_width_m: Fin width (span), w_fin [m].
        fin_efficiency: Fin efficiency, eta_f [-].
        base_exposed_area_m2: Base area directly exposed to air, A_base_exposed [m^2].
    """
    if num_fins < 0:
        raise ValueError(f"num_fins must be >= 0. Received {num_fins}.")
    _require_non_negative(fin_length_m, "fin_length_m")
    _require_non_negative(fin_width_m, "fin_width_m")
    _require_non_negative(base_exposed_area_m2, "base_exposed_area_m2")
    if not (0.0 <= fin_efficiency <= 1.0):
        raise ValueError(f"fin_efficiency must be between 0 and 1. Received {fin_efficiency}.")

    fin_area_m2 = num_fins * (2.0 * fin_length_m * fin_width_m)
    return fin_area_m2 * fin_efficiency + base_exposed_area_m2


def convection_resistance(h_w_per_m2k: float, effective_area_m2: float) -> float:
    """Compute convection resistance: R = 1/(h*A_eff).

    Args:
        h_w_per_m2k: Convection coefficient, h [W/(m^2*K)].
        effective_area_m2: Effective area, A_eff [m^2].
    """
    _require_positive(h_w_per_m2k, "h_w_per_m2k")
    _require_positive(effective_area_m2, "effective_area_m2")
    return 1.0 / (h_w_per_m2k * effective_area_m2)


def chip_temperature_c(ambient_c: float, heat_load_w: float, total_thermal_resistance_c_per_w: float) -> float:
    """Compute chip temperature: T = T_ambient + Q*R_total.

    Args:
        ambient_c: Ambient air temperature, T_ambient [degC].
        heat_load_w: Heat load, Q [W].
        total_thermal_resistance_c_per_w: Total thermal resistance, R_total [degC/W].
    """
    _require_non_negative(heat_load_w, "heat_load_w")
    _require_non_negative(total_thermal_resistance_c_per_w, "total_thermal_resistance_c_per_w")
    return ambient_c + heat_load_w * total_thermal_resistance_c_per_w


if __name__ == "__main__":
    # Simple sanity test only. Final heat sink dimensions are intentionally not selected here.
    chip_area_m2 = CHIP_LENGTH_M * CHIP_WIDTH_M
    example_l_base_m = 0.005  # [m]
    example_k_aluminum_w_per_mk = 237.0  # [W/(m*K)]

    chip_temp_at_allowable_c = chip_temperature_c(
        AMBIENT_AIR_C,
        HEAT_LOAD_W,
        ALLOWABLE_TOTAL_THERMAL_RESISTANCE_C_PER_W,
    )
    example_base_r_c_per_w = base_conduction_resistance(
        example_l_base_m,
        example_k_aluminum_w_per_mk,
        chip_area_m2,
    )

    print(f"Chip area (m^2): {chip_area_m2:.8f}")
    print(
        "Allowable total thermal resistance (C/W): "
        f"{ALLOWABLE_TOTAL_THERMAL_RESISTANCE_C_PER_W:.2f}"
    )
    print(f"Chip temperature at R_total = 0.45 C/W (C): {chip_temp_at_allowable_c:.2f}")
    print(
        "Example aluminum base conduction resistance (C/W): "
        f"{example_base_r_c_per_w:.6f}"
    )
