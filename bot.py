import telebot
from random import randint
from bot_utils import read_token

# Инициализация бота
bot_token = read_token('token.txt')
bot = telebot.TeleBot(bot_token)
print('[i] Starting bot')


# Стартовая команда
@bot.message_handler(commands=['start', 'help'])
def command_start(message):
    bot.send_message(message.chat.id, '*Список доступных команд:*\n'
                                      '/coin - Подбросить монетку\n'
                                      '/cube - Подбросить кубик', parse_mode= 'Markdown')


# Бросить монетку
@bot.message_handler(commands=['coin'])
def command_coin(message):
    orel = randint(0, 1)
    if orel == 1:
        bot.send_photo(message.chat.id, 'https://monetka.nurk.ru/images/reshka.png')
    else:
        bot.send_photo(message.chat.id, 'https://monetka.nurk.ru/images/orel.png')
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(text='Подбросить еще раз 🌕', callback_data='coin'),
                 telebot.types.InlineKeyboardButton(text='К списку команд', callback_data='back'))
    bot.send_message(message.chat.id, text="Подбросить еще раз монетку?", reply_markup=keyboard)


# Бросить кубик
@bot.message_handler(commands=['cube'])
def command_cube(message):
    cub = randint(1, 6)
    cub_e = ''
    if cub == 1:
        cub_e = '1️⃣'
    elif cub == 2:
        cub_e = '2️⃣'
    elif cub == 3:
        cub_e = '3️⃣'
    elif cub == 4:
        cub_e = '4️⃣'
    elif cub == 5:
        cub_e = '5️⃣'
    elif cub == 6:
        cub_e = '6️⃣'
    bot.send_message(message.chat.id, cub_e)
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(text='Подбросить еще раз 🎲', callback_data='cube'),
                 telebot.types.InlineKeyboardButton(text='К списку команд', callback_data='back'))
    bot.send_message(message.chat.id, text="Подбросить еще раз кубик?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'back':
        command_start(call.message)
    elif call.data == 'coin':
        command_coin(call.message)
    elif call.data == 'cube':
        command_cube(call.message)
    # Скрыть клавиатуру
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


bot.polling()

