import requests
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer

def editText(words):
    origin = ['Latin', 'Old English', 'Proto-Germanic', 'Russian']
    result = []
    stemmer = PorterStemmer()

    for word in words:
        url = f'https://www.etymonline.com/search?q={word}'

        oldest_date = None
        first_origin = None

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            etymology_div = soup.find('div', class_=re.compile(r'word__etymology_expand'))

            if etymology_div:
                paragraphs = etymology_div.find_all('p')

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

                    found_dates = re.findall(r'\b\d{2,4}s?\b|\b\d{2,4}c\.\b', paragraph_text)
                    dates.extend(found_dates)

                if dates:
                    date_objects = [int(date.rstrip('s').rstrip('c.')) for date in dates]  # Удаление 's' и 'c.'
                    oldest_date = min(date_objects)
                    
                if not first_origin:
                    word_links = etymology_div.find_all('a', href=True)
                    for link in word_links:
                        linked_word = link.get('href').split('/')[-1]
                        if linked_word:
                            new_url = f'https://www.etymonline.com{link.get("href")}'
                            new_response = requests.get(new_url)
                            if new_response.status_code == 200:
                                new_soup = BeautifulSoup(new_response.text, 'html.parser')
                                new_etymology_div = new_soup.find('div', class_=re.compile(r'word__etymology_expand'))
                                if new_etymology_div:
                                    new_paragraphs = new_etymology_div.find_all('p')
                                    for new_paragraph in new_paragraphs:
                                        new_paragraph_text = new_paragraph.get_text()
                                        for origin_word in origin:
                                            index = new_paragraph_text.find(origin_word)
                                            if index != -1:
                                                first_origin = origin_word
                                                break
                                        if first_origin:
                                            break
                                if first_origin:
                                    break

                if not first_origin:
                    stemmed_word = stemmer.stem(word)
                    url = f'https://www.etymonline.com/search?q={stemmed_word}'
                    response = requests.get(url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        etymology_div = soup.find('div', class_=re.compile(r'word__etymology_expand'))
                        if etymology_div:
                            paragraphs = etymology_div.find_all('p')
                            for paragraph in paragraphs:
                                paragraph_text = paragraph.get_text()
                                for origin_word in origin:
                                    index = paragraph_text.find(origin_word)
                                    if index != -1:
                                        first_origin = origin_word
                                        break
                                if first_origin:
                                    break

                result.append(f'{word} {first_origin} {oldest_date}')
        else:
            continue

    return result
