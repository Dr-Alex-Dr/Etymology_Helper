import requests
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer

def parse_etymology(words):
    info_origin = []
    
    for word in words:     
        origin, date = get_origin_and_date(word)
        
        if origin is None:
            origin, date = get_origin_and_date(stemmer(word))
            
        if (origin is None and date is None):
            info_origin.append(f'{word} None')
            print(f'{word} None')
        else:
            info_origin.append(f'{word} {origin} {date}')
            print(f'{word} {origin} {date}')

    return '\n'.join(info_origin)
             
def get_origin_and_date(word):
    url = f'https://www.etymonline.com/search?q={word}'
    
    text = fetch_etymology_text(url)
    origin = find_first_matching_word(text)
    date = find_earliest_date_century(text)
    
    return origin, date

def stemmer(word):
    stemmer = PorterStemmer()
    return stemmer.stem(word)
     
def fetch_etymology_text(url):
    try:
        httpResponse = requests.get(url)

        if httpResponse.status_code == 200:
            htmlSoup = BeautifulSoup(httpResponse.text, 'html.parser')
            domElement = htmlSoup.find('div')
            
            return domElement.get_text()          
    except:
        print("Error getting data from etymology") 
              
def find_first_matching_word(text):
    if text is None:
        return None
    
    origin_list = ['Latin', 'Old English', 'Proto-Germanic', 'Russian']
    
    first_origin = None
    min_index = float("inf") 

    for origin_word in origin_list:
        index = text.find(origin_word)
        if index < min_index and index >= 0:
            min_index = index
            first_origin = origin_word
            
    return first_origin

def find_earliest_date_century(text):
    if text is None:
        return None
    
    found_dates_or_centuries = re.findall(r'\b(\d{1,2}c|\d{4}(?:s)?)\b', text)
    
    min_date = None
    for date_or_century in found_dates_or_centuries:
        if normalizes_date(date_or_century) < normalizes_date(min_date):
            min_date = date_or_century.rstrip('s')
        
    return min_date

def normalizes_date(date):
    if (date is None):
        return float('inf') 
    if date.endswith('c'):
        return int(date[:-1]) * 100
    elif date.endswith('s'):
        return int(date[:-1])
    return int(date)