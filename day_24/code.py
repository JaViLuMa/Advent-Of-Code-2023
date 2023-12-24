import sympy


LEAST = 200000000000000
MOST = 400000000000000


def get_point_and_velocity(lines):
    points_array = []
    velocities_array = []

    for line in lines:
        points_string, velocities_string = line.split(" @ ")

        points_array.append(tuple(map(int, points_string.split(", "))))
        velocities_array.append(tuple(map(int, velocities_string.split(", "))))

    return points_array, velocities_array


def second_point(px, py, pz, vx, vy, vz):
    return px + vx, py + vy, pz + vz


def get_slope_without_Z(p1x, p1y, p2x, p2y):
    return (p2y - p1y) / (p2x - p1x)


def get_B(p1x, p1y, slope):
    return p1y - slope * p1x


def create_linear_function(points_arr, velocities_arr):
    linear_equations = []

    for points, velocities in zip(points_arr, velocities_arr):
        new_point = second_point(*points, *velocities)

        slope = get_slope_without_Z(*points[:-1], *new_point[:-1])

        B = get_B(*points[:-1], slope)

        linear_equations.append((slope, B))

    return linear_equations


def get_intersecting_points(points, velocities, linear_equations):
    intersecting_points = 0

    for index, (point, velocity, linear_function) in enumerate(
        zip(points, velocities, linear_equations)
    ):
        for other_point, other_velocity, other_linear_function in zip(
            points[index + 1 :], velocities[index + 1 :], linear_equations[index + 1 :]
        ):
            slope, B = linear_function
            other_slope, other_B = other_linear_function

            if slope == other_slope:
                continue

            x = (other_B - B) / (slope - other_slope)
            y = slope * x + B

            if LEAST <= x <= MOST and LEAST <= y <= MOST:
                if all(
                    (x - point[0]) * velocity[0] >= 0
                    and (y - point[1]) * velocity[1] >= 0
                    for point, velocity in zip(
                        (point, other_point), (velocity, other_velocity)
                    )
                ):
                    intersecting_points += 1

    return intersecting_points


def get_sum_of_initial_position(points, velocities):
    equations = []

    xr, yr, zr, xvr, yvr, zvr = sympy.symbols("xr yr zr xvr, yvr, zvr")

    for index, (p, v) in enumerate(zip(points, velocities)):
        px, py, pz = p
        vx, vy, vz = v

        equations.append((xr - px) * (vy - yvr) - (yr - py) * (vx - xvr))
        equations.append((yr - py) * (vz - zvr) - (zr - pz) * (vy - yvr))

        if index < 2:
            continue

        answers = [
            solution
            for solution in sympy.solve(equations)
            if all(x % 1 == 0 for x in solution.values())
        ]

        if len(answers) == 1:
            break

    return answers[0][xr] + answers[0][yr] + answers[0][zr]


lines = open("input.txt").read().splitlines()

points, velocities = get_point_and_velocity(lines)

linear_equations = create_linear_function(points, velocities)

intersecting_points = get_intersecting_points(points, velocities, linear_equations)

sum_of_initial_position = get_sum_of_initial_position(points, velocities)

print(f"Part 1: {intersecting_points} | Part 2: {sum_of_initial_position}")
