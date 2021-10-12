#import package
import connection
import utils
from dotenv import load_dotenv
import os
import time
import math
from datetime import datetime

#run dotenv
load_dotenv()

#declare global variables
starting_block = 3478616 #july 1 2021 00:00:00
ending_block = starting_block + 500 # crawling every 500 block
url_contract_address_events = 'https://api.covalenthq.com/v1/{chain_id}/events/address/{address}/?key={api_key}&starting-block={starting_block}&ending-block={ending_block}&limit=9999'
url_transaction = 'https://api.covalenthq.com/v1/{chain_id}/transaction_v2/{tx_hash}/?key={api_key}'
url_get_a_block = 'https://api.covalenthq.com/v1/{chain_id}/block_v2/{block_height}/?key={api_key}'
url_get_price = 'https://api.covalenthq.com/v1/pricing/historical_by_addresses_v2/{chain_id}/{quote_currency}/{contract_addresses}/?key={api_key}&from={fromDate}&to={toDate}'
API_KEY = os.getenv('COVALENT_API_KEY')
contract_address_babelfish = '0x1440d19436bEeaF8517896bffB957a88EC95a00F'
wbnb_contract_address = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
eth_contract_address = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
_database = connection.database()

while True:
    try :
        _get_date_transaction = utils.get_response_api_covalent(url_get_a_block.format(chain_id=30, block_height=starting_block, api_key=API_KEY))
        time.sleep(1)
        date_now = datetime.today().strftime('%Y-%m-%d')
        print(datetime.now())
        if date_now != _get_date_transaction[0]['signed_at'][:10] :
            _d = utils.get_response_api_covalent(url_contract_address_events.format(chain_id=30, address=contract_address_babelfish, api_key=API_KEY, starting_block=starting_block, ending_block=ending_block))
            _unique_tx = set((d['tx_hash'] for d in _d))
            for i in _unique_tx:
                print('running!')
                _t = utils.get_response_api_covalent(url_transaction.format(chain_id=30, tx_hash=i, api_key=API_KEY))
                if len(_t[0]['log_events']) == 11:
                    _date = _get_date_transaction[0]['signed_at'][:10]
                    _price = _database.get_bpro_price(_date)
                    trader = _t[0]['from_address']
                    from_token = _t[0]['log_events'][1]['sender_contract_ticker_symbol']
                    from_value = int(_t[0]['log_events'][1]['decoded']['params'][2]['value'])/math.pow(10, int(_t[0]['log_events'][1]['sender_contract_decimals']))
                    to_token = _t[0]['log_events'][len(_t[0]['log_events'])-1]['sender_contract_ticker_symbol']
                    to_value = int(_t[0]['log_events'][len(_t[0]['log_events'])-1]['decoded']['params'][2]['value'])/math.pow(10, int(_t[0]['log_events'][len(_t[0]['log_events'])-1]['sender_contract_decimals']))
                    collected_fee = int(_t[0]['log_events'][5]['decoded']['params'][2]['value'])/math.pow(10,18)
                    gas_fee = (int(_t[0]['gas_price'])/math.pow(10,18))*int(_t[0]['gas_spent'])*float(_price['btc'])
                    if from_token != 'XUSD':
                        if 'BNB' in from_token:
                            _price_other_token = utils.get_response_api_covalent(url_get_price.format(chain_id=56, quote_currency='usd', contract_addresses=wbnb_contract_address, api_key=API_KEY, fromDate=_date, toDate=_date))
                        else :
                            _price_other_token = utils.get_response_api_covalent(url_get_price.format(chain_id=1, quote_currency='usd', contract_addresses=eth_contract_address, api_key=API_KEY, fromDate=_date, toDate=_date))
                        amount = from_value*_price_other_token[0]['price']
                        _database.insert_data(i, _date, from_token, from_value, to_token, to_value, collected_fee, trader, amount, gas_fee)
                    else :
                        _database.insert_data(i, _date, from_token, from_value, to_token, to_value, collected_fee, trader, from_value, gas_fee)
                    print('new Data!')
                time.sleep(2)
            starting_block = ending_block
            ending_block = starting_block + 500
        else:
            print('not now sorry!')
    except Exception as e:
        print(e)
        print('Oops something went wrong!')
        continue