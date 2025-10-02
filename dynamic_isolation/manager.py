"""Dynamic isolation manager (toy simulator)
Simulates isolating agents/tasks by changing state, recording actions to the blockchain ledger.
"""
import time
from blockchain_ledger.simple_chain import SimpleChain

class IsolationManager:
    def __init__(self, chain: SimpleChain):
        self.chain = chain
        self.isolated = {}  # agent_id -> timestamp

    def isolate(self, agent_id: str, reason: str):
        ts = time.time()
        self.isolated[agent_id] = ts
        block = self.chain.add_block({'action':'isolate', 'agent':agent_id, 'reason':reason, 'time':ts})
        return block

    def release(self, agent_id: str, reason: str):
        ts = time.time()
        if agent_id in self.isolated:
            del self.isolated[agent_id]
        block = self.chain.add_block({'action':'release', 'agent':agent_id, 'reason':reason, 'time':ts})
        return block

    def is_isolated(self, agent_id: str) -> bool:
        return agent_id in self.isolated
