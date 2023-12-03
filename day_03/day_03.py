
from ast import Try
import urllib.request
from urllib.request import Request
import re

test_data= ["467..114..",
            "...*......",
            "..35..633.",
            "......#...",
            "617*......",
            ".....+.58.",
            "..592.....",
            "......755.",
            "...$.*....",
            ".664.598.."]

class symbol():
    symbl:str
    x:int 
    y:int
    surround_coors: list[(int,int)]

    def __init__(self,x,y,char):
        self.x=x 
        self.y=y
        self.symbl=char

symbols = []
parts = []

def decode_date(lines):
    coors = [["." for i in range(len(lines))] for j in range(len(lines[0]))]
    for i,line in enumerate(lines):
        for j,char in enumerate(line):
            if re.findall("[^\w.\n]",char):
                #print("symbol found: "+char)
                new_symbol:symbol = symbol(x =i, y=j,char=char)
                new_symbol.surround_coors = surrounding_coordinates(i,j,len(lines),len(lines[0]))
                symbols.append(new_symbol)
            coors[i][j]=char
    raw_coors = coors
    return coors


def process_raw_input(day_num) -> list[str]:
    aoc_request = Request(f'https://adventofcode.com/2023/day/{day_num}/input')
    aoc_request.add_header("Cookie","_ga=GA1.2.290855350.1670445740; _gid=GA1.2.1026598299.1701436696; session=53616c7465645f5f1d1d4327f1cab878a9dcde37e0f6b21048d3312f029d6b6d29842ae8293da5c6114babb5aeea894636c7a775ceba8592149c609913f41fb0; _ga_MHSNPJKWC7=GS1.2.1701449827.3.1.1701450196.0.0.0")
    html = urllib.request.urlopen(aoc_request).read()
    decoded_string = html.decode("utf-8")
    datalines = decoded_string.split('\n')
    return datalines

def get_full_num(x,y, raw_coors):
    full_number = [raw_coors[x][y]]
    pos_limit_reached = False
    neg_limit_reached = False
    for i in range(1,len(raw_coors[x])):
        try:
            char = raw_coors[x][y+i]
            if not char.isdigit():
                pos_limit_reached = True
        except:
            pos_limit_reached = True
            continue
        try:
            char = raw_coors[x][y-i]
            if not char.isdigit():
                neg_limit_reached = True
        except:
            neg_limit_reached = True
            continue

        if raw_coors[x][y+i].isdigit() and pos_limit_reached == False:
            digit= raw_coors[x][y+i]
            full_number.append(digit)

        if  raw_coors[x][y-i].isdigit() and neg_limit_reached == False:
            digit= raw_coors[x][y-i]
            full_number.insert(0,digit)
        
        if pos_limit_reached and neg_limit_reached:
            break
    try:
        full_int = int(''.join(full_number))
    except:
        print(full_number + " is not a valid int")
    return full_int

def surrounding_coordinates(x:int,y:int,limit_x,limit_y) -> list[(int,int)]:
   coordinates = []
   
   for i in range(-1,2):
       coor_x = x+i 
       for j in range(-1,2):
           coor_y= y+j 
           if coor_x >= 0 and coor_x < limit_x and coor_y>=0 and coor_y < limit_y:
               coordinates.append((coor_x,coor_y))     
   return coordinates;


def main():
    raw_lines = process_raw_input(3)
    raw_coors = decode_date(raw_lines)
    for sym in symbols:
        for coor in sym.surround_coors:
            char = raw_coors[coor[0]][coor[1]]
            if char.isdigit():
                num = get_full_num(coor[0],coor[1],raw_coors)
                print(num)
                parts.append(num)
    #There is most likely on purpose duplicate values
    set_parts = set(parts)
    for part in set_parts:
        print(part)
    print(sum(set_parts))


main()