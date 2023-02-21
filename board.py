from dataclasses import dataclass, field
from enum import Enum
from typing import Union


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


class Board:
    field: list[list[CellState]]
    board_size: int
    center_cell: CellCoord
    corner_cells: list[CellCoord]
    white_turn: bool = True

    def __init__(self):
        self.field = list(map(lambda s: list(map(CellState, s)), [
            '    wwwww    ',
            '     w w     ',
            '      w      ',
            '      b      ',
            'w   b   b   w',
            'ww   bbb   ww',
            'w wb bkb bw w',
            'ww   bbb   ww',
            'w   b   b   w',
            '      b      ',
            '      w      ',
            '     w w     ',
            '    wwwww    ']))
        self.board_size = len(self.field)
        self.center_cell = CellCoord(self.board_size // 2 + 1, self.board_size // 2 + 1)
        self.corner_cells = [CellCoord(1, 1),
                             CellCoord(self.board_size, 1),
                             CellCoord(1, self.board_size),
                             CellCoord(self.board_size, self.board_size)]

    def get_field_cell_state(self, vertical: int, horizontal: int) -> Union[CellState, None]:
        if not (1 <= vertical <= self.board_size and 1 <= horizontal <= self.board_size):
            return None
        return self.field[vertical - 1][horizontal - 1]

    def _set_field_cell_state(self, vertical: int, horizontal: int, cell_state: CellState):
        self.field[vertical - 1][horizontal - 1] = cell_state

    def get_available_turns(self):
        available_figures = [CellState.WHITE] if self.white_turn else [CellState.BLACK, CellState.KING]
        available_turns = []
        for vertical_coord in set(range(1, self.board_size + 1)):
            for horizontal_coord in set(range(1, self.board_size + 1)):
                if self.get_field_cell_state(vertical_coord, horizontal_coord) in available_figures:
                    available_turns.extend(self.get_turns_for_figure(CellCoord(horizontal_coord, vertical_coord)))
        return available_turns

    def get_turns_for_figure(self, from_cell: CellCoord) -> list[TurnCode]:
        if self.get_field_cell_state(from_cell.vertical, from_cell.horizontal) == CellState.EMPTY:
            return []
        forbidden_cells = [self.center_cell] + self.corner_cells if \
            self.get_field_cell_state(from_cell.vertical, from_cell.horizontal) != CellState.KING else []
        result = []
        # В каждом из 4х направлений от центра движемся до момента пока не встретим препятствие.
        for horizontal_coords, vertical_coords in \
                ((range(from_cell.horizontal - 1, 0, -1), [from_cell.vertical]),
                 (range(from_cell.horizontal + 1, self.board_size + 1), [from_cell.vertical]),
                 ([from_cell.horizontal], range(from_cell.vertical + 1, self.board_size + 1)),
                 ([from_cell.horizontal], range(from_cell.vertical - 1, 0, -1))):
            # Собираем все свободные координаты.
            possible_coords = []
            searching_stopped = False
            for vertical_coord in vertical_coords:
                for horizontal_coord in horizontal_coords:
                    probe_cell = CellCoord(vertical_coord, horizontal_coord)
                    if (self.get_field_cell_state(probe_cell.vertical,
                                                  probe_cell.horizontal) != CellState.EMPTY) or \
                            (probe_cell in forbidden_cells):
                        searching_stopped = True
                        break
                    possible_coords.append(TurnCode(from_cell, probe_cell))
                if searching_stopped:
                    break
            result += possible_coords
        return result

    def make_turn(self, turn_code: TurnCode):
        prev_coord = turn_code.coord_from
        next_coord = turn_code.coord_to
        next_coord_state = self.get_field_cell_state(prev_coord.vertical,
                                                     prev_coord.horizontal)

        # Определим свои и вражеские фигуры.
        ally_and_enemy_states = [[CellState.BLACK, CellState.KING], [CellState.WHITE]]
        if next_coord_state == CellState.WHITE:
            ally_and_enemy_states = reversed(ally_and_enemy_states)
        ally_states, enemy_states = ally_and_enemy_states

        # Двигать можно только свои фигуры в свой ход и на пустую клетку.
        if (next_coord_state not in ally_states) or \
                (next_coord_state == CellState.WHITE and self.white_turn) or \
                (self.get_field_cell_state(next_coord.vertical,
                                           next_coord.horizontal) != CellState.EMPTY):
            return

        self._set_field_cell_state(next_coord.vertical,
                                   next_coord.horizontal,
                                   next_coord_state)
        self._set_field_cell_state(prev_coord.vertical,
                                   prev_coord.horizontal,
                                   CellState.EMPTY)

        # Проверка соседей
        for next_first, next_second in ((CellCoord(next_coord.vertical + 1, next_coord.horizontal),
                                         CellCoord(next_coord.vertical + 2, next_coord.horizontal)),
                                        (CellCoord(next_coord.vertical - 1, next_coord.horizontal),
                                         CellCoord(next_coord.vertical - 2, next_coord.horizontal)),
                                        (CellCoord(next_coord.vertical, next_coord.horizontal + 1),
                                         CellCoord(next_coord.vertical, next_coord.horizontal + 2)),
                                        (CellCoord(next_coord.vertical, next_coord.horizontal - 1),
                                         CellCoord(next_coord.vertical, next_coord.horizontal - 2))):
            # next_first должна быть вражеской, а стоящая за ней - союзной или специальной клеткой, тогда срубаем.
            if (self.get_field_cell_state(next_first.vertical, next_first.horizontal) in enemy_states) and \
                    ((self.get_field_cell_state(next_second.vertical, next_second.horizontal) in ally_states) or
                     next_second in [self.center_cell] + self.corner_cells):
                self._set_field_cell_state(next_first.vertical,
                                           next_first.horizontal,
                                           CellState.EMPTY)

        self.white_turn = not self.white_turn


if __name__ == '__main__':
    b = Board()
    at = b.get_available_turns()
    print(CellCoord(1, 12))
