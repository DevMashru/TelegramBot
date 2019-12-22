from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
tokens = [] 

def getTokens():
    fileManager = open('res/TOKENS.txt', 'r')  #make the file in such a way that token[0] is for news, token[1] for weather, token[2] for bot
    tokenText = fileManager.read()
    global tokens
    tokens = tokenText.split('\n')
    
getTokens()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token = tokens[2], use_context = True)
dispatcher = updater.dispatcher

def start(update, context):
    update.message.reply_text("I'm a bot, please talk to me!")
start_handler = CommandHandler('start', start)

def help(update, context):
    fileManager = open('res/bot_intro.txt', 'r')
    bot_intro = fileManager.read()
    update.message.reply_text(bot_intro)
    fileManager.close()
help_handler = CommandHandler('help', help)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
updater.start_polling()