#declare pacakage
import pymysql.cursors
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
    
    def insert_mint_or_redeem(self, tx_hash, block, date, token_name, amount, amount_usd, type_event, trader, gas_fee):
        conn = self.mysqlconnect()
        cur = conn.cursor()
        query_sql = 'INSERT INTO moc_protocol_mint_redeem(tx_hash, block, date, token_name, amount, amount_usd, type_event, trader, gas_fee) VALUES("{tx_hash}", "{block}", "{date}", "{token_name}", "{amount}", "{amount_usd}", "{type_event}", "{trader}", "{gas_fee}")'
        cur.execute(query_sql.format(tx_hash=tx_hash, block=block, date=date, token_name=token_name, amount=amount, amount_usd=amount_usd, type_event=type_event, trader=trader, gas_fee=gas_fee ))
        return True
    
    def select_latest_block(self):
        conn = self.mysqlconnect()
        cur = conn.cursor()
        query_sql = 'SELECT block FROM moc_protocol_mint_redeem ORDER BY id DESC LIMIT 1'
        cur.execute(query_sql)
        _d = cur.fetchone()
        return _d