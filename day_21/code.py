from collections import deque


STEPS = 64


def get_S_position(matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == "S":
                return (row, col)


def directions(row, col):
    return [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]


def check_if_border_or_hash_or_seen(matrix, row, col, seen):
    return (
        row < 0
        or row >= len(matrix)
        or col < 0
        or col >= len(matrix[row])
        or matrix[row][col] == "#"
        or (row, col) in seen
    )


def get_number_of_reached_graden_plots(garden, S_coords):
    reached_garden_plots = set()

    seen_garden_plots = {S_coords}

    garden_plots_queue = deque([(*S_coords, STEPS)])

    while garden_plots_queue:
        garden_row, garden_column, steps = garden_plots_queue.popleft()

        if steps % 2 == 0:
            reached_garden_plots.add((garden_row, garden_column))

        if steps == 0:
            continue

        for next_garden_row, next_garden_column in directions(
            garden_row, garden_column
        ):
            if check_if_border_or_hash_or_seen(
                garden, next_garden_row, next_garden_column, seen_garden_plots
            ):
                continue

            seen_garden_plots.add((next_garden_row, next_garden_column))

            garden_plots_queue.append((next_garden_row, next_garden_column, steps - 1))

    return len(reached_garden_plots)


garden = open("input.txt").read().splitlines()

S_coords = get_S_position(garden)

number_of_reached_graden_plots = get_number_of_reached_graden_plots(garden, S_coords)

print(number_of_reached_graden_plots)
