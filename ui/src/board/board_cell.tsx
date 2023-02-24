import React from 'react';

type BoardCellProp = {
    onSelectionChange: () => boolean;
}

type BoardCellState = {
    selected: boolean;
}

class BoardCell extends React.Component<BoardCellProp, BoardCellState> {
    constructor(p: BoardCellProp) {
        super(p);
        this.state = {
            selected: false
        };
    }

    public changeSelection(selected: boolean) {
        this.setState({
            selected: selected
        });
    }

    render() {
        return <button
            className={`board-cell${this.state.selected ? ' selected' : ''}`}
            onClick={() => this.changeSelection(
                this.props.onSelectionChange())}/>;
    };
}

export default BoardCell