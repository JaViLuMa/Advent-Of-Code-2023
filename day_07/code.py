from collections import Counter


lines: list[str] = open("input.txt").read().splitlines()


STRENGTHS: dict[str, int] = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


HAND_TYPE = tuple[tuple[int], int]
HANDS_TYPE = list[HAND_TYPE]

hands: HANDS_TYPE = []


def counter_values(hand: HAND_TYPE) -> Counter[int]:
    return Counter(hand).values()


def sorted_hand(hand: HAND_TYPE) -> tuple[int]:
    return tuple(sorted(counter_values(hand), reverse=True))


def handle_jokers(hand: HAND_TYPE):
    number_of_jokers: int = hand.count(11)

    hand_with_joker_value: tuple[int] = ()
    hand_without_jokers: tuple[int] = ()

    for card in hand:
        if card == 11:
            hand_with_joker_value += (1,)
        else:
            hand_without_jokers += (card,)
            hand_with_joker_value += (card,)

    strength = list(sorted_hand(hand_without_jokers))

    if not strength:
        strength = (5,)
    else:
        strength[0] += number_of_jokers

    return tuple(strength), hand_with_joker_value


for line in lines:
    hand_original, bid = line.split(" ")

    hand: tuple[int] = tuple(STRENGTHS[card] for card in hand_original)

    hands.append((hand, int(bid)))


sorted_hands: HANDS_TYPE = sorted(
    hands, key=lambda hand: (tuple(sorted_hand(hand[0])), hand[0])
)

sorted_hands_with_jokers: HANDS_TYPE = sorted(
    hands, key=lambda hand: handle_jokers(hand[0])
)

total_winnings: int = sum(hand[-1] * rank for rank, hand in enumerate(sorted_hands, 1))
total_winnings_with_jokers: int = sum(
    hand[-1] * rank for rank, hand in enumerate(sorted_hands_with_jokers, 1)
)

print(f"Part 1: {total_winnings} | Part 2: {total_winnings_with_jokers}")
