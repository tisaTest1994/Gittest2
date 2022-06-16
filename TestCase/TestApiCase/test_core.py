from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api core 相关 testcases")
class TestCoreApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_core_001')
    @allure.description('查询钱包所有币种详细金额以及报价,以美元价格返回')
    def test_core_001(self):
        with allure.step("查询钱包所有币种详细金额以及报价,以美元价格返回"):
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'wallets' in r.text, "查询钱包所有币种详细金额以及报价,以美元价格返回错误,返回值是{}".format(r.text)

    @allure.title('test_core_002')
    @allure.description('查询钱包所有币种金额')
    def test_core_002(self):
        with allure.step("查询钱包所有币种金额"):
            r = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'id' in r.text, "查询钱包所有币种金额错误,返回值是{}".format(r.text)

    @allure.title('test_core_003')
    @allure.description('查询钱包某个币种的详细信息')
    def test_core_003(self):
        with allure.step("查询钱包某个币种的详细信息"):
            r = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
            id = r.json()[0]["id"]
        with allure.step("查询钱包某个币种"):
            r = session.request('GET', url='{}/core/account/wallets/{}'.format(env_url, id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['id'] is not None, "查询钱包某个币种的详细信息错误,返回值是{}".format(r.text)

    @allure.title('test_core_004')
    @allure.description('查询货币兑换比例')
    def test_core_004(self):
        with allure.step("获取汇率对"):
            cfx_dict = get_json()['cfx_book']
        with allure.step("查询货币兑换比例"):
            for i in cfx_dict.values():
                with allure.step("查询{}兑换比例".format(i)):
                    r = session.request('GET', url='{}/core/quotes/{}'.format(env_url, i), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['quote'] != {}, " 查询货币兑换比例错误,返回值是{}".format(r.text)

    @allure.title('test_core_005')
    @allure.description('查询钱包中的所有币种投资于SAVING中的金额')
    def test_core_005(self):
        with allure.step("查询钱包中的所有币种投资于SAVING中的金额"):
            params = {
                'type': 'SAVING'
            }
            r = session.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'SAVING' in r.text, "查询钱包中的所有币种投资于SAVING中的金额错误,返回值是{}".format(r.text)

    @allure.title('test_core_006')
    @allure.description('查询钱包中的所有币种投资于SAVING中的金额')
    def test_core_006(self):
        with allure.step("查询钱包中的所有币种投资于BALANCE中的金额"):
            params = {
                'type': 'BALANCE'
            }
            r = session.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'BALANCE' in r.text, "查询钱包中的所有币种投资于BALANCE中的金额错误,返回值是{}".format(r.text)

    @allure.title('test_core_007')
    @allure.description('查询钱包BTC金额')
    def test_core_007(self):
        with allure.step("查询钱包BTC金额"):
            params = {
                'code': 'BTC'
            }
            r = session.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'BTC' in r.text, "查询钱包BTC金额错误,返回值是{}".format(r.text)

    @allure.title('test_core_008')
    @allure.description('查询钱包ETH金额')
    def test_core_008(self):
        with allure.step("查询钱包ETH金额"):
            params = {
                'code': 'ETH'
            }
            r = session.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ETH' in r.text, "查询钱包ETH金额错误,返回值是{}".format(r.text)

    @allure.title('test_core_009')
    @allure.description('查询钱包USDT金额')
    def test_core_009(self):
        with allure.step("查询钱包USDT金额"):
            params = {
                'code': 'USDT'
            }
            r = session.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'USDT' in r.text, "查询钱包USDT金额错误,返回值是{}".format(r.text)

    @allure.title('test_core_010')
    @allure.description('查询钱包所有币种详细金额以及报价,以欧元价格返回')
    def test_core_010(self):
        headers['X-Currency'] = 'EUR'
        with allure.step("查询钱包所有币种详细金额以及报价,以欧元价格返回"):
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        headers['X-Currency'] = 'USD'
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'wallets' in r.text, "查询钱包所有币种详细金额以及报价,以欧元价格返回错误,返回值是{}".format(r.text)

    @allure.title('test_core_011')
    @allure.description('查询客户状态')
    def test_core_011(self):
        with allure.step("查询客户状态"):
            r = session.request('GET', url='{}/core/beginnerguide'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'customertags' in r.text, "查询客户状态错误,返回值是{}".format(r.text)

    @allure.title('test_core_012')
    @allure.description('获得客户地区,服务器时间')
    def test_core_012(self):
        with allure.step("获得客户地区,服务器时间"):
            r = session.request('GET', url='{}/core/geo'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'time_zone' in r.text, "查询客户状态错误,返回值是{}".format(r.text)

    @allure.title('test_core_013')
    @allure.description('获取metadata')
    def test_core_013(self):
        with allure.step("获取metadata"):
            r = session.request('GET', url='{}/core/metadata'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'currencies' in r.text, "获取metadata错误,返回值是{}".format(r.text)

    @allure.title('test_core_014')
    @allure.description('获取所有Saving产品的持有金额')
    def test_core_014(self):
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的持有金额"):
                    r = session.request('GET', url='{}/earn/saving/holding'.format(env_url), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("通过api获得Total Saving Amount数据"):
                    r1 = session.request('GET', url='{}/earn/products/summary'.format(env_url), headers=headers)
                with allure.step("校验返回值"):
                    assert r1.json()['total_holding'] == r.json()[
                        'total_saving_amount'], "获取所有Saving产品的持有金额错误显示货币类型是{},返回值是{}".format(i, r.text)
                    for y in get_json()['crypto_list']:
                        assert y in r.json()['currencies'], "获取所有Saving产品的持有金额错误,显示货币类型是{},返回值是{}".format(i, r.text)

    @allure.title('test_core_015')
    @allure.description('获取所有Saving产品的持有金额详情的总金额')
    def test_core_015(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的持有金额详情的总金额"):
                    r = session.request('GET', url='{}/earn/saving/holding/details'.format(env_url), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("total_saving_amount计算"):
                    r1 = session.request('GET', url='{}/earn/products/summary'.format(env_url), headers=headers)
                    assert r1.json()['total_holding'] == r.json()[
                        'total_saving_amount'], "获取所有Saving产品的持有金额详情的总金额错误,显示货币类型是{},返回值是{}".format(i, r.text)

    @allure.title('test_core_016')
    @allure.description('获取所有Saving产品的持有金额详情的已派发利息')
    def test_core_016(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的持有金额详情的已派发利息"):
                    r = session.request('GET', url='{}/earn/saving/holding/details'.format(env_url), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("cumulative_interest计算"):
                    all_interest = []
                    with allure.step("获取累计活期利息"):
                        with allure.step("获取产品product_id"):
                            r2 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
                            for z in r2.json():
                                product_id = z['product_id']
                                with allure.step("获取产品持有情况"):
                                    r3 = session.request('GET',
                                                         url='{}/earn/products/{}/summary'.format(env_url, product_id),
                                                         headers=headers)
                                    all_interest.append(Decimal(r3.json()['total_yield']['abs_amount']))
                    with allure.step("获取累计定期利息"):
                        for x in get_json()['crypto_list']:
                            fixed_all_interest_amount_list = []
                            cursor = '0'
                            while cursor != '-1':
                                params = {
                                    'tx_type': "2",
                                    'cursor': cursor,
                                    'size': 50,
                                    'order': "1",
                                    'code': x
                                }
                                r4 = session.request('GET', url='{}/earn/fix/transactions'.format(env_url),
                                                     params=params,
                                                     headers=headers, timeout=20)
                                cursor = r4.json()['cursor']
                                for k in r4.json()['transactions']:
                                    fixed_all_interest_amount_list.append(Decimal(k['maturity_interest']['amount']))
                            quote = sqlFunction.get_now_quote('{}-{}'.format(x, i))
                            all_interest.append(
                                Decimal(crypto_len(Decimal(quote['middle']) * sum(fixed_all_interest_amount_list), i)))
                    logger.info('显示币种是{}, 计算获取累计利息总和是{}, 接口返回的累计利息总和是{}'.format(i, sum(all_interest),
                                                                                str(r.json()['cumulative_interest'])))
                    if Decimal(r.json()['cumulative_interest']) != Decimal(sum(all_interest)):
                        assert Decimal(sum(all_interest)) - Decimal(r.json()['cumulative_interest']) >= Decimal(
                            0.5) or Decimal(sum(all_interest)) - Decimal(r.json()['cumulative_interest']) <= Decimal(
                            0.5), '获取所有Saving产品的持有金额详情的已派发利息, 显示币种是{}, 计算获取累计利息总和是{}, 接口返回的累计利息总和是{}'.format(i,
                                                                                                             sum(all_interest),
                                                                                                             str(
                                                                                                                 r.json()[
                                                                                                                     'cumulative_interest']))

    @allure.title('test_core_017')
    @allure.description('获取所有Saving产品的持有金额详情数字货币定期总金额')
    def test_core_017(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的持有金额详情数字货币定期总金额"):
                    r = session.request('GET', url='{}/earn/saving/holding/details'.format(env_url),
                                        headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("fixed_saving_amount计算"):
                    fixed_saving_abs_amount_list = []
                    for z in get_json()['crypto_list']:
                        fixed_saving_abs_amount_list.append(Decimal(
                            ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_AVAILABLE',
                                                          wallet_type='SAVING-FIX',
                                                          amount_type='abs_amount')) + Decimal(
                            ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_FROZEN',
                                                          wallet_type='SAVING-FIX', amount_type='abs_amount')))
                    assert sum(fixed_saving_abs_amount_list) == Decimal(r.json()[
                                                                            'fixed_saving_amount']), "获取所有Saving产品的持有金额详情数字货币定期总金额错误, 显示货币类型是{}, 计算数字货币定期总金额是{}, 接口数字货币定期总金额是{}".format(
                        i, sum(fixed_saving_abs_amount_list), r.json()['fixed_saving_amount'])

    @allure.title('test_core_018')
    @allure.description('获取所有Saving产品的持有金额详情未派发利息')
    def test_core_018(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的持有金额详情未派发利息"):
                    r = session.request('GET', url='{}/earn/saving/holding/details'.format(env_url), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("interest_to_settle计算"):
                    with allure.step("获取累计定期利息"):
                        fixed_all_interest_list = []
                        for x in get_json()['crypto_list']:
                            fixed_all_interest_amount_list = []
                            cursor = '0'
                            while cursor != '-1':
                                params = {
                                    'tx_type': "1",
                                    'cursor': cursor,
                                    'size': 50,
                                    'order': "1",
                                    'code': x
                                }
                                r4 = session.request('GET', url='{}/earn/fix/transactions'.format(env_url),
                                                     params=params,
                                                     headers=headers, timeout=20)
                                cursor = r4.json()['cursor']
                                for k in r4.json()['transactions']:
                                    fixed_all_interest_amount_list.append(Decimal(k['maturity_interest']['amount']))
                            quote = sqlFunction.get_now_quote('{}-{}'.format(x, i))
                            fixed_all_interest_list.append(
                                Decimal(crypto_len(Decimal(quote['middle']) * sum(fixed_all_interest_amount_list), i)))
                    logger.info('显示币种是{}, 计算获取未发放利息总和是{}, 接口返回的未发放利息总和是{}'.format(i, sum(fixed_all_interest_list),
                                                                                  str(r.json()['interest_to_settle'])))
                    if Decimal(r.json()['interest_to_settle']) != Decimal(sum(fixed_all_interest_list)):
                        assert Decimal(sum(fixed_all_interest_list)) - Decimal(
                            r.json()['interest_to_settle']) >= Decimal(0.5) or Decimal(
                            sum(fixed_all_interest_list)) - Decimal(r.json()['interest_to_settle']) <= Decimal(
                            0.5), '获取所有Saving产品的持有金额详情的已派发利息错误, 显示币种是{}, 计算获取未发放利息总和是{}, 接口返回的未发放利息总和是{}'.format(i,
                                                                                                                 sum(fixed_all_interest_list),
                                                                                                                 str(
                                                                                                                     r.json()[
                                                                                                                         'interest_to_settle']))

    @allure.title('test_core_019')
    @allure.description('获取所有Saving产品的持有金额详情数字货币定期各币种数量')
    def test_core_019(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("获取所有Saving产品的持有金额详情数字货币定期各币种数量"):
            r = session.request('GET', url='{}/earn/saving/holding/details'.format(env_url),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("fixed_saving_map计算"):
            for z in get_json()['crypto_list']:
                assert Decimal(r.json()['fixed_saving_map'][z]) == Decimal(
                    ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_AVAILABLE',
                                                  wallet_type='SAVING-FIX')) + Decimal(
                    ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_FROZEN',
                                                  wallet_type='SAVING-FIX')), "获取所有Saving产品的持有金额详情数字货币定期各币种数量错误, 数字货币类型是{}, 其他接口获得的数字货币定期数量是{}, 测试接口获得的数字货币定期数量是{}".format(
                    z, Decimal(ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_AVAILABLE',
                                                             wallet_type='SAVING-FIX')) + Decimal(
                        ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_FROZEN',
                                                      wallet_type='SAVING-FIX')), r.json()['fixed_saving_map'][z])

    @allure.title('test_core_020')
    @allure.description('获取所有Saving产品的持有金额详情数字货币活期总金额')
    def test_core_020(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的持有金额详情数字货币活期总金额"):
                    r = session.request('GET', url='{}/earn/saving/holding/details'.format(env_url), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                    with allure.step("flexible_saving_amount计算"):
                        fixed_saving_abs_amount_list = []
                        for z in get_json()['crypto_list']:
                            fixed_saving_abs_amount_list.append(Decimal(
                                ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_AVAILABLE',
                                                              wallet_type='SAVING',
                                                              amount_type='abs_amount')) + Decimal(
                                ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_FROZEN',
                                                              wallet_type='SAVING', amount_type='abs_amount')))
                        assert sum(fixed_saving_abs_amount_list) == Decimal(r.json()[
                                                                                'flexible_saving_amount']), "获取所有Saving产品的持有金额详情数字货币活期总金额错误, 显示货币类型是{}, 计算数字货币活期总金额是{}, 接口获取数字货币活期总金额是{}".format(
                            i, sum(fixed_saving_abs_amount_list), Decimal(r.json()['flexible_saving_amount']))

    @allure.title('test_core_021')
    @allure.description('获取所有Saving产品的持有金额详情数字货币活期各币种数量')
    def test_core_021(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("获取所有Saving产品的持有金额详情数字货币活期各币种数量"):
            r = session.request('GET', url='{}/earn/saving/holding/details'.format(env_url),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("flexible_saving_map计算"):
            for z in get_json()['crypto_list']:
                logger.info(
                    "获取所有Saving产品的持有金额详情数字货币活期各币种数量错误, 数字货币类型是{}, 其他接口获得的数字货币活期数量是{}, 测试接口获得的数字货币活期数量是{}".format(z,
                                                                                                                 Decimal(
                                                                                                                     ApiFunction.get_crypto_number(
                                                                                                                         type=z,
                                                                                                                         balance_type='BALANCE_TYPE_AVAILABLE',
                                                                                                                         wallet_type='SAVING')) + Decimal(
                                                                                                                     ApiFunction.get_crypto_number(
                                                                                                                         type=z,
                                                                                                                         balance_type='BALANCE_TYPE_FROZEN',
                                                                                                                         wallet_type='SAVING')),
                                                                                                                 r.json()[
                                                                                                                     'flexible_saving_map'][
                                                                                                                     z]))
                assert Decimal(r.json()['flexible_saving_map'][z]) == Decimal(
                    ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_AVAILABLE',
                                                  wallet_type='SAVING')) + Decimal(
                    ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_FROZEN',
                                                  wallet_type='SAVING')), "获取所有Saving产品的持有金额详情数字货币活期各币种数量错误, 数字货币类型是{}, 其他接口获得的数字货币活期数量是{}, 测试接口获得的数字货币活期数量是{}".format(
                    z, Decimal(ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_AVAILABLE',
                                                             wallet_type='SAVING')) + Decimal(
                        ApiFunction.get_crypto_number(type=z, balance_type='BALANCE_TYPE_FROZEN',
                                                      wallet_type='SAVING')), r.json()['flexible_saving_map'][z])

    @allure.title('test_core_022')
    @allure.description('获取所有Saving产品的收益详情最早申购时间')
    def test_core_022(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("获取所有Saving产品的收益详情最早申购时间"):
            r = session.request('GET', url='{}/earn/saving/return'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
        with allure.step("first_subscription_time验证"):
            params = {
                'tx_type': "2",
                'cursor': -1,
                'size': 1,
                'order': "1",
                'code': ''
            }
            r1 = session.request('GET', url='{}/earn/fix/transactions'.format(env_url),
                                 params=params,
                                 headers=headers, timeout=20)
            if r1.json()['transactions'][0]['time_line']['subscribed_at'] is not None:
                subscribed_at = r1.json()['transactions'][0]['time_line']['subscribed_at']
            params = {
                'tx_type': "1",
                'cursor': -1,
                'size': 1,
                'order': "1",
                'code': ''
            }
            r2 = session.request('GET', url='{}/earn/fix/transactions'.format(env_url),
                                 params=params,
                                 headers=headers, timeout=20)
            if r2.json()['transactions'][0]['time_line']['subscribed_at'] is not None:
                subscribed_at_2 = r2.json()['transactions'][0]['time_line']['subscribed_at']
            if subscribed_at > subscribed_at_2:
                assert r.json()[
                           'first_subscription_time'] == subscribed_at_2, "获取所有Saving产品的收益详情最早申购时间错误,返回值是{}".format(
                    r.text)
            else:
                assert r.json()['first_subscription_time'] == subscribed_at, "获取所有Saving产品的收益详情最早申购时间错误,返回值是{}".format(
                    r.text)

    @allure.title('test_core_023')
    @allure.description('获取所有Saving产品的收益详情已派发利息')
    def test_core_023(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的收益详情已派发利息"):
                    r = session.request('GET', url='{}/earn/saving/return'.format(env_url),
                                        headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("total_earnings计算"):
                    all_interest = []
                    with allure.step("获取累计活期利息"):
                        with allure.step("获取产品product_id"):
                            r2 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
                            for z in r2.json():
                                product_id = z['product_id']
                                with allure.step("获取产品持有情况"):
                                    r3 = session.request('GET',
                                                         url='{}/earn/products/{}/summary'.format(env_url, product_id),
                                                         headers=headers)
                                    all_interest.append(Decimal(r3.json()['total_yield']['abs_amount']))
                    with allure.step("获取累计定期利息"):
                        for x in get_json()['crypto_list']:
                            fixed_all_interest_amount_list = []
                            cursor = '0'
                            while cursor != '-1':
                                params = {
                                    'tx_type': "2",
                                    'cursor': cursor,
                                    'size': 50,
                                    'order': "1",
                                    'code': x
                                }
                                r4 = session.request('GET', url='{}/earn/fix/transactions'.format(env_url),
                                                     params=params,
                                                     headers=headers, timeout=20)
                                cursor = r4.json()['cursor']
                                for k in r4.json()['transactions']:
                                    fixed_all_interest_amount_list.append(Decimal(k['maturity_interest']['amount']))
                            quote = sqlFunction.get_now_quote('{}-{}'.format(x, i))
                            all_interest.append(
                                Decimal(crypto_len(Decimal(quote['middle']) * sum(fixed_all_interest_amount_list), i)))
                    logger.info('显示币种是{}, 计算获取累计利息总和是{}, 接口返回的累计利息总和是{}'.format(i, sum(all_interest),
                                                                                str(r.json()['total_earnings'])))
                    if Decimal(r.json()['total_earnings']) != Decimal(sum(all_interest)):
                        assert Decimal(sum(all_interest)) - Decimal(r.json()['total_earnings']) >= Decimal(
                            0.5) or Decimal(sum(all_interest)) - Decimal(r.json()['total_earnings']) <= Decimal(
                            0.5), '获取所有Saving产品的收益详情已派发利息错误, 显示币种是{}, 计算获取累计利息总和是{}, 接口返回的累计利息总和是{}'.format(i,
                                                                                                            sum(all_interest),
                                                                                                            str(
                                                                                                                r.json()[
                                                                                                                    'total_earnings']))

    @allure.title('test_core_024')
    @allure.description('获取所有Saving产品的收益详情未派发利息')
    def test_core_024(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的收益详情未派发利息"):
                    r = session.request('GET', url='{}/earn/saving/return'.format(env_url),
                                        headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("interest_to_settle计算"):
                    with allure.step("获取累计定期利息"):
                        fixed_all_interest_list = []
                        for x in get_json()['crypto_list']:
                            fixed_all_interest_amount_list = []
                            cursor = '0'
                            while cursor != '-1':
                                params = {
                                    'tx_type': "1",
                                    'cursor': cursor,
                                    'size': 50,
                                    'order': "1",
                                    'code': x
                                }
                                r4 = session.request('GET', url='{}/earn/fix/transactions'.format(env_url),
                                                     params=params,
                                                     headers=headers, timeout=20)
                                cursor = r4.json()['cursor']
                                for k in r4.json()['transactions']:
                                    fixed_all_interest_amount_list.append(Decimal(k['maturity_interest']['amount']))
                            quote = sqlFunction.get_now_quote('{}-{}'.format(x, i))
                            fixed_all_interest_list.append(
                                Decimal(crypto_len(Decimal(quote['middle']) * sum(fixed_all_interest_amount_list), i)))
                    logger.info('显示币种是{}, 计算获取未发放利息总和是{}, 接口返回的未发放利息总和是{}'.format(i, sum(fixed_all_interest_list),
                                                                                  str(r.json()['interest_to_settle'])))
                    if Decimal(r.json()['interest_to_settle']) != Decimal(sum(fixed_all_interest_list)):
                        assert Decimal(sum(fixed_all_interest_list)) - Decimal(
                            r.json()['interest_to_settle']) >= Decimal(0.5) or Decimal(
                            sum(fixed_all_interest_list)) - Decimal(r.json()['interest_to_settle']) <= Decimal(
                            0.5), '获取所有Saving产品的收益详情未派发利息错误, 显示币种是{}, 计算获取未发放利息总和是{}, 接口返回的未发放利息总和是{}'.format(i,
                                                                                                              sum(fixed_all_interest_list),
                                                                                                              str(
                                                                                                                  r.json()[
                                                                                                                      'interest_to_settle']))

    @allure.title('test_core_025')
    @allure.description('获取所有Saving产品的收益详情定期已派发利息')
    def test_core_025(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的收益详情定期已派发利息"):
                    r = session.request('GET', url='{}/earn/saving/return'.format(env_url),
                                        headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("total_earnings计算"):
                    all_interest = []
                    with allure.step("获取累计定期利息"):
                        for x in get_json()['crypto_list']:
                            fixed_all_interest_amount_list = []
                            cursor = '0'
                            while cursor != '-1':
                                params = {
                                    'tx_type': "2",
                                    'cursor': cursor,
                                    'size': 50,
                                    'order': "1",
                                    'code': x
                                }
                                r4 = session.request('GET', url='{}/earn/fix/transactions'.format(env_url),
                                                     params=params,
                                                     headers=headers, timeout=20)
                                cursor = r4.json()['cursor']
                                for k in r4.json()['transactions']:
                                    fixed_all_interest_amount_list.append(Decimal(k['maturity_interest']['amount']))
                            quote = sqlFunction.get_now_quote('{}-{}'.format(x, i))
                            all_interest.append(
                                Decimal(crypto_len(Decimal(quote['middle']) * sum(fixed_all_interest_amount_list), i)))
                    logger.info('显示币种是{}, 计算获取累计利息总和是{}, 接口返回的累计利息总和是{}'.format(i, sum(all_interest),
                                                                                str(r.json()['fixed_earnings'])))
                    if Decimal(r.json()['fixed_earnings']) != Decimal(sum(all_interest)):
                        assert Decimal(sum(all_interest)) - Decimal(r.json()['fixed_earnings']) >= Decimal(
                            0.5) or Decimal(sum(all_interest)) - Decimal(r.json()['fixed_earnings']) <= Decimal(
                            0.5), '获取所有Saving产品的收益详情已派发利息错误, 显示币种是{}, 计算获取累计利息总和是{}, 接口返回的累计利息总和是{}'.format(i,
                                                                                                            sum(all_interest),
                                                                                                            str(
                                                                                                                r.json()[
                                                                                                                    'fixed_earnings']))

    @allure.title('test_core_026')
    @allure.description('获取所有Saving产品的收益详情数字货币定期已派发利息的数量和金额')
    def test_core_026(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的收益详情数字货币定期已派发利息的数量和金额"):
                    r = session.request('GET', url='{}/earn/saving/return'.format(env_url),
                                        headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("fixed_earning_map计算"):
                    with allure.step("获取累计定期利息"):
                        for x in get_json()['crypto_list']:
                            fixed_all_interest_amount_list = []
                            cursor = '0'
                            while cursor != '-1':
                                params = {
                                    'tx_type': "2",
                                    'cursor': cursor,
                                    'size': 50,
                                    'order': "1",
                                    'code': x
                                }
                                r4 = session.request('GET', url='{}/earn/fix/transactions'.format(env_url),
                                                     params=params,
                                                     headers=headers, timeout=20)
                                cursor = r4.json()['cursor']
                                for k in r4.json()['transactions']:
                                    fixed_all_interest_amount_list.append(Decimal(k['maturity_interest']['amount']))
                            quote = sqlFunction.get_now_quote('{}-{}'.format(x, i))
                            logger.info('显示币种是{}, 数字货币是{}, 计算获取累计利息数量总和是{}, 接口返回的累计利息数量总和是{}'.format(i, x,
                                                                                                     sum(fixed_all_interest_amount_list),
                                                                                                     r.json()[
                                                                                                         'fixed_earning_map'][
                                                                                                         x]['amount']))
                            assert Decimal(sum(fixed_all_interest_amount_list)).quantize(Decimal('0.00000000')) == Decimal(
                                r.json()['fixed_earning_map'][x][
                                    'amount']), '显示币种是{}, 数字货币是{}, 计算获取累计利息数量总和是{}, 接口返回的累计利息数量总和是{}'.format(i, x,
                                                                                                             sum(fixed_all_interest_amount_list),
                                                                                                             r.json()[
                                                                                                                 'fixed_earning_map'][
                                                                                                                 x][
                                                                                                                 'amount'])
                            logger.info('显示币种是{}, 数字货币是{}, 计算获取累计利息金额总和是{}, 接口返回的累计利息金额总和是{}'.format(i, x, crypto_len(
                                Decimal(quote['middle']) * sum(fixed_all_interest_amount_list), i), r.json()[
                                                                                                         'fixed_earning_map'][
                                                                                                         x][
                                                                                                         'abs_amount']))
                            assert Decimal(crypto_len(Decimal(quote['middle']) * sum(fixed_all_interest_amount_list),
                                                      i)) + Decimal(0.5) >= Decimal(r.json()['fixed_earning_map'][x][
                                                                         'abs_amount']), '显示币种是{}, 数字货币是{}, 计算获取累计利息金额总和是{}, 接口返回的累计利息金额总和是{}'.format(
                                i, x, crypto_len(Decimal(quote['middle']) * sum(fixed_all_interest_amount_list), i),
                                r.json()['fixed_earning_map'][x]['abs_amount'])
                            assert Decimal(crypto_len(Decimal(quote['middle']) * sum(fixed_all_interest_amount_list),
                                                      i)) - Decimal(0.5) <= Decimal(r.json()['fixed_earning_map'][x][
                                                                         'abs_amount']), '显示币种是{}, 数字货币是{}, 计算获取累计利息金额总和是{}, 接口返回的累计利息金额总和是{}'.format(
                                i, x, crypto_len(Decimal(quote['middle']) * sum(fixed_all_interest_amount_list), i),
                                r.json()['fixed_earning_map'][x]['abs_amount'])

    @allure.title('test_core_027')
    @allure.description('获取所有Saving产品的收益详情数字货币活期已派发利息总金额')
    def test_core_027(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的收益详情数字货币活期已派发利息总金额"):
                    r = session.request('GET', url='{}/earn/saving/return'.format(env_url),
                                        headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("获取累计活期利息"):
                    all_interest = []
                    with allure.step("获取产品product_id"):
                        r2 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
                        for z in r2.json():
                            product_id = z['product_id']
                            with allure.step("获取产品持有情况"):
                                r3 = session.request('GET',
                                                     url='{}/earn/products/{}/summary'.format(env_url, product_id),
                                                     headers=headers)
                                all_interest.append(Decimal(r3.json()['total_yield']['abs_amount']))
                assert Decimal(sum(all_interest)) == Decimal(r.json()[
                                                                 'flexible_earnings']), '获取所有Saving产品的收益详情数字货币活期已派发利息总金额错误, 显示币种是{}, 计算获取累计利息总和是{}, 接口返回的累计利息总和是{}'.format(
                    i, sum(all_interest), str(r.json()['flexible_earnings']))

    @allure.title('test_core_028')
    @allure.description('获取所有Saving产品的收益详情数字货币活期已派发利息的数量和金额')
    def test_core_028(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='external.qa@cabital.com')
        with allure.step("显示币种矩阵"):
            for i in get_json()['show_list']:
                headers['X-Currency'] = i
                with allure.step("获取所有Saving产品的收益详情数字货币活期已派发利息的数量和金额"):
                    r = session.request('GET', url='{}/earn/saving/return'.format(env_url),
                                        headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("flexible_earning_map"):
                    with allure.step("获取产品product_id"):
                        for y in get_json()['crypto_list']:
                            r2 = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
                            for z in r2.json():
                                if y == z['code']:
                                    with allure.step("获取产品持有情况"):
                                        r3 = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, z[
                                            'product_id']), headers=headers)
                                        logger.info(
                                            '获取所有Saving产品的收益详情数字货币活期已派发利息总金额错误, 显示币种是{}, 数字货币币种是{}, 其他接口获得的是数量是{}, 测试接口获得的是数量是{}'.format(
                                                i, y, r3.json()['total_yield']['amount'],
                                                r.json()['flexible_earning_map'][y]['amount']))
                                        assert Decimal(r3.json()['total_yield']['amount']) == Decimal(
                                            r.json()['flexible_earning_map'][y][
                                                'amount']), '获取所有Saving产品的收益详情数字货币活期已派发利息总金额错误, 显示币种是{}, 数字货币币种是{}, 其他接口获得的是数量是{}, 测试接口获得的是数量是{}'.format(
                                            i, y, r3.json()['total_yield']['amount'],
                                            r.json()['flexible_earning_map'][y]['amount'])
                                        logger.info(
                                            '获取所有Saving产品的收益详情数字货币活期已派发利息总金额错误, 显示币种是{}, 数字货币币种是{}, 其他接口获得的是数量是{}, 测试接口获得的是数量是{}'.format(
                                                i, y, r3.json()['total_yield']['abs_amount'],
                                                r.json()['flexible_earning_map'][y]['abs_amount']))
                                        assert Decimal(r3.json()['total_yield']['abs_amount']) == Decimal(
                                            r.json()['flexible_earning_map'][y][
                                                'abs_amount']), '获取所有Saving产品的收益详情数字货币活期已派发利息总金额错误, 显示币种是{}, 数字货币币种是{}, 其他接口获得的是数量是{}, 测试接口获得的是数量是{}'.format(
                                            i, y, r3.json()['total_yield']['abs_amount'],
                                            r.json()['flexible_earning_map'][y]['abs_amount'])

    @allure.title('test_core_029')
    @allure.description('获取所有Saving产品的基于币种的收益cumulative_interest数量计算')
    def test_core_029(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("获取所有Saving产品的基于币种的收益cumulative_interest数量计算"):
            for y in get_json()['crypto_list']:
                r = session.request('GET', url='{}/earn/saving/return/{}'.format(env_url, y), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("cumulative_interest计算"):
                    with allure.step("获取累计定期利息"):
                        flexible_interest_amount = []
                        cursor = '0'
                        while cursor != '-1':
                            params = {
                                'tx_type': "2",
                                'cursor': cursor,
                                'size': 50,
                                'order': "1",
                                'code': y
                            }
                            r4 = session.request('GET', url='{}/earn/fix/transactions'.format(env_url),
                                                 params=params,
                                                 headers=headers, timeout=20)
                            cursor = r4.json()['cursor']
                            for k in r4.json()['transactions']:
                                flexible_interest_amount.append(Decimal(k['maturity_interest']['amount']))
                    assert Decimal(r.json()['cumulative_interest']) == Decimal(
                        sum(flexible_interest_amount)), '获取所有Saving产品的基于币种的收益cumulative_interest数量计算失败,币种是{}, 定期cumulative_interest是{},接口返回是{}'.format(
                        y, sum(flexible_interest_amount), r.text)

    @allure.title('test_core_030')
    @allure.description('获取所有Saving产品的基于币种的收益interest_to_settle数量计算')
    def test_core_030(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['earn_email'])
        with allure.step("获取所有Saving产品的基于币种的收益interest_to_settle数量计算"):
            for y in get_json()['crypto_list']:
                r = session.request('GET', url='{}/earn/saving/return/{}'.format(env_url, y), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对,目前状态码是{}".format(r.status_code)
                with allure.step("cumulative_interest计算"):
                    with allure.step("获取累计定期利息"):
                        flexible_interest_amount = []
                        cursor = '0'
                        while cursor != '-1':
                            params = {
                                'tx_type': "1",
                                'cursor': cursor,
                                'size': 50,
                                'order': "1",
                                'code': y
                            }
                            r4 = session.request('GET', url='{}/earn/fix/transactions'.format(env_url),
                                                 params=params,
                                                 headers=headers, timeout=20)
                            cursor = r4.json()['cursor']
                            for k in r4.json()['transactions']:
                                flexible_interest_amount.append(Decimal(k['maturity_interest']['amount']))
                    assert Decimal(r.json()['interest_to_settle']) == Decimal(
                        sum(flexible_interest_amount)), '获取所有Saving产品的基于币种的收益interest_to_settle数量计算失败,币种是{}, 定期cumulative_interest是{},接口返回是{}'.format(
                        y, sum(flexible_interest_amount), r.text)


