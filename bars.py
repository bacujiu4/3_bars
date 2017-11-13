import json
import codecs
from math import sin, cos, asin, sqrt, radians
import argparse

def load_data(file_path):
    with codecs.open(file_path, 'r', "utf_8_sig") as opened_file:
        raw_json_data = opened_file.read()
        parsed_json_data = json.loads(raw_json_data)
    return parsed_json_data


def get_biggest_bar_attributes(parsed_json_data):
    biggest_bar_attributes = max(parsed_json_data['features'],
                       key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    return biggest_bar_attributes


def get_smallest_bar_attributes(parsed_json_data):
    smallest_bar_attributes = min(parsed_json_data['features'],
                       key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    return smallest_bar_attributes


def get_distance(longitude1, latitude1, longitude2, latitude2):
        longitude1, latitude1, longitude2, latitude2 = map(radians, [longitude1, latitude1, longitude2, latitude2])
        longitudes_diff = longitude2 - longitude1
        latitudes_diff = latitude2 - latitude1
        a = sin(latitudes_diff / 2) ** 2 + cos(latitude1) * cos(latitude2) * sin(longitudes_diff / 2) ** 2
        c = 2 * asin(sqrt(a))
        distance = 6371 * c #6371 - Радиус Земли
        return distance


def get_closest_bar_attributes(parsed_json_data, longitude, latitude):
    min_distance = get_distance(parsed_json_data['features'][0]['geometry']['coordinates'][0],
                               parsed_json_data['features'][0]['geometry']['coordinates'][1],
                               longitude, latitude)
    min_distance_bar = list()
    for bar in parsed_json_data['features']:
        distance = get_distance(bar['geometry']['coordinates'][0],
                                bar['geometry']['coordinates'][1],
                                longitude, latitude)
        if distance < min_distance:
            min_distance = distance
            min_distance_bar = bar
    return min_distance_bar, min_distance


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
    smallest_bar_attributes = get_smallest_bar_attributes(parsed_json_data)
    biggest_bar_attributes = get_biggest_bar_attributes(parsed_json_data)
    closest_bar = get_closest_bar_attributes(parsed_json_data, longitude, latitude)
    print('Самый маленький бар:',
          '\n Название:', smallest_bar_attributes['properties']['Attributes']['Name'],
          '\n Число мест:', smallest_bar_attributes['properties']['Attributes']['SeatsCount'],
          '\n Координаты:', smallest_bar_attributes['geometry']['coordinates'])
    print('Самый большой бар:',
          '\n Название:', biggest_bar_attributes['properties']['Attributes']['Name'],
          '\n Число мест:', biggest_bar_attributes['properties']['Attributes']['SeatsCount'],
          '\n Координаты:', biggest_bar_attributes['geometry']['coordinates'])
    print('Ближайший бар:',
          '\n Название:', closest_bar[0]['properties']['Attributes']['Name'],
          '\n Число мест:', closest_bar[0]['properties']['Attributes']['SeatsCount'],
          '\n Координаты:', closest_bar[0]['geometry']['coordinates'],
          '\n Расстояние:', closest_bar[1])
