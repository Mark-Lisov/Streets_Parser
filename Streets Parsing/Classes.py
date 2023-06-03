from dataclasses import dataclass
from enum import Enum

dict_ = {'улица': 'STREET', 'переулок': 'LANE', 'проезд': 'DRIVEWAY', 'микрорайон': 'NEIGHBORHOOD', 'площадь': 'SQUARE',
         'проспект': 'AVENUE', 'дорога': 'ROAD', 'линия': 'LINE', 'тупик': 'DEAD_END', 'шоссе': 'HIGHWAY',
         'бульвар': 'BOULEVARD', 'квартал': 'QUARTER', 'аллея': 'ALLEY', 'набережная': 'EMBANKMENT',
         'посёлок': 'VILLAGE', 'мост': 'BRIDGE', 'спуск': 'DESCENT', 'тракт': 'TRACT', 'массив': 'ARRAY',
         'путепровод': 'VIADUCT', 'тоннель': 'TUNNEL'}

dict_2 = {'улица': 1, 'переулок': 2, 'проезд': 3, 'микрорайон': 4, 'площадь': 5,
          'проспект': 6, 'дорога': 7, 'линия': 8, 'тупик': 9, 'шоссе': 10,
          'бульвар': 11, 'квартал': 12, 'аллея': 13, 'набережная': 14,
          'посёлок': 15, 'мост': 16, 'спуск': 17, 'тракт': 18, 'массив': 19,
          'путепровод': 20, 'тоннель': 21}

dict_3 = {1: 'улица', 2: 'переулок', 3: 'проезд', 4: 'микрорайон', 5: 'площадь',
          6: 'проспект', 7: 'дорога', 8: 'линия', 9: 'тупик', 10: 'шоссе',
          11: 'бульвар', 12: 'квартал', 13: 'аллея', 14: 'набережная',
          15: 'посёлок', 16: 'мост', 17: 'спуск', 18: 'тракт', 19: 'массив',
          20: 'путепровод', 21: 'тоннель'}


class StreetsTypes(Enum):
    STREET = "улица"
    LANE = "переулок"
    DRIVEWAY = "проезд"
    NEIGHBORHOOD = "микрорайон"
    SQUARE = "площадь"
    AVENUE = "проспект"
    ROAD = "дорога"
    LINE = "линия"
    DEAD_END = "тупик"
    HIGHWAY = "шоссе"
    BOULEVARD = "бульвар"
    QUARTER = "квартал"
    ALLEY = "аллея"
    EMBANKMENT = "набережная"
    VILLAGE = "посёлок"
    BRIDGE = "мост"
    DESCENT = "спуск"
    TRACT = "тракт"
    ARRAY = "массив"
    VIADUCT = "путепровод"
    TUNNEL = "тоннель"


@dataclass
class Street:
    name: str
    type: int
    coordinates: str

