import pymysql
from Function.common_function import *


def connect_mysql():
    account = get_json()['mysql']['account']
    password = get_json()['mysql']['password']
    host = get_json()['mysql']['host']
    port = get_json()['mysql']['port']
    con = pymysql.connect(host=host, user=account, passwd=password, db='account', port=port, charset='utf8')
    print(con)