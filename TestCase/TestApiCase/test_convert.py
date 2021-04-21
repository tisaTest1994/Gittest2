from Function.api_function import *
from run import *
from Function.log import *
import allure


# convert相关cases
class TestConvertApi:

    @allure.testcase('test_convert_001 查询单笔交易')
    def test_convert_001(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获得交易transaction_id"):
            transaction_id = AccountFunction.get_payout_transaction_id()
        with allure.step("查询单笔交易"):
            params = {
                "txn_type": 2,
                "txn_sub_type": "withdraw"
            }
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "获取产品列表错误，返回值是{}".format(r.text)

    @allure.testcase('test_convert_002 查询特定条件的交易')
    def test_convert_002(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "cursor": "0",
                "page_size": 10
            },
            "user_txn_sub_types": [3, 5],
            "statuses": [1, 2, 3, 4],
            "codes": ["BTC"]
        }
        with allure.step("查询特定条件的交易"):
            r = requests.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "获取产品列表错误，返回值是{}".format(r.text)

    @allure.testcase('test_convert_003 查询换汇交易限制')
    def test_convert_003(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询换汇交易限制"):
            r = requests.request('GET', url='{}/txn/cfx/restriction'.format(env_url), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'restrictions' in r.text, "获取产品列表错误，返回值是{}".format(r.text)

    @allure.testcase('test_convert_004 换汇交易')
    def test_convert_004(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("换汇交易"):
            List = ['BTC-ETH', 'BTC-USDT', 'BTC-GBP', 'BTC-EUR', 'ETH-USDT', 'ETH-GBP', 'ETH-EUR', 'USDT-GBP', 'USDT-EUR']
            for i in List:
                cryptos = i.split('-')
                if cryptos[0] == 'BTC':
                    buy_amount = random.uniform(0.1, 0.9)
                    if len(str(buy_amount)) >= 8:
                        buy_amount = str(buy_amount)[:8]
                    else:
                        buy_amount = str(buy_amount)
                elif cryptos[0] == 'ETH':
                    buy_amount = random.uniform(0.1, 0.9)
                    if len(str(buy_amount)) >= 6:
                        buy_amount = str(buy_amount)[:6]
                    else:
                        buy_amount = str(buy_amount)
                else:
                    buy_amount = random.randint(100, 2000)
                r = requests.request('GET', url='{}/core/quotes/{}'.format(env_url, i), headers=headers)
                sell_amount = str(float(buy_amount) * float(r.json()['quote']))
                if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                    if len(str(sell_amount).split('.')[1]) >= 8:
                        sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0], str(sell_amount).split('.')[1][:8])
                else:
                    if len(str(sell_amount).split('.')[1]) >= 2:
                        sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0], str(sell_amount).split('.')[1][:2])
                with allure.step("查询{}兑换比例".format(i)):
                    r = requests.request('GET', url='{}/core/quotes/{}'.format(env_url, i), headers=headers)
                data = {
                    "quote_id": r.json()['quote_id'],
                    "quote": r.json()['quote'],
                    "pair": i,
                    "buy_amount": buy_amount,
                    "sell_amount": sell_amount,
                    "major_ccy": i.split("-")[0]
                }
                r = requests.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data), headers=headers)
                print(data)
                print(r.text)
