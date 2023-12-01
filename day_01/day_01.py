
import re
import urllib.request
from urllib.request import Request

def main():
    str_data_lst = process_raw_input(1)
    list_nums = get_coors(str_data_lst)
    print(sum(list_nums))
   
def get_coors(data: list[str])-> list[int]:
    int_list = []
    for line in data:
        coor_points = re.findall(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line)
        if len(coor_points) >=1:
            first_num = word_to_num(coor_points[0])
            last_num = word_to_num(coor_points[-1])
            full_num = first_num + last_num
            int_list.append(int(full_num))
    return int_list

def word_to_num(data:str) -> str:
    comparison_dict = {"one":'1',"two":'2',"three":'3',"four":'4',"five":'5', "six":'6', "seven":'7', "eight": '8', "nine":'9'}
    if data in comparison_dict:
        return comparison_dict[data]
    return data

def process_raw_input(day_num) -> list[str]:
    aoc_request = Request(f'https://adventofcode.com/2023/day/{day_num}/input')
    aoc_request.add_header("Cookie","_ga=GA1.2.290855350.1670445740; _gid=GA1.2.1026598299.1701436696; session=53616c7465645f5f1d1d4327f1cab878a9dcde37e0f6b21048d3312f029d6b6d29842ae8293da5c6114babb5aeea894636c7a775ceba8592149c609913f41fb0; _ga_MHSNPJKWC7=GS1.2.1701449827.3.1.1701450196.0.0.0")
    html = urllib.request.urlopen(aoc_request).read()
    decoded_string = html.decode("utf-8")
    datalines = decoded_string.split('\n')
    return datalines

main()

