import telebot
from extensions import APIException, Convert
from config import key, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def help_and_start(message: telebot.types.Message):
    text = f"""
        Привет {message.from_user.first_name} !
        Я помогу узнать вам курс определенных валют для этого отправьте мне сообщение формате:
        <имя валюты, цену которую ты хочешь узнать> 
        <имя валюты, в которой надо узнать цену первой валюты> 
        <количество первой валюты>
        Однако , я работаю только с этими валютами: евро, доллар или рубль:(
    """
    bot.send_message(message.chat.id, text)
    bot.send_sticker(message.chat.id, sticker="CAACAgIAAxkBAAEFjKVi92q6DMv97AiPoFh3LSJihZRRJQACGwADO2AkFNCUnNAljlGHKQQ")


@bot.message_handler(commands=['values'])
def values_converts(message: telebot.types.Message):
    text = """
           Доступные валюты:
           рубль
           доллар
           евро
       """
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def result_convert(message: telebot.types.Message):
    convert_ = Convert()
    base, qute, amount = message.text.split()
    try:
        if (not amount.isdigit()) or float(amount) < 0:
            raise APIException(f"Количество первой валюты некорректно!")

        if not (qute in key or base in key):
            raise APIException(f" Валюта не поддерживается ")
        amount = float(amount)
        bot.send_message(message.chat.id, qute)

        result = convert_.get_price(key[base], key[qute], amount)
        bot.send_message(message.chat.id, result)
    except APIException as e:
        bot.send_message(message.chat.id, e)


bot.polling(none_stop=True)
