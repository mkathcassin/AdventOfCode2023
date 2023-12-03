import re
import urllib.request
from urllib.request import Request

test_data = ["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green","Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red","Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 1 blue, 14 red","Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]
class Session:
    id:int
    red: int
    blue: int
    green: int
    total: int

    def __init__(self,sesh_id, red,blue,green):
        self.id = sesh_id
        self.red = red
        self.blue = blue
        self.green = green
        self.total = red+blue+green
        
class GamesInfo():
    game_id: int
    sessions: list[Session]
    higest_total: int

    def __init__(self, game_id:int, sessions:list[Session]):
        self.id = game_id
        self.sessions = sessions
        totals = [s.total for s in self.sessions]
        self.higest_total = max(totals)
        print("id is: "+str(game_id) +"   total is: " + str(self.higest_total))

def decode_data(data_lines) -> list[GamesInfo]:
    games_data:  list[GamesInfo] = []
    for i, line in enumerate(data_lines):
        sessions = line.split(";")
        seshes = []
        for i,sesh in enumerate(sessions):
            sesh_id = i+1
            red = num_or_none("red", line)
            blue = num_or_none("blue", line)
            green = num_or_none("green", line)
            sesh = Session(sesh_id,red,blue,green)
            seshes.append(sesh)
        game = GamesInfo(game_id = i+1,sessions = seshes)
        games_data.append(game)
    return games_data

def num_or_none(color:str, input:str):
    result = re.findall(r"\d(?= {})".format(color), input)
    if len(result) == 0:
        return 0
    return int(result[0])

def main():
    str_list = process_raw_input(2)
    games_results = decode_data(test_data)
    id_total = 0
    for result in games_results:
        if result.higest_total <= 14:
            id_total = id_total + result.id
    print("The total is: "+str(id_total))

def process_raw_input(day_num) -> list[str]:
    aoc_request = Request(f'https://adventofcode.com/2023/day/{day_num}/input')
    aoc_request.add_header("Cookie","_ga=GA1.2.290855350.1670445740; _gid=GA1.2.1026598299.1701436696; session=53616c7465645f5f1d1d4327f1cab878a9dcde37e0f6b21048d3312f029d6b6d29842ae8293da5c6114babb5aeea894636c7a775ceba8592149c609913f41fb0; _ga_MHSNPJKWC7=GS1.2.1701449827.3.1.1701450196.0.0.0")
    html = urllib.request.urlopen(aoc_request).read()
    decoded_string = html.decode("utf-8")
    datalines = decoded_string.split('\n')
    return datalines

main()