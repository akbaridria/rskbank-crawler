#declare pacakage
import pymysql
from pymysql.constants import CLIENT
from dotenv import load_dotenv
import os

#run dotenv
load_dotenv()

#database class
class database :

    def __init__(self) :
        self.user = os.getenv('DATABASE_USER')
        self.password = os.getenv('DATABASE_PASSWORD')
        self.host = os.getenv('DATABASE_HOST') 
        self.db_name = os.getenv('DATABASE_NAME')

    def mysqlconnect(self):
        conn = pymysql.connect(
            host=self.host,
            user=self.user, 
            password=self.password,
            db=self.db_name,
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
            client_flag=CLIENT.MULTI_STATEMENTS
            )
        return conn
    
    def get_bpro_price(self, date):
        conn = self.mysqlconnect()
        cur = conn.cursor()
        query_sql = 'SELECT * FROM brpo_price WHERE date= "{date}"'.format(date = date)
        cur.execute(query_sql)
        _r = cur.fetchone()
        return _r

    def insert_data(self, tx_hash, date, from_token, from_value, to_token, to_value, fee, address, amount, gas_fee):
        conn = self.mysqlconnect()
        cur = conn.cursor()
        query_sql = 'INSERT IGNORE INTO sov_bridge VALUES("{tx_hash}", "{date}", "{from_token}", "{from_value}", "{to_token}", "{to_value}", "{fee}", "{address}", "{amount}", "{gas_fee}")'
        cur.execute(query_sql.format(tx_hash=tx_hash, date=date, from_token=from_token, from_value=from_value, to_token=to_token, to_value=to_value, fee=fee, address=address, amount=amount, gas_fee=gas_fee ))
        return True