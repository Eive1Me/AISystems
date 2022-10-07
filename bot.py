from time import sleep
from dotenv import load_dotenv
import telebot
import os
from deeppavlov import build_model, configs

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)

class Context:
    def __init__(self, c):
        self.c = c

    def set_context(self, arg):
        self.c = arg

    def get_context(self):
        return self.c

model = build_model(configs.squad.squad_bert_infer, download=True)
mess_context = Context('')
with open('data.txt', 'r') as file:
    data = file.read().replace('\n', ' ')
file_context = Context(data)


# Возвращает аргумент из сообщения от телеграм-бота (/c <context> -- вернёт context)
def extract_arg(arg):
    if len(arg.split()) > 1:
        return arg[arg.index(' '):]
    else:
        raise Exception


# Обработка '/start' и '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет!")


#Обработка установки нового контекста
@bot.message_handler(commands=['c'])
def set_main_context(message):
    mess_context.set_context(extract_arg(message.text))
    bot.reply_to(message, 'Контекст установлен!')


#Обработка вопросов по новому контексту
@bot.message_handler(commands=['q'])
def ask_question(message):
    bot.reply_to(message, model([f'{mess_context.get_context()}'], [f'{extract_arg(message.text)}'])[0][0])


#Обработка вопросов по тексту из файла
@bot.message_handler(content_types=['text'])
def ask_question(message):
    bot.reply_to(message, model([f'{file_context.get_context()}'], [f'{message.text}'])[0][0])


print("I\'m listening!")
while True:
    try:
        bot.infinity_polling()
    except Exception as error:
        print(error)
        sleep(15)
