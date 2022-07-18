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
        with allure.step("获取入账显示"):
            account_id = get_json()['infinni_games']['account_vid']
            with allure.step("验签"):
                unix_time = int(time.time())
                nonce = generate_string(30)
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', key='infinni games',
                                                    nonce=nonce)
                headers['ACCESS-SIGN'] = sign
                headers['ACCESS-TIMESTAMP'] = str(unix_time)
                headers['ACCESS-NONCE'] = nonce
            with allure.step("获取合作方的配置"):
                r = session.request('GET', url='{}/config'.format(self.url), headers=headers)
                for i in r.json()['currencies']:
                    if i['type'] == 1:
                        for y in i['deposit_methods']:
                            with allure.step("获取入账显示"):
                                with allure.step("验签"):
                                    unix_time = int(time.time())
                                    nonce = generate_string(30)
                                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                                        url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(account_id, i['symbol'], y), key='infinni games',
                                                                        nonce=nonce)
                                    headers['ACCESS-SIGN'] = sign
                                    headers['ACCESS-TIMESTAMP'] = str(unix_time)
                                    headers['ACCESS-NONCE'] = nonce
                                with allure.step("获取入账显示"):
                                    r = session.request('GET', url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i['symbol'], y), headers=headers)
                                    logger.info('r.json返回值是：{}'.format(r.json()))
                                with allure.step("校验状态码"):
                                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                                with allure.step("校验返回值"):
                                    assert r.json()['symbol'] == i['symbol'], "获取入账显示错误，返回值是{}".format(r.text)


