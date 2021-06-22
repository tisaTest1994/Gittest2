import run
from run import *
from Function.log import *
from decimal import *
import time
import pyotp


class AccountFunction:

    # 获取用户token
    @staticmethod
    def get_account_token(account=email['email'], password=email['password']):
        data = {
            "username": account,
            "password": password
        }
        r = session.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                            headers=headers, timeout=100)
        return r.json()['accessToken']

    # 加headers，只能默认账户
    @staticmethod
    def add_headers(currency='USD'):
        run.accountToken = AccountFunction.get_account_token()
        headers['Authorization'] = "Bearer " + run.accountToken
        headers['X-Currency'] = currency

    # 获取operate用户 token
    @staticmethod
    def get_operate_account_token(account, password):
        data = {
            "username": account,
            "password": password
        }
        r = session.request('POST', url='{}/operator/operator/login'.format(env_url), data=json.dumps(data),
                            headers=headers, timeout=3)
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
                        timeout=10)

    # 提现获取交易id
    @staticmethod
    def get_payout_transaction_id(amount='0.03', address='0x428DA40C585514022b2eB537950d5AB5C7365a07'):
        requests.request('GET', url='{}/account/security/mfa/email/sendVerificationCode'.format(env_url),
                         headers=headers)
        sleep(40)
        email_info = get_email()
        assert '[Cabital] Confirm your email' == email_info['title'], '邮件验证码获取失败，获取的邮件标题是是{}'.format(
            email_info['title'])
        code = str(email_info['body']).split('"code":')[1].split('"')[1]
        secretKey = get_json()['secretKey']
        totp = pyotp.TOTP(secretKey)
        mfaVerificationCode = totp.now()
        headers['X-Mfa-Otp'] = str(mfaVerificationCode)
        headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['email'], code)
        data = {
            "amount": amount,
            "code": "ETH",
            "address": address,
            "method": "ERC20"
        }
        print(headers)
        r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data),
                            headers=headers)
        logger.info('获取的交易订单json是{}'.format(r.text))
        return r.json()['transaction_id']

    # 获取下次清算金额
    @staticmethod
    def get_interest(productId):
        r1 = session.request('GET', url='{}/earn/products/{}/next_yield'.format(env_url, productId), headers=headers)
        return r1.json()['next_yield']

    # 获取当前换汇报价
    @staticmethod
    def get_quote(pair):
        cryptos = pair.split('-')
        r1 = session.request('GET',
                             url='{}/core/quotes/{}'.format(env_url, "{}-{}".format(cryptos[0], cryptos[1])),
                             headers=headers)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(r1.json()['valid_until'])))
        logger.info('获得报价的服务器时间是{}'.format(strTime))
        return r1.json()

    # 获取钱包指定币种某个交易状态的数量
    @staticmethod
    def get_crypto_number(type='BTC', balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE'):
        r = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers, timeout=10)
        for i in r.json():
            if i['code'] == type and i['wallet_type'] == wallet_type:
                for y in i['balances']:
                    if y['type'] == balance_type:
                        balance_type_available_amount = y['amount']
        return balance_type_available_amount

    # 获取钱包指定币种全部数量
    @staticmethod
    def get_all_crypto_number():
        r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        crypto_list = get_json()['crypto_list']
        number_dict = {}
        for i in r.json()['wallets']:
            for y in crypto_list:
                if i['code'] == y:
                    number_dict[y] = i['amount']
        return number_dict

    # 获取当前某个币的当前资产价值，用USD结算
    @staticmethod
    def get_crypto_abs_amount(type='BTC'):
        r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        for i in r.json()['wallets']:
            if i['code'] == type:
                return i['abs_amount']

    # 获得今日损益
    @staticmethod
    def get_today_increase():
        crypto_list = get_json()['crypto_list']
        # 当前全部货币数量
        number_dict = AccountFunction.get_all_crypto_number()
        # 今天utc0点时间
        yesterday_time = datetime.now(tz=pytz.timezone('UTC')).strftime("%Y%m%d")
        today_increase = {}
        for i in crypto_list:
            # 目前货币数量
            number = number_dict[i]
            data = {
                "pagination_request": {
                    "cursor": "0",
                    "page_size": 99999
                },
                "user_txn_sub_types": [1, 2, 4, 6, 7],
                "statuses": [2],
                "codes": [i],
                "created_from": int(get_zero_utc_time())
            }
            r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers)
            for y in r.json()['transactions']:
                if y['user_txn_sub_type'] == 1:
                    number = float(number) - float(json.loads(y['details'])['currency']['amount'])
                elif y['user_txn_sub_type'] == 2 and json.loads(y['details'])['buy_currency']['code'] == i:
                    number = float(number) - float(json.loads(y['details'])['buy_currency']['amount'])
                elif y['user_txn_sub_type'] == 2 and json.loads(y['details'])['sell_currency']['code'] == i:
                    number = float(number) + float(json.loads(y['details'])['buy_currency']['amount'])
                elif y['user_txn_sub_type'] == 4:
                    number = float(number) - float(json.loads(y['details'])['currency']['amount'])
                elif y['user_txn_sub_type'] == 6:
                    number = float(number) + float(json.loads(y['details'])['currency']['amount'])
                    print(y)
                elif y['user_txn_sub_type'] == 7:
                    number = float(number) - float(json.loads(y['details'])['currency']['amount'])
            # 获取昨天UTC23:59的汇率价格
            quote = sqlFunction.get_crypto_quote(type=i, day_time=yesterday_time)
            yesterday_amount = (Decimal(number) * Decimal(quote)).quantize(Decimal('0.00'), ROUND_FLOOR)
            # 获得当前价格
            now_amount = AccountFunction.get_crypto_abs_amount(type=i)
            today_increase[i] = (Decimal(yesterday_amount) - Decimal(now_amount)).quantize(Decimal('0.00'), ROUND_FLOOR)
        return str(today_increase)

    # 获得总持仓成本
    @staticmethod
    def get_cost(type='ETH'):
        # 获得交易记录
        data = {
            "pagination_request": {
                "cursor": "0",
                "page_size": 9999999
            },
            "user_txn_sub_types": [1, 2, 6],
            "statuses": [2],
            "codes": [type]
        }
        r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers,
                            timeout=10)
        for y in r.json()['transactions']:
            cost = 0
            if y['user_txn_sub_type'] == 1:
                order_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(y['updated_at']))
            if y['user_txn_sub_type'] == 2:
                order_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(y['updated_at']))
            if y['user_txn_sub_type'] == 6:
                order_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(y['updated_at']))
                amount = json.loads(y['details'])['currency']['amount']

    # 查询交易状态
    @staticmethod
    def get_transaction_status(transaction_id, type):
        params = {
            'txn_sub_type': type
        }
        r = session.request('GET', url='{}/txn/{}'.format(env_url, transaction_id), params=params, headers=headers)
        return r.json()['transaction']['status']

    # 获取一天cfx数据
    @staticmethod
    def get_cfx_info(day_time='2021-05-26'):
        cfx_book = get_json()['cfx_book']
        time_list = get_zero_time(day_time=day_time)
        cfx_info = []
        for i in time_list:
            info = sqlFunction().get_cfx_detail(end_time=i)
            if info is not None and '()' not in str(info):
                cfx_info.append(info)
        cfx_list = []
        for y in cfx_info:
            for z in y:
                cfx_dict = {}
                if z['trading_direction'] == 1:
                    cfx_dict['buy_us'] = str(cfx_book[str(z['book_id'])]).split('-')[1]
                    cfx_dict['sell_us'] = str(cfx_book[str(z['book_id'])]).split('-')[0]
                    cfx_dict['buy_us_amount'] = z['pnl_amount']
                    cfx_dict['sell_us_amount'] = z['trading_amount']
                    cfx_dict['profit'] = z['gnl']
                    cfx_dict['order_time'] = z['aggregation_no']
                    profit = Decimal(z['trading_amount']) * Decimal(z['cost'])
                    if str(cfx_book[str(z['book_id'])]).split('-')[1] == 'BTC' or \
                            str(cfx_book[str(z['book_id'])]).split('-')[1] == 'ETH':
                        profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:8])
                    elif str(cfx_book[str(z['book_id'])]).split('-')[1] == 'USDT':
                        profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
                    else:
                        profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:2])
                    profit = Decimal(profit) - Decimal(z['pnl_amount'])
                    assert Decimal(profit) == Decimal(z['gnl']), '预计损益是{}，数据库返回是{}'.format(profit, z['gnl'])
                elif z['trading_direction'] == 2:
                    cfx_dict['buy_us'] = str(cfx_book[str(z['book_id'])]).split('-')[0]
                    cfx_dict['sell_us'] = str(cfx_book[str(z['book_id'])]).split('-')[1]
                    cfx_dict['buy_us_amount'] = z['trading_amount']
                    cfx_dict['sell_us_amount'] = z['pnl_amount']
                    cfx_dict['profit'] = z['gnl']
                    cfx_dict['order_time'] = z['aggregation_no']
                    profit = Decimal(z['trading_amount']) * Decimal(z['cost'])
                    if str(cfx_book[str(z['book_id'])]).split('-')[1] == 'BTC' or \
                            str(cfx_book[str(z['book_id'])]).split('-')[1] == 'ETH':
                        profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:8])
                    elif str(cfx_book[str(z['book_id'])]).split('-')[1] == 'USDT':
                        profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
                    else:
                        profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:2])
                    profit = Decimal(z['pnl_amount']) - Decimal(profit)
                    assert Decimal(profit) == Decimal(z['gnl']), '预计损益是{}，数据库返回是{}'.format(profit, z['gnl'])
                cfx_dict['cost'] = z['cost']
                cfx_list.append(cfx_dict)
        return cfx_list
