import React, {FC, useMemo} from 'react';
import {BoardCellProps} from "./types.ts";


const BoardCell: FC<BoardCellProps &
    { onClick: () => void }> =
    ({selected, onClick}) => {
        const className = useMemo(() => {
            let className = 'board-cell'
            if (selected) {
                className = `${className} selected`
            }
            return className
        }, [selected])
        return (<button
            className={className}
            onClick={() => onClick()}/>);
    }

export default BoardCell