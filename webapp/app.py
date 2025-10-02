from flask import Flask, jsonify, request, render_template
from threading import Lock
import time
import os, sys

# Ensure project root is on sys.path when running this file directly
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from multi_agent_trust.trust_sim import TrustManager
from blockchain_ledger.simple_chain import SimpleChain
from dynamic_isolation.manager import IsolationManager

# Optional import of benchmark helpers
try:
    from benchmark.run_benchmarks import bench_trust_updates, bench_blockchain, bench_isolation
except Exception:
    bench_trust_updates = bench_blockchain = bench_isolation = None

app = Flask(__name__, template_folder="templates", static_folder="static")

# Shared state
_state_lock = Lock()
chain = SimpleChain(difficulty=2)
isolation = IsolationManager(chain)
trust = TrustManager()

# Seed a few agents
for i in range(5):
    trust.register(f"a{i}")


def _ensure_agent(agent_id: str):
    if agent_id not in trust.agents:
        trust.register(agent_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/agents", methods=["GET"])  # View agents & trust
def api_agents():
    with _state_lock:
        agents = []
        for aid, a in trust.agents.items():
            agents.append({
                "agent_id": aid,
                "trust": a.trust,
                "isolated": isolation.is_isolated(aid)
            })
        return jsonify({"agents": agents, "ts": time.time()})


@app.route("/api/observe", methods=["POST"])  # Update trust via action
def api_observe():
    data = request.get_json(force=True)
    agent_id = data.get("agent_id")
    action = data.get("action", "request_info:general")
    if not agent_id:
        return jsonify({"error": "agent_id required"}), 400
    with _state_lock:
        _ensure_agent(agent_id)
        label = trust.observe(agent_id, action)
        return jsonify({
            "agent_id": agent_id,
            "action": action,
            "malicious": bool(label),
            "trust": trust.get_trust(agent_id)
        })


@app.route("/api/isolate", methods=["POST"])  # Trigger isolation
def api_isolate():
    data = request.get_json(force=True)
    agent_id = data.get("agent_id")
    reason = data.get("reason", "manual")
    if not agent_id:
        return jsonify({"error": "agent_id required"}), 400
    with _state_lock:
        _ensure_agent(agent_id)
        block = isolation.isolate(agent_id, reason)
        return jsonify({"ok": True, "block": block.__dict__})


@app.route("/api/release", methods=["POST"])  # Release isolation
def api_release():
    data = request.get_json(force=True)
    agent_id = data.get("agent_id")
    reason = data.get("reason", "manual")
    if not agent_id:
        return jsonify({"error": "agent_id required"}), 400
    with _state_lock:
        block = isolation.release(agent_id, reason)
        return jsonify({"ok": True, "block": block.__dict__})


@app.route("/api/ledger", methods=["GET"])  # View blockchain entries
def api_ledger():
    with _state_lock:
        return jsonify({"chain": chain.to_dict(), "valid": chain.is_valid(), "length": len(chain.chain)})


@app.route("/api/benchmark", methods=["POST"])  # Run benchmarks
def api_benchmark():
    params = request.get_json(force=True) or {}
    trust_ops = int(params.get("trust_ops", 500))
    blocks = int(params.get("blocks", 50))
    difficulty = int(params.get("difficulty", 2))
    iso_ops = int(params.get("iso_ops", 100))

    # Fallback if import failed: provide minimal inline benchmarks
    def _bench_trust_fallback(n):
        tm = TrustManager()
        agents = [tm.register(f"b{i}") for i in range(10)]
        t0 = time.time()
        for i in range(n):
            a = agents[i % len(agents)]
            action = 'exfiltrate:secret' if (i % 10 == 0) else 'request_info:general'
            tm.observe(a.agent_id, action)
        t1 = time.time()
        return {"ops": n, "time": t1 - t0, "ops_per_sec": n / max(1e-9, (t1 - t0))}

    def _bench_chain_fallback(n, diff):
        ch = SimpleChain(difficulty=diff)
        t0 = time.time()
        for i in range(n):
            ch.add_block({"event": f"block_{i}"})
        t1 = time.time()
        return {"blocks": n, "time": t1 - t0, "blocks_per_sec": n / max(1e-9, (t1 - t0)), "valid": ch.is_valid()}

    def _bench_iso_fallback(n):
        ch = SimpleChain(difficulty=2)
        im = IsolationManager(ch)
        t0 = time.time()
        for i in range(n):
            im.isolate(f"x{i}", "auto")
            if i % 3 == 0:
                im.release(f"x{i}", "timeout")
        t1 = time.time()
        return {"ops": n, "time": t1 - t0, "ops_per_sec": n / max(1e-9, (t1 - t0))}

    results = {
        "trust": (bench_trust_updates(trust_ops) if bench_trust_updates else _bench_trust_fallback(trust_ops)),
        "blockchain": (bench_blockchain(blocks, difficulty) if bench_blockchain else _bench_chain_fallback(blocks, difficulty)),
        "isolation": (bench_isolation(iso_ops) if bench_isolation else _bench_iso_fallback(iso_ops))
    }
    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
