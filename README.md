# Assignment 2 — Cybersecurity Prototype

This project demonstrates a simple end-to-end security prototype:
- A trust model that updates agent trust scores based on actions.
- Dynamic isolation and release of agents when needed.
- A minimal blockchain ledger to record isolation/release actions.
- Benchmarks and a web dashboard to visualize and control everything.

## Features
- **Trust**: `multi_agent_trust/trust_sim.py` updates trust toward 1.0 for benign actions and toward 0.0 for malicious ones, with a small decay per observation.
- **Blockchain**: `blockchain_ledger/simple_chain.py` appends blocks with a tiny proof-of-work simulation and integrity checks via `is_valid()`.
- **Isolation**: `dynamic_isolation/manager.py` isolates/releases agents and logs each event to the blockchain.
- **Benchmarks**: `benchmark/run_benchmarks.py` measures throughput for trust updates, block creation, and isolation.
- **Web UI**: `webapp/app.py` (Flask) serves a dashboard to view agents, trigger isolation/release, see the ledger, and run benchmarks.

## Project Structure
- `multi_agent_trust/` — trust logic (`trust_sim.py`)
- `blockchain_ledger/` — blockchain (`simple_chain.py`)
- `dynamic_isolation/` — isolation manager (`manager.py`)
- `benchmark/` — CLI benchmarks (`run_benchmarks.py`)
- `webapp/` — Flask app (`app.py`, `templates/index.html`, `static/main.js`)
- `tests/` — sample test (`test_trust.py`)
- `results/` — benchmark outputs
- `requirements.txt` — dependencies (Flask for the web UI)

## Prerequisites
- Python 3.10+ (tested with 3.12)
- Windows PowerShell examples below (adjust for macOS/Linux as needed)

## Setup
```
# From project root
python -m venv venv
./venv/Scripts/Activate.ps1
python -m pip install -U pip -r requirements.txt
```

## Run the Web UI (Dashboard)
```
# From project root
python webapp/app.py
```
Open http://127.0.0.1:5000

Dashboard capabilities:
- View agents and live trust scores.
- Send benign/malicious actions to update trust.
- Isolate/Release agents (writes blocks to the ledger).
- View blockchain entries and validity.
- Run benchmarks and view results JSON.

## Run Benchmarks (CLI)
Recommended: module mode to ensure imports work from project root.
```
python -m benchmark.run_benchmarks --out results/benchmarks.json
Type ./results/benchmarks.json
```
Custom options:
```
python -m benchmark.run_benchmarks --trust-ops 2000 --block-n 300 --iso-ops 500 --out results/bench_custom.json
```

## Run Tests (optional)
```
python -m pip install -U pytest
python -m pytest -q
```

## Troubleshooting
- If you see `ModuleNotFoundError` when running by path, run modules instead:
  - Web: `python -m webapp.app`
  - Benchmarks: `python -m benchmark.run_benchmarks`
- The web app already adjusts `sys.path` for direct execution.
- The blockchain’s proof-of-work gets slower with higher `difficulty`.

# Trust, Isolation, and Blockchain — Toy Prototype

This project demonstrates a simple end-to-end security prototype:
- A trust model that updates agent trust scores based on actions.
- Dynamic isolation and release of agents when needed.
- A minimal blockchain ledger to record isolation/release actions.
- Benchmarks and a web dashboard to visualize and control everything.

These are educational, simplified components intended for learning and demos.

## Features
- **Trust**: `multi_agent_trust/trust_sim.py` updates trust toward 1.0 for benign actions and toward 0.0 for malicious ones, with a small decay per observation.
- **Blockchain**: `blockchain_ledger/simple_chain.py` appends blocks with a tiny proof-of-work simulation and integrity checks via `is_valid()`.
- **Isolation**: `dynamic_isolation/manager.py` isolates/releases agents and logs each event to the blockchain.
- **Benchmarks**: `benchmark/run_benchmarks.py` measures throughput for trust updates, block creation, and isolation.
- **Web UI**: `webapp/app.py` (Flask) serves a dashboard to view agents, trigger isolation/release, see the ledger, and run benchmarks.

## Project Structure
- `multi_agent_trust/` — trust logic (`trust_sim.py`)
- `blockchain_ledger/` — blockchain (`simple_chain.py`)
- `dynamic_isolation/` — isolation manager (`manager.py`)
- `benchmark/` — CLI benchmarks (`run_benchmarks.py`)
- `webapp/` — Flask app (`app.py`, `templates/index.html`, `static/main.js`)
- `tests/` — sample test (`test_trust.py`)
- `results/` — benchmark outputs
- `requirements.txt` — dependencies (Flask for the web UI)

## Prerequisites
- Python 3.10+ (tested with 3.12)
- Windows PowerShell examples below (adjust for macOS/Linux as needed)

## Setup
```
# From project root
python -m venv venv
./venv/Scripts/Activate.ps1
python -m pip install -U pip -r requirements.txt
```

## Run the Web UI (Dashboard)
```
# From project root
python webapp/app.py
```
Open http://127.0.0.1:5000

Dashboard capabilities:
- View agents and live trust scores.
- Send benign/malicious actions to update trust.
- Isolate/Release agents (writes blocks to the ledger).
- View blockchain entries and validity.
- Run benchmarks and view results JSON.

## Run Benchmarks (CLI)
Recommended: module mode to ensure imports work from project root.
```
python -m benchmark.run_benchmarks --out results/benchmarks.json
Type ./results/benchmarks.json
```
Custom options:
```
python -m benchmark.run_benchmarks --trust-ops 2000 --block-n 300 --iso-ops 500 --out results/bench_custom.json
```

## Run Tests (optional)
```
python -m pip install -U pytest
python -m pytest -q
```

## Troubleshooting
- If you see `ModuleNotFoundError` when running by path, run modules instead:
  - Web: `python -m webapp.app`
  - Benchmarks: `python -m benchmark.run_benchmarks`
- The web app already adjusts `sys.path` for direct execution.
- The blockchain’s proof-of-work gets slower with higher `difficulty`.

