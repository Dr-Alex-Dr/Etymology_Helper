from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
import re
from controllers.pageScrapper import pageScrapper


def start(update: Update, context):
    update.message.reply_text(
        'Привет! Я бот, который определяет происхождение слов, а также год или век их появления в английском языке. Присылай слова или текст. Проанализирую всё быстро и точно:')


def handle_message(update: Update, context):
    input_text = remove_punctuation(update.message.text)
    user_message = input_text.split()
    words = pageScrapper(user_message)

    if words:
        result_words = '\n'.join(words)
        update.message.reply_text(f'{result_words}')
    else:
        update.message.reply_text(
            'Извините, я не смог найти информацию по вашим словам.')


def main():
    updater = Updater('7393561125:AAFmPkiuzWNXgV3a337ntj-d0oxrGO7XdGI')
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~
                   Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)


if __name__ == '__main__':
    main()
