from telegram import Update
import string
from controllers.parse_etymology import parse_etymology
from controllers.normalize_time_difference import normalize_time_difference

async def start(update: Update, context):
    await update.message.reply_text('Привет! Я бот, который определяет происхождение слов, а также год или век их появления в английском языке. Присылай слова или текст. Проанализирую всё быстро и точно:')

async def handle_message(update: Update, context):
    user_text = update.message.text
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = user_text.translate(translator)
    words = cleaned_text.split(' ')

    work_time = len(words) * 0.9
    await update.message.reply_text(f'Обработка займет около {normalize_time_difference(work_time)}')
    
    info_origin = parse_etymology(words)
    await update.message.reply_text(info_origin)

