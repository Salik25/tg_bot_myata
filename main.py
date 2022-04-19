import datetime
import telebot
from telebot import types  # для указание типов
import psycopg2
from psycopg2 import Error
import re
import config

bot = telebot.TeleBot(config.key)


def bot_feedback(message):
    '''
    Функция для заполнения базы данных по отзывам работы бота
    '''
    insert_query = "INSERT INTO feedback_bot (AUTHOR,FEEDBACK_MESSAGE) VALUES(%s,%s)"
    cursor.execute(insert_query,
                   (message.from_user.username, message.text))
    connection.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("МЕНЮ")
    markup.add(back)
    bot.send_message(message.chat.id,
                     "Спасибо за ответ! Снизу есть кнопка МЕНЮ, там вы можете забронировать стол, заказать еду, посмотреть график мероприятий и просто написать нам)Будем рады видеть вас снова)",
                     reply_markup=markup)


def work_feedback(message):
    '''
    Функция для заполнения базы данных по отзывам работы заведения
    '''
    insert_query = "INSERT INTO work_feedback (AUTHOR,FEEDBACK_MESSAGE) VALUES(%s,%s)"
    cursor.execute(insert_query,
                   (message.from_user.username, message.text))
    connection.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("МЕНЮ")
    markup.add(back)
    bot.send_message(message.chat.id,
                     "Спасибо за ответ! Снизу есть кнопка МЕНЮ, там вы можете забронировать стол, заказать еду, посмотреть график мероприятий и просто написать нам)Будем рады видеть вас снова)",
                     reply_markup=markup)


def booking_db(message):
    '''
    Функция для заполнения базы данных при бронировании стола и т.д.
    '''
    today = datetime.datetime.now()
    insert_query = "INSERT INTO booking_db (TELEGRAM,NUMBER,TIME_OF_APPEAL) VALUES(%s,%s,%s)"
    cursor.execute(insert_query,
                   (message.from_user.username, message.text, str(today)))
    connection.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("МЕНЮ")
    markup.add(back)
    bot.send_message(message.chat.id, 'Ожидайте звонок', reply_markup=markup)


def root(message):
    '''
    Функция для доступа в админку
    '''
    cursor.execute(f"SELECT root FROM user_tg_bot WHERE TG_NAME='{message.chat.username}'")  # доп проверка на админа
    data = cursor.fetchall()
    if data[0][0]:
        bot.send_message(message.chat.id, text='Вы в режиме администратора')
        menu_root(message)
    else:
        bot.send_message(message.chat.id,
                         text='Вы не администратор.',
                         reply_markup=types.ReplyKeyboardRemove())
        menu(message)


def menu(message):
    '''
    Функция для вызова меню
    '''
    cursor.execute(f"SELECT * FROM menu_db")
    data = dict(cursor.fetchall())
    cursor.execute(f"SELECT * FROM menu_content")
    content_url = dict(cursor.fetchall())

    markup = types.InlineKeyboardMarkup()
    button_menu1 = types.InlineKeyboardButton(data[1], callback_data='график мероприятий')
    button_menu2 = types.InlineKeyboardButton(data[2], callback_data='бронь стола')
    button_menu3 = types.InlineKeyboardButton(data[3],
                                              url=content_url[3],
                                              callback_data='заказ еды')
    button_menu4 = types.InlineKeyboardButton(data[4], callback_data='заказ мероприятия')
    button_menu5 = types.InlineKeyboardButton(data[5], url=content_url[5],
                                              callback_data='осмотр интерьера')
    button_menu6 = types.InlineKeyboardButton(data[6],
                                              url=content_url[6],
                                              callback_data='где мы находимся')
    button_menu7 = types.InlineKeyboardButton(data[7], callback_data='оставить отзыв')
    button_menu8 = types.InlineKeyboardButton(data[8],
                                              callback_data='не нашел нужного пункта')
    markup.row(button_menu1, button_menu2)
    markup.row(button_menu3, button_menu4)
    markup.row(button_menu5, button_menu6)
    markup.row(button_menu7, button_menu8)
    bot.send_message(message.chat.id, text="Выберите пункт из меню", reply_markup=markup)


