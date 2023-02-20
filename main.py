import pymysql
import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

#fetch api data and transform json file in DataFrame
def fetch_api_data (url):

    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['value'])

    os.system("echo '----> fetch data API'")

    return df

#load data function
def load_data_rds(df):
    
    #load environment variables .env
    load_dotenv()  
    host_rds = os.getenv("RDS_HOST").strip()
    pwd_rds = os.getenv("RDS_PASSWORD").strip()
    usr_rds = os.getenv("RDS_USER").strip()

    #connect to RDS
    db = pymysql.connect(host=host_rds,
                         user=usr_rds,
                         passwd=pwd_rds,
                         port=3306
                         )

    cursor = db.cursor()

    #checks if the database exists in RDS and
    #create the database if it does not exist
    db_exists = cursor.execute("show databases like 'exchange'") 
    if (db_exists == 0):
        create_db(cursor)
        
    #use database 'banks' 
    cursor.execute('use exchange')

    #checks if the table exists in database
    #create the table if it does not exist
    tb_exists = cursor.execute("show tables like 'brl_usd'")
    if (tb_exists == 0):
        create_tb(cursor)

    #insert data into table
    insert_tb(cursor, db)

    return

#Create database exchange
def create_db(cursor):
    cursor.execute('create database exchange')
    cursor.connection.commit()

    os.system("echo '----> created new database'")
    return

#Create table brl_usd
def create_tb(cursor):
    cursor.execute('''
        create table brl_usd (
        paridadeCompra FLOAT,
        paridadeVenda FLOAT,
        cotacaoCompra FLOAT,
        cotacaoVenda FLOAT,
        dataHoraCotacao VARCHAR (30),
        tipoBoletim VARCHAR (50)       
        )
        ''')

    os.system("echo '----> created new table'")
    return

#Insert dataframe data into brl_usd table 
def insert_tb(cursor, db):
    for index, row in df.iterrows():
        sql = '''
        insert into brl_usd(paridadeCompra, 
                            paridadeVenda, 
                            cotacaoCompra, 
                            cotacaoVenda, 
                            dataHoraCotacao, 
                            tipoBoletim)\
             values('%f', '%f', '%f', '%f', '%s', '%s')''' % (
                row.paridadeCompra, 
                row.paridadeVenda, 
                row.cotacaoCompra, 
                row.cotacaoVenda, 
                row.dataHoraCotacao,
                row.tipoBoletim) 
        
        cursor.execute(sql)
        db.commit()
        cursor.close

    os.system("echo '----> inserted new record'")
    return



if __name__ == "__main__":
    
    #tday = datetime.now().strftime("%m-%d-%Y")
    tday = '02-16-2023'

    url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda='USD'&@dataCotacao='{}'&$top=100&$format=json&$select=paridadeCompra,paridadeVenda,cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim".format(tday)
    df = fetch_api_data(url)
    load_data_rds(df)
    os.system("echo '----> Process completed'")