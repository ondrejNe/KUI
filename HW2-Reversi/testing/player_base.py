import abc


class BasePlayer(abc.ABC):
    """Base player class. All players should inherit from this class."""

    def __init__(self, my_color, opponent_color, board_size=8):
        self.name = 'necasond'
        self.my_color = my_color
        self.opp_color = opponent_color
        self.board_size = board_size

    @abc.abstractmethod
    def move(self, board) -> (int, int):
        """
        :param board: current board
        :return: the next move
        """
        pass
