ADJACENCY_LIST: list[tuple[int, int]] = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]

lines = open("input.txt").read().splitlines()

schematic_engine: list[list[str]] = [[*line] for line in lines]


def add_border_to_all_matrix_sides(matrix: list[list[str]]) -> None:
    for row in range(len(matrix)):
        matrix[row].insert(0, ".")
        matrix[row].append(".")

    matrix.insert(0, ["."] * len(matrix[0]))
    matrix.append(["."] * len(matrix[0]))


def has_part_as_adjacent_element(row: int, col: int) -> bool:
    for direction in ADJACENCY_LIST:
        row_direction: int = row + direction[0]
        col_direction: int = col + direction[1]

        row_and_col_value: str = schematic_engine[row_direction][col_direction]

        if not row_and_col_value.isdigit() and row_and_col_value != ".":
            return True

    return False


def join_constructed_number(
    constructed_number: list[str], type_of_part: str | None
) -> int | None:
    number: int = int("".join(constructed_number))

    if type_of_part:
        return number

    return 0


def search_for_parts_as_adjacent_element(row: int, col: int) -> tuple[str, str] | None:
    parts = []

    for direction in ADJACENCY_LIST:
        row_direction: int = row + direction[0]
        col_direction: int = col + direction[1]

        row_and_col_value: str = schematic_engine[row_direction][col_direction]

        if not row_and_col_value.isdigit() and row_and_col_value != ".":
            parts.append(f"{row_direction}-{col_direction}")

    return parts


def populate_gears_dict(gears: dict[str, dict[str, str | list[int]]]) -> None:
    for row in range(1, len(schematic_engine) - 1):
        for col in range(1, len(schematic_engine[row]) - 1):
            row_col_value = schematic_engine[row][col]

            if not row_col_value.isdigit() and row_col_value != ".":
                row_col_as_key = f"{row}-{col}"

                gears[row_col_as_key] = {}

                gears[row_col_as_key]["type"] = row_col_value
                gears[row_col_as_key]["values"] = []


add_border_to_all_matrix_sides(schematic_engine)

valid_parts_sum: int = 0
gear_ratios_sum: int = 0
gears: dict[str, dict[str, str | list[int]]] = {}

populate_gears_dict(gears)

for row in range(1, len(schematic_engine) - 1):
    constructed_number: list[str] = []
    parts_coords = []
    type_of_part: str | None = None

    for col in range(1, len(schematic_engine[row]) - 1):
        if schematic_engine[row][col] != ".":
            coords = search_for_parts_as_adjacent_element(row, col)

            if len(coords):
                parts_coords = coords

        if len(constructed_number) == 0:
            type_of_part = None

        if len(constructed_number) and not schematic_engine[row][col].isdigit():
            number = int("".join(constructed_number))

            if type_of_part:
                valid_parts_sum += number

                for part_coord in parts_coords:
                    gears[part_coord]["values"].append(number)

            constructed_number = []

        if schematic_engine[row][col].isdigit():
            constructed_number.append(schematic_engine[row][col])

        if has_part_as_adjacent_element(row, col):
            type_of_part = True

    if constructed_number:
        number = int("".join(constructed_number))

        if type_of_part:
            valid_parts_sum += number

            for part_coord in parts_coords:
                gears[part_coord]["values"].append(number)


for gear_key in gears:
    gear = gears[gear_key]

    gear_type = gear["type"]

    if gear_type == "*":
        if len(gear["values"]) == 2:
            if gear["type"] == "*":
                gear_ratios_sum += int(gear["values"][0]) * int(gear["values"][1])

print(f"Part 1: {valid_parts_sum} | Part 2: {gear_ratios_sum}")
