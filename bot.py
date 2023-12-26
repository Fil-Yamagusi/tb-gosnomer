#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
    2023-12-19 Filipp Yamagusi
    Телеграм-бот Лото автомобильных номеров!
    Fil FC Лото госномеров
    fil_fc_gosnomer_bot
    https://t.me/fil_fc_gosnomer_bot
"""
# стандартные модули
from time import time_ns, localtime, strftime
from sys import getsizeof
import json
# наш любимый бот Telegram
from telebot import TeleBot
from telebot import types
from telebot.types import Message
# Токен и прочие настройки бота
import config
# Таблица кодов, ради которых все мы здесь сегодня собрались
from numeri import code_rf, code_black, code_diplomat, code_ino

# данные всех пользователей в сложном формате, с сохранением в JSON-файле
JSON_FILE_USERS = "users.json"


# Сохраняем информацию о коллекциях. Смысл этого урока
def save_users() -> None:
    """ При открытии указывается кодировка utf8 """
    with open(JSON_FILE_USERS, 'w', encoding='utf8') as file_for_json:
        # Записываем данные в файл, не разрешив нестандартные символы
        json.dump(Users, file_for_json, ensure_ascii=True)


# Читаем сохранённую информацию о коллекциях. Смысл этого урока
def load_users() -> dict:
    """ При открытии указывается кодировка utf8 """
    with open(JSON_FILE_USERS, 'r', encoding='utf8') as file_for_json:
        # Записываем данные в файл, не разрешив нестандартные символы
        return json.load(file_for_json)


Users = load_users()

# основной класс для бота
bot = TeleBot(config.TOKEN)

# Пустое меню, может пригодиться на промежуточных вопросах
markup_empty = types.ReplyKeyboardMarkup(
)

# Главное меню
menu_main = {
    'add': '🚙 Новый номер!',
    'stat': '📊 Статистика',
    'help': '❓ Справка',
}
markup_main = types.ReplyKeyboardMarkup(
    row_width=3,
    resize_keyboard=True
)
markup_main.add(* menu_main.values())


# Выбор типа интересного номера
menu_add = {
    'rf': 'Регионы\n'
          '🇷🇺 РФ',
    'amr': 'Мигалки\n'
           '🚔 АМР97',
    'black': 'Военные\n'
             '⬛️ (чёрные)',
    'diplomat': 'Дипломаты\n'
                '🟥 (красные)',
    'int_org': 'Организации\n'
               '🟥 (красные)',
}
markup_add = types.ReplyKeyboardMarkup(
    row_width=3,
    resize_keyboard=True
)
markup_add.add(* menu_add.values())


# Уточнение типа дипломатического номера
menu_diplomat = {
    'diplomat_cd1': 'CD 1',
    'diplomat_cd2': 'CD 2',
    'diplomat_d': 'D',
    'diplomat_t': 'T',
}
markup_diplomat = types.ReplyKeyboardMarkup(
    row_width=4,
    resize_keyboard=True
)
markup_diplomat.add(* menu_diplomat.values())


# Уточнение типа номера международной организации
menu_int_org = {
    'int_org_cd1': 'CD 1 (босс)',
    'int_org_cd2': 'CD 2 (зам)',
    'int_org_d': 'D (сотрудник)',
    'int_org_t': 'T (техперсонал)',
}
markup_int_org = types.ReplyKeyboardMarkup(
    row_width=4,
    resize_keyboard=True
)
markup_int_org.add(* menu_int_org.values())


# Ответы ДА и НЕТ кнопками
menu_yes_no = {
    'yes': 'Да, добавить!',
    'no': 'Нет, не надо',
}
markup_yes_no = types.ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True
)
markup_yes_no.add(* menu_yes_no.values())


# Показываем отладочную информацию о всх коллекциях
def show_users(show_size: bool = False, show_content: bool = False) -> None:
    """ Немного отладочной информации """
    if show_size:
        print(getsizeof(Users) // 1000000, "Mib",
              getsizeof(Users) // 1000, "Kib")
    if show_content:
        print(Users)


# Создаём пользователя в общем словаре, если не было
def check_user(user_id: str) -> None:
    """ Функция вызывается из разных мест """
    # user_id = str(user_id)
    if user_id not in Users:
        Users[user_id] = {}
        Users[user_id]["collection"] = {}
        show_users(show_content=False)


@bot.message_handler(commands=["start"])
def handle_start(message: Message):
    """ Главный экран """
    user_id = str(message.from_user.id)
    check_user(user_id)
    bot.send_message(
        message.chat.id,
        f"<b>Привет, {message.chat.first_name}!</b>\n\n"
        f"На дороге встречаются интересные номера.\n"
        f"Здесь ты можешь как в лото: заполнять карточки с регионами, "
        f"кодами дипломатических номеров или мигалок АМР97.\n\n"
        f"Интересно, как быстро ты сможешь заполнить все?\n\n"
        f"<b>Увидел интересный номер</b>? Давай запишем! /add\n"
        f"Или посмотрим твою и общую статистику /stat\n"
        f"Подробности в справке /help",

        parse_mode="HTML",
        reply_markup=markup_main
    )


def perc_to_text(perc: float) -> str:
    """ По набранному проценту (десятку процентов) выдать похвалу """
    match int(perc):
        case 0:
            return "Твоя коллекция ещё мала, но и Рим не сразу строился."
        case 1:
            return "В тавернах пошли слухи о росте твоей коллекции."
        case 2:
            return "Да, внимательность - твоё второе имя!"
        case 3:
            return "Надеюсь, ты не слишком отвлекаешься от дороги?"
        case 4:
            return "Ещё чуть-чуть и половина позади!"
        case 5:
            return "Ура! Экватор пройден, теперь только вперёд!"
        case 6:
            return "Удача на твоей стороне, и коллекция неуклонно растёт."
        case 7:
            return "Скажу по секрету, у тебя не осталось конкурентов."
        case 8:
            return "Топовые блогеры мечтают взять интервью у тебя!"
        case 9:
            return "Это невообразимо! Ты очень настойчивый коллекционер!"


@bot.message_handler(
    content_types=["text"],
    func=lambda message: message.text == menu_main["stat"])
@bot.message_handler(commands=["stat"])
def handle_stat(message: Message):
    """ Самая простая статистика. Пора делать следующих ботов """
    user_id = str(message.from_user.id)
    check_user(user_id)
    rf_you, rf_all = 0, 0
    amr_you, amr_all = 0, 0
    black_you, black_all = 0, 0

    diplomat_cd1_you = 0
    diplomat_cd2_you = 0
    diplomat_d_you = 0
    diplomat_t_you = 0

    for uid in Users:
        you = uid == user_id
        user = Users[uid]
        # print(user)
        # print(user["collection"].keys())

        if "rf" in user["collection"]:
            rf_all += len(user["collection"]["rf"])
            if you:
                rf_you = len(user["collection"]["rf"])

        if "amr" in user["collection"]:
            amr_all += len(user["collection"]["amr"])
            if you:
                amr_you = len(user["collection"]["amr"])

        if "black" in user["collection"]:
            black_all += len(user["collection"]["black"])
            if you:
                black_you = len(user["collection"]["black"])

        if "diplomat_cd1" in user["collection"] and you:
            diplomat_cd1_you = len(user["collection"]["diplomat_cd1"])
        if "diplomat_cd2" in user["collection"] and you:
            diplomat_cd2_you = len(user["collection"]["diplomat_cd2"])
        if "diplomat_d" in user["collection"] and you:
            diplomat_d_you = len(user["collection"]["diplomat_d"])
        if "diplomat_t" in user["collection"] and you:
            diplomat_t_you = len(user["collection"]["diplomat_t"])

    res_rf = 100 * rf_you / len(code_rf)
    res_amr = 100 * amr_you / 999
    res_black = 100 * black_you / len(code_black)

    bot.send_message(
        message.chat.id,
        f"<b>Немного статистики:</b>\n\n"
        f"Всего пользователей: <b>{len(Users)}</b>\n\n"
        f"🇷🇺 Записано регионов РФ:\n"
        f"<b>{rf_all}</b> - у всех пользователей (с повторами)\n"
        f"<b>{rf_you}</b> из <b>{len(code_rf)}</b> - у тебя. "
        f"Это {res_rf:.1f}%!\n<i>{perc_to_text(res_rf / 10)}</i>\n\n"
        f"🚔 Надоедливых мигалок АМР97:\n"
        f"<b>{amr_all}</b> - у всех пользователей (с повторами)\n"
        f"<b>{amr_you}</b> из <b>999</b> - у тебя. "
        f"Это {res_amr:2.1f}%!\n<i>{perc_to_text(res_amr / 10)}</i>\n\n"
        f"⬛️ Секретных военных:\n"
        f"<b>{black_all}</b> - у всех пользователей (с повторами)\n"
        f"<b>{black_you}</b> из <b>{len(code_black)}</b> - у тебя. "
        f"Это {res_black:.1f}%!\n<i>{perc_to_text(res_black / 10)}</i>\n\n"
        f"🟥 Сколько посольских машин у тебя:\n"
        f"- послов: <b>{diplomat_cd1_you}</b>\n"
        f"- послиц: <b>{diplomat_cd2_you}</b>\n"
        f"- дипломатов: <b>{diplomat_d_you}</b>\n"
        f"- техников: <b>{diplomat_t_you}</b>\n\n"
        f"(в моей базе <b>{len(code_diplomat)}</b> разных стран)\n\n"
        f"Так держать, следи за дорогой!\n\n"
        f"Остальная статистика - в том же духе. Можно выводить картинкой, "
        f"но пора делать следующее домашнее задание.\n",

        parse_mode="HTML",
        reply_markup=markup_main
    )


@bot.message_handler(
    content_types=["text"],
    func=lambda message: message.text == menu_main["help"])
@bot.message_handler(commands=["help"])
def handle_help(message: Message):
    """ Чуть более подробное описание """
    user_id = str(message.from_user.id)
    check_user(user_id)
    bot.send_message(
        message.chat.id,
        f"<b>Привет, {message.chat.first_name}!</b>\n\n"
        f"Этот бот поможет тебе сохранить некоторые красивые номера машин, "
        f"которые встречаются на дороге.\n"
        f"Просто ради интереса. Например, возможно ли встретить посольские "
        f"машины всех стран (красные номера)? Или все виды военных чёрных "
        f"номеров? Или все 999 надоедливых мигалок АМР97?\n\n"
        f"<b>Для добавления нового номера</b> используй кнопки меню "
        f"или команду /add\n"
        f"далее следуй подсказкам.\n\n"
        f"Нет никаких соревнований с другими пользователями или проверки 'на "
        f"честность'. Можешь сразу указать десятки уже встреченных номеров.\n\n"
        f"<i>Кстати, можно использовать бота чтобы просто узнать "
        f"название региона РФ по его номеру. Или номер страны "
        f"по посольскому коду.</i>\n\n"
        f"<b>Свою и общую статистику</b> смотри тут: /stat\n\n"
        f"<b>Прочитать справку</b> ещё раз: /help",

        parse_mode="HTML",
        reply_markup=markup_main
    )


@bot.message_handler(
    content_types=["text"],
    func=lambda message: message.text == menu_main["add"])
@bot.message_handler(commands=["add"])
def handle_add(message: Message):
    """ Раздел добавления разных типов номеров """
    user_id = str(message.from_user.id)
    check_user(user_id)
    bot.send_message(
        message.chat.id,
        "Выбери тип номера, а потом укажи подробности",

        parse_mode="HTML",
        reply_markup=markup_add
    )


# Пять основных типов номеров.
@bot.message_handler(
    content_types=["text"],
    func=lambda message: message.text in menu_add.values())
@bot.message_handler(
    content_types=["text"],
    func=lambda message: message.text in menu_diplomat.values())
@bot.message_handler(
    content_types=["text"],
    func=lambda message: message.text in menu_int_org.values())
def handle_menu(message: Message):
    """ У интересных номеров разный формат для ввода """
    user_id = str(message.from_user.id)
    check_user(user_id)
    action = [k for k, v in menu_add.items() if v == message.text]
    if not action:
        action = [k for k, v in menu_diplomat.items() if v == message.text]
    if not action:
        action = [k for k, v in menu_int_org.items() if v == message.text]
    action = action[0]
    Users[user_id]["action"] = action
    show_users()

    # Все типы немного отличаются друг от друга. Поясняем пользователю
    action_reply_markup = markup_empty
    msg = "act"
    match action:
        case "rf":
            msg = "Укажи <b>код региона РФ</b>. Например, 01, 769, 977:"
        case "amr":
            msg = "Укажи *** из номера <b>[A *** MP 97 RUS]</b>:"
        case "black":
            msg = "Укажи цифры справа (где у обычных машин регион):"
        case "diplomat":
            msg, action_reply_markup = \
                (("У <b>дипломатов</b> число слева <b>не более 200</b>.\n"
                  "Какие именно <b>буквы</b> в номере?"),
                 markup_diplomat)
        case "diplomat_cd1":
            msg = ("Вау! Это ж посол!\n"
                   "Укажи три цифры перед <b>CD 1</b>:")
        case "diplomat_cd2":
            msg = ("Это же послица. Или послиха. Или посолка :)\n"
                   "Укажи три цифры перед <b>CD 2</b>:")
        case "diplomat_d":
            msg = ("Транспорт простого сотрудника посольства\n"
                   "Укажи три цифры перед буквой <b>D</b>\n"
                   "(должно быть не более 200)")
        case "diplomat_t":
            msg = ("Это транспорт техперсонала посольства\n"
                   "Укажи три цифры перед буквой <b>T</b>\n"
                   "(должно быть не более 200)")
        case "int_org":
            msg, action_reply_markup = \
                (("У <b>организаций</b> число слева <b>не менее 499</b>.\n"
                  "Какие именно <b>буквы</b> в номере?"),
                 markup_int_org)
        case "int_org_cd1":
            msg = ("Руководитель организации\n"
                   "Укажи три цифры перед буквами <b>CD 1</b>\n"
                   "(должно быть не менее 499)")
        case "int_org_cd2":
            msg = ("Заместитель руководителя\n"
                   "Укажи три цифры перед буквами <b>CD 2</b>\n"
                   "(должно быть не менее 499)")
        case "int_org_d":
            msg = ("Это транспорт сотрудника организации\n"
                   "Укажи три цифры перед буквой <b>D</b>\n"
                   "(должно быть не менее 499)")
        case "int_org_t":
            msg = ("Это транспорт техперсонала\n"
                   "Укажи три цифры перед буквой <b>T</b>\n"
                   "(должно быть не менее 499)")

    bot.send_message(
        message.chat.id,
        f"{msg}",

        parse_mode="HTML",
        reply_markup=action_reply_markup
    )


# И вот нам прислали число. Разбираем, для какого оно типа (action)
@bot.message_handler(
    content_types=["text"],
    func=lambda message: str(message.text).isdecimal())
def handle_decimal(message: Message):
    """ Если пришло число и выбран тип номера (action) """
    user_id = str(message.from_user.id)
    check_user(user_id)
    if "action" not in Users[user_id] or Users[user_id]["action"] == "":
        bot.send_message(
            message.chat.id,
            "Хочешь добавить интересный номер? Выбери тип: /add",

            reply_markup=markup_main,
        )
        return

    action = Users[user_id]["action"]
    markup_decimal = markup_empty

    num = int(message.text)
    if not 0 < num < 1000:
        bot.send_message(
            message.chat.id,
            "Невозможное значение, так не бывает! Попробуй ещё раз",
        )
        return

    # Регион РФ с лидирующим нулём для однозначных
    if action == "rf":
        norm_num = str(num).zfill(2)
        if norm_num not in code_rf:
            msg = (f"<b>{norm_num}</b>? В моей базе нет такого кода региона.\n"
                   "Техподдержке уже сообщил.")
        else:
            Users[user_id]["norm_num"] = norm_num
            msg = (f"🇷🇺 <b>{norm_num}</b>: {code_rf[norm_num]}\n"
                   f"Вау! Добавить в твою коллекцию?")
            markup_decimal = markup_yes_no
    # Тут полный набор: от 001 до 999
    elif action == "amr":
        norm_num = str(num).zfill(3)
        Users[user_id]["norm_num"] = norm_num
        msg = (f"Вау! <b>[A {norm_num} MP 97 RUS]</b>\n"
               f"Добавить в твою коллекцию?")
        markup_decimal = markup_yes_no
    # Тут очень рваный набор. Двузначные с одним однозначным
    elif action == "black":
        norm_num = str(num).zfill(2)
        if norm_num not in code_black:
            msg = (f"<b>{norm_num}</b>? В моей базе нет такого кода.\n"
                   "Техподдержке уже сообщил.")
        else:
            Users[user_id]["norm_num"] = norm_num
            msg = (f"Вау, код <b>{norm_num}</b>! Добавить в твою коллекцию?\n"
                   f"{code_black[norm_num]}")
            markup_decimal = markup_yes_no
    # Если вводят номер, не уточнив детали дипломата
    elif action in ["diplomat"]:
        msg = ("У <b>дипломатов</b> бывает четыре типа номеров.\n"
               "Выбери кнопкой <b>буквы</b> после первого числа")
        markup_decimal = markup_diplomat
    # Коды стран от 001 до 170. Все четыре типа по одному сценарию
    elif action in ["diplomat_cd1", "diplomat_cd2", "diplomat_d", "diplomat_t"]:
        norm_num = str(num).zfill(3)
        if num > 200:
            msg = f"<b>{norm_num}</b>? Код должен быть не больше 200!\n"
        elif norm_num not in code_diplomat:
            msg = (f"<b>{norm_num}</b>? В моей базе нет этого кода.\n"
                   f"Техподдержке уже сообщил.")
        else:
            Users[user_id]["norm_num"] = norm_num
            msg = (f"<b>{norm_num} {menu_diplomat[action]}</b>: "
                   f"{code_diplomat[norm_num]}\n"
                   f"Вау! Добавить в твою коллекцию?")
            markup_decimal = markup_yes_no
    #
    # Если вводят номер, не уточнив детали организации
    elif action in ["int_org"]:
        msg = ("У <b>организаций</b> несколько типов номеров.\n"
               "Выбери кнопкой <b>буквы</b> после первого числа")
        markup_decimal = markup_int_org
    #
    # Коды стран от 499 до 900. Оба типа по одному сценарию
    elif action in ["int_org_cd1", "int_org_cd2", "int_org_d", "int_org_t"]:
        norm_num = str(num)
        if num < 499:
            msg = f"<b>{norm_num}</b>? Код должен быть не меньше 499!\n"
        elif norm_num not in code_ino:
            msg = (f"<b>{norm_num}</b>? В моей базе нет этого кода.\n"
                   f"Техподдержке уже сообщил.")
        else:
            Users[user_id]["norm_num"] = norm_num
            msg = (f"<b>{norm_num} {menu_int_org[action]}</b>: "
                   f"{code_ino[norm_num]}\n"
                   f"Вау! Добавить в твою коллекцию?")
            markup_decimal = markup_yes_no

    bot.send_message(
        message.chat.id,
        f"{msg}",

        parse_mode="HTML",
        reply_markup=markup_decimal
    )

    show_users()


# Тип номера выбрали, число в правильный формат привели. Пора сохранять
@bot.message_handler(
    content_types=["text"],
    func=lambda message: message.text == menu_yes_no["yes"])
def handle_yes_to_save(message: Message):
    """ Если пришло число и выбран тип номера (action) """
    user_id = str(message.from_user.id)
    check_user(user_id)
    if "action" not in Users[user_id]:
        bot.send_message(
            message.chat.id,
            "Хочешь добавить интересный номер? Выбери тип: /add",

            reply_markup=markup_main,
        )
        return

    if "norm_num" not in Users[user_id]:
        bot.send_message(
            message.chat.id,
            "Не указан номер. Попробуйте добавить ещё раз: /add",
        )
        return

    action = Users[user_id]["action"]
    norm_num = Users[user_id]["norm_num"]

    # Создаём пользователю коллекцию, если не было
    if "collection" not in Users[user_id]:
        Users[user_id]["collection"] = {}
    if action not in Users[user_id]["collection"]:
        Users[user_id]["collection"][action] = {}
    show_users()

    # Если не было этого номера - добавляем
    if norm_num not in Users[user_id]["collection"][action]:
        Users[user_id]["collection"][action][norm_num] = {}
        dt = time_ns() // (10 ** 9)
        Users[user_id]["collection"][action][norm_num]["first"] = dt
        Users[user_id]["collection"][action][norm_num]["times"] = 1
        # Users[user_id]["collection"][action][norm_num]["last"] = dt
        msg = "Этот номер добавлен впервые! 🌟\n"
    # Если был этот номер - обновляем
    else:
        first = Users[user_id]["collection"][action][norm_num]["first"]
        first = strftime("%Y-%m-%d %H:%M", localtime(first))

        times = Users[user_id]["collection"][action][norm_num]["times"]
        Users[user_id]["collection"][action][norm_num]["times"] += 1

        msg = "Этот номер уже был добавлен.\n"
        msg += f"Впервые: {first}\n"
        if times > 1:
            last = Users[user_id]["collection"][action][norm_num]["last"]
            last = strftime("%Y-%m-%d %H:%M", localtime(last))
            msg += f"Сколько раз: {times}\n"
            msg += f"В последний раз: {last}\n"

        dt = time_ns() // (10 ** 9)
        Users[user_id]["collection"][action][norm_num]["last"] = dt

    # Обнуляем данные для записи, чтобы не мешали
    Users[user_id]["action"] = ""
    Users[user_id]["norm_num"] = ""

    bot.send_message(
        message.chat.id,
        f"Готово! {msg}"
        f"\nПродолжайте наблюдение за дорогой 👀",

        parse_mode="HTML",
        reply_markup=markup_main
    )

    show_users(show_size=False)
    save_users()


print(strftime("%H:%M:%S"))
print(config.TOKEN)
bot.polling()
