class MyPlayer:
    '''po staru minimalizuje zisk snazi se zahrat rohy ke konci greedy'''

    def __init__(self, my_stone, enemy_stone, board_size):
        self.name = 'zacekpe2'
        self.round_counter = 0
        self.my_stone = my_stone
        self.enemy_stone = enemy_stone
        self.matrix = []
        self.value_matrix = []
        self.coordinates = []
        self.board_size = board_size

    def move(self, matrix):
        import copy
        self.matrix = matrix
        self.value_matrix = copy.deepcopy(matrix)
        self.coordinates = self.chose_strategy()
        self.round_counter += 1
        return self.coordinates

    def find_free_space(self):
        for idy in range(8):
            for idx in range(8):
                self.value_matrix[idx][idy] = 0
                if self.matrix[idx][idy] == -1:
                    self.value_matrix[idx][idy] = self.set_value_for_space(idx, idy)

    def chose_strategy(self):
        result = []
        if self.round_counter <= 20:
            # prioretizuje rohy pak stred
            # snazi se mit conejmensi zisk
            result = self.fiding_best_cordinates(1)
            return result
        if self.round_counter > 20:
            # greedy player
            result = self.fiding_best_cordinates(3)
            return result

    def fiding_best_cordinates(self, strategy):
        self.find_free_space()
        x = 0
        y = 0
        value = 0
        for idx in (0, 7):
            for idy in (0, 7):
                if self.value_matrix[idx][idy] > 0:
                    self.value_matrix[idx][idy] += 10000
        for idx in range(2, 6):
            for idy in range(2, 6):
                if self.value_matrix[idx][idy] > 0:
                    self.value_matrix[idx][idy] += 1000
        for target in (10000, 1000, 0):
            for idx in range(8):
                for idy in range(8):
                    if self.value_matrix[idx][idy] > target:
                        if strategy == 1 and value > self.value_matrix[idx][idy]:
                            value = self.value_matrix[idx][idy]
                            x = idx
                            y = idy
                        elif value == 0:
                            value = self.value_matrix[idx][idy]
                            x = idx
                            y = idy
                        if strategy == 3 and value < self.value_matrix[idx][idy]:
                            value = self.value_matrix[idx][idy]
                            x = idx
                            y = idy
                        if value > 0:
                            return x, y
        return None

    def set_value_for_space(self, r, c):
        move_a = r
        move_b = c
        final_value = 0
        for idx in range(-1, 2):
            for idy in range(-1, 2):
                counter = 0
                move_a += idx
                move_b += idy
                if idx == 0 and idy == 0:
                    continue
                if move_a < 0 or move_b < 0 or move_a > 7 or move_b > 7:
                    move_a = r
                    move_b = c
                    continue
                while (self.matrix[move_a][move_b] == self.enemy_stone):
                    counter += 1
                    move_a += idx
                    move_b += idy
                    if move_a < 0 or move_b < 0 or move_a > 7 or move_b > 7:
                        counter = 0
                        break
                    if self.matrix[move_a][move_b] == self.my_stone:
                        break
                    if self.matrix[move_a][move_b] == -1:
                        counter = 0
                    move_a = r
                    move_b = c
                    final_value += counter
        return final_value
