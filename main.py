import telebot
from telebot.types import ReplyKeyboardRemove
import os
import src.keyboards as kb
import src.db as db
from sys import platform
from random import randint
from src.config import is_datetime_valid, is_text_valid


try:
    if platform == "linux" or platform == "linux2":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")
except: pass


try:
    bot = telebot.TeleBot(kb.config.API_TOKEN)
    print(f"[INITIALIZATION BOT] OK")
except Exception as error:
    print(f"[INITIALIZATION BOT] {error}")


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id,
                    "Приветствую тебя в боте: \n"
                    "Расписание страйкбольных мероприятий!🎉 \n"
                    "Здесь ты можешь узнать о всех предстоящих страйкбольных событиях, планировать свои выходные и подготовиться к захватывающим битвам.\n"
                    "🏹 Давай начнем планировать твои приключения! 💪",
                    reply_markup=kb.main_keyboard)
    

@bot.message_handler(func=lambda message: message.text == "Регистрация события")
def input_event_name(message):
    bot.send_message(message.chat.id, "Укажите название мероприятия", reply_markup = kb.cancel_keyboard)
    bot.register_next_step_handler(message, input_datetime)


def input_datetime(message):
    if message.text == "Отмена":
        cancel(message)
    elif not is_text_valid(message.text):
        bot.send_message(message.chat.id, "Укажите корректное название мероприятия", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_datetime)
    else:
        kb.config.EVENT_TEMP["event_name"] = message.text
        bot.send_message(message.chat.id, "Укажите дату и время мероприятия\n\n"
                        "Необходимый формат даты и времени: \n"
                        "ДЕНЬ-МЕСЯЦ_ГОД ЧАСЫ:МИНУТЫ\n\n"
                        "Пример: 12-01-2024 12:00"
                        , reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_district)

        
def input_district(message):
    if message.text == "Отмена":
        cancel(message)
    if not is_datetime_valid(message.text):
            bot.send_message(message.chat.id, "Укажите корректную дату и время мероприятия", reply_markup = kb.cancel_keyboard)
            bot.register_next_step_handler(message, input_district)
    else:
        kb.config.EVENT_TEMP["datetime"] = message.text
        bot.send_message(message.chat.id, "Укажите Ваш федеральный округ", reply_markup = kb.district_keyboard)
        bot.register_next_step_handler(message, input_subject)


def input_subject(message):
    if message.text == "Отмена":
        cancel(message)
    elif not kb.config.is_district(message.text):
        bot.send_message(message.chat.id, "Укажите корректный федеральный округ", reply_markup = kb.district_keyboard)
        bot.register_next_step_handler(message, input_subject)
    else:
        kb.config.EVENT_TEMP["district"] = message.text
        bot.send_message(message.chat.id, "Укажите Ваш город/область", reply_markup = kb.make_subject_keyboard(message.text))
        bot.register_next_step_handler(message, input_address)
        

def input_address(message):
    if message.text == "Отмена":
        cancel(message)
    elif not kb.config.is_subject(message.text):
        bot.send_message(message.chat.id, "Укажите корректный город/область", reply_markup = kb.make_subject_keyboard(message.text))
        bot.register_next_step_handler(message, input_address)
    else:
        kb.config.EVENT_TEMP["subject"] = message.text
        bot.send_message(message.chat.id, "Укажите точный адрес проведения мероприятия", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_location_info)
        

def input_location_info(message):
    if message.text == "Отмена":
        cancel(message)
    elif not is_text_valid(message.text):
        bot.send_message(message.chat.id, "Укажите корректный адрес проведения мероприятия", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_location_info)
    else:
        kb.config.EVENT_TEMP["address"] = message.text
        bot.send_message(message.chat.id, "Укажите краткое описание локации", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_game_type)
        
    
def input_game_type(message):
    if message.text == "Отмена":
        cancel(message)
    elif not is_text_valid(message.text):
        bot.send_message(message.chat.id, "Укажите корректное краткое описание локации", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_game_type)
        if len(message.text) > 200:
            bot.send_message(message.chat.id, "Краткое описание не должно превышать 200 символов\nУкажите корректное описание локации", reply_markup = kb.cancel_keyboard)
            bot.register_next_step_handler(message, input_group_link)
    else:
        kb.config.EVENT_TEMP["location_info"] = message.text
        bot.send_message(message.chat.id, "Укажите тип игры", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_event_info)
        

