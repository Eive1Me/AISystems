import telebot
import sys
import os
from dotenv import load_dotenv
from deeppavlov import build_model, configs
from deeppavlov.core.common.file import read_json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from googlesearch import search

print(sys.argv)
load_dotenv()
token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)

model_config = read_json('squad_ru_bert_infer.json')
model = build_model(model_config, download=True)
    

#Установка контекста
class Context:
    def __init__(self, c):
        self.c = c

    def set_context(self, arg):
        self.c = arg

    def get_context(self):
        return self.c
mess_context = Context('')
html_context = Context('')
with open('text.txt', 'r') as file:
    data = file.read().replace('\n', ' ')
file_context = Context(data)


answer = model([file_context.get_context()], [sys.argv[2]])
print(answer)
if answer[0][0].strip() and answer[2][0] > 500:
    bot.send_message(sys.argv[1], answer)
    #bot.reply_to(message, answer)
else:
    bot.send_message(sys.argv[1], "Не понял вопроса")


# # Возвращает аргумент из сообщения от телеграм-бота (/c <context> -- вернёт context)
# def extract_arg(arg):
#     if len(arg.split()) > 1:
#         return arg[arg.index(' '):]
#     else:
#         raise Exception


# #Считать файл заново
# @bot.message_handler(commands=['reload_file'])
# def reload_file(message):
#     with open('text.txt', 'r') as file:
#         data = file.read().replace('\n', ' ')
#     file_context.set_context(data)
#     bot.reply_to(message, 'Контекст установлен!')


# # Обработка '/parse'
# @bot.message_handler(commands=['parse'])
# def parse_html(message):
#     req = Request(extract_arg(message.text))
#     html_page = urlopen(req)
#     soup = BeautifulSoup(html_page, "html.parser")
#     html_text = soup.get_text()
#     html_context.set_context(html_text)
#     bot.reply_to(message, 'Контекст установлен!')


# # Обработка '/search'
# @bot.message_handler(commands=['search'])
# def search_for(message):
#     query = extract_arg(message.text)
#     for j in search(query, num=1, stop=1):
#         req = (j)
#     print(req)
#     html_page = urlopen(req)
#     soup = BeautifulSoup(html_page, "html.parser")
#     html_text = soup.get_text()
#     html_context.set_context(html_text)
#     bot.reply_to(message, 'Контекст установлен!')


# #Обработка вопросов по контексту со страницы
# @bot.message_handler(commands=['ask'])
# def ask_html(message):
#     bot.reply_to(message, 'Ответ: \n' + model([f'{html_context.get_context()}'], [f'{extract_arg(message.text)}'])[0][0])


# #Обработка установки нового контекста
# @bot.message_handler(commands=['c'])
# def set_main_context(message):
#     mess_context.set_context(extract_arg(message.text))
#     bot.reply_to(message, 'Контекст установлен!')


# #Обработка вопросов по новому контексту
# @bot.message_handler(commands=['q'])
# def ask_question(message):
#     bot.reply_to(message, 'Ответ: \n' + model([f'{mess_context.get_context()}'], [f'{extract_arg(message.text)}'])[0][0])


# #Обработка вопросов по тексту из файла
# @bot.message_handler(content_types=['text'])
# def ask_question(message):
#     bot.reply_to(message, 'Ответ: \n' + model([f'{file_context.get_context()}'], [f'{message.text}'])[0][0])


