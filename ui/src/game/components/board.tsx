import React, {FC, useState} from 'react';

import BoardCell from "./board_cell";
import {BoardCells, Coord} from "../types";

const Board: FC<
    {
        cells: BoardCells,
        changeCellSelected: (coord: Coord, value: boolean) => void
        onTurnAttempt: (coord_from: Coord,
                        coord_to: Coord) => void
    }> = ({cells, changeCellSelected, onTurnAttempt}) => {


    const [lastSelection, setLastSelection] =
        useState({
            initialized: false,
            vertical: 0,
            horizontal: 0
        });

    const onCellSelect = (newSelection: Coord) => {
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

    return (
        <div className='board'>{cells.map(
            (row, row_idx) => (
                <div key={row_idx}>{
                    row.map(
                        (cellProps,
                         cell_idx) => (
                            <BoardCell key={cell_idx}
                                       {...cellProps}
                                       onClick={() =>
                                           onCellSelect({
                                               vertical: row_idx,
                                               horizontal: cell_idx
                                           })}/>
                        ))
                }</div>)
        )}</div>);
}

export default Board;
