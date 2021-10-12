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
starting_block = 2988697
ending_block = starting_block + 500 # crawling every 500 block
url_contract_address_events = 'https://api.covalenthq.com/v1/{chain_id}/events/address/{address}/?key={api_key}&starting-block={starting_block}&ending-block={ending_block}'
url_transaction = 'https://api.covalenthq.com/v1/{chain_id}/transaction_v2/{tx_hash}/?key={api_key}'
url_get_a_block = 'https://api.covalenthq.com/v1/{chain_id}/block_v2/{block_height}/?key={api_key}'
API_KEY = os.getenv('COVALENT_API_KEY')
url_rif_exchange = '0x9497d2aECd0757dD4fCb4D5f2131293570FAd305'
_database = connection.database()

# crawler execution
while True:
    try:
        _get_date_transaction = utils.get_response_api_covalent(url_get_a_block.format(chain_id=30, block_height=starting_block, api_key=API_KEY))
        date_now = datetime.today().strftime('%Y-%m-%d')
        if date_now != _get_date_transaction[0]['signed_at'][:10] :
            _d = (utils.get_response_api_covalent(url_contract_address_events.format(chain_id=30, address=url_rif_exchange, api_key=API_KEY, starting_block=starting_block, ending_block=ending_block)))
            print(_d)
            for i in _d:
                _t = utils.get_response_api_covalent(url_transaction.format(chain_id=30, tx_hash=i['tx_hash'], api_key=API_KEY))
                for j in _t :
                    if j['successful'] == True:
                        gas_price = j['gas_quote']
                        tx_hash = i['tx_hash']
                        if j['log_events'][len(j['log_events'])-1]['decoded'] is not None:
                            if j['log_events'][len(j['log_events'])-1]['decoded']['name'] == 'Transfer':
                                token_name = j['log_events'][len(j['log_events'])-1]['sender_name']
                                from_address = j['log_events'][len(j['log_events'])-1]['decoded']['params'][0]['value']
                                to_address = j['log_events'][len(j['log_events'])-1]['decoded']['params'][1]['value']
                                amount = int(j['log_events'][len(j['log_events'])-1]['decoded']['params'][2]['value'])/math.pow(10, j['log_events'][len(j['log_events'])-1]['sender_contract_decimals'])
                                block_signed_at = j['log_events'][len(j['log_events'])-1]['block_signed_at'][:10]
                                _price =  _database.get_bpro_price(block_signed_at)
                                gas_fee = (int(j['gas_price'])/math.pow(10,18))*int(j['gas_spent'])*float(_price['btc'])
                                print(gas_fee)
                                if token_name == 'RIFPro':
                                    print(block_signed_at)
                                    _price_rifp = _database.get_rifp_price(block_signed_at)
                                    time.sleep(2)
                                    amount_usd = float(amount)*float(_price_rifp['rifp'])
                                    utils.process_and_insert_data_moc(tx_hash, block_signed_at, token_name, amount, amount_usd, from_address, to_address, gas_fee)
                                    time.sleep(2)
                                elif token_name == 'RIF Dollar on Chain':
                                    utils.process_and_insert_data_moc(tx_hash, block_signed_at, token_name, amount, amount, from_address, to_address, gas_fee)
                                    time.sleep(2)
                    time.sleep(2)
            starting_block = ending_block
            ending_block = ending_block + 500
    except Exception as e:
        print(e)
        print('oops something went wrong')
        continue

