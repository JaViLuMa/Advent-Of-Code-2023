LENSES = dict[str, int]
BOXES = dict[int, LENSES]


def HASH(sequence: str) -> int:
    current_value: int = 0

    for char in sequence:
        current_value = ((current_value + ord(char)) * 17) % 256

    return current_value


def HASHMAP(sequences: list[str]) -> BOXES:
    boxes: BOXES = {box: {} for box in range(256)}

    for sequence in sequences:
        if "=" in sequence:
            sequence, value = sequence.split("=")

            hash_value = HASH(sequence)

            boxes[hash_value][sequence] = int(value)
        else:
            sequence, _ = sequence.split("-")

            hash_value = HASH(sequence)

            if sequence in boxes[hash_value]:
                del boxes[hash_value][sequence]

    return boxes


def specific_box_sum(lens: LENSES, box: int) -> int:
    return sum((box + 1) * (i + 1) * value for i, (_, value) in enumerate(lens.items()))


initial_sequence: list[str] = open("input.txt").read().split(",")

total_HASH_sum: int = sum(HASH(sequence) for sequence in initial_sequence)

populated_boxes = HASHMAP(initial_sequence)

total_HASHMAP_sum: int = sum(
    specific_box_sum(populated_boxes[box], box) for box in range(256)
)

print(f"Part 1: {total_HASH_sum} | Part 2: {total_HASHMAP_sum}")
