# Design notes and documentation

## Overview
This repository contains toy/prototype implementations to demonstrate possible practical mitigations
and infrastructure to address gaps identified in the selected cybersecurity paper (agentic AI risks).

Modules:
- multi_agent_trust: simple trust model to simulate agent behaviour and dynamic trust updates.
- blockchain_ledger: toy ledger for auditability of actions (isolate/release/trust-events).
- dynamic_isolation: simulated isolation manager which records isolations to the ledger.
- benchmark: measures performance and throughput of operations for reporting.

## How components interact
- The TrustManager observes agent actions and updates trust scores.
- When trust falls below a threshold, the IsolationManager can isolate the agent and records this action on the blockchain ledger.
- The blockchain ledger provides tamper-evident storage for isolation events and can be verified by auditors.

## Limitations
- The blockchain is a toy PoW-like chain and is not secure for any production usage.
- Trust updates are simplistic and intended for demonstration. Real trust systems should use richer telemetry, ML models, and provenance.
- Isolation is simulated and does not perform real container or network isolation.

## Extension ideas
- Replace trust update heuristics with a learned model and features from real telemetry.
- Use real cryptographic signatures for blocks and a network of nodes to simulate consensus.
- Integrate with container runtimes (Docker) or orchestration for real isolation actions.
- Add role-based access control and certificate-based verification.
