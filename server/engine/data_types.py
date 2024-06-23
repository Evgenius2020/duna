from dataclasses import dataclass
from enum import Enum


class CellState(Enum):
    EMPTY = ' '
    WHITE = 'w'
    BLACK = 'b'
    KING = 'k'

    def __str__(self):
        return self.value


class GameState(Enum):
    PLAYING = ('p',)
    WHITE_WIN = ('w',)
    BLACK_WIN = 'b'


@dataclass(frozen=True)
class CellCoordinates:
    vertical: int
    horizontal: int

    def __str__(self):
        return f'{self.vertical:x}{self.horizontal:x}'

    def __eq__(self, other):
        # Default eq works unstable.
        return (self.vertical == other.vertical) and (
            self.horizontal == other.horizontal
        )


@dataclass(frozen=True)
class TurnCode:
    coord_from: CellCoordinates
    coord_to: CellCoordinates

    def __str__(self):
        return f'{self.coord_from}{self.coord_to}'

    def __eq__(self, other):
        return (self.coord_from == other.coord_from) and (
            self.coord_to == other.coord_to
        )
