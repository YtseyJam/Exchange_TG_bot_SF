import telebot
from telebot import types
from config import keys, TOKEN
from utils import ConvertionExeption, CryptoConverter, RoubleCourse


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", ])
def start(message: telebot.types.Message):
    text = "👋 Введите команду боту на русском: \n*<имя валюты>* \
*<в какую валюту перевести>* \
*<количество валюты>*\nВсе доступные валюты: _/values_\nКурс валют к рублю ₽: _/buttons_"
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "Бот призван конвертировать пары валют. Введите команду боту в следующем формате: \n*<имя валюты>* \
*<в какую валюту перевести>* \
*<количество валюты>*\n\nПример: _<доллар рубль 1.5>_\n\nУвидеть список всех доступных валют: /values\n\nВы также можете воспользоваться кнопками /buttons, чтобы увидеть курс популярных валют к рублю ₽"
    bot.reply_to(message, text, parse_mode='Markdown')


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(commands=['buttons'])
def buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Курс рубля 🤑")
    markup.add(btn1)
    text = "Курс рубля 🤑"
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    if message.text != "Курс рубля 🤑":
        try:
            values = message.text.split(" ")

            if len(values) != 3:
                raise ConvertionExeption('‼️Введите три параметра!')

            quote, base, amount = values
            total_base = CryptoConverter.convert(quote, base, amount)
        except ConvertionExeption as e:
            bot.reply_to(message, f'‼️Ошибка пользователя\n{e}')
        except Exception as e:
            bot.reply_to(message, f'‼️Не удалось обработать команду\n{e}')
        else:
            text = f'Цена *{amount}* _{quote}_ в _{base}_  ➡️  *{total_base}*'
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
    else:
        usd_rub = RoubleCourse.get_rouble()[0]
        eur_rub = RoubleCourse.get_rouble()[1]
        cny_rub = RoubleCourse.get_rouble()[2]
        text = f'1💵 доллар 🟰  {usd_rub}₽\n1💶 евро 🟰  {eur_rub}₽\n1💹 йена🟰  {cny_rub}₽'

        bot.send_message(message.chat.id, text)



bot.polling()