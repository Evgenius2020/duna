import React, {FC, useCallback, useState} from 'react';
import Board from "./components/Board";
import {
    BoardCellProps,
    BoardCells,
    Coord,
    GameStatusProps,
    Piece,
    TurnStatus
} from "./types";
import GameStatus from "./components/GameStatus";

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
                turnStatus: TurnStatus.Black,
                blackLosses: 0,
                whiteLosses: 0
            }
        });

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

    const onTurnAttempt = (coordFrom: Coord,
                           coordTo: Coord) => {
        coordFrom = {
            vertical: 12 - coordFrom.vertical + 1,
            horizontal: coordFrom.horizontal + 1,
        }
        coordTo = {
            vertical: 12 - coordTo.vertical + 1,
            horizontal: coordTo.horizontal + 1,
        };
        console.log(coordFrom, coordTo);
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
