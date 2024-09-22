from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters
from .etymology_service import editText

def start(update: Update, context):
    update.message.reply_text('Привет! Я бот, который определяет происхождение слов, а также год или век их появления в английском языке. Присылай слова или текст. Проанализирую всё быстро и точно:')

def handle_message(update: Update, context):
    user_message = update.message.text.split(' ')

    words = editText(user_message)
    result_words = '\n'.join(words)
    update.message.reply_text(f'{result_words}')

def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
