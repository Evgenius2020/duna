import asyncio
import json

import websockets

from board import Board, TurnCode, CellCoord

board = Board()


def pack_game_state():
    return {
        'type': 'SendGameState',
        'gameState': {
            'boardCells': [
                [{
                    'selected': False,
                    'piece': board.get_field_cell_state(v, h).value
                } for h in range(1, 14)]
                for v in range(13, 0, -1)
            ],
            'gameStatus': {
                'side': 'black',
                'turnStatus': 'black',
                'blackLosses': 0,
                'whiteLosses': 0
            }}
    }


async def serve(websocket):
    async for message in websocket:
        message = json.loads(message)
        if message['type'] == 'GetGameState':
            await websocket.send(json.dumps(pack_game_state()))
        elif message['type'] == 'SendTurn':
            turn = message['turn']
            turn = TurnCode(coord_from=CellCoord(**turn['coordFrom']),
                            coord_to=CellCoord(**turn['coordTo']))
            if board.make_turn(turn):
                await websocket.send(json.dumps(pack_game_state()))


async def main():
    async with websockets.serve(serve, 'localhost', 8765):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
