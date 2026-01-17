from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple
from src.data_loader import Result

@dataclass(frozen=True)
class DriverStanding:
    driver: str
    points: int
    wins: int

def _points_for_position(position: int, points: Dict[str, int]) -> int:
    return points.get(str(position), 0)

def compute_driver_standings(
    results: Iterable[Result],
    points: Dict[str, int],
    race_ids: set[str],
) -> List[DriverStanding]:

    acc: Dict[str, Dict[str, int]] = {}

    for r in results:
        if r.race_id not in race_ids:
            continue
        pts = _points_for_position(r.position, points)
        d = acc.setdefault(r.driver, {"points": 0, "wins": 0})
        d["points"] += pts
        if r.position == 1:
            d["wins"] += 1

    standings = [
        DriverStanding(driver=k, points=v["points"], wins=v["wins"])
        for k, v in acc.items()
    ]

    standings.sort(key=lambda x: (-x.points, -x.wins, x.driver))
    return standings

def compute_constructor_points(
    results: Iterable[Result],
    points: Dict[str, int],
    race_ids: set[str],
) -> List[Tuple[str, int]]:
    acc: Dict[str, int] = {}
    for r in results:
        if r.race_id not in race_ids:
            continue
        acc[r.team] = acc.get(r.team, 0) + _points_for_position(r.position, points)
    return sorted(acc.items(), key=lambda x: (-x[1], x[0]))

