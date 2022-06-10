from Function.api_function import *
from Function.operate_sql import *


# Convert相关cases
class TestConvertApi:
    url = get_json()['infinni_games']['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("多语言支持"):
            headers['locale'] = 'zh-TW'
        with allure.step("ACCESS-KEY"):
            headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']

    @allure.title('test_convert_001')
    @allure.description('获取报价最新的报价')
    def test_convert_001(self):
        with allure.step("获取最新的报价"):
            for i in ApiFunction.get_connect_cfx_list(self.url, headers, key='infinni games'):
                with allure.step("获取正向报价"):
                    r = session.request('GET', url='{}/quotes/{}'.format(self.url, i), headers=headers)
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['quote'] is not None, "获取报价错误，返回值是{}".format(r.text)
                with allure.step("获取反向报价"):
                    new_pair = '{}{}{}'.format(i.split('-')[1], '-', i.split('-')[0])
                    r = session.request('GET', url='{}/quotes/{}'.format(self.url, new_pair),
                                        headers=headers)
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['quote'] is not None, "获取报价错误，返回值是{}".format(r.text)

    @allure.title('test_convert_002')
    @allure.description('换汇交易')
    def test_convert_002(self):
        for i in ApiFunction.get_cfx_list():
            with allure.step("正向币种对，major_ccy 是buy值"):
                with allure.step("获得换汇前buy币种balance金额"):
                    buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                with allure.step('获得换汇前sell币种balance金额'):
                    sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                with allure.step('获得换汇前sell币种balance金额'):




                    transaction = ApiFunction.cfx_random(i, i.split('-')[0])
                    sleep(5)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                        transaction['data']['buy_amount']) == Decimal(
                        buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[0], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                        buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                        transaction['data']['sell_amount']) == Decimal(
                        sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[1], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                        sell_amount_wallet_balance_latest)
            with allure.step("正向币种对，major_ccy 是sell值"):
                with allure.step("获得换汇前buy币种balance金额"):
                    buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                with allure.step('获得换汇前sell币种balance金额'):
                    sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    transaction = ApiFunction.cfx_random(i, i.split('-')[1])
                    sleep(5)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                        transaction['data']['buy_amount']) == Decimal(
                        buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[0], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                        buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                        transaction['data']['sell_amount']) == Decimal(
                        sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[1], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                        sell_amount_wallet_balance_latest)
            with allure.step("反向币种对，major_ccy 是buy值"):
                with allure.step("获得换汇前buy币种balance金额"):
                    buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                with allure.step('获得换汇前sell币种balance金额'):
                    sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    transaction = ApiFunction.cfx_random('{}-{}'.format(i.split('-')[1], i.split('-')[0]),
                                                         i.split('-')[1])
                    sleep(5)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                        transaction['data']['buy_amount']) == Decimal(
                        buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[1], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                        buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                        transaction['data']['sell_amount']) == Decimal(
                        sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[0], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                        sell_amount_wallet_balance_latest)
            with allure.step("反向币种对，major_ccy 是sell值"):
                with allure.step("获得换汇前buy币种balance金额"):
                    buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                with allure.step('获得换汇前sell币种balance金额'):
                    sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    transaction = ApiFunction.cfx_random('{}-{}'.format(i.split('-')[1], i.split('-')[0]),
                                                         i.split('-')[0])
                    sleep(5)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                        transaction['data']['buy_amount']) == Decimal(
                        buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[1], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                        buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                        transaction['data']['sell_amount']) == Decimal(
                        sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[0], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                        sell_amount_wallet_balance_latest)

