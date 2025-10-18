import unittest
from math import floor

from triangles import TriangleGrid


class TestTriangleGrid(unittest.TestCase):
    x = y = rows = cols = 0

    def setUp(self):
        c = type(self)
        self.grid = TriangleGrid(c.y, c.x, c.rows, c.cols)
        self.x = c.x
        self.y = c.y
        self.rows = c.rows
        self.cols = c.cols

    def test_letters_to_index(self):
        self.assertEqual(self.grid.letters_to_index(["A"]), 0)
        self.assertEqual(self.grid.letters_to_index(["B"]), 1)
        self.assertEqual(self.grid.letters_to_index(["Z"]), 25)
        self.assertEqual(self.grid.letters_to_index(["A", "A"]), 26)
        self.assertEqual(self.grid.letters_to_index(["A", "B"]), 27)

    def test_index_to_letters(self):
        self.assertEqual(self.grid.index_to_letters(0), "A")
        self.assertEqual(self.grid.index_to_letters(1), "B")
        self.assertEqual(self.grid.index_to_letters(25), "Z")
        self.assertEqual(self.grid.index_to_letters(26), "AA")
        self.assertEqual(self.grid.index_to_letters(27), "AB")

    def test_input_validation_valid(self):
        try:
            self.grid.grid_validation(self.cols // 2, self.rows // 2)
        except ValueError:
            self.fail("input_validation raised ValueError unexpectedly!")

    def test_input_validation_invalid(self):
        with self.assertRaises(ValueError):
            self.grid.grid_validation(self.cols * 2, self.rows // 2)
        with self.assertRaises(ValueError):
            self.grid.grid_validation(self.cols // 2, self.rows + 5)
        with self.assertRaises(ValueError):
            self.grid.grid_validation(-self.cols, self.rows // 2)
        with self.assertRaises(ValueError):
            self.grid.grid_validation(self.cols // 2, -self.rows)

    def test_get_triangle_labels(self):
        # on one hand, we could be very confident if we had a pre-computed set of expected values
        # but also I feel like this is a mathematical problem that can be validated by deriving the expected values

        for pixel_x in range(0, self.x):
            for pixel_y in range(0, self.y):
                col_index = floor(pixel_x / self.grid.cell_width)
                row_index = floor(pixel_y / self.grid.cell_height)

                row_label = self.grid.index_to_letters(row_index)

                y_offset = pixel_y - (row_index * self.grid.cell_height)
                x_offset = pixel_x - (col_index * self.grid.cell_width)

                even = x_offset >= y_offset

                col_label = str((col_index * 2) + (2 if even else 1))
                expected_label = f"{row_label}{col_label}"

                label = self.grid.get_triangle_label(pixel_x, pixel_y)
                self.assertEqual(
                    label,
                    expected_label,
                    f"Failed at pixel ({pixel_x}, {pixel_y}) -> {label}, expected {expected_label}",
                )

    def test_get_triangle_vertices(self):
        # same with this one

        for row in range(self.rows):
            for col in range(self.cols * 2):
                row_label = self.grid.index_to_letters(row)
                label = f"{row_label}{col + 1}"

                vertices = self.grid.get_triangle_vertices(label)

                col_index = col // 2
                even = (col % 2) == 0
                expected_vertices = self.grid.grid_to_vertices(row, col_index, even)

                self.assertEqual(
                    vertices,
                    expected_vertices,
                    f"Failed at label {label} -> {vertices}, expected {expected_vertices}",
                )


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for x in range(10, 200, 10):
        for y in range(10, 200, 10):
            for rows in range(1, 51, 5):
                for cols in range(1, 51, 5):
                    if (x % cols) or (y % rows):
                        # skip non-integer cell sizes,
                        # I'm assuming that triangles with fractional pixel vertices
                        # are not expected to be handled
                        continue
                    name = f"TestTriangleGrid_height:{y}_width:{x}__rows:{rows}_columns:{cols}"
                    cls = type(
                        name,
                        (TestTriangleGrid,),
                        {"x": x, "y": y, "rows": rows, "cols": cols},
                    )
                    suite.addTests(loader.loadTestsFromTestCase(cls))
    return suite


if __name__ == "__main__":
    unittest.main(verbosity=1)
