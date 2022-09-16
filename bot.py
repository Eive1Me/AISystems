from time import sleep
from dotenv import load_dotenv
import telebot
import os

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)

# Обработка '/start' и '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет!")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as error:
        print(error)
        sleep(15)
