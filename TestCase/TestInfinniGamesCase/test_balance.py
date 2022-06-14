from Function.api_function import *
from Function.operate_sql import *


# Balance相关cases
class TestBalanceApi:
    url = get_json()['infinni_games']['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("多语言支持"):
            headers['locale'] = 'zh-TW'
        with allure.step("ACCESS-KEY"):
            headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']

    @allure.title('test_balance_001')
    @allure.description('获取用户的所有账户余额')
    def test_balance_001(self):
        with allure.step("获取用户的所有账户余额"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), key='infinni games', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['balances'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)
        with allure.step("判断提供给bybit的和我们自用的值一致"):
            balance_list = ApiFunction.balance_list()
            for i in balance_list:
                mobile_balance = ApiFunction.get_crypto_number(type=i, balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
                for y in r.json()['balances']:
                    if y['code'] == i:
                        assert float(mobile_balance) == float(y['balances']), '币种{}判断提供给infinni games的和我们自用的值一致失败，我们自用balance是{},bybit是{}'.format(i, mobile_balance, y['balances'])

    @allure.title('test_balance_002')
    @allure.description('获取账户可用余额单币(有资金）')
    def test_balance_002(self):
        with allure.step("获取用户的所有账户余额"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("获得balance list"):
            balance_list = ApiFunction.balance_list()
        with allure.step("从metadata接口获取已开启的币种信息"):
            fiat_metadata = session.request('GET', url='{}/core/metadata'.format(env_url), headers=headers)
            fiat_list_metadata = fiat_metadata.json()['currencies']
            fiat_all_metadata = fiat_list_metadata.keys()
        with allure.step("如在metada中关闭，则去除"):
            for i in range(0, len(balance_list)):
                if balance_list[i] not in fiat_all_metadata:
                    balance_list.remove(balance_list[i])
        with allure.step("循环获取单币种"):
            for i in balance_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}'.format(account_id, i), key='infinni games',
                                                        nonce=nonce)
                    headers['ACCESS-SIGN'] = sign
                    headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    headers['ACCESS-NONCE'] = nonce
                with allure.step("账户可用余额列表"):
                    r = session.request('GET', url='{}/accounts/{}/balances/{}'.format(self.url, account_id, i), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "当币种为{},http状态码不对，目前状态码是{}".format(i, r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['balance'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)
                with allure.step("通过mobile接口获取金额"):
                    mobile_balance = ApiFunction.get_crypto_number(type=i, balance_type='BALANCE_TYPE_AVAILABLE',
                                                                   wallet_type='BALANCE')
                with allure.step("获取的金额和通过mobile接口获取的金额对比"):
                    assert float(mobile_balance) == float(r.json()['balance']['balances']), '币种{}判断提供给infinni games的和我们自用的值一致失败，我们自用balance是{},bybit是{}'.format(i, mobile_balance, r.json()['balance']['balances'])