import random
import copy


class MyPlayer:
    """Corners first, evaporation at the start, mobility evaluation"""

    def __init__(self, my_color, opponent_color):
        self.name = 'simanvo1'
        # Student's username
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.round_number = 0
        self.score = [2, 2]
        self.possible_move = []
        self.move_value = []

    @staticmethod
    def is_on_board(row, col):
        return not (row < 0 or row > 7 or col < 0 or col > 7)

    @staticmethod
    def is_in_corner(row, col):
        return (row, col) == (0, 0) or (row, col) == (0, 7) or (row, col) == (7, 0) or (row, col) == (7, 7)

    @staticmethod
    def is_on_x_square(row, col):
        return (row, col) == (1, 1) or (row, col) == (1, 6) or (row, col) == (6, 1) or (row, col) == (6, 6)

    @staticmethod
    def is_on_c_square(row, col):
        c_squares = [(0, 1), (0, 6), (1, 0), (1, 7), (6, 0), (6, 7), (7, 1), (7, 6)]
        for item in c_squares:
            if item == (row, col):
                return True
        return False

    def is_on_c_square_my_corner(self, row, col, board):
        if ((row, col) == (0, 1) or (row, col) == (1, 0)) and board[0][0] == self.my_color:
            return True
        if ((row, col) == (0, 6) or (row, col) == (1, 7)) and board[0][7] == self.my_color:
            return True
        if ((row, col) == (6, 0) or (row, col) == (7, 1)) and board[7][0] == self.my_color:
            return True
        if ((row, col) == (6, 7) or (row, col) == (7, 6)) and board[7][7] == self.my_color:
            return True
        return False

    @staticmethod
    def is_in_sweet_sixteen(row, col):
        return 1 < row < 6 and 1 < col < 6

    @staticmethod
    def is_empty(row, col, board):
        return board[row][col] == -1

    @staticmethod
    def direction():
        """  Generates direction vectors  """

        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for i in range(len(directions)):
            yield directions[i]

    @staticmethod
    def board_coordinates():
        """  Generates all possible board coordinates  """

        for row in range(8):
            for col in range(8):
                yield row, col

    def is_adjacent_opponent(self, row, col, dir_row, dir_col, board, op_color):
        if self.is_on_board(row + dir_row, col + dir_col):
            return board[row + dir_row][col + dir_col] == op_color
        else:
            return False

    def is_disc_in_line(self, row, col, dir_row, dir_col, board, my_color, op_color):
        """  Checks whether there is a continuous line of opponent\'s discs followed by own disc  """

        row += dir_row
        col += dir_col
        while self.is_on_board(row, col) and board[row][col] == op_color:
            row += dir_row
            col += dir_col
            if self.is_on_board(row, col):
                if board[row][col] == my_color:
                    return True
        return False

    def get_possible_moves(self, board, move_list, my_color, op_color):
        for row, col in self.board_coordinates():
            if self.is_empty(row, col, board):
                for move in self.find_move(row, col, board, move_list, my_color, op_color):
                    yield move

    def find_move(self, row, col, board, move_list, my_color, op_color):
        """  Checks whether it can play at row,col position, if yes, it stores a move  """

        for vec in self.direction():
            if self.is_adjacent_opponent(row, col, vec[0], vec[1], board, op_color):
                if self.is_disc_in_line(row, col, vec[0], vec[1], board, my_color, op_color):
                    if (row, col) not in move_list:
                        yield row, col

    def get_score(self, board):
        self.score = [0, 0]

        for row, col in self.board_coordinates():
            if board[row][col] == 0:
                self.score[0] += 1
            elif board[row][col] == 1:
                self.score[1] += 1

    def get_round_number(self, board):
        """  Returns a number of the current round, however, it doesn\'t account for moves that had to be passed.  """

        self.round_number = 0
        for x, y in self.board_coordinates():
            if board[x][y] != -1:
                self.round_number += 1
        return self.round_number - 3

    def get_move_value(self, row, col, board):
        """  Counts how many discs will be flipped if this move gets played  """

        value = 0
        for vec_dir in self.direction():
            dir_row = row + vec_dir[0]
            dir_col = col + vec_dir[1]
            while self.is_on_board(dir_row, dir_col) and board[dir_row][
                dir_col] == self.opponent_color and self.is_disc_in_line(row, col, vec_dir[0], vec_dir[1], board,
                                                                         self.my_color, self.opponent_color):
                value += 1
                dir_row += vec_dir[0]
                dir_col += vec_dir[1]

        return value

    def get_move_mobility(self, row, col, board):
        """  Simulates playing a move, returns:  -the amount of moves available in the next round (mobility)  -potential mobility  -opponent\'s mobility  """

        board_copy = copy.deepcopy(board)
        board_copy[row][col] = self.my_color
        # Flips the discs after playing the input move
        for vec_dir in self.direction():
            dir_row = row + vec_dir[0]
            dir_col = col + vec_dir[1]
        while self.is_on_board(dir_row, dir_col) and board[dir_row][
            dir_col] == self.opponent_color and self.is_disc_in_line(row, col, vec_dir[0], vec_dir[1], board,
                                                                     self.my_color, self.opponent_color):
            board_copy[dir_row][dir_col] = self.my_color
            dir_row += vec_dir[0]
            dir_col += vec_dir[1]
            mobility_move = []
        for move in self.get_possible_moves(board_copy, mobility_move, self.my_color, self.opponent_color):
            mobility_move.append(move)
        return len(mobility_move), self.get_potential_mobility(board_copy), self.get_opponent_mobility(board_copy)

    def get_potential_mobility(self, board):
        """  Counts the amount of opponent\'s disks that are adjacent to an empty field.  """

        potential_mobility = 0
        for row, col in self.board_coordinates():
            if board[row][col] == self.opponent_color:
                for row_dir, col_dir in self.direction():
                    if self.is_on_board(row + row_dir, col + col_dir):
                        if self.is_empty(row + row_dir, col + col_dir, board):
                            potential_mobility += 1

        return potential_mobility

    def get_opponent_mobility(self, board):
        """  Counts the amount of opponent\'s possible moves (mobility).  """

        opponent_mobility_move = []
        for move in self.get_possible_moves(board, opponent_mobility_move, self.opponent_color, self.my_color):
            opponent_mobility_move.append(move)
        return len(opponent_mobility_move)

    def evaluate_moves(self, board):
        self.move_value = []

        for move in self.possible_move:
            flip_amt = self.get_move_value(move[0], move[1], board)
            mobility = self.get_move_mobility(move[0], move[1], board)
            potential_mobility = mobility[1]
            opponent_mobility = mobility[2]

            # Formula for determining the mobility coefficient
            mobility_value = mobility[0] - opponent_mobility + 0.3 * potential_mobility
            self.move_value.append((move, flip_amt, mobility_value))

    def choose_move(self, board):
        """  Determines which move to play. Firstly it tries to play on the corner.
        If the round number is below 12, it tries to play in the sweet sixteen to increase mobility.
        If there is a risk of evaporation, it plays a move that flips the most discs.
        Near the end, it plays a move that flips the most discs.
        Otherwise, it attempts to increase own mobility and decrease opponent's mobility.  """
        if len(self.possible_move) == 0:
            return None
        random.shuffle(self.possible_move)
        # To avoid starting evaluation from top left corner every time
        # Corners first
        for move in self.possible_move:
            if self.is_in_corner(move[0], move[1]):
                return move
            self.evaluate_moves(board)
            if self.round_number < 12:
                return_move = self.play_evaporation_strategy()
            elif self.round_number > 56:
                return_move = self.play_greedy_strategy()
            else:
                return_move = self.play_mobility_strategy(board)
            return return_move

    def play_evaporation_strategy(self):
        """  Plays the move that flips only a few discs - unless there is a risk of premature loss.  """
        self.move_value.sort(key=lambda index: index[1], reverse=True)
        if self.score[0] > 2:
            for i in range(1, len(self.possible_move)):
                row = self.move_value[-i][0][0]
                col = self.move_value[-i][0][1]
                if self.is_in_sweet_sixteen(row, col) and not self.is_on_x_square(row, col) and not self.is_on_c_square(
                        row, col):
                    return self.move_value[-i][0]
        return self.move_value[0][0]  # Fallback strategy

    def play_greedy_strategy(self):
        """  Plays the move that flips the most discs - unless it is on X square or C square  """
        self.move_value.sort(key=lambda index: index[1], reverse=True)
        for i in range(0, len(self.move_value) - 1):
            move_row = self.move_value[i][0][0]
            move_col = self.move_value[i][0][1]
            if not self.is_on_x_square(move_row, move_col) and not self.is_on_c_square(move_row, move_col):
                return self.move_value[i][0]
        return self.move_value[0][0]  # Fallback strategy

    def play_mobility_strategy(self, board):
        """  Plays the move that maximizes own mobility, minimizes opponent\'s mobility
        Avoid playing on C square unless the nearby corner is mine  """
        self.move_value.sort(key=lambda index: 0.5 * index[1] + index[2], reverse=True)
        for i in range(0, len(self.move_value)):
            move_row = self.move_value[i][0][0]
            move_col = self.move_value[i][0][1]
            if not self.is_on_x_square(move_row, move_col):
                if self.is_on_c_square_my_corner(move_row, move_col, board):
                    return self.move_value[i][0]
                else:
                    if not self.is_on_c_square(move_row, move_col):
                        return self.move_value[i][0]
        return self.move_value[0][0]  # Fallback strategy

    def move(self, board):
        self.round_number = self.get_round_number(board)
        self.get_score(board)
        self.possible_move = []
        for move in self.get_possible_moves(board, self.possible_move, self.my_color, self.opponent_color):
            self.possible_move.append(move)
            return_move = self.choose_move(board)
            return return_move
