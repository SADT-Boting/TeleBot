import telebot
import json
import time
import requests


#получение токена бота
def getTOKEN(configFile):
    """Вернет токен бота из файла configFile."""
    data = None
    with open(configFile, 'r') as f:
        data = json.load(f)
    if 'TOKEN' not in data:
        raise KeyError
    return data['TOKEN']


#получение URL сервера с сообщениями
def getURL(configFile):
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
    print("Запуск")
    print("Введите путь до файла конфигурации: ")
    configFile = input()
    try:
        URL = getURL(configFile)
        TOKEN = getTOKEN(configFile)
    except KeyError:
        print("Проверьте файл конфигураций " + configFile)
        exit()
    print("Авторизация")
    bot = telebot.TeleBot(TOKEN)
    print("Работа")
    while True:
        try:
            messages = getNewMessages(URL)
        except Exception:
            print("Ошибка получения новых сообщений")
        else:
            print("Новых сообщений: ", len(messages))
            sendMessages(messages, bot)
        time.sleep(3)
    print("Конец")
