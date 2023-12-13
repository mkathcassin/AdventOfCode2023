import urllib.request
import re
from urllib.request import Request

test_data = 'Time:      7  15   30\nDistance:  9  40  200\n'

def process_raw_input(day_num) -> list[str]:
    print('inputing')
    aoc_request = Request(f'https://adventofcode.com/2023/day/{day_num}/input')
    aoc_request.add_header("Cookie","_ga=GA1.2.290855350.1670445740; _gid=GA1.2.1026598299.1701436696; session=53616c7465645f5f1d1d4327f1cab878a9dcde37e0f6b21048d3312f029d6b6d29842ae8293da5c6114babb5aeea894636c7a775ceba8592149c609913f41fb0; _ga_MHSNPJKWC7=GS1.2.1701449827.3.1.1701450196.0.0.0")
    html = urllib.request.urlopen(aoc_request).read()
    decoded_string = html.decode("utf-8")
    return decoded_string

def decode_data(raw_string):
    times, distances, nl = raw_string.split('\n')
    times = list(map(int, re.findall('\d+', times)))
    distances = list(map(int, re.findall('\d+', distances)))

    return times,distances

def decode_data_pt2(raw_string):
    times, distances, nl = raw_string.split('\n')
    times = int(''.join(re.findall('\d+', times)))
    distances = int(''.join(re.findall('\d+', distances)))

    return times,distances

def main_pt2():
    data_string = process_raw_input(6)
    time, distance = decode_data_pt2(data_string)

    win = 0
    for t in range(time):
        result = t * (time-t)
        if result > distance:
            win += 1
    print(win)

def main():
    data_string = process_raw_input(6)
    times, distances = decode_data(data_string)

    possible_wins = []
    for time, distance in zip(times, distances):
        win = 0
        for t in range(time):
            result = t * (time-t)
            if result > distance:
                win += 1
        possible_wins.append(win)
    print(possible_wins)

    win_product = 1
    for w in possible_wins:
        win_product = win_product*w 
    print(win_product)

main()
main_pt2()