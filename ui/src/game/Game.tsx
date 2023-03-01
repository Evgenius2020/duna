import React, {FC, useCallback, useMemo, useRef, useState} from 'react';
import Board from "./components/Board";
import {
    BoardCellProps,
    BoardCells,
    Coord, GameState,
    GameStatusProps,
    Piece,
    Side,
    Turn
} from "./types";
import GameStatus from "./components/GameStatus";
import {WsClient} from "./WsClient";

const Game: FC = () => {

    const [cells, setCells] =
        useState<BoardCells>(() =>
            Array.from({length: 13}).map(
                () => Array.from({length: 13}).map(
                    () => ({
                        selected: false,
                        piece: Piece.Empty
                    })))
        );

    const [gameStatusProps, setGameStatusProps] =
        useState<GameStatusProps>(() => {
            return {
                turnStatus: Side.Black,
                side: Side.Black,
                blackLosses: 0,
                whiteLosses: 0
            }
        });

    const wsClient = useMemo(
        () => new WsClient(
            (gameState: GameState) => {
                setGameStatusProps(gameState.gameStatus);
                setCells(gameState.boardCells);
            }), []);

    const changeCell = useCallback(
        (
            coord: Coord,
            cellProps: BoardCellProps) => {
            setCells(prevState => {
                const newState = [...prevState];
                newState[coord.vertical] = [...newState[coord.vertical]];
                newState[coord.vertical][coord.horizontal] = {
                    ...prevState[coord.vertical][coord.horizontal],
                    selected: cellProps.selected,
                    piece: cellProps.piece
                }
                return newState;
            });
        }, []);

    const onTurnAttempt = (turn: Turn) => {
        turn.coordFrom = {
            vertical: 12 - turn.coordFrom.vertical + 1,
            horizontal: turn.coordFrom.horizontal + 1,
        }
        turn.coordTo = {
            vertical: 12 - turn.coordTo.vertical + 1,
            horizontal: turn.coordTo.horizontal + 1,
        };
        wsClient.sendTurn(turn);
    }

    return (
        <div className='game'>
            <Board
                cells={cells}
                changeCellSelected={(coord: Coord,
                                     selected: boolean) =>
                    changeCell(coord, {
                        ...cells[coord.vertical][coord.horizontal],
                        selected: selected,
                    })}
                onTurnAttempt={onTurnAttempt}/>
            <GameStatus
                gameStatusProps={gameStatusProps}/>
        </div>);
}

export default Game;
