
import string
import random
import requests 
import html
import json
import telegram

config = json.load(open("config.json"))

def random_string(length=12):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    letters = lowercase + uppercase
    secret = ''.join(random.choice(letters) for i in range(length))
    return secret
def make_deposit(update,contex,secret_id):
    url = 'https://api.cryptapi.io/ltc/create/'
    nonce = random_string()
    invoice = secret_id
    callback = 'https://61193d3bc8c5.ngrok.io/verifypayment/?invoice={}&nonce={}'.format(invoice,nonce)
    address = 'MLZpq6QEdtbGfKdUQAMsERM94qpGJpQmrW'
    params = {'callback':callback,
              'address':address,'confirmations':1,'email':'tomibami2020@gmail.com',
              'post':1}
    req = requests.get(url,params=params)
    temp_dict = req.json()
    wallet_address = temp_dict['address_in']
    contex.bot.send_message(chat_id=update.effective_chat.id , text=config['messages']['deposit'].format(wallet_address),
                            parse_mode=telegram.ParseMode.MARKDOWN)
