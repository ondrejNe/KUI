import random

from kuimaze2.map import Map, State, Action
from kuimaze2.rl import RLProblem
from rl_agent_base import RLAgentBase
from rl_agent_q_table import RLAgentQTable

"""
Global settings for the Q-learning algorithm

EPISODE_NUM: Number of episodes
EPISODE_MAX_STEPS: Maximum steps in an episode
"""
EPISODE_NUM = 2000
EPISODE_MAX_STEPS = 500


class RLAgent(RLAgentBase):
    """Concrete implementation of the RL agent using Q-learning algorithm"""

    def __init__(self, env: RLProblem, gamma: float = 0.9, alpha: float = 0.1):
        super().__init__(env, gamma, alpha)
        self.q_table = RLAgentQTable(env, gamma, alpha)

    def learn_policy(self) -> dict[State, Action]:
        """RL agent learns the policy mapping from states to actions using Q-learning algorithm"""
        for episode in range(EPISODE_NUM):
            total_reward = self.run_episode()
            if episode % 100 == 0:
                print(f"Episode: {episode}, Total reward: {total_reward}")
        return self.q_table.best_actions()

    def run_episode(self) -> float:
        state = self.env.reset()
        total_reward = 0
        steps = 0

        while steps < EPISODE_MAX_STEPS:
            action = self.choose_action(state)
            next_state, reward, done = self.env.step(action)
            self.q_table.update_q_value(state, action, reward, next_state)
            state = next_state
            total_reward += reward
            steps += 1
            if done:
                break
        return total_reward

    def choose_action(self, state, epsilon=0.1):
        """Choose an action using an epsilon-greedy strategy - exploration vs exploitation"""
        if random.random() < epsilon:
            # Either explore from the action space
            return random.choice(self.q_table.actions(state))
        else:
            # Or exploit from the Q-table to best action
            return self.q_table.best_action(state)


if __name__ == "__main__":
    MAP = """
    ...G
    .#.D
    S...
    """
    map = Map.from_string(MAP)
    env = RLProblem(
        map,
        action_probs=dict(forward=0.8, left=0.1, right=0.1, backward=0.0),
        graphics=True,
    )

    agent = RLAgent(env, gamma=0.9, alpha=0.1)
    policy = agent.learn_policy()
    print("Policy found:", policy)
