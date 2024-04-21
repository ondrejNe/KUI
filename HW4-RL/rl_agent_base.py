from typing import Dict

from kuimaze2.map import State, Action
from kuimaze2.rl import RLProblem


class RLAgentBase:
    """Base interface for implementation of RL agent using Q-learning algorithm"""

    def __init__(self, env: RLProblem, gamma: float, alpha: float):
        self.env = env
        self.gamma = gamma
        self.alpha = alpha

    def learn_policy(self) -> Dict[State, Action]:
        """Learns and returns a policy mapping from states to actions."""
        raise NotImplementedError
