import pymysql
import requests
import pandas as pd


def load_data_rds(db_info):

    db = pymysql.connect(host='db-1.cecwsw8d7xh0.us-east-1.rds.amazonaws.com',
                         user='cris',
                         passwd='cris1988',
                         port=3306
                         )
    cursor = db.cursor()
    
    db_info['db_exists'] = cursor.execute("show databases like 'exchange'")
    try:
        cursor.execute('use exchange')        
    finally:
        db_info['tb_exists'] = cursor.execute("show tables like 'brl_usd'")
        db_info['records'] = cursor.execute("select count(*) from brl_usd")

    cursor.execute("select * from brl_usd")
    res = cursor.fetchall()
    print(res)

    cursor.execute("select count(*) from brl_usd")
    res2 = cursor.fetchall()
    print(res2)


    return db_info['records']

db_info = {}
print(load_data_rds(db_info))