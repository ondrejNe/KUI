from typing import List, Tuple, Optional
import math
import heapq

"""
priority, counter, move
"""
QueueElement = Tuple[float, int, Tuple[int, int]]


class PriorityQueue:
    """
    Wrapper for a priority queue using heapq.
    """
    elements: List[QueueElement]
    counter: int

    def __init__(self) -> None:
        self.elements = []
        self.counter = 0  # Counter to ensure unique sequence numbers for tie-breaking

    def push(self, item: (int, int), priority: float) -> None:
        # The heapq module uses min-heap, so we use priority directly
        # The counter ensures that two items with the same priority are ordered by insertion order
        # Reversed priority setting
        heapq.heappush(self.elements, (-priority, self.counter, item))
        self.counter += 1

    def pop(self) -> (int, int):
        # Returns the item with the highest priority (lowest value)
        ele = heapq.heappop(self.elements)[2]
        return ele

    def is_empty(self) -> bool:
        return len(self.elements) == 0

    def clear(self) -> None:
        self.elements = []
