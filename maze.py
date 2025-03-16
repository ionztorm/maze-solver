import time

from cell import Cell
from window import Window


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window | None = None,
    ) -> None:
        self._cells: list[list[Cell]] = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        self._break_entrance_and_exit()

    def _create_cells(self) -> None:
        for _ in range(self._num_cols):
            col = []
            for _ in range(self._num_rows):
                col.append(Cell(self._win))
            self._cells.append(col)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int) -> None:
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self) -> None:
        if self._win is not None:
            self._win.redraw()
            time.sleep(0.05)

    def _break_entrance_and_exit(self) -> None:
        if self._cells is not None:
            self._cells[0][0].has_top_wall = False
            self._cells[-1][-1].has_bottom_wall = False
            self._draw_cell(0, 0)
            self._draw_cell(self._num_cols - 1, self._num_rows - 1)
