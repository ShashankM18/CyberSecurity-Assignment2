"""Toy blockchain ledger for auditability and verification.
Not secure for production. Demonstrates block creation, simple proof-of-work,
and verification of chain integrity for logging actions (e.g., isolations, trust updates).
"""
import hashlib, json, time
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Block:
    index: int
    timestamp: float
    data: dict
    prev_hash: str
    nonce: int = 0
    hash: str = ''

    def compute_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'prev_hash': self.prev_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class SimpleChain:
    def __init__(self, difficulty=2):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.create_genesis()

    def create_genesis(self):
        genesis = Block(0, time.time(), {'msg':'genesis'}, '0')
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def latest_block(self):
        return self.chain[-1]

    def add_block(self, data: dict):
        prev = self.latest_block()
        new_block = Block(prev.index + 1, time.time(), data, prev.hash)
        computed = new_block.compute_hash()
        attempts = 0
        target_prefix = '0' * self.difficulty
        while not computed.startswith(target_prefix) and attempts < 20000:
            new_block.nonce += 1
            computed = new_block.compute_hash()
            attempts += 1
        new_block.hash = computed
        self.chain.append(new_block)
        return new_block

    def is_valid(self):
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i-1]
            if cur.prev_hash != prev.hash:
                return False
            if cur.compute_hash() != cur.hash:
                return False
        return True

    def to_dict(self):
        return [asdict(b) for b in self.chain]
