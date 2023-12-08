import math

lines: list[str] = open("input.txt").read().splitlines()

filtered_lines: list[str] = [line.strip() for line in lines if line.strip()]

graph: dict[str, tuple[str, str]] = {}

directions: str = filtered_lines.pop(0)

for line in filtered_lines:
    node, vertices = line.split(" = ")

    graph[node] = tuple(vertices.strip("()").split(", "))


def reach(curr_node: str, condition: bool) -> int:
    steps: int = 0
    end_reached: bool = False
    current_node: str = curr_node

    while not end_reached:
        for direction in directions:
            current_node = graph[current_node][0 if direction == "L" else 1]

            steps += 1

            if condition(current_node):
                end_reached = True

                break

    return steps


def ghost_all_reach_z() -> int:
    start_nodes = [node for node in graph.keys() if node.endswith("A")]

    steps_of_each_start_node: list[int] = []

    for start_node in start_nodes:
        steps_of_each_start_node.append(
            reach(start_node, lambda node: node.endswith("Z"))
        )

    return math.lcm(*steps_of_each_start_node)


print(
    f"Part 1: {reach('AAA', lambda node: node == 'ZZZ')} | Part 2: {ghost_all_reach_z()}"
)
