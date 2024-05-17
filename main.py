import telebot
import os
import src.keyboards as kb
import src.db as db
from sys import platform


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
    elif len(message.text) <= 1:
        bot.send_message(message.chat.id, "Укажите корректное название мероприятия", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_datetime)
    else:
        kb.config.EVENT_TEMP["event_name"] = message.text
        bot.send_message(message.chat.id, "Укажите дату и время мероприятия", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_district)

        
def input_district(message):
    if message.text == "Отмена":
        cancel(message)
    elif len(message.text) <= 7:
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
    elif len(message.text) <= 1:
        bot.send_message(message.chat.id, "Укажите корректный адрес проведения мероприятия", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_location_info)
    else:
        kb.config.EVENT_TEMP["address"] = message.text
        bot.send_message(message.chat.id, "Укажите краткое описание локации", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_game_type)
        
    
def input_game_type(message):
    if message.text == "Отмена":
        cancel(message)
    elif len(message.text) <= 1:
        bot.send_message(message.chat.id, "Укажите корректное краткое описание локации", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_game_type)
    elif len(message.text) > 200:
        bot.send_message(message.chat.id, "Краткое описание не должно превышать 200 символов\nУкажите корректное описание локации", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_group_link)
    else:
        kb.config.EVENT_TEMP["location_info"] = message.text
        bot.send_message(message.chat.id, "Укажите тип игры", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_event_info)
        

def input_event_info(message):
    if message.text == "Отмена":
        cancel(message)
    elif len(message.text) <= 1:
        bot.send_message(message.chat.id, "Укажите тип игры", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_event_info)
    else:
        kb.config.EVENT_TEMP["game_type"] = message.text
        bot.send_message(message.chat.id, "Укажите краткую информацию о событии", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_group_link)
        

def input_group_link(message):
    if message.text == "Отмена":
        cancel(message)
    elif len(message.text) <= 1:
        bot.send_message(message.chat.id, "Укажите краткую информацию о событии", reply_markup = kb.cancel_keyboard)
        bot.register_next_step_handler(message, input_group_link)
    elif len(message.text) > 200:
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
    bot.send_message(message.chat.id, "Какой федеральный округ вас интересует?", reply_markup=kb.district_inline_keyboard)


@bot.message_handler(content_types=["text"])
def send_text(message):
    pass


@bot.callback_query_handler(func = lambda call : True)
def distrit_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.id,
                          text="Какой город/область вас интересует?")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                          message_id=call.message.id,
                          reply_markup=kb.make_subject_keyboard(call.message.text))
    bot.register_next_step_handler(call.message, chouse_subject)
    
    
def chouse_subject(message):
    pass
    

if __name__ == "__main__": 
    try:
        print(f"[LAUNCHING BOT] OK")
        bot.infinity_polling(none_stop=True, interval=0, timeout=20)
    except Exception as error:
        print(f"[LAUNCHING BOT] {error}")
