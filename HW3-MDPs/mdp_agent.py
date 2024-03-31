#!/usr/bin/env python3

import random

from kuimaze2 import MDPProblem
from kuimaze2.typing import VTable, Policy


class MDPAgent:
    """Base class for VI and PI agents"""
    def __init__(self, env: MDPProblem, gamma: float = 0.9, epsilon: float = 0.001):
        self.env = env
        self.gamma = gamma
        self.epsilon = epsilon

    def _bellman_equation(self, state, action, values) -> float:
        """
        Computes the value of taking a given action in a given state according to the Bellman equation.

        This method calculates the expected utility of taking an action in a state, considering
        the immediate reward and the discounted value of the next state as per the current value function.

        Parameters:
            state: The current state from which the action is taken.
            action: The action being evaluated.
            values (VTable): The current value table that maps states to their values.

        Returns:
            float: The expected utility (value) of taking the given action in the given state.
        """
        action_value = 0
        for next_state, prob in self.env.get_next_states_and_probs(state, action):
            reward = self.env.get_reward(state)  # Assuming reward is on leaving the state
            action_value += prob * (reward + self.gamma * values[next_state])
        return action_value


class ValueIterationAgent(MDPAgent):
    """
    An agent that implements the Value Iteration algorithm for Markov Decision Processes (MDPs).
    This agent iteratively updates the values of states to converge to the optimal value function,
    and then derives an optimal policy based on these values.

    Inherits from:
    - MDPAgent: A base class providing common attributes and methods for MDP agents.

    Attributes:
        env (MDPProblem): The environment the agent operates in, which should provide the MDP framework.
        gamma (float): The discount factor, representing the importance of future rewards.
        epsilon (float): The threshold for determining convergence of the value function.
    """

    def _init_values(self) -> VTable:
        """
        Initializes the value table with the immediate rewards for each state.

        This initialization strategy sets the foundation for the Value Iteration algorithm,
        by assigning to each state a starting value based on its immediate reward.

        Returns:
            VTable: A dictionary mapping each state to its initial value.
        """
        return {state: self.env.get_reward(state) for state in self.env.get_states()}

    def find_policy(self) -> Policy:
        """
        Performs the Value Iteration algorithm to find the optimal policy.

        This method iteratively updates the value table until the changes between iterations
        fall below a specified epsilon threshold, considering a discount factor gamma.
        It derives and returns an optimal policy based on the converged value function.

        The optimal policy indicates the best action to take in each state to maximize
        the expected cumulative future reward.

        Returns:
            Policy: A dictionary mapping from states to the optimal action in each state.
        """
        # Initialization: Assign initial values to states
        delta = float('inf')
        values = self._init_values()
        policy = {}

        # Iteration: Loop until the value function changes are below a threshold
        while delta >= self.epsilon * (1 - self.gamma) / self.gamma:
            delta = 0
            # Update each state's value
            for state in self.env.get_states():
                # Skip terminal states
                if self.env.is_terminal(state):
                    continue
                # Calculate the value of each action and choose the max
                action_values = [(action, self._bellman_equation(state, action, values))
                                 for action in self.env.get_actions(state)]
                # Select the action with the highest value
                best_action, best_action_value = max(action_values, key=lambda x: x[1])
                # Save the delta
                delta = max(delta, abs(best_action_value - values[state]))
                # Update the value table
                values[state] = best_action_value

        # Convergence: Derive policy from values
        for state in self.env.get_states():
            if self.env.is_terminal(state):
                policy[state] = self.env.get_actions(state)[0]  # Any action will do
            else:
                # Find the best action based on the updated value function
                best_action = max(
                    self.env.get_actions(state),
                    key=lambda action: self._bellman_equation(state, action, values)
                )
                policy[state] = best_action

        return policy


class PolicyIterationAgent(MDPAgent):
    """
    Implements the Policy Iteration algorithm for solving Markov Decision Processes (MDPs).
    This agent iteratively refines its policy by alternately evaluating the current policy
    and improving it until it converges to an optimal policy that maximizes expected rewards
    from any given state.

    Inherits from:
    - MDPAgent: A base class providing common attributes and methods for MDP agents.

    Attributes:
    - env (MDPProblem): The environment the agent is interacting with, encapsulating the MDP.
    - gamma (float): Discount factor used to prioritize immediate rewards over distant rewards.
    - epsilon (float): Threshold for convergence, determining when the value function's change
      is sufficiently small to assume it has stabilized.
    """

    def _init_policy(self) -> Policy:
        """
        Initializes the policy by randomly selecting an available action for each state.

        Returns:
            Policy: A dictionary mapping each state in the environment to a randomly chosen action.
        """
        return {
            state: random.choice(self.env.get_actions(state))
            for state in self.env.get_states()
        }

    def find_policy(self) -> Policy:
        """
        Executes the policy iteration algorithm, alternating between policy evaluation
        (to determine the value of taking actions under the current policy) and policy
        improvement (to update the policy based on those evaluations).

        The process iterates until the policy remains unchanged through an entire improvement cycle,
        indicating that an optimal policy has been found.

        Returns:
            Policy: The optimal policy as a dictionary mapping states to actions.
        """
        # Initialization: Assign initial policies to the states
        policy = self._init_policy()
        is_policy_stable = False

        while not is_policy_stable:
            # Policy Evaluation: Evaluate the current policy and return the value table
            # iteratively update the value table of the current policy until convergence
            V = {state: self.env.get_reward(state) for state in self.env.get_states()}
            delta = float('inf')
            while delta != 0:
                delta = 0
                for state in self.env.get_states():
                    # Skip terminal states
                    if self.env.is_terminal(state):
                        continue
                    action, value = policy[state], V[state]
                    # Evaluate the value of the current policy
                    V[state] = self._bellman_equation(state, action, V)
                    # Update the delta
                    delta = max(delta, abs(value - V[state]))

            # Policy Improvement: Update the policy based on the value table
            new_policy = {}
            for state in self.env.get_states():
                # Calculate the value of each action and choose the max
                action_values = [(action, self._bellman_equation(state, action, V))
                                 for action in self.env.get_actions(state)]
                # Select the action with the highest value
                best_action, _ = max(action_values, key=lambda x: x[1])
                new_policy[state] = best_action

            # Convergence Check: The policy has not changed
            is_policy_stable = (policy == new_policy)

            # Update the policy
            policy = new_policy

        return policy
