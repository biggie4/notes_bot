import telebot
from bot_config import *
from keyboard import *
from database import *


bot = telebot.TeleBot(bot_apikey)



def show_main_keyboard(user_id):
    bot.send_message(user_id, text="Выберите действие", reply_markup=main_keyboard())


def show_all(user_id):
    bot.send_message(user_id, text=get_notes(user_id))
    show_main_keyboard(user_id)


def add_note(user_id):
    print("Функция add_note")
    msg = bot.send_message(user_id, "Введите название заметки (^ для разделения названия и описания)")
    bot.register_next_step_handler(msg, add_note_step)


def add_note_step(message):
    if not send_note(message.from_user.id, message.text):
        bot.send_message(message.from_user.id, "Технические работы. Попробуйте позже.")
    else:
        bot.send_message(message.from_user.id, "Заметка создана.")
        show_main_keyboard(message.from_user.id)




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "show_all":
        show_all(call.from_user.id)
    if call.data == "add_note":
        add_note(call.from_user.id)


@bot.message_handler(content_types=['text'])
def greetings(message):
    print(message.from_user.id)
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, сохраняй здесь свои заметки")
        show_main_keyboard(message.from_user.id)



bot.polling(none_stop=True, interval=0)