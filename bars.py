import json
import codecs
from math import sin, cos, asin, sqrt, radians
import argparse


def load_data(file_path):
    with codecs.open(file_path, 'r', "utf_8_sig") as opened_file:
        raw_json_data = opened_file.read()
        parsed_json_data = json.loads(raw_json_data)
    return parsed_json_data


def get_bar_by_size(parsed_json_data, function):
    bar = function(parsed_json_data['features'],
                   key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    return bar


def get_bar_by_coordinates(parsed_json_data, longitude, latitude):
    closest_bar = min(parsed_json_data['features'],
              key=lambda bar: get_distance(bar['geometry']['coordinates'][0],
                                           bar['geometry']['coordinates'][1],
                                           longitude, latitude))
    return closest_bar


def get_distance(longitude1, latitude1, longitude2, latitude2):
    longitude1, latitude1, longitude2, latitude2 = map(radians, [longitude1, latitude1, longitude2, latitude2])
    longitudes_diff = longitude2 - longitude1
    latitudes_diff = latitude2 - latitude1
    a = sin(latitudes_diff / 2) ** 2 + cos(latitude1) * cos(latitude2) * sin(longitudes_diff / 2) ** 2
    c = 2 * asin(sqrt(a))
    earth_radius = 6371
    distance = earth_radius * c
    return distance


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('latitude')
    parser.add_argument('longitude')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    parsed_json_data = load_data(args.path)
    longitude = float(args.longitude)
    latitude = float(args.latitude)
    smallest_bar = get_bar_by_size(parsed_json_data, min)
    biggest_bar = get_bar_by_size(parsed_json_data, max)
    closest_bar = get_bar_by_coordinates(parsed_json_data, longitude, latitude)
    print('Самый маленький бар:')
    print('   Название:', smallest_bar['properties']['Attributes']['Name'])
    print('   Число мест:', smallest_bar['properties']['Attributes']['SeatsCount'])
    print('   Координаты:', smallest_bar['geometry']['coordinates'])
    print('Самый большой бар:')
    print('   Название:', biggest_bar['properties']['Attributes']['Name'])
    print('   Число мест:', biggest_bar['properties']['Attributes']['SeatsCount'])
    print('   Координаты:', biggest_bar['geometry']['coordinates'])
    print('Ближайший бар:')
    print('   Название:', closest_bar['properties']['Attributes']['Name'])
    print('   Число мест:', closest_bar['properties']['Attributes']['SeatsCount'])
    print('   Координаты:', closest_bar['geometry']['coordinates'])
    print('   Расстояние:', get_distance(closest_bar['geometry']['coordinates'][0],
                                                closest_bar['geometry']['coordinates'][1],
                                                longitude, latitude))

