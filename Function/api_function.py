from run import *
import requests


class AccountFunction:

    @staticmethod
    def get_account_token(account, password):
        data = {
            "username": account,
            "password": password
        }
        r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                             headers=headers)
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
        requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)

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
        r = requests.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        return r.json()['transaction_id']

    # 获取下次清算金额
    @staticmethod
    def get_interest(productId, account=email['email'],  password=email['password']):
        accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        r1 = requests.request('GET', url='{}/earn/products/{}/next_yield'.format(env_url, productId), headers=headers)
        return r1.json()['next_yield']

    # 获取换汇报价
    @staticmethod
    def get_quote(pair):
        cryptos = pair.split('-')
        r1 = requests.request('GET',
                              url='{}/core/quotes/{}'.format(env_url, "{}-{}".format(cryptos[0], cryptos[1])),
                              headers=headers)
        return r1.json()

    # 获取钱包指定币种数量
    @staticmethod
    def get_crypto_number(account=email['email'], password=email['password'], crypto_type='BTC'):
        accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
        for i in r.json():
            if i['code'] == crypto_type and i['wallet_type'] == 'BALANCE':
                for y in i['balances']:
                    if y['type'] == 'BALANCE_TYPE_AVAILABLE':
                        balance_type_available_amount = y['amount']
        return balance_type_available_amount


