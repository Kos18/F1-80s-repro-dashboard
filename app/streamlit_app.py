import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

from src.data_loader import load_races, load_results, load_points
from src.standings import compute_driver_standings, compute_constructor_points
from src.scenario import load_scenarios, apply_scenario

@st.cache_data
def load_all():
    return (
        load_races("data/races.csv"),
        load_results("data/results.csv"),
        load_points("data/points.json"),
        load_scenarios("data/scenarios.json"),
    )

races, results, points, scenarios = load_all()

st.title("Formula 1 1980–1989: Standings, Scenarios & Analytics")

years = sorted({r.year for r in races})
year = st.sidebar.selectbox("Season", years)

year_race_ids = {r.race_id for r in races if r.year == year}

scenario_name = st.sidebar.selectbox(
    "Scenario", ["None"] + [s["name"] for s in scenarios]
)

active_results = results
if scenario_name != "None":
    s = next(x for x in scenarios if x["name"] == scenario_name)
    active_results = apply_scenario(results, s)

drivers = compute_driver_standings(active_results, points, year_race_ids)
constructors = compute_constructor_points(active_results, points, year_race_ids)

# --- Summary cards ---
c1, c2, c3 = st.columns(3)
c1.metric("Races in season", len(year_race_ids))
c2.metric("Champion", drivers[0].driver if drivers else "N/A")
c3.metric("Champion points", drivers[0].points if drivers else 0)

# --- Bar chart: Top 10 drivers ---
st.subheader("Top drivers (points)")
df_dr = pd.DataFrame([{"driver": d.driver, "points": d.points, "wins": d.wins} for d in drivers])
if not df_dr.empty:
    st.bar_chart(df_dr.head(10).set_index("driver")["points"])

# --- Bar chart: Constructors ---
st.subheader("Constructors (points)")
df_con = pd.DataFrame(constructors, columns=["team", "points"])
if not df_con.empty:
    st.bar_chart(df_con.set_index("team")["points"])

# --- Line chart: points per round (Top 5 drivers) ---
st.subheader("Points progression by round (Top 5 drivers)")
races_year = [r for r in races if r.year == year]
races_year = sorted(races_year, key=lambda x: x.round)

rows = []
for rr in races_year:
    race_res = [x for x in active_results if x.race_id == rr.race_id]
    for res in race_res:
        rows.append({
            "round": rr.round,
            "driver": res.driver,
            "points": points.get(str(res.position), 0)
        })

df_round = pd.DataFrame(rows)
if not df_round.empty:
    pivot = df_round.pivot_table(index="round", columns="driver", values="points", aggfunc="sum").fillna(0)
    top5 = pivot.sum(axis=0).sort_values(ascending=False).head(5).index
    st.line_chart(pivot[top5].cumsum())


st.subheader("Driver Standings")
st.dataframe(pd.DataFrame(drivers).reset_index(drop=True))

st.subheader("Constructor Standings")
st.dataframe(pd.DataFrame(constructors, columns=["Team", "Points"]))

st.subheader("Results")
df = pd.DataFrame([r.__dict__ for r in active_results if r.race_id in year_race_ids])
st.dataframe(df.reset_index(drop=True))

