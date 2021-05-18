from Function.api_function import *
from run import *
from Function.log import *
import allure


# payout相关cases
class TestPayoutApi:

    # 初始化class
    def setup_class(self):
        AccountFunction.add_headers()

    @allure.testcase('test_payout_001 没有Kyc用户添加常用收款地址失败')
    def test_payout_001(self):
        account = generate_email()
        password = 'Abc112233'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("没有Kyc用户添加常用收款地址失败"):
            data = {
                "nickName": "alan EUR ERC20",
                "currency": "USDT",
                "method": "ERC20",
                "address": "test-address"
            }
            r = session.request('POST', url='{}/account/myPayee/create'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 403, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_FORBIDDEN' in r.text, "没有Kyc用户添加常用收款地址失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_002 有Kyc用户添加非ETH常用收款地址')
    def test_payout_002(self):
        with allure.step("有Kyc用户添加非ETH常用收款地址"):
            List = ["USDT", "BTC"]
            for i in List:
                data = {
                    "nickName": generate_string(20),
                    "currency": i,
                    "method": "ERC20",
                    "address": generate_string(30)
                }
                r = session.request('POST', url='{}/account/myPayee/create'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('添加{}的常用地址，返回值是{}'.format(i, str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert {} == r.json(), "有Kyc用户添加非ETH常用收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_003 获取存储的常用收款地址list')
    def test_payout_003(self):
        with allure.step("获取存储的常用收款地址list"):
            r = session.request('GET', url='{}/account/myPayee/list'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['payeeList'] is not None, "获取存储的常用收款地址list错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_004 获取某个常用收款地址')
    def test_payout_004(self):
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

    @allure.testcase('test_payout_005 使用不存在id获取常用收款地址')
    def test_payout_005(self):
        with allure.step("使用不存在id获取常用收款地址"):
            r = session.request('GET', url='{}/account/myPayee/{}'.format(env_url, '1111300'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_MY_PAYEE_000001' in r.text, "使用不存在id获取常用收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_006 更新收款地址')
    def test_payout_006(self):
        with allure.step("更新收款地址"):
            data = {
                "nickName": "alan EUR ERC20",
                "currency": "EUR",
                "method": "ERC20",
                "address": generate_string(30),
                "isValid": True,
                "whitelisted": False
            }
            r = session.request('PUT', url='{}/account/myPayee/{}'.format(env_url, '3'), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "更新收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_007 更新使用不存在id收款地址')
    def test_payout_007(self):
        with allure.step("更新使用不存在id收款地址"):
            data = {
                "nickName": "alan EUR ERC20",
                "currency": "ETH",
                "method": "ERC20",
                "address": generate_string(30),
                "isValid": True,
                "whitelisted": False
            }
            r = session.request('PUT', url='{}/account/myPayee/{}'.format(env_url, '300'), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Invalid payee address' in r.text, "更新使用不存在id收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_008 删除常用收款地址')
    def test_payout_008(self):
        with allure.step("获取收款地址list"):
            r = session.request('GET', url='{}/account/myPayee/list'.format(env_url), headers=headers)
        with allure.step("获取单个收款地址id"):
            id = r.json()['payeeList'][0]['id']
        with allure.step("删除常用收款地址"):
            session.request('Delete', url='{}/account/myPayee/{}'.format(env_url, id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "payeeList" in r.text, "删除收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_009 删除不存在的收款地址')
    def test_payout_009(self):
        with allure.step("凭借空id号删除地址"):
            r = session.request('DELETE', url='{}/account/myPayee/{}'.format(env_url, '123131300'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_MY_PAYEE_000001' in r.text, "删除收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_010 获取提现费率和提现限制')
    def test_payout_010(self):
        with allure.step("获取提现费率和提现限制"):
            data = {
                "amount": "0.11",
                "code": "ETH",
                "address": "0x623089BFb1dc2d3023Ba4bd0f42F61d66826994eu",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/verification'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '"fee":"0.001"' in r.text, "获取提现费率和提现限制错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_011 提现BTC成功')
    def test_payout_011(self):
        with allure.step("提现BTC成功"):
            data = {
                "amount": "0.001",
                "code": "BTC",
                "address": "tb1qw5vxujxtp0zqueman28cwm344tucezhxenvfrg",
                "method": ""
            }
            r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transaction_id'] is not None, "提现BTC错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_012 提现ETH成功')
    def test_payout_012(self):
        with allure.step("提现ETH成功"):
            data = {
                "amount": "0.02",
                "code": "ETH",
                "address": "0x428DA40C585514022b2eB537950d5AB5C7365a07",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transaction_id'] is not None, "提现ETH错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_013 提现USDT成功')
    def test_payout_013(self):
        with allure.step("提现USDT成功"):
            data = {
                "amount": "40",
                "code": "USDT",
                "address": "0x428DA40C585514022b2eB537950d5AB5C7365a07",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transaction_id'] is not None, "提现USDT错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_014 提现超过可用数量的BTC，返回失败')
    def test_payout_014(self):
        with allure.step("提现超过可用数量的BTC，返回失败"):
            data = {
                "amount": "999999999",
                "code": "BTC",
                "address": "tb1qw5vxujxtp0zqueman28cwm344tucezhxenvfrg",
                "method": ""
            }
            r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'WALLET000003' in r.text, "提现超过可用数量的BTC，返回失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_015 提现超过可用数量的ETH，返回失败')
    def test_payout_015(self):
        with allure.step("提现超过可用数量的ETH，返回失败"):
            data = {
                "amount": "999999",
                "code": "ETH",
                "address": "0x428DA40C585514022b2eB537950d5AB5C7365a07",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'WALLET000003' in r.text, "提现超过可用数量的ETH，返回失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_016 提现超过可用数量的USDT，返回失败')
    def test_payout_016(self):
        with allure.step("提现超过可用数量的USDT，返回失败"):
            data = {
                "amount": "99999999",
                "code": "USDT",
                "address": "0xB76a92f3293b8Fa0f30aA4FfF75325201C2F67F6",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'WALLET000003' in r.text, "提现超过可用数量的USDT，返回失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_017 提现小于最低要求数量的BTC，返回失败')
    def test_payout_017(self):
        with allure.step("提现小于最低要求数量的BTC，返回失败"):
            data = {
                "amount": "0.00099",
                "code": "BTC",
                "address": "tb1qw5vxujxtp0zqueman28cwm344tucezhxenvfrg",
                "method": ""
            }
            r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'PAYOUTTXN000025' in r.text, "提现小于最低要求数量的BTC，返回失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_018 提现小于最低要求数量的ETH，返回失败')
    def test_payout_018(self):
        with allure.step("提现超过可用数量的ETH，返回失败"):
            data = {
                "amount": "0.019",
                "code": "ETH",
                "address": "0x428DA40C585514022b2eB537950d5AB5C7365a07",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'PAYOUTTXN000025' in r.text, "提现小于最低要求数量的ETH，返回失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_019 提现小于最低要求数量的USDT，返回失败')
    def test_payout_019(self):
        with allure.step("提现超过可用数量的USDT，返回失败"):
            data = {
                "amount": "39",
                "code": "USDT",
                "address": "0xB76a92f3293b8Fa0f30aA4FfF75325201C2F67F6",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'PAYOUTTXN000025' in r.text, "提现超过可用数量的USDT，返回失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_020 查询提现详情')
    def test_payout_020(self):
        with allure.step("获得交易transaction_id"):
            transaction_id = AccountFunction.get_payout_transaction_id()
            logger.info('transaction_id是{}'.format(transaction_id))
        with allure.step("查询提现详情"):
            r = session.request('GET', url='{}/pay/withdraw/transactions/{}'.format(env_url, transaction_id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'status' in r.text, "查询提现详情错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_021 使用错误id查询提现详情')
    def test_payout_021(self):
        with allure.step("查询提现详情"):
            r = session.request('GET', url='{}/pay/withdraw/transactions/{}'.format(env_url, '468422531310-3fa0-4bd1-9d46-4467dfa9ce52'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'no rows in result set' in r.text, "使用错误id查询提现详情错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_022 有Kyc用户添加ETH常用收款地址')
    def test_payout_022(self):
        with allure.step("有Kyc用户添加ETH常用收款地址"):
            data = {
                "nickName": generate_string(20),
                "currency": "ETH",
                "method": "ERC20",
                "address": "0x428DA40C585514022b2eB537950d5AB5C7365a07"
            }
            r = session.request('POST', url='{}/account/myPayee/create'.format(env_url), data=json.dumps(data),
                                 headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('添加{}的常用地址，返回值是{}'.format("0x428DA40C585514022b2eB537950d5AB5C7365a07", str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert {} == r.json(), "有Kyc用户添加ETH常用收款地址错误，返回值是{}".format(r.text)
