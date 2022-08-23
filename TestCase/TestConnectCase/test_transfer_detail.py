from Function.api_function import *
from Function.operate_sql import *


# 账户划转详情相关cases
class TestTransferDetailApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_transfer_detail_001')
    @allure.description('账户划转详情使用错误transfer_id')
    def test_transfer_detail_001(self):
        with allure.step("测试用户的account_id"):
            account_id = '96f29441-feb4-495a-a531-96c833e8261a'
            transfer_id = "f5346953-d422-4c56-846f-779fafd1c2b2"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers/{}'.format(account_id, transfer_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转详情使用错误transfer_id"):
            r = session.request('GET',
                                url='{}/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "账户划转详情使用错误transfer_id错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_detail_002')
    @allure.description('账户划转详情使用正确transfer_id')
    def test_transfer_detail_002(self):
        with allure.step("测试用户的account_id"):
            account_id = '96f29441-feb4-495a-a531-96c833e8261a'
            transfer_id = "fa8765b0-bc77-4ee8-840b-e292df6a9f06"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers/{}'.format(account_id, transfer_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转详情使用正确transfer_id"):
            r = session.request('GET',
                                url='{}/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert (r.json()['actual_amount'] == '0.02') and (r.json()['transfer_id']
                                                              == 'fa8765b0-bc77-4ee8-840b-e292df6a9f06'),\
                "账户划转详情使用正确transfer_id查询失败，返回值是{}".format(r.text)

    @allure.title('test_transfer_detail_003')
    @allure.description('对账 - 划转交易详情')
    def test_transfer_detail_003(self):
        external_id = '16'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/recon/transfers/{}'.format(external_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("划转交易详情使用正确external_id"):
            r = session.request('GET', url='{}/recon/transfers/{}'.format(self.url, external_id),headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfer_id'] == 'f5946953-d422-4c54-846f-789fafd1c2b2', "对账 - 划转交易详情错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_detail_004')
    @allure.description('对账 - 划转交易详情使用无效external_id')
    def test_transfer_detail_004(self):
        external_id = generate_string(15)
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/recon/transfers/{}'.format(external_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("划转交易详情使用无效external_id"):
            r = session.request('GET', url='{}/recon/transfers/{}'.format(self.url, external_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'PA030', "对账 - 划转交易详情使用无效external_id错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_detail_005')
    @allure.description('基于划转ID获取划转详情')
    def test_transfer_detail_005(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='neoding@yandex.com', password='Zcdsw123')
        transfer_id = "5fbbd31e-5703-4f0c-bdb7-3a43881c8c74"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/transfers/{}'.format(transfer_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("把数字货币从cabital转移到bybit账户"):
            r = session.request('GET', url='{}/transfers/{}'.format(self.url, transfer_id), headers=connect_headers)
            logger.info('r.json()返回值是{}'.format(r.json()))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['user_ext_ref'] == 'cd7e353b-6f4c-45db-bdd5-78bdc13a53c7', '基于划转ID获取划转详情错误，返回值是{}'.format(r.text)

    @allure.title('test_transfer_detail_006')
    @allure.description('UserExtRef划转列表（不传默认参数）')
    def test_transfer_detail_006(self):
        with allure.step("测试用户的account_id"):
            user_ext_ref = get_json()['bybit']['uid_A']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/userextref/{}/transfers'.format(user_ext_ref), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET', url='{}/userextref/{}/transfers'.format(self.url, user_ext_ref),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfers'] is not None, "账户划转列表错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_detail_007')
    @allure.description('UserExtRef划转列表（不传默认参数），Created权限校验')
    def test_transfer_detail_007(self):
        with allure.step("测试用户的account_id"):
            user_ext_ref = get_json()['bybit']['uid_B']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/userextref/{}/transfers'.format(user_ext_ref), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET', url='{}/userextref/{}/transfers'.format(self.url, user_ext_ref),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 403, "http状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_transfer_detail_008')
    @allure.description('交易列表查询（不传默认参数）')
    def test_transfer_detail_008(self):
        with allure.step("测试用户的account_id"):
            user_ext_ref = get_json()['bybit']['uid_A']
            tx_type_list = ['buy', 'convert', 'transfer']
        for tx_type in tx_type_list:
            with allure.step("验签"):
                unix_time = int(time.time())
                nonce = generate_string(30)
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                    url='/api/v1/accounts/{}/transactions/{}'.format(user_ext_ref, tx_type), nonce=nonce)
                connect_headers['ACCESS-SIGN'] = sign
                connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                connect_headers['ACCESS-NONCE'] = nonce
            with allure.step("账户划转列表"):
                r = session.request('GET', url='{}/accounts/{}/transactions/{}'.format(self.url, user_ext_ref, tx_type),
                                    headers=connect_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_transfer_detail_009')
    @allure.description('交易列表查询（不传默认参数）-Created权限校验')
    def test_transfer_detail_009(self):
        with allure.step("测试用户的account_id"):
            user_ext_ref = 'a765b947392c5c972601e334dbc9ab85'
            tx_type = 'transfer'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transactions/{}'.format(user_ext_ref, tx_type), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET', url='{}/accounts/{}/transactions/{}'.format(self.url, user_ext_ref, tx_type),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 403, "http状态码不对，目前状态码是{}".format(r.status_code)