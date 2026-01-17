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

