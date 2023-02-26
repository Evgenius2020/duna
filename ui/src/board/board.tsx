import React, {useCallback, useState} from 'react';

import BoardCell from "./board_cell";
import {BoardCells, Coord} from "./types.ts";

export default class Board extends React.Component<
    {
        onTurnAttempt: (coord_from: Coord,
                        coord_to: Coord) => void
    }> {
    private lastSelection?: Coord = undefined;

    private onCellSelect(newSelection: Coord,
                         changeCellSelected: (row_idx: number,
                                              cell_idx: number,
                                              value: boolean) => void): void {
        if (!this.lastSelection) {
            // Turn started.
            this.lastSelection = newSelection;
            changeCellSelected(
                newSelection.vertical,
                newSelection.horizontal,
                true);
        }
        if ((this.lastSelection.vertical != newSelection.vertical) ||
            (this.lastSelection.horizontal != newSelection.horizontal)) {
            // Turn selected.
            this.props.onTurnAttempt(this.lastSelection, newSelection);
            changeCellSelected(
                this.lastSelection.vertical,
                this.lastSelection.horizontal,
                false);
        } else {
            // Turn canceled
            this.lastSelection = undefined;
        }
    }

    render() {
        const [cells, setState] = useState<BoardCells>(
            Array.from({length: 13}).map(
                () => Array.from({length: 13}).map(
                    () => ({selected: false}))
            )
        );
        const changeCellSelected = useCallback(
            (
                row_idx: number,
                cell_idx: number,
                value: boolean) => {
                if (cells[row_idx][cell_idx].selected === value) {
                    return;
                }
                setState(prevState => {
                    const newState = [...prevState];
                    newState[row_idx] = [...newState[row_idx]];
                    newState[row_idx][cell_idx] = {
                        ...prevState[row_idx][cell_idx],
                        selected: value,
                    }
                    return newState;
                });
            }, []);
        return cells.map((row, row_idx) => (
            <div key={row_idx}>{
                row.map((cellProps, cell_idx) => (
                    <BoardCell key={cell_idx}
                               selected={cellProps.selected}
                               onClick={() => this.onCellSelect({
                                   vertical: row_idx,
                                   horizontal: cell_idx
                               }, changeCellSelected)}/>
                ))
            }</div>)
        );
    }
}
