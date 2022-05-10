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
