lines: list[str] = open("input.txt").read().split("\n\n")


MIRROR = list[str]
TR_MIRROR = list[tuple[str]]
MIRRORS = list[MIRROR]


def parse_mirrors() -> MIRRORS:
    mirrors: MIRRORS = []

    for line in lines:
        mirrors.append(line.splitlines())

    return mirrors


def find_reflection(mirror: MIRROR | TR_MIRROR, smudged=False) -> int:
    for mirror_row in range(1, len(mirror)):
        above_mirror_row = mirror[:mirror_row][::-1]
        below_mirror_row = mirror[mirror_row:]

        above_mirror_row = above_mirror_row[: len(below_mirror_row)]
        below_mirror_row = below_mirror_row[: len(above_mirror_row)]

        if smudged:
            errors: int = 0

            zipped_above_and_below = zip(above_mirror_row, below_mirror_row)

            for above_row, below_row in zipped_above_and_below:
                zipped_rows = zip(above_row, below_row)

                for above, below in zipped_rows:
                    if above != below:
                        errors += 1

            if errors == 1:
                return mirror_row
        else:
            if above_mirror_row == below_mirror_row:
                return mirror_row

    return 0


def transpose_mirror(mirror: MIRROR) -> TR_MIRROR:
    return list(zip(*mirror))


def find_reflection_based_on_columns(mirror: MIRROR, smudged=False) -> int:
    transposed_mirror = transpose_mirror(mirror)

    return find_reflection(transposed_mirror, smudged)


mirrors: MIRRORS = parse_mirrors()

notes_sum: int = 0
notes_with_smudges_sum: int = 0

for mirror in mirrors:
    notes_sum += find_reflection(mirror) * 100
    notes_sum += find_reflection_based_on_columns(mirror)

    notes_with_smudges_sum += find_reflection(mirror, True) * 100
    notes_with_smudges_sum += find_reflection_based_on_columns(mirror, True)

print(f"Part 1: {notes_sum} | Part 2: {notes_with_smudges_sum}")
