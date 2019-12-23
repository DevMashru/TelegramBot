from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import logging
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

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token = tokens[2], use_context = True)
dispatcher = updater.dispatcher

def reply_to_message(update, context, message):
    context.bot.send_message(update.effective_chat.id, message, reply_to_message_id = update.message.message_id)

def start(update, context):
    update.message.reply_text("Yeah, I'm still awake!! ;)")

def help(update, context):
    fileManager = open('res/bot_intro.txt', 'r')
    bot_intro = fileManager.read()
    update.message.reply_text(bot_intro)
    fileManager.close()

def messages(update, context):
    if(update.message.text.startswith('#weatherUpdate')):
        city = update.message.text[15:]
        reply_to_message(update, context, return_weather(city))
    
    elif(update.message.text.startswith('#intNews')):
        reply_to_message(update, context, NewsFromBBC())
    
    elif(update.message.text.startswith('#indNews')):
        reply_to_message(update, context, indianNews())

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.text, messages))

updater.start_polling()