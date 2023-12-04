import re

lines: list[str] = open("input.txt").read().splitlines()

winning_numbers: list[list[int]] = []
numbers_we_have: list[list[int]] = []

for line in lines:
    winning_and_have_numbers = re.sub(r"Card\s+\d+:\s+", "", line).split("|")

    winning = list(
        map(int, re.sub(r"\s+", " ", winning_and_have_numbers[0]).strip().split(" "))
    )
    
    have = list(
        map(int, re.sub(r"\s+", " ", winning_and_have_numbers[1]).strip().split(" "))
    )

    winning_numbers.append(winning)
    numbers_we_have.append(have)

total_sum: int = 0

scratchcard_copies: list[int] = [1] * len(lines)

for i, nums in enumerate(numbers_we_have):
    have_set = set(numbers_we_have[i])
    winning_set = set(winning_numbers[i])

    length_of_intersection = len(have_set.intersection(winning_set))

    if length_of_intersection:
        total_sum += 2 ** (length_of_intersection - 1)

        for j in range(1, length_of_intersection + 1):
            scratchcard_copies[i + j] += scratchcard_copies[i]

print(f"Part 1: {total_sum} | Part 2: {sum(scratchcard_copies)}")
