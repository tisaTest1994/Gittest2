import pymysql.cursors
from Function.common_function import *


class sqlFunction:

    @staticmethod
    def connect_mysql(db, sql):
        account = get_json()['mysql']['account']
        password = get_json()['mysql']['password']
        host = get_json()['mysql']['host']
        port = get_json()['mysql']['port']
        connection = pymysql.connect(host=host, user=account, passwd=password, db=db, port=port, charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                return result

    # 获取quote值
    @staticmethod
    def get_crypto_quote(pair_type='middle', type='BTC', limit_time='2021-05-07 08:00:00'):
        sql = "select {} from quote where pair = '{}-USD' and purpose = 'Customer' and valid_until > '{}' limit 1;". \
            format(pair_type, type, limit_time)
        logger.info('sql命令是{}'.format(sql))
        quote = sqlFunction().connect_mysql('pricing', sql=sql)
        if 'None' not in str(quote):
            quote_number = str((str(quote).split("'"))[3])
            logger.info('{}的quote是{}'.format(type, quote_number))
            return quote_number
        else:
            assert False, '获取quote失败，返回{}'.format(str(quote))

    # 获取某个时间段数据
    @staticmethod
    def get_cfx_detail(end_time):
        start_time = datetime.utcfromtimestamp(end_time - 60).strftime("%Y-%m-%d %H:%M:%S")
        end_time = datetime.utcfromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")
        sql = "select * from book_detail where created_at >= '{}' and created_at < '{}';".format(start_time, end_time)
        info = sqlFunction().connect_mysql('hedging', sql=sql)
        if info is not None:
            return info
