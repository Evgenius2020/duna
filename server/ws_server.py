import asyncio
import json
import os

import websockets

from engine.board import Board
from engine.board_estimation import estimate_board
from engine.data_types import TurnCode, CellCoordinates, GameState
from engine.mcts.mcts import MCTS
from engine.mcts.neo4j_client import Neo4jClient
from game_logger import CSVLogger

board = Board()
INITIAL_WHITE_FIGURES = estimate_board(board).white_figures_left
INITIAL_BLACK_FIGURES = estimate_board(board).black_figures_left
neo4j_client = Neo4jClient(
    f'bolt://{os.getenv('NEO4J_HOST')}:{os.getenv('NEO4J_PORT_BOLT')}',
    os.getenv('NEO4J_USERNAME'),
    os.getenv('NEO4J_PASSWORD'),
)
mcts = MCTS(neo4j_client)
logger = CSVLogger()


def make_bot_turn():
    best_move = mcts.run(board)
    board.make_turn(best_move)
    # Inverted because turn already taken
    logger.log([('white' if not board.white_turn else 'black'), str(best_move)])
    print('bot turn:', best_move)
    print(f'cache stats: {mcts.board_estimation_cache.get_stats()}')
    mcts.board_estimation_cache.save()


make_bot_turn()


def pack_game_state():
    return {
        'type': 'SendGameState',
        'gameState': {
            'boardCells': [
                [
                    {'piece': board.get_field_cell_state(v, h).value}
                    for h in range(1, 14)
                ]
                for v in range(13, 0, -1)
            ],
            'gameStatus': {
                'side': 'white',
                'turnStatus': 'white' if board.white_turn else 'black',
                'blackLosses': INITIAL_BLACK_FIGURES
                - estimate_board(board).black_figures_left,
                'whiteLosses': INITIAL_WHITE_FIGURES
                - estimate_board(board).white_figures_left,
            },
        },
    }


async def serve(websocket):
    async for message in websocket:
        message = json.loads(message)
        if message['type'] == 'GetGameState':
            await websocket.send(json.dumps(pack_game_state()))
        elif message['type'] == 'SendTurn':
            turn = message['turn']
            turn = TurnCode(
                coord_from=CellCoordinates(**turn['coordFrom']),
                coord_to=CellCoordinates(**turn['coordTo']),
            )
            if board.make_turn(turn):
                logger.log(
                    [('white' if not board.white_turn else 'black'), str(turn)]
                )
                print('player turn:', turn)

                await websocket.send(json.dumps(pack_game_state()))
                if estimate_board(board).game_state != GameState.PLAYING:
                    logger.log(estimate_board(board).game_state)
                    print('game over')
                    return

                # Sync mcts board with game board
                mcts.manual_move(board, turn)
                make_bot_turn()
                await websocket.send(json.dumps(pack_game_state()))
                if estimate_board(board).game_state != GameState.PLAYING:
                    logger.log(estimate_board(board).game_state)
                    print('game over')
                    return


async def main():
    async with websockets.serve(serve, 'localhost', 8765):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
