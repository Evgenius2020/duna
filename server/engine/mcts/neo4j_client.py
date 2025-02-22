from neo4j import GraphDatabase

from engine.board import Board
from engine.board_estimation import estimate_board
from engine.mcts import neo4j_queries as queries


class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node_or_get_exists(
        self, board: Board, parent_id=None, edge_name=None
    ):
        if node_id := self.find_node_by_board(board):
            return node_id
        with self.driver.session() as session:
            node_id = session.execute_write(
                queries.create_node_query,
                str(board),
                board.white_turn,
                str(estimate_board(board)),
                parent_id,
                edge_name,
            )
            return node_id

    def find_node_by_board(self, board: Board):
        with self.driver.session() as session:
            result = session.execute_read(
                queries.find_node_by_board_query, str(board), board.white_turn
            )
            return result

    def increment_node(self, node_id, white_wins, black_wins, visits):
        with self.driver.session() as session:
            session.execute_write(
                queries.increment_node_query,
                node_id,
                white_wins,
                black_wins,
                visits,
            )

    def get_parent(self, node_id):
        with self.driver.session() as session:
            result = session.execute_read(queries.get_parent_query, node_id)
            return result

    def get_best_move(self, board: Board):
        with self.driver.session() as session:
            result = session.execute_read(
                queries.get_best_move_query, str(board), board.white_turn
            )
            return result
