from copy import deepcopy

from engine.board import Board
from engine.board_estimation import (
    estimate_board,
    EstimationResult,
    check_game_state,
)
from engine.data_types import GameState
import random


def value_function(board_estimation: EstimationResult, side_is_white: bool):
    shortest_path_to_finish_len = (
        10
        if board_estimation.shortest_path_to_finish_len is None
        else board_estimation.shortest_path_to_finish_len
    )
    white_win = board_estimation.game_state == GameState.WHITE_WIN
    black_win = board_estimation.game_state == GameState.BLACK_WIN
    if side_is_white:
        return (
            board_estimation.king_available_directions * -25
            + board_estimation.black_figures_left * -10
            + board_estimation.white_figures_left * 5
            + board_estimation.king_available_turns * -1
            + shortest_path_to_finish_len * 10
            + white_win * 100
            + black_win * -100
        )
    else:
        return (
            board_estimation.king_available_directions * 10
            + board_estimation.black_figures_left * 5
            + board_estimation.white_figures_left * -2
            + board_estimation.king_available_turns
            + shortest_path_to_finish_len * -10
            + white_win * -100
            + black_win * 100
        )


if __name__ == '__main__':
    board = Board()
    turn_number = 1
    while check_game_state(board) == GameState.PLAYING:
        side_is_white = board.white_turn
        board_estimations = {}
        for turn in board.get_available_turns():
            probe_board = deepcopy(board)
            if not probe_board.make_turn(turn):
                continue
            board_estimations[turn] = value_function(
                estimate_board(probe_board), side_is_white
            )
        if not board_estimations:
            break
        best_turns = [
            turn
            for (turn, _) in sorted(
                board_estimations.items(), key=lambda _: _[1], reverse=True
            )
        ]
        if side_is_white:
            best_turn = random.choice(best_turns[:1])
        else:
            best_turn = random.choice(best_turns[:1])
        print(best_turn)
        board.make_turn(best_turn)
        print(
            'turn',
            turn_number,
            'white' if side_is_white else 'black',
            best_turn,
            estimate_board(board),
        )
        print(board)
        turn_number += 1
    print('game finished!')
