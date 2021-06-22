from locust import HttpUser, task, between
from Function.api_function import *
import allure
import os


class MyUser(HttpUser):
    account_list = ['yilei6@cabital.com']
    wait_time = between(0.25, 0.5)

    @task(1)
    def core(self):
        accessToken = AccountFunction.get_account_token(account=random.choice(MyUser.account_list), password='Zcdsw123')
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        r = self.client.get(url="/core/account", headers=headers)
        if r.status_code == 200:
            print("success: {}".format(r.json()))
        else:
            print("failed: {}".format(r.text))

    @task(1)
    def cfx(self):
        accessToken = AccountFunction.get_account_token(account=random.choice(MyUser.account_list), password='Zcdsw123')
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        with allure.step("换汇交易"):
            List = ['BTC-ETH', 'BTC-USDT', 'ETH-USDT']
            # 获取换汇值
            for i in List:
                cryptos = i.split('-')
                with allure.step("major_ccy 是buy值，正兑换"):
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        buy_amount_wallet_balance = AccountFunction.get_crypto_number(type=cryptos[0])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = AccountFunction.get_crypto_number(type=cryptos[1])
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
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[0], cryptos[1]))
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
                        buy_amount_wallet_balance_latest = AccountFunction.get_crypto_number(type=cryptos[0])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = AccountFunction.get_crypto_number(type=cryptos[1])
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
                        buy_amount_wallet_balance = AccountFunction.get_crypto_number(type=cryptos[1])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = AccountFunction.get_crypto_number(type=cryptos[0])
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
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[1], cryptos[0]))
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
                        buy_amount_wallet_balance_latest = AccountFunction.get_crypto_number(type=cryptos[1])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = AccountFunction.get_crypto_number(type=cryptos[0])
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
                        buy_amount_wallet_balance = AccountFunction.get_crypto_number(type=cryptos[0])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = AccountFunction.get_crypto_number(type=cryptos[1])
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
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[0], cryptos[1]))
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
                        buy_amount_wallet_balance_latest = AccountFunction.get_crypto_number(type=cryptos[0])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = AccountFunction.get_crypto_number(type=cryptos[1])
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
                        buy_amount_wallet_balance = AccountFunction.get_crypto_number(type=cryptos[1])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = AccountFunction.get_crypto_number(type=cryptos[0])
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
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[1], cryptos[0]))
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
                        buy_amount_wallet_balance_latest = AccountFunction.get_crypto_number(type=cryptos[1])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = AccountFunction.get_crypto_number(type=cryptos[0])
                    logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[1],
                                                                                  buy_amount_wallet_balance,
                                                                                  buy_amount,
                                                                                  buy_amount_wallet_balance_latest))
                    logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[0],
                                                                                    sell_amount_wallet_balance,
                                                                                    sell_amount,
                                                                                    sell_amount_wallet_balance_latest))


if __name__ == "__main__":
    os.system("locust -f press.py --host={}".format(get_json()['test']))
