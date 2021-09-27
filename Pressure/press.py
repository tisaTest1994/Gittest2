from locust import HttpUser, task, between
from Function.api_function import *
import allure
import os


class MyUser(HttpUser):
    account_list = get_json()['account_list']
    wait_time = between(0.2, 0.5)

    @task(2)
    def core(self):
        accessToken = ApiFunction.get_account_token(account=random.choice(MyUser.account_list), password='Zcdsw123')
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        r = self.client.get(url="/core/account", headers=headers)
        if r.status_code == 200:
            print("success: {}".format(r.json()))
        else:
            print("failed: status code is {}, 返回值是 {}".format(r.status_code, r.text))

    @task(0)
    def cfx(self):
        accessToken = ApiFunction.get_account_token(account=random.choice(MyUser.account_list), password='Zcdsw123')
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        with allure.step("换汇交易"):
            List = ['BTC-ETH', 'BTC-USDT', 'ETH-USDT']
            # 获取换汇值
            for i in List:
                cryptos = i.split('-')
                with allure.step("major_ccy 是buy值，正兑换"):
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        buy_amount_wallet_balance = ApiFunction.get_crypto_number(type=cryptos[0])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = ApiFunction.get_crypto_number(type=cryptos[1])
                    if cryptos[0] == 'BTC' or cryptos[0] == 'ETH':
                        buy_amount = random.uniform(0.01, 0.19)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:8])
                    elif cryptos[0] == 'USDT':
                        buy_amount = random.uniform(20, 40.10)
                        if len(str(buy_amount).split('.')[1]) >= 6:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:6])
                    else:
                        buy_amount = random.uniform(20, 40.10)
                        if len(str(buy_amount).split('.')[1]) >= 2:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:2])
                    quote = ApiFunction.get_quote('{}-{}'.format(cryptos[0], cryptos[1]))
                    sell_amount = str(float(buy_amount) * float(quote['quote']))
                    if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                        if len(str(sell_amount).split('.')[1]) >= 8:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    elif cryptos[1] == 'USDT':
                        if len(str(sell_amount).split('.')[1]) >= 6:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:6])
                    else:
                        if len(str(sell_amount).split('.')[1]) >= 2:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:2])
                    data = {
                        "quote_id": quote['quote_id'],
                        "quote": quote['quote'],
                        "pair": '{}-{}'.format(cryptos[0], cryptos[1]),
                        "buy_amount": str(buy_amount),
                        "sell_amount": str(sell_amount),
                        "major_ccy": cryptos[0]
                    }
                    r = self.client.post(url='{}/txn/cfx'.format(env_url), data=json.dumps(data),
                                        headers=headers)
                    logger.info('申请换汇参数{}'.format(data))
                    sleep(8)
                    logger.info('换汇返回值{}'.format(r.text))
                    assert r.json()['transaction']['status'] == 2, '换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r.text)
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=cryptos[0])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=cryptos[1])
                    logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[0],
                                                                                  buy_amount_wallet_balance,
                                                                                  buy_amount,
                                                                                  buy_amount_wallet_balance_latest))
                    logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[1],
                                                                                    sell_amount_wallet_balance,
                                                                                    sell_amount,
                                                                                    sell_amount_wallet_balance_latest))
                with allure.step("major_ccy 是buy值，逆兑换 "):
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        buy_amount_wallet_balance = ApiFunction.get_crypto_number(type=cryptos[1])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = ApiFunction.get_crypto_number(type=cryptos[0])
                    if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                        buy_amount = random.uniform(0.01, 0.19)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:8])
                    elif cryptos[1] == 'USDT':
                        buy_amount = random.uniform(20, 40.10)
                        if len(str(buy_amount).split('.')[1]) >= 6:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:6])
                    else:
                        buy_amount = random.uniform(20, 40.10)
                        if len(str(buy_amount).split('.')[1]) >= 2:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:2])
                    quote = ApiFunction.get_quote('{}-{}'.format(cryptos[1], cryptos[0]))
                    sell_amount = str(float(buy_amount) * float(quote['quote']))
                    if cryptos[0] == 'BTC' or cryptos[0] == 'ETH':
                        if len(str(sell_amount).split('.')[1]) >= 8:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    elif cryptos[0] == 'USDT':
                        if len(str(sell_amount).split('.')[1]) >= 6:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:6])
                    else:
                        if len(str(sell_amount).split('.')[1]) >= 2:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:2])
                    data = {
                        "quote_id": quote['quote_id'],
                        "quote": quote['quote'],
                        "pair": '{}-{}'.format(cryptos[1], cryptos[0]),
                        "buy_amount": str(buy_amount),
                        "sell_amount": str(sell_amount),
                        "major_ccy": cryptos[1]
                    }
                    r1 = self.client.post(url='{}/txn/cfx'.format(env_url), data=json.dumps(data),
                                         headers=headers)
                    logger.info('申请换汇参数{}'.format(data))
                    sleep(8)
                    logger.info('换汇返回值{}'.format(r1.text))
                    assert r1.json()['transaction']['status'] == 2, '换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r1.text)
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=cryptos[1])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=cryptos[0])
                    logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[1],
                                                                                  buy_amount_wallet_balance,
                                                                                  buy_amount,
                                                                                  buy_amount_wallet_balance_latest))
                    logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[0],
                                                                                    sell_amount_wallet_balance,
                                                                                    sell_amount,
                                                                                    sell_amount_wallet_balance_latest))
                with allure.step("major_ccy 是sell值，正兑换 "):
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        buy_amount_wallet_balance = ApiFunction.get_crypto_number(type=cryptos[0])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = ApiFunction.get_crypto_number(type=cryptos[1])
                    if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                        sell_amount = random.uniform(0.01, 0.19)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    elif cryptos[1] == 'USDT':
                        sell_amount = random.uniform(20, 40.10)
                        if len(str(sell_amount).split('.')[1]) >= 6:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:6])
                    else:
                        sell_amount = random.uniform(20, 40.10)
                        if len(str(sell_amount).split('.')[1]) >= 2:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:2])
                    quote = ApiFunction.get_quote('{}-{}'.format(cryptos[0], cryptos[1]))
                    buy_amount = str(float(sell_amount) / float(quote['quote']))
                    if cryptos[0] == 'BTC' or cryptos[0] == 'ETH':
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:8])
                    elif cryptos[0] == 'USDT':
                        if len(str(buy_amount).split('.')[1]) >= 6:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:6])
                    else:
                        if len(str(buy_amount).split('.')[1]) >= 2:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:2])
                    data = {
                        "quote_id": quote['quote_id'],
                        "quote": quote['quote'],
                        "pair": '{}-{}'.format(cryptos[0], cryptos[1]),
                        "buy_amount": str(buy_amount),
                        "sell_amount": str(sell_amount),
                        "major_ccy": cryptos[1]
                    }
                    r2 = self.client.post(url='{}/txn/cfx'.format(env_url), data=json.dumps(data),
                                         headers=headers)
                    logger.info('申请换汇参数{}'.format(data))
                    sleep(8)
                    logger.info('换汇返回值{}'.format(r2.text))
                    assert r2.json()['transaction']['status'] == 2, '换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r2.text)
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=cryptos[0])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=cryptos[1])
                    logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[0],
                                                                                  buy_amount_wallet_balance,
                                                                                  buy_amount,
                                                                                  buy_amount_wallet_balance_latest))
                    logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[1],
                                                                                    sell_amount_wallet_balance,
                                                                                    sell_amount,
                                                                                    sell_amount_wallet_balance_latest))
                with allure.step("major_ccy 是sell值，逆兑换"):
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        buy_amount_wallet_balance = ApiFunction.get_crypto_number(type=cryptos[1])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = ApiFunction.get_crypto_number(type=cryptos[0])
                    if cryptos[0] == 'BTC' or cryptos[0] == 'ETH':
                        sell_amount = random.uniform(0.01, 0.19)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    elif cryptos[0] == 'USDT':
                        sell_amount = random.uniform(20, 40.10)
                        if len(str(sell_amount).split('.')[1]) >= 6:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:6])
                    else:
                        sell_amount = random.uniform(20, 40.10)
                        if len(str(sell_amount).split('.')[1]) >= 2:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:2])
                    quote = ApiFunction.get_quote('{}-{}'.format(cryptos[1], cryptos[0]))
                    buy_amount = str(float(sell_amount) / float(quote['quote']))
                    if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:8])
                    elif cryptos[1] == 'USDT':
                        if len(str(buy_amount).split('.')[1]) >= 6:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:6])
                    else:
                        if len(str(buy_amount).split('.')[1]) >= 2:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:2])
                    data = {
                        "quote_id": quote['quote_id'],
                        "quote": quote['quote'],
                        "pair": '{}-{}'.format(cryptos[1], cryptos[0]),
                        "buy_amount": str(buy_amount),
                        "sell_amount": str(sell_amount),
                        "major_ccy": cryptos[0]
                    }
                    r3 = self.client.post(url='{}/txn/cfx'.format(env_url), data=json.dumps(data),
                                         headers=headers)
                    logger.info('申请换汇参数{}'.format(data))
                    sleep(8)
                    logger.info('换汇返回值{}'.format(r3.text))
                    assert r3.json()['transaction']['status'] == 2, '换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r3.text)
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=cryptos[1])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=cryptos[0])
                    logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[1],
                                                                                  buy_amount_wallet_balance,
                                                                                  buy_amount,
                                                                                  buy_amount_wallet_balance_latest))
                    logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[0],
                                                                                    sell_amount_wallet_balance,
                                                                                    sell_amount,
                                                                                    sell_amount_wallet_balance_latest))

    @task(0)
    def earn_current(self):
        accessToken = ApiFunction.get_account_token(account=random.choice(MyUser.account_list), password='Zcdsw123')
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        data = {
            "tx_type": 1,
            "amount": "0.02327",
            "code": 'ETH'
        }
        r = self.client.post(url='{}/earn/products/a1220392-194c-432c-a961-eff561bb72b2/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        if r.status_code == 200:
            print("success: {}".format(r.json()))
        else:
            print("failed: status code is {}, 返回值是 {}".format(r.status_code, r.text))

    @task(0)
    def redeem_current(self):
        accessToken = ApiFunction.get_account_token(account=random.choice(MyUser.account_list), password='Zcdsw123')
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        data = {
            "tx_type": 2,
            "amount": "0.00087",
            "code": 'ETH'
        }
        r = self.client.post(url='{}/earn/products/a1220392-194c-432c-a961-eff561bb72b2/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        if r.status_code == 200:
            print("success: {}".format(r.json()))
        else:
            print("failed: status code is {}, 返回值是 {}".format(r.status_code, r.text))

    @task(0)
    def fixed(self):
        accessToken = ApiFunction.get_account_token(account=random.choice(MyUser.account_list), password='Zcdsw123')
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        with allure.step("获取定期产品列表"):
            r = self.client.get(url='{}/earn/fix/products'.format(env_url), headers=headers)
        for i in r.json():
            for y in i['products']:
                sleep(5)
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
                    r = self.client.post(url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']), data=json.dumps(data), headers=headers)
                    if r.status_code == 200:
                        print("success: {}".format(r.json()))
                    else:
                        print("failed: status code is {}, 返回值是 {}".format(r.status_code, r.text))
                elif i['code'] == 'ETH':
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
                    r = self.client.post(url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']), data=json.dumps(data), headers=headers)
                    if r.status_code == 200:
                        print("success: {}".format(r.json()))
                    else:
                        print("failed: status code is {}, 返回值是 {}".format(r.status_code, r.text))
                elif i['code'] == 'USDT':
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
                    r = self.client.post(url='{}/earn/fix/products/{}/transactions'.format(env_url, y['product_id']), data=json.dumps(data), headers=headers)
                    if r.status_code == 200:
                        print("success: {}".format(r.json()))
                    else:
                        print("failed: status code is {}, 返回值是 {}".format(r.status_code, r.text))

    @task(0)
    def get_market(self):
        for i in ['BTCEUR', 'BTCUSD', 'ETHEUR', 'ETHUSD', 'USDEUR']:
            for y in ['10', '60', 'D', 'W', 'M']:
                params = {
                    "pair": i,
                    "interval": y,
                    "from_time": "0",
                    "to_time": str(datetime.now().timestamp()).split('.')[0]
                }
                r = self.client.get(url='{}/marketstat/public/quote-chart'.format(env_url), params=params)
                if r.status_code == 200:
                    print("success: {}".format(r.json()))
                else:
                    print("failed: status code is {}, 返回值是 {}".format(r.status_code, r.text))


if __name__ == "__main__":
    os.system("locust -f press.py --host={}".format(get_json()['test']))
