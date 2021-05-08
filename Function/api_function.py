from run import *
from Function.log import *
import time


class AccountFunction:

    # 获取用户token
    @staticmethod
    def get_account_token(account, password):
        data = {
            "username": account,
            "password": password
        }
        r = session.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data), headers=headers, timeout=3)
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
        session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers, timeout=3)

    # 提现获取交易id
    @staticmethod
    def get_payout_transaction_id(account=email['email'], password=email['password'], amount='0.0007', address='0x428DA40C585514022b2eB537950d5AB5C7365a07' ):
        accessToken = AccountFunction.get_account_token(account=account,  password=password)['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        data = {
            "amount": amount,
            "code": "ETH",
            "address": address,
            "method": "ERC20"
        }
        r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        logger.info('获取的交易订单json是{}'.format(r.text))
        return r.json()['transaction_id']

    # 获取下次清算金额
    @staticmethod
    def get_interest(productId, account=email['email'],  password=email['password']):
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
    def get_crypto_number(account=email['email'], password=email['password'], crypto_type='BTC'):
        accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        r = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
        for i in r.json():
            if i['code'] == crypto_type and i['wallet_type'] == 'BALANCE':
                for y in i['balances']:
                    if y['type'] == 'BALANCE_TYPE_AVAILABLE':
                        balance_type_available_amount = y['amount']
        return balance_type_available_amount

    # 获取当前某个币的资产价值，用USD结算
    @staticmethod
    def get_crypto_abs_amount(type, account=email['email'], password=email['password']):
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
        quote = connect_mysql('marketstat',
                              "select quote from customer_quote_stat where pair='{}USD' and open_time='20210506';".format(
                                  type, open_time))
        quote_number = str(quote).split("'")[3]
        logger.info('{}的quote是{}'.format(type, quote_number))
        return quote_number
