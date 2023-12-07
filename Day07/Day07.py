""" Advent of Code 2023, Day 7
    Day 7: Camel Cards
    Author: Chi-Kit Pao
"""

from collections import defaultdict
import copy
import os
import time


def get_card_value(card, part):
    if part == 1:
        value_list = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    else:
        value_list = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
    return value_list.index(card[0])


def get_answer(lines, part):
    hands = []
    for line in lines:
        cards, bid = line.split()
        hands.append(Hand(cards, int(bid), part))
    hands.sort(key=lambda h: h.hash(part))
    return sum([hand.bid * i for i, hand in enumerate(hands, 1)])


class Hand:
    # Differences to normal card game:
    # - Five of a kind is possible
    # - No Straights or related.
    # - No Flush or related.
    # - Card order is important on same rank.
    RANK_HIGH_CARD = 0
    RANK_ONE_PAIR = 1
    RANK_TWO_PAIRS = 2
    RANK_THREE_OF_A_KIND = 3
    RANK_FULL_HOUSE = 4
    RANK_FOUR_OF_A_KIND = 5
    RANK_FIVE_OF_A_KIND = 6

    def __init__(self, cards, bid, part):
        self.cards = copy.copy(cards)
        self.bid = bid
        self.rank = Hand.RANK_HIGH_CARD
        self.__evaluate_cards(part)

    # def compare(self, other):
    #     if self.rank != other.rank:
    #         return self.rank - other.rank

    #     for i in range(len(self.cards)):
    #         diff = get_card_value(self.cards[0]) - get_card_value(other.cards[0])
    #         if diff != 0:
    #             return diff
    #     raise AssertionError("Both hands are the same!")

    def hash(self, part):
        result = 0
        for i in range(5):
            result += get_card_value(self.cards[4 - i], part) * 100**i
        result += self.rank * 100**5
        return result

    def __evaluate_cards(self, part):
        assert 1 <= part <= 2
        cards = list(self.cards)
        if part == 2:
            joker_count = cards.count("J")
            card_count = defaultdict(int)
            for c in cards:
                card_count[c] += 1
            if joker_count > 0:
                del card_count["J"]
            if joker_count == 5:
                cards = ["A"] * 5
            elif joker_count == 0:
                pass
            else:
                temp = [(k, v) for k, v in card_count.items()]
                temp.sort(key=lambda p: p[1] * 100 + get_card_value(p[0], part), reverse=True) 
                cards = [x if x != "J" else temp[0][0] for x in cards]
        cards.sort(key=lambda x: get_card_value(x, part), reverse=True)
        values = list(map(lambda x: get_card_value(x, part), cards))
        value_differences = []
        value_diff_bits = 0
        for i in range(0, 4):
            value_differences.append(values[i] - values[i + 1])
            if values[i] != values[i + 1]:
                value_diff_bits |= 1 << i

        if value_diff_bits == 0:
            self.rank = Hand.RANK_FIVE_OF_A_KIND
            return
        if value_diff_bits == 0xF:
            self.rank = Hand.RANK_HIGH_CARD
            return
        if value_diff_bits == 0x1 or value_diff_bits == 0x8:
            self.rank = Hand.RANK_FOUR_OF_A_KIND
            return
        if value_diff_bits == 0x2 or value_diff_bits == 0x4:
            self.rank = Hand.RANK_FULL_HOUSE
            return
        if value_diff_bits == 0x3 or value_diff_bits == 0x9 or value_diff_bits == 0xC:
            self.rank = Hand.RANK_THREE_OF_A_KIND
            return
        if value_differences.count(0) == 1:
            self.rank = Hand.RANK_ONE_PAIR
            return

        self.rank = Hand.RANK_TWO_PAIRS


def main():
    start_time = time.time()
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))

    print("Question 1: What are the total winnings?")
    print(f"Answer: {get_answer(lines, 1)}")
    print("Question 2: What are the new total winnings?")
    print(f"Answer: {get_answer(lines, 2)}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: What are the total winnings?
# Answer: 250120186
# Question 2: What are the new total winnings?
# Answer: 250665248
# Time elapsed: 0.020941495895385742 s
