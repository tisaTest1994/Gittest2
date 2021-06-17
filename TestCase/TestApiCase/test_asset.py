from Function.api_function import *
from run import *
from Function.log import *
from decimal import *
import allure


class TestAssetApi:

    # 初始化class
    def setup_class(self):
        AccountFunction.add_headers()

    @allure.testcase('test_asset_001 查询每个币种当前资产市值')
    def test_asset_001(self):
        crypto_list = get_json()['crypto_list']
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

    @allure.testcase('test_asset_002 ')
    def test_asset_002(self):
        a = AccountFunction.get_today_increase()
        print(a)


