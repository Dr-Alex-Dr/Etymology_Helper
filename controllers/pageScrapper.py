from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
import re


def pageScrapper(words):
    result = []

    for word in words:
        url = f'https://www.etymonline.com/search?q={word}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            etymology_div = soup.find(
                'div', class_=re.compile(r'word__etymology_expand'))

            word_info = dataProcessing(etymology_div, word)
            result.append(word_info)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса для слова '{word}': {e}")
            result.append(f'{word} запрос не выполнен')
        except Exception as e:
            print(f"Ошибка при обработке слова '{word}': {e}")
            result.append(f'{word} обработка не удалась')

    return result


def dataProcessing(pageData, word):
    origin = ['Latin', 'Old English', 'Proto-Germanic', 'Russian', 'Old French']

    paragraphs = pageData.find_all('p')

    first_occurrence = None
    dates = []

    for paragraph in paragraphs:
        paragraph_text = paragraph.get_text()

        for origin_word in origin:
            index = paragraph_text.find(origin_word)
            if index != -1:
                if first_occurrence is None or index < first_occurrence:
                    first_occurrence = index
                    first_origin = origin_word

        found_dates = re.findall(r'\b\d{2,4}\b', paragraph_text)
        dates.extend(found_dates)

    if dates:
        date_objects = [int(date) for date in dates]
        oldest_date = min(date_objects)

    if first_origin or oldest_date:
        return f'{word} {first_origin if first_origin else "Не найдено"} {oldest_date if oldest_date else "Неизвестная дата"}'
    else:
        return f'{word} информация не найдена'
