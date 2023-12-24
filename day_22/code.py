from copy import deepcopy
from collections import deque


def get_bricks(lines):
    bricks = []

    for line in lines:
        first_perspective, second_perspective = line.split("~")

        brick = [
            *list(map(int, first_perspective.split(","))),
            *list(map(int, second_perspective.split(","))),
        ]

        bricks.append(brick)

    return sorted(bricks, key=lambda brick: brick[2])


def check_if_overlap(brick_a, brick_b):
    def overlap_X(a, b):
        return max(a[0], b[0]) <= min(a[3], b[3])

    def overlap_Y(a, b):
        return max(a[1], b[1]) <= min(a[4], b[4])

    return overlap_X(brick_a, brick_b) and overlap_Y(brick_a, brick_b)


def drop_down_bricks(bricks):
    for index, brick in enumerate(bricks):
        max_Z = 1

        for new_brick in bricks[:index]:
            if check_if_overlap(brick, new_brick):
                max_Z = max(max_Z, new_brick[5] + 1)

        brick[5] -= brick[2] - max_Z
        brick[2] = max_Z

    return sorted(bricks, key=lambda brick: brick[2])


def supporting_bricks(bricks):
    upper_supports = {index: set() for index in range(len(bricks))}
    lower_supports = deepcopy(upper_supports)

    for upper_index, upper_brick in enumerate(bricks):
        for lower_index, lower_brick in enumerate(bricks[:upper_index]):
            if (
                check_if_overlap(lower_brick, upper_brick)
                and upper_brick[2] == lower_brick[5] + 1
            ):
                upper_supports[lower_index].add(upper_index)
                lower_supports[upper_index].add(lower_index)

    return upper_supports, lower_supports


def get_total_disintegrate_blocks(bricks, upper_supports, lower_supports):
    total_disintegrate_blocks = 0

    for i in range(len(bricks)):
        if all(len(lower_supports[j]) >= 2 for j in upper_supports[i]):
            total_disintegrate_blocks += 1

    return total_disintegrate_blocks


def get_total_of_each_disinegrated_block(bricks, upper_supports, lower_supports):
    total_of_each_disinegrated_block = 0

    for i in range(len(bricks)):
        bricks_deque = deque(
            j for j in upper_supports[i] if len(lower_supports[j]) == 1
        )

        falling_bricks = set(bricks_deque)

        falling_bricks.add(i)

        while bricks_deque:
            brick = bricks_deque.popleft()

            for k in upper_supports[brick] - falling_bricks:
                if lower_supports[k] <= falling_bricks:
                    bricks_deque.append(k)
                    falling_bricks.add(k)

        total_of_each_disinegrated_block += len(falling_bricks) - 1

    return total_of_each_disinegrated_block


lines = open("input.txt").read().splitlines()

bricks = get_bricks(lines)

bricks = drop_down_bricks(bricks)

upper_supports, lower_supports = supporting_bricks(bricks)

total_disintegrate_blocks = get_total_disintegrate_blocks(
    bricks, upper_supports, lower_supports
)

total_of_each_disinegrated_block = get_total_of_each_disinegrated_block(
    bricks, upper_supports, lower_supports
)

print(
    f"Part 1: {total_disintegrate_blocks} | Part 2: {total_of_each_disinegrated_block}"
)
