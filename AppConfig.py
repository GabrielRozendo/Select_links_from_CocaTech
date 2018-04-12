import configparser

appConfig = configparser.ConfigParser()
appConfig.read("App.ini")

def GetValue(section, option):
    return appConfig.get(section, option)

def GetConnectionURI():
    return GetValue("Connection", "uri")

def GetTelegramToken():
    return GetValue("Telegram", "BotToken")
