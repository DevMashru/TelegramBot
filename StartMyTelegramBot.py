# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 19:44:55 2019

@author: ANANTA SRIKAR
"""
import telebot
import time
import requests

tokens = [] 

def getTokens():
    fileManager = open('res/TOKENS.txt', 'r')  #make the file in such a way that token[0] is for news, token[1] for weather, token[2] for bot
    tokenText = fileManager.read()
    global tokens
    tokens = tokenText.split('\n')

def NewsFromBBC(): 
    
    # BBC news api 
    main_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey={}".format(tokens[0])
  
    # fetching data in json format 
    open_bbc_page = requests.get(main_url).json() 
  
    # getting all articles in a string article 
    article = open_bbc_page["articles"] 

  
    # empty list which will  
    # contain all trending news 
    results = [] 
    data = ''
      
    for ar in article: 
        results.append(ar['title']) 
          
    for i in range(len(results)): 
          
        # printing all trending news 
        #print(i + 1, results[i])
        data = data + str(i+1) + ') ' + str(results[i]) + '\n'
    
    return data

def indianNews():
    
    main_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey={}".format(tokens[0])

    news = requests.get(main_url).json()

    article = news["articles"]

    results = [] 
    data = ''
      
    for ar in article: 
        results.append(ar['title']) 
          
    for i in range(len(results)): 
        data = data + str(i+1) + ') ' + str(results[i]) + '\n'
    
    return data

def return_weather(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city, tokens[1])

    res = requests.get(url)

    data = res.json()

    try :
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description']
        data = 'Weather in {} :\n'.format(city) + 'Temperature : {} °C\n'.format(temp) + 'Wind Speeds : {} m/s\n'.format(wind_speed) + 'Description : {}'.format(description)

    except KeyError :
        data = 'Please enter a valid city name'

    return data

getTokens()

bot = telebot.TeleBot(token=tokens[2])

@bot.message_handler(commands=['start']) # welcome message handler
def send_awake(message):
    bot.reply_to(message, "Yeah, I'm still awake!! ;)")

@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    fileManager = open('res/bot_intro.txt', 'r')
    bot_intro = fileManager.read()
    bot.reply_to(message, bot_intro)
    fileManager.close()

@bot.message_handler(commands = ['weatherUpdate']) # weatherUpdate command
def send_weather(message):
    city = message.text[15:]
    bot.reply_to(message, return_weather(city))

@bot.message_handler(commands = ['kick']) #To kick out a user
def kick_user(message):
    admins = bot.get_chat_administrators(message.chat.id)
    isUserAdmin = False
    isToBeKickedAdmin = False
    for i in range(0,len(admins)):
            if(admins[i].user.id == message.from_user.id):
                isUserAdmin = True
            if(admins[i].user.id == message.reply_to_message.from_user.id):
                isToBeKickedAdmin = True
            if(isUserAdmin and isToBeKickedAdmin):
                break
    if(isUserAdmin):
        if(not isToBeKickedAdmin):
            bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            bot.reply_to(message, "Kicked @" + message.reply_to_message.from_user.username)
        else:
            #bot.reply_to(message, "Cannot kick @" +  message.reply_to_message.from_user.dir() + " a they are administrators")
            print(dir(message.reply_to_message.from_user))
            print(message.reply_to_message.from_user.username)

    else:
        bot.reply_to(message, "Sorry, you're not an Admin!")

@bot.message_handler(func=lambda msg : msg.text is not None and '#' in msg.text) #special commands
def send_reply(message):
    if(message.text.startswith('#weatherUpdate')):
        city = message.text[15:]
        bot.reply_to(message, text = return_weather(city))

    elif(message.text.startswith('#intNews')):
        bot.reply_to(message, NewsFromBBC())
    
    elif(message.text.startswith('#indNews')):
        bot.reply_to(message, indianNews())

    elif(message.text.startswith('#admins')):
        admins = bot.get_chat_administrators(message.chat.id)
        adminNames = ''
        for i in range(0, len(admins)):
            adminNames = adminNames + '@' + admins[i].user.username + '\n'
        bot.reply_to(message, "Admins of " + message.chat.title + " are :\n" + adminNames)

@bot.message_handler(func = lambda msg : msg.text is not None) #general chatting with bot
def chat_with_user(message):
    #TODO : Do something here that saves the current time and works accordingly
    if (message.text.lower().startswith('hey') or message.text.lower().startswith('hi') or message.text.lower().startswith('sup')):
        if(message.from_user.username is not None):
            bot.reply_to(message, text = 'Wassup @' + message.from_user.username)
        else:
            bot.reply_to(message, text = 'Wassup ' + message.from_user.first_name)
    
    elif ('gn' in message.text.lower()):
        if (message.from_user.username is not None):
            bot.reply_to(message, text = 'Good Night @' + message.from_user.username + '!')
        else:
            bot.reply_to(message, text = 'Good Night ' + message.from_user.first_name + '!')
    
    elif ('ok boomer' in message.text.lower() or 'boomer' in message.text.lower()):
        bot.send_photo(message.chat.id, photo = open('res/ok_boomer.jpg', 'rb'), reply_to_message_id= message.message_id)

@bot.message_handler(content_types=['new_chat_members'])
def message_new_user(message):
    if (message.new_chat_member.username is not None):
        bot.reply_to(message, text = 'Welcome @' + str(message.new_chat_member.username))

    else:
        bot.reply_to(message, text = 'Welcome ' + message.new_chat_member.first_name)

@bot.message_handler(content_types = ["left_chat_member"])
def message_user_left(message):
    if (message.left_chat_member.username is not None):
        bot.send_message(message.left_chat_member.id, text = 'Goodbye ' + str(message.left_chat_member.username) + '\nHope to see you back in The {} group ;)'.format(message.chat.title))
    else:
        bot.send_message(message.left_chat_member.id, text = 'Goodbye ' + str(message.left_chat_member.first_name) + '\nHope to see you back in The {} group ;)'.format(message.chat.title))
  
while True:
    try:
        bot.polling(none_stop=True)
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(10)