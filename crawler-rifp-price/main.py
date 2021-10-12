#declare pacakge
import requests
import connection
import time

#declare global variable
_database = connection.database()

#execution
while True:
    _r = requests.get('https://api.moneyonchain.com/api/report/mocMainnet2/ProVsCollateral1yr')
    _data = _r.json()['values']
    _date_on_moc = _data[len(_data)-1]['time'][:10]
    _data_on_database = _database.check_date(_date_on_moc)
    print('running')
    print(_date_on_moc)
    if _data_on_database is  None :
        print('new data incoming!')
        _database.insert_price(_date_on_moc, _data[len(_data)-1]['BPro'], _data[len(_data)-1]['BTC'], _data[len(_data)-1]['Difference'])
    time.sleep(120)