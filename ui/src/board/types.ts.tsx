export type BoardCellProps = {
    selected: boolean;
}

export type BoardCells = BoardCellProps[][];

export type Coord = {
    vertical: number;
    horizontal: number;
}