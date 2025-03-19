import time
import random

from cell import Cell
from window import Window


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: float,
        cell_size_y: float,
        win: Window | None = None,
        seed: int | None = None,
    ) -> None:
        self._cells: list[list[Cell]] = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self) -> None:
        for _ in range(self._num_cols):
            col = []
            for _ in range(self._num_rows):
                col.append(Cell(self._win))
            self._cells.append(col)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, col_idx: int, row_idx: int) -> None:
        x1 = self._x1 + col_idx * self._cell_size_x
        y1 = self._y1 + row_idx * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[col_idx][row_idx].draw(x1, y1, x2, y2)
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

    def _break_walls_r(self, col_idx: int, row_idx: int) -> None:
        self._cells[col_idx][row_idx]._visited = True
        while True:
            to_visit: list = []

            if col_idx > 0 and not self._cells[col_idx - 1][row_idx]._visited:
                to_visit.append((col_idx - 1, row_idx))  # Left
            if (
                col_idx < self._num_cols - 1
                and not self._cells[col_idx + 1][row_idx]._visited
            ):
                to_visit.append((col_idx + 1, row_idx))  # Right
            if row_idx > 0 and not self._cells[col_idx][row_idx - 1]._visited:
                to_visit.append((col_idx, row_idx - 1))  # Up
            if (
                row_idx < self._num_rows - 1
                and not self._cells[col_idx][row_idx + 1]._visited
            ):
                to_visit.append((col_idx, row_idx + 1))  # Down

            if len(to_visit) == 0:
                self._draw_cell(col_idx, row_idx)
                return

            direction_idx = random.randrange(len(to_visit))  # noqa: S311
            next_cell = to_visit[direction_idx]
            next_col, next_row = next_cell

            # Check column of the first neighbor (Right)
            if next_col == col_idx + 1:
                self._cells[col_idx][row_idx].has_right_wall = False
                self._cells[col_idx + 1][row_idx].has_left_wall = False

            # Check column of the first neighbor (Left)
            if next_col == col_idx - 1:
                self._cells[col_idx][row_idx].has_left_wall = False
                self._cells[col_idx - 1][row_idx].has_right_wall = False

            # Check row of the second neighbor (Down)
            if next_row == row_idx + 1:
                self._cells[col_idx][row_idx].has_bottom_wall = False
                self._cells[col_idx][row_idx + 1].has_top_wall = False

            # Check row of the second neighbor (Up)
            if next_row == row_idx - 1:
                self._cells[col_idx][row_idx].has_top_wall = False
                self._cells[col_idx][row_idx - 1].has_bottom_wall = False

            self._break_walls_r(next_col, next_row)

    def _reset_cells_visited(self) -> None:
        for col in self._cells:
            for cell in col:
                cell._visited = False

    def solve(self) -> bool:
        return self._solve_r(0, 0)

    def _solve_r(self, col_idx: int = 0, row_idx: int = 0) -> bool:
        self._animate()
        self._cells[col_idx][row_idx]._visited = True
        if self._cells[col_idx][row_idx] == self._cells[-1][-1]:
            return True

        # Move left
        if (
            col_idx > 0
            and not self._cells[col_idx][row_idx].has_left_wall
            and not self._cells[col_idx - 1][row_idx]._visited
        ):
            self._cells[col_idx][row_idx].draw_move(
                self._cells[col_idx - 1][row_idx]
            )
            if self._solve_r(col_idx - 1, row_idx):
                return True
            self._cells[col_idx][row_idx].draw_move(
                self._cells[col_idx - 1][row_idx], True
            )

        # Move right
        if (
            col_idx < self._num_cols - 1
            and not self._cells[col_idx][row_idx].has_right_wall
            and not self._cells[col_idx + 1][row_idx]._visited
        ):
            self._cells[col_idx][row_idx].draw_move(
                self._cells[col_idx + 1][row_idx]
            )
            if self._solve_r(col_idx + 1, row_idx):
                return True
            self._cells[col_idx][row_idx].draw_move(
                self._cells[col_idx + 1][row_idx], True
            )

        # Move up
        if (
            row_idx > 0
            and not self._cells[col_idx][row_idx].has_top_wall
            and not self._cells[col_idx][row_idx - 1]._visited
        ):
            self._cells[col_idx][row_idx].draw_move(
                self._cells[col_idx][row_idx - 1]
            )
            if self._solve_r(col_idx, row_idx - 1):
                return True
            self._cells[col_idx][row_idx].draw_move(
                self._cells[col_idx][row_idx - 1], True
            )

        # Move down
        if (
            row_idx < self._num_rows - 1
            and not self._cells[col_idx][row_idx].has_bottom_wall
            and not self._cells[col_idx][row_idx + 1]._visited
        ):
            self._cells[col_idx][row_idx].draw_move(
                self._cells[col_idx][row_idx + 1]
            )
            if self._solve_r(col_idx, row_idx + 1):
                return True
            self._cells[col_idx][row_idx].draw_move(
                self._cells[col_idx][row_idx + 1], True
            )

        return False
