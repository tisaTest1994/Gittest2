from Function.api_function import *
from run import *
from Function.log import *
import allure


# asset相关cases
def get_crypto_abs_amount(type, account=email['email'], password=email['password']):
    accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
    headers['Authorization'] = "Bearer " + accessToken
    headers['X-Currency'] = 'USD'
    r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
    for i in r.json()['wallets']:
        if i['code'] == type:
            return i['abs_amount']


def get_crypto_quote(type, time):
    connect_mysql()


class TestAssetApi:

    @allure.testcase('test_asset_001 查询每个币种当前资产市值')
    def test_asset_001(self):
        crypto_list = get_json()['crypto_list']
        for i in crypto_list:
            print(get_crypto_abs_amount(i))

    @allure.testcase('test_asset_002 查询每个币种今日损益')
    def test_asset_002(self):
        crypto_list = get_json()['crypto_list']
        for i in crypto_list:
            print(get_crypto_abs_amount(i))
