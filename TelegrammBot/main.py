import telebot
import json
import time
import requests

configFile = 'configure.json'
"""Название файла с конфигурацией"""

#получение токена бота
def getTOKEN():
    """Вернет токен бота из файла configFile."""
    data = None
    with open(configFile, 'r') as f:
        data = json.load(f)
    if 'TOKEN' not in data:
        raise KeyError
    return data['TOKEN']


#получение URL сервера с сообщениями
def getURL():
    """Вернет URL сервера с удаленной БД."""
    data = None
    with open(configFile, 'r') as f:
        data = json.load(f)
    if 'TOKEN' not in data:
        raise KeyError
    return data['URL']


#получение новых сообщений
def getNewMessages(URL):
    """
    Сделает запрос к удаленной бд для получения новых сообщений и вернет их.

    Аргументы:
    URL (str): url-адрес сервера
    """
    response = requests.get(URL+'/newMessages')
    if response.status_code != 200:
        raise Exception
    return response.json()


#рассылка сообщений
def sendMessages(messages, bot):
    """
    Отправит сообщения пользователям.

    Аргументы:
    messages (list): список сообщений
    bot (TeleBot): объект телеграмм-бота
    """
    if len(messages) == 0:
        return
    for mess in messages:
        if mess['TelegrammId'] == 0:
            continue
        bot.send_message(mess['TelegrammId'], mess['Text'])
    

if __name__ == "__main__":
    print("Starting")
    try:
        URL = getURL()
        TOKEN = getTOKEN()
    except KeyError:
        print("Проверьте файл конфигураций " + configFile)
        exit()
    print("Initialize")
    bot = telebot.TeleBot('%ваш токен%')
    print("Work")
    while True:
        try:
            messages = getNewMessages(URL)
        except Exception:
            print("Getting new messages error")
        else:
            sendMessages(messages, bot)
        time.sleep(3)
    print("End")
