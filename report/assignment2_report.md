# Assignment 2 — Report

**Paper:** Transforming cybersecurity with agentic AI to combat emerging cyber threats (selected).

## Abstract
This assignment implements toy prototypes addressing gaps found in the paper: lack of empirical / prototype defenses for agentic-AI prompt-injection and lack of quantitative evaluation. The repo provides a trust simulation, toy blockchain ledger for audit, a dynamic isolation manager, benchmarking scripts, example runs, and documentation.

## Identified gaps
1. No prototype defenses demonstrating practical mitigations.
2. Lack of quantitative benchmarks for proposed mitigations.
3. No operational guidance or reproducible experiments.

## Contributions
- Multi-agent trust simulation with automatic isolation when trust falls below threshold.
- Toy blockchain ledger to record isolation and audit events.
- Dynamic isolation manager that records actions to the ledger.
- Benchmark scripts to measure throughput/latency of core operations.
- Documentation and example runs for reproducibility.

## Methodology
- Simulate agents, update trust based on observed actions (rule-based).
- Record isolate/release events to the toy blockchain for tamper-evident audit.
- Benchmark trust updates, block creation, and isolation operations.

## Results
Run `examples/run_all.py` and `benchmark/run_benchmarks.py` locally to produce the results files under `results/` and screenshots for submission.

## Future work
- Use real telemetry and ML-based trust scoring.
- Replace toy ledger with a signed multi-node ledger and consensus.
- Integrate with container-level isolation.
