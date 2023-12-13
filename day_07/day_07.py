import urllib.request
import re
from collections import Counter
from urllib.request import Request

test_data = '32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483'


class Hand():
    raw_hand: str
    bid: int
    int_hand:list[int]
    hand_type: int
    rank: int

    def convert_hand(self):
        temp_hand= []
        for card in self.raw_hand:
            match card:
                case 'A':
                    temp_hand.append(14)
                case 'K':
                    temp_hand.append(13)
                case 'Q':
                    temp_hand.append(12)
                case 'J':
                    temp_hand.append(11)
                case 'T':
                    temp_hand.append(10)
                case _:
                    temp_hand.append(int(card))
        temp_hand.sort(reverse=True)
        self.int_hand = temp_hand
    
    def hand_type(self):
        sorted_hand = sorted(Counter(self.int_hand).values(), reverse = True)
        match sorted_hand[0]:
            case 5:
                self.hand_type=6
            case 4:
                self.hand_type=5
            case 3:
                if sorted_hand[1]==2:
                    self.hand_type=3
                else:
                    self.hand_type=4
            case 2:
                if sorted_hand[1]==2:
                    self.hand_type=2
                else:
                    self.hand_type=1
            case _:
                self.hand_type=0

    def __init__(self,hand, bid):
        self.raw_hand = hand
        self.bid = int(bid)
        self.convert_hand()
        self.hand_type()




def process_raw_input(day_num) -> list[str]:
    print('inputing')
    aoc_request = Request(f'https://adventofcode.com/2023/day/{day_num}/input')
    aoc_request.add_header("Cookie","_ga=GA1.2.290855350.1670445740; _gid=GA1.2.1026598299.1701436696; session=53616c7465645f5f1d1d4327f1cab878a9dcde37e0f6b21048d3312f029d6b6d29842ae8293da5c6114babb5aeea894636c7a775ceba8592149c609913f41fb0; _ga_MHSNPJKWC7=GS1.2.1701449827.3.1.1701450196.0.0.0")
    html = urllib.request.urlopen(aoc_request).read()
    decoded_string = html.decode("utf-8")
    return decoded_string

def decode_data(raw_data):
    hands = []
    hand_bids = re.findall(r'(\w+) (\d+)', raw_data)
    for hand_bid in hand_bids:
        hands.append(Hand(hand_bid[0],hand_bid[1]))

    return hands

def compare_hands(hands):
    temp_rankings = []
    for i in reversed(range(7)):
        section = [hand for hand in hands if hand.hand_type == i]
        section.sort(key=lambda h:h.int_hand, reverse=True)
        if len(section) > 0:
            temp_rankings.extend(section)
    temp_rankings_rev = temp_rankings[::-1]
    for hand in hands:
        rank = temp_rankings_rev.index(hand)
        hand.rank = rank+1

def total_winnings(hands:Hand):
    total = 0
    for hand in hands:
        print('hand: '+ hand.raw_hand +'   vals:'+ ''.join(str(hand.int_hand)) + '   ranking'+ str(hand.rank))
        total += (hand.bid * hand.rank)
    print(total)


def main():
    raw_data = process_raw_input(7)
    hands = decode_data(raw_data)
    hands.sort(key=lambda x: x.hand_type, reverse=True)
    compare_hands(hands)
    total_winnings(hands)

main()
print('The answer is: 246424613')