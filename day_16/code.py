from collections import deque


UP_DOWN = [(1, 0), (-1, 0)]
LEFT_RIGHT = [(0, 1), (0, -1)]


MATRIX = list[list[str]]
COORD_KEY = tuple[int, int]
COORD_VALUE = dict[str, int | str]
COORDS_MAP = dict[COORD_KEY, COORD_VALUE]
TILE = tuple[int, int, int, int]
TILES = list[TILE]


def matrix_print(matrix: MATRIX) -> None:
    for row in matrix:
        print(*row)


def get_coords_map(matrix: MATRIX) -> COORDS_MAP:
    coords_map = {}

    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            coords_map[(row, col)] = {
                "type": matrix[row][col],
                "energy": 0,
            }

    return coords_map


def check_if_matrix_border(contraption: MATRIX, row: int, column: int) -> bool:
    return (
        row < 0
        or row >= len(contraption)
        or column < 0
        or column >= len(contraption[row])
    )


def check_if_should_pass(type: str | int, delta_row: int, delta_column: int) -> bool:
    return (
        type == "."
        or (type == "|" and delta_row != 0)
        or (type == "-" and delta_column != 0)
    )


def add_to_seen_and_deque(
    seen_coords: set[TILE],
    tiles_deque: deque[TILE],
    row: int,
    column: int,
    delta_row: int,
    delta_column: int,
) -> None:
    if (row, column, delta_row, delta_column) not in seen_coords:
        seen_coords.add((row, column, delta_row, delta_column))
        tiles_deque.append((row, column, delta_row, delta_column))


def get_total_tiles_energized_from_specific_start(
    contraption: MATRIX, r: int, c: int, d_row: int, d_column: int
) -> int:
    beginning_tile: TILES = [(r, c, d_row, d_column)]

    seen_coords = set()
    tiles_deque = deque(beginning_tile)

    while tiles_deque:
        row, column, delta_row, delta_column = tiles_deque.popleft()

        row += delta_row
        column += delta_column

        if check_if_matrix_border(contraption, row, column):
            continue

        current_type = contraption[row][column]

        if check_if_should_pass(current_type, delta_row, delta_column):
            add_to_seen_and_deque(
                seen_coords, tiles_deque, row, column, delta_row, delta_column
            )

        elif current_type == "/":
            delta_row, delta_column = -delta_column, -delta_row

            add_to_seen_and_deque(
                seen_coords, tiles_deque, row, column, delta_row, delta_column
            )

        elif current_type == "\\":
            delta_row, delta_column = delta_column, delta_row

            add_to_seen_and_deque(
                seen_coords, tiles_deque, row, column, delta_row, delta_column
            )

        else:
            if current_type == "|":
                for d_row, d_column in UP_DOWN:
                    add_to_seen_and_deque(
                        seen_coords, tiles_deque, row, column, d_row, d_column
                    )
            else:
                for d_row, d_column in LEFT_RIGHT:
                    add_to_seen_and_deque(
                        seen_coords, tiles_deque, row, column, d_row, d_column
                    )

    return len({(row, column) for (row, column, _, _) in seen_coords})


def get_total_tiles_energized(contraption: MATRIX) -> tuple[int, int]:
    tiles_energized_from_top_left = get_total_tiles_energized_from_specific_start(
        contraption, 0, -1, 0, 1
    )

    maximally_possible_energized_tiles: int = 0

    for row in range(len(contraption)):
        maximally_possible_energized_tiles = max(
            maximally_possible_energized_tiles,
            get_total_tiles_energized_from_specific_start(contraption, row, -1, 0, 1),
        )

        maximally_possible_energized_tiles = max(
            maximally_possible_energized_tiles,
            get_total_tiles_energized_from_specific_start(
                contraption, row, len(contraption[row]), 0, -1
            ),
        )

    for col in range(len(contraption)):
        maximally_possible_energized_tiles = max(
            maximally_possible_energized_tiles,
            get_total_tiles_energized_from_specific_start(contraption, -1, col, 1, 0),
        )

        maximally_possible_energized_tiles = max(
            maximally_possible_energized_tiles,
            get_total_tiles_energized_from_specific_start(
                contraption, len(contraption), col, -1, 0
            ),
        )

    return tiles_energized_from_top_left, maximally_possible_energized_tiles


contraption: MATRIX = [list(line) for line in open("input.txt").read().splitlines()]

(
    total_tiles_from_top_left,
    maximally_possible_energized_tiles,
) = get_total_tiles_energized(contraption)

print(
    f"Part 1: {total_tiles_from_top_left} | Part 2: {maximally_possible_energized_tiles}"
)
