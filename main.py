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
    if 'TOKEN' not in data:
        raise KeyError
    return data['URL']


#получение новых сообщений
def getNewMessages(URL):
    response = requests.get(URL+'/newMessages')
    if response.code != 200:
        raise Exception
    return response.json()


#рассылка сообщений
def sendMessages(messages, bot):
    if len(messages) == 0:
        return
    for mess in messages:
        if mess['TelegrammId'] == 0:
            continue
        bot.send_message(mess['TelegrammId'], mess['Text'])
    

if __name__ == "__main__":
    try:
        URL = getURL()
        TOKEN = getTOKEN()
    except KeyError:
        print("Проверьте файл конфигураций " + configFile)
        exit()

    bot = telebot.TeleBot('%ваш токен%')
    while True:
        try:
            messages = getNewMessages(URL)
        except Exception:
            pass
        else:
            sendMessages(messages, bot)
        time.sleep(300)
    
