import telebot
from bot_utils import read_token, get_coin, get_cube, get_synonym, get_antonym, days_lived, get_horoscope

# Инициализация бота
bot_token = read_token('token.txt')
bot = telebot.TeleBot(bot_token)
print('[i] Starting bot')


# Стартовая команда
@bot.message_handler(commands=['start', 'help'])
def command_start(message):
    bot.send_message(message.chat.id, 'Список доступных команд:\n'
                                      '/coin - Подбросить монетку\n'
                                      '/cube - Подбросить кубик\n'
                                      '/synonym - Поиск синонимов\n'
                                      '/antonym - Поиск антонимов\n'
                                      '/days_lived - Вычислений дней прожитых вами\n'
                                      '/horoscope - Гороскоп по дате рождения')


# Бросить монетку
@bot.message_handler(commands=['coin'])
def command_coin(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(text='Подбросить еще раз 🌕', callback_data='coin'),
                 telebot.types.InlineKeyboardButton(text='К списку команд', callback_data='back'))

    bot.send_photo(message.chat.id, get_coin())
    bot.send_message(message.chat.id, text="Подбросить еще раз монетку?", reply_markup=keyboard)


# Бросить кубик
@bot.message_handler(commands=['cube'])
def command_cube(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(text='Подбросить еще раз 🎲', callback_data='cube'),
                 telebot.types.InlineKeyboardButton(text='К списку команд', callback_data='back'))

    bot.send_message(message.chat.id, get_cube())
    bot.send_message(message.chat.id, text="Подбросить еще раз кубик?", reply_markup=keyboard)


# Поиск синонимов (ввод слова)
@bot.message_handler(commands=['synonym'])
def command_input_synonym(message):
    sent = bot.send_message(message.chat.id, 'Введите слово для поиска его синонима:')
    bot.register_next_step_handler(sent, command_synonym)


# Поиск синонимов (возвращение синонима)
def command_synonym(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(text='Начать поиск нового синонима', callback_data='synonym'),
                 telebot.types.InlineKeyboardButton(text='К списку команд', callback_data='back'))

    bot.send_message(message.chat.id, get_synonym(message.text), reply_markup=keyboard)


# Поиск антонимов (ввод слова)
@bot.message_handler(commands=['antonym'])
def command_input_antonym(message):
    sent = bot.send_message(message.chat.id, 'Введите слово для поиска его антонима:')
    bot.register_next_step_handler(sent, command_antonym)


# Поиск антонимов (возвращение антонима)
def command_antonym(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(text='Начать поиск нового антонима', callback_data='antonym'),
                 telebot.types.InlineKeyboardButton(text='К списку команд', callback_data='back'))

    bot.send_message(message.chat.id, get_antonym(message.text), reply_markup=keyboard)


# Расчет прожитых дней (ввод даты)
@bot.message_handler(commands=['days_lived'])
def command_input_days_lived(message):
    sent = bot.send_message(message.chat.id, 'Введите дату рождения в формате дд.мм.гггг:')
    bot.register_next_step_handler(sent, command_days_lived)


# Расчет прожитых дней (возвращение количества дней)
def command_days_lived(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(text='Расчитать заново', callback_data='days_lived'),
                 telebot.types.InlineKeyboardButton(text='К списку команд', callback_data='back'))

    bot.send_message(message.chat.id, days_lived(message.text), reply_markup=keyboard)


# Гороскоп (ввод даты)
@bot.message_handler(commands=['horoscope'])
def command_input_horoscope(message):
    sent = bot.send_message(message.chat.id, 'Введите дату рождения в формате дд.мм.гггг:')
    bot.register_next_step_handler(sent, command_horoscope)


# Вывод гороскопа (возвращение количества дней)
def command_horoscope(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(text='Другой гороскоп', callback_data='horoscope'),
                 telebot.types.InlineKeyboardButton(text='К списку команд', callback_data='back'))

    bot.send_message(message.chat.id, get_horoscope(message.text), reply_markup=keyboard)


# Обработка результатов
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'back':
        command_start(call.message)
    elif call.data == 'coin':
        command_coin(call.message)
    elif call.data == 'cube':
        command_cube(call.message)
    elif call.data == 'synonym':
        command_input_synonym(call.message)
    elif call.data == 'antonym':
        command_input_antonym(call.message)
    elif call.data == 'days_lived':
        command_input_days_lived(call.message)
    elif call.data == 'horoscope':
        command_input_horoscope(call.message)
    # Скрыть клавиатуру
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


bot.polling()
