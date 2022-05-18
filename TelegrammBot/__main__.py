import telebot
import json
import time
import requests

configFile = 'configure.json'

#получение токена бота
def getTOKEN():
    data = None
    with open(configFile, 'r') as f:
        data = json.load(f)
    if 'TOKEN' not in data:
        raise KeyError
    return data['TOKEN']


#получение URL сервера с сообщениями
def getURL():
    data = None
    with open(configFile, 'r') as f:
        data = json.load(f)
    if 'URL' not in data:
        raise KeyError
    return data['URL']


#получение новых сообщений
def getNewMessages(URL):
    response = requests.get(URL+'/newMessagesTelegramm')
    if not response.ok:
        return None
    return response.json()


#рассылка сообщений
def sendMessages(messages, bot):
    print('New messages: ', len(messages))
    if len(messages) == 0:
        return
    for message in messages:
        if message['IdTarget'] == 0:
            continue
        idTraget = message['IdTarget']
        student = requests.post(getURL()+'/getStudentById', data={'Id':idTraget}).json()
        student = student['TelegrammId']
        bot.send_message(student, message['Text'])
        a = requests.post(getURL()+'/sendMessage', data={"Platform":"Telegramm", 'Id':message['Id']})


#################### ЛОГИКА БОТА #########################################
token = getTOKEN()
bot = telebot.TeleBot(token)

# ответ на команду start
# добавление пользователя в БД
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет. Давай познакомимся поближе. Напиши свое имя")
    bot.register_next_step_handler(message, registration_name_wrapper({'TelegrammId':message.chat.id}))

def registration_name_wrapper(user):
    def registration_name(message, user=user):
        name = message.text.capitalize()
        user['FName'] = name
        bot.send_message(message.chat.id, "Теперь фамилию")
        bot.register_next_step_handler(message, registration_surname_wrapper(user))
    return registration_name

def registration_surname_wrapper(user):
    def registration_surname(message, user=user):
        surname = message.text.capitalize()
        user['LName'] = surname
        bot.send_message(message.chat.id, "Теперь группу")
        bot.register_next_step_handler(message, registration_group_wrapper(user)) 
    return registration_surname

def registration_group_wrapper(user):
    def registration_group(message, user=user):
        group = message.text.upper()
        user['Group'] = group
        result = requests.post(getURL()+"/addTelegrammIdByName", data=user)
        if result.text != 'success':
            bot.send_message(message.chat.id, "Ой, что-то пошло не так. Перепроверь введенные данные")
        else:
            print(result.text)
            bot.send_message(message.chat.id, "Я тебя запомнил")
    return registration_group


# рассылка сообщений от сервера
@bot.message_handler()
def sendng_messages(message):
    messages = getNewMessages(getURL())
    if messages is None:
        return
    sendMessages(messages, bot)
    


print(f'starting on \nTOKEN:{getTOKEN()} \nURL:{getURL()}')
bot.polling()
    
