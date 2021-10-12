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
starting_block = 2988697 #july 1 2021 00:00:00
ending_block = starting_block + 500 # crawling every 500 block
url_contract_address_events = 'https://api.covalenthq.com/v1/{chain_id}/events/address/{address}/?key={api_key}&starting-block={starting_block}&ending-block={ending_block}&limit=100'
url_transaction = 'https://api.covalenthq.com/v1/{chain_id}/transaction_v2/{tx_hash}/?key={api_key}'
url_get_a_block = 'https://api.covalenthq.com/v1/{chain_id}/block_v2/{block_height}/?key={api_key}'
url_get_price = 'https://api.covalenthq.com/v1/pricing/historical_by_addresses_v2/{chain_id}/{quote_currency}/{contract_addresses}/?key={api_key}&from={fromDate}&to={toDate}'
API_KEY = os.getenv('COVALENT_API_KEY')
cointract_address_rsk_token_bridge = '0x9d11937E2179dC5270Aa86A3f8143232D6DA0E69'
_database = connection.database()

while True:
    try :
        _get_date_transaction = utils.get_response_api_covalent(url_get_a_block.format(chain_id=30, block_height=starting_block, api_key=API_KEY))
        time.sleep(1)
        date_now = datetime.today().strftime('%Y-%m-%d')
        if date_now != _get_date_transaction[0]['signed_at'][:10] :
            _d = utils.get_response_api_covalent(url_contract_address_events.format(chain_id=30, address=cointract_address_rsk_token_bridge, api_key=API_KEY, starting_block=starting_block, ending_block=ending_block))
            _unique_tx = set((d['tx_hash'] for d in _d))
            for i in _unique_tx:
                print('running!')
                _t = utils.get_response_api_covalent(url_transaction.format(chain_id=30, tx_hash=i, api_key=API_KEY))
                count_log = len(_t[0]['log_events'])
                params_1 = 1 if count_log == 8 else 3
                params_2 = 3 if count_log == 8 else 0
                if (count_log == 9 or count_log == 8) and _t[0]['log_events'][len(_t[0]['log_events'])-1]['decoded']['name'] != 'Voted':
                    print(i)
                    _date = _get_date_transaction[0]['signed_at'][:10]
                    _price = _database.get_bpro_price(_date)
                    trader = _t[0]['from_address']
                    from_token = _t[0]['log_events'][params_1]['sender_contract_ticker_symbol']
                    from_value = int(_t[0]['log_events'][params_1]['decoded']['params'][2]['value'])/math.pow(10, int(_t[0]['log_events'][params_1]['sender_contract_decimals']))
                    collected_fee = int(_t[0]['log_events'][params_2]['decoded']['params'][2]['value'])/math.pow(10, int(_t[0]['log_events'][params_2]['sender_contract_decimals']))
                    gas_fee = (int(_t[0]['gas_price'])/math.pow(10,18))*int(_t[0]['gas_spent'])*float(_price['btc'])
                    _database.insert_data(i, _date, from_token, float(from_value) + float(collected_fee), trader, gas_fee, collected_fee)
                time.sleep(2)
            starting_block = ending_block
            ending_block = starting_block + 500
        else:
            print('not now sorry!')
    except Exception as e:
        print(e)
        print('Oops something went wrong!')
        continue