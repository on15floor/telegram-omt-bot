from random import randint
from bs4 import *
import requests


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
