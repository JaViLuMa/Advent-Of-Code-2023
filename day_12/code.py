from functools import lru_cache

lines: list[str] = open("input.txt").read().splitlines()


@lru_cache(maxsize=None)
def get_number_of_arrangements(
    springs: str, numbers_of_damaged_springs: tuple[int]
) -> int:
    arrangements: int = 0

    if springs == "":
        return 1 if len(numbers_of_damaged_springs) == 0 else 0

    if len(numbers_of_damaged_springs) == 0:
        return 1 if "#" not in springs else 0

    if springs[0] in ".?":
        arrangements += get_number_of_arrangements(
            springs[1:], numbers_of_damaged_springs
        )

    if springs[0] in "#?":
        if (
            numbers_of_damaged_springs[0] <= len(springs)
            and "." not in springs[: numbers_of_damaged_springs[0]]
            and (
                numbers_of_damaged_springs[0] == len(springs)
                or springs[numbers_of_damaged_springs[0]] != "#"
            )
        ):
            arrangements += get_number_of_arrangements(
                springs[numbers_of_damaged_springs[0] + 1 :],
                numbers_of_damaged_springs[1:],
            )

    return arrangements


total_number_of_arrangements: int = 0
total_number_of_arrangements_with_copies: int = 0

for line in lines:
    springs, damaged_springs = line.split()

    springs_copies = "?".join([springs] * 5)

    numbers_of_damaged_springs = tuple(map(int, damaged_springs.split(",")))
    numbers_of_damaged_springs_copies = numbers_of_damaged_springs * 5

    total_number_of_arrangements += get_number_of_arrangements(
        springs, numbers_of_damaged_springs
    )

    total_number_of_arrangements_with_copies += get_number_of_arrangements(
        springs_copies, numbers_of_damaged_springs_copies
    )

print(
    f"Part 1: {total_number_of_arrangements} | Part 2: {total_number_of_arrangements_with_copies}"
)
