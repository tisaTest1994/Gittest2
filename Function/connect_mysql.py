import pymysql.cursors
from Function.common_function import *


def connect_mysql(db, sql):
    account = get_json()['mysql']['account']
    password = get_json()['mysql']['password']
    host = get_json()['mysql']['host']
    port = get_json()['mysql']['port']
    connection = pymysql.connect(host=host, user=account, passwd=password, db=db, port=port, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
            return result