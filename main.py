"""Основной файл тестового задания."""

import logging
import os
import re
import requests

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from dotenv import load_dotenv
from telebot import TeleBot, types


load_dotenv()


# Из окружения извлекаем необходимые токены и ссылки
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADDRESS = os.getenv('ADDRESS')
PAYMENT = os.getenv('PAYMENT')
DOG_IMAGE_URL = os.getenv('DOG_IMAGE_URL')
GOOGLE_SHEETS_URL = os.getenv('GOOGLE_SHEETS_URL')
GOOGLE_SHEETS_NAME = os.getenv('GOOGLE_SHEETS_NAME')

# Задаём валидный формат даты с помощью регулярного выражения
DATE_FORMAT = r'^\d{2}\.\d{2}\.\d{4}$'

# Создаём объект класса Telebot
bot = TeleBot(token=TELEGRAM_TOKEN)


logging.basicConfig(
    encoding='utf-8',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


def take_value_from_google_sheets():
    """Получаем значение поля А2 из Google Sheets."""
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'сredentials.json',
        scope
    )
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEETS_NAME).sheet1
    value_A2 = sheet.acell('A2').value
    return (f"Значение ячейки A2 в Google Sheets:\n{value_A2}")


def save_valid_date(user_date):
    """Сохраняем валидную дату в Google Sheets."""
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'сredentials.json',
        scope
    )
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEETS_NAME).sheet1
    sheet.append_row([user_date])


def random_dog_image():
    """Получаем рандомное изображение собаки."""
    response = requests.get(DOG_IMAGE_URL)
    response = response.json()
    image = response.get('message')
    return image


@bot.message_handler(commands=['start'])
def awakening(message):
    """Обработчик активации бота."""
    chat_id = message.chat.id
    name = message.chat.first_name
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
        chat_id=chat_id,
        text=f'Привет, {name}!',
        reply_markup=keyboard
    )
    logging.info(
        f'{name} с ID "{chat_id}" запустил бота.'
    )


@bot.message_handler(commands=['Кнопка_1'])
def give_me_address(message):
    """Отправляем кнопку с ссылкой на необходимый адрес."""
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


# Я не работал ещё с платёжными системами.
# Регистрировать СЗ на том же YooMoney для тестового не стал.
# Очень быстро разберусь в работе.
@bot.message_handler(commands=['Кнопка_2'])
def pay_the_order(message):
    """Отправляем кнопку с ссылкой на оплату."""
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    button_address = types.InlineKeyboardButton(
        text='Оплатить',
        url=PAYMENT
    )
    keyboard.add(button_address)
    bot.send_message(
        chat_id=chat_id,
        text='Сумма заказа составляет 2 рубля.',
        reply_markup=keyboard
    )


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
    """Отправляем юзеру данные из Google Sheets."""
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text=take_value_from_google_sheets()
    )


@bot.message_handler(commands=['Кнопка_5'])
def send_validator_date(message):
    """Предлагаем юзеру ввести дату в определённом формате."""
    chat_id = message.chat.id
    remove_keyboard = types.ReplyKeyboardRemove()
    bot.send_message(
        chat_id=chat_id,
        text='Введи любимую дату в формате:\n01.01.2001',
        reply_markup=remove_keyboard
    )


@bot.message_handler(content_types=['text'])
def check_user_date(message):
    """Проверяем формат введённой даты для сохранения в Google Sheets."""
    chat_id = message.chat.id
    name = message.chat.first_name
    user_date = message.text
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

    # Валидную дату сохраняем в Google Sheets
    if re.match(DATE_FORMAT, user_date):
        save_valid_date(user_date=user_date)
        bot.send_message(
            chat_id=chat_id,
            text='Дата успешно сохранена!',
            reply_markup=keyboard
        )
        logging.info(
            f'{name} с ID: {chat_id} добавил информацию в Google Sheets.'
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text=f'{name}, попробуй ввести дату именно такого формата:'
            '\ndd.mm.yyyy'
        )


def main():
    """Основная логика бота."""
    # Запускаем цикл с ловлей исключений
    # и логгированием ошибок.
    while True:
        try:
            bot.polling()
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)


if __name__ == '__main__':
    logging.info('Бот активирован.')
    main()
