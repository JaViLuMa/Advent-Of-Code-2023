lines: list[str] = []

with open('input.txt') as f:
    lines = f.read().splitlines()

only_digits_from_lines: list[int] = []

for line in lines:
    only_digits_from_lines.append([int(digit) for digit in line if digit.isdigit()])

sum_of_first_and_last_digits: int = 0

for digits in only_digits_from_lines:
    if (len(digits) == 0):
        continue

    if len(digits) == 1:
        digits.append(digits[0])

    number_to_add_to_sum: int = int(f"{digits[0]}{digits[-1]}")

    sum_of_first_and_last_digits += number_to_add_to_sum

print(f"Part 1: {sum_of_first_and_last_digits}")
