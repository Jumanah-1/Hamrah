def calculate_road_risk(
    rain_6h_mm,
    slope_percent,
    upstream_area_km2,
    impervious_fraction,
    is_tunnel
):
    """
    Calculate a preliminary road flood-exposure index.
    Returns a score from 0 to 100.
    """

    # Validate inputs
    if (
        rain_6h_mm < 0
        or slope_percent < 0
        or upstream_area_km2 < 0
        or not 0 <= impervious_fraction <= 1
    ):
        raise ValueError("Invalid risk model inputs")

    # Normalize the factors between 0 and 1
    rain_factor = min(rain_6h_mm / 60, 1)

    flatness_factor = 1 - min(slope_percent / 8, 1)

    upstream_factor = min(upstream_area_km2 / 2, 1)

    surface_factor = impervious_fraction

    tunnel_factor = 1 if is_tunnel else 0

    # Preliminary road vulnerability
    vulnerability = (
        0.25 * flatness_factor
        + 0.25 * upstream_factor
        + 0.25 * surface_factor
        + 0.25 * tunnel_factor
    )

    # Rainfall-dependent risk score
    risk_score = round(
        100 * rain_factor * (0.45 + 0.55 * vulnerability),
        1
    )

    # Risk classification
    if risk_score < 30:
        risk_level = "low"
    elif risk_score < 60:
        risk_level = "medium"
    else:
        risk_level = "high"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level
    }