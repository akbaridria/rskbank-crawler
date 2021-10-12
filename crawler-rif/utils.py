#declare package
import requests
import connection

#declare global variable
_database = connection.database()

#functions global get covalent api response
def get_response_api_covalent(url):
    r = requests.get(url)
    return r.json()['data']['items']

#process data to insert to database
def process_and_insert_data_moc(tx_hash, date, token_name, amount, amount_usd, from_address, to_address, gas_fee):
    if from_address == '0x0000000000000000000000000000000000000000' :
        type_event = 'mint'
        trader = to_address
    elif to_address == '0x0000000000000000000000000000000000000000':
        type_event = 'redeem'
        trader = from_address
    else:
        return True
    _database.insert_mint_or_redeem(tx_hash, date, token_name, amount, amount_usd, type_event, trader, gas_fee)
    return True