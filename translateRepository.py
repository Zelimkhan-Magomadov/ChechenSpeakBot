import re

import requests

url_translate = "https://ps95.ru/dikdosham/dosh.php"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 "
                  "YaBrowser/24.4.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru,en;q=0.9",
    "Origin": "https://ps95.ru",
    "Referer": "https://ps95.ru/dikdosham/ru/",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "qtrans_front_language=ru",
    "Dnt": "1",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}


def __parse_translation(json_response):
    clean_translations = []
    for translator in json_response.values():
        for translation in translator:
            clean_translation = {
                'id': translation['id'],
                'word': __clean_text(translation['word']),
                'translate': __clean_text(translation['translate'])
            }
            clean_translations.append(clean_translation)
    return clean_translations


def __clean_text(text):
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def get_translation(word):
    data_translate = {
        "word": word,
        "lang": "ru"
    }

    response_translate = requests.post(url_translate, data=data_translate, headers=headers)

    if response_translate.status_code == 200:
        try:
            data = response_translate.json()
            if isinstance(data, dict):
                return __parse_translation(data)
        except ValueError:
            pass
    return "Нет перевода, проверьте корректность ввода"
