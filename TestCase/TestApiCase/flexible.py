from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api flexible 相关 testcases")
class TestFlexibleApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_flexible_001')
    @allure.description('获取产品列表')
    def test_flexible_001(self):
        with allure.step("获取产品列表"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert len(r.json()) >= 1, '至少有一个活期项目'
                for i in r.json():
                    assert i['name_code'] != '', '获取产品列表错误'

    @allure.title('test_flexible_002')
    @allure.description('通过产品id获取id产品的详情')
    def test_flexible_002(self):
        with allure.step("获取产品product_id"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product_id = []
            for i in r.json():
                product_id.append(i['product_id'])
        with allure.step("通过产品id获取id产品的详情"):
            # 随机获取一个id
            id = random.choice(product_id)
            logger.info('产品id是{}'.format(id))
            r = session.request('GET', url='{}/earn/products/{}'.format(env_url, id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "通过产品id获取id产品的详情错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_003')
    @allure.description('获取今日之后的利息列表')
    def test_flexible_003(self):
        with allure.step("获取产品product_id"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product_id = []
            for i in r.json():
                product_id.append(i['product_id'])
        with allure.step("获取今日之后的利息列表"):
            # 随机获取一个id
            id = random.choice(product_id)
            logger.info('id是{}'.format(id))
            params = {
                "cursor": 0,
                "size": 30
            }
            r = session.request('GET', url='{}/earn/products/{}/interests'.format(env_url, id), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'items' in r.text, "获取今日之后的利息列表错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_004')
    @allure.description('获取交易记录')
    def test_flexible_004(self):
        with allure.step("获取产品product_id"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
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
            r = session.request('GET', url='{}/earn/products/{}/transactions'.format(env_url, id), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'items' in r.text, "获取多条交易记录错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_005')
    @allure.description('有足够BTC的用户发起购买BTC投资项目成功')
    def test_flexible_005(self):
        with allure.step("获取产品product_id"):
            r1 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择BTC投资项目"):
            BTCList = []
            for i in r1.json():
                if i['code'] == 'BTC':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
        with allure.step("获得投资前，目前持有总数"):
            r2 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, BTC_item['product_id']), headers=headers)
            total_holding_old = r2.json()['total_holding']['amount']
            logger.info('投资btc前，目前持有项目的btc数量是{}'.format(total_holding_old))
        with allure.step("投资前，查询钱包可用btc金额"):
            r3 = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
            for i in r3.json():
                if i['code'] == 'BTC' and i['wallet_type'] == 'BALANCE':
                    for y in i['balances']:
                        if y['type'] == 'BALANCE_TYPE_AVAILABLE':
                            balance_type_available_amount_old = y['amount']
            logger.info('投资btc前，目前持有可用的btc数量是{}'.format(balance_type_available_amount_old))
        with allure.step("有足够BTC的用户发起购买BTC投资项目成功"):
            data = {
                "tx_type": 1,
                "amount": "0.0087",
                "code": BTC_item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            sleep(2)
            with allure.step("获得投资后，目前持有总数"):
                r4 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, BTC_item['product_id']), headers=headers)
                total_holding_latest = r4.json()['total_holding']['amount']
                logger.info('投资btc后，目前持有项目的btc数量是{}'.format(total_holding_latest))
            with allure.step("投资后，查询钱包可用btc金额"):
                r3 = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
                for i in r3.json():
                    if i['code'] == 'BTC' and i['wallet_type'] == 'BALANCE':
                        for y in i['balances']:
                            if y['type'] == 'BALANCE_TYPE_AVAILABLE':
                                balance_type_available_amount_latest = y['amount']
                logger.info('投资btc后，目前持有可用的btc数量是{}'.format(balance_type_available_amount_latest))
            with allure.step("校验返回值"):
                logger.info('本次投资是{}'.format(data['amount']))
                assert Decimal(total_holding_old) + Decimal(data['amount']) == Decimal(total_holding_latest), \
                    "有足够BTC的用户发起购买BTC投资项目,投资金额（total_holding）错误，返回值是{}".format(r.text)
                assert Decimal(balance_type_available_amount_old) - Decimal(data['amount']) == Decimal(balance_type_available_amount_latest), \
                    "有足够BTC的用户发起购买BTC投资项目,剩余可用资金错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_006')
    @allure.description('有足够ETH的用户发起购买ETH投资项目成功')
    def test_flexible_006(self):
        with allure.step("获取产品product_id"):
            r1 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择ETH投资项目"):
            List = []
            for i in r1.json():
                if i['code'] == 'ETH':
                    List.append(i)
            if len(List) >= 1:
                item = random.choice(List)
        with allure.step("获得投资前，目前持有总数"):
            r2 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, item['product_id']), headers=headers)
            total_holding_old = r2.json()['total_holding']['amount']
            logger.info('投资ETH前，目前持有项目的ETH数量是{}'.format(total_holding_old))
        with allure.step("投资前，查询钱包可用ETH金额"):
            r3 = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
            for i in r3.json():
                if i['code'] == 'ETH' and i['wallet_type'] == 'BALANCE':
                    for y in i['balances']:
                        if y['type'] == 'BALANCE_TYPE_AVAILABLE':
                            balance_type_available_amount_old = y['amount']
            logger.info('投资ETH前，目前持有可用的ETH数量是{}'.format(balance_type_available_amount_old))
        with allure.step("有足够ETH的用户发起购买ETH投资项目成功"):
            data = {
                "tx_type": 1,
                "amount": "0.06327",
                "code": item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, item['product_id']), data=json.dumps(data), headers=headers)
            sleep(2)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("获得投资后，目前持有总数"):
                r4 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, item['product_id']), headers=headers)
                total_holding_latest = r4.json()['total_holding']['amount']
                logger.info('投资ETH后，目前持有项目的ETH数量是{}'.format(total_holding_latest))
            with allure.step("投资后，查询钱包可用ETH金额"):
                r3 = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
                for i in r3.json():
                    if i['code'] == 'ETH' and i['wallet_type'] == 'BALANCE':
                        for y in i['balances']:
                            if y['type'] == 'BALANCE_TYPE_AVAILABLE':
                                balance_type_available_amount_latest = y['amount']
                logger.info('投资ETH后，目前持有可用的ETH数量是{}'.format(balance_type_available_amount_latest))
            with allure.step("校验返回值"):
                logger.info('本次投资是{}'.format(data['amount']))
                assert Decimal(total_holding_old) + Decimal(data['amount']) == Decimal(total_holding_latest), \
                    "有足够ETH的用户发起购买ETH投资项目,投资金额（total_holding）错误，返回值是{}".format(r.text)
                assert Decimal(balance_type_available_amount_old) - Decimal(data['amount']) == Decimal(balance_type_available_amount_latest), \
                    "有足够ETH的用户发起购买ETH投资项目,剩余可用资金错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_007')
    @allure.description('有足够USDT的用户发起购买USDT投资项目成功')
    def test_flexible_007(self):
        with allure.step("获取产品product_id"):
            r1 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择USDT投资项目"):
            BTCList = []
            for i in r1.json():
                if i['code'] == 'USDT':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
        with allure.step("获得投资前，目前持有总数"):
            r2 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, BTC_item['product_id']), headers=headers)
            total_holding_old = r2.json()['total_holding']['amount']
            logger.info('投资USDT前，目前持有项目的USDT数量是{}'.format(total_holding_old))
        with allure.step("投资前，查询钱包可用USDT金额"):
            r3 = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
            for i in r3.json():
                if i['code'] == 'USDT' and i['wallet_type'] == 'BALANCE':
                    for y in i['balances']:
                        if y['type'] == 'BALANCE_TYPE_AVAILABLE':
                            balance_type_available_amount_old = y['amount']
            logger.info('投资USDT前，目前持有可用的USDT数量是{}'.format(balance_type_available_amount_old))
        with allure.step("有足够USDT的用户发起购买USDT投资项目成功"):
            data = {
                "tx_type": 1,
                "amount": "51.17",
                "code": BTC_item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            sleep(2)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("获得投资后，目前持有总数"):
                r4 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, BTC_item['product_id']),
                                      headers=headers)
                total_holding_latest = r4.json()['total_holding']['amount']
                logger.info('投资USDT后，目前持有项目的USDT数量是{}'.format(total_holding_latest))
            with allure.step("投资后，查询钱包可用USDT金额"):
                r3 = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
                for i in r3.json():
                    if i['code'] == 'USDT' and i['wallet_type'] == 'BALANCE':
                        for y in i['balances']:
                            if y['type'] == 'BALANCE_TYPE_AVAILABLE':
                                balance_type_available_amount_latest = y['amount']
                logger.info('投资USDT后，目前持有可用的USDT数量是{}'.format(balance_type_available_amount_latest))
            with allure.step("校验返回值"):
                logger.info('本次投资是{}'.format(data['amount']))
                assert Decimal(total_holding_old) + Decimal(data['amount']) == Decimal(total_holding_latest), \
                    "有足够BTC的用户发起购买USDT投资项目,投资金额（total_holding）错误，返回值是{}".format(r.text)
                assert Decimal(balance_type_available_amount_old) - Decimal(data['amount']) == Decimal(balance_type_available_amount_latest), \
                    "有足够BTC的用户发起购买USDT投资项目,剩余可用资金错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_008')
    @allure.description('投资金额小于最小投资BTC数量')
    def test_flexible_008(self):
        with allure.step("获取产品product_id"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
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
                "amount": "0.00000167",
                "code": BTC_item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '104002', "投资金额小于最小投资BTC数量错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_009')
    @allure.description('投资金额使用非常小的ETH数量判定无效')
    def test_flexible_009(self):
        with allure.step("获取产品product_id"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
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
                "amount": "0.00000000167",
                "code": BTC_item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '104016', "投资金额小于最小投资ETH数量错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_010')
    @allure.description('投资金额小于最小投资USDT数量')
    def test_flexible_010(self):
        with allure.step("获取产品product_id"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
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
                "amount": "0.009",
                "code": BTC_item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '104002', "投资金额小于最小投资USDT数量错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_011')
    @allure.description('获取产品持有情况')
    def test_flexible_011(self):
        with allure.step("获取产品product_id"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product_id = []
            for i in r.json():
                product_id.append(i['product_id'])
        with allure.step("获取产品持有情况"):
            # 随机获取一个id
            id = random.choice(product_id)
            logger.info('id是{}'.format(id))
            r = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'total_holding' in r.text, "获取产品持有情况错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_012')
    @allure.description('赎回BTC投资项目成功')
    def test_flexible_012(self):
        with allure.step("获取产品product_id"):
            r1 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择BTC投资项目"):
            BTCList = []
            for i in r1.json():
                if i['code'] == 'BTC':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
                logger.info('产品信息是{}'.format(BTC_item))
        with allure.step("赎回项目前，总共持有金额"):
            r2 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, BTC_item['product_id']), headers=headers)
            total_holding_old = r2.json()['total_holding']['amount']
            logger.info('赎回项目前，总共持有金额数量是{}'.format(total_holding_old))
        with allure.step("赎回项目前，可计息金额"):
            accruing_amount_old = r2.json()['accruing_amount']['amount']
            logger.info('赎回项目前，可计息金额数量是{}'.format(accruing_amount_old))
        with allure.step("赎回项目前，今天申购金额"):
            subscribing_amount_old = r2.json()['subscribing_amount']['amount']
            logger.info('赎回项目前，今天申购金额数量是{}'.format(subscribing_amount_old))
        with allure.step("赎回项目前，可赎回金额"):
            redeemable_amount_old = r2.json()['redeemable_amount']['amount']
            logger.info('赎回项目前，可赎回金额数量是{}'.format(redeemable_amount_old))
        with allure.step("赎回项目前，赎回中金额"):
            redeeming_amount_old = r2.json()['redeeming_amount']['amount']
            logger.info('赎回项目前，赎回中金额数量是{}'.format(redeeming_amount_old))
        with allure.step("赎回项目前，检查可赎回金额 + 正在赎回金额 = 总持有金额"):
            assert Decimal(redeemable_amount_old) + Decimal(redeeming_amount_old) == Decimal(total_holding_old), \
                "，检查可赎回金额 + 正在赎回金额 != 总持有金额"
        with allure.step("赎回BTC投资项目成功"):
            data = {
                "tx_type": 2,
                "amount": "0.00087",
                "code": BTC_item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            sleep(2)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("赎回项目后，总共持有金额"):
                r5 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, BTC_item['product_id']),
                                      headers=headers)
                accruing_amount_latest = r5.json()['accruing_amount']['amount']
                logger.info('赎回项目后，总共持有金额数量是{}'.format(accruing_amount_latest))
            with allure.step("赎回项目后，今天申购金额"):
                subscribing_amount_latest = r5.json()['subscribing_amount']['amount']
                logger.info('赎回项目后，今天申购金额数量是{}'.format(subscribing_amount_latest))
            with allure.step("赎回项目后，可赎回金额"):
                redeemable_amount_latest = r5.json()['redeemable_amount']['amount']
                logger.info('赎回项目后，可赎回金额数量是{}'.format(redeemable_amount_latest))
            with allure.step("赎回项目后，赎回中金额"):
                redeeming_amount_latest = r5.json()['redeeming_amount']['amount']
                logger.info('赎回项目后，赎回中金额数量是{}'.format(redeeming_amount_latest))
            with allure.step("校验返回值"):
                logger.info('本次赎回是{}'.format(data['amount']))
            with allure.step("赎回项目后，检查可赎回金额 + 正在赎回金额 = 总持有金额"):
                assert Decimal(redeemable_amount_old) + Decimal(redeeming_amount_old) == Decimal(total_holding_old), "检查可赎回金额 + 正在赎回金额 != 总持有金额"
            with allure.step("赎回项目后，之前正在赎回金额 + 赎回金额 = 当前正在赎回金额"):
                assert Decimal(redeeming_amount_old) + Decimal(data['amount']) == Decimal(redeeming_amount_latest), "之前正在赎回金额 + 赎回金额 = 当前正在赎回金额"

    @allure.title('test_flexible_013')
    @allure.description('赎回ETH投资项目成功')
    def test_flexible_013(self):
        with allure.step("获取产品product_id"):
            r1 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择ETH投资项目"):
            BTCList = []
            for i in r1.json():
                if i['code'] == 'ETH':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
                logger.info('产品信息是{}'.format(BTC_item))
        with allure.step("赎回项目前，总共持有金额"):
            r2 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, BTC_item['product_id']), headers=headers)
            total_holding_old = r2.json()['total_holding']['amount']
            logger.info('赎回项目前，总共持有金额数量是{}'.format(total_holding_old))
        with allure.step("赎回项目前，可计息金额"):
            accruing_amount_old = r2.json()['accruing_amount']['amount']
            logger.info('赎回项目前，可计息金额数量是{}'.format(accruing_amount_old))
        with allure.step("赎回项目前，今天申购金额"):
            subscribing_amount_old = r2.json()['subscribing_amount']['amount']
            logger.info('赎回项目前，今天申购金额数量是{}'.format(subscribing_amount_old))
        with allure.step("赎回项目前，可赎回金额"):
            redeemable_amount_old = r2.json()['redeemable_amount']['amount']
            logger.info('赎回项目前，可赎回金额数量是{}'.format(redeemable_amount_old))
        with allure.step("赎回项目前，赎回中金额"):
            redeeming_amount_old = r2.json()['redeeming_amount']['amount']
            logger.info('赎回项目前，赎回中金额数量是{}'.format(redeeming_amount_old))
        with allure.step("赎回项目前，检查可赎回金额 + 正在赎回金额 = 总持有金额"):
            assert Decimal(redeemable_amount_old) + Decimal(redeeming_amount_old) == Decimal(total_holding_old), \
                "，检查可赎回金额 + 正在赎回金额 != 总持有金额"
        with allure.step("赎回BTC投资项目成功"):
            data = {
                "tx_type": 2,
                "amount": "0.00187",
                "code": BTC_item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            sleep(2)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("赎回项目后，总共持有金额"):
                r5 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, BTC_item['product_id']),
                                      headers=headers)
                accruing_amount_latest = r5.json()['accruing_amount']['amount']
                logger.info('赎回项目后，总共持有金额数量是{}'.format(accruing_amount_latest))
            with allure.step("赎回项目后，今天申购金额"):
                subscribing_amount_latest = r5.json()['subscribing_amount']['amount']
                logger.info('赎回项目后，今天申购金额数量是{}'.format(subscribing_amount_latest))
            with allure.step("赎回项目后，可赎回金额"):
                redeemable_amount_latest = r5.json()['redeemable_amount']['amount']
                logger.info('赎回项目后，可赎回金额数量是{}'.format(redeemable_amount_latest))
            with allure.step("赎回项目后，赎回中金额"):
                redeeming_amount_latest = r5.json()['redeeming_amount']['amount']
                logger.info('赎回项目后，赎回中金额数量是{}'.format(redeeming_amount_latest))
            with allure.step("校验返回值"):
                logger.info('本次赎回是{}'.format(data['amount']))
            with allure.step("赎回项目后，检查可赎回金额 + 正在赎回金额 = 总持有金额"):
                assert Decimal(redeemable_amount_old) + Decimal(redeeming_amount_old) == Decimal(total_holding_old), "检查可赎回金额 + 正在赎回金额 != 总持有金额"
            with allure.step("赎回项目后，之前正在赎回金额 + 赎回金额 = 当前正在赎回金额"):
                assert Decimal(redeeming_amount_old) + Decimal(data['amount']) == Decimal(redeeming_amount_latest), "之前正在赎回金额 + 赎回金额 = 当前正在赎回金额"

    @allure.title('test_flexible_014')
    @allure.description('赎回USDT投资项目成功')
    def test_flexible_014(self):
        with allure.step("获取产品product_id"):
            r1 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择USDT投资项目"):
            BTCList = []
            for i in r1.json():
                if i['code'] == 'USDT':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
                logger.info('产品信息是{}'.format(BTC_item))
        with allure.step("赎回项目前，总共持有金额"):
            r2 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, BTC_item['product_id']), headers=headers)
            total_holding_old = r2.json()['total_holding']['amount']
            logger.info('赎回项目前，总共持有金额数量是{}'.format(total_holding_old))
        with allure.step("赎回项目前，可计息金额"):
            accruing_amount_old = r2.json()['accruing_amount']['amount']
            logger.info('赎回项目前，可计息金额数量是{}'.format(accruing_amount_old))
        with allure.step("赎回项目前，今天申购金额"):
            subscribing_amount_old = r2.json()['subscribing_amount']['amount']
            logger.info('赎回项目前，今天申购金额数量是{}'.format(subscribing_amount_old))
        with allure.step("赎回项目前，可赎回金额"):
            redeemable_amount_old = r2.json()['redeemable_amount']['amount']
            logger.info('赎回项目前，可赎回金额数量是{}'.format(redeemable_amount_old))
        with allure.step("赎回项目前，赎回中金额"):
            redeeming_amount_old = r2.json()['redeeming_amount']['amount']
            logger.info('赎回项目前，赎回中金额数量是{}'.format(redeeming_amount_old))
        with allure.step("赎回项目前，检查可赎回金额 + 正在赎回金额 = 总持有金额"):
            assert Decimal(redeemable_amount_old) + Decimal(redeeming_amount_old) == Decimal(total_holding_old), \
                "，检查可赎回金额 + 正在赎回金额 != 总持有金额"
        with allure.step("赎回USDT投资项目成功"):
            data = {
                "tx_type": 2,
                "amount": "1.7",
                "code": BTC_item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
            sleep(2)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("赎回项目后，总共持有金额"):
                r5 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, BTC_item['product_id']),
                                      headers=headers)
                accruing_amount_latest = r5.json()['accruing_amount']['amount']
                logger.info('赎回项目后，总共持有金额数量是{}'.format(accruing_amount_latest))
            with allure.step("赎回项目后，今天申购金额"):
                subscribing_amount_latest = r5.json()['subscribing_amount']['amount']
                logger.info('赎回项目后，今天申购金额数量是{}'.format(subscribing_amount_latest))
            with allure.step("赎回项目后，可赎回金额"):
                redeemable_amount_latest = r5.json()['redeemable_amount']['amount']
                logger.info('赎回项目后，可赎回金额数量是{}'.format(redeemable_amount_latest))
            with allure.step("赎回项目后，赎回中金额"):
                redeeming_amount_latest = r5.json()['redeeming_amount']['amount']
                logger.info('赎回项目后，赎回中金额数量是{}'.format(redeeming_amount_latest))
            with allure.step("校验返回值"):
                logger.info('本次赎回是{}'.format(data['amount']))
            with allure.step("赎回项目后，检查可赎回金额 + 正在赎回金额 = 总持有金额"):
                assert Decimal(redeemable_amount_old) + Decimal(redeeming_amount_old) == Decimal(total_holding_old), "检查可赎回金额 + 正在赎回金额 != 总持有金额"
            with allure.step("赎回项目后，之前正在赎回金额 + 赎回金额 = 当前正在赎回金额"):
                assert Decimal(redeeming_amount_old) + Decimal(data['amount']) == Decimal(redeeming_amount_latest), "之前正在赎回金额 + 赎回金额 = 当前正在赎回金额"

    @allure.title('test_flexible_015')
    @allure.description('赎回金额超过最大的可赎回BTC数量')
    def test_flexible_015(self):
        with allure.step("获取产品product_id"):
            r1 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择BTC投资项目"):
            BTCList = []
            for i in r1.json():
                if i['code'] == 'BTC':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
        with allure.step("赎回BTC投资项目成功"):
            data = {
                "tx_type": 2,
                "amount": "1111111.001",
                "code": BTC_item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'tx_id' in r.text, "赎回金额超过最大的可赎回BTC数量错误，返回值是{}".format(r.text)
            transaction_id = r.json()['tx_id']
        with allure.step("通过transaction_id查询交易是否成功"):
            params = {
                'product_id': BTC_item['product_id'],
                'transaction_id': transaction_id
            }
            r = session.request('GET', url='{}/earn/products/{}/transactions/{}'.format(env_url, BTC_item['product_id'], transaction_id), params=json.dumps(params), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 3, "赎回金额超过最大的可赎回BTC数量错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_016')
    @allure.description('赎回金额超过最大的可赎回ETH数量')
    def test_flexible_016(self):
        with allure.step("获取产品product_id"):
            r1 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择ETH投资项目"):
            BTCList = []
            for i in r1.json():
                if i['code'] == 'ETH':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
        with allure.step("赎回BTC投资项目成功"):
            data = {
                "tx_type": 2,
                "amount": "1111110.02",
                "code": BTC_item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'tx_id' in r.text, "赎回金额超过最大的可赎回BTC数量错误，返回值是{}".format(r.text)
            transaction_id = r.json()['tx_id']
        with allure.step("通过transaction_id查询交易是否成功"):
            params = {
                'product_id': BTC_item['product_id'],
                'transaction_id': transaction_id
            }
            r = session.request('GET', url='{}/earn/products/{}/transactions/{}'.format(env_url, BTC_item['product_id'],
                                                                                        transaction_id),
                                params=json.dumps(params), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 3, "赎回金额超过最大的可赎回BTC数量错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_017')
    @allure.description('赎回金额超过最大的可赎回USDT数量')
    def test_flexible_017(self):
        with allure.step("获取产品product_id"):
            r1 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        with allure.step("选择BTC投资项目"):
            BTCList = []
            for i in r1.json():
                if i['code'] == 'USDT':
                    BTCList.append(i)
            if len(BTCList) >= 1:
                BTC_item = random.choice(BTCList)
        with allure.step("赎回USDT投资项目成功"):
            data = {
                "tx_type": 2,
                "amount": "1111110",
                "code": BTC_item['code']
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, BTC_item['product_id']),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'tx_id' in r.text, "赎回金额超过最大的可赎回BTC数量错误，返回值是{}".format(r.text)
            transaction_id = r.json()['tx_id']
        with allure.step("通过transaction_id查询交易是否成功"):
            params = {
                'product_id': BTC_item['product_id'],
                'transaction_id': transaction_id
            }
            r = session.request('GET', url='{}/earn/products/{}/transactions/{}'.format(env_url, BTC_item['product_id'],
                                                                                        transaction_id),
                                params=json.dumps(params), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 3, "赎回金额超过最大的可赎回BTC数量错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_018')
    @allure.description('正在赎回金额等于wallet中冻结金额')
    def test_flexible_018(self):
        with allure.step("获取产品product"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product = random.choice(r.json())
            # 随机获取一个id
            id = product['product_id']
            logger.info('项目id是{}'.format(id))
        with allure.step("获得项目当前持有中的赎回冻结金额"):
            r = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, id), headers=headers)

            redeeming_amount = r.json()['redeeming_amount']['amount']
            logger.info('获得项目当前持有中的赎回冻结金额是{}'.format(redeeming_amount))
        with allure.step("wallet中saving冻结金额"):
            r = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
            for i in r.json():
                if i['code'] == product['code'] and i['wallet_type'] == 'SAVING':
                    for y in i['balances']:
                        if y['type'] == 'BALANCE_TYPE_FROZEN':
                            frozen_amount = y['amount']
                            logger.info('wallet中saving冻结金额是{}'.format(frozen_amount))
        assert redeeming_amount == frozen_amount, "获得项目当前持有中的赎回冻结金额不等于不wallet中saving冻结金额"

    @allure.title('test_flexible_019')
    @allure.description('校验明日计息金额')
    def test_flexible_019(self):
        sleep(10)
        with allure.step("获取产品product"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product = random.choice(r.json())
        with allure.step("通过接口获取产品明天计息情况"):
            # 随机获取一个id
            id = product['product_id']
            logger.info('项目id是{}'.format(id))
            interest = ApiFunction.get_interest(id)
            logger.info('通过接口得到明日的利息是{}'.format(interest))
        sleep(2)
        with allure.step("自己计算明天计息情况"):
            with allure.step("获得计息利率"):
                r = session.request('GET', url='{}/earn/products/{}'.format(env_url, id), headers=headers)
                apy = (Decimal(r.json()['apy'])/100)/365
                logger.info('计息时候的利率{}'.format(apy))
            with allure.step("获得计息本金"):
                r = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, id), headers=headers)
                amount = r.json()['accruing_amount']['amount']
                logger.info('获得计息本金{}'.format(amount))
                if product['code'] == 'BTC' or product['code'] == 'ETH':
                    interest_my_count = (Decimal(amount) * Decimal(apy)).quantize(Decimal('0.00000000'), ROUND_FLOOR)
                elif product['code'] == 'USDT':
                    interest_my_count = (Decimal(amount) * Decimal(apy)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                else:
                    interest_my_count = (Decimal(amount) * Decimal(apy)).quantize(Decimal('0.00'), ROUND_FLOOR)
                logger.info('自己计算明天计息情况是{}'.format(interest_my_count))
        assert interest_my_count == Decimal(interest), '接口获得和自己计算今天计算的利息不对'

    @allure.title('test_flexible_020')
    @allure.description('获取今日之前的利息列表')
    def test_flexible_020(self):
        with allure.step("获取产品product_id"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product_id = []
            for i in r.json():
                product_id.append(i['product_id'])
        with allure.step("获取今日之前的利息列表"):
            # 随机获取一个id
            id = random.choice(product_id)
            logger.info('id是{}'.format(id))
            params = {
                "cursor": 0,
                "size": -30
            }
            r = session.request('GET', url='{}/earn/products/{}/interests'.format(env_url, id), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'items' in r.text, "获取今日之前的利息列表错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_021')
    @allure.description('确定利息派发日期是T+1')
    def test_flexible_021(self):
        with allure.step("获取产品product_id"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product_id = []
            for i in r.json():
                product_id.append(i['product_id'])
        with allure.step("确定利息派发日期是T+1"):
            # 随机获取一个id
            id = random.choice(product_id)
            logger.info('产品id是{}'.format(id))
            r = session.request('GET', url='{}/earn/products/{}'.format(env_url, id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            earning_start_time = r.json()['earning_start_time']
            logger.info('计息时间戳是{}'.format(earning_start_time))
            # 获得现在时间
            now_time = str(time.time()).split('.')[0]
            logger.info('现在时间戳是{}'.format(now_time))
            assert int(now_time) <= int(earning_start_time), '确定利息派发日期是T+1错误'
            assert int(now_time) + 86400 >= int(earning_start_time), '确定利息派发日期是T+1错误'

    @allure.title('test_flexible_022')
    @allure.description('确定赎回日期是D+1')
    def test_flexible_022(self):
        with allure.step("获取产品product_id"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            product_id = []
            for i in r.json():
                product_id.append(i['product_id'])
        with allure.step("确定赎回日期是D+1"):
            # 随机获取一个id
            id = random.choice(product_id)
            logger.info('产品id是{}'.format(id))
            r = session.request('GET', url='{}/earn/products/{}'.format(env_url, id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            redeem_settle_time = r.json()['redeem_settle_time']
            logger.info('计息时间戳是{}'.format(redeem_settle_time))
            # 获得现在时间
            now_time = str(time.time()).split('.')[0]
            logger.info('现在时间戳是{}'.format(now_time))
            assert int(now_time) <= int(redeem_settle_time), '确定赎回日期是D+1错误'
            assert int(now_time) + 86400*2 >= int(redeem_settle_time), '确定赎回日期是D+1错误'

    @allure.title('test_flexible_023')
    @allure.description('获取所有产品持有情况')
    def test_flexible_023(self):
        with allure.step("获取所有产品持有情况"):
            r = session.request('GET', url='{}/earn/products/summary'.format(env_url), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'total_holding' in r.text, "获取所有产品持有情况错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_024')
    @allure.description('获取所有产品持有情况以EUR显示')
    def test_flexible_024(self):
        with allure.step("获取所有产品持有情况以EUR显示"):
            headers['X-Currency'] = 'EUR'
            r = session.request('GET', url='{}/earn/products/summary'.format(env_url), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'total_holding' in r.text, "获取所有产品持有情况以EUR显示错误，返回值是{}".format(r.text)
                assert r.json()['code'] == 'EUR', "获取所有产品持有情况以EUR显示错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_025')
    @allure.description('快速赎回')
    def test_flexible_025(self):
        with allure.step("获取产品列表"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            for i in r.json():
                with allure.step("获取目前balance"):
                    balance_available = ApiFunction.get_crypto_number(type=i['code'])
                    balance_saving_available = ApiFunction.get_crypto_number(type=i['code'], wallet_type='SAVING')
                with allure.step("快速赎回"):
                    data = {
                        "amount": "0.01",
                        "code": i['code'],
                        "tx_type": 2,
                        "is_fast_redemption": True
                    }
                    r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, i['product_id']), data=json.dumps(data), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['tx_id'] is not None, "快速赎回错误，返回值是{}".format(r.text)
                    sleep(10)
                    with allure.step("获取目前balance"):
                        balance_available_latest = ApiFunction.get_crypto_number(type=i['code'])
                        balance_saving_available_latest = ApiFunction.get_crypto_number(type=i['code'], wallet_type='SAVING')
                    with allure.step("检查balance增减正确"):
                        assert Decimal(balance_available) + Decimal(data['amount']) == Decimal(balance_available_latest)
                        assert Decimal(balance_saving_available) == Decimal(data['amount']) + Decimal(balance_saving_available_latest)

    @allure.title('test_flexible_026')
    @allure.description('快速赎回使用无效product id')
    def test_flexible_026(self):
        with allure.step("快速赎回"):
            data = {
                "amount": "0.01",
                "code": 'ETH',
                "tx_type": 2,
                "is_fast_redemption": True
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, '123123123123'), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '104001', "快速赎回使用无效product id错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_027')
    @allure.description('快速赎回使用错误product id')
    def test_flexible_027(self):
        with allure.step("快速赎回"):
            data = {
                "amount": "0.01",
                "code": 'ETH',
                "tx_type": 2,
                "is_fast_redemption": True
            }
            r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, 'a1220392-194c-432c-a961-eff561bb72b3'), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '104040', "快速赎回使用错误product id错误，返回值是{}".format(r.text)

    @allure.title('test_flexible_028')
    @allure.description('快速赎回赎回条件')
    def test_flexible_028(self):
        with allure.step("获取产品列表"):
            r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
            for i in r.json():
                with allure.step("快速赎回赎回条件"):
                    r = session.request('GET', url='{}/earn/products/{}/redeem/conditions'.format(env_url, i['product_id']), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['fast_redemption'] is not None, "快速赎回错误，返回值是{}".format(r.text)

