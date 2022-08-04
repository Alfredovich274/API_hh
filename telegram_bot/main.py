import telebot
import requests
import os
import time
import speech_recognition as sr
import subprocess
import xml.etree.ElementTree as ET


def recognition_voice(telegram_voice):
    # OGG в WAV
    subprocess.run(['ffmpeg', '-i', telegram_voice, 'voice.wav'])
    # Создаем объект распознавания речи
    store = sr.Recognizer()
    # Открываем файл для распознавания
    voice = open("voice.wav", "rb")
    with sr.AudioFile(voice) as source:
        audio_input = store.record(source)
    # Получаем текст из аудио
    try:
        text_output = store.recognize_google(audio_input, language='ru')
    except ValueError:
        return 'Не понятно'
    # Удаляем файл
    if os.path.exists('voice.wav'):
        os.remove('voice.wav')
    return text_output


def wood_if(message_list):
    result = []
    anchors = {
        'turn_on': ['включить', 'поставить', 'засечь', 'включи', 'поставь',
                    'засеки'],
        'turn_off': ['выключи', 'отключи', 'убери', 'выключить', 'отключить',
                     'убрать', 'отмени', 'отменить'],
        'timer': ['таймер', 'будильник'],
        'save': ['сохранить', 'сохрани', 'записать', 'запиши', 'заметка',
                 'хранить'],
        'show': ['показать', 'покажи', 'выведи', 'сколько'],
        'time': ['время', 'часы', 'времени'],
        'currency': ['курс', 'валют', 'валюты']
        }
    for message_word in message_list[:4]:
        message_word = message_word.lower()
        for anchor, words in anchors.items():
            if message_word in words:
                result.append(anchor)
    return result


def timer_val(message):
    time_size = {
        '0': ['сек', 'секунд', 'секунды', 'секунду'],
        '60': ['мин', 'минут', 'минуту', 'минуты'],
        '3600': ['час', 'часа', 'часов']
    }
    value_timer = {
        '1': 'одну',
        '2': 'два',
        '3': 'три',
        '4': 'четыре',
        '5': 'пять',
        '6': 'шесть',
        '7': 'семь',
        '8': 'восемь',
        '9': 'девять'
    }
    message = message.split(' ')
    time_timer = []
    for i, val in enumerate(message):
        try:
            time_timer.append(int(val))
        except ValueError:
            for number, val_time in value_timer.items():
                if val_time in val:
                    time_timer.append(int(number))
        if time_timer:
            if i <= len(message) - 2:
                for size, value in time_size.items():
                    if message[i + 1] in value:
                        time_timer.append(int(size))
    if not time_timer:
        for val in message:
            try:
                if ':' in val:
                    time_timer.append(val)
            except ValueError:
                pass
    return time_timer


def timer_on(value_timer):
    time_sec = value_timer[0]
    if value_timer[1] != 0:
        time_sec = value_timer[0] * value_timer[1]
    for i in range(time_sec):
        time.sleep(1)


# Переменные
src_filename = 'voice.ogg'
TOKEN = '1349274107:AAFTUG3mCNGcXvTIy5M4uWAkn87WfQhf7tk'
bot = telebot.TeleBot(TOKEN)
url_sbr = 'http://www.cbr.ru/scripts/XML_daily.asp'


@bot.message_handler(content_types=['voice'])
def reverse_text(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/'
                        'file/bot{0}/{1}'.format(TOKEN,
                                                 file_info.file_path))
    with open('voice.ogg', 'wb') as f:
        f.write(file.content)
    voice_text = recognition_voice(src_filename)
    # print(voice_text)
    menu = wood_if(str(voice_text).split(' '))
    if 'timer' in menu:
        if 'turn_on' in menu:
            if len(timer_val(voice_text)) == 1:
                bot.send_message(message.chat.id, f'Простите, но будильник'
                                                  f' ставить пока не умею')
            elif len(timer_val(voice_text)) == 2:
                data_time = timer_val(voice_text)
                bot.send_message(message.chat.id, f'Засекаю '
                f'{data_time[0]} {"секунд" if data_time[1] == 0 else "минут"}')
                timer_on(data_time)
                bot.send_message(message.chat.id, f'Время')
    elif 'save' in menu:
        voice_text = voice_text.split(' ')
        voice_text = ' '.join(voice_text[1:])
        bot.send_message(message.chat.id, f'{voice_text}')
    elif 'show' in menu:
        if 'time' in menu:
            bot.send_message(message.chat.id, f'{time.ctime()}')
        elif 'currency' in menu:
            curr = requests.get(url_sbr).text
            currency = ET.fromstring(curr)
            usd = f'{currency[10][3].text}-{currency[10][4].text}'
            eur = f'{currency[11][3].text}-{currency[11][4].text}'
            bot.send_message(message.chat.id, f'Курс на сегодня\n{usd}\n{eur}')
    else:
        bot.send_message(message.chat.id, f'Простите, пока нет такой команды')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Приветствую тебя, пользователь!")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "У меня есть голосовой помощник, но его действия "
                          "ограничены.\nСкажи: Включить таймер на 5 минут\nИли:"
                          " показать время\nМожет: курс валют\nМожешь сказать "
                          "'записать' или 'сохранить врепеди фразы и бот "
                          "сохранит твои слова'")


bot.polling()
