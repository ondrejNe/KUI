from kuimaze2.map import State, Action
from kuimaze2.rl import RLProblem


class RLAgentQTable:
    """
    Q-table wrapper for RL agent

    Data structure as: Dict[State, Dict[Action, float]]
    """

    def __init__(self, env: RLProblem, gamma: float, alpha: float) -> None:
        self.gamma = gamma
        self.alpha = alpha
        # Initialize Q-table uniformly with zeros
        self.q_table = {
            state: {action: 0.0 for action in env.get_action_space()} for state in env.get_states()
        }

    def __getitem__(self, state: State) -> dict[Action, float]:
        return self.q_table[state]

    def actions(self, state: State) -> list[Action]:
        """Return the Q table actions for given state"""
        return list(self.q_table[state].keys())

    def best_action(self, state: State) -> Action:
        """Return the best valued action for a given state"""
        return max(self.q_table[state], key=self.q_table[state].get)

    def best_actions(self) -> dict[State, Action]:
        """Return the best valued action for all states"""
        return {state: max(actions, key=actions.get) for state, actions in self.q_table.items()}

    def update_q_value(self, state: State, action: Action, reward: float, next_state: State) -> None:
        """Update Q value using the Bellman q-equation"""
        current_q = self.q_table[state][action]
        max_future_q = max(self.q_table[next_state].values()) if next_state else 0
        new_q = (1 - self.alpha) * current_q + self.alpha * (reward + self.gamma * max_future_q)
        self.q_table[state][action] = new_q
