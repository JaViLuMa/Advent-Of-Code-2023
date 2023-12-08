lines: list[str] = open("input.txt").read().splitlines()

filtered_lines: list[str] = [line.strip() for line in lines if line.strip()]

graph: dict[str, tuple[str, str]] = {}

directions: str = filtered_lines.pop(0)

for line in filtered_lines:
    node, vertices = line.split(" = ")

    graph[node] = tuple(vertices.strip("()").split(", "))


def reach_zzz() -> int:
    steps: int = 0
    end_reached: bool = False
    current_node: str = "AAA"

    while not end_reached:
        for direction in directions:
            current_node = graph[current_node][0 if direction == "L" else 1]

            steps += 1

            if current_node == "ZZZ":
                end_reached = True

                break

    return steps


def ghost_all_reach_z() -> int:
    start_nodes = [node for node in graph.keys() if node.endswith("A")]

    ghosts = {node: 0 for node in start_nodes}
    ghost_positions = {node: node for node in start_nodes}

    total_steps = 0
    while True:
        for ghost in list(ghosts):
            direction_index = ghosts[ghost]

            direction = directions[direction_index % len(directions)]

            next_node = graph[ghost_positions[ghost]][0 if direction == "L" else 1]

            ghost_positions[ghost] = next_node

            ghosts[ghost] = (direction_index + 1) % len(directions)

        total_steps += 1

        if all(node.endswith("Z") for node in ghost_positions.values()):
            break

    return total_steps


print(f"Part 1: {reach_zzz()} | Part 2: {ghost_all_reach_z()}")
