import telebot
import requests
from telebot import types
from dotenv import load_dotenv
import os

### Load the .env file
load_dotenv()

token = os.getenv('BOT_TOKEN')
print(token)
api_key = os.getenv('WEATHER_API_KEY')

bot = telebot.TeleBot(token, parse_mode=None)
chats = {
    'chatId': {
        'city': 'Пермь',
        'awaitingForCity': True,
    }
}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chatId = message.chat.id
    if not chatId in chats:
        chats[chatId] = {
            'city': False,
            'awaitingForCity': False,
        }
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Город")
    item2=types.KeyboardButton("Погода")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    chatId = message.chat.id
    if chats[chatId]['awaitingForCity']:
        chats[chatId]['awaitingForCity'] = False
        chats[chatId]['city'] = message.text
        bot.send_message(chatId, 'Город сохранен')
    elif message.text=="Погода":
        if chats[chatId]['city']:
            getWeather(chatId)
        else:
            bot.send_message(chatId, 'Для начала укажите город')
    elif message.text=="Город":
        chats[chatId]['awaitingForCity'] = True
        bot.send_message(chatId, 'Укажите наименование города: ')

        

def getWeather(chatId):
    responseWeather = requests.get('https://api.weatherapi.com/v1/current.json?q={0}&key={1}'.format(chats[chatId]['city'], api_key)).json()
    if 'error' in responseWeather:
        return bot.send_message(chatId, 'Указанного города не существует, укажите другой!')
    temp = responseWeather['current']['temp_c']
    humididty = responseWeather['current']['humidity']
    cloud = responseWeather['current']['cloud']
    bot.send_message(chatId, f'Температура воздуха: {temp}\nВлажность: {humididty}%\nОблачность: {cloud}%')

bot.infinity_polling()