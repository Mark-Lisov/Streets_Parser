import json
import requests

from bs4 import BeautifulSoup
from data import english_georgian_dict
from translate import Translator

all_types = ['улица', 'переулок', 'проезд', 'микрорайон', 'площадь', 'проспект', 'дорога', 'линия', 'тупик', 'шоссе',
             'бульвар', 'квартал', 'аллея', 'набережная', 'посёлок', 'мост', 'спуск', 'тракт', 'массив', 'путепровод',
             'тоннель']


def search(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    func_names = []
    func_types = []
    func_coordinates = []

    counter_for_test = 0

    # get name of current street
    get_names = soup.find('div', class_='table-wrapper').findAll('a', class_='bold-fw')
    get_types = soup.find('div', class_='table-wrapper').findAll('td', class_='sm-rp right-ta')
    types_counter = 0

    for name in get_names:
        counter_for_test += 1
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

    # get links to all the streets
    urls = []
    urls_counter = 0
    for i in soup.findAll('a', class_='bold-fw'):
        urls.append('https://geodzen.com' + i.get('href'))

    for current_url in urls:
        urls_counter += 1
        current_request = requests.get(current_url)
        if str(current_request)[11:14] != '200':
            # check if the request was successful
            func_coordinates.append('No data')
            continue
        else:
            # follow the link and get the coordinates
            current_soup = BeautifulSoup(current_request.text, 'lxml')
            coordinates_parts = current_soup.find('div', class_='street-description').findAll('b',
                                                                                              class_='positive-coord')
            if func_types[urls_counter - 1] not in all_types:
                # if the street type was written on the other side, it was not possible to take it
                # let's try again, now through the link
                type_from_link = current_soup.find('div', class_='container street').find('h1').text
                type_from_link_lst = type_from_link.split(' ')
                try:
                    int(type_from_link[0])
                    func_types[urls_counter - 1] = type_from_link_lst[2]
                except ValueError:
                    func_types[urls_counter - 1] = type_from_link_lst[1]

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

    print('Iteration #' + str(counter_for_test - 1))
    return func_names, func_types, func_coordinates


def appropriation(a: list, b: list, c: list, r: list):
    a.extend(r[0])
    b.extend(r[1])
    c.extend(r[2])


def types_to_nums(types_list: list, dictionary: dict) -> list:
    new_types = types_list
    types_counter = 0
    for i in types_list:
        types_counter += 1
        if i == '':
            new_types[types_counter - 1] = 'No data'
        new_types[types_counter - 1] = (dictionary[i])
    return new_types


def three_lists_to_class_objects(class_, names: list, types: list, coordinates: list) -> list:
    streets = []
    streets_counter = 0
    for ns in names:
        streets_counter += 1
        streets.append(class_(name=ns, type=types[streets_counter - 1], coordinates=coordinates[streets_counter - 1]))
    return streets


def serialization(streets: list, num: int):
    all_streets_together = []
    for i in range(num):
        all_streets_together.append(streets[i].__dict__)

    with open("my_file.json", "w", encoding='utf8') as json_file:
        json.dump(all_streets_together, json_file, ensure_ascii=False, indent='\t', sort_keys=True)


def translation_into_en_and_ka(streets_names: list) -> list[dict]:
    georgian_letters = [chr(code) for code in range(ord('ა'), ord('ჺ') + 1)]

    t_to_en = Translator(from_lang='ru', to_lang='en')
    t_to_ka = Translator(from_lang='ru', to_lang='ka')
    translations_counter = 0
    for i in streets_names:
        translations_counter += 1
        ru = i
        en = t_to_en.translate(ru)
        ka = t_to_ka.translate(ru)
        # some names in 'ka' translator still returns in english instead of georgian
        # let's fix it
        while True:
            list_ka = [lett for lett in ka]
            boolean = [False]
            for letter in list_ka:
                if any(boolean):
                    break
                if letter in georgian_letters:
                    boolean.append(True)
                else:
                    boolean.append(False)
            if any(boolean):
                break
            else:
                letters_counter = 0
                for en_lett in list_ka:
                    letters_counter += 1
                    try:
                        list_ka[letters_counter - 1] = english_georgian_dict[en_lett]
                    except KeyError:
                        continue
                ka = ''.join(list_ka)
                break

        streets_names[translations_counter - 1] = {'ru': ru, 'en': en, 'ka': ka}
    return streets_names
