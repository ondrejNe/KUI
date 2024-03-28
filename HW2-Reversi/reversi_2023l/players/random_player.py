import random
from typing import Optional
from base_player import BasePlayer


class RandomPlayer(BasePlayer):
    """Random player class. RnG."""

    def __init__(self, my_color, opp_color, board_size):
        super().__init__(my_color, opp_color, board_size)

    def move(self, board) -> Optional[tuple[int, int]]:
        valid_moves = self.get_all_valid_moves(board)
        if valid_moves:
            return random.choice(valid_moves)
        else:
            return None
