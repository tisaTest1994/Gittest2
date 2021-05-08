from run import *
from Function.log import *
from decimal import *
import time


class AccountFunction:

    # 获取用户token
    @staticmethod
    def get_account_token(account, password):
        data = {
            "username": account,
            "password": password
        }
        r = session.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                            headers=headers, timeout=3)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'accessToken' in r.text, "成功注册用户错误，返回值是{}".format(r.json())
        return r.json()

    # 注册
    @staticmethod
    def sign_up(account='', password='Zcdsw123'):
        citizenCountryCode = random.choice(citizenCountryCodeList)
        data = {
            "emailAddress": account,
            "verificationCode": "666666",
            "citizenCountryCode": citizenCountryCode,
            "password": password
        }
        session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers,
                        timeout=3)

    # 提现获取交易id
    @staticmethod
    def get_payout_transaction_id(account=email['email'], password=email['password'], amount='0.0007',
                                  address='0x428DA40C585514022b2eB537950d5AB5C7365a07'):
        accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        data = {
            "amount": amount,
            "code": "ETH",
            "address": address,
            "method": "ERC20"
        }
        r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data),
                            headers=headers)
        logger.info('获取的交易订单json是{}'.format(r.text))
        return r.json()['transaction_id']

    # 获取下次清算金额
    @staticmethod
    def get_interest(productId, account=email['email'], password=email['password']):
        accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        r1 = session.request('GET', url='{}/earn/products/{}/next_yield'.format(env_url, productId), headers=headers)
        return r1.json()['next_yield']

    # 获取换汇报价
    @staticmethod
    def get_quote(pair):
        cryptos = pair.split('-')
        r1 = session.request('GET',
                             url='{}/core/quotes/{}'.format(env_url, "{}-{}".format(cryptos[0], cryptos[1])),
                             headers=headers)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(r1.json()['valid_until'])))
        logger.info('获得报价的服务器时间是{}'.format(strTime))
        return r1.json()

    # 获取钱包指定币种数量
    @staticmethod
    def get_crypto_number(type='BTC', account=email['email'], password=email['password']):
        accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        r = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
        for i in r.json():
            if i['code'] == type and i['wallet_type'] == 'BALANCE':
                for y in i['balances']:
                    if y['type'] == 'BALANCE_TYPE_AVAILABLE':
                        balance_type_available_amount = y['amount']
        return balance_type_available_amount

    # 获取当前某个币的当前资产价值，用USD结算
    @staticmethod
    def get_crypto_abs_amount(type='BTC', account=email['email'], password=email['password']):
        accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        for i in r.json()['wallets']:
            if i['code'] == type:
                return i['abs_amount']

    # 获取quote值
    @staticmethod
    def get_crypto_quote(type='BTC', open_time='20210506'):
        if type == 'EUR':
            sql = "select quote from customer_quote_stat where pair='USDEUR' and open_time='{}';".format(open_time)
        else:
            sql = "select quote from customer_quote_stat where pair='{}USD' and open_time='{}';".format(type, open_time)
        logger.info('sql命令是{}'.format(sql))
        quote = connect_mysql('marketstat', sql=sql)
        if 'None' not in str(quote):
            print(str(quote).split("'"))
            quote_number = str((str(quote).split("'"))[3])
            if type == 'EUR':
                quote_number = 1 / float(quote_number)
            logger.info('{}的quote是{}'.format(type, quote_number))
            return quote_number
        else:
            assert False, '获取quote失败，返回{}'.format(str(quote))

    # 获得今日损益
    @staticmethod
    def get_today_increase(type='BTC', account=email['email'], password=email['password']):
        # 获取本日utc0点
        utc_zero = get_zero_utc_time()
        accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        # "获得现在数量币数量"
        number = AccountFunction.get_crypto_number(type=type)
        data = {
            "pagination_request": {
                "cursor": "0",
                "page_size": 9999999
            },
            "user_txn_sub_types": [1, 2, 4, 6],
            "statuses": [2],
            "codes": [type]
        }
        r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers,
                            timeout=10)
        for y in r.json()['transactions']:
            if y['created_at'] >= utc_zero:
                if y['user_txn_sub_type'] == 1:
                    number = float(number) - float(json.loads(y['details'])['currency']['amount'])
                elif y['user_txn_sub_type'] == 2 and json.loads(y['details'])['but_currency']['code'] == type:
                    number = float(number) - float(json.loads(y['details'])['but_currency']['amount'])
                elif y['user_txn_sub_type'] == 2 and json.loads(y['details'])['sell_currency']['code'] == type:
                    number = float(number) + float(json.loads(y['details'])['but_currency']['amount'])
                elif y['user_txn_sub_type'] == 4:
                    number = float(number) - float(json.loads(y['details'])['currency']['amount'])
                elif y['user_txn_sub_type'] == 6:
                    number = float(number) + float(json.loads(y['details'])['currency']['amount'])
        # 获取昨天UTC23:59的价格
        yesterday_time = datetime.datetime.now(tz=pytz.timezone('UTC')).strftime("%Y%m%d") + '0000'
        quote = AccountFunction.get_crypto_quote(type=type, open_time=yesterday_time)
        yesterday_amount = (Decimal(number) * Decimal(quote)).quantize(Decimal('0.00'), ROUND_FLOOR)
        # 获得当前价格
        now_amount = AccountFunction.get_crypto_abs_amount(type=type, account=account, password=password)
        today_increase = (Decimal(now_amount) - Decimal(yesterday_amount)).quantize(Decimal('0.00'), ROUND_FLOOR)
        return str(today_increase)

