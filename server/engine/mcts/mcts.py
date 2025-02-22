from copy import deepcopy

from tqdm import tqdm

from engine.board import Board
from engine.board_estimation import check_game_state, estimate_board
from engine.data_types import GameState, TurnCode
from engine.mcts.board_estimation_cache import InMemoryCache
from engine.mcts.constants import MAX_SIMULATION_DEPTH, ITERATIONS_PER_MOVE
from engine.mcts.evaluate_best_move import evaluate_best_move
from engine.mcts.neo4j_client import Neo4jClient


class MCTS:
    neo4j_client: Neo4jClient

    def __init__(self, neo4j_client):
        self.neo4j_client = neo4j_client
        self.board_estimation_cache = InMemoryCache()

    def simulate(self, node_id: int, board: Board) -> (int, GameState):
        current_depth = 0
        # Случайная симуляция игры
        while (check_game_state(board) == GameState.PLAYING) and (
            (current_depth := current_depth + 1) <= MAX_SIMULATION_DEPTH
        ):
            best_move = evaluate_best_move(
                board,
                estimate_board_func=lambda board: self.board_estimation_cache.get(
                    str(board), lambda: estimate_board(board)
                ),
            )
            board.make_turn(best_move)
            node_id = self.neo4j_client.create_node_or_get_exists(
                board, parent_id=node_id, edge_name=str(best_move)
            )
        return node_id, check_game_state(board)

    def manual_move(self, board: Board, turn: TurnCode):
        current_node_id = self.neo4j_client.find_node_by_board(board)
        board.make_turn(turn)
        next_node_id = self.neo4j_client.create_node_or_get_exists(
            board, parent_id=current_node_id, edge_name=str(turn)
        )
        self.backpropagate(next_node_id, estimate_board(board))

    def backpropagate(self, node_id, result: GameState):
        white_wins = 1 if result == GameState.WHITE_WIN else 0
        black_wins = 1 if result == GameState.BLACK_WIN else 0
        while node_id is not None:
            self.neo4j_client.increment_node(
                node_id, white_wins=white_wins, black_wins=black_wins, visits=1
            )
            node_id = self.neo4j_client.get_parent(node_id)

    def run(self, board: Board) -> TurnCode:
        # Each iteration, create 'iterations_per_move' random simulations
        for _ in tqdm(range(ITERATIONS_PER_MOVE)):
            # Selection
            root_id = self.neo4j_client.create_node_or_get_exists(board)

            # Simulation + expansion (in-depth)
            simulation_board = deepcopy(board)
            end_node_id, result = self.simulate(root_id, simulation_board)

            # Backpropagation
            self.backpropagate(end_node_id, result)

        # Return best move
        return TurnCode.from_str(self.neo4j_client.get_best_move(board))
