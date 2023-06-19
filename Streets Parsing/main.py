import json
import requests
import random

from bs4 import BeautifulSoup
from time import sleep

from data import Street, type_to_number_dict
from funcs import search, appropriation, types_to_nums, three_lists_to_class_objects, serialization, \
    translation_into_en_and_ka

names = []
types = []
coordinates = []

# getting the streets of each current letter
for p in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
    print(p)
    url = f'https://geodzen.com/ge/tbilisi/streets/{p}'
    try:
        # getting names, types and coordinates of streets that are on first page
        result = search(url)
    # but some letters don't have any streets at all so just ignore them
    except AttributeError:
        continue
    # all names, types and coordinates from 'result' appropriate to relevant variables
    appropriation(names, types, coordinates, result)

    sleep(random.randint(1, 3))

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    try:
        pages_number = len(soup.find('div', class_='parts').findAll('a'))
    except AttributeError:
        continue

    for n in range(1, pages_number - 2):
        url = f'https://geodzen.com/ge/tbilisi/streets/{p}?part={n}'
        result = search(url)
        appropriation(names, types, coordinates, result)

print('Parsing finished')
# all types to numbers
types = types_to_nums(types, type_to_number_dict)

print('types_to_nums() finished')
# all names translate in three languages
names = translation_into_en_and_ka(names)

print('Translation finished')
# create list of class' objects with name, type and coordinates of each street
streets = three_lists_to_class_objects(Street, names, types, coordinates)

print('three_lists_to_class_objects() finished')
# serialization
serialization(streets, len(types))
# now we have my_file.json
print('Serialization finished')

with open('my_file.json', 'r', encoding='utf8') as data_file:
    d_data = json.load(data_file)
    print(d_data)
