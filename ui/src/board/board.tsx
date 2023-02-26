import React, {FC, useCallback, useState} from 'react';

import BoardCell from "./board_cell";
import {BoardCells, Coord} from "./types.ts";

const Board: FC<
    {
        onTurnAttempt: (coord_from: Coord,
                        coord_to: Coord) => void
    }> = ({onTurnAttempt}) => {

    const [lastSelection, setLastSelection] =
        useState({
            initialized: false,
            vertical: 0,
            horizontal: 0
        });

    const onCellSelect = (newSelection: Coord,
                          changeCellSelected: (coord: Coord,
                                               value: boolean) => void) => {
        if (!lastSelection.initialized) {
            // Turn started.
            setLastSelection({...newSelection, initialized: true});
            changeCellSelected(newSelection, true);
        } else if ((lastSelection.vertical != newSelection.vertical) ||
            (lastSelection.horizontal != newSelection.horizontal)) {
            // Turn selected.
            if ((lastSelection.vertical == newSelection.vertical) ||
                (lastSelection.horizontal == newSelection.horizontal)) {
                // Valid move.
                changeCellSelected(lastSelection, false);
                setLastSelection({...newSelection, initialized: false});
                onTurnAttempt(lastSelection, newSelection);
            } else {
                // Invalid move (start from another cell).
                changeCellSelected(lastSelection, false);
                setLastSelection({...newSelection, initialized: true});
                changeCellSelected(newSelection, true);
            }
        } else {
            // Turn canceled
            changeCellSelected(lastSelection, false);
            setLastSelection({...newSelection, initialized: false});
        }
    }

    const [cells, setState] = useState<BoardCells>(
        Array.from({length: 13}).map(
            () => Array.from({length: 13}).map(
                () => ({selected: false}))
        )
    );
    const changeCellSelected = useCallback(
        (
            coord: Coord,
            value: boolean) => {
            setState(prevState => {
                const newState = [...prevState];
                newState[coord.vertical] = [...newState[coord.vertical]];
                newState[coord.vertical][coord.horizontal] = {
                    ...prevState[coord.vertical][coord.horizontal],
                    selected: value,
                }
                return newState;
            });
        }, []);

    return (
        <div>{cells.map(
            (row, row_idx) => (
                <div key={row_idx}>{
                    row.map(
                        (cellProps, cell_idx) => (
                            <BoardCell key={cell_idx}
                                       selected={cellProps.selected}
                                       onClick={() => onCellSelect({
                                           vertical: row_idx,
                                           horizontal: cell_idx
                                       }, changeCellSelected)}/>
                        ))
                }</div>)
        )}</div>);
}

export default Board;
