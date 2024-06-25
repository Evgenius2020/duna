from copy import deepcopy

from engine.board import Board
from engine.board_estimation import (
    estimate_board,
    EstimationResult,
    check_game_state,
)
from engine.data_types import GameState, TurnCode
import random

WIN_VALUE = 1000
NO_ESCAPE_PATH_LEN = 20


def value_function(
    board_estimation: EstimationResult, coefficients: list[float]
) -> float:
    [
        king_available_directions_coeff,
        king_available_turns_coeff,
        white_figures_left_coeff,
        black_figures_left_coeff,
        shortest_path_to_finish_len_coeff,
    ] = coefficients
    shortest_path_to_finish_len = (
        NO_ESCAPE_PATH_LEN
        if board_estimation.shortest_path_to_finish_len is None
        else board_estimation.shortest_path_to_finish_len
    )
    return (
        board_estimation.king_available_directions
        * king_available_directions_coeff
        + board_estimation.black_figures_left * black_figures_left_coeff
        + board_estimation.white_figures_left * white_figures_left_coeff
        + board_estimation.king_available_turns * king_available_turns_coeff
        + shortest_path_to_finish_len * shortest_path_to_finish_len_coeff
    )


def evaluate_best_move(board: Board, bot_coeffs: list[float]) -> TurnCode:
    board_estimations = {}
    for turn in board.get_available_turns():
        probe_board = deepcopy(board)
        if not probe_board.make_turn(turn):
            continue
        white_win = check_game_state(probe_board) == GameState.WHITE_WIN
        black_win = check_game_state(probe_board) == GameState.BLACK_WIN
        board_estimations[turn] = (
            value_function(estimate_board(probe_board), bot_coeffs)
            + white_win * (WIN_VALUE if board.white_turn else -WIN_VALUE)
            + black_win * (-WIN_VALUE if board.white_turn else WIN_VALUE)
        )
    best_turn_value = max(
        estimation for turn, estimation in board_estimations.items()
    )
    best_turns = [
        turn
        for turn, estimation in board_estimations.items()
        if estimation == best_turn_value
    ]
    best_turn = random.choice(best_turns)
    return best_turn
