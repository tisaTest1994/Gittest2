from Function.api_function import *
from Function.operate_sql import *


# Balance相关cases
class TestBalanceApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_balance_001')
    @allure.description('获取用户的所有账户余额')
    def test_balance_001(self, partner):
        with allure.step("获取用户的所有账户余额"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances'.format(account_vid), connect_type=partner, nonce=nonce)
            connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(connect_url, account_vid), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['balances'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)
        with allure.step("判断提供给partner的和我们自用的值一致"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                mobile_balance = ApiFunction.get_crypto_number(type=i['symbol'], balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
                for y in r.json()['balances']:
                    if y['code'] == i['symbol']:
                        assert float(mobile_balance) == float(y['balances']), '币种{}判断提供给{}的和我们自用的值一致失败，我们自用balance是{},bybit是{}'.format(i['symbol'], partner, mobile_balance, y['balances'])

    @allure.title('test_balance_002')
    @allure.description('获取账户可用余额单币(有资金）')
    def test_balance_002(self, partner):
        with allure.step("获取用户的所有账户余额"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']
        with allure.step("循环获取单币种"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances/{}'.format(account_vid, i['symbol']), connect_type=partner, nonce=nonce)
                    connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                        'Partner_ID']
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("账户可用余额列表"):
                    r = session.request('GET', url='{}/accounts/{}/balances/{}'.format(connect_url, account_vid, i['symbol']), headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "当币种为{},http状态码不对，目前状态码是{}".format(i['symbol'], r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['balance'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)
                with allure.step("通过mobile接口获取金额"):
                    mobile_balance = ApiFunction.get_crypto_number(type=i['symbol'], balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
                with allure.step("获取的金额和通过mobile接口获取的金额对比"):
                    assert float(mobile_balance) == float(r.json()['balance']['balances']), '币种{}判断提供给infinni games的和我们自用的值一致失败，我们自用balance是{},bybit是{}'.format(i, mobile_balance, r.json()['balance']['balances'])