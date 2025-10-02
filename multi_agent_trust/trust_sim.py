"""Multi-agent trust simulation module (toy implementation).
Provides Agent class and TrustManager which updates trust scores based on interactions.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import random
import time

@dataclass
class Agent:
    # Unique identifier for the agent in the system.
    agent_id: str
    # Current trust score in [0.0, 1.0]. Initialized at a neutral 0.5.
    trust: float = 0.5  # initial trust between 0 and 1
    # Interaction history as a list of (timestamp, is_malicious) tuples.
    history: List[Tuple[float, bool]] = field(default_factory=list)

    def act(self, behavior: str = "benign") -> str:
        """Return a textual action.
        behavior options:
        - 'benign': safe information request
        - 'noisy': benign but broader, can touch config
        - 'malicious': attempts to exfiltrate or bypass auth
        """
        if behavior == 'benign':
            return "request_info:general"
        if behavior == 'noisy':
            return random.choice(["request_info:general", "request_info:config"])
        if behavior == 'malicious':
            # Randomly select a malicious action from the set of possible actions.
            return random.choice(["exfiltrate:secret", "bypass_auth:token"])
        return "request_info:general"

class TrustManager:
    def __init__(self, decay=0.01, learning_rate=0.2):
        self.agents: Dict[str, Agent] = {}
        self.decay = decay
        self.lr = learning_rate

    def register(self, agent_id: str) -> Agent:
        a = Agent(agent_id)
        self.agents[agent_id] = a
        return a

    def observe(self, agent_id: str, action: str):
        """Update trust based on an observed action.
        Rule-based policy:
        - Classify an action as malicious if it contains 'exfiltrate' or 'bypass_auth'.
        - Move trust toward target (1.0 for benign, 0.0 for malicious) with learning rate.
        - Apply a small decay to simulate natural trust erosion over time.
        - Clamp trust to [0.0, 1.0].
        - Record the observation in the agent's history.
        """
        a = self.agents[agent_id]
        # Detect malicious intent from action keywords.
        is_malicious = 1 if ("exfiltrate" in action or "bypass_auth" in action) else 0
        prior = a.trust
        # Compute delta toward target trust:
        #   target = 0.0 if malicious, else 1.0
        #   delta  = lr * (target - prior)
        delta = self.lr * (0.0 - prior) if is_malicious else self.lr * (1.0 - prior)
        # Update with decay: subtract a small constant to reflect trust decay each observation.
        updated = prior + delta - self.decay
        # Clamp to keep trust within [0, 1].
        a.trust = max(0.0, min(1.0, updated))
        # Append timestamped label of whether the action was malicious.
        a.history.append((time.time(), bool(is_malicious)))
        return is_malicious

    def get_trust(self, agent_id: str) -> float:
        return self.agents[agent_id].trust

    def summary(self):
        return {aid: a.trust for aid,a in self.agents.items()}
