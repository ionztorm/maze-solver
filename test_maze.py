import unittest

from maze import Maze

NUM_COLS = 12
NUM_ROWS = 10


class Tests(unittest.TestCase):
    def setUp(self, num_rows: int = 10, num_cols: int = 12) -> None:
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.maze = Maze(0, 0, self.num_rows, self.num_cols, 10, 10)

    def test_maze_create_cells(self) -> None:
        # Testing cell creation
        self.assertEqual(len(self.maze._cells), NUM_COLS)
        self.assertEqual(len(self.maze._cells[0]), NUM_ROWS)

    # Testing entrance and exit creation
    def test_entrance_and_exit(self) -> None:
        self.assertEqual(self.maze._cells[0][0].has_top_wall, False)
        self.assertEqual(self.maze._cells[-1][-1].has_bottom_wall, False)

    # Testing visited reset
    def test_reset_visited(self) -> None:
        for col in self.maze._cells:
            for cell in col:
                self.assertEqual(cell._visited, False)


if __name__ == "__main__":
    unittest.main()
