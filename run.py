# in a terminal, prompt a user to provide the height, width, and rows and columns of a triangle grid,
# create the triangle grid object, then prompt the user to either provide a triangle label to get its vertices
# or provide coordinates to get the triangle label.
# I'll keep things simple can prompt inputs one by one.

from triangles import TriangleGrid


def main():
    height = float(input("Enter the height of the grid (in pixels): "))
    width = float(input("Enter the width of the grid (in pixels): "))
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))

    try:
        grid = TriangleGrid(height, width, rows, cols)
    except ValueError as e:
        print(e)
        return

    while True:
        choice = input(
            "Enter '1' to get triangle vertices by label, '2' to get triangle label by coordinates, or 'q' to quit: "
        )
        if choice == "1":
            label = input("Enter the triangle label (e.g., A1, B2): ")
            try:
                vertices = grid.get_triangle_vertices(label)
                print(f"Vertices of triangle {label}: {vertices}")
            except ValueError as e:
                print(e)
        elif choice == "2":
            x = int(input("Enter the x coordinate: "))
            y = int(input("Enter the y coordinate: "))
            try:
                label = grid.get_triangle_label(x, y)
                print(f"The triangle containing point ({x}, {y}) is: {label}")
            except ValueError as e:
                print(e)
        elif choice.lower() == "q":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
