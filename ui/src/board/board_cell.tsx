import React, {FC, useMemo} from 'react';
import {BoardCellProps, Piece} from "./types.ts";


const BoardCell: FC<BoardCellProps &
    { onClick: () => void }> =
    ({selected, piece, onClick}) => {
        const className = useMemo(() => {
            let className = 'board-cell'
            if (selected) {
                className = `${className} selected`
            }
            if (piece == Piece.king) {
                className = `${className} piece-king`
            } else if (piece == Piece.black) {
                className = `${className} piece-black`
            } else if (piece == Piece.white) {
                className = `${className} piece-white`
            }

            return className
        }, [selected])
        return (<button
            className={className}
            onClick={() => onClick()}/>);
    }

export default BoardCell