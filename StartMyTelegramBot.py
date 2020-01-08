# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 07:32:12 2019

@author: ANANTA SRIKAR
"""
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import logging
import requests
markdown = "Markdown" 
tokens = [] 

def getTokens():
    fileManager = open('res/TOKENS.txt', 'r')  #make the file in such a way that token[0] is for news, token[1] for weather, token[2] for bot
    tokenText = fileManager.read()
    global tokens
    tokens = tokenText.split('\n')

def NewsFromBBC(): 

    main_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey={}".format(tokens[0])
    
    open_bbc_page = requests.get(main_url).json() 
    article = open_bbc_page["articles"] 

    results = [] 
    data = ''
      
    for ar in article: 
        results.append(ar['title']) 
          
    for i in range(len(results)): 
        # printing all trending news
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

def interact_with_members(update, context):
    chat_id = update.message.chat_id
    try:
        hrs = 13       #Enter hours after the last message for the bot to interact
        due = 3600*hrs #this is the time 

        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_once(notify, due, context=chat_id)
        context.chat_data['job'] = new_job

    except (IndexError, ValueError):
        pass #removing this causes indentation error

def notify(context):
    #Send the interaction message.
    job = context.job
    context.bot.send_message(job.context, text='Hey! Y so silent?')

def start(update, context):
    update.message.reply_text("Yeah, I'm still awake!! ;)")

def help(update, context):
    fileManager = open('res/bot_intro.txt', 'r')
    bot_intro = fileManager.read()
    update.message.reply_text(bot_intro)
    fileManager.close()

def welcome_member(update, context):
    for i in range (0, len(update.message.new_chat_members)):
        update.message.reply_text('Welcome to {} '.format(update.message.chat.title) + update.message.new_chat_members[i].mention_markdown(), parse_mode = markdown)

def goodbye_member(update, context):
    context.bot.send_message(update.message.left_chat_member.id, text = 'Goodbye ' + update.message.left_chat_member.name + '\nHope to see you back in The {} group ;)'.format(update.message.chat.title))

def kick_member(update, context):
    admins = context.bot.get_chat_administrators(update.message.chat.id)
    isUserAdmin = False
    isToBeKickedAdmin = False
    for i in range(0,len(admins)):
            if(admins[i].user.id == update.message.from_user.id):
                isUserAdmin = True
            if(admins[i].user.id == update.message.reply_to_message.from_user.id):
                isToBeKickedAdmin = True
            if(isUserAdmin and isToBeKickedAdmin):
                break
    if(isUserAdmin):
        if(not isToBeKickedAdmin):
            context.bot.kick_chat_member(update.message.chat.id, update.message.reply_to_message.from_user.id)
            update.message.reply_text("Kicked " + update.message.reply_to_message.from_user.mention_markdown(), parse_mode = markdown)
        else:
            update.message.reply_text("Cannot kick " +  update.message.reply_to_message.from_user.mention_markdown()+ " as they are administrators", parse_mode = markdown)

    else:
        update.message.reply_text("Sorry, you're not an Admin!")

def messages(update, context):
    if(update.message.text.startswith('#weatherUpdate')):
        city = update.message.text[15:]
        update.message.reply_text(return_weather(city))
    
    elif(update.message.text.startswith('#intNews')):
        update.message.reply_text(NewsFromBBC())
    
    elif(update.message.text.startswith('#indNews')):
        update.message.reply_text(indianNews())
    
    elif(update.message.text.startswith('#admins')):
        admins = context.bot.get_chat_administrators(update.message.chat.id)
        adminText = 'The admins of {} are :\n'.format(update.message.chat.title)
        for i in range (0, len(admins)):
            adminText = adminText + admins[i].user.mention_markdown() + '\n'
        update.message.reply_text(adminText, parse_mode = markdown)

    elif(update.message.text.startswith('#members')):
        update.message.reply_text("Sorry, my API doesn't allow that. But I can tell you the total no of members : {}".format(context.bot.get_chat_members_count(update.message.chat.id)))
    
    if (update.message.text.lower().startswith('hey') or update.message.text.lower().startswith('hi') or update.message.text.lower().startswith('sup')):
        update.message.reply_text('Wassup ' + update.message.from_user.mention_markdown(), parse_mode = markdown)
    
    elif (update.message.text.lower().startswith('gn')):
        update.message.reply_text('Good Night ' + update.message.from_user.mention_markdown(), parse_mode = markdown)

    elif ('ok boomer' in update.message.text.lower() or 'boomer' in update.message.text.lower()):
        context.bot.send_photo(update.message.chat.id, photo = open('res/ok_boomer.jpg', 'rb'), reply_to_message_id = update.message.message_id)
    
    interact_with_members(update, context)

def main():
    getTokens()

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater = Updater(token = tokens[2], use_context = True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('kick', kick_member))
    dispatcher.add_handler(MessageHandler(Filters.text, messages))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_member))
    dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, goodbye_member))
    
    updater.start_polling() # starts the bot
    updater.idle() # stops the bot gracefully when KeyboadInterrupt is encountered
    
    # TODO : bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING) - Bot is typing
    # TODO : add timed messages when nobody is chatting
    # TODO : mute certain members

if __name__ == '__main__':
    main()