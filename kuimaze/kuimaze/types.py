# Some named tuples to be used throughout the package
import typing
import collections

#: Namedtuple to hold state position.
# State = collections.namedtuple("State", ["x", "y"])
class State(typing.NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return f"(x={self.x}, y={self.y})"


#: Namedtuple to hold path section from state A to state B. Expects C{state_from} and C{state_to} to be of type L{State}
PathSection = collections.namedtuple(
    "PathSection", ["state_from", "state_to", "cost", "action"]
)


def ensure_state(pos: tuple|State) -> State:
    """Ensure that the given position is a state.

    :param pos: The position to check.
    :return: The position as a state.
    """
    if isinstance(pos, State):
        return pos
    return State(*pos)