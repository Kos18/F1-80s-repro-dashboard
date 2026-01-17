from dataclasses import dataclass
import csv
import json
from typing import Dict, List

@dataclass(frozen=True)
class Race:
    race_id: str
    year: int
    round: int
    race_name: str
    circuit: str
    country: str

@dataclass(frozen=True)
class Result:
    race_id: str
    driver: str
    team: str
    grid: int
    position: int
    status: str

def load_races(path: str) -> List[Race]:
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append(Race(
                race_id=r["race_id"],
                year=int(r["year"]),
                round=int(r["round"]),
                race_name=r["race_name"],
                circuit=r["circuit"],
                country=r["country"],
            ))
    return out

def load_results(path: str) -> List[Result]:
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append(Result(
                race_id=r["race_id"],
                driver=r["driver"],
                team=r["team"],
                grid=int(r["grid"]),
                position=int(r["position"]),
                status=r["status"],
            ))
    return out

def load_points(path: str) -> Dict[str, int]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

