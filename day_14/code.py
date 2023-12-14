CYCLES = 1_000_000_000


MATRIX_L = list[str]
MATRIX_T = list[tuple[str]]


def transpose_matrix(matrix: MATRIX_L) -> MATRIX_T:
    return list(zip(*matrix))


def platform_tilt_north(platform: MATRIX_T) -> MATRIX_T:
    tilted_platform: MATRIX_T = []

    for row in platform:
        row_list = list(row)

        for i in range(len(row_list) - 1):
            if row_list[i] == ".":
                for j in range(i + 1, len(row_list)):
                    if row_list[j] == "O":
                        row_list[i], row_list[j] = row_list[j], row_list[i]
                        break
                    elif row_list[j] == "#":
                        break

        tilted_platform.append(tuple(row_list))

    return tilted_platform


def platform_tilt_west(platform: MATRIX_T) -> MATRIX_T:
    return platform_tilt_north(platform)


def platform_tilt_south(platform: MATRIX_T) -> MATRIX_T:
    reversed_platform: MATRIX_T = platform[::-1]

    transposed_platform = transpose_matrix(reversed_platform)

    return transpose_matrix(platform_tilt_north(transposed_platform))[::-1]


def platform_tilt_east(platform: MATRIX_T) -> MATRIX_T:
    reversed_platform_rows: MATRIX_T = [row[::-1] for row in platform]

    tilted_north = platform_tilt_north(reversed_platform_rows)

    return [row[::-1] for row in tilted_north]


def get_total_load(platform: MATRIX_T) -> int:
    total_load: int = 0

    for row in range(len(platform)):
        joined_platform_row = "".join(platform[row])

        number_of_Os = joined_platform_row.count("O")

        total_load += number_of_Os * (len(platform) - row)

    return total_load


def get_total_load_after_cycles(matrix: MATRIX_L, cycles: int) -> int:
    cached_platforms: dict[tuple[MATRIX_T], int] = {}

    current_platform: MATRIX_T = matrix

    for cycle in range(cycles):
        tupled_platform = tuple(current_platform)

        print(tupled_platform)

        if tupled_platform in cached_platforms:
            previous_cycle = cached_platforms[tupled_platform]

            length_of_the_loop = cycle - previous_cycle

            target_cycle = previous_cycle + (
                (cycles - previous_cycle) % length_of_the_loop
            )

            for key in cached_platforms:
                if cached_platforms[key] == target_cycle:
                    return get_total_load(list(key))

        cached_platforms[tupled_platform] = cycle

        transposed_matrix = transpose_matrix(current_platform)

        tilted_platform_north = transpose_matrix(platform_tilt_north(transposed_matrix))

        tilted_platform_west = platform_tilt_west(tilted_platform_north)

        tilted_platform_south = platform_tilt_south(tilted_platform_west)

        tilted_platform_east = platform_tilt_east(tilted_platform_south)

        current_platform = tilted_platform_east


lines: list[str] = open("input.txt").read().splitlines()

platform = transpose_matrix(lines)

tilted_platform = transpose_matrix(platform_tilt_north(platform))

total_load = get_total_load(tilted_platform)

total_load_after_cycles = get_total_load_after_cycles(lines, CYCLES)

print(f"Part 1: {total_load} | Part 2: {total_load_after_cycles}")
