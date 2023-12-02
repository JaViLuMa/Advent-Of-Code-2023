lines: list[str] = []

with open('input.txt') as f:
    lines = f.read().splitlines()

only_digits_from_lines: list[str] = []

numbers: dict[str, str] = {
    "one": "on1e",
    "two": "tw2o",
    "three": "th3ree",
    "four": "fou4r",
    "five": "fiv5e",
    "six": "si6x",
    "seven": "sev7en",
    "eight": "eig8ht",
    "nine": "nin9e",
}

numbered_lines: list[str] = []

for line in lines:
    for number in numbers:
        line = line.replace(number, numbers[number])

    numbered_lines.append(line)

for numbered_line in numbered_lines:
    only_digits_from_lines.append([int(digit) for digit in numbered_line if digit.isdigit()])

sum_of_first_and_last_digits: int = 0

for digits in only_digits_from_lines:
    if (len(digits) == 0):
        continue

    if len(digits) == 1:
        digits.append(digits[0])

    number_to_add_to_sum: int = int(f"{digits[0]}{digits[-1]}")

    sum_of_first_and_last_digits += number_to_add_to_sum

print(f"Part 2: {sum_of_first_and_last_digits}")
