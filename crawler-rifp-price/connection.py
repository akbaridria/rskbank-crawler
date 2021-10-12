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

    def check_date(self, date):
        conn = self.mysqlconnect()
        cur = conn.cursor()
        query_sql = 'SELECT * FROM rif_price WHERE date="{date}"'
        cur.execute(query_sql.format(date=date))
        _d = cur.fetchone()
        return _d
    
    def insert_price(self, date, rifp, rif, diff):
        conn = self.mysqlconnect()
        cur = conn.cursor()
        query_sql = 'INSERT INTO rif_price VALUES("{date}", "{bpro}", "{btc}", "{diff}")'
        cur.execute(query_sql.format(date=date, rifp=rifp, rif=rif, diff=diff))
        return True