def edit_menu(message):
    '''
    Функция для изменения меню
    '''
    cursor.execute(f"SELECT * FROM menu_db")
    data = dict(cursor.fetchall())
    markup = types.InlineKeyboardMarkup()
    button_text1 = types.InlineKeyboardButton(data[1], callback_data='1')
    button_text2 = types.InlineKeyboardButton(data[2], callback_data='2')
    button_text3 = types.InlineKeyboardButton(data[3], callback_data='3')
    button_text4 = types.InlineKeyboardButton(data[4], callback_data='4')
    button_text5 = types.InlineKeyboardButton(data[5], callback_data='5')
    button_text6 = types.InlineKeyboardButton(data[6], callback_data='6')
    button_text7 = types.InlineKeyboardButton(data[7], callback_data='7')
    button_text8 = types.InlineKeyboardButton(data[8], callback_data='8')
    markup.row(button_text1, button_text2)
    markup.row(button_text3, button_text4)
    markup.row(button_text5, button_text6)
    markup.row(button_text7, button_text8)
    bot.send_message(message.chat.id, 'Какой пункт изменить?', reply_markup=markup)


def edit_name_menu(message, call_data):
    '''
    Изменение названия поля в меню
    '''
    insert_query = f"UPDATE menu_db SET new_name='{message.text}' WHERE button={call_data}"
    cursor.execute(insert_query)
    connection.commit()
    bot.send_message(message.chat.id, text="Название изменено")
    menu_root(message)


def menu_root(message):
    '''
    Функция для вызова меню администратора
    '''
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Изменить мероприятия", callback_data='изменить мероприятия')
    button2 = types.InlineKeyboardButton("Изменить ссылку на заказ еды", callback_data='13')
    button3 = types.InlineKeyboardButton("Изменить ссылку на интерьер", callback_data='15')
    button4 = types.InlineKeyboardButton("Изменить ссылку на местонахождение", callback_data='16')
    button5 = types.InlineKeyboardButton("Изменить название пункта",
                                         callback_data='изменить пункты')
    button6 = types.InlineKeyboardButton("Выйти",
                                         callback_data='не входить в админку')
    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    markup.row(button4)
    markup.row(button5)
    markup.row(button6)
    bot.send_message(message.chat.id, text="Выберите пункт из меню", reply_markup=markup)


def edit_link(message, call_data):
    '''
    Функция для изменения ссылок в кнопках меню
    '''
    insert_query = f"UPDATE menu_content SET content='{message.text}' WHERE how_but={call_data}"
    cursor.execute(insert_query)
    connection.commit()
    bot.send_message(message.chat.id, text="Название изменено")
    menu_root(message)


def edit_title(message, call_data):
    '''
    Функция для изменения название у СУЩЕСТВУЮЩЕГО мероприятия
    '''
    insert_query = f"UPDATE events_db SET title='{message.text}' WHERE id={call_data}"
    cursor.execute(insert_query)
    connection.commit()
    bot.send_message(message.chat.id, text="Название изменено")
    menu_root(message)


def edit_description(message, call_data):
    '''
    Функция для изменения описания у СУЩЕСТВУЮЩЕГО мероприятия
    '''
    insert_query = f"UPDATE events_db SET description='{message.text}' WHERE id={call_data}"
    cursor.execute(insert_query)
    connection.commit()
    bot.send_message(message.chat.id, text="Описание изменено")
    menu_root(message)


def new_title(message):
    '''
    Функция для создания названия мероприятия
    '''
    cursor.execute(f"INSERT INTO events_db (title) VALUES('{str(message.text)}')")
    connection.commit()
    bot.send_message(message.chat.id, text="Название добавлено")
    bot.send_message(message.chat.id, 'Введите новое описание:')
    bot.register_next_step_handler(message, new_description, message.text)


def new_description(message, title):
    '''
    Функция для создания описания мероприятия
    '''
    cursor.execute(f"UPDATE events_db SET description='{message.text}' WHERE title='{title}'")
    connection.commit()
    bot.send_message(message.chat.id, text="Описание добавлено")
    menu_root(message)


