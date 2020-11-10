from flask import Flask 
from flask import request
from flask import Response
import json
import pymongo
app = Flask(__name__)

config = json.load(open("config.json"))
client = pymongo.MongoClient(config["db"]["host"], config["db"]["port"])
db = client[config["db"]["db_name"]]

@app.route('/verifypayment/',methods=['GET', 'POST'])
def verifypayment():
    queryStringDict = request.args
    invoice =  queryStringDict['invoice']
    nonce = queryStringDict['nonce']
    data = request.form
    if db.transactions.find_one({'nonce':nonce})==None:
        txid_in = data['txid_in']
        txid_out = data['txid_out']
        value = data['value']
        value_coin = data['value_coin']
        value_forwarded_coin = float(data['value_forwarded_coin'])
        coin = data['coin']
        db.transactions.insert_one({'invoice':invoice,'nonce':nonce,
                                    'txid_in':txid_in,'txid_out':txid_out,
                                    'value':value,'value_coin':value_coin,
                                    'value_forwarded_coin':value_forwarded_coin, 'coin':coin})
        db.users.update_one({'secret_id':invoice}, {"$inc":{'balance_ltc':value_forwarded_coin }})
        
    return Response(status=200)
@app.route('/')
def index():
    return '<h1>Hi there</h1>'

if __name__ == '__main__':
    app.run(debug=True)
 