from typing import Union

MAP_TYPE = list[list[int]]
INPUT_TYPE = dict[str, Union[list[int], MAP_TYPE]]


KEYS = [
    "seed_to_soil_map",
    "soil_to_fertilizer_map",
    "fertilizer_to_water_map",
    "water_to_light_map",
    "light_to_temperature_map",
    "temperature_to_humidity_map",
    "humidity_to_location_map",
]


def parse_input(input_text: str) -> INPUT_TYPE:
    lines = input_text.splitlines()
    current_section: str = None
    data: INPUT_TYPE = {}

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if ":" in line:
            parts = line.split(":")
            current_section = parts[0].replace("-", "_").replace(" ", "_").lower()
            data[current_section] = []

            if current_section == "seeds" and len(parts) > 1:
                seed_values = parts[1].strip()

                if seed_values:
                    data[current_section] = list(map(int, seed_values.split()))
        else:
            values = list(map(int, line.split()))

            data[current_section].append(values)

    return data


def transform_seed_through_map(seed: int, transformation_map: MAP_TYPE) -> int:
    for destination_start, source_start, range_length in transformation_map:
        source_end = source_start + range_length

        if source_start <= seed < source_end:
            return destination_start + (seed - source_start)

    return seed


def transform_seed_range_through_map(
    seed_range: tuple[int, int], transformation_map: MAP_TYPE
) -> list[tuple[int, int]]:
    range_start, range_end = seed_range

    transformed_ranges: list[tuple[int, int]] = []

    for destination_start, source_start, range_length in transformation_map:
        source_end = source_start + range_length - 1

        if source_start <= range_end and range_start <= source_end:
            overlap_start = max(range_start, source_start)
            overlap_end = min(range_end, source_end)

            offset = destination_start - source_start

            transformed_ranges.append((overlap_start + offset, overlap_end + offset))

    return transformed_ranges if transformed_ranges else [seed_range]


def merge_overlapping_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []

    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged_ranges: list[tuple[int, int]] = [sorted_ranges[0]]

    for current in sorted_ranges[1:]:
        last = merged_ranges[-1]

        if current[0] <= last[1] + 1:
            merged_ranges[-1] = (last[0], max(last[1], current[1]))
        else:
            merged_ranges.append(current)

    return merged_ranges


input_text: str = open("input.txt").read()
parsed_data: INPUT_TYPE = parse_input(input_text)

min_location_single_seeds: float = float("inf")

for seed in parsed_data["seeds"]:
    for key in KEYS:
        seed = transform_seed_through_map(seed, parsed_data[key])

    min_location_single_seeds = min(min_location_single_seeds, seed)

seed_ranges: list[tuple[int, int]] = [
    (start, start + length - 1)
    for start, length in zip(parsed_data["seeds"][::2], parsed_data["seeds"][1::2])
]

for key in KEYS:
    updated_ranges: list[tuple[int, int]] = []

    for seed_range in seed_ranges:
        updated_ranges.extend(
            transform_seed_range_through_map(seed_range, parsed_data[key])
        )

    seed_ranges = merge_overlapping_ranges(updated_ranges)

min_location_ranges: int = min(start for start, end in seed_ranges)

print(f"Part 1: {min_location_single_seeds} | Part 2: {min_location_ranges}")
