from matplotlib.path import Path


ADJACENCY_OBJECT = {
    "up": ["F", "|", "7"],
    "down": ["L", "|", "J"],
    "left": ["L", "-", "F"],
    "right": ["7", "-", "J"],
}
ADJACENCY_OBJECT_S = {key: [*ADJACENCY_OBJECT[key], "S"] for key in ADJACENCY_OBJECT}


COORDS_TYPE = tuple[int, int]
COORDS_AND_PIPE = tuple[COORDS_TYPE, str]


lines = open("input.txt").read().splitlines()

pipes: list[list[str]] = [list(line) for line in lines]


def add_border_to_all_matrix_sides(matrix: list[list[str]]) -> None:
    for row in range(len(matrix)):
        matrix[row].insert(0, ".")
        matrix[row].append(".")

    matrix.insert(0, ["."] * len(matrix[0]))
    matrix.append(["."] * len(matrix[0]))


def adjacency_checker(
    row: int, col: int, side: str, visited: list[COORDS_TYPE], is_S: bool
) -> bool:
    adjacency_object = ADJACENCY_OBJECT_S if not is_S else ADJACENCY_OBJECT

    return pipes[row][col] in adjacency_object[side] and not (row, col) in visited


def adjacent_path(
    coordinates: COORDS_TYPE, pipe: str, visited: list[COORDS_TYPE], is_S: bool = True
) -> COORDS_AND_PIPE:
    row, col = coordinates

    if pipe == "|":
        if adjacency_checker(row - 1, col, "up", visited, is_S):
            return ((row - 1, col), pipes[row - 1][col])

        if adjacency_checker(row + 1, col, "down", visited, is_S):
            return ((row + 1, col), pipes[row + 1][col])

    if pipe == "-":
        if adjacency_checker(row, col - 1, "left", visited, is_S):
            return ((row, col - 1), pipes[row][col - 1])

        if adjacency_checker(row, col + 1, "right", visited, is_S):
            return ((row, col + 1), pipes[row][col + 1])

    if pipe == "F":
        if adjacency_checker(row + 1, col, "down", visited, is_S):
            return ((row + 1, col), pipes[row + 1][col])

        if adjacency_checker(row, col + 1, "right", visited, is_S):
            return ((row, col + 1), pipes[row][col + 1])

    if pipe == "7":
        if adjacency_checker(row + 1, col, "down", visited, is_S):
            return ((row + 1, col), pipes[row + 1][col])

        if adjacency_checker(row, col - 1, "left", visited, is_S):
            return ((row, col - 1), pipes[row][col - 1])

    if pipe == "J":
        if adjacency_checker(row - 1, col, "up", visited, is_S):
            return ((row - 1, col), pipes[row - 1][col])

        if adjacency_checker(row, col - 1, "left", visited, is_S):
            return ((row, col - 1), pipes[row][col - 1])

    if pipe == "L":
        if adjacency_checker(row - 1, col, "up", visited, is_S):
            return ((row - 1, col), pipes[row - 1][col])

        if adjacency_checker(row, col + 1, "right", visited, is_S):
            return ((row, col + 1), pipes[row][col + 1])


def get_S_coordinates() -> COORDS_TYPE:
    for row in range(len(pipes)):
        for col in range(len(pipes[row])):
            if pipes[row][col] == "S":
                return (row, col)

    return (0, 0)


def get_valid_adjacent_paths_from_S(
    S_coordinates: COORDS_TYPE,
) -> list[COORDS_AND_PIPE]:
    valid_paths: list[COORDS_AND_PIPE] = []

    S_row, S_col = S_coordinates

    if pipes[S_row][S_col - 1] in ADJACENCY_OBJECT["left"]:
        valid_paths.append(((S_row, S_col - 1), pipes[S_row][S_col - 1]))

    if pipes[S_row][S_col + 1] in ADJACENCY_OBJECT["right"]:
        valid_paths.append(((S_row, S_col + 1), pipes[S_row][S_col + 1]))

    if pipes[S_row - 1][S_col] in ADJACENCY_OBJECT["up"]:
        valid_paths.append(((S_row - 1, S_col), pipes[S_row - 1][S_col]))

    if pipes[S_row + 1][S_col] in ADJACENCY_OBJECT["down"]:
        valid_paths.append(((S_row + 1, S_col), pipes[S_row + 1][S_col]))

    return valid_paths


is_S = True


def create_full_cycle_in_one_direction(
    coordinates: COORDS_AND_PIPE, S_coordinates: COORDS_TYPE
) -> list[COORDS_TYPE]:
    global is_S

    full_cycle_coords: list[COORDS_TYPE] = []

    full_cycle_coords.append(coordinates[0])

    current_full_cycle_coords: COORDS_TYPE = coordinates[0]
    current_full_cycle_type: str = coordinates[1]

    while current_full_cycle_coords != S_coordinates:
        adjacent_path_coords = adjacent_path(
            current_full_cycle_coords, current_full_cycle_type, full_cycle_coords, is_S
        )

        current_full_cycle_coords = adjacent_path_coords[0]
        current_full_cycle_type = adjacent_path_coords[1]

        full_cycle_coords.append(current_full_cycle_coords)

        is_S = False

    return full_cycle_coords


def count_steps_for_first_and_second_path_to_meet(paths: list[COORDS_AND_PIPE]) -> int:
    steps: int = 1

    visited: list[COORDS_TYPE] = []

    first_path_coords = paths[0][0]
    first_path_type = paths[0][1]

    second_path_coords = paths[1][0]
    second_path_type = paths[1][1]

    visited.append(first_path_coords)
    visited.append(second_path_coords)

    while first_path_coords != second_path_coords:
        first_path = adjacent_path(first_path_coords, first_path_type, visited)
        second_path = adjacent_path(second_path_coords, second_path_type, visited)

        first_path_coords = first_path[0]
        first_path_type = first_path[1]

        second_path_coords = second_path[0]
        second_path_type = second_path[1]

        visited.append(first_path_coords)
        visited.append(second_path_coords)

        steps += 1

    return steps


def get_number_of_enclosed_tiles(full_cycle_coords: list[COORDS_TYPE]) -> int:
    number_of_enclosed_tiles: int = 0

    path_polygon = Path(full_cycle_coords)

    for row in range(len(pipes)):
        for col in range(len(pipes[row])):
            if (
                path_polygon.contains_point((row, col))
                and not (row, col) in full_cycle_coords
            ):
                number_of_enclosed_tiles += 1

    return number_of_enclosed_tiles


add_border_to_all_matrix_sides(pipes)

S_coordinates = get_S_coordinates()

coords_of_valid_paths_from_S: list[COORDS_AND_PIPE] = get_valid_adjacent_paths_from_S(
    S_coordinates
)

first_valid_path_coords = coords_of_valid_paths_from_S[0][0]
second_valid_path_coords = coords_of_valid_paths_from_S[1][0]

full_cycle_coords = create_full_cycle_in_one_direction(
    coords_of_valid_paths_from_S[0], S_coordinates
)

steps = count_steps_for_first_and_second_path_to_meet(coords_of_valid_paths_from_S)

number_of_enclosed_tiles = get_number_of_enclosed_tiles(full_cycle_coords)

print(f"Part 1: {steps} | Part 2: {number_of_enclosed_tiles}")
