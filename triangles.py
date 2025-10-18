# in a screen-coordinate system, there is an 8x8 grid of triangles are drawn within the grid, -- should make it more generic than 8x8
# where each square cell of the grid is divided into two triangles along the diagonal from the top-left to the bottom-right corner.
# The labeling of the triangles follows a specific pattern:
# - Each row starts with a letter (A, B, C, ...) representing the row number. I'll assume that if there are more than 26 rows, it will continue with AA, AB, etc.
# - Each column is numbered (1, 2, 3, ...) representing the column number.
# - Odd numbered triangles (1, 3, 5, ...) in each cell are encompassed by top-left, bottom-left, bottom-right corners.
# - Even numbered triangles (2, 4, 6, ...) in each cell are encompassed by top-left, top-right, bottom-right corners.
# The height of the entire grid and the width of the entire grid are assumed to be provided as inputs, as coordinate values (pixel measurements).

# Parameters for the object: height, width, rows, cols
# need to be able to:
# given a label, return the coordinates of the triangle's vertices (as the representation of the triangle)
# given the coordinates of a point, return the label of the triangle that contains that point

# Boundary conditions to consider:
# if height and width are both 100px, is point (100, 100) valid? or is max (99, 99)?
#  -- I'll assume that 0,0 is the most top-left point, and 99,99 is the most bottom-right point, so (100,100) is invalid
# I'll bias towards even triangles when a point lies exactly on the diagonal line.
# I'm assuming that the ratio of height to rows and width to cols should yield integer cell dimensions,
#   otherwise, we'd have triangle vertices at fractional pixel coordinates, which sounds incorrect.

from math import floor


class TriangleGrid:
    def __init__(self, height, width, rows=8, cols=8):
        self.height = height
        self.width = width
        self.rows = rows
        self.cols = cols
        self.cell_height = height / rows
        self.cell_width = width / cols

        if self.cell_width % 1 != 0 or self.cell_height % 1 != 0:
            raise ValueError(
                f"Cell dimensions evaluate to integers. Given height: {height}, width: {width}, rows: {rows}, cols: {cols} -> cell size: ({self.cell_width}, {self.cell_height}) Ratio of height/rows and width/cols must yield integer values."
            )

    def coordinate_validation(self, x: int, y: int):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise ValueError(
                f"Coordinates out of bounds: ({x}, {y}) -> max: ({self.width - 1}, {self.height - 1})"
            )

    def grid_validation(self, col_index: int, row_index: int, extra_data={}):
        # things get confusing since each cell has 2 triangles, so the col_index is doubled
        # so even though there are say, 10 columns, there are actually 20 triangle columns
        if (
            col_index < 0
            or col_index >= (self.cols * 2)
            or row_index < 0
            or row_index > self.rows
        ):
            raise ValueError(
                f"Grid out of bounds: ({col_index}, {row_index}) -> max: ({(self.cols * 2 - 1)}, {self.rows}) | extra: {extra_data}"
            )

    def handle_label(self, label: str):
        letters = []
        for i in range(len(label)):
            if label[i].isalpha():
                letters.append(label[i])
            else:
                col_number = label[i:]
                break
        return letters, col_number

    def letters_to_index(self, letters: list) -> int:
        # A = 0, B = 1, ..., Z = 25, AA = 26, AB = 27, etc.
        index = 0
        for i, letter in enumerate(reversed(letters)):
            index += (ord(letter.upper()) - ord("A") + 1) * (26**i)
        return index - 1

    def index_to_letters(self, index: int) -> str:
        # 0 -> A, 1 -> B, ..., 25 -> Z, 26 -> AA, 27 -> AB, etc.
        letters = []
        index += 1  # Convert to 1-based index for easier calculation
        while index > 0:
            index -= 1
            remainder = index % 26
            letters.append(chr(remainder + ord("A")))
            index //= 26
        return "".join(reversed(letters))

    def grid_to_vertices(self, row_index: int, col_index: int, even: bool):
        x1 = col_index * self.cell_width
        y1 = row_index * self.cell_height
        x2 = (col_index + 1) * self.cell_width
        y2 = (row_index + 1) * self.cell_height

        if even:  # Even numbered triangle
            return [(x1, y1), (x1, y2), (x2, y2)]
        else:  # Odd numbered triangle
            return [(x1, y1), (x2, y1), (x2, y2)]

    def get_triangle_vertices(self, label):
        letters, col_number = self.handle_label(label)
        row_index = self.letters_to_index(letters)
        col_index = int(col_number) - 1
        self.grid_validation(col_index, row_index, {"label": label})

        return self.grid_to_vertices(row_index, col_index // 2, col_index % 2 == 0)

    def get_triangle_label(self, x: int, y: int) -> str:

        self.coordinate_validation(x, y)

        # x = column position, y = row position
        col_index = floor(x / self.cell_width)
        row_index = floor(y / self.cell_height)
        self.grid_validation(
            col_index,
            row_index,
            {
                "x": x,
                "y": y,
                "col_height": self.cell_height,
                "cell_width": self.cell_width,
            },
        )

        row_label = self.index_to_letters(row_index)

        # determine if the column is the odd or even triangle
        # calculate offsets within the cell
        y_offset = y - (row_index * self.cell_height)
        x_offset = x - (col_index * self.cell_width)

        # since the diagonal goes from top-left to bottom-right,
        # compare the offsets to determine which triangle the point is in

        if x_offset >= y_offset:
            triangle_number = (col_index * 2) + 2  # even triangle
        else:
            triangle_number = (col_index * 2) + 1  # odd triangle

        return f"{row_label}{triangle_number}"
