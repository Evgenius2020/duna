export enum Piece {
    White = 'w',
    Black = 'b',
    King = 'k',
    Empty = ''
}


export type Coord = {
    vertical: number;
    horizontal: number;
}

export enum TurnStatus {
    Black = 'black',
    White = 'white'
}

export type BoardCellProps = {
    selected: boolean;
    piece: Piece
}

export type BoardCells = BoardCellProps[][];

export type GameStatusProps = {
    turnStatus: TurnStatus,
    blackLosses: number,
    whiteLosses: number
}