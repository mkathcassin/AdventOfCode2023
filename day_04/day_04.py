from dataclasses import dataclass
import urllib.request
from urllib.request import Request
import re
import copy

@dataclass
class lotto_ticket():
    ticket_id: int
    winning_numbers: list[int]
    my_numbers: list[int]
    number_wins: int

test_data = [
            "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
            "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
            "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
            "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
            "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
            "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
            ]

def decode_data(lines: list[str]):
    tickets=[]
    for line in lines:
        if(line ==""): continue
        numbers = line.split(':')[1]
        winning_numbers = numbers.split('|')[0]
        losing_numbers = numbers.split('|')[1]
        w_nums = re.findall('\d+',winning_numbers)
        w_ints = [eval(i) for i in w_nums]
        l_nums = re.findall('\d+', losing_numbers)
        l_ints = [eval(i) for i in l_nums]
        tickets.append((w_ints,l_ints))
    return(tickets)

def ticket_total(w_nums, my_nums)->int:
    w_set = set(w_nums)
    my_set = set(my_nums)
    winners = w_set.intersection(my_set)
    if len(winners)==0 :
        return 0
    if len(winners)==1:
        return 1
    total_points = 2**(len(winners)-1)
    return total_points

def decode_date_part2(data:list[str])-> list[lotto_ticket]:
    tickets = []
    for i,line in enumerate(data):
        if line == "": continue
        numbers = line.split(':')[1]
        winning_numbers = numbers.split('|')[0]
        losing_numbers = numbers.split('|')[1]
        w_nums = re.findall('\d+',winning_numbers)
        w_ints = [eval(i) for i in w_nums]
        l_nums = re.findall('\d+', losing_numbers)
        l_ints = [eval(i) for i in l_nums]
        w_set = set(w_ints)
        my_set = set(l_ints)
        winners = w_set.intersection(my_set)
        ticket = lotto_ticket(i+1,w_ints,l_ints,len(winners))
        tickets.append(ticket)
    return tickets

def process_tickets(tickets:list[lotto_ticket]):
    unprocessed_tickets = tickets
    for i in range(1,len(tickets)+1):
        print("processing ticket: "+str(i))
        in_progress_tickets = [t for t in unprocessed_tickets if t.ticket_id == i]
        for t_copy in in_progress_tickets:
            for j in range(1,in_progress_tickets[0].number_wins+1):
                unprocessed_tickets.append(copy.copy(tickets[j+i-1]))
    print(len(unprocessed_tickets))

def process_raw_input(day_num) -> list[str]:
    aoc_request = Request(f'https://adventofcode.com/2023/day/{day_num}/input')
    aoc_request.add_header("Cookie","_ga=GA1.2.290855350.1670445740; _gid=GA1.2.1026598299.1701436696; session=53616c7465645f5f1d1d4327f1cab878a9dcde37e0f6b21048d3312f029d6b6d29842ae8293da5c6114babb5aeea894636c7a775ceba8592149c609913f41fb0; _ga_MHSNPJKWC7=GS1.2.1701449827.3.1.1701450196.0.0.0")
    html = urllib.request.urlopen(aoc_request).read()
    decoded_string = html.decode("utf-8")
    datalines = decoded_string.split('\n')
    return datalines

def main_part1():
    raw_lines = process_raw_input(4)
    ticket_nums = decode_data(raw_lines)
    ticket_values=[]
    for ticket in ticket_nums:
        ticket_values.append(ticket_total( ticket[0],ticket[1]))
    print(sum(ticket_values))

def main_part2():
    raw_lines = process_raw_input(4)
    tickets = decode_date_part2(raw_lines)
    process_tickets(tickets)

main_part2()