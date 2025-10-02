"""Example script that runs a small simulation end-to-end and prints outcomes.
Generates agents, simulates interactions, triggers isolations based on trust threshold,
and records events into the toy blockchain."""
from multi_agent_trust.trust_sim import TrustManager
from blockchain_ledger.simple_chain import SimpleChain
from dynamic_isolation.manager import IsolationManager
import time, json, random, os

def main():
    chain = SimpleChain(difficulty=2)
    tm = TrustManager()
    im = IsolationManager(chain)

    agents = [tm.register(f'agent_{i}') for i in range(5)]
    print('Registered agents:', [a.agent_id for a in agents])

    for step in range(200):
        a = random.choice(agents)
        behavior = 'malicious' if random.random() < 0.08 else 'benign'
        action = a.act(behavior)
        mal = tm.observe(a.agent_id, action)
        if tm.get_trust(a.agent_id) < 0.3 and not im.is_isolated(a.agent_id):
            blk = im.isolate(a.agent_id, 'low_trust_auto')
            print(f'Isolated {a.agent_id} at step {step}, block_index={blk.index}')
    print('Final trust summary:', tm.summary())
    print('Blockchain valid?', chain.is_valid())
    os.makedirs('results', exist_ok=True)
    with open('results/chain.json', 'w') as f:
        json.dump(chain.to_dict(), f, indent=2)
    print('Saved blockchain to results/chain.json')

if __name__ == '__main__':
    main()
