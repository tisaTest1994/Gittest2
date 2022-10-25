from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api payout 相关 testcases")
class TestPayoutApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_payout_001')
    @allure.description('没有Kyc用户添加常用收款地址失败')
    def test_payout_001(self):
        account = generate_email()
        password = get_json()['email']['password']
        with allure.step("提前先注册好"):
            ApiFunction.sign_up(account, password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=account, password=password)
        with allure.step("没有Kyc用户添加常用收款地址失败"):
            data = {
                "nickName": "alan EUR ERC20",
                "currency": "USDT",
                "method": "ERC20",
                "address": "0xf4af4d6dfcba0844d78bf091070d33c0e378cc88"
            }
            r = session.request('POST', url='{}/account/myPayee/create'.format(env_url), data=json.dumps(data),
                                headers=headers)
        ApiFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 403, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'ACC_FORBIDDEN', "没有Kyc用户添加常用收款地址失败错误，返回值是{}".format(r.text)

    @allure.title('test_payout_002')
    @allure.description('获取存储的常用收款地址list')
    def test_payout_002(self):
        with allure.step("获取存储的常用收款地址list"):
            r = session.request('GET', url='{}/account/myPayee/list'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['payeeList'] is not None, "获取存储的常用收款地址list错误，返回值是{}".format(r.text)

    @allure.title('test_payout_003')
    @allure.description('获取某个常用收款地址')
    def test_payout_003(self):
        with allure.step("获取收款地址list"):
            r = session.request('GET', url='{}/account/myPayee/list'.format(env_url), headers=headers)
        with allure.step("获取单个收款地址id"):
            id = r.json()['payeeList'][0]['id']
        with allure.step("获取某个常用收款地址"):
            r = session.request('GET', url='{}/account/myPayee/{}'.format(env_url, id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['payeeList'] is not None, "获取某个常用收款地址错误，返回值是{}".format(r.text)

    @allure.title('test_payout_004')
    @allure.description('使用不存在id获取常用收款地址')
    def test_payout_004(self):
        with allure.step("使用不存在id获取常用收款地址"):
            r = session.request('GET', url='{}/account/myPayee/{}'.format(env_url, '1111300'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == '001015', "使用不存在id获取常用收款地址错误，返回值是{}".format(r.text)

    @allure.title('test_payout_005')
    @allure.description('删除不存在的收款地址')
    def test_payout_005(self):
        with allure.step("凭借空id号删除地址"):
            r = session.request('DELETE', url='{}/account/myPayee/{}'.format(env_url, '123131300'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == '001015', "删除收款地址错误，返回值是{}".format(r.text)

    @allure.title('test_payout_006')
    @allure.description('查询提现详情')
    def test_payout_006(self):
        with allure.step("获得交易transaction_id"):
            transaction_id = ApiFunction.get_payout_transaction_id()
            logger.info('transaction_id是{}'.format(transaction_id))
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token()
        with allure.step("查询提现详情"):
            r = session.request('GET', url='{}/pay/withdraw/transactions/{}'.format(env_url, transaction_id),
                                headers=headers)
            ApiFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'status' in r.text, "查询提现详情错误，返回值是{}".format(r.text)

    @allure.title('test_payout_007')
    @allure.description('使用错误id查询提现详情')
    def test_payout_007(self):
        with allure.step("查询提现详情"):
            r = session.request('GET', url='{}/pay/withdraw/transactions/{}'.format(env_url,
                                                                                    '4684225231310-3fa0-4bd1-9d46-4467dfa9ce52'),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'no rows in result set' in r.text, "使用错误id查询提现详情错误，返回值是{}".format(r.text)

    @allure.title('test_payout_008')
    @allure.description('获得全部提现币种')
    def test_payout_008(self):
        with allure.step("提现币种"):
            r = session.request('GET', url='{}/pay/withdraw/ccy/{}'.format(env_url, ''), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'fiat' in r.text, "获得全部提现币种错误，返回值是{}".format(r.text)
                assert 'crypto' in r.text, "获得全部提现币种错误，返回值是{}".format(r.text)

    @allure.title('test_payout_009')
    @allure.description('获取所有币种提现方式')
    def test_payout_009(self):
        with allure.step("获取所有可以提现的币种"):
            r = session.request('GET', url='{}/pay/withdraw/ccy/{}'.format(env_url, ''), headers=headers)
        ccy = []
        for y in (r.json()['fiat'] + r.json()['crypto']):
            if y['status'] == 1:
                ccy.append(y['name'])
        ccy.remove('VND')
        for i in ccy:
            with allure.step("获取法币{}的提现方式".format(i)):
                r = session.request('GET', url='{}/pay/withdraw/{}'.format(env_url, i), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                if i == 'BTC':
                    assert r.json()['payment_methods'][0]['type'] == "Bitcoin" \
                           and r.json()['payment_methods'][0]['method'] == "BTC" \
                           and r.json()['payment_methods'][0]['key'] == "BTC" \
                           and r.json()['payment_methods'][0]['status'] == 1,\
                        "币种{}提现方式错误，接口返回结果为{}".format(i, r.json()['payment_methods'])
                elif i == 'ETH':
                    assert r.json()['payment_methods'][0]['type'] == "Ethereum(ERC-20)" \
                           and r.json()['payment_methods'][0]['method'] == "ERC20" \
                           and r.json()['payment_methods'][0]['key'] == "ETH" \
                           and r.json()['payment_methods'][0]['status'] == 1, \
                        "币种{}提现方式错误，接口返回结果为{}".format(i, r.json()['payment_methods'])
                elif i == 'USDT':
                    assert r.json()['payment_methods'][0]['type'] == "Ethereum(ERC-20)" \
                           and r.json()['payment_methods'][0]['method'] == "ERC20" \
                           and r.json()['payment_methods'][0]['key'] == "ETH" \
                           and r.json()['payment_methods'][0]['status'] == 1, \
                        "币种{}提现方式错误，接口返回结果为{}".format(i, r.json()['payment_methods'])
                elif i == 'USD':
                    assert r.json()['payment_methods'][0]['type'] == "Ethereum(ERC-20)" \
                           and r.json()['payment_methods'][0]['method'] == "ERC20" \
                           and r.json()['payment_methods'][0]['key'] == "ETH" \
                           and r.json()['payment_methods'][0]['status'] == 1 \
                           and r.json()['payment_methods'][0]['ccy'] == "USDC", \
                        "币种{}提现方式错误，接口返回结果为{}".format(i, r.json()['payment_methods'])
                elif i == 'USDT':
                    assert r.json()['payment_methods'][0]['type'] == "Ethereum(ERC-20)" \
                           and r.json()['payment_methods'][0]['method'] == "ERC20" \
                           and r.json()['payment_methods'][0]['key'] == "ETH" \
                           and r.json()['payment_methods'][0]['status'] == 1, \
                        "币种{}提现方式错误，接口返回结果为{}".format(i, r.json()['payment_methods'])
                elif i == 'EUR':
                    assert r.json()['payment_methods'][0]['type'] == "SEPA" \
                           and r.json()['payment_methods'][0]['method'] == "SEPA" \
                           and r.json()['payment_methods'][0]['key'] == "SEPA" \
                           and r.json()['payment_methods'][0]['status'] == 1, \
                        "币种{}提现方式错误，接口返回结果为{}".format(i, r.json()['payment_methods'])
                elif i == 'GBP':
                    assert r.json()['payment_methods'][0]['type'] == "Faster Payments" \
                           and r.json()['payment_methods'][0]['method'] == "Faster Payments" \
                           and r.json()['payment_methods'][0]['key'] == "Faster Payments" \
                           and r.json()['payment_methods'][0]['status'] == 1, \
                        "币种{}提现方式错误，接口返回结果为{}".format(i, r.json()['payment_methods'])
                elif i == 'CHF':
                    assert r.json()['payment_methods'][0]['type'] == "SIC/SWIFT" \
                           and r.json()['payment_methods'][0]['method'] == "SIC/SWIFT" \
                           and r.json()['payment_methods'][0]['key'] == "SIC" \
                           and r.json()['payment_methods'][0]['status'] == 1, \
                        "币种{}提现方式错误，接口返回结果为{}".format(i, r.json()['payment_methods'])
                elif i == 'BRL':
                    assert r.json()['payment_methods'][0]['type'] == "PIX" \
                           and r.json()['payment_methods'][0]['method'] == "PIX" \
                           and r.json()['payment_methods'][0]['key'] == "PIX" \
                           and r.json()['payment_methods'][0]['status'] == 1, \
                        "币种{}提现方式错误，接口返回结果为{}".format(i, r.json()['payment_methods'])
                else:
                    assert False, "提现币种有新增需要维护脚本"