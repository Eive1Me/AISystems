from time import sleep
from dotenv import load_dotenv
import telebot
import os
from deeppavlov import build_model, configs
from deeppavlov.core.common.file import read_json

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.AsyncTeleBot(token)

model_config = read_json('squad_ru_bert_infer.json')
model = build_model(configs.squad.squad_bert_infer, download=True)


# Обработка '/start' и '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет!")


#Обработка вопросов по тексту
@bot.message_handler(content_types=['text'])
def ask_question(message):
    bot.reply_to(message, model(['Школа это место для обучения.'], [f'{message.text}'])[0][0])


print("I\'m listening!")
while True:
    try:
        bot.infinity_polling()
    except Exception as error:
        print(error)
        sleep(15)
