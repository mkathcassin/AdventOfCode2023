import urllib.request
import re
from urllib.request import Request
from pathlib import Path

test_string = 'seeds: 79 14 55 13\n\nseed-to-soil map:\n50 98 2\n52 50 48\n\nsoil-to-fertilizer map:\n0 15 37\n37 52 2\n39 0 15\n\nfertilizer-to-water map:\n49 53 8\n0 11 42\n42 0 7\n57 7 4\n\nwater-to-light map:\n88 18 7\n18 25 70\n\nlight-to-temperature map:\n45 77 23\n81 45 19\n68 64 13\n\ntemperature-to-humidity map:\n0 69 1\n1 0 69\n\nhumidity-to-location map:\n60 56 37\n56 93 4\n\n'

def process_raw_input(day_num) -> list[str]:
    print('inputing')
    aoc_request = Request(f'https://adventofcode.com/2023/day/{day_num}/input')
    aoc_request.add_header("Cookie","_ga=GA1.2.290855350.1670445740; _gid=GA1.2.1026598299.1701436696; session=53616c7465645f5f1d1d4327f1cab878a9dcde37e0f6b21048d3312f029d6b6d29842ae8293da5c6114babb5aeea894636c7a775ceba8592149c609913f41fb0; _ga_MHSNPJKWC7=GS1.2.1701449827.3.1.1701450196.0.0.0")
    html = urllib.request.urlopen(aoc_request).read()
    decoded_string = html.decode("utf-8")
    return decoded_string

def decode_data(raw_data):
    print('decoding')
    number_list = []
    chunks = re.split(r'\n\n', raw_data)
    for chunk in chunks:
        numbers = re.findall(r'\d+', chunk)
        numbers = [eval(i) for i in numbers]
        number_list.append(numbers) 
    return number_list

def chunker(seq:list[int], size:int):
    chunks=[] 
    for pos in range(0, len(seq), size):
        chunks.append(seq[pos:pos + size])
    return chunks

def create_map(raw_numbers):
  value_map = {}
  vals = chunker(raw_numbers,3)
  
  for line in vals:
      range_len = line[2]
      dest_range_strt = line[0]
      d_range = range(dest_range_strt, dest_range_strt+range_len)
      source_range_strt = line[1]
      s_range = range(source_range_strt, source_range_strt+range_len)
      value_map = value_map|dict(zip(s_range, d_range))

  return value_map

def get_location_total(seeds): 
    location_value =[seed['location'] for seed in seeds]

    return min(location_value)

def main():
    #create seeds
    raw_lines= process_raw_input(5)
    raw_numbers = decode_data(test_string)
    
    seed_nums = raw_numbers[0]
    
    maps = []
    for i in range(1,len(raw_numbers)):
        print(f'processing map:{i}')
        maps.append(create_map(raw_numbers[i]))
    
    seeds = []
    value_names = ['soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']
    for i,seed in enumerate(seed_nums):
        print(f'{i} seed being processed')
        current_seed = {'seed':seed}
        for j, cat in enumerate(value_names):
            vals = list(current_seed.values())
            value = None
            if vals[j] in list(maps[j].values()):
                value = maps[j][vals[j]]
            else:
                value = vals[j]

            current_seed[cat] = value
        seeds.append(current_seed)
        print(seeds[i])
    print(get_location_total(seeds))
main()