from time import sleep
from dotenv import load_dotenv
import telebot
import os
import requests
from deeppavlov import build_model, train_model
from deeppavlov.core.common.file import read_json
from multiprocessing import Process, Queue

load_dotenv()
token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)


#Настройка моделей
intent_catcher_model_config = read_json('intent_catcher.json')


#Основная обработка сообщений
@bot.message_handler(content_types=['text'])
def get_text_message(message):
    queue.put(message.text)
    intent_result = queue.get()
    print("Сообщение:", message.text)
    print("Интент:", intent_result[0])

    if intent_result[0] == 'cqa':
        bot.reply_to(message, "Что вы хотите знать?")
        bot.register_next_step_handler(message,launch_cqa)
        print("1")
    elif intent_result[0] == 'start':
        send_welcome(message)
        print("2")
    elif intent_result[0] == 'cat':
        url = get_url()
        bot.send_photo(message.chat.id, url)
        print("3")
    else:
        bot.reply_to(message, "Я не понимаю, что Вы от меня хотите:(")


#Обработка запроса к cqa
def launch_cqa(message):
    messageText = message.text
    os.system("python cqa.py \"" + str(message.chat.id) + "\" " + "\"" + messageText + "\"")


#Тренировка модели
def work_with_intent_catcher_model(q):
    intent_catcher_model = build_model(intent_catcher_model_config)

    q.put(1)
    while True:
        q.put(intent_catcher_model([q.get()]))


# Возвращает аргумент из сообщения от телеграм-бота (/c <context> -- вернёт context)
def extract_arg(arg):
    if len(arg.split()) > 1:
        return arg[arg.index(' '):]
    else:
        raise Exception


# Обработка '/start' и '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "🌸 Привет! 🌸\n\n🧷 Говори, чем интересуешься, я со всем помогу.\n" + 
    "🧷 Я могу рассказать про то, что записано в файле, если хочешь (сейчас там про кфу). 👉👈 \n" + 
    "🧷 Ну, а если тебе совсем скучно могу отправить фоточки котиков!")


def get_url():
    contents = requests.get('https://aws.random.cat/meow').json()
    image_url = contents['file']
    return image_url


queue = Queue()
child_process = Process(target=work_with_intent_catcher_model, args=(queue,))
child_process.start()
queue.get()
print("I\'m listening!")
while True:
    try:
        bot.infinity_polling()
    except Exception as error:
        print(error)
        sleep(15)
