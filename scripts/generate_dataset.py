from __future__ import annotations
import csv
import random
from pathlib import Path

YEARS = list(range(1980, 1990))  # 1980..1990 inclusive
RACES_PER_YEAR = 5

# A curated pool of famous-ish race names (re-used across years is fine)
RACE_POOL = [
    ("Brazilian Grand Prix", "Interlagos", "Brazil"),
    ("Monaco Grand Prix", "Monte Carlo", "Monaco"),
    ("British Grand Prix", "Silverstone", "United Kingdom"),
    ("Italian Grand Prix", "Monza", "Italy"),
    ("Japanese Grand Prix", "Suzuka", "Japan"),
    ("Canadian Grand Prix", "Montreal", "Canada"),
    ("German Grand Prix", "Hockenheim", "Germany"),
    ("Belgian Grand Prix", "Spa-Francorchamps", "Belgium"),
    ("Spanish Grand Prix", "Jerez", "Spain"),
    ("Australian Grand Prix", "Adelaide", "Australia"),
    ("San Marino Grand Prix", "Imola", "Italy"),
    ("Hungarian Grand Prix", "Hungaroring", "Hungary"),
]

# A small driver/team pool (you can edit names freely)
DRIVERS_TEAMS = [
    ("Ayrton Senna", "McLaren"),
    ("Alain Prost", "McLaren"),
    ("Nigel Mansell", "Williams"),
    ("Nelson Piquet", "Williams"),
    ("Gerhard Berger", "Ferrari"),
    ("Michele Alboreto", "Ferrari"),
    ("Keke Rosberg", "Williams"),
    ("Niki Lauda", "McLaren"),
    ("Riccardo Patrese", "Brabham"),
    ("Teo Fabi", "Benetton"),
    ("Derek Warwick", "Lotus"),
    ("Thierry Boutsen", "Benetton"),
    ("Stefan Johansson", "Ferrari"),
    ("Eddie Cheever", "Alfa Romeo"),
    ("Elio de Angelis", "Lotus"),
    ("John Watson", "McLaren"),
]

SEED = 19801234  # fixed seed => deterministic output

def main() -> None:
    random.seed(SEED)

    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)

    races_path = out_dir / "races.csv"
    results_path = out_dir / "results.csv"

    # Build races: 5 per year, pick distinct names per year
    races_rows = []
    for year in YEARS:
        picked = random.sample(RACE_POOL, k=RACES_PER_YEAR)
        for rnd, (name, circuit, country) in enumerate(picked, start=1):
            race_id = f"{year}_{rnd:02d}"
            races_rows.append({
                "race_id": race_id,
                "year": year,
                "round": rnd,
                "race_name": name,
                "circuit": circuit,
                "country": country,
            })

    # Build results: top 6 per race
    results_rows = []
    for r in races_rows:
        # pick 10 drivers for grid, then choose finishing order top 6
        grid_pool = random.sample(DRIVERS_TEAMS, k=10)
        # assign grid positions 1..10
        grid_assigned = list(enumerate(grid_pool, start=1))
        # choose top 6 finishers from those 10
        finishers = random.sample(grid_assigned, k=6)
        # order them by finishing position 1..6 deterministically (shuffle -> then sort by random key)
        # to keep deterministic but "race-like", we sort by a generated random score
        ranked = sorted(finishers, key=lambda _: random.random())

        for pos, (grid_pos, (driver, team)) in enumerate(ranked, start=1):
            results_rows.append({
                "race_id": r["race_id"],
                "driver": driver,
                "team": team,
                "grid": grid_pos,
                "position": pos,
                "status": "Finished",
            })

    # Write CSVs
    with races_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["race_id", "year", "round", "race_name", "circuit", "country"])
        w.writeheader()
        w.writerows(races_rows)

    with results_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["race_id", "driver", "team", "grid", "position", "status"])
        w.writeheader()
        w.writerows(results_rows)

    print(f"Wrote {len(races_rows)} races to {races_path}")
    print(f"Wrote {len(results_rows)} results to {results_path}")

if __name__ == "__main__":
    main()

