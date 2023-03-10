import pymysql.cursors
from Function.api_common_function import *
from Function.log import *


class sqlFunction:

    @staticmethod
    def connect_mysql(db, sql, type=2):
        account = get_json()['mysql']['account']
        password = get_json()['mysql']['password']
        host = get_json()['mysql']['host']
        port = get_json()['mysql']['port']
        connection = pymysql.connect(host=host, user=account, passwd=password, db=db, port=port, charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                if type == 1:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()
                return result

    # 获取quote值
    @staticmethod
    def get_crypto_quote(type='BTC', day_time='20210617'):
        sql = "select middle from quote_{} where pair = '{}-USD' and purpose = 'Customer' limit 1;".format(day_time, type)
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
        if info is not None and '()' not in str(info):
            logger.info(info)
            return info

    # 根据时间获取第一层损益
    @staticmethod
    def get_one_floor(aggregation_no, book_id):
        sql = "select * from book_aggregation where aggregation_no='{}' and book_id={};".format(aggregation_no, book_id)
        info = sqlFunction().connect_mysql('hedging', sql=sql)
        if info is not None and '()' not in str(info):
            return info

    # 根据时间获取第二层损益
    @staticmethod
    def get_two_floor(transaction_id):
        sql = "select * from movement where transaction_id='{}';".format(transaction_id)
        info = sqlFunction().connect_mysql('wallet', sql=sql)
        if info is not None and '()' not in str(info):
            return info

    # 获取bybit利率
    @staticmethod
    def get_order_info(aggregation_no, book_id):
        sql = "select * from `order` where biz_id='{}';".format('{}:{}'.format(aggregation_no, book_id))
        info = sqlFunction().connect_mysql('cfxorder', sql=sql)
        if info is not None and '()' not in str(info):
            return info[0]

    # 获取当前middle汇率
    @staticmethod
    def get_now_quote(pair):
        utc = pytz.timezone('UTC')
        utc_zero = datetime.now(tz=utc).strftime("%Y%m%d")
        sql = "select middle from quote_{} where pair = '{}' and purpose = 'Customer' order by id desc limit 1;".format(utc_zero, pair)
        info = sqlFunction().connect_mysql('pricing', sql=sql)
        if info is not None and '()' not in str(info):
            return info[0]


