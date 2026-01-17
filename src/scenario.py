import json
from typing import Dict, List
from src.data_loader import Result

def load_scenarios(path: str) -> List[Dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def apply_scenario(results: List[Result], scenario: Dict) -> List[Result]:
    out = []
    for r in results:
        if r.race_id == scenario["race_id"] and r.driver == scenario["driver"]:
            out.append(Result(
                race_id=r.race_id,
                driver=r.driver,
                team=r.team,
                grid=r.grid,
                position=int(scenario["new_position"]),
                status=scenario["new_status"],
            ))
        else:
            out.append(r)
    return out

