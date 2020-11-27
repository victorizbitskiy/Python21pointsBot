import random
import time
import config

from telebot import types


class Process:

    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def yes(self, chat_id):
        card_user = random.choice(list(config.all_carts.keys()))
        card_pic = open(card_user, 'rb')
        self.bot.send_photo(chat_id, card_pic)
        points_card = config.all_carts.get(card_user)
        config.all_carts.pop(card_user)
        self.bot.send_message(chat_id, "Вы взяли карту {0}! ".format(int(points_card)))
        self.db.add_points(chat_id, points_card, 0)
        (points_user, points_bot) = self.db.get_item(chat_id)
        time.sleep(1)

        self.bot.send_message(chat_id, "У вас {0}! ".format(int(points_user)))

        if points_user == 21:
            self.bot.send_message(chat_id, 'Вы выиграли! У вас 21')
            self.db.delete_item(chat_id)

        if points_user > 21:
            self.bot.send_message(chat_id, 'Перебор. Вы проиграли. У вас больше 21\n')
            self.db.delete_item(chat_id)
        else:
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Еще", callback_data='Yes')
            item2 = types.InlineKeyboardButton("Себе", callback_data='No')
            markup.add(item1, item2)
            self.bot.send_message(chat_id, 'Еще?', reply_markup=markup)

    def no(self, chat_id):
        self.bot.send_message(chat_id, 'Мой ход')

        while True:
            (points_user, points_bot) = self.db.get_item(chat_id)
            if points_bot <= points_user:
                self.bot.send_message(chat_id, 'Беру карту...')
                card_bot = random.choice(list(config.all_carts.keys()))
                card_pic = open(card_bot, 'rb')
                points_card = config.all_carts.get(card_bot)
                config.all_carts.pop(card_bot)

                self.bot.send_photo(chat_id, card_pic)
                self.bot.send_message(chat_id, "Выпало {0}".format(int(points_card)), 'очков')

                self.db.add_points(chat_id, 0, points_card)
                (points_user, points_bot) = self.db.get_item(chat_id)
                self.bot.send_message(chat_id, "У меня {0} ".format(int(points_bot)))
                time.sleep(2)

            if points_bot > 21:
                self.bot.send_message(chat_id,
                                      "Я проиграл.\nУ меня {0}. У вас {1}".format(int(points_bot), int(points_user)))
                self.db.delete_item(chat_id)

            if points_user < points_bot <= 21:
                self.bot.send_message(chat_id,
                                      "Я победил!\nУ меня {0}. У вас {1}".format(int(points_bot), int(points_user)))
                self.bot.send_message(chat_id, 'Не растраивайтесь. Попробуйте ещё раз.')
                self.db.delete_item(chat_id)

            if points_bot == points_user and points_bot > 17:
                self.bot.send_message(chat_id, 'Ничья. Мы набрали равное количество очков.')
                self.db.delete_item(chat_id)
