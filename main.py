#!/usr/bin/env python

#### Импорт библиотек

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from datetime import datetime

#### Определение констант

URL = "https://smoothie.ru/catalog/all/"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
HOST = "https://smoothie.ru"

#### Формируем запрос к странице
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

#### Функция парсинга данных
def get_content():
    cur_date = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    # with open("smoothie_save_page.html", "w", encoding="utf-8") as file:
    #     file.write(page.text)
    #
    # with open("smoothie_save_page.html", encoding="utf-8") as file:
    #     page = file.read()

    #### Создаем форму CSV таблицы

    with open(f"{cur_date}.csv", "w", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            (
                "Наименование",
                "Артикул",
                "Цена",
                "Наличие"
            )
        )
    list_items_smoothie = []
    # Формируем запрос к странице
    for page in range(2, 3):
        r = get_html(URL + f'?show_all=1&sort=3&pg={page}')
        soup = BeautifulSoup(r.text, 'lxml')
        list_items = soup.find_all('div', class_="white_bl_str white_bl_str2 b10")
        for item in list_items:
            try:
                item_title = item.find("a", class_="s20 green").text
            except:
                item_title = "Название не найдено"
            try:
                item_href = HOST + item.find("a", class_="s20 green").get("href")
                r = get_html(item_href)
                soup = BeautifulSoup(r.text, 'lxml')
                item_artikul = soup.find('div', class_='s12').text.replace("Артикул:", "")

            except:
                item_artikul = "Информация не найдена"
            try:
                item_price = soup.find('span', class_='bl_l').text
                item_price = item_price.strip().replace("руб.", "")
            except:
                item_price = "Цена не найдена"
            try:
                item_exists = soup.find('span', class_='available').text
                if item_exists == "товар в наличии":
                    item_exists = "Есть"
                else:
                    item_exists = "Нет"
            except:
                item_exists = "Информация не найдена"

            list_items_smoothie.append({
                'item_title': item_title,
                'item_artikul': item_artikul,
                'item_price': item_price,
                'item_exists': item_exists
            })

            with open(f"{cur_date}.csv", "a", newline='') as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(
                    (
                        item_title,
                        item_artikul,
                        item_price,
                        item_exists
                    )
                )
        print(f"[INFO] Обработана страница {page}/32")
        time.sleep(1)


def main():
    get_content()


if __name__ == '__main__':
    main()












