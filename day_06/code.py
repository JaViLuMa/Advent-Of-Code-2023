import re
from math import sqrt, pow, floor, ceil

lines: list[str] = open("input.txt").read().splitlines()

times: list[int] = []
distances: list[int] = []

for line in lines:
    if "Time" in line:
        without_time_prefix = re.sub(r"Time:\s+", "", line)
        cleared_times = list(
            map(int, re.sub(r"\s+", " ", without_time_prefix).split(" "))
        )

        times = cleared_times

    if "Distance" in line:
        without_distance_prefix = re.sub(r"Distance:\s+", "", line)
        cleared_distances = list(
            map(int, re.sub(r"\s+", " ", without_distance_prefix).split(" "))
        )

        distances = cleared_distances


def calculate_num_of_ways_to_beat_record(t: list[int], d: list[int]) -> int:
    num_of_ways_to_beat_record: int = 1

    for i in range(len(t)):
        a = t[i] - sqrt(pow(t[i], 2) - (4 * d[i]))
        b = t[i] + sqrt(pow(t[i], 2) - (4 * d[i]))

        lower_bound = floor(a / 2)
        upper_bound = ceil(b / 2)

        num_of_ways_to_beat_record *= upper_bound - lower_bound - 1

    return num_of_ways_to_beat_record


num_of_ways_to_beat_record: int = calculate_num_of_ways_to_beat_record(times, distances)

joined_time = [int("".join(list(map(str, times))))]
joined_distance = [int("".join(list(map(str, distances))))]

joined_num_of_ways_to_beat_record = calculate_num_of_ways_to_beat_record(
    joined_time, joined_distance
)

print(
    f"Part 1: {num_of_ways_to_beat_record} | Part 2: {joined_num_of_ways_to_beat_record}"
)
