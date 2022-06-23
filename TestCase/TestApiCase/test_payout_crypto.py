from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api payout crypto相关 testcases")
class TestPayoutCryptoApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_payout_crypto_001')
    @allure.description('获取提现费率和提现限制-预校验数字货币')
    def test_payout_crypto_001(self):
        crypto_list = get_json()['crypto_list']
        for i in crypto_list:
            with allure.step("获取提现费率和提现限制"):
                data = {
                    "amount": "0.11",
                    "code": i,
                    "address": "0x623089BFb1dc2d3023Ba4bd0f42F61d66826994eu",
                    "method": "ERC20"
                }
                r = session.request('POST', url='{}/pay/withdraw/verification'.format(env_url), data=json.dumps(data),
                                    headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                logger.info('接口返回值是{}'.format(str(r.text)))
                if i not in crypto_list:
                    raise Exception(("查看法币列表是否新增", crypto_list), ('接口返回', r.json()))
                elif i == 'BTC':
                    assert r.json()['fee'] == '0.0006'
                elif i == 'USDT':
                    assert r.json()['fee'] == '12'
                elif i == 'BRL':
                    assert r.json()['ETH'] == '0.004'

    @allure.title('test_payout_crypto_002')
    @allure.description('获得数字货币提现币种')
    def test_payout_crypto_002(self):
        with allure.step("提现币种"):
            r = session.request('GET', url='{}/pay/withdraw/ccy/{}'.format(env_url, 'crypto'), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'crypto' in r.text, "获得数字货币提现币种错误，返回值是{}".format(r.text)