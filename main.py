"""Основной файл тестового задания."""

import logging
import os
import requests

from dotenv import load_dotenv
from http import HTTPStatus
from telebot import TeleBot, types


load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FATHER_ID = os.getenv('FATHER_ID')
ADDRESS = (
    'https://yandex.ru/maps/239/sochi/house/ulitsa_lenina_1/'
    'Z0AYfwVkQE0CQFppfXhzdHxkZg==/'
    '?indoorLevel=1&ll=39.924985%2C43.425072&z=17'
)
PAYMENT = ''
DOG_IMAGE_URL = 'https://dog.ceo/api/breeds/image/random'

# Создаём объект класса Telebot
bot = TeleBot(token=TELEGRAM_TOKEN)


logging.basicConfig(
    encoding='utf-8',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


def random_dog_image():
    """Получаем рандомное изображение собаки."""
    response = requests.get(DOG_IMAGE_URL)
    response = response.json()
    image = response.get('message')
    return image


@bot.message_handler(commands=['start'])
def awakening(message):
    """Обработчик активации бота."""
    chat = message.chat
    name = chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton('/Кнопка_1')
    button_2 = types.KeyboardButton('/Кнопка_2')
    button_3 = types.KeyboardButton('/Кнопка_3')
    button_4 = types.KeyboardButton('/Кнопка_4')
    button_5 = types.KeyboardButton('/Кнопка_5')
    keyboard.add(
        button_1,
        button_2,
        button_3,
        button_4,
        button_5
    )
    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}!',
        reply_markup=keyboard
    )
    logging.info(
        f'{name} с ID "{chat.id}" запустил бота.'
    )


@bot.message_handler(commands=['Кнопка_1'])
def give_me_address(message):
    """Отправляю кнопку с ссылкой на необходимый адрес."""
    chat = message.chat
    keyboard = types.InlineKeyboardMarkup()
    button_address = types.InlineKeyboardButton(
        text='Смотреть',
        url=ADDRESS
    )
    keyboard.add(button_address)
    bot.send_message(
        chat_id=chat.id,
        text='Показать сердце моего города?',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['Кнопка_2'])
def pay_the_order(message):
    pass


@bot.message_handler(commands=['Кнопка_3'])
def give_me_image(message):
    """Отправляем юзеру изображение кота."""
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text='Смотри какой милаш)'
    )
    bot.send_photo(
        chat_id=chat_id,
        photo=random_dog_image()
    )


@bot.message_handler(commands=['Кнопка_4'])
def give_me_value(message):
    pass


@bot.message_handler(commands=['Кнопка_5'])
def date_validator(message):
    pass


def main():
    """Основная логика бота."""
    # Запускаем переодическую проверку новых событий
    while True:
        try:
            bot.polling()
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)


if __name__ == '__main__':
    logging.info('Бот активирован.')
    main()
