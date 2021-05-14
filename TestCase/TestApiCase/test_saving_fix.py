import json

from Function.api_function import *
from run import *
from Function.log import *
from decimal import *
import allure


# saving相关cases
class TestSavingFixApi:

    @allure.testcase('test_saving_fix_001 获取定期产品列表')
    def test_saving_fix_001(self):
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

    @allure.testcase('test_saving_fix_002 获取定期产品详情')
    def test_saving_fix_002(self):
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
                        assert 'Earn Bit Fixed' in r.text, '获取定期产品详情失败,返回值是{}'.format(r.json())

    @allure.testcase('test_saving_fix_003 获取定期产品利息列表')
    def test_saving_fix_003(self):
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

    @allure.testcase('test_saving_fix_004 购买定期产品')
    def test_saving_fix_004(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            headers['X-Currency'] = 'USD'
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
        for i in r.json():
            logger.info('定期产品详情。 {}'.format(i))
            for y in i['products']:
                sleep(2)
                logger.info('定期产品product_id是{}'.format(y['product_id']))
                with allure.step("获取购买定期前BTC可用数量"):
                    balance_amount_old = AccountFunction.get_crypto_number(type='BTC', balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
                with allure.step("获取购买定期前BTC购买活期数量"):
                    saving_amount_old = AccountFunction.get_crypto_number(type='BTC',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='SAVING')
                with allure.step("获取购买定期前BTC购买定期数量"):
                    fix_amount_old = AccountFunction.get_crypto_number(type='BTC',
                                                                       balance_type='BALANCE_TYPE_AVAILABLE',
                                                                       wallet_type='SAVING-FIX')
                if i['code'] == 'BTC':
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": "0.00124"
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * Decimal(y['apy']) / Decimal(365)).quantize(Decimal('0.00000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']), data=json.dumps(data), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前BTC可用数量"):
                        balance_amount_latest = AccountFunction.get_crypto_number(type='BTC',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前BTC购买活期数量"):
                        saving_amount_latest = AccountFunction.get_crypto_number(type='BTC',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前BTC购买定期数量"):
                        fix_amount_latest = AccountFunction.get_crypto_number(type='BTC',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert AccountFunction.get_transaction_status(transaction_id=r.json()['tx_id'], type='3') == 2, '{}项目错误，购买定期产品失败，返回值是{}'.format(y['product_id'], r.text)
                        assert Decimal(balance_amount_old) - Decimal(data['subscribe_amount']['amount']) == Decimal(balance_amount_latest), '购买定期产品后钱包余额错误,购买前钱包BTC数量{},购买定期数量{},购买后钱包BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品后活期金额错误,购买前活期BTC数量{},购买后活期BTC数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) + Decimal(data['subscribe_amount']['amount']) == Decimal(fix_amount_latest), '购买定期产品后定期金额错误,购买前定期BTC数量{},购买定期数量{},购买后定期BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)
                elif i['code'] == 'ETH':
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_old = AccountFunction.get_crypto_number(type='ETH',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = AccountFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = AccountFunction.get_crypto_number(type='ETH',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='SAVING-FIX')
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": "0.0224"
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * Decimal(y['apy']) / Decimal(365)).quantize(Decimal('0.00000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']), data=json.dumps(data), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_latest = AccountFunction.get_crypto_number(type='ETH',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_latest = AccountFunction.get_crypto_number(type='ETH',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_latest = AccountFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert AccountFunction.get_transaction_status(transaction_id=r.json()['tx_id'], type='3') == 2, '{}项目错误，购买定期产品失败，返回值是{}'.format(y['product_id'], r.text)
                        assert Decimal(balance_amount_old) - Decimal(data['subscribe_amount']['amount']) == Decimal(balance_amount_latest), '购买定期产品后钱包余额错误,购买前钱包BTC数量{},购买定期数量{},购买后钱包BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品后活期金额错误,购买前活期BTC数量{},购买后活期BTC数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) + Decimal(data['subscribe_amount']['amount']) == Decimal(fix_amount_latest), '购买定期产品后定期金额错误,购买前定期BTC数量{},购买定期数量{},购买后定期BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)
                elif i['code'] == 'USDT':
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_old = AccountFunction.get_crypto_number(type='USDT',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = AccountFunction.get_crypto_number(type='USDT',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = AccountFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    data = {
                        "subscribe_amount": {
                            "code": i["code"],
                            "amount": "22"
                        },
                        "maturity_interest": {
                            "code": i["code"],
                            "amount": "0.01"
                        }
                    }
                    data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * Decimal(y['apy']) / Decimal(365)).quantize(Decimal('0.000000'), ROUND_FLOOR)) * Decimal(y['tenor']))
                    r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']), data=json.dumps(data), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("获取购买定期前USDT可用数量"):
                        balance_amount_latest = AccountFunction.get_crypto_number(type='USDT',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前USDT购买活期数量"):
                        saving_amount_latest = AccountFunction.get_crypto_number(type='USDT',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前USDT购买定期数量"):
                        fix_amount_latest = AccountFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert AccountFunction.get_transaction_status(transaction_id=r.json()['tx_id'], type='3') == 2, '{}项目错误，购买定期产品失败，返回值是{}'.format(y['product_id'], r.text)
                        assert Decimal(balance_amount_old) - Decimal(data['subscribe_amount']['amount']) == Decimal(balance_amount_latest), '购买定期产品后钱包余额错误,购买前钱包BTC数量{},购买定期数量{},购买后钱包BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品后活期金额错误,购买前活期BTC数量{},购买后活期BTC数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) + Decimal(data['subscribe_amount']['amount']) == Decimal(fix_amount_latest), '购买定期产品后定期金额错误,购买前定期BTC数量{},购买定期数量{},购买后定期BTC数量{}'.format(balance_amount_old, data['subscribe_amount']['amount'], balance_amount_latest)

                else:
                    assert False, "币种不对，购买定期产品失败。"

    @allure.testcase('test_saving_fix_005 购买定期产品最小额度')
    def test_saving_fix_005(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            headers['X-Currency'] = 'USD'
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
        for i in r.json():
            logger.info('定期产品详情。 {}'.format(i))
            for y in i['products']:
                sleep(2)
                max_input = y['subscribe_attr']['subscribe_min_amount']
                logger.info('定期产品product_id是{}'.format(y['product_id']))
                with allure.step("获取购买定期前BTC可用数量"):
                    balance_amount_old = AccountFunction.get_crypto_number(type='BTC',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='BALANCE')
                with allure.step("获取购买定期前BTC购买活期数量"):
                    saving_amount_old = AccountFunction.get_crypto_number(type='BTC',
                                                                          balance_type='BALANCE_TYPE_AVAILABLE',
                                                                          wallet_type='SAVING')
                with allure.step("获取购买定期前BTC购买定期数量"):
                    fix_amount_old = AccountFunction.get_crypto_number(type='BTC',
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
                        balance_amount_latest = AccountFunction.get_crypto_number(type='BTC',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前BTC购买活期数量"):
                        saving_amount_latest = AccountFunction.get_crypto_number(type='BTC',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前BTC购买定期数量"):
                        fix_amount_latest = AccountFunction.get_crypto_number(type='BTC',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'EARNINGTXN000013' in r.text, '购买定期产品最小额度错误, 返回值是{}'.format(r.text)
                        assert Decimal(balance_amount_old) == Decimal(balance_amount_latest), '购买定期产品最小额度错误,购买前钱包BTC数量{},购买后钱包BTC数量{}'.format(balance_amount_old, balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品最小额度错误,购买前活期BTC数量{},购买后活期BTC数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) == Decimal(fix_amount_latest), '购买定期产品最小额度错误,购买前定期BTC数量{},购买后定期BTC数量{}'.format(balance_amount_old,  balance_amount_latest)
                elif i['code'] == 'ETH':
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_old = AccountFunction.get_crypto_number(type='ETH',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = AccountFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = AccountFunction.get_crypto_number(type='ETH',
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
                        balance_amount_latest = AccountFunction.get_crypto_number(type='ETH',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_latest = AccountFunction.get_crypto_number(type='ETH',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_latest = AccountFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'EARNINGTXN000013' in r.text, '购买定期产品最小额度错误, 返回值是{}'.format(r.text)
                        assert Decimal(balance_amount_old) == Decimal(balance_amount_latest), '购买定期产品最小额度错误,购买前钱包ETH数量{},购买后钱包BTC数量{}'.format(balance_amount_old, balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品最小额度错误,购买前活期ETH数量{},购买后活期BTC数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) == Decimal(fix_amount_latest), '购买定期产品最小额度错误,购买前定期ETH数量{},购买后定期ETH数量{}'.format(balance_amount_old,  balance_amount_latest)
                elif i['code'] == 'USDT':
                    with allure.step("获取购买定期前ETH可用数量"):
                        balance_amount_old = AccountFunction.get_crypto_number(type='USDT',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = AccountFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = AccountFunction.get_crypto_number(type='USDT',
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
                        balance_amount_latest = AccountFunction.get_crypto_number(type='USDT',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前USDT购买活期数量"):
                        saving_amount_latest = AccountFunction.get_crypto_number(type='USDT',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前USDT购买定期数量"):
                        fix_amount_latest = AccountFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'EARNINGTXN000013' in r.text, '购买定期产品最小额度错误, 返回值是{}'.format(r.text)
                        assert Decimal(balance_amount_old) == Decimal(balance_amount_latest), '购买定期产品最小额度错误,购买前钱包USDT数量{},购买后钱包USDT数量{}'.format(balance_amount_old, balance_amount_latest)
                        assert Decimal(saving_amount_old) == Decimal(saving_amount_latest), '购买定期产品最小额度错误,购买前活期USDT数量{},购买后活期USDT数量{}'.format(saving_amount_old, saving_amount_latest)
                        assert Decimal(fix_amount_old) == Decimal(fix_amount_latest), '购买定期产品最小额度错误,购买前定期USDT数量{},购买后定期USDT数量{}'.format(balance_amount_old,  balance_amount_latest)


                else:
                    assert False, "币种不对，购买定期产品失败。"

    @allure.testcase('test_saving_fix_006 购买定期产品最大额度')
    def test_saving_fix_006(self):
        sleep(5)
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            headers['X-Currency'] = 'USD'
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
        for i in r.json():
            logger.info('定期产品详情。 {}'.format(i))
            for y in i['products']:
                sleep(2)
                max_input = y['subscribe_attr']['user_single_subscribe_upper_limit']
                logger.info('定期产品product_id是{}'.format(y['product_id']))
                with allure.step("获取购买定期前BTC可用数量"):
                    balance_amount_old = AccountFunction.get_crypto_number(type='BTC',
                                                                           balance_type='BALANCE_TYPE_AVAILABLE',
                                                                           wallet_type='BALANCE')
                with allure.step("获取购买定期前BTC购买活期数量"):
                    saving_amount_old = AccountFunction.get_crypto_number(type='BTC',
                                                                          balance_type='BALANCE_TYPE_AVAILABLE',
                                                                          wallet_type='SAVING')
                with allure.step("获取购买定期前BTC购买定期数量"):
                    fix_amount_old = AccountFunction.get_crypto_number(type='BTC',
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
                        balance_amount_latest = AccountFunction.get_crypto_number(type='BTC',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前BTC购买活期数量"):
                        saving_amount_latest = AccountFunction.get_crypto_number(type='BTC',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前BTC购买定期数量"):
                        fix_amount_latest = AccountFunction.get_crypto_number(type='BTC',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'EARNINGTXN000014' in r.text, '购买定期产品最大额度错误, 返回值是{}'.format(r.text)
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
                        balance_amount_old = AccountFunction.get_crypto_number(type='ETH',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = AccountFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = AccountFunction.get_crypto_number(type='ETH',
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
                        balance_amount_latest = AccountFunction.get_crypto_number(type='ETH',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_latest = AccountFunction.get_crypto_number(type='ETH',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_latest = AccountFunction.get_crypto_number(type='ETH',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'EARNINGTXN000014' in r.text, '购买定期产品最大额度错误, 返回值是{}'.format(r.text)
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
                        balance_amount_old = AccountFunction.get_crypto_number(type='USDT',
                                                                               balance_type='BALANCE_TYPE_AVAILABLE',
                                                                               wallet_type='BALANCE')
                    with allure.step("获取购买定期前ETH购买活期数量"):
                        saving_amount_old = AccountFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING')
                    with allure.step("获取购买定期前ETH购买定期数量"):
                        fix_amount_old = AccountFunction.get_crypto_number(type='USDT',
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
                        balance_amount_latest = AccountFunction.get_crypto_number(type='USDT',
                                                                                  balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                  wallet_type='BALANCE')
                    with allure.step("获取购买定期前USDT购买活期数量"):
                        saving_amount_latest = AccountFunction.get_crypto_number(type='USDT',
                                                                                 balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                 wallet_type='SAVING')
                    with allure.step("获取购买定期前USDT购买定期数量"):
                        fix_amount_latest = AccountFunction.get_crypto_number(type='USDT',
                                                                              balance_type='BALANCE_TYPE_AVAILABLE',
                                                                              wallet_type='SAVING-FIX')
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'EARNINGTXN000014' in r.text, '购买定期产品最大额度错误, 返回值是{}'.format(r.text)
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

    @allure.testcase('test_saving_fix_007 项目不传预计派息金额')
    def test_saving_fix_007(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            headers['X-Currency'] = 'USD'
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

    @allure.testcase('test_saving_fix_008 项目传入错误预计派息金额')
    def test_saving_fix_008(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            headers['X-Currency'] = 'USD'
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

    @allure.testcase('test_saving_fix_009 查询申购项目的交易记录详情')
    def test_saving_fix_009(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            headers['X-Currency'] = 'USD'
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
            product_info = random.choice(random.choice(r.json())['products'])
        with allure.step("申购一笔项目"):
            logger.info('申购项目信息是{}'.format(product_info))
            data = {
                "subscribe_amount": {
                    "code": product_info['code'],
                    "amount": "0.00124"
                },
                "maturity_interest": {
                    "code": product_info['code'],
                    "amount": "0.01"
                }
            }
            if product_info['code'] == 'USDT':
                data['subscribe_amount']['amount'] = '30'
                data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * Decimal(
                    product_info['apy']) / Decimal(365)).quantize(Decimal('0.000000'), ROUND_FLOOR)) * Decimal(
                    product_info['tenor']))
            else:
                data['maturity_interest']['amount'] = str(((Decimal(data['subscribe_amount']['amount']) * Decimal(
                    product_info['apy']) / Decimal(365)).quantize(Decimal('0.00000000'), ROUND_FLOOR)) * Decimal(product_info['tenor']))
                r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, product_info['product_id']),
                                data=json.dumps(data), headers=headers)
                transaction_id = r.json()['tx_id']
                with allure.step("校验返回值"):
                    assert AccountFunction.get_transaction_status(transaction_id=transaction_id, type='3') == 2, '{}项目错误，购买定期产品失败，返回值是{}'.format(product_info['product_id'], r.text)
        with allure.step("查看交易记录详情"):
            r = session.request('GET', url='{}/earn/fix/transactions/{}'.format(env_url, transaction_id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert transaction_id in r.text, '查询申购项目的交易记录详情错误, 返回值是{}'.format(r.text)

    @allure.testcase('test_saving_fix_010 查询申购BTC项目的交易记录')
    def test_saving_fix_010(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            headers['X-Currency'] = 'USD'
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

    @allure.testcase('test_saving_fix_011 查询申购ETH项目的交易记录')
    def test_saving_fix_011(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            headers['X-Currency'] = 'USD'
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

    @allure.testcase('test_saving_fix_010 查询申购USDT项目的交易记录')
    def test_saving_fix_009(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            headers['X-Currency'] = 'USD'
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