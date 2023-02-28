export type BoardCellProps = {
    selected: boolean;
    piece: Piece
}

export enum Piece {
    white= 'white',
    black = 'black',
    king = 'king',
    empty = ''
}

export type BoardCells = BoardCellProps[][];

export type Coord = {
    vertical: number;
    horizontal: number;
}