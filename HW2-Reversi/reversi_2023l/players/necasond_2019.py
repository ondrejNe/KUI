import copy

class MyPlayer:
    '''Weighted decision making reversi'''
    def __init__(self, my_color, opponent_color):
        self.color_me = my_color
        self.color_op = opponent_color
        # colors are either 1 or 0
        # -1 for empty board space
        self.name = 'necasond'

        self.weight_matrix = [  [ 100  ,-5.00 , 5    , 4    , 4    , 5    ,-5.00 , 100  ],
                                [-5.00 ,-20   , 0.01 , 0.01 , 0.01 , 0.01 ,-20   ,-5.00 ],
                                [ 5    , 0.01 ,-4.00 , 0.02 , 0.02 ,-4.00 , 0.01 , 5    ],
                                [ 4    , 0.01 , 0.02 , 0.01 , 0.01 , 0.02 , 0.01 , 4    ],
                                [ 4    , 0.01 , 0.02 , 0.01 , 0.01 , 0.02 , 0.01 , 4    ],
                                [ 5    , 0.01 ,-4.00 , 0.02 , 0.02 ,-4.00 , 0.01 , 5    ],
                                [-5.00 ,-20   , 0.01 , 0.01 , 0.01 , 0.01 ,-20   ,-5.00 ],
                                [ 100  ,-5.00 , 5    , 4    , 4    , 5    ,-5.00 ,  100 ]  ]

        self.size = 8
        # size of playing board
        # def corner_situation(self, board, color_me, row, column):
        #     '''Returns True if the corner is occupied by color_me'''
        #     Bool = False
        #     corners = [(0,0), (7,7), (0,7), (7,0)]
        #     variable = (row,column)
        #     if variable in corners and board[row][column] == color_me:
        #         Bool = True

        #     return Bool

    def count_weights(self, board, color_me, color_op):
        '''Return sum of weighted_matrix * board'''
        weight = 0
        # sum of board
        act_pos = 0
        # coeficient based on position ownership

        for row in range(self.size):
            for col in range(self.size):

                if board[row][col] == color_me:
                    act_pos = 1
                elif board[row][col] == color_op:
                    act_pos = -1
                else:
                    act_pos = 0


                weight += act_pos * self.weight_matrix[row][col]

        return weight

    def playable_positions(self, board, color_me, color_op):
        '''Returns playable positions and according directions'''
        positions = []
        # all playable positions with possible directions
        moves = [(1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1), (1,1)]
        # playable moves

        def direction(row, col, move, board, color_me, color_op):
            '''Returns whether the move is playable'''
            if board[row][col] != -1:
                return False

            x = col + move[0]
            y = row + move[1]
            # modable coords
            try:
                if board[y][x] != color_op:
                    return False
            except:
                return False

            while 0 <= x <= ( self.size - 1 ) and 0 <= y <= ( self.size - 1 ):
                if board[y][x] == color_op:
                    x += move[0]
                    y += move[1]
                elif board[y][x] == color_me:
                    return True
                else:
                    return False

            return False

        '''Function main ======================================================'''
        for row in range(self.size):
            for col in range(self.size):

                directions = [] # playable directions for position
                for move in moves:
                    if direction(row, col, move, board, color_me, color_op): # True or False
                        directions.append(move)

                if directions != []:
                    directions.insert(0, (row, col)) # first index are board coords
                    positions.append(directions)

        return positions

    def update_board(self, board, position, color_me, color_op):
        '''Returns updated board'''
        act_board = copy.deepcopy(board)
        # new updateable board

        coords = position[0]
        # first item is position, the rest are moves
        root_y = coords[0]
        root_x = coords[1]

        act_board[root_y][root_x] = color_me

        for move in position[1:]:
            y = root_y + move[1]
            x = root_x + move[0]
            while board[y][x] != color_me:
                act_board[y][x] = color_me
                y += move[1]
                x += move[0]

        return act_board


    def search_algo(self, depth, board, color_me, color_op): # True == Max
        '''Recursive max algorithm'''
        act_board = copy.deepcopy(board)
        # actual board setup
        positions = self.playable_positions(act_board, color_me, color_op)
        weights = []

        if positions == []:
            return (-500,-500) # no position can be played

        for i in range(len(positions)):
            new_board = self.update_board(act_board, positions[i], color_me, color_op)

            if depth - 1 != -1: # reached depth
                weight = self.search_algo(depth - 1, new_board, color_op, color_me)
                weights.append( (weight[0], positions[i][0]) )
            else:
                weight = self.count_weights(new_board, color_me, color_op)
                weights.append( (weight, positions[i][0]) )

        weights.sort(reverse = True)
        return weights[0]

    def move(self, board):
        '''Returns position to play'''

        try:
            recursion_depth = 2

            verdict = self.search_algo(recursion_depth, board, self.color_me, self.color_op)
            # return best position according to weight

            if verdict == (-500, -500): # no position can be played
                return None

            return verdict[1]

        except:
            verdict = self.playable_positions(board, self.color_me, self.color_op)
            if verdict == []:
                return None
                # no valid position
            return verdict[0][0]
            # play fisrt valid position