def input_event_info(message):
    if message.text == "Отмена":
        cancel(message)
    elif not is_text_valid(message.text):
        bot.send_message(message.chat.id, "Укажите корректный тип игры", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_event_info)
    else:
        kb.config.EVENT_TEMP["game_type"] = message.text
        bot.send_message(message.chat.id, "Укажите краткую информацию о событии", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_group_link)
        

def input_group_link(message):
    if message.text == "Отмена":
        cancel(message)
    elif not is_text_valid(message.text):
        bot.send_message(message.chat.id, "Укажите корректную информацию о событии", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_group_link)
        if len(message.text) > 200:
            bot.send_message(message.chat.id, "Краткая информация не должна превышать 200 символов\nУкажите корректную информацию о событии", reply_markup = kb.cancel_keyboard)
            bot.register_next_step_handler(message, input_group_link)
    else:
        kb.config.EVENT_TEMP["event_info"] = message.text
        bot.send_message(message.chat.id, "Укажите ссылку на группу мероприятия", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, save_event_data)
        

def save_event_data(message):
    if message.text == "Отмена":
        cancel(message)
    elif not kb.config.is_url(message.text):
        bot.send_message(message.chat.id, "Укажите корректную ссылку на группу мероприятия", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, save_event_data)
    else:
        kb.config.EVENT_TEMP["group_link"] = message.text
        db.add_new_event(kb.config.EVENT_TEMP["event_name"],
                        kb.config.EVENT_TEMP["datetime"],
                        kb.config.EVENT_TEMP["district"],
                        kb.config.EVENT_TEMP["subject"],
                        kb.config.EVENT_TEMP["address"],
                        kb.config.EVENT_TEMP["location_info"],
                        kb.config.EVENT_TEMP["game_type"],
                        kb.config.EVENT_TEMP["event_info"],
                        kb.config.EVENT_TEMP["group_link"])
        kb.config.EVENT_TEMP.clear()
        bot.send_message(message.chat.id, "Ваше мероприятие зарегистрировано", reply_markup = kb.main_keyboard)
        

def cancel(message):
    bot.send_message(message.chat.id,
                    "Регистрация мероприятия отменена",
                    reply_markup=kb.main_keyboard)
        

@bot.message_handler(func=lambda message: message.text == "Просмотр события")
def show_event(message):
    db.delete_old_events()
    bot.send_message(message.chat.id, "Какой федеральный округ вас интересует?", reply_markup=kb.district_inline_keyboard)


@bot.callback_query_handler(func = lambda call : True)
def distrit_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.id,
                          text="Какой город/область вас интересует?")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                message_id=call.message.id,
                                inline_message_id=call.message.id, 
                                reply_markup=kb.get_district_inline_keyboard(call.data))

    bot.send_message(chat_id=call.message.chat.id, 
                                text="Выберите город/область из списка",
                                reply_markup=kb.get_subject_keyboard(call.data))

    bot.register_next_step_handler(call.message, chouse_subject)
    
    
def chouse_subject(message):
    events = db.get_names_by_subject(message.text)
    if len(events)>0:
        random_event_num = randint(0, len(events)-1)
        current_event_name = str((events[random_event_num])[0])
        current_event_datetime = db.get_data(current_event_name, "datetime")
        current_event_address = db.get_data(current_event_name, "address")
        current_location_info = db.get_data(current_event_name, "location_info")
        current_game_type = db.get_data(current_event_name, "game_type")
        current_event_info = db.get_data(current_event_name, "event_info")
        current_group_link = db.get_data(current_event_name, "group_link")
        bot.send_message(message.chat.id,
                        f"⭐️ Название: {current_event_name}\n"
                        f"📅 Дата: {current_event_datetime}\n"
                        f"🗺️ Адрес: {current_event_address}\n"
                        f"💬 Описание локации: {current_location_info}\n"
                        f"🏹 Тип игры: {current_game_type}\n"
                        f"🔥 О мероприятии: {current_event_info}\n"
                        f"🔗 Ссылка: {current_group_link}",
                        reply_markup=kb.main_keyboard)
        
    else: bot.send_message(message.chat.id, 
                        f"Мы не нашли ни одного мероприятия в выбранной области 😢",
                        reply_markup=kb.main_keyboard)
    

if __name__ == "__main__": 
    try:
        print(f"[LAUNCHING BOT] OK")
        bot.infinity_polling(none_stop=True, interval=0, timeout=20)
    except Exception as error:
        print(f"[LAUNCHING BOT] {error}")
