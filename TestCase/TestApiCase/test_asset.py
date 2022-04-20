from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api asset 相关 testcases")
class TestAssetApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_asset_001')
    @allure.description('查询每个币种当前资产市值')
    def test_asset_001(self):
        with allure.step("获取币种列表"):
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
                        assert ApiFunction.get_crypto_abs_amount(i) == y['value'], '{}币种当前资产市值是{},接口返回值是{}.查询每个币种当前资产市值错误'.format(i, ApiFunction.get_crypto_abs_amount(i), y['value'])

    @allure.title('test_asset_002')
    @allure.description('获取账户资金状态')
    def test_asset_002(self):
        with allure.step("获取账户资金状态"):
            r = session.request('GET', url='{}/assetstatapi/assetstat'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'overview' in r.text, "获取账户资金状态错误，返回值是{}".format(r.text)

    @allure.title('test_asset_003')
    @allure.description('获取账户详细损益')
    def test_asset_003(self):
        with allure.step("获取账户资金状态"):
            r = session.request('GET', url='{}/assetstatapi/asset_pl_detail'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'profit_loss_overview' in r.text, "获取账户资金状态错误，返回值是{}".format(r.text)
