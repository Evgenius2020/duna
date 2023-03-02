from dataclasses import dataclass
from enum import Enum


class CellState(Enum):
    EMPTY = ' '
    WHITE = 'w'
    BLACK = 'b'
    KING = 'k'

    def __str__(self):
        return self.value


@dataclass
class CellCoord:
    vertical: int
    horizontal: int

    def __str__(self):
        return f'{self.vertical:x}{self.horizontal:x}'


@dataclass
class TurnCode:
    coord_from: CellCoord
    coord_to: CellCoord

    def __str__(self):
        return f'{self.coord_from}{self.coord_to}'
