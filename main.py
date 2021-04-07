#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from bs4 import BeautifulSoup
import configparser
import logging
import requests
import datetime

from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Initial bot by Telegram access token
Token = (config['TELEGRAM']['ACCESS_TOKEN'])
#bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('/stock -> 標的')
    update.message.reply_text('/news -> 新聞')
    update.message.reply_text('/drgon -> 飛哥報名牌')


def createKeyBoardBtn(title, titles, hrefs) -> None:
    arr = []
    print(len(titles))
    for i in range(len(titles)):
        arr.append( InlineKeyboardButton(titles[i], url=hrefs[i]))
    update.message.reply_text( title,reply_markup = InlineKeyboardMarkup([arr]))
    #return InlineKeyboardMarkup([arr])
    
def upPageUrl(soup):
    upBtns = soup.findAll("a", class_="btn wide")
    for i in upBtns:
        if(  "上頁" in i.getText()):     
            print(i.get('href'))
            return i.get('href')

# type = date or month
def todayis(type):
    x = datetime.datetime.now()
    if (type == "date"):
        return x.strftime('%d')
    elif (type == "month"):
        return x.strftime('%m')



uripath = "/bbs/Stock/index.html"
website = "https://www.ptt.cc"
def getStockNews(mode) -> None:
    payload = {'from': uripath, 'yes': 'yes'}
    rs = requests.session()
    res = rs.get(website+uripath)
    soup = BeautifulSoup(res.text, features="html.parser")
    authors = soup.findAll("div", class_="author")
    titles = []
    hrefs = []
    if mode == "drgon":
        drgon = soup.find(text='drgon')
        if drgon:
            dr = drgon.find_parent("div").find_parent("div", class_="meta").find_previous_siblings("div")
            for ti in alltitles:
                hrefs.append(ti.find("a").get("href"))
                titles.append(ti.find("a").getText())
        #drLink = dr.find("a").get("href")
        #drTitle = dr.find("a").getText()
        return ("Drgon", titles , hrefs)
    if mode == "target":
        alltitles = soup.findAll("div", class_="title")
        resTitle = ""
        for ti in alltitles:
            if("標的" in ti.getText()):
                hrefs.append(ti.find("a").get("href"))
                titles.append(ti.find("a").getText())
        print(titles)
        return ("PPT STOCK", titles, hrefs)
    if mode == "news":
        alltitles = soup.findAll("div", class_="title")
        resTitle = ""
        for ti in alltitles:
            if("新聞" in ti.getText()):
                hrefs.append(ti.find("a").get("href"))
                titles.append(ti.find("a").getText())
        print(hrefs)
        return ("NEWS", titles, hrefs)
    pass


def stock_drgon(update: Update, _: CallbackContext) -> None:
    (title, titles, hrefs) = getStockNews("drgon")
    print (titles)
    #update.message.reply_text( 'PTT STOCK',reply_markup = news)
    #arr = []
    if len(titles) == 0:
         update.message.reply_text(' 飛哥還沒有報名牌')    
    for i in range(len(titles)):
        arr = []
        arr.append( InlineKeyboardButton(titles[i], url=website+hrefs[i]))
        update.message.reply_text( titles[i],reply_markup = InlineKeyboardMarkup([arr]))
    #return InlineKeyboardMarkup([arr])

def stock_target(update: Update, _: CallbackContext) -> None:
    (title, titles, hrefs) = getStockNews("target")
    #print (news)
    #update.message.reply_text( 'PTT STOCK',reply_markup = news)
    #arr = []
    if len(titles) == 0:
        update.message.reply_text('沒有最新標的')
    for i in range(len(titles)):
        arr = []
        arr.append( InlineKeyboardButton(titles[i], url=website+hrefs[i]))
        update.message.reply_text( titles[i],reply_markup = InlineKeyboardMarkup([arr]))
    #return InlineKeyboardMarkup([arr])

def stock_news(update: Update, _: CallbackContext) -> None:
    (title, titles, hrefs) = getStockNews("news")
    if len(titles) == 0:
        update.message.reply_text('沒有最新新聞')
    #arr = []
    print("----")
    #print (news)
    #print(KeyboardMarkup([[
    #        KeyboardButton('課程網站', url = 'https://github.com/mzshieh/pa19spring'),
    #        KeyboardButton('Documentation', url = 'https://python-telegram-bot.readthedocs.io/en/stable/index.html')]]))
    #update.message.reply_text( 'PTT STOCK',reply_markup = news)
    for i in range(len(titles)):
        arr = []
        print(titles[i])
        print(hrefs[i])
        arr.append( InlineKeyboardButton(titles[i], url=website+hrefs[i]))
        #arr.append( KeyboardButton(titles[i], url=website+hrefs[i]))
        update.message.reply_text( titles[i],reply_markup = InlineKeyboardMarkup([arr]))
    #update.message.reply_text( title,reply_markup = ReplyKeyboardMarkup([arr]))
    #return InlineKeyboardMarkup([arr])

def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    #stockNews = getStockNews("drgon")
    #print(stockNews) 
    user_id = update.message.from_user.id #(gets user’s id)
    user_name = update.message.from_user.name
    update.message.reply_text(str(user_id) + user_name)
    #update.message.reply_text(update.message.text)
    

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(Token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("stock", stock_target))
    dispatcher.add_handler(CommandHandler("news", stock_news))
    dispatcher.add_handler(CommandHandler("drgon", stock_drgon))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
