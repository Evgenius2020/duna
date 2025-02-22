import React, { FC, useState } from 'react';

import BoardCell from "./BoardCell";
import { BoardCells, Coord, Turn } from "../types";

const Board: FC<
    {
        cells: BoardCells,
        changeCellSelected: (coord: Coord, value: boolean) => void
        onTurnAttempt: (turn: Turn) => void
    }> = ({ cells, changeCellSelected, onTurnAttempt }) => {


        const [lastSelection, setLastSelection] =
            useState({
                initialized: false,
                vertical: 0,
                horizontal: 0
            });

        const onCellSelect = (newSelection: Coord) => {
            if (!lastSelection.initialized) {
                // Turn started.
                setLastSelection({ ...newSelection, initialized: true });
                changeCellSelected(newSelection, true);
            } else if ((lastSelection.vertical != newSelection.vertical) ||
                (lastSelection.horizontal != newSelection.horizontal)) {
                // Turn selected.
                if ((lastSelection.vertical == newSelection.vertical) ||
                    (lastSelection.horizontal == newSelection.horizontal)) {
                    // Valid move.
                    changeCellSelected(lastSelection, false);
                    setLastSelection({ ...newSelection, initialized: false });
                    onTurnAttempt({
                        coordFrom: lastSelection,
                        coordTo: newSelection
                    });
                } else {
                    // Invalid move (start from another cell).
                    changeCellSelected(lastSelection, false);
                    setLastSelection({ ...newSelection, initialized: true });
                    changeCellSelected(newSelection, true);
                }
            } else {
                // Turn canceled
                changeCellSelected(lastSelection, false);
                setLastSelection({ ...newSelection, initialized: false });
            }
        }

        const [tooltip, setTooltip] = useState({ visible: false, x: 0, y: 0 });

        const handleMouseEnter = (row: number, col: number) => {
            setTooltip({ visible: true, x: col, y: row });
        };

        const handleMouseLeave = () => {
            setTooltip({ ...tooltip, visible: false });
        };

        return (
            <div className='board'>
                {cells.map((row, row_idx) => (
                    <div key={row_idx}>
                        {row.map((cellProps, cell_idx) => (
                            <BoardCell
                                key={cell_idx}
                                {...cellProps}
                                onClick={() => onCellSelect({ vertical: row_idx, horizontal: cell_idx })}
                                onMouseEnter={() => handleMouseEnter(row_idx, cell_idx)}
                                onMouseLeave={handleMouseLeave}
                            />
                        ))}
                    </div>
                ))}
                {tooltip.visible && (
                    <div className="tooltip" style={{ top: tooltip.y * 50 + 35, left: tooltip.x * 50 + 20 }}>
                        {`(${(13 - tooltip.y).toString(16).toUpperCase()}, ${(tooltip.x + 1).toString(16).toUpperCase()})`}
                    </div>
                )}
            </div>);
    }

export default Board;
