from random import randint
from bs4 import *
import requests
import datetime


# Считывание токена из файла
def read_token(filename: str):
    with open(filename) as f:
        return f.read().strip()


# Возвращает ссылку на случайную монету
def get_coin():
    orel = randint(0, 1)
    if orel == 1:
        link = 'https://monetka.nurk.ru/images/reshka.png'
    else:
        link = 'https://monetka.nurk.ru/images/orel.png'
    return link


# Возвращает случайное значение кубика
def get_cube():
    cub = randint(1, 6)
    if cub == 1:
        cub_e = '1️⃣'
    elif cub == 2:
        cub_e = '2️⃣'
    elif cub == 3:
        cub_e = '3️⃣'
    elif cub == 4:
        cub_e = '4️⃣'
    elif cub == 5:
        cub_e = '5️⃣'
    else:
        cub_e = '6️⃣'
    return cub_e


# Возвращает синоним к слову
def get_synonym(word: str):
    response = requests.get(f"https://synonymonline.ru/{word[0].title()}/{word.lower().strip()}")
    html = BeautifulSoup(''.join(response.text), features="html.parser")
    class_synonym = html.findAll("ol", {'class': 'synonyms-list row'})
    if class_synonym:
        return class_synonym[0].text.replace('\n', ' | ')
    else:
        return 'По вашему слову синонимов не найдено :('


# Возвращает антоним к слову
def get_antonym(word: str):
    response = requests.get(f"https://antonymonline.ru/{word[0].title()}/{word.lower().strip()}")
    html = BeautifulSoup(''.join(response.text), features="html.parser")
    class_synonym = html.findAll("ol", {'class': 'row antonyms-list'})
    if class_synonym:
        return class_synonym[0].text.replace('\n', ' | ')
    else:
        return 'По вашему слову антонимов не найдено :('


# Взвращает количество прожитых дней (дд.мм.гггг)
def days_lived(birthday: str):
    birthday = birthday.strip().split('.')
    try:
        date_birthday = datetime.date(int(birthday[2]), int(birthday[1]), int(birthday[0]))
        date_today = datetime.date.today()
        day_passed = date_today - date_birthday
        return f'Дней прожито: {day_passed.days}'
    except ValueError:
        return 'Некорректно введена дата рождения'


# Возвращает гороскоп на сегодня по дате рождения (дд.мм.гггг)
def get_horoscope(birthday: str):
    birthday = birthday.strip().split('.')
    try:
        # Получаем по дате информацию о знаке зодиака
        response = requests.get(f'https://1001goroskop.ru/astroportret/?day='
                                f'{birthday[0]}&month={birthday[1]}&year={birthday[2]}')
        html = BeautifulSoup(''.join(response.text), features="html.parser")
        class_astro = html.findAll("ul", {'class': 'astroprtret'})
        zodiac = class_astro[0].contents[0]
        zodiac_result = f'Знак зодиака: ' \
                        f'{zodiac.contents[1].text.strip()}\n{zodiac.contents[2].text.replace(">>>","").strip()}\n\n'
        maya = class_astro[0].contents[1]
        maya_result = f'Майянский знак рождения: ' \
                      f'{maya.contents[1].text.strip()}\n{maya.contents[2].text.replace(">>>","").strip()}\n\n'
        china = class_astro[0].contents[2]
        china_result = f'Китайский знак рождения: ' \
                       f'{china.contents[1].text.strip()}\n{china.contents[2].text.replace(">>>","").strip()}\n\n'

        # Получаем гороскоп
        key = zodiac.contents[1].contents[1].attrs['href'].split('/')[4].split('?')[1]
        response = requests.get(f'https://1001goroskop.ru/?znak={key}')
        html = BeautifulSoup(''.join(response.text), features="html.parser")
        itemprop = html.findAll("div", {'itemprop': 'description'})
        horoscope_result = f'Гороскоп на сегодня: {itemprop[0].text}'

        return zodiac_result + maya_result + china_result + horoscope_result
    except:
        return 'Некорректно введена дата рождения'
