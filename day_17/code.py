from heapq import heappush, heappop


MATRIX = list[list[int]]
NODE = tuple[int, int, int, int, int]


def a_star_with_3_move_constraint(grid):
    def heuristic(row: int, column: int) -> int:
        return abs(row - (len(grid) - 1)) + abs(column - (len(grid[0]) - 1))

    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    seen: set[NODE] = set()
    priority_queue: list[NODE] = [(0 + heuristic(0, 0), 0, 0, 0, 0, 0)]

    while priority_queue:
        (
            estimated_total_cost,
            row,
            column,
            delta_row,
            delta_column,
            steps_in_direction,
        ) = heappop(priority_queue)

        if row == len(grid) - 1 and column == len(grid[0]) - 1:
            return estimated_total_cost - heuristic(row, column)

        if (row, column, delta_row, delta_column, steps_in_direction) in seen:
            continue

        seen.add((row, column, delta_row, delta_column, steps_in_direction))

        if steps_in_direction < 3 and (delta_row, delta_column) != (0, 0):
            next_row, next_column = row + delta_row, column + delta_column
            if 0 <= next_row < len(grid) and 0 <= next_column < len(grid[0]):
                new_cost = (
                    estimated_total_cost
                    - heuristic(row, column)
                    + grid[next_row][next_column]
                )

                heappush(
                    priority_queue,
                    (
                        new_cost + heuristic(next_row, next_column),
                        next_row,
                        next_column,
                        delta_row,
                        delta_column,
                        steps_in_direction + 1,
                    ),
                )

        for next_direction_row, next_direction_column in DIRECTIONS:
            if (next_direction_row, next_direction_column) != (
                delta_row,
                delta_column,
            ) and (next_direction_row, next_direction_column) != (
                -delta_row,
                -delta_column,
            ):
                next_row, next_column = (
                    row + next_direction_row,
                    column + next_direction_column,
                )

                if 0 <= next_row < len(grid) and 0 <= next_column < len(grid[0]):
                    new_cost = (
                        estimated_total_cost
                        - heuristic(row, column)
                        + grid[next_row][next_column]
                    )

                    heappush(
                        priority_queue,
                        (
                            new_cost + heuristic(next_row, next_column),
                            next_row,
                            next_column,
                            next_direction_row,
                            next_direction_column,
                            1,
                        ),
                    )

    return float("inf")


def a_star_with_4_and_10_move_constraint(grid):
    def heuristic(row: int, column: int) -> int:
        return abs(row - (len(grid) - 1)) + abs(column - (len(grid[0]) - 1))

    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    seen: set[NODE] = set()
    priority_queue: list[NODE] = [(0 + heuristic(0, 0), 0, 0, 0, 0, 0)]

    while priority_queue:
        (
            estimated_total_cost,
            row,
            column,
            delta_row,
            delta_column,
            steps_in_direction,
        ) = heappop(priority_queue)

        if (
            row == len(grid) - 1
            and column == len(grid[0]) - 1
            and steps_in_direction >= 4
        ):
            return estimated_total_cost - heuristic(row, column)

        if (row, column, delta_row, delta_column, steps_in_direction) in seen:
            continue

        seen.add((row, column, delta_row, delta_column, steps_in_direction))

        if steps_in_direction < 10 and (delta_row, delta_column) != (0, 0):
            next_row, next_column = row + delta_row, column + delta_column
            if 0 <= next_row < len(grid) and 0 <= next_column < len(grid[0]):
                new_cost = (
                    estimated_total_cost
                    - heuristic(row, column)
                    + grid[next_row][next_column]
                )

                heappush(
                    priority_queue,
                    (
                        new_cost + heuristic(next_row, next_column),
                        next_row,
                        next_column,
                        delta_row,
                        delta_column,
                        steps_in_direction + 1,
                    ),
                )

        if steps_in_direction >= 4 or (delta_row, delta_column) == (0, 0):
            for next_direction_row, next_direction_column in DIRECTIONS:
                if (next_direction_row, next_direction_column) != (
                    delta_row,
                    delta_column,
                ) and (next_direction_row, next_direction_column) != (
                    -delta_row,
                    -delta_column,
                ):
                    next_row, next_column = (
                        row + next_direction_row,
                        column + next_direction_column,
                    )

                    if 0 <= next_row < len(grid) and 0 <= next_column < len(grid[0]):
                        new_cost = (
                            estimated_total_cost
                            - heuristic(row, column)
                            + grid[next_row][next_column]
                        )

                        heappush(
                            priority_queue,
                            (
                                new_cost + heuristic(next_row, next_column),
                                next_row,
                                next_column,
                                next_direction_row,
                                next_direction_column,
                                1,
                            ),
                        )

    return float("inf")


city_block_map: MATRIX = [
    list(map(int, line)) for line in open("input.txt").read().splitlines()
]

print(
    f"Part 1: {a_star_with_3_move_constraint(city_block_map)} | Part 2: {a_star_with_4_and_10_move_constraint(city_block_map)}"
)
