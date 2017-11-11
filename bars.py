import json
import codecs
from math import *
import argparse

def load_data(file_path):
    with codecs.open(file_path, 'r', "utf_8_sig") as opened_file:
        raw_json_data = opened_file.read()
        parsed_json_data = json.loads(raw_json_data)
    return parsed_json_data


def get_bars_parameters_list(parsed_json_data):
    bars_parameters_list = list()
    for bar in parsed_json_data["features"]:
        bars_parameters_list.append([bar["properties"]["Attributes"]["Name"],
                                     bar["properties"]["Attributes"]["SeatsCount"],
                                     bar["geometry"]["coordinates"]])
    return bars_parameters_list


def get_biggest_bar(bars_parameters_list):
    biggest_bar = max(bars_parameters_list,
                      key=lambda get_bar_parameter: get_bar_parameter[1])
    return biggest_bar


def get_smallest_bar(bars_parameters_list):
    return min(bars_parameters_list,
               key=lambda get_bar_parameter: get_bar_parameter[1])


def get_distance(longitude1, latitude1, longitude2, latitude2):
        longitude1, latitude1, longitude2, latitude2 = map(radians, [longitude1, latitude1, longitude2, latitude2])
        longitudes_diff = longitude2 - longitude1
        latitudes_diff = latitude2 - latitude1
        a = sin(latitudes_diff / 2) ** 2 + cos(latitude1) * cos(latitude2) * sin(longitudes_diff / 2) ** 2
        c = 2 * asin(sqrt(a))
        distance = 6371 * c #6371 - Радиус Земли
        return distance


def get_closest_bar(bars_parameters_list, longitude, latitude):
    with_distance_list = list()
    for bar in bars_parameters_list:
        distance = get_distance(bar[2][1], bar[2][0], longitude, latitude)
        with_distance_list.append((bar[0], bar[1], bar[2], distance))
    return min(with_distance_list,
               key=lambda get_bar_parameter: get_bar_parameter[3])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Путь к файлу .json')
    parser.add_argument('-la','--latitude', help='Ввести широту')
    parser.add_argument('-lo', '--longitude', help='Ввести долготу')
    args = parser.parse_args()
    parsed_json_data = load_data(args.path)
    bars_parameters_list = get_bars_parameters_list(parsed_json_data)
    smallest_bar = get_smallest_bar(bars_parameters_list)
    biggest_bar = get_biggest_bar(bars_parameters_list)
    print(smallest_bar)
    print(biggest_bar)
    print(get_closest_bar(bars_parameters_list, float(args.longitude), float(args.latitude)))
