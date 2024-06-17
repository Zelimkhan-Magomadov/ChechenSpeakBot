import os

import telebot

from translateRepository import get_translation

token = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(token)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        if message.chat.type == 'private':
            text_to_translate = message.text
        elif message.text.startswith('/'):
            text_to_translate = message.text[1:]

        translations = get_translation(text_to_translate)

        if isinstance(translations, list):
            for translation in translations:
                bot.send_message(message.chat.id, f"{translation['word']} - {translation['translate']}")
        else:
            bot.send_message(message.chat.id, translations)
    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")


print('Bot started')
bot.polling(interval=5)
