#declare package
import requests
import connection

#declare global variable
_database = connection.database()

#functions global get covalent api response
def get_response_api_covalent(url):
    r = requests.get(url)
    return r.json()['data']['items']

def get_response_api_covalent_price(url):
    r = requests.get(url)
    return r.json()['data'][0]['prices']