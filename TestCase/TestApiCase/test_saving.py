from Function.api_function import *
from run import *
from Function.log import *
import allure


# saving相关cases
class TestSavingApi:

    @allure.testcase('test_saving_001 获取产品列表')
    def test_saving_001(self):
        with allure.step("获取产品列表"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "获取产品列表错误，返回值是{}".format(r.text)

    @allure.testcase('test_saving_002 获取产品详情')
    def test_saving_002(self):
        with allure.step("获取产品product_id"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product_id = []
            for i in r.json():
                product_id.append(i['product_id'])
        with allure.step("获取产品详情"):
            # 随机获取一个id
            id = random.choice(product_id)
            logger.info('id是{}'.format(id))
            r = requests.request('GET', url='{}/earn/products/{}'.format(env_url, id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "获取产品详情错误，返回值是{}".format(r.text)

    @allure.testcase('test_saving_003 获取利息列表')
    def test_saving_003(self):
        with allure.step("获取产品product_id"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product_id = []
            for i in r.json():
                product_id.append(i['product_id'])
        with allure.step("获取利息列表"):
            # 随机获取一个id
            id = random.choice(product_id)
            logger.info('id是{}'.format(id))
            params = {
                "cursor": 0,
                "size": 30
            }
            r = requests.request('GET', url='{}/earn/products/{}/interests'.format(env_url, id), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'items' in r.text, "获取利息列表错误，返回值是{}".format(r.text)

    @allure.testcase('test_saving_004 获取交易记录')
    def test_saving_004(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取产品product_id"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product_id = []
            for i in r.json():
                product_id.append(i['product_id'])
        with allure.step("获取交易记录"):
            # 随机获取一个id
            id = random.choice(product_id)
            logger.info('id是{}'.format(id))
            params = {
                "tx_type": 1,
                "cursor": 0,
                "size": 30
            }
            r = requests.request('GET', url='{}/earn/products/{}/transactions'.format(env_url, id), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'items' in r.text, "获取交易记录错误，返回值是{}".format(r.text)

    @allure.testcase('test_saving_005 有足够BTC的用户发起购买BTC投资项目成功')
    def test_saving_005(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取产品product_id"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择BTC投资项目"):
            BTCList = []
            for i in r.json():
                if i['code'] == 'BTC':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
            print(BTC_item)
        with allure.step("有足够BTC的用户发起购买BTC投资项目成功"):
            data = {
                "tx_type": 1,
                "amount": "0.00087",
                "code": BTC_item['code']
            }
            r = requests.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'tx_id' in r.text, "有足够BTC的用户发起购买BTC投资项目成功错误，返回值是{}".format(r.text)

    @allure.testcase('test_saving_006 有足够ETH的用户发起购买ETH投资项目成功')
    def test_saving_006(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取产品product_id"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择ETH投资项目"):
            BTCList = []
            for i in r.json():
                if i['code'] == 'ETH':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
        with allure.step("有足够ETH的用户发起购买ETH投资项目成功"):
            data = {
                "tx_type": 1,
                "amount": "0.00167",
                "code": BTC_item['code']
            }
            r = requests.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'tx_id' in r.text, "有足够ETH的用户发起购买ETH投资项目成功错误，返回值是{}".format(r.text)

    @allure.testcase('test_saving_007 有足够USDT的用户发起购买USDT投资项目成功')
    def test_saving_007(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取产品product_id"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择USDT投资项目"):
            BTCList = []
            for i in r.json():
                if i['code'] == 'USDT':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
        with allure.step("有足够BTC的用户发起购买USDT投资项目成功"):
            data = {
                "tx_type": 1,
                "amount": "22",
                "code": BTC_item['code']
            }
            r = requests.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'tx_id' in r.text, "有足够USDT的用户发起购买USDT投资项目成功错误，返回值是{}".format(r.text)

    @allure.testcase('test_saving_008 投资金额小于最小投资BTC数量')
    def test_saving_008(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取产品product_id"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择ETH投资项目"):
            BTCList = []
            for i in r.json():
                if i['code'] == 'BTC':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
        with allure.step("投资金额小于最小投资BTC数量"):
            data = {
                "tx_type": 1,
                "amount": "0.00000000167",
                "code": BTC_item['code']
            }
            r = requests.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'amount < min amount' in r.text, "投资金额小于最小投资BTC数量错误，返回值是{}".format(r.text)

    @allure.testcase('test_saving_009 投资金额小于最小投资ETH数量')
    def test_saving_009(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取产品product_id"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择ETH投资项目"):
            BTCList = []
            for i in r.json():
                if i['code'] == 'ETH':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
        with allure.step("投资金额小于最小投资ETH数量"):
            data = {
                "tx_type": 1,
                "amount": "0.00167",
                "code": BTC_item['code']
            }
            r = requests.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'tx_id' in r.text, "投资金额小于最小投资ETH数量错误，返回值是{}".format(r.text)

    @allure.testcase('test_saving_010 投资金额小于最小投资USDT数量')
    def test_saving_010(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取产品product_id"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择ETH投资项目"):
            BTCList = []
            for i in r.json():
                if i['code'] == 'USDT':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
        with allure.step("投资金额小于最小投资USDT数量"):
            data = {
                "tx_type": 1,
                "amount": "0.1",
                "code": BTC_item['code']
            }
            r = requests.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'EARNINGTXN000013' in r.text, "投资金额小于最小投资USDT数量错误，返回值是{}".format(r.text)

    @allure.testcase('test_saving_011 获取产品持有情况')
    def test_saving_0011(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取产品product_id"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product_id = []
            for i in r.json():
                product_id.append(i['product_id'])
        with allure.step("获取产品持有情况"):
            # 随机获取一个id
            id = random.choice(product_id)
            logger.info('id是{}'.format(id))
            r = requests.request('GET', url='{}/earn/products/{}/summary'.format(env_url, id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'total_holding' in r.text, "获取产品持有情况错误，返回值是{}".format(r.text)

    @allure.testcase('test_saving_012 赎回已经投资的ETH项目')
    def test_saving_010(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取产品product_id"):
            r = requests.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择ETH投资项目"):
            BTCList = []
            for i in r.json():
                if i['code'] == 'ETH':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
        with allure.step("投资金额小于最小投资USDT数量"):
            data = {
                "tx_type": 2,
                "amount": "0.0001",
                "code": BTC_item['code']
            }
            r = requests.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'tx_id' in r.text, "投资金额小于最小投资USDT数量错误，返回值是{}".format(r.text)
