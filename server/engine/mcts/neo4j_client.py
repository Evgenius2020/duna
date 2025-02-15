from neo4j import GraphDatabase

from engine.board import Board
from engine.board_estimation import estimate_board
import neo4j_queries as queries


class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, board: Board, parent_id=None, edge_name=None):
        with self.driver.session() as session:
            result = session.execute_write(
                queries.create_node_query,
                str(board),
                str(estimate_board(board)),
                parent_id,
                edge_name,
            )
            return result

    def find_node_by_board(self, board: Board):
        with self.driver.session() as session:
            result = session.execute_read(
                queries.find_node_by_board_query, str(board)
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

    def get_children(self, node_id):
        with self.driver.session() as session:
            result = session.execute_read(queries.get_children_query, node_id)
            return result

    def get_parent(self, node_id):
        with self.driver.session() as session:
            result = session.execute_read(queries.get_parent_query, node_id)
            return result

    def get_best_move(self, root_id, is_white_turn):
        with self.driver.session() as session:
            result = session.execute_read(
                queries.get_best_move_query, root_id, is_white_turn
            )
            return result
