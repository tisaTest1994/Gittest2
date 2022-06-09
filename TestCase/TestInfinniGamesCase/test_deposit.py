from Function.api_function import *
from Function.operate_sql import *


# Deposit相关cases
class TestDepositApi:
    url = get_json()['infinni_games']['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("多语言支持"):
            headers['locale'] = 'zh-TW'
            headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']

    @allure.title('test_deposit_001')
    @allure.description('获取入账显示')
    def test_deposit_001(self):
        with allure.step("获取用户的所有账户余额"):
            account_id = get_json()['infinni_games']['account_vid']
            with allure.step("验签"):
                unix_time = int(time.time())
                nonce = generate_string(30)
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config',
                                                    nonce=nonce)
                connect_headers['ACCESS-SIGN'] = sign
                connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                connect_headers['ACCESS-NONCE'] = nonce
            with allure.step("获取合作方的配置"):
                r = session.request('GET', url='{}/config'.format(self.url), headers=headers)
                support_list = []
                for i in r.json()['currencies']:
                    if i['type'] == 1:
                        support_list.append(i['symbol'])




        # with allure.step("账户可用余额列表"):
        #     r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id), headers=headers)
        # with allure.step("状态码和返回值"):
        #     logger.info('状态码是{}'.format(str(r.status_code)))
        #     logger.info('返回值是{}'.format(str(r.text)))
        # with allure.step("校验状态码"):
        #     assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        # with allure.step("校验返回值"):
        #     assert r.json()['balances'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)
