from itertools import combinations

MATRIX = list[list[str]]
COORDS = tuple[int, int]
EMPTY = tuple[list[int], list[int]]

lines: list[str] = open("input.txt").read().splitlines()

galaxies: MATRIX = [list(line) for line in lines]


def get_indexes_of_empty_rows_and_cols(matrix: MATRIX) -> EMPTY:
    indexes_of_empty_rows: list[int] = []
    indexes_of_empty_cols: list[int] = []

    for row in range(len(matrix)):
        if matrix[row].count("#") == 0:
            indexes_of_empty_rows.append(row)

    for col in range(len(matrix[0])):
        if [matrix[row][col] for row in range(len(matrix))].count("#") == 0:
            indexes_of_empty_cols.append(col)

    return indexes_of_empty_rows, indexes_of_empty_cols


def get_all_galaxies_coords(matrix: MATRIX) -> list[COORDS]:
    coordinates_of_galaxies: list[COORDS] = []

    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == "#":
                coordinates_of_galaxies.append((row, col))

    return coordinates_of_galaxies


def get_shortest_path_sum(
    coords: list[COORDS], empty_rows_and_cols: EMPTY, expanded=False
) -> int:
    shortest_path_sum: int = 0

    empty_rows, empty_cols = empty_rows_and_cols

    distance_adder = 1 if not expanded else 999999

    for row_index, row in enumerate(coords):
        for col_index, col in enumerate(coords[:row_index]):
            x_max, x_min = max(row[0], col[0]), min(row[0], col[0])
            y_max, y_min = max(row[1], col[1]), min(row[1], col[1])

            distance = (x_max - x_min) + (y_max - y_min)

            for empty_row in empty_rows:
                if x_min < empty_row < x_max:
                    distance += distance_adder

            for empty_col in empty_cols:
                if y_min < empty_col < y_max:
                    distance += distance_adder

            shortest_path_sum += distance

    return shortest_path_sum


galaxies_coords = get_all_galaxies_coords(galaxies)

shortest_path_sum = get_shortest_path_sum(
    galaxies_coords, get_indexes_of_empty_rows_and_cols(galaxies)
)

shortest_path_expanded_sum = get_shortest_path_sum(
    galaxies_coords, get_indexes_of_empty_rows_and_cols(galaxies), expanded=True
)

print(f"Part 1: {shortest_path_sum} | Part 2: {shortest_path_expanded_sum}")
