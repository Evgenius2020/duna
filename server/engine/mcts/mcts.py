from copy import deepcopy

from tqdm import tqdm

from engine.board import Board
from engine.board_estimation import check_game_state
from engine.mcts.evaluate_best_move import evaluate_best_move
from engine.data_types import GameState, TurnCode
from engine.mcts.constants import MAX_SIMULATION_DEPTH
from engine.mcts.neo4j_client import Neo4jClient


class MCTS:
    board: Board
    neo4j_client: Neo4jClient

    def __init__(self, board, neo4j_client):
        self.board = board
        self.neo4j_client = neo4j_client

    @staticmethod
    def uct(node, is_white_turn) -> float:
        # UCT (Upper Confidence Bound for Trees) formula (hard-coded)
        if node["visits"] == 0:
            return float("inf")
        wins = node["white_wins"] if is_white_turn else node["black_wins"]
        return wins / node["visits"] + 1.41 * (2 * (node["visits"] ** 0.5))

    def select(self, node_id, is_white_turn) -> int:
        children = self.neo4j_client.get_children(node_id)
        if not children:
            return node_id
        return max(children, key=lambda node: self.uct(node, is_white_turn))[
            "id"
        ]

    def expand(self, node_id) -> None:
        available_turns = self.board.get_available_turns()
        for turn in available_turns:
            new_board = deepcopy(self.board)
            new_board.make_turn(turn)
            self.neo4j_client.create_node(
                new_board, parent_id=node_id, edge_name=str(turn)
            )

    @staticmethod
    def simulate(board: Board) -> GameState:
        current_depth = 0
        # Случайная симуляция игры
        while (check_game_state(board) == GameState.PLAYING) and (
            current_depth < MAX_SIMULATION_DEPTH
        ):
            best_move = evaluate_best_move(board)
            board.make_turn(best_move)
            current_depth += 1
        return check_game_state(board)

    def backpropagate(self, node_id, result: GameState):
        white_wins = 1 if result == GameState.WHITE_WIN else 0
        black_wins = 1 if result == GameState.BLACK_WIN else 0
        while node_id is not None:
            self.neo4j_client.increment_node(
                node_id, white_wins=white_wins, black_wins=black_wins, visits=1
            )
            node_id = self.neo4j_client.get_parent(node_id)

    def run(self, iterations_per_move: int):
        # Get root node, create if not exists
        root_id = self.neo4j_client.find_node_by_board(self.board)
        if root_id is None:
            root_id = self.neo4j_client.create_node(self.board)

        for _ in tqdm(range(iterations_per_move)):
            # 1. Selection
            node_id = self.select(root_id, self.board.white_turn)

            # 2. Expansion
            self.expand(node_id)

            # 3. Simulation
            board_copy = deepcopy(self.board)
            result = self.simulate(board_copy)

            # 4. Backpropagation
            self.backpropagate(node_id, result)

        # Return best move
        return TurnCode.from_str(
            self.neo4j_client.get_best_move(root_id, self.board.white_turn)
        )
