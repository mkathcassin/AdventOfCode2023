import re
import urllib.request
from urllib.request import Request

test_data = ["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green","Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red","Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 1 blue, 14 red","Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]

class Session:
    sesh_id:int
    red: int
    blue: int
    green: int
    total: int

    def __init__(self,sesh_id, red,blue,green):
        self.sesh_id = sesh_id
        self.red = red
        self.blue = blue
        self.green = green
        
class GamesInfo():
    game_id: int
    sessions: list[Session]
    bag_total: dict[str,int] = {"red":0,"blue":0,"green":0}
    valid_bag:bool = False
    power_value = 0

    def __init__(self, game_id:int, sessions:list[Session]):
        self.game_id = game_id
        self.sessions = sessions
        red_totals = [s.red for s in self.sessions]
        blue_totals = [s.blue for s in self.sessions]
        green_totals = [s.green for s in self.sessions]
        self.bag_total["red"] = max(red_totals)
        self.bag_total["blue"] = max(blue_totals)
        self.bag_total["green"] = max(green_totals)
        if self.bag_total["red"] <= 12 and self.bag_total["green"] <= 13 and self.bag_total["blue"] <= 14:
            self.valid_bag = True
        self.power_value= self.bag_total["red"]*self.bag_total["green"]*self.bag_total["blue"]
        print("valid bag?l:"+str(self.bag_total)+" it is:"+ str(self.valid_bag))


def decode_data(data_lines) -> list[GamesInfo]:
    games_data:  list[GamesInfo] = []
    for i, line in enumerate(data_lines):
        if len(line) < 2: continue
        no_game_info = line.split(":")[1]
        sessions = no_game_info.split(";")
        seshes = []
        for j,sesh in enumerate(sessions):
            sesh_id = j+1
            red = num_or_none("red", sesh)
            blue = num_or_none("blue", sesh)
            green = num_or_none("green", sesh)
            sesh = Session(sesh_id,red,blue,green)
            seshes.append(sesh)
        game = GamesInfo(game_id = i+1,sessions = seshes)
        games_data.append(game)
    return games_data

def num_or_none(color:str, input:str):
    result = re.findall(r"\d*(?= {})".format(color), input)
    if len(result) == 0:
        return 0
    return int(result[0])

def main():
    str_list = process_raw_input(2)
    games_results = decode_data(str_list)
    id_total = 0
    power_total = 0
    for result in games_results:
        power_total = power_total + result.power_value
        if result.valid_bag:
            id_total = id_total + result.game_id
            print(result.game_id)
    print("The id total is: "+str(id_total))
    print("The power total is:"+ str(power_total))

def process_raw_input(day_num) -> list[str]:
    aoc_request = Request(f'https://adventofcode.com/2023/day/{day_num}/input')
    aoc_request.add_header("Cookie","_ga=GA1.2.290855350.1670445740; _gid=GA1.2.1026598299.1701436696; session=53616c7465645f5f1d1d4327f1cab878a9dcde37e0f6b21048d3312f029d6b6d29842ae8293da5c6114babb5aeea894636c7a775ceba8592149c609913f41fb0; _ga_MHSNPJKWC7=GS1.2.1701449827.3.1.1701450196.0.0.0")
    html = urllib.request.urlopen(aoc_request).read()
    decoded_string = html.decode("utf-8")
    datalines = decoded_string.split('\n')
    return datalines

main()