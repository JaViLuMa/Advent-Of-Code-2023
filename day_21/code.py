import numpy as np
from math import ceil
from collections import deque


STEPS = 64
NUMERATOR = 26501365


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


def get_number_of_reached_graden_plots_in_64_steps(garden, S_coords):
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


def get_number_of_reached_garden_plots_in_a_lot_of_steps(garden):
    rows, columns_as_denominator = len(garden), len(garden[0])

    quotient, remainder = divmod(NUMERATOR, columns_as_denominator)

    borders = [
        remainder,
        remainder + columns_as_denominator,
        remainder + (columns_as_denominator * 2),
    ]

    reached_garden_plots = set()

    garden_plots_queue = deque(
        [(columns_as_denominator // 2, columns_as_denominator // 2)]
    )

    evens_and_odds = [0, 0]

    Y = []

    for step in range(1, borders[-1] + 1):
        for _ in range(len(garden_plots_queue)):
            garden_row, garden_column = garden_plots_queue.popleft()

            for next_garden_row, next_garden_column in directions(
                garden_row, garden_column
            ):
                if (
                    next_garden_row,
                    next_garden_column,
                ) in reached_garden_plots or garden[next_garden_row % rows][
                    next_garden_column % columns_as_denominator
                ] == "#":
                    continue

                reached_garden_plots.add((next_garden_row, next_garden_column))
                garden_plots_queue.append((next_garden_row, next_garden_column))

                evens_and_odds[step % 2] += 1

        if step in borders:
            Y.append(evens_and_odds[step % 2])

    X = [0, 1, 2]

    coefficients = np.polyfit(X, Y, deg=2)

    Y_final = np.polyval(coefficients, quotient)

    return ceil(Y_final)


garden = open("input.txt").read().splitlines()

S_coords = get_S_position(garden)

number_of_reached_garden_plots_in_64_steps = (
    get_number_of_reached_graden_plots_in_64_steps(garden, S_coords)
)

number_of_reached_garden_plots_in_a_lot_of_steps = (
    get_number_of_reached_garden_plots_in_a_lot_of_steps(garden)
)

print(
    f"Part 1: {number_of_reached_garden_plots_in_64_steps} | Part 2: {number_of_reached_garden_plots_in_a_lot_of_steps}"
)
