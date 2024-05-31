from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import src.config as config

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(KeyboardButton("Регистрация события"), KeyboardButton("Просмотр события"))


district_inline_keyboard = InlineKeyboardMarkup()
district_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

for district_name in config.DISTRICT_NAMES:
    district_keyboard.add(KeyboardButton(text=district_name[0]))
    district_inline_keyboard.add(InlineKeyboardButton(text=district_name[0], callback_data=district_name[1]))


cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keyboard.add(KeyboardButton("Отмена"))


def make_subject_keyboard(district_name):
    district_code = config.get_district_code(district_name)
    subject_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for subject_name in config.SUBJECT_TOWNS[district_code]:
        subject_keyboard.add(KeyboardButton(text=subject_name))
    return subject_keyboard


def get_district_inline_keyboard(district_code):
    district_name = config.get_district_name(district_code)
    district_button = InlineKeyboardMarkup()
    district_button.add(InlineKeyboardButton(text=district_name, callback_data=district_code))
    return district_button


def get_subject_keyboard(district_code):
    subject_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    towns = config.get_subject_towns(district_code)
    for towm in towns:
        subject_keyboard.add(KeyboardButton(text=towm))
        
    return subject_keyboard