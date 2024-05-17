import re


API_TOKEN = "5672523634:AAEl2LI8W3Py2jp1mrnhZ66SZwTe5y7wcD8"


EVENT_TEMP = {
    "event_name": None, 
    "datetime": None,
    "district": None,
    "subject": None,
    "address": None, 
    "location_info": None, 
    "game_type": None, 
    "event_info": None, 
    "group_link" : None
}


DISTRICT_NAMES = [["Центральный (ЦФО)", "CFO"],
                ["Северо-Западный (СЗФО)", "NWFO"],
                ["Приволжский (ПФО)", "PFO"],
                ["Южный (ЮФО)", "YUFO"],
                ["Северо-Кавказский (СКФО)", "SKFO"],
                ["Уральский (УФО)", "UFO"],
                ["Сибирский (СФО)", "SFO"],
                ["Дальневосточный (ДВФО)", "DFO"]
                ]


SUBJECT_TOWNS = {
    "CFO" : [
        "Москва",
        "Московская область",
        "Тверская область",
        "Смоленская область",
        "Калужская область",
        "Брянская область",
        "Тульская область",
        "Орловская область",
        "Рязанская область",
        "Владимирская область",
        "Ивановская область",
        "Костромская область",
        "Ярославская область",
        "Курская область",
        "Белгородская область",
        "Липецкая область",
        "Воронежская область",
        "Тамбовская область" 
        ],
    "NWFO" : [
        "Санкт-Петербург",
        "Ленинградская область",
        "Новгородская область",
        "Псковская область",
        "Вологодская область",
        "Республика Карелия",
        "Мурманская область",
        "Архангельская область",
        "Ненецкий автономный округ (Архангелская обл.)",
        "Республика Коми",
        "Калининградская область"
        ],
    "PFO" : [
        "Нижегородская область",
        "Кировская область",
        "Республика Марий Эл",
        "Чувашская Республика",
        "Республика Мордовия",
        "Республика Татарстан",
        "Ульяновская область",
        "Пензенская область",
        "Саратовская область",
        "Самарская область",
        "Пермский край",
        "Удмуртская Республика",
        "Республика Татарстан",
        "Республика Башкортостан",
        "Оренбургская область"
        ],
    "YUFO" : [
        "Волгоградская область",
        "Астраханская область",
        "Республика Калмыкия",
        "Ростовская область",
        "Краснодарский край",
        "Республика Адыгея",
        "Республика Крым",
        "Севастополь",
        ],
    "SKFO" : [
        "Ставропольский край",
        "Карачаево-Черкесская Республика",
        "Кабардино-Балкарская Республика",
        "Республика Северная Осетия - Алания"
        "Республика Ингушетия"
        "Республика Чечня"
        "Республика Дагестан"
        ],
    "UFO" : [
        "Свердловская область",
        "Челябинская область",
        "Курганская область",
        "Тюменская область",
        "Ханты-Мансийский автономный округ - Югра (Тюменская обл.)",
        "Ямало-Ненецкий автономный округ (Тюменская обл.)"
        ],
    "SFO" : [
        "Омская область",
        "Томская область",
        "Новосибирская область",
        "Кемеровская область",
        "Алтайский край",
        "Республика Алтай",
        "Красноярский край",
        "Республика Хакасия",
        "Республика Тыва",
        "Иркутская область"
        ],
    "DFO" : [
        "Республика Бурятия",
        "Забайкальский край",
        "Республика Саха (Якутия)", 
        "Магаданская область",
        "Чукотский автономный округ",
        "Камчатский край",
        "Амурская область",
        "Еврейская автономная область",
        "Хабаровский край",
        "Приморский край",  
        "Сахалинская область"
    ]
}


def is_url(url):
    regex = re.compile(
        r"^(?:http|ftp)s?://", re.IGNORECASE)
    return bool(regex.match(url))


def is_district(name):
    for district in DISTRICT_NAMES:
        if name in district[0]:
            return True
    return False


def is_subject(name):
    for district in SUBJECT_TOWNS:
        for towns in SUBJECT_TOWNS[district]:
            if name in towns:
                return True
    return False


def get_district_code(district_name):
    for district in DISTRICT_NAMES:
        if district_name in district[0]:
            return district[1]
    return None