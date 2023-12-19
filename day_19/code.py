import re


def parse_workflows(workflow_line):
    pattern = re.compile(r"(.*)({.*})")

    workflows = workflow_line.split("\n")

    workflow_map = {}

    for workflow in workflows:
        match = pattern.match(workflow)

        if match:
            parsed_group = match.group(2).strip("{}").split(",")

            workflow_map[match.group(1)] = ([], parsed_group[-1])

            for step in parsed_group[:-1]:
                condition, destination = step.split(":")

                condition_key, comparator, value = (
                    condition[0],
                    condition[1],
                    condition[2:],
                )

                workflow_map[match.group(1)][0].append(
                    (condition_key, comparator, int(value), destination)
                )

    return workflow_map


def parse_parts(parts_line):
    splitted_parts = parts_line.split("\n")

    parts = []

    for part in splitted_parts:
        parsed_part = part.strip("{}").split(",")

        parsed_parts_list = {}

        for p in parsed_part:
            variable, value = p.split("=")

            parsed_parts_list[variable] = int(value)

        parts.append(parsed_parts_list)

    return parts


def get_parsed_inputs(lines):
    workflow_line, parts_line = lines

    workflow_map = parse_workflows(workflow_line)
    parts = parse_parts(parts_line)

    return workflow_map, parts


def should_get_accepted(parts, workflow_map, key="in"):
    if key == "R":
        return False

    if key == "A":
        return True

    workflow_conditions, fallback = workflow_map[key]

    for condition_key, comparator, value, destination in workflow_conditions:
        if eval(f"{parts[condition_key]}{comparator}{value}"):
            return should_get_accepted(parts, workflow_map, destination)

    return should_get_accepted(parts, workflow_map, fallback)


def get_total_accepted_parts(workflow_map, parts_array):
    total_accepted_parts = 0

    for parts in parts_array:
        if should_get_accepted(parts, workflow_map):
            total_accepted_parts += sum(parts.values())

    return total_accepted_parts


def get_total_accepted_parts_with_all_distinct_combinations(
    parts, workflow_map, xmas_ranges, key="in"
):
    if key == "R":
        return False

    if key == "A":
        product = 1

        for low_range, high_range in xmas_ranges.values():
            product *= high_range - low_range + 1

        return product

    workflow_conditions, fallback = workflow_map[key]

    running_total = 0

    for condition_key, comparator, value, destination in workflow_conditions:
        low_range, high_range = xmas_ranges[condition_key]

        if comparator == "<":
            included_range = (low_range, value - 1)
            excluded_range = (value, high_range)
        else:
            included_range = (value + 1, high_range)
            excluded_range = (low_range, value)

        if included_range[0] <= included_range[1]:
            xmas_ranges_copy = dict(xmas_ranges)

            xmas_ranges_copy[condition_key] = included_range

            running_total += get_total_accepted_parts_with_all_distinct_combinations(
                parts, workflow_map, xmas_ranges_copy, destination
            )

        if excluded_range[0] <= excluded_range[1]:
            xmas_ranges = dict(xmas_ranges)

            xmas_ranges[condition_key] = excluded_range
        else:
            break
    else:
        running_total += get_total_accepted_parts_with_all_distinct_combinations(
            parts, workflow_map, xmas_ranges, fallback
        )

    return running_total


lines = open("input.txt").read().split("\n\n")

workflow_map, parts = get_parsed_inputs(lines)

total_accepted_parts = get_total_accepted_parts(workflow_map, parts)

xmas_ranges_dict = {key: (1, 4000) for key in "xmas"}

total_accepted_parts_with_all_distinct_combinations = (
    get_total_accepted_parts_with_all_distinct_combinations(
        parts, workflow_map, xmas_ranges_dict
    )
)

print(
    f"Part 1: {total_accepted_parts} | Part 2: {total_accepted_parts_with_all_distinct_combinations}"
)
