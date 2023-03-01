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

export type Turn = {
    coordFrom: Coord,
    coordTo: Coord
}

export enum Side {
    Black = 'black',
    White = 'white'
}

export type BoardCellProps = {
    selected: boolean;
    piece: Piece
}

export type BoardCells = BoardCellProps[][];

export type GameStatusProps = {
    side: Side
    turnStatus: Side,
    blackLosses: number,
    whiteLosses: number
}

export type GameState = {
    gameStatus: GameStatusProps,
    boardCells: BoardCells
};