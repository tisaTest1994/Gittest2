from Function.api_function import *
from run import *
from Function.log import *
import allure


class TestAssetApi:

    @allure.testcase('test_asset_001 查询每个币种当前资产市值')
    def test_asset_001(self):
        crypto_list = get_json()['crypto_list']
        accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        with allure.step("查询每个币种当前资产市值"):
            r = session.request('GET', url='{}/assetstatapi/assetstat'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            for i in crypto_list:
                for y in r.json()['overview']:
                    if i == y['code']:
                        assert AccountFunction.get_crypto_abs_amount(i) == y['value'], '{}币种当前资产市值是{},接口返回值是{}.查询每个币种当前资产市值错误'.format(i, AccountFunction.get_crypto_abs_amount(i), y['value'])

    @allure.testcase('test_asset_002 查询每个币种今日损益')
    def test_asset_002(self):
        with allure.step("获取本日utc0点"):
            utc_zero = get_zero_utc_time()
        crypto_list = get_json()['crypto_list']
        accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        for i in crypto_list:
            with allure.step("获得{}现在数量".format(i)):
                number = AccountFunction.get_crypto_number(crypto_type=i)
            data = {
                "pagination_request": {
                    "cursor": "0",
                    "page_size": 9999999
                },
                "user_txn_sub_types": [1, 2, 4, 6],
                "statuses": [2],
                "codes": [i]
            }
            r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers, timeout=10)
            for y in r.json()['transactions']:
                if y['created_at'] >= utc_zero:
                    if y['user_txn_sub_type'] == 1:
                        number = float(number) - float(json.loads(y['details'])['currency']['amount'])
                    elif y['user_txn_sub_type'] == 2 and json.loads(y['details'])['but_currency']['code'] == i:
                        number = float(number) - float(json.loads(y['details'])['but_currency']['amount'])
                    elif y['user_txn_sub_type'] == 2 and json.loads(y['details'])['sell_currency']['code'] == i:
                        number = float(number) + float(json.loads(y['details'])['but_currency']['amount'])
                    elif y['user_txn_sub_type'] == 4:
                        number = float(number) - float(json.loads(y['details'])['currency']['amount'])
                    elif y['user_txn_sub_type'] == 6:
                        number = float(number) + float(json.loads(y['details'])['currency']['amount'])
            # 获取昨天UTC23:59的价格
            print(utc_zero)
            yesterday_number = number
