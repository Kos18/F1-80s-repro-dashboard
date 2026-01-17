# Formula 1 (1980–1989) — Reproducible Analytics Dashboard

An interactive Streamlit dashboard that computes F1 season standings (drivers + constructors), visualizes points with charts, and supports reproducible “what-if” scenarios.

This repository is designed to be **fully reproducible**:
- **Fixed environment** using Docker
- **Deterministic dataset** (generated with a fixed seed)
- **Deterministic computations** (stable sorting + fixed points system)
- **One-command run** for the app and tests

---

## Requirements
- Docker (Docker Desktop on macOS/Windows, Docker Engine on Linux)

---

## Quick start (recommended)

### 1) Build the Docker image
```bash
docker build -t f1-dashboard .

### 2) Run unit tests (reproducibility check)
```bash
docker run --rm f1-dashboard pytest -q

- **Expected outcome "1 passed"

### 3) Run the dashboard localy
```bash
docker run --rm -p 8501:8501 f1-dashboard

- **Open your browser at "http://localhost:8501"- copying and pasting from the outcome of point 2

---

## Project structure

.
├── app/        # Streamlit user interface
├── src/        # Core logic (data loading, standings, scenarios)
├── data/       # Fixed reproducible datasets
├── scripts/    # Deterministic data generation scripts (optional)
├── tests/      # Unit tests
├── Dockerfile
├── requirements.txt
└── README.md

---

## Data description

- **data/races.csv — Races from 1980 to 1989 (5 races per year)

- **data/results.csv — Top 6 classified drivers per race

- **data/points.json — Points system (top 6)

- **data/scenarios.json — One reproducible scenario per season

