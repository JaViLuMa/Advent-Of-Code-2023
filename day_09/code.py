lines: list[str] = open("input.txt").read().splitlines()

sequences = [list(map(int, line.split())) for line in lines]


def calculate_differences(sequence: list[int]) -> list[list[int]]:
    differences: list[list[int]] = [sequence]

    while not all(x == 0 for x in differences[-1]):
        diffs = []

        for i in range(1, len(differences[-1])):
            diffs.append(differences[-1][i] - differences[-1][i - 1])

        differences.append(diffs)

    return differences


sum_of_extrapolated_values: int = 0
sum_of_reversed_extrapolated_values: int = 0

for sequence in sequences:
    differences = calculate_differences(sequence)
    reversed_differences = calculate_differences(sequence[::-1])

    current_extrapolated_value = 0
    current_reversed_extrapolated_value = 0

    for i in range(len(differences) - 2, -1, -1):
        sum_of_extrapolated_values += current_extrapolated_value + differences[i][-1]
        sum_of_reversed_extrapolated_values += (
            current_reversed_extrapolated_value + reversed_differences[i][-1]
        )

print(
    f"Part 1: {sum_of_extrapolated_values} | Part 2: {sum_of_reversed_extrapolated_values}"
)
