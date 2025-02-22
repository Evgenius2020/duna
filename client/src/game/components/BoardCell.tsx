import React, { FC, useMemo } from 'react';
import { BoardCellProps, Piece } from "../types";


const BoardCell: FC<BoardCellProps & { onClick: () => void, onMouseEnter: () => void, onMouseLeave: () => void }> =
    ({ selected, piece, onClick, onMouseEnter, onMouseLeave }) => {

        const className = useMemo(() => {
            let className = 'board-cell piece';
            if (selected) {
                className = `${className} selected`;
            }
            if (piece === Piece.King) {
                className = `${className} king`;
            } else if (piece === Piece.Black) {
                className = `${className} black`;
            } else if (piece === Piece.White) {
                className = `${className} white`;
            }
            return className;
        }, [selected, piece]);

        return (
            <button
                className={className}
                onClick={onClick}
                onMouseEnter={onMouseEnter}
                onMouseLeave={onMouseLeave}
            />
        );
    };
export default BoardCell