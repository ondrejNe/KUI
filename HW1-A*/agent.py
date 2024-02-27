from kuimaze2 import SearchProblem, Map, State
from typing import List, Tuple, Optional
import math
import heapq


class QueueItem:
    """
    Wrapper for a state and the path to reach it.
    """
    state: State
    path: List[State]

    def __init__(self, state: State, path_to_state: list[State]) -> None:
        self.state = state
        self.path = path_to_state

    def unpack(self) -> tuple[State, list[State]]:
        return self.state, self.path


"""
Alias for a tuple containing a priority and a QueueItem.
"""
QueueElement = Tuple[float, int, QueueItem]


class PriorityQueue:
    """
    Wrapper for a priority queue using heapq.
    """
    elements: List[QueueElement]
    counter: int

    def __init__(self) -> None:
        self.elements = []
        self.counter = 0  # Counter to ensure unique sequence numbers for tie-breaking

    def push(self, item: QueueItem, priority: float) -> None:
        # The heapq module uses min-heap, so we use priority directly
        # The counter ensures that two items with the same priority are ordered by insertion order
        heapq.heappush(self.elements, (priority, self.counter, item))
        self.counter += 1

    def pop(self) -> QueueItem:
        # Returns the item with the highest priority (lowest value)
        return heapq.heappop(self.elements)[2]  # [2] to return the item

    def is_empty(self) -> bool:
        return len(self.elements) == 0


class Heuristic:
    @staticmethod
    def euclidean_distance(current_state: State, goals: set[State]) -> float:
        """
        Euclidean distance heuristic for A* search.
        """
        return min(math.sqrt((current_state.r - goal.r) ** 2 + (current_state.c - goal.c) ** 2) for goal in goals)


class Agent:

    def __init__(self, environment: SearchProblem) -> None:
        self.environment = environment

    def find_path(self) -> Optional[list[State]]:
        start_state = self.environment.get_start()
        goals = self.environment.get_goals()
        print(f"Starting A* search from {start_state} aiming for goals: {goals}")

        pq = PriorityQueue()
        pq.push(
            QueueItem(start_state, []),
            Heuristic.euclidean_distance(start_state, goals)
        )

        costs = {start_state: 0}

        while not pq.is_empty():
            current_state, current_path = pq.pop().unpack()
            current_cost = costs[current_state]

            print(f"Exploring state: {current_state} with current cost: {current_cost}")

            if self.environment.is_goal(current_state):
                final_path = current_path + [current_state]
                print(f"Goal found! Path: {final_path}")
                return final_path

            for action in self.environment.get_actions(current_state):
                new_state, action_cost = self.environment.get_transition_result(current_state, action)
                new_cost = current_cost + action_cost

                if new_state not in costs or new_cost < costs[new_state]:
                    costs[new_state] = new_cost
                    pq.push(
                        QueueItem(new_state, current_path + [current_state]),
                        new_cost + Heuristic.euclidean_distance(new_state, goals)
                    )
                    print(f"Adding state: {new_state} with new cost: {new_cost}")

        print("No path found to the goal.")
        return None


if __name__ == "__main__":
    # Create a Map instance
    MAP = """
    .S...
    .###.
    ...#G
    """
    map = Map.from_string(MAP)
    # Create an environment as a SearchProblem initialized with the map
    env = SearchProblem(map, graphics=False)  # Set graphics=False for debugging without GUI
    # Create the agent x cand find the path
    agent = Agent(env)
    path = agent.find_path()
    print(f"Final path: {path}")
