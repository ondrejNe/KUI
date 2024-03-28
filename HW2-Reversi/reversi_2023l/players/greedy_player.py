import copy
import random
from typing import Optional
from game_board import GameBoard
from base_player import BasePlayer


class GreedyPlayer(BasePlayer):
    """Greed is good!"""

    def __init__(self, my_color, opp_color, board_size):
        super().__init__(my_color, opp_color, board_size)
        self.sim_board = GameBoard(board_size, my_color, opp_color, -1)

    def move(self, board: list[list]) -> Optional[tuple[int, int]]:
        board_copy = copy.deepcopy(board)
        valid_moves = self.get_all_valid_moves(board_copy)
        if valid_moves is None:
            return None  # No valid moves available

        # Calculate the number of stones each move would acquire
        move_scores = []
        for move in valid_moves:
            self.sim_board.init_from_list(board_copy, self.my_color, self.opponent_color, -1)
            self.sim_board.play_move(move, self.my_color)
            sim_score = self.sim_board.get_color_score(self.my_color)
            move_scores.append((move, sim_score))

        # Sort moves based on the number of acquired stones (higher is better)
        move_scores.sort(key=lambda x: x[1], reverse=True)

        # Find one or more moves with the highest score
        best_moves = [move_score[0] for move_score in move_scores if move_score[1] == move_scores[0][1]]

        # Choose one of the best moves randomly
        return random.choice(best_moves)
