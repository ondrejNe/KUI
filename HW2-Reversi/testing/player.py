import copy
import time
import random
from typing import Optional, Tuple

from player_base import BasePlayer
from player_pqueue import PriorityQueue
from player_board import GameBoard


class MyPlayer(BasePlayer):
    """Iterative alpha-beta with heuristic"""

    def __init__(self, my_color, opp_color, board_size):
        # Default settings
        super().__init__(my_color, opp_color, board_size)
        # Enhanced settings
        self.move_pqueue = PriorityQueue()

    @staticmethod
    def move_act_mobility(board_ref: GameBoard, max_player, min_player) -> float:
        """
        :return: Actual mobility
        """
        max_moves = len(board_ref.get_all_valid_moves(max_player))
        min_moves = len(board_ref.get_all_valid_moves(min_player))
        total_moves = max_moves + min_moves
        if total_moves == 0:
            return 0
        else:
            return 100 * (max_moves - min_moves) / total_moves

    @staticmethod
    def move_coin_parity(board_ref: GameBoard, max_player, min_player) -> float:
        """
        This component of the utility function captures
        the difference in coins between the max player
        and min player.
        """
        max_coins = sum(row.count(max_player) for row in board_ref.board)
        min_coins = sum(row.count(min_player) for row in board_ref.board)
        if max_coins + min_coins == 0:  # Prevent division by zero
            return 0
        return 100 * (max_coins - min_coins) / (max_coins + min_coins)

    @staticmethod
    def move_stability(board_ref: GameBoard, max_player, min_player) -> float:
        max_stable = 0
        max_unstable = 0
        min_stable = 0
        min_unstable = 0
        for x, y in board_ref.board_coordinates():
            if board_ref.board[x][y] == board_ref.empty_color:
                continue  # Skip empty spaces
            if board_ref.board[x][y] == max_player:
                if board_ref.is_stable_coin(x, y):
                    max_stable += 1
                else:
                    max_unstable += 1
            else:
                if board_ref.is_stable_coin(x, y):
                    min_stable += 1
                else:
                    min_unstable += 1

        max_stability = max_stable - max_unstable
        min_stability = min_stable - min_unstable

        total_stability = max_stability + min_stability
        if total_stability == 0:
            return 0
        else:
            return 100 * (max_stability - min_stability) / total_stability

    @staticmethod
    def move_corners_capture(board_ref: GameBoard, max_player, min_player) -> float:
        """
        The specialty of these squares is that once
        captured, they cannot be flanked by the opponent.
        """
        max_corners = 0
        min_corners = 0
        for x, y in board_ref.board_corners():
            if board_ref.board[x][y] == max_player:
                max_corners += 1
            elif board_ref.board[x][y] == min_player:
                min_corners += 1
        total_corners = max_corners + min_corners
        if total_corners == 0:
            return 0
        else:
            return 100 * (max_corners - min_corners) / total_corners

    @staticmethod
    def evaluate_board(board_ref: GameBoard, max_player, min_player) -> float:
        mobility = MyPlayer.move_act_mobility(board_ref, max_player, min_player)
        coin_parity = MyPlayer.move_coin_parity(board_ref, max_player, min_player)
        stability = MyPlayer.move_stability(board_ref, max_player, min_player)
        corners = MyPlayer.move_corners_capture(board_ref, max_player, min_player)
        score = mobility * 5 + coin_parity * 25 + corners * 30 + stability * 25
        return score

    def alpha_beta_search(self, board_ref: GameBoard, depth, alpha, beta, max_player, min_player, maximizing_player):
        # Base case: maximum depth reached or game over
        if depth == 0 or board_ref.game_over():
            return self.evaluate_board(board_ref, max_player, min_player)

        if maximizing_player:
            max_eval = float('-inf')
            for child in board_ref.get_children(max_player):
                _eval = self.alpha_beta_search(child, depth - 1, alpha, beta, max_player, min_player, False)
                max_eval = max(max_eval, _eval)
                alpha = max(alpha, _eval)
                if beta <= alpha:
                    break  # (* Beta cut-off *)
            return max_eval
        else:
            min_eval = float('inf')
            for child in board_ref.get_children(min_player):
                _eval = self.alpha_beta_search(child, depth - 1, alpha, beta, max_player, min_player, True)
                min_eval = min(min_eval, _eval)
                beta = min(beta, _eval)
                if beta <= alpha:
                    break  # (* Alpha cut-off *)
            return min_eval

    def iterative_deepening_alpha_beta(self, board, max_depth=3, time_limit=4.8 * 1000):
        start_time = time.time()
        self.move_pqueue.clear()
        board_ref_og = GameBoard()
        board_ref_og.init_from_list(
            copy.deepcopy(board),
            self.my_color,
            self.opp_color
        )

        for depth in range(1, max_depth + 1):
            current_time = time.time()
            time_diff = current_time - start_time
            if time_diff * 2 >= time_limit:
                # Heuristic to prevent starting a search that might exceed the time limit
                break
            # Assume get_all_valid_moves returns all valid moves and a way to apply them to create a new board state

            for move in board_ref_og.get_all_valid_moves(self.my_color):
                board_ref = copy.deepcopy(board_ref_og)
                board_ref.play_move(move, self.my_color)
                score = self.alpha_beta_search(board_ref, depth,
                                               float('-inf'),
                                               float('inf'),
                                               self.my_color,
                                               self.opp_color,
                                               True)
                self.move_pqueue.push(move, score)
        best_move = self.move_pqueue.pop()
        return best_move

    def move(self, board: list[list]) -> Optional[Tuple[int, int]]:
        try:
            return self.iterative_deepening_alpha_beta(board)
        except:
            board_ref_og = GameBoard()
            board_ref_og.init_from_list(
                copy.deepcopy(board),
                self.my_color,
                self.opp_color
            )
            valid_moves = board_ref_og.get_all_valid_moves(self.my_color)
            if valid_moves:
                return random.choice(valid_moves)
            else:
                return None
