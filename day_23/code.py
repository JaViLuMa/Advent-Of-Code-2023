from copy import deepcopy
from collections import deque


ADJACENT_DIRECTIONS = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
]
POSSIBLE_DIRECTIONS_BASED_ON_TYPE = {
    "^": [(-1, 0)],
    "v": [(1, 0)],
    ">": [(0, 1)],
    "<": [(0, -1)],
    ".": [direction for direction in ADJACENT_DIRECTIONS],
}


def get_start_and_end_position(maze):
    start_node = (0, None)
    end_node = (len(maze) - 1, None)

    for index, column in enumerate(maze[0]):
        if column == ".":
            start_node = (0, index)

    for index, column in enumerate(maze[-1]):
        if column == ".":
            end_node = (len(maze) - 1, index)

    return start_node, end_node


def check_if_matrix_border_and_hash(maze, row, column):
    return (
        0 <= row < len(maze) and 0 <= column < len(maze[0]) and maze[row][column] != "#"
    )


def get_adjacent_coords(row, column):
    return [
        (row + next_row, column + next_column)
        for next_row, next_column in ADJACENT_DIRECTIONS
    ]


def get_points_with_more_than_3_neighbors(maze, start, end):
    points = [start, end]

    for row in range(len(maze)):
        for column in range(len(maze[0])):
            if maze[row][column] == "#":
                continue

            neighbors = 0

            for next_row, next_column in get_adjacent_coords(row, column):
                if check_if_matrix_border_and_hash(maze, next_row, next_column):
                    neighbors += 1

            if neighbors >= 3:
                points.append((row, column))

    return points


def check_if_matrix_border_and_hash_and_not_seen(maze, row, column, seen):
    return (
        check_if_matrix_border_and_hash(maze, row, column) and (row, column) not in seen
    )


def get_populated_adjacency_graph(maze, adjacency_graph, points, longest=False):
    populated_adjacency_graph = deepcopy(adjacency_graph)

    for start_row, start_column in points:
        stack_of_points = [(0, start_row, start_column)]

        seen = {(start_row, start_column)}

        while stack_of_points:
            distance, row, column = stack_of_points.pop()

            if distance != 0 and (row, column) in points:
                populated_adjacency_graph[(start_row, start_column)][
                    (row, column)
                ] = distance
                continue

            directions = (
                ADJACENT_DIRECTIONS
                if longest
                else POSSIBLE_DIRECTIONS_BASED_ON_TYPE[maze[row][column]]
            )

            for delta_row, delta_column in directions:
                new_row = row + delta_row
                new_column = column + delta_column

                if check_if_matrix_border_and_hash_and_not_seen(
                    maze, new_row, new_column, seen
                ):
                    stack_of_points.append((distance + 1, new_row, new_column))
                    seen.add((new_row, new_column))

    return populated_adjacency_graph


def dfs(adjacency_graph, point, end, seen=set()):
    if point == end:
        return 0

    minimal = -float("inf")

    seen.add(point)

    for new_point in adjacency_graph[point]:
        if new_point not in seen:
            minimal = max(
                minimal,
                dfs(adjacency_graph, new_point, end, seen)
                + adjacency_graph[point][new_point],
            )

    seen.remove(point)

    return minimal


maze = open("input.txt").read().splitlines()

start_node, end_node = get_start_and_end_position(maze)

points = get_points_with_more_than_3_neighbors(maze, start_node, end_node)

adjacency_graph = {point: {} for point in points}

populated_adjacency_graph_shortest = get_populated_adjacency_graph(
    maze, adjacency_graph, points
)
populated_adjacency_graph_longest = get_populated_adjacency_graph(
    maze, adjacency_graph, points, True
)

shortest_path = dfs(populated_adjacency_graph_shortest, start_node, end_node)

longest_path = dfs(populated_adjacency_graph_longest, start_node, end_node)

print(f"Part 1: {shortest_path} | Part 2: {longest_path}")
