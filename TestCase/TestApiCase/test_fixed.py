from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api fixed 相关 testcases")
class TestFixedApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_fixed_001')
    @allure.description('获取定期产品列表')
    def test_fixed_001(self):
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                for i in r.json():
                    assert i['code'] == 'BTC' or i['code'] == 'ETH' or i['code'] == 'USDT', "获取定期产品列表失败，返回值是{}".format(r.text)

    @allure.title('test_fixed_002')
    @allure.description('获取定期产品详情')
    def test_fixed_002(self):
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
        for i in r.json():
            for y in i['products']:
                logger.info('定期产品product_id是{}'.format(y['product_id']))
                with allure.step("获取定期产品详情"):
                    r = session.request('GET', url='{}/earn/fix/products/{}'.format(env_url, y['product_id']), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'maturity_date' in r.text, '获取定期产品详情失败,返回值是{}'.format(r.json())

    @allure.title('test_fixed_003')
    @allure.description('获取定期产品利息列表')
    def test_fixed_003(self):
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
        for i in r.json():
            for y in i['products']:
                logger.info('定期产品product_id是{}'.format(y['product_id']))
                with allure.step("获取定期产品详情"):
                    params = {
                        'cursor': "0",
                        'size': 99999
                    }
                    r = session.request('GET', url='{}/earn/products/{}/interests'.format(env_url, y['product_id']), params=params, headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        for z in r.json()['items']:
                            assert z['apy'] is not None, "获取定期产品利息列表失败，返回值是{}".format(r.text)
                            assert z['date'] is not None, "获取定期产品利息列表失败，返回值是{}".format(r.text)

    @allure.title('test_fixed_004')
    @allure.description('购买定期产品')
    def test_fixed_004(self):
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
        for i in r.json():
            logger.info('定期产品详情。 {}'.format(i))
            for y in i['products']:
                sleep(1)
                logger.info('定期产品product_id是{}'.format(y['product_id']))
                with allure.step("获取购买定期前BTC可用数量"):
                    balance_amount_old = ApiFunction.get_crypto_number(type='BTC', balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
                with allure.step("获取购买定期前BTC购买活期数量"):
                    saving_amount_old = ApiFunction.get_crypto_number(type='BTC',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='SAVING')
                with allure.step("获取购买定期前BTC购买定期数量"):
                    fix_amount_old = ApiFunction.get_crypto_number(type='BTC',
                                                                       balance_type='BALANCE_TYPE_AVAILABLE',
                                                                       wallet_type='SAVING-FIX')
                if i['code'] == 'BTC':
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": "0.13"
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * (Decimal(y['apy']) / 100 ) / Decimal(365)).quantize(Decimal('0.00000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']), data=json.dumps(data), headers=headers)
                    sleep(3)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前BTC可用数量"):
                        balance_amount_latest = ApiFunction.get_crypto_number(type='BTC',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前BTC购买活期数量"):
                        saving_amount_latest = ApiFunction.get_crypto_number(type='BTC',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前BTC购买定期数量"):
                        fix_amount_latest = ApiFunction.get_crypto_number(type='BTC',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['status'] == 1, '{}项目错误，购买定期产品失败，返回值是{}'.format(y['product_id'], r.text)
                        assert ApiFunction.get_transaction_status(transaction_id=r.json()['tx_id'], type='3') == 2 or ApiFunction.get_transaction_status(transaction_id=r.json()['tx_id'], type='3') == 1, '{}项目错误，购买定期产品失败，返回值是{}'.format(y['product_id'], r.text)
                        assert Decimal(balance_amount_old) - Decimal(data['subscribe_amount']['amount']) == Decimal(balance_amount_latest), '购买定期产品后钱包余额错误,购买前钱包BTC数量{},购买定期数量{},购买后钱包BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品后活期金额错误,购买前活期BTC数量{},购买后活期BTC数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) + Decimal(data['subscribe_amount']['amount']) == Decimal(fix_amount_latest), '购买定期产品后定期金额错误,购买前定期BTC数量{},购买定期数量{},购买后定期BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)
                elif i['code'] == 'ETH':
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_old = ApiFunction.get_crypto_number(type='ETH',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = ApiFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = ApiFunction.get_crypto_number(type='ETH',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='SAVING-FIX')
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": "0.13"
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * (Decimal(y['apy']) / 100 ) / Decimal(365)).quantize(Decimal('0.00000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']), data=json.dumps(data), headers=headers)
                    sleep(3)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_latest = ApiFunction.get_crypto_number(type='ETH',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_latest = ApiFunction.get_crypto_number(type='ETH',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_latest = ApiFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['status'] == 1, '{}项目错误，购买定期产品失败，返回值是{}'.format(y['product_id'], r.text)
                        assert ApiFunction.get_transaction_status(transaction_id=r.json()['tx_id'], type='3') == 2 or ApiFunction.get_transaction_status(transaction_id=r.json()['tx_id'], type='3') == 1, '{}项目错误，购买定期产品失败，返回值是{}'.format(y['product_id'], r.text)
                        assert Decimal(balance_amount_old) - Decimal(data['subscribe_amount']['amount']) == Decimal(balance_amount_latest), '购买定期产品后钱包余额错误,购买前钱包BTC数量{},购买定期数量{},购买后钱包BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品后活期金额错误,购买前活期BTC数量{},购买后活期BTC数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) + Decimal(data['subscribe_amount']['amount']) == Decimal(fix_amount_latest), '购买定期产品后定期金额错误,购买前定期BTC数量{},购买定期数量{},购买后定期BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)
                elif i['code'] == 'USDT':
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_old = ApiFunction.get_crypto_number(type='USDT',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = ApiFunction.get_crypto_number(type='USDT',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = ApiFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": "50"
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * (Decimal(y['apy']) / 100 ) / Decimal(365)).quantize(Decimal('0.000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']), data=json.dumps(data), headers=headers)
                    sleep(3)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前USDT可用数量"):
                        balance_amount_latest = ApiFunction.get_crypto_number(type='USDT',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前USDT购买活期数量"):
                        saving_amount_latest = ApiFunction.get_crypto_number(type='USDT',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前USDT购买定期数量"):
                        fix_amount_latest = ApiFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['status'] == 1, '{}项目错误，购买定期产品失败，返回值是{}'.format(y['product_id'], r.text)
                        assert ApiFunction.get_transaction_status(transaction_id=r.json()['tx_id'], type='3') == 1 or ApiFunction.get_transaction_status(transaction_id=r.json()['tx_id'], type='3') == 2, '{}项目错误，购买定期产品失败，返回值是{}'.format(y['product_id'], r.text)
                        assert Decimal(balance_amount_old) - Decimal(data['subscribe_amount']['amount']) == Decimal(balance_amount_latest), '购买定期产品后钱包余额错误,购买前钱包BTC数量{},购买定期数量{},购买后钱包BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品后活期金额错误,购买前活期BTC数量{},购买后活期BTC数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) + Decimal(data['subscribe_amount']['amount']) == Decimal(fix_amount_latest), '购买定期产品后定期金额错误,购买前定期BTC数量{},购买定期数量{},购买后定期BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)

                else:
                    assert False, "币种不对，购买定期产品失败。"

    @allure.title('test_fixed_005')
    @allure.description('购买定期产品最小额度')
    def test_fixed_005(self):
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
        for i in r.json():
            logger.info('定期产品详情。 {}'.format(i))
            for y in i['products']:
                sleep(2)
                max_input = y['subscribe_attr']['subscribe_min_amount']
                logger.info('定期产品product_id是{}'.format(y['product_id']))
                with allure.step("获取购买定期前BTC可用数量"):
                    balance_amount_old = ApiFunction.get_crypto_number(type='BTC',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='BALANCE')
                with allure.step("获取购买定期前BTC购买活期数量"):
                    saving_amount_old = ApiFunction.get_crypto_number(type='BTC',
                                                                          balance_type='BALANCE_TYPE_AVAILABLE',
                                                                          wallet_type='SAVING')
                with allure.step("获取购买定期前BTC购买定期数量"):
                    fix_amount_old = ApiFunction.get_crypto_number(type='BTC',
                                                                       balance_type='BALANCE_TYPE_AVAILABLE',
                                                                       wallet_type='SAVING-FIX')
                if i['code'] == 'BTC':
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": str((Decimal(max_input) / 10).quantize(Decimal('0.00000000'), ROUND_FLOOR))
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * Decimal(
                        y['apy']) / Decimal(365)).quantize(Decimal('0.00000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST',
                                        url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']),
                                        data=json.dumps(data), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前BTC可用数量"):
                        balance_amount_latest = ApiFunction.get_crypto_number(type='BTC',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前BTC购买活期数量"):
                        saving_amount_latest = ApiFunction.get_crypto_number(type='BTC',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前BTC购买定期数量"):
                        fix_amount_latest = ApiFunction.get_crypto_number(type='BTC',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'Minimum:' in r.text, '购买定期产品最小额度错误, 返回值是{}'.format(r.text)
                        assert Decimal(balance_amount_old) == Decimal(balance_amount_latest), '购买定期产品最小额度错误,购买前钱包BTC数量{},购买后钱包BTC数量{}'.format(balance_amount_old, balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品最小额度错误,购买前活期BTC数量{},购买后活期BTC数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) == Decimal(fix_amount_latest), '购买定期产品最小额度错误,购买前定期BTC数量{},购买后定期BTC数量{}'.format(balance_amount_old,  balance_amount_latest)
                elif i['code'] == 'ETH':
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_old = ApiFunction.get_crypto_number(type='ETH',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = ApiFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = ApiFunction.get_crypto_number(type='ETH',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='SAVING-FIX')
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": str((Decimal(max_input) / 10).quantize(Decimal('0.00000000'), ROUND_FLOOR))
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * Decimal(
                        y['apy']) / Decimal(365)).quantize(Decimal('0.00000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST',
                                        url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']),
                                        data=json.dumps(data), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_latest = ApiFunction.get_crypto_number(type='ETH',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_latest = ApiFunction.get_crypto_number(type='ETH',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_latest = ApiFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'Minimum:' in r.text, '购买定期产品最小额度错误, 返回值是{}'.format(r.text)
                        assert Decimal(balance_amount_old) == Decimal(balance_amount_latest), '购买定期产品最小额度错误,购买前钱包ETH数量{},购买后钱包BTC数量{}'.format(balance_amount_old, balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品最小额度错误,购买前活期ETH数量{},购买后活期BTC数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) == Decimal(fix_amount_latest), '购买定期产品最小额度错误,购买前定期ETH数量{},购买后定期ETH数量{}'.format(balance_amount_old,  balance_amount_latest)
                elif i['code'] == 'USDT':
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_old = ApiFunction.get_crypto_number(type='USDT',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = ApiFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = ApiFunction.get_crypto_number(type='USDT',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='SAVING-FIX')
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": str((Decimal(max_input) / 10).quantize(Decimal('0.00000000'), ROUND_FLOOR))
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * Decimal(
                        y['apy']) / Decimal(365)).quantize(Decimal('0.000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST',
                                        url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']),
                                        data=json.dumps(data), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前USDT可用数量"):
                        balance_amount_latest = ApiFunction.get_crypto_number(type='USDT',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前USDT购买活期数量"):
                        saving_amount_latest = ApiFunction.get_crypto_number(type='USDT',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前USDT购买定期数量"):
                        fix_amount_latest = ApiFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'Minimum:' in r.text, '购买定期产品最小额度错误, 返回值是{}'.format(r.text)
                        assert Decimal(balance_amount_old) == Decimal(balance_amount_latest), '购买定期产品最小额度错误,购买前钱包USDT数量{},购买后钱包USDT数量{}'.format(balance_amount_old, balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品最小额度错误,购买前活期USDT数量{},购买后活期USDT数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) == Decimal(fix_amount_latest), '购买定期产品最小额度错误,购买前定期USDT数量{},购买后定期USDT数量{}'.format(balance_amount_old,  balance_amount_latest)
                else:
                    assert False, "币种不对，购买定期产品失败。"

    @allure.title('test_fixed_006')
    @allure.description('购买定期产品最大额度')
    def test_fixed_006(self):
        sleep(5)
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
        for i in r.json():
            logger.info('定期产品详情。 {}'.format(i))
            for y in i['products']:
                sleep(2)
                max_input = y['subscribe_attr']['user_single_subscribe_upper_limit']
                logger.info('定期产品product_id是{}'.format(y['product_id']))
                with allure.step("获取购买定期前BTC可用数量"):
                    balance_amount_old = ApiFunction.get_crypto_number(type='BTC',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='BALANCE')
                with allure.step("获取购买定期前BTC购买活期数量"):
                    saving_amount_old = ApiFunction.get_crypto_number(type='BTC',
                                                                          balance_type='BALANCE_TYPE_AVAILABLE',
                                                                          wallet_type='SAVING')
                with allure.step("获取购买定期前BTC购买定期数量"):
                    fix_amount_old = ApiFunction.get_crypto_number(type='BTC',
                                                                       balance_type='BALANCE_TYPE_AVAILABLE',
                                                                       wallet_type='SAVING-FIX')
                if i['code'] == 'BTC':
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": str(Decimal(max_input) * 2)
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * Decimal(
                        y['apy']) / Decimal(365)).quantize(Decimal('0.00000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST',
                                        url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']),
                                        data=json.dumps(data), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前BTC可用数量"):
                        balance_amount_latest = ApiFunction.get_crypto_number(type='BTC',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前BTC购买活期数量"):
                        saving_amount_latest = ApiFunction.get_crypto_number(type='BTC',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前BTC购买定期数量"):
                        fix_amount_latest = ApiFunction.get_crypto_number(type='BTC',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'Maximum:' in r.text, '购买定期产品最大额度错误, 返回值是{}'.format(r.text)
                        assert Decimal(balance_amount_old) == Decimal(
                            balance_amount_latest), '购买定期产品最大额度错误,购买前钱包BTC数量{},购买后钱包BTC数量{}'.format(balance_amount_old,
                                                                                                    balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(
                            saving_amount_latest), '购买定期产品最大额度错误,购买前活期BTC数量{},购买后活期BTC数量{}'.format(saving_amount_old,
                                                                                                   saving_amount_latest)
                        assert Decimal(fix_amount_old) == Decimal(
                            fix_amount_latest), '购买定期产品最大额度错误,购买前定期BTC数量{},购买后定期BTC数量{}'.format(balance_amount_old,
                                                                                                balance_amount_latest)
                elif i['code'] == 'ETH':
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_old = ApiFunction.get_crypto_number(type='ETH',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = ApiFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = ApiFunction.get_crypto_number(type='ETH',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='SAVING-FIX')
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": str(Decimal(max_input) * 2)
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * Decimal(
                        y['apy']) / Decimal(365)).quantize(Decimal('0.00000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST',
                                        url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']),
                                        data=json.dumps(data), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_latest = ApiFunction.get_crypto_number(type='ETH',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_latest = ApiFunction.get_crypto_number(type='ETH',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_latest = ApiFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'Maximum:' in r.text, '购买定期产品最大额度错误, 返回值是{}'.format(r.text)
                        assert Decimal(balance_amount_old) == Decimal(
                            balance_amount_latest), '购买定期产品最大额度错误,购买前钱包ETH数量{},购买后钱包BTC数量{}'.format(balance_amount_old,
                                                                                                    balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(
                            saving_amount_latest), '购买定期产品最大额度错误,购买前活期ETH数量{},购买后活期BTC数量{}'.format(saving_amount_old,
                                                                                                   saving_amount_latest)
                        assert Decimal(fix_amount_old) == Decimal(
                            fix_amount_latest), '购买定期产品最大额度错误,购买前定期ETH数量{},购买后定期ETH数量{}'.format(balance_amount_old,
                                                                                                balance_amount_latest)
                elif i['code'] == 'USDT':
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_old = ApiFunction.get_crypto_number(type='USDT',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = ApiFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = ApiFunction.get_crypto_number(type='USDT',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='SAVING-FIX')
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": str(Decimal(max_input) * 2)
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * Decimal(
                        y['apy']) / Decimal(365)).quantize(Decimal('0.000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST',
                                        url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']),
                                        data=json.dumps(data), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前USDT可用数量"):
                        balance_amount_latest = ApiFunction.get_crypto_number(type='USDT',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前USDT购买活期数量"):
                        saving_amount_latest = ApiFunction.get_crypto_number(type='USDT',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前USDT购买定期数量"):
                        fix_amount_latest = ApiFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'Maximum:' in r.text, '购买定期产品最大额度错误, 返回值是{}'.format(r.text)
                        assert Decimal(balance_amount_old) == Decimal(
                            balance_amount_latest), '购买定期产品最大额度错误,购买前钱包USDT数量{},购买后钱包USDT数量{}'.format(
                            balance_amount_old, balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(
                            saving_amount_latest), '购买定期产品最大额度错误,购买前活期USDT数量{},购买后活期USDT数量{}'.format(saving_amount_old,
                                                                                                     saving_amount_latest)
                        assert Decimal(fix_amount_old) == Decimal(
                            fix_amount_latest), '购买定期产品最大额度错误,购买前定期USDT数量{},购买后定期USDT数量{}'.format(balance_amount_old,
                                                                                                  balance_amount_latest)
                else:
                    assert False, "币种不对，购买定期产品失败。"

    @allure.title('test_fixed_007')
    @allure.description('项目不传预计派息金额')
    def test_fixed_007(self):
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
            product_info = random.choice(random.choice(r.json())['products'])
        with allure.step("申购一笔项目"):
            logger.info('申购项目信息是{}'.format(product_info))
            data = {
                "subscribe_amount": {
                    "code": product_info['code'],
                    "amount": "0.013"
                },
                "maturity_interest": {
                    "code": product_info['code'],
                }
            }
            if product_info['code'] == 'USDT':
                data['subscribe_amount']['amount'] = '30'
            r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, product_info['product_id']),
                                data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'field maturity_interest.amount is not set' in r.text, '项目不传预计派息金额错误, 返回值是{}'.format(r.text)

    @allure.title('test_fixed_008')
    @allure.description('项目传入错误预计派息金额')
    def test_fixed_008(self):
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
            product_info = random.choice(random.choice(r.json())['products'])
        with allure.step("申购一笔项目"):
            logger.info('申购项目信息是{}'.format(product_info))
            data = {
                "subscribe_amount": {
                    "code": product_info['code'],
                    "amount": "0.021"
                },
                "maturity_interest": {
                    "code": product_info['code'],
                    "amount": "10"
                }
            }
            if product_info['code'] == 'USDT':
                data['subscribe_amount']['amount'] = '30'
            r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, product_info['product_id']),
                                data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_fixed_009')
    @allure.description('查询申购项目的交易记录详情')
    def test_fixed_009(self):
        with allure.step("申购一笔定期"):
            transaction_info = ApiFunction.subscribe_fix()
        with allure.step("查询申购项目的交易记录详情"):
            r = session.request('GET', url='{}/earn/fix/transactions/{}'.format(env_url, transaction_info['tx_id']), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert transaction_info['tx_id'] in r.text, '查询申购项目的交易记录详情错误, 返回值是{}'.format(r.text)

    @allure.title('test_fixed_010')
    @allure.description('查询申购BTC项目的交易记录')
    def test_fixed_010(self):
        with allure.step("查询申购项目的交易记录"):
            params = {
                'tx_type': "1",
                'cursor': 0,
                'size': 900,
                'order': "1",
                'code': "BTC"
            }
            r = session.request('GET', url='{}/earn/fix/transactions'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() is not None, '查询申购项目的交易记录失败，返回值是{}'.format(r.text)

    @allure.title('test_fixed_011')
    @allure.description('查询申购ETH项目的交易记录')
    def test_fixed_011(self):
        with allure.step("查询申购项目的交易记录"):
            params = {
                'tx_type': "1",
                'cursor': 0,
                'size': 900,
                'order': "1",
                'code': "ETH"
            }
            r = session.request('GET', url='{}/earn/fix/transactions'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() is not None, '查询申购ETH项目的交易记录失败，返回值是{}'.format(r.text)

    @allure.title('test_fixed_012')
    @allure.description('查询申购USDT项目的交易记录')
    def test_fixed_012(self):
        with allure.step("查询申购项目的交易记录"):
            params = {
                'tx_type': "1",
                'cursor': 0,
                'size': 900,
                'order': "1",
                'code': "USDT"
            }
            r = session.request('GET', url='{}/earn/fix/transactions'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() is not None, '查询申购USDT项目的交易记录失败，返回值是{}'.format(r.text)

    @allure.title('test_fixed_013')
    @allure.description('更新（打开）某笔交易的复投状态')
    def test_fixed_013(self):
        with allure.step("申购一笔产品，并且获取信息"):
            product_list = ApiFunction.subscribe_fix()
        with allure.step("打开这笔申购的自动复投"):
            data = {
                "auto_renew": True
            }
            r = session.request('POST', url='{}/earn/fix/transactions/{}/renew'.format(env_url, product_list['tx_id']), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['update_result'] == True, '更新（打开）某笔交易的复投状态错误, 返回值是{}'.format(r.text)

    @allure.title('test_fixed_014')
    @allure.description('更新（关闭）某笔交易的复投状态')
    def test_fixed_014(self):
        with allure.step("申购一笔产品，并且获取信息"):
            product_list = ApiFunction.subscribe_fix()
        with allure.step("打开这笔申购的自动复投"):
            data = {
                "auto_renew": True
            }
            session.request('POST', url='{}/earn/fix/transactions/{}/renew'.format(env_url, product_list['tx_id']), data=json.dumps(data), headers=headers)
        with allure.step("关闭这笔申购的自动复投"):
            data = {
                "auto_renew": False
            }
            r = session.request('POST', url='{}/earn/fix/transactions/{}/renew'.format(env_url, product_list['tx_id']), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['update_result'] == True, '更新（关闭）某笔交易的复投状态错误, 返回值是{}'.format(r.text)

    @allure.title('test_fixed_015')
    @allure.description('更新错误交易id的复投状态')
    def test_fixed_015(self):
        with allure.step("打开这笔申购的自动复投"):
            data = {
                "auto_renew": True
            }
            r = session.request('POST', url='{}/earn/fix/transactions/{}/renew'.format(env_url, '131231231231231'), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'EARNINGTXN000036', '更新错误交易id的复投状态错误, 返回值是{}'.format(r.text)

    @allure.title('test_fixed_016')
    @allure.description('申购定期时，直接打开复投开关')
    def test_fixed_016(self):
        transaction_info = ApiFunction.subscribe_fix(auto_renew=True)
        logger.info("交易信息是{}".format(transaction_info))

    @allure.title('test_fixed_017')
    @allure.description('申购定期时，直接关闭复投开关')
    def test_fixed_017(self):
        transaction_info = ApiFunction.subscribe_fix()
        logger.info("交易信息是{}".format(transaction_info))

    @allure.title('test_fixed_018')
    @allure.description('查询包含复投的交易记录')
    def test_fixed_018(self):
        with allure.step("申购一笔产品，并且获取信息"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
            product_list = random.choice(random.choice(r.json())['products'])
            code = product_list['code']
            product_id = product_list['product_id']
            if code == 'USDT':
                amount = '20'
            else:
                amount = "0.01327"
            data = {
                "subscribe_amount": {
                    "code": code,
                    "amount": amount
                },
                "maturity_interest": {
                    "code": code,
                    "amount": amount
                },
                "auto_renew": True
            }
            r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, product_id), data=json.dumps(data), headers=headers)
            transaction_id = r.json()['tx_id']
        with allure.step("查询申购项目的交易记录"):
            params = {
                'tx_type': "1",
                'cursor': 0,
                'size': 900,
                'order': "1",
                'code': product_list['code']
            }
            r = session.request('GET', url='{}/earn/fix/transactions'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            for i in r.json()['transactions']:
                if transaction_id == i['transaction_id']:
                    assert i['auto_renew'] is True, "查询包含复投的交易记录错误，返回值是{}".format(i)
                    assert i['time_line']['renew_subscription_id'] == '', "查询包含复投的交易记录错误，返回值是{}".format(i)

    @allure.title('test_fixed_019')
    @allure.description('查询包含复投的交易记录详情信息')
    def test_fixed_019(self):
        with allure.step("申购一笔产品，并且获取信息"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
            product_list = random.choice(random.choice(r.json())['products'])
            code = product_list['code']
            product_id = product_list['product_id']
            if code == 'USDT':
                amount = '20'
            else:
                amount = "0.01327"
            data = {
                "subscribe_amount": {
                    "code": code,
                    "amount": amount
                },
                "maturity_interest": {
                    "code": code,
                    "amount": amount
                },
                "auto_renew": True
            }
            r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, product_id), data=json.dumps(data), headers=headers)
            transaction_id = r.json()['tx_id']
        with allure.step("查询申购项目的交易记录信息"):
            r = session.request('GET', url='{}/earn/fix/transactions/{}'.format(env_url, transaction_id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['auto_renew'] == True, "查询包含复投的交易记录错误，返回值是{}".format(r.json())
            assert r.json()['time_line']['renew_subscription_id'] == '', "查询包含复投的交易记录详情信息错误，返回值是{}".format(r.json())

    @allure.title('test_fixed_020')
    @allure.description('通过分页查询包含复投的交易记录详情信息')
    def test_fixed_020(self):
        with allure.step("申购一笔产品，并且获取信息"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
            product_list = random.choice(random.choice(r.json())['products'])
            code = product_list['code']
            product_id = product_list['product_id']
            if code == 'USDT':
                amount = '20'
            else:
                amount = "0.01327"
            data = {
                "subscribe_amount": {
                    "code": code,
                    "amount": amount
                },
                "maturity_interest": {
                    "code": code,
                    "amount": amount
                },
                "auto_renew": True
            }
            r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, product_id), data=json.dumps(data), headers=headers)
            transaction_id = r.json()['tx_id']
        with allure.step("通过分页查询交易记录信息"):
            data = {
                "pagination_request": {
                    "cursor": "0",
                    "page_size": 100
                },
                "user_txn_sub_types": [3],
                "statuses": [1, 2, 3, 4],
                "codes": ["ETH", "BTC", "USDT"]
            }
            r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            for i in r.json()['transactions']:
                if i['transaction_id'] == transaction_id:
                    assert json.loads(i['details'])['subscribe_type'] == 0, "通过分页查询包含复投的交易记录详情信息错误，返回值是{}".format(r.json())

    @allure.title('test_fixed_021')
    @allure.description('查询申购全部项目的交易记录')
    def test_fixed_021(self):
        with allure.step("查询申购项目的交易记录"):
            params = {
                'tx_type': "1",
                'cursor': 0,
                'size': 900,
                'order': "1",
                'code': ""
            }
            r = session.request('GET', url='{}/earn/fix/transactions'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() is not None, '查询申购ETH项目的交易记录失败，返回值是{}'.format(r.text)
