from src.data_loader import load_races, load_results, load_points
from src.standings import compute_driver_standings

def test_driver_standings_deterministic():
    races = load_races("data/races.csv")
    results = load_results("data/results.csv")
    points_map = load_points("data/points.json")

    year = 1988
    year_race_ids = {r.race_id for r in races if r.year == year}

    s1 = compute_driver_standings(results, points_map, year_race_ids)
    s2 = compute_driver_standings(results, points_map, year_race_ids)

    assert [(x.driver, x.points, x.wins) for x in s1] == [(x.driver, x.points, x.wins) for x in s2]
