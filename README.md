# Telegram Chatbot
Made using [python-telegram-bot 12.2.0](https://pypi.org/project/python-telegram-bot/).
Still in development, hosted on my Raspberry Pi 4 ;)

# Functions:
* `/start` - To check if the bot is still working
* `/help`  - To find out what the bot can do 
* `/kick`  - Replying this command to a users message kick them out of the group (**Note** : U need to be an admin to kick them out)
* `#weatherUpdate cityName` - Gives the current weather in the city u input
* `#intNews` - Gives global news
* `#indNews` - Gives Indian news
* `#admins` - Replies with the list of admins in a group

Also wishes good night, and replies back when you initiate chat like "Hey" or "Hi"

Also has some small Easter eggs (try sending ok boomer)

# APIs
Below are the list of APIs used in the Telegram Bot:
* [python-telegram-bot 12.2.0](https://pypi.org/project/python-telegram-bot/) - The main API for the bot
* [News API](https://newsapi.org/) - API for latest news
* [OpenWeather](https://openweathermap.org/api) - API for latest weather