try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  password="123",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="client")
    cursor = connection.cursor()


    @bot.message_handler(commands=['start'])
    def start(message):
        cursor.execute(
            f"SELECT EXISTS(SELECT TG_NAME FROM user_tg_bot WHERE TG_NAME='{message.from_user.username}')")  # проверка на наличие администраторских прав у пользователя
        data = cursor.fetchall()
        if not data[0][0]:
            insert_query = "INSERT INTO user_tg_bot (TG_NAME,FIRST_NAME,LAST_NAME) VALUES(%s,%s,%s)"
            cursor.execute(insert_query,
                           (message.from_user.username, message.from_user.first_name, message.from_user.last_name))
            connection.commit()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("✅ Да")
            btn2 = types.KeyboardButton("❌ Нет")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id,
                             text=f'Приветствуем вас, {message.from_user.last_name}!\nМы рады видеть вас в Мята Cyber lounge! 🍃\n'
                                  f'Здесь вы можете бронировать столы, видеть анонсы мероприятий и заказывать еду, а так же узнавать о новостях Мяты)\n'
                                  f'Уже бывали у нас в гостях?',
                             reply_markup=markup)
        else:
            cursor.execute(f"SELECT root FROM user_tg_bot WHERE TG_NAME='{message.from_user.username}'")
            data = cursor.fetchall()
            if data[0][0]:
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton("Войти в панель администрирования", callback_data='войти в админку')
                btn2 = types.InlineKeyboardButton("Продолжить как пользователь", callback_data='не входить в админку')
                markup.row(btn1)
                markup.row(btn2)
                bot.send_message(message.chat.id,
                                 text='Добро пожаловать администратор. Хотите войти в режим администрирования?',
                                 reply_markup=markup)
            else:
                bot.send_message(message.chat.id,
                                 text=f'С возвращением вас, {message.from_user.last_name}!\nМы рады видеть вас снова в Мята Cyber lounge!🍃\n'
                                      f'Здесь вы можете бронировать столы, видеть анонсы мероприятий и заказывать еду, а так же узнавать о новостях Мяты)')
                menu(message)


    @bot.message_handler(commands=['admin'])
    def root_panel(message):
        root(message)


    @bot.message_handler(content_types=['text'])
    def func(message):
        if message.text == "✅ Да":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Кальяны")
            btn2 = types.KeyboardButton("Еда, напитки")
            btn3 = types.KeyboardButton("Мероприятия")
            btn4 = types.KeyboardButton("Настольные игры")
            btn5 = types.KeyboardButton("Обслуживание")
            btn6 = types.KeyboardButton("Компьютеры, Sony PC")
            btn7 = types.KeyboardButton('Любой ответ ')
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
            bot.send_message(message.chat.id, text="Спасибо, что выбираете нас!\nЧто вам нравится у нас больше всего?",
                             reply_markup=markup)
        elif message.text == "❌ Нет":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("МЕНЮ")
            markup.add(btn1)
            bot.send_message(message.chat.id,
                             text="🍃Ждем вас в гости, наш адрес: Тюменский ЦУМ, отдельный вход с пересечения улиц Герцена-Орджоникидзе!\n"
                                  "Снизу есть кнопка МЕНЮ, там вы можете забронировать стол, заказать еду, посмотреть график мероприятий или просто написать нам) До встречи)",
                             reply_markup=markup)
        elif message.text in ["Кальяны", "Еда, напитки", "Мероприятия", "Настольные игры", "Обслуживание",
                              "Компьютеры, Sony PC"]:
            work_feedback(message)
        elif message.text == "Любой ответ":
            bot.send_message(message.chat.id, 'Напишите ваш отзыв и отправьте')
            bot.register_next_step_handler(message, work_feedback)
        elif message.text == "МЕНЮ":
            menu(message)
        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        if call.data == 'войти в админку':
            root(call.message)
        elif call.data == 'не входить в админку':
            menu(call.message)
        elif call.data == 'график мероприятий':
            cursor.execute(f"SELECT * FROM events_db") # список мероприятий из бд
            data = cursor.fetchall()
            events = {}
            for i in data: # формируем словарь для удобства работы
                for j in range(1, 3):
                    if i[0] in events.keys():
                        events[i[0]].append(i[j])
                    else:
                        events[i[0]] = [i[j]]
            markup = types.InlineKeyboardMarkup()
            for id in events: # заполняем список кнопок для меню
                button1 = types.InlineKeyboardButton(events[id][0], callback_data=f'описание{id}')
                markup.row(button1)
            bot.send_message(call.message.chat.id, text="Список мероприятий", reply_markup=markup)
        elif re.fullmatch(r'описание\d+', call.data): # при нажатии на описание предлагаем бронь
            cursor.execute(f"SELECT description FROM events_db WHERE id={call.data[8:]}")
            data = cursor.fetchall()
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(data[0][0], callback_data='бронь на мероприятие')
            markup.row(button1)
            bot.send_message(call.message.chat.id, text="Описание мероприятия", reply_markup=markup)
        elif call.data == 'бронь на мероприятие':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Да', callback_data='бронь стола')
            button2 = types.InlineKeyboardButton('Нет', callback_data='нет')
            markup.row(button1, button2)
            bot.send_message(call.message.chat.id, text="Для вас забронировать столик на мероприятие?",
                             reply_markup=markup)
        elif call.data == 'нет':
            bot.send_message(call.message.chat.id,
                             text="Если вам интересно что-то другое - нажмите на кнопку Меню снизу.\n"
                                  "Всегда рады вам у нас в гостях)")
            menu(call.message)
        elif call.data == 'бронь стола':
            bot.send_message(call.message.chat.id,
                             'Оставьте ваш номер телефона, мы скоро вам перезвоним и подтвердим бронь')
            bot.register_next_step_handler(call.message, booking_db)
        elif call.data == 'заказ мероприятия':
            bot.send_message(call.message.chat.id,
                             'Оставьте ваш номер телефона, мы свяжемся с вами и уточним все детали')
            bot.register_next_step_handler(call.message, booking_db)
        elif call.data == 'оставить отзыв':
            bot.send_message(call.message.chat.id, 'Мы будем рады услышать ваше мнение о любых сторонах нашей работы')
            bot.register_next_step_handler(call.message, work_feedback)
        elif call.data == 'не нашел нужного пункта':
            bot.send_message(call.message.chat.id,
                             'Отправте нам какого пункта не хватает. Мы будем рады услышать ваше мнение о любых сторонах нашей работы')
            bot.register_next_step_handler(call.message, bot_feedback)
        elif call.data == 'изменить пункты':
            edit_menu(call.message)
        elif call.data in ['1', '2', '3', '4', '5', '6', '7', '8']:
            bot.send_message(call.message.chat.id, 'Введите новое название пункта:')
            bot.register_next_step_handler(call.message, edit_name_menu, call.data)
        elif call.data in ['13', '15', '16']:
            bot.send_message(call.message.chat.id, 'Введите новую ссылку:')
            bot.register_next_step_handler(call.message, edit_link, str(int(call.data) % 10))
        elif call.data == 'изменить мероприятия':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Добавить новое', callback_data='добавить')
            button2 = types.InlineKeyboardButton('Изменить существующее', callback_data='изменить')
            markup.row(button1, button2)
            bot.send_message(call.message.chat.id, text="Вы хотите добавит мероприятие или изменить существующее?",
                             reply_markup=markup)
        elif call.data == 'добавить':
            bot.send_message(call.message.chat.id, 'Введите новое название:')
            bot.register_next_step_handler(call.message, new_title)
        elif call.data == 'изменить':
            cursor.execute(f"SELECT * FROM events_db")
            data = cursor.fetchall()
            events = {}
            for i in data: # формируем словарь для удобства работы
                for j in range(1, 3):
                    if i[0] in events.keys():
                        events[i[0]].append(i[j])
                    else:
                        events[i[0]] = [i[j]]
            markup = types.InlineKeyboardMarkup()
            for id in events: # заполняем список кнопок меню
                button1 = types.InlineKeyboardButton(events[id][0], callback_data=f'изменение{id}')
                markup.row(button1)
            bot.send_message(call.message.chat.id, text="Какое мероприятие хотите изменить?",
                             reply_markup=markup)
        elif re.fullmatch(r'изменение\d+', call.data):
            id = call.data[9:]
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Изменить название', callback_data=f'изменить_название{id}')
            button2 = types.InlineKeyboardButton('Изменить описание', callback_data=f'изменить_описание{id}')
            markup.row(button1, button2)
            bot.send_message(call.message.chat.id, text="Что вы хотите изменить?",
                             reply_markup=markup)
        elif re.fullmatch(r'изменить_название\d+', call.data):
            bot.send_message(call.message.chat.id, 'Введите новое название:')
            bot.register_next_step_handler(call.message, edit_title, call.data[17:])
        elif re.fullmatch(r'изменить_описание\d+', call.data):
            bot.send_message(call.message.chat.id, 'Введите новое описание:')
            bot.register_next_step_handler(call.message, edit_description, call.data[17:])


    bot.polling(none_stop=True)
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
