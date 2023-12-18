MATRIX = list[list[str]]
POINT = tuple[int, int]


DIRECTIONS: dict[str, POINT] = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}
DIRECTIONS_NUMBER = {
    "0": DIRECTIONS["R"],
    "1": DIRECTIONS["D"],
    "2": DIRECTIONS["L"],
    "3": DIRECTIONS["U"],
}


def get_corner_and_boundary_points(
    grid: MATRIX,
) -> tuple[list[POINT], int, list[POINT], int]:
    corners = [(0, 0)]
    color_corners = [(0, 0)]

    boundary_points = 0
    color_boundary_points = 0

    for row in grid:
        direction, steps, color = row

        cleaned_color = color[2:-1]

        direction_row, direction_column = DIRECTIONS[direction]
        color_direction_row, color_direction_column = DIRECTIONS_NUMBER[
            cleaned_color[-1]
        ]

        steps_as_int = int(steps)
        color_steps_as_int = int(cleaned_color[:-1], 16)

        boundary_points += steps_as_int
        color_boundary_points += color_steps_as_int

        row_of_last_corner, column_of_last_corner = corners[-1]
        color_row_of_last_corner, color_column_of_last_corner = color_corners[-1]

        corners.append(
            (
                row_of_last_corner + direction_row * steps_as_int,
                column_of_last_corner + direction_column * steps_as_int,
            )
        )

        color_corners.append(
            (
                color_row_of_last_corner + color_direction_row * color_steps_as_int,
                color_column_of_last_corner
                + color_direction_column * color_steps_as_int,
            )
        )

    return corners, boundary_points, color_corners, color_boundary_points


def get_total_lava_tiles(corners: list[POINT], boundary_points: int) -> int:
    amount_of_corners = len(corners)

    area = 0.0

    for i in range(amount_of_corners):
        j = (i + 1) % amount_of_corners

        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]

    area = abs(area) / 2.0

    i = area - boundary_points // 2 + 1

    return int(i + boundary_points)


grid_plan = [line.split() for line in open("input.txt").read().splitlines()]

(
    corners,
    boundary_points,
    color_corners,
    color_boundary_points,
) = get_corner_and_boundary_points(grid_plan)

total_lava_tiles = get_total_lava_tiles(corners, boundary_points)
total_lava_tiles_with_color = get_total_lava_tiles(color_corners, color_boundary_points)

print(f"Part 1: {total_lava_tiles} | Part 2: {total_lava_tiles_with_color}")
