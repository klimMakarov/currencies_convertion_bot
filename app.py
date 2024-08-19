import telebot
from config import *
from extensions import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def handle_start_help(message: telebot.types.Message):
    text = ("Бот показывает стоимость валют\n\n"
            "Введите комманду в формате:"
            "<код валюты А> <код валюты B, в которую необходимо перевести валюту А> <Кол-во валюты А>\n\n"
            "Пример: usd rub 5\n\n"
            "Введите /values для получения списка доступных валют")

    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def handle_values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for currency in currencies:
        text = "\n".join((text, f"{currency} ({currencies[currency]})"))

    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def handle_text(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Некорректное число параметров")

        base, quote, amount = values
        total_quote = CurrencyConvertor.get_price(base, quote, amount)
        amount = float(amount)

    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Сбой в работе бота.\n{e}")

    else:
        format_ = "{:.2f}"
        text = f"{format_.format(amount)} {base} = {format_.format(amount * total_quote)} {quote}"
        bot.reply_to(message, text)


bot.polling(non_stop=True)
