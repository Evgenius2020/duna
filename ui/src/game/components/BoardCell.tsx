import React, {FC, useMemo} from 'react';
import {BoardCellProps, Piece} from "../types";


const BoardCell:
    FC<BoardCellProps & { onClick: () => void }> =
    ({selected, piece, onClick}) => {

        const className = useMemo(() => {
            let className = 'board-cell piece'
            if (selected) {
                className = `${className} selected`
            }
            if (piece == Piece.King) {
                className = `${className} king`
            } else if (piece == Piece.Black) {
                className = `${className} black`
            } else if (piece == Piece.White) {
                className = `${className} white`
            }
            return className
        }, [selected, piece])

        return (<button
            className={className}
            onClick={() => onClick()}/>);
    }

export default BoardCell