import json
import requests
from bs4 import BeautifulSoup
from time import sleep
import random

from Classes import Street, dict_2
from funcs import search, appropriation, types_to_nums, three_lists_to_class_objects, serialization
from translator_by_Chat_GPT import my_translator

names = []
types = []
coordinates = []

for p in 'у':  # абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
    print(p)
    url = f'https://geodzen.com/ge/tbilisi/streets/{p}'
    try:
        result = search(url)
    except AttributeError:
        continue
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

# all types to numbers
types = types_to_nums(types, dict_2)

# all names in three languages
translations_counter = 0
for i in names:
    translations_counter += 1
    ru = i
    en = my_translator(text_for_translation=i, from_language='ru', to_language='en')
    ka = my_translator(text_for_translation=i, from_language='ru', to_language='ka')
    names[translations_counter - 1] = {'ru': ru, 'en': en, 'ka': ka}

print(names)

# create list of class' objects with name, type and coordinates of each street
streets = three_lists_to_class_objects(Street, names, types, coordinates)
print(streets)
# serialization
serialization(streets, len(types))
# now we have my_file.json


with open('my_file.json', 'r') as data_file:
    d_data = json.load(data_file)
    print(d_data)
