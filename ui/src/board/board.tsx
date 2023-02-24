import React from 'react';

import BoardCell from "./board_cell";

type Coord = {
    vertical: number;
    horizontal: number;
}

type BoardProp = {
    onTurnAttempt: (coord_from: Coord,
                    coord_to: Coord) => void
}

export default class Board extends React.Component<BoardProp> {
    private lastSelection?: Coord = undefined;
    private cells: Array<Array<React.ReactElement>> = [[]];

    private onCellSelect(newSelection: Coord): boolean {
        if (!this.lastSelection) {
            // Turn started.
            this.lastSelection = newSelection;
            return true;
        }
        if ((this.lastSelection.vertical != newSelection.vertical) ||
            (this.lastSelection.horizontal != newSelection.horizontal)) {
            // Turn selected.
            this.props.onTurnAttempt(this.lastSelection, newSelection);
            let lastSelectionCell: BoardCell =
                this.cells[13 - this.lastSelection.vertical - 1]
                    [13 - this.lastSelection.horizontal] as any as BoardCell;
            console.log(this.cells);
            lastSelectionCell.changeSelection(false);
            return false;
        } else {
            // Turn canceled
            this.lastSelection = undefined;
            return false;
        }
    }

    render() {
        this.cells = [];
        let board_lines = [];
        for (let vertical = 13; vertical >= 1; vertical--) {
            const boardRow = [];
            for (let horizontal = 1; horizontal <= 13; horizontal++) {
                boardRow.push(
                    <BoardCell
                        onSelectionChange={() => this.onCellSelect({
                            vertical: vertical,
                            horizontal: horizontal
                        })}
                        key={`${vertical}-${horizontal}`}
                    />);
            }
            this.cells.push(boardRow);
            board_lines.push(
                <div className="board-row" key={vertical}>
                    {boardRow}
                </div>)
        }

        return (
            <div>
                {board_lines}
            </div>
        );
    }
}