from __future__ import annotations

from math import asin, ceil, cos, radians, sin, sqrt


def haversine_km(a_lat: float, a_lon: float, b_lat: float, b_lon: float) -> float:
    dlat = radians(b_lat - a_lat)
    dlon = radians(b_lon - a_lon)
    lat1, lat2 = radians(a_lat), radians(b_lat)
    value = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371 * 2 * asin(sqrt(value))


def estimated_walk_minutes(
    distance_km: float, route_factor: float = 1.25, speed_kmh: float = 4.5
) -> int:
    if distance_km <= 0:
        return 0
    return ceil(distance_km * route_factor / speed_kmh * 60)
