from app.services.distance import estimated_walk_minutes, haversine_km


def test_walk_minutes_applies_route_factor():
    assert estimated_walk_minutes(1.0) == 17


def test_haversine_returns_zero_for_same_point():
    assert haversine_km(37.5, 127.0, 37.5, 127.0) == 0


def test_haversine_is_symmetric():
    first = haversine_km(37.5, 127.0, 37.6, 127.1)
    second = haversine_km(37.6, 127.1, 37.5, 127.0)
    assert round(first, 6) == round(second, 6)
