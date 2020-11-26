import telebot
import config
import os

from telebot import types
from dbhelp import DBHelp
from process import Process

# if local server
# bot = telebot.TeleBot(config.TOKEN_21)

# if heroku
# when deploying the app run this command:
# heroku config:set TOKEN_21=YOUR_TOKEN
token = os.environ['TOKEN_21']
bot = telebot.TeleBot(token)

db = DBHelp()
db.setup()
process = Process(bot, db)


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🃏 Начать игру")
    markup.add(btn1)

    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b> бот.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['h', 'help'])
def h(message):
    bot.send_message(message.chat.id,
                     "Количество колод: 1\nКоличество карт в колоде: 36\nКоличество игроков: 2\n"
                     "Старшинство карт: B(2), Д(3), K(4), 6(6), 7(7), 8(8), 9(9), 10(10), Т(11).\n"
                     "Цель игры: набрать первым 21 очко.")


@bot.message_handler(content_types=['text'])
def start_game(message):
    if message.chat.type == 'private':
        if message.text == '🃏 Начать игру':

            db.delete_item(message.chat.id)
            db.add_item(message.chat.id, 0, 0)

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Да", callback_data='Yes')
            item2 = types.InlineKeyboardButton("Нет", callback_data='No')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Хотите взять карту?', reply_markup=markup)

        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        try:
            if call.data == 'Yes':
                process.yes(call.message.chat.id)

            elif call.data == 'No':
                process.no(call.message.chat.id)

        except Exception as e:
            print(repr(e))


# RUN
bot.polling(none_stop=True)
