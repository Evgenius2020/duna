from engine.board import Board
from engine.board_estimation import check_game_state
from engine.data_types import GameState
from engine.mcts.constants import TURN_COUNT
from engine.mcts.mcts import MCTS
from engine.mcts.neo4j_client import Neo4jClient
import os

if __name__ == "__main__":
    # Connect to neo4j database
    neo4j_client = Neo4jClient(
        f'bolt://{os.getenv('NEO4J_HOST')}:{os.getenv('NEO4J_PORT_BOLT')}',
        os.getenv('NEO4J_USERNAME'),
        os.getenv('NEO4J_PASSWORD'),
    )

    # Initialize the board
    board = Board()

    for turn_count in range(TURN_COUNT):
        if check_game_state(board) != GameState.PLAYING:
            break

        mcts = MCTS(neo4j_client)
        best_move = mcts.run(board)
        board.make_turn(best_move)

        print(
            f'Turn #{turn_count+1}, '
            f'White turn: {not board.white_turn}, '
            f'Best move: {best_move}'
        )
        print(board)
        print(f'cache stats: {mcts.board_estimation_cache.get_stats()}')
        mcts.board_estimation_cache.save()

    neo4j_client.close()
