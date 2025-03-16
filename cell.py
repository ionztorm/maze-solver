from line import Line
from point import Point
from window import Window


class Cell:
    def __init__(self, win: Window | None = None) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1: int | None = None
        self._x2: int | None = None
        self._y1: int | None = None
        self._y2: int | None = None
        self._win: Window | None = win

    def draw(self, x1: int, y1: int, x2: int, y2: int) -> None:
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        def wall_color(wall: bool) -> str:
            return "black" if wall else "white"

        left_wall = Line(Point(x1, y1), Point(x1, y2))
        right_wall = Line(Point(x2, y1), Point(x2, y2))
        top_wall = Line(Point(x1, y1), Point(x2, y1))
        bottom_wall = Line(Point(x1, y2), Point(x2, y2))
        self._win.draw_line(left_wall, wall_color(self.has_left_wall))
        self._win.draw_line(right_wall, wall_color(self.has_right_wall))
        self._win.draw_line(top_wall, wall_color(self.has_top_wall))
        self._win.draw_line(bottom_wall, wall_color(self.has_bottom_wall))

    def draw_move(self, to_cell: "Cell", undo: bool = False) -> None:
        line_color = "red" if not undo else "gray"
        if (
            self._x1 is None
            or self._x2 is None
            or self._y1 is None
            or self._y2 is None
        ):
            print("Missing coordinates in current cell, unable to draw_move()")
            return

        from_x = (self._x1 + self._x2) // 2
        from_y = (self._y1 + self._y2) // 2
        if (
            to_cell._x1 is None
            or to_cell._x2 is None
            or to_cell._y1 is None
            or to_cell._y2 is None
        ):
            print("Missing coordinates in target cell, unable to draw_move()")
            return
        to_x = (to_cell._x1 + to_cell._x2) // 2
        to_y = (to_cell._y1 + to_cell._y2) // 2

        line = Line(Point(from_x, from_y), Point(to_x, to_y))
        if self._win is not None:
            self._win.draw_line(line, line_color)
