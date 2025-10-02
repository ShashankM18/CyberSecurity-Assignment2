"""Benchmark core operations: trust updates, blockchain adds, isolation actions."""
import time, json, argparse, os
from multi_agent_trust.trust_sim import TrustManager
from blockchain_ledger.simple_chain import SimpleChain
from dynamic_isolation.manager import IsolationManager

def bench_trust_updates(n_ops=1000):
    tm = TrustManager()
    agents = [tm.register(f'a{i}') for i in range(10)]
    start = time.time()
    for i in range(n_ops):
        a = agents[i % len(agents)]
        a_id = a.agent_id
        action = 'exfiltrate:secret' if (i % 10 == 0) else 'request_info:general'
        tm.observe(a_id, action)
    end = time.time()
    return {'ops': n_ops, 'time': end-start, 'ops_per_sec': n_ops/(end-start)}

def bench_blockchain(n_blocks=100, difficulty=2):
    chain = SimpleChain(difficulty=difficulty)
    start = time.time()
    for i in range(n_blocks):
        chain.add_block({'event':f'block_{i}'})
    end = time.time()
    return {'blocks': n_blocks, 'time': end-start, 'blocks_per_sec': n_blocks/(end-start), 'valid': chain.is_valid()}

def bench_isolation(n_ops=100):
    chain = SimpleChain(difficulty=2)
    im = IsolationManager(chain)
    start = time.time()
    for i in range(n_ops):
        im.isolate(f'a{i}', 'auto-detect')
        if i % 3 == 0:
            im.release(f'a{i}', 'timeout')
    end = time.time()
    return {'ops': n_ops, 'time': end-start, 'ops_per_sec': n_ops/(end-start)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='results/benchmarks.json')
    parser.add_argument('--trust-ops', type=int, default=1000)
    parser.add_argument('--block-n', type=int, default=100)
    parser.add_argument('--iso-ops', type=int, default=200)
    args = parser.parse_args()
    out = {}
    out['trust'] = bench_trust_updates(args.trust_ops)
    out['blockchain'] = bench_blockchain(args.block_n)
    out['isolation'] = bench_isolation(args.iso_ops)
    # Ensure the output directory exists if a nested path is provided.
    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    with open(args.out, 'w') as f:
        json.dump(out, f, indent=2)
    print('Wrote benchmarks to', args.out)

if __name__ == '__main__':
    main()
