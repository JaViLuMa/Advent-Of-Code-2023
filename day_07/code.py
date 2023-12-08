from collections import Counter

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


lines: list[str] = open("input.txt").read().splitlines()

hands: HANDS_TYPE = []
hands_with_jokers: HANDS_TYPE = []


for line in lines:
    hand_original, bid = line.split(" ")

    hand_strength: tuple[int] = tuple(STRENGTHS[card] for card in hand_original)
    hand_values: tuple[int] = tuple(
        sorted(Counter(hand_original).values(), reverse=True)
    )

    joker_count: int = hand_strength.count(11)

    hand_with_joker_value: tuple[int] = tuple(
        1 if card == 11 else card for card in hand_strength
    )

    hand_without_jokers: tuple[int] = tuple(
        card for card in hand_strength if card != 11
    )

    hand_without_jokers_values = Counter(hand_without_jokers).values()

    sorted_hand_without_jokers: list[int] = list(
        sorted(hand_without_jokers_values, reverse=True)
    )

    if not sorted_hand_without_jokers:
        sorted_hand_without_jokers = (5,)
    else:
        sorted_hand_without_jokers[0] += joker_count

        sorted_hand_without_jokers = tuple(sorted_hand_without_jokers)

    hands.append((hand_strength, hand_values, int(bid)))
    hands_with_jokers.append(
        (hand_with_joker_value, sorted_hand_without_jokers, int(bid))
    )


sorted_hands = sorted(hands, key=lambda hand: (hand[1], hand[0]))
sorted_hands_with_jokers = sorted(
    hands_with_jokers, key=lambda hand: (hand[1], hand[0])
)


total_winnings: int = sum(hand[-1] * rank for rank, hand in enumerate(sorted_hands, 1))
total_winnings_with_jokers: int = sum(
    hand[-1] * rank for rank, hand in enumerate(sorted_hands_with_jokers, 1)
)

print(f"Part 1: {total_winnings} | Part 2: {total_winnings_with_jokers}")
