import React, {useMemo} from 'react';
import {BoardCellProps} from "./types.ts";


export default class BoardCell extends React.Component<BoardCellProps &
    { onClick: () => void }> {

    render() {
        const className = useMemo(() => {
            let className = 'board-cell'
            if (this.props.selected) {
                className = `${className} selected`
            }
            return className
        }, [this.props.selected])
        return <button
            className={className}
            onClick={() => this.props.onClick()}/>;
    };
}