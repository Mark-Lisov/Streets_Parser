import json

import requests
from bs4 import BeautifulSoup

all_types = ['улица', 'переулок', 'проезд', 'микрорайон', 'площадь', 'проспект', 'дорога', 'линия', 'тупик', 'шоссе',
             'бульвар', 'квартал', 'аллея', 'набережная', 'посёлок', 'мост', 'спуск', 'тракт', 'массив', 'путепровод',
             'тоннель']


def search(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    func_names = []
    func_types = []
    func_coordinates = []

    # get name of current street
    get_names = soup.find('div', class_='table-wrapper').findAll('a', class_='bold-fw')
    get_types = soup.find('div', class_='table-wrapper').findAll('td', class_='sm-rp right-ta')
    types_counter = 0

    for name in get_names:
        func_names.append(name.text)

    # get type of current street and add additional parts to name
    for not_trimmed_type in get_types:
        types_counter += 1
        type_ = not_trimmed_type.text.strip()
        type_lst = type_.split(' ')
        if len(type_lst) > 2:
            try:
                int(type_[0])
                func_types.append(type_lst[1])
                func_names[types_counter - 1] = str(
                    type_lst[0] + ' ' + func_names[types_counter - 1] + ' ' + type_lst[2])
            except ValueError:
                func_types.append(type_lst[0])
        elif len(type_lst) == 2:
            try:
                int(type_[0])
                func_types.append(type_lst[1])
                func_names[types_counter - 1] = str(type_lst[0] + ' ' + func_names[types_counter - 1])
            except ValueError:
                func_types.append(type_lst[0])
                func_names[types_counter - 1] = str(func_names[types_counter - 1] + ' ' + type_lst[1])
        else:
            func_types.append(type_)

    # follow the link and get the coordinates
    urls = []
    urls_counter = 0
    for i in soup.findAll('a', class_='bold-fw'):
        urls.append('https://geodzen.com' + i.get('href'))

    for current_url in urls:
        urls_counter += 1
        current_request = requests.get(current_url)
        if str(current_request)[11:14] != '200':
            func_coordinates.append('Нет данных')
            continue
        else:
            current_soup = BeautifulSoup(current_request.text, 'lxml')
            coordinates_parts = current_soup.find('div', class_='street-description').findAll('b',
                                                                                              class_='positive-coord')
            if func_types[urls_counter - 1] not in all_types:
                text_from_link = current_soup.find('div', class_='container street').find('h1').text
                tfl_lst = text_from_link.split(' ')
                try:
                    int(text_from_link[0])
                    func_types[urls_counter - 1] = tfl_lst[2]
                except ValueError:
                    func_types[urls_counter - 1] = tfl_lst[1]

            c1 = None
            c2 = None
            counter = 0

            for coord in coordinates_parts:
                if counter % 2 == 0:
                    c1 = coord.text
                    counter += 1
                else:
                    c2 = coord.text
                    counter += 1

            func_coordinates.append(c1 + ";" + c2)
    return func_names, func_types, func_coordinates


def appropriation(a: list, b: list, c: list, r: list):
    a.extend(r[0])
    b.extend(r[1])
    c.extend(r[2])


def types_to_nums(types_list: list, dictionary: dict):
    new_types = types_list
    types_counter = 0
    for i in types_list:
        types_counter += 1
        new_types[types_counter - 1] = (dictionary[i])
    return new_types


def three_lists_to_class_objects(class_, names: list, types: list, coordinates: list):
    streets = []
    streets_counter = 0
    for ns in names:
        streets_counter += 1
        streets.append(class_(name=ns, type=types[streets_counter - 1], coordinates=coordinates[streets_counter - 1]))
    return streets


def serialization(streets: list, num: int):
    open("my_file.json", "w")
    all_streets_together = []
    for i in range(num):
        all_streets_together.append(streets[i].__dict__)

    with open("my_file.json", "a") as json_file:
        json.dump(all_streets_together, json_file, indent='\t', sort_keys=True)


def filter_out(*lists: list):
    list_of_lists = [*lists]
    for one_list in list_of_lists:
        try:
            while True:
                one_list.remove([])
        except ValueError:
            pass
