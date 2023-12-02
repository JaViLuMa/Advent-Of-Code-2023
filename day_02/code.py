import re
from re import Pattern
from typing import Union


# Types
POSSIBLE_COLORS = Union["red", "green", "blue"]
COLORS = list[tuple[str, POSSIBLE_COLORS]]

# Constants
POSSIBLE_GAME: dict[POSSIBLE_COLORS, int] = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def get_colors(line: str) -> COLORS:
    colors_pattern: Pattern = r"(\d+)\s*(blue|red|green)"

    return re.findall(colors_pattern, line)


def check_if_game_is_possible(colors: COLORS) -> bool:
    for color in colors:
        number, color_type = int(color[0]), color[1]

        if POSSIBLE_GAME[color_type] < number:
            return False

    return True


def max_value_of_specific_color(colors: COLORS, color_type_arg: POSSIBLE_COLORS) -> int:
    max_value: int = 0

    for color in colors:
        number, color_type = int(color[0]), color[1]

        if color_type == color_type_arg and number > max_value:
            max_value = number

    return max_value


def fewest_number_of_cubes_of_each_color(colors: COLORS):
    multiplied_color_values: int = 1

    for color in POSSIBLE_GAME.keys():
        max_value: int = max_value_of_specific_color(colors, color)

        multiplied_color_values *= max_value

    return multiplied_color_values


lines: list[str] = []

with open("input.txt") as f:
    lines = f.read().splitlines()


sum_of_possible_games: int = 0
sum_of_fewest_number_of_cubes_of_each_color: int = 0

for line in lines:
    game_id_pattern: Pattern = r"Game \d+: "

    game_id: int = int(
        re.search(game_id_pattern, line).group(0).strip().replace(":", "").split(" ")[1]
    )

    line_without_game_id = re.sub(game_id_pattern, "", line)

    colors: COLORS = get_colors(line_without_game_id)

    if check_if_game_is_possible(colors):
        sum_of_possible_games += game_id

    sum_of_fewest_number_of_cubes_of_each_color += fewest_number_of_cubes_of_each_color(
        colors
    )

print(
    f"Part 1: {sum_of_possible_games} | Part 2: {sum_of_fewest_number_of_cubes_of_each_color}"
)
