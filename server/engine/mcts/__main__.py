from engine.board import Board
from engine.board_estimation import check_game_state
from engine.data_types import GameState
from engine.mcts.mcts import MCTS
from engine.mcts.neo4j_client import Neo4jClient
import os

if __name__ == "__main__":
    # Connect to neo4j database
    neo4j_client = Neo4jClient(
        f'bolt://{'NEO4J_HOST'}:{os.getenv('NEO4J_PORT_BOLT')}',
        os.getenv('NEO4J_USERNAME'),
        os.getenv('NEO4J_PASSWORD'),
    )

    # Initialize the board
    board = Board()

    for _ in range(20):
        mcts = MCTS(board, neo4j_client)
        if check_game_state(board) != GameState.PLAYING:
            break
        best_move = mcts.run(iterations_per_move=10)
        print('Best move:', best_move)
        board.make_turn(best_move)
        print(board)

    neo4j_client.close()
