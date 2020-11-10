from telegram.ext import Updater
from telegram.ext import CommandHandler , MessageHandler, Filters , ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from utils import random_string, make_deposit

import json
import pymongo
import logging
import threading

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
config = json.load(open("config.json"))
client = pymongo.MongoClient(config["db"]["host"], config["db"]["port"])
db = client[config["db"]["db_name"]]

def start(update, contex):
    user_id = update.effective_chat.id
    
    if db.users.find_one({'user_id':user_id})==None:
        secret_id = random_string()
        first_name = update.message.chat.first_name
        last_name = update.message.chat.last_name
        username = update.message.chat.username
        reg_dict = {'user_id':user_id,'secret_id':secret_id,'username':username,
                    'first_name':first_name,'last_name':last_name,'balance_ltc':0.00000000}
        db.users.insert_one(reg_dict)
    
    user_query= db.users.find_one({'user_id':user_id})
    balance = "Balance {} LTC".format(user_query['balance_ltc'])
    keyboard = [[KeyboardButton(text=balance)],
                [KeyboardButton(text='📘 Deposit'),KeyboardButton(text='📕 Withdrawal')],
                [KeyboardButton(text='📗 Reinvest'),KeyboardButton(text='📚 Trasanctions')],
                [KeyboardButton(text='Team'),KeyboardButton(text='FAQ'),KeyboardButton(text='📞 Support')]
                ]
    update.message.reply_text(text=config['messages']['welcome'], reply_markup=ReplyKeyboardMarkup(keyboard))
    
def echo(update, contex):
    contex.bot.send_message(chat_id=update.effective_chat.id , text=update.message.text)

def deposit(update , contex):
    invoice = db.users.find_one({'user_id':update.effective_chat.id})
    secret_id = invoice['secret_id']
    thread = threading.Thread(target=make_deposit , args=[update,contex,secret_id])
    thread.start()
    
def main():
    updater = Updater(token='1455581354:AAGx1at9mgkAf-5YVJNRsvRB66AeZTenBwQ', use_context=True)
    dispatcher = updater.dispatcher
    
    deposit_handler = MessageHandler(Filters.regex('(Deposit|deposit|d)'), deposit)
    
    start_handler = CommandHandler('start', start)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(deposit_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()