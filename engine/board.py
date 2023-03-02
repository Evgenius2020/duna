from copy import copy
from typing import Union

from data_types import CellState, CellCoord, TurnCode


class Board:
    field: list[list[CellState]]
    board_size: int
    center_cell: CellCoord
    corner_cells: list[CellCoord]
    white_turn: bool = False

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
        # King start position.
        self.center_cell = CellCoord(self.board_size // 2 + 1,
                                     self.board_size // 2 + 1)
        # King destination points.
        self.corner_cells = [CellCoord(1, 1),
                             CellCoord(self.board_size, 1),
                             CellCoord(1, self.board_size),
                             CellCoord(self.board_size, self.board_size)]
        # Center (when empty) and corner cells can be used for attacking.
        self.special_cells = copy(self.corner_cells)

    def get_field_cell_state(self,
                             vertical: int,
                             horizontal: int) -> Union[CellState, None]:
        if not (1 <= vertical <= self.board_size and
                1 <= horizontal <= self.board_size):
            return None
        return self.field[vertical - 1][horizontal - 1]

    def _set_field_cell_state(self,
                              vertical: int,
                              horizontal: int,
                              cell_state: CellState):
        self.field[vertical - 1][horizontal - 1] = cell_state

    def get_available_turns(self):
        available_figures = [CellState.WHITE] if self.white_turn else [
            CellState.BLACK, CellState.KING]
        available_turns = []
        for vertical_coord in set(range(1, self.board_size + 1)):
            for horizontal_coord in set(range(1, self.board_size + 1)):
                if self.get_field_cell_state(
                        vertical_coord, horizontal_coord) in available_figures:
                    available_turns.extend(self.get_turns_for_figure(
                        CellCoord(horizontal_coord, vertical_coord)))
        return available_turns

    def get_turns_for_figure(self,
                             from_cell: CellCoord) -> list[TurnCode]:
        if self.get_field_cell_state(from_cell.vertical,
                                     from_cell.horizontal) == CellState.EMPTY:
            return []
        # You can't move to center cell. Only king can go to corner cells.
        forbidden_cells = \
            [self.center_cell] + (
                self.corner_cells if self.get_field_cell_state(
                    from_cell.vertical,
                    from_cell.horizontal) != CellState.KING else [])
        result = []
        # Look all 4 directions from center until we hit an obstacle.
        # TODO: Make it simple:
        #  look at ([H] * [V] - current_pos) + check not obstacle method.
        for horizontal_coords, vertical_coords in \
                ((range(from_cell.horizontal - 1, 0, -1),
                  [from_cell.vertical]),

                 (range(from_cell.horizontal + 1, self.board_size + 1),
                  [from_cell.vertical]),

                 ([from_cell.horizontal],
                  range(from_cell.vertical + 1, self.board_size + 1)),

                 ([from_cell.horizontal],
                  range(from_cell.vertical - 1, 0, -1))):
            # Collect available cells to move at direction.
            possible_coords = []
            searching_stopped = False
            for vertical_coord in vertical_coords:
                for horizontal_coord in horizontal_coords:
                    probe_cell = CellCoord(vertical_coord, horizontal_coord)
                    if (self.get_field_cell_state(
                            probe_cell.vertical,
                            probe_cell.horizontal) != CellState.EMPTY) \
                            or (probe_cell in forbidden_cells):
                        searching_stopped = True
                        break
                    possible_coords.append(TurnCode(from_cell, probe_cell))
                if searching_stopped:
                    break
            result += possible_coords
        return result

    def make_turn(self,
                  turn_code: TurnCode) -> bool:
        prev_coord = turn_code.coord_from
        next_coord = turn_code.coord_to
        next_coord_state = self.get_field_cell_state(prev_coord.vertical,
                                                     prev_coord.horizontal)
        # Defines ally and enemy pieces.
        ally_and_enemy_states = [[CellState.BLACK, CellState.KING],
                                 [CellState.WHITE]]
        if self.white_turn:
            ally_and_enemy_states = reversed(ally_and_enemy_states)
        ally_states, enemy_states = ally_and_enemy_states

        # You can move only your pieces and only to empty cell.
        if (next_coord_state not in ally_states) or \
                (self.get_field_cell_state(
                    next_coord.vertical,
                    next_coord.horizontal) != CellState.EMPTY):
            return False

        # Check that piece move is possible.
        if turn_code not in self.get_turns_for_figure(turn_code.coord_from):
            return False

        # Switch cell states.
        self._set_field_cell_state(next_coord.vertical,
                                   next_coord.horizontal,
                                   next_coord_state)
        self._set_field_cell_state(prev_coord.vertical,
                                   prev_coord.horizontal,
                                   CellState.EMPTY)

        # Checking the attack of adjacent enemy pieces.
        for next_first_cell, next_second_cell in \
                ((CellCoord(next_coord.vertical + 1, next_coord.horizontal),
                  CellCoord(next_coord.vertical + 2, next_coord.horizontal)),
                 (CellCoord(next_coord.vertical - 1, next_coord.horizontal),
                  CellCoord(next_coord.vertical - 2, next_coord.horizontal)),
                 (CellCoord(next_coord.vertical, next_coord.horizontal + 1),
                  CellCoord(next_coord.vertical, next_coord.horizontal + 2)),
                 (CellCoord(next_coord.vertical, next_coord.horizontal - 1),
                  CellCoord(next_coord.vertical, next_coord.horizontal - 2))):
            # next_first_cell should be enemy,
            # next to it (in a row) - ally or special cell.
            next_first_cell_state = self.get_field_cell_state(
                next_first_cell.vertical,
                next_first_cell.horizontal)
            next_second_cell_state = self.get_field_cell_state(
                next_second_cell.vertical,
                next_second_cell.horizontal)
            if (next_first_cell_state in enemy_states) and \
                    ((next_second_cell_state in ally_states) or
                     (next_second_cell in self.special_cells)):
                if next_first_cell_state == CellState.KING:
                    # You can't kill king, only surround him :0
                    continue
                # If OK, enemy piece at next_first_cell can be removed.
                self._set_field_cell_state(next_first_cell.vertical,
                                           next_first_cell.horizontal,
                                           CellState.EMPTY)

        if turn_code.coord_from == self.center_cell:
            # When center cell is free, it can be used for attacking.
            self.special_cells.append(self.center_cell)

        self.white_turn = not self.white_turn

        return True


if __name__ == '__main__':
    b = Board()
    at = b.get_available_turns()
    print(CellCoord(1, 12))
    print(list(reversed([[c.value for c in row] for row in b.field])))
