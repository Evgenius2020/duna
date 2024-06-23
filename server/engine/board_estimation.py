from dataclasses import dataclass
from typing import Tuple, List

import numpy as np

from engine.board import Board
from engine.data_types import CellCoordinates, CellState, GameState


@dataclass(frozen=True)
class EstimationResult:
    king_available_directions: int
    king_available_turns: int
    white_figures_left: int
    black_figures_left: int
    shortest_path_to_finish_len: int
    game_state: GameState


def get_figures_positions(
    board: Board,
) -> Tuple[CellCoordinates, List[CellCoordinates], List[CellCoordinates]]:
    king_positions = []
    black_positions = []
    white_positions = []
    for vertical in range(1, board.board_size + 1):
        for horizontal in range(1, board.board_size + 1):
            coordinates = CellCoordinates(vertical, horizontal)
            # Oh man why enums works so strange?
            match CellState(
                board.get_field_cell_state(vertical, horizontal).value
            ):
                case CellState.KING:
                    king_positions.append(coordinates)
                case CellState.BLACK:
                    black_positions.append(coordinates)
                case CellState.WHITE:
                    white_positions.append(coordinates)

    if len(king_positions) != 1:
        raise Exception(
            f'The number of king positions found is not equal to 1: '
            f'{king_positions}'
        )

    return king_positions[0], black_positions, white_positions


def analyze_short_paths_to_finish(board: Board):
    """
    DFS algorithm implementation with unlimited one-directional move.
    Searching the shortest path of king to any corner cell.
    Shortest path is not needed, returns only its length (or None instead).
    """
    # 0 for cells with figures,
    # 3*board_size for not-visited cells.
    king_position, black_positions, white_positions = get_figures_positions(
        board
    )
    if king_position in board.corner_cells:
        return 0
    all_figures_positions = [king_position] + black_positions + white_positions
    dfs_board = [
        [
            0 if CellCoordinates(y + 1, x + 1) in all_figures_positions else -1
            for x in range(board.board_size)
        ]
        for y in range(board.board_size)
    ]
    probe_positions = [king_position]
    path_length = 1
    while True:
        new_positions = []
        while probe_positions:
            current_position = probe_positions.pop()
            available_moves = board.get_turns_for_figure(
                current_position, virtual_position=True
            )
            for move in available_moves:
                if move.coord_to in board.corner_cells:
                    return path_length
                if (
                    dfs_board[move.coord_to.vertical - 1][
                        move.coord_to.horizontal - 1
                    ]
                    != 0
                ):
                    continue
                dfs_board[move.coord_to.vertical - 1][
                    move.coord_to.horizontal - 1
                ] = path_length
                new_positions.append(move.coord_to)
        if not new_positions:
            return None

        probe_positions = new_positions
        path_length += 1


def check_game_state(board: Board) -> GameState:
    king_position, _, _ = get_figures_positions(board)
    if king_position in board.corner_cells:
        return GameState.BLACK_WIN
    # If every adjacent cell is white or out of border, king is trapped.
    for adjacent_cell in [
        CellCoordinates(king_position.vertical - 1, king_position.horizontal),
        CellCoordinates(king_position.vertical + 1, king_position.horizontal),
        CellCoordinates(king_position.vertical, king_position.horizontal - 1),
        CellCoordinates(king_position.vertical, king_position.horizontal + 1),
    ]:
        adjacent_cell_state = board.get_field_cell_state(
            adjacent_cell.vertical, adjacent_cell.horizontal
        )
        if not (
            (
                adjacent_cell_state is None
                or (adjacent_cell == board.center_cell)
            )
            or (adjacent_cell_state == CellState.WHITE)
        ):
            return GameState.PLAYING
    return GameState.WHITE_WIN


def estimate_board(board: Board):
    # Count available king directions.
    king_coordinates, black_positions, white_positions = get_figures_positions(
        board
    )
    king_available_turns = board.get_turns_for_figure(king_coordinates)
    # You can go only in up, down, left or right direction.
    king_available_directions = len(
        set(
            (
                np.sign(turn.coord_to.vertical - turn.coord_to.vertical),
                np.sign(turn.coord_to.horizontal - turn.coord_to.horizontal),
            )
            for turn in king_available_turns
        )
    )

    return EstimationResult(
        king_available_directions=king_available_directions,
        king_available_turns=len(king_available_turns),
        white_figures_left=len(white_positions),
        black_figures_left=len(black_positions),
        shortest_path_to_finish_len=analyze_short_paths_to_finish(board),
        game_state=check_game_state(board),
    )
