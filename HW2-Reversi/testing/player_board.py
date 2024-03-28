import copy


class GameBoard(object):

    def __init__(self, board_size: int = 8, player1_color=0, player2_color=1, empty_color=-1):
        self.board_size = board_size
        self.p1_color = player1_color
        self.p2_color = player2_color
        self.empty_color = empty_color
        self.board = self.init_board()

    def init_from_list(self, board: list[list], player1_color, player2_color, empty_color=-1):
        self.board_size = len(board)
        self.p1_color = player1_color
        self.p2_color = player2_color
        self.empty_color = empty_color
        self.board = board

    def clear(self):
        self.board = self.init_board()

    def init_board(self):
        """
        Crates board and adds initial stones.
        :return: Initiated board
        """
        board = [self.empty_color] * self.board_size
        for row in range(self.board_size):
            board[row] = [self.empty_color] * self.board_size

        board[self.board_size // 2 - 1][self.board_size // 2 - 1] = self.p1_color
        board[self.board_size // 2][self.board_size // 2] = self.p1_color
        board[self.board_size // 2][self.board_size // 2 - 1] = self.p2_color
        board[self.board_size // 2 - 1][self.board_size // 2] = self.p2_color

        return board

    def play_move(self, move, players_color):
        """
        :param move: position where the move is made [x,y]
        :param players_color: player that made the move
        """

        self.board[move[0]][move[1]] = players_color
        for x, y in self.board_directions():
            if self.confirm_direction(move, x, y, players_color):
                self.change_stones_in_direction(move, x, y, players_color)

    def is_correct_move(self, move, players_color):
        """
        Check if the move is correct
        """
        if self.board[move[0]][move[1]] == self.empty_color:
            dx = [-1, -1, -1, 0, 1, 1, 1, 0]
            dy = [-1, 0, 1, 1, 1, 0, -1, -1]
            for i in range(len(dx)):
                if self.confirm_direction(move, dx[i], dy[i], players_color):
                    return True

        return False

    def confirm_direction(self, move, dx, dy, players_color):
        """
        Looks into direction [dx,dy] to find if the move in this direction is correct.
        It means that first stone in the direction is opponents and last stone is players.
        :param move: position where the move is made [x,y]
        :param dx: x direction of the search
        :param dy: y direction of the search
        :param players_color: player that made the move
        :return: True if move in this direction is correct
        """
        if players_color == self.p1_color:
            opponents_color = self.p2_color
        else:
            opponents_color = self.p1_color

        posx = move[0] + dx
        posy = move[1] + dy
        if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
            if self.board[posx][posy] == opponents_color:
                while (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                        if self.board[posx][posy] == self.empty_color:
                            return False
                        if self.board[posx][posy] == players_color:
                            return True

        return False

    def change_stones_in_direction(self, move, dx, dy, players_color):
        posx = move[0] + dx
        posy = move[1] + dy
        while self.board[posx][posy] != players_color:
            self.board[posx][posy] = players_color
            posx += dx
            posy += dy

    def can_play(self, players_color):
        """
        :return: True if there is a possible move for player
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.is_correct_move([x, y], players_color):
                    return True

        return False

    def get_board_copy(self):
        return copy.deepcopy(self.board)

    def get_score(self):
        stones = [0, 0]
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == self.p1_color:
                    stones[0] += 1
                if self.board[x][y] == self.p2_color:
                    stones[1] += 1
        return stones

    def get_color_score(self, color):
        count = 0
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == color:
                    count += 1
        return count

    def board_coordinates(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                yield row, col

    def board_corners(self):
        return [
            (0, 0),
            (0, self.board_size - 1),
            (self.board_size - 1, 0),
            (self.board_size - 1, self.board_size - 1)
        ]

    def board_directions(self):
        return [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        ]

    def print_board(self):
        for x in range(self.board_size):
            row_string = ''
            for y in range(self.board_size):
                if self.board[x][y] == self.empty_color:
                    row_string += ' -'
                else:
                    row_string += ' ' + str(self.board[x][y])
            print(row_string)
        print('')

    def get_all_valid_moves(self, players_color):
        valid_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if (self.board[x][y] == self.empty_color) and self.is_correct_move([x, y], players_color):
                    valid_moves.append((x, y))
        return valid_moves

    def is_board_full(self):
        for row in self.board:
            if self.empty_color in row:
                return False
        return True

    def can_any_player_move(self):
        if self.get_all_valid_moves(self.p1_color):
            return True
        if self.get_all_valid_moves(self.p2_color):
            return True
        return False

    def game_over(self):
        # The game is over if the board is full or if neither player can make a valid move
        return self.is_board_full() or not self.can_any_player_move()

    def is_corner(self, x, y) -> bool:
        return ((x, y) == (0, 0) or
                (x, y) == (0, self.board_size - 1) or
                (x, y) == (self.board_size - 1, 0) or
                (x, y) == (self.board_size - 1, self.board_size - 1))

    def is_stable_coin(self, x, y) -> bool:
        if self.board[x][y] == self.empty_color:
            return False  # Empty space is not stable

        coin_color = self.board[x][y]
        # Corners are always stable
        if self.is_corner(x, y):
            return True

        # Check edges for potential stability
        if x == 0 or x == self.board_size - 1 or y == 0 or y == self.board_size - 1:
            stable_horizontal = True
            stable_vertical = True

            # Check horizontal stability on edges
            if x == 0 or x == self.board_size - 1:
                for col in range(self.board_size):
                    if self.board[x][col] != coin_color:
                        stable_horizontal = False
                        break

            # Check vertical stability on edges
            if y == 0 or y == self.board_size - 1:
                for row in range(self.board_size):
                    if self.board[row][y] != coin_color:
                        stable_vertical = False
                        break

            return stable_horizontal or stable_vertical

        # Simplified internal stability (very basic and not fully accurate)
        stable_internal = True
        for dx, dy in self.board_directions():
            nx, ny = x + dx, y + dy
            if 0 <= nx <= self.board_size - 1 and 0 <= ny <= self.board_size - 1:
                if self.board[nx][ny] != coin_color:
                    stable_internal = False
                    break
        return stable_internal

    def get_children(self, player_color):
        valid_moves = self.get_all_valid_moves(player_color)
        children = []

        for move in valid_moves:
            new_board_ref = copy.deepcopy(self)
            new_board_ref.play_move(move, player_color)
            children.append(new_board_ref)

        return children
