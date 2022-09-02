from Function.api_function import *
from Function.operate_sql import *


# 账户划转相关cases
class TestTransferApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_transfer_001')
    @allure.description('partner发起请求，把资金从cabital转移到partner账户')
    def test_transfer_001(self, partner):
        with allure.step("获取用户的account_vid"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']
        with allure.step("获得otp"):
            mfaVerificationCode = get_mfa_code('richard')
        with allure.step("获得data"):
            external_id = generate_string(25)
            data = {
                'amount': '20',
                'symbol': 'USDT',
                'otp': str(mfaVerificationCode),
                'direction': 'DEBIT',
                'external_id': external_id
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_signature(unix_time=str(unix_time), method='POST', url='/api/v1/accounts/{}/transfers'.format(account_vid), connect_type=partner, nonce=nonce, body=json.dumps(data))
            connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("把数字货币从cabital转移到bybit账户"):
            r = session.request('POST', url='{}/accounts/{}/transfers'.format(connect_url, account_vid), data=json.dumps(data), headers=connect_headers)
            logger.info('r.json()返回值是{}'.format(r.json()))
        # if "PA043" not in r.text:
        #     with allure.step("校验状态码"):
        #         assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        #     with allure.step("验签"):
        #         unix_time = int(time.time())
        #         nonce = generate_string(30)
        #         sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
        #                                             url='/api/v1/recon/transfers/{}'.format(external_id),
        #                                             nonce=nonce)
        #         connect_header['ACCESS-SIGN'] = sign
        #         connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
        #         connect_header['ACCESS-NONCE'] = nonce
        #     with allure.step("查询转账记录"):
        #         r = session.request('GET', url='{}/recon/transfers/{}'.format(self.url, external_id),
        #                             headers=connect_header)
        #     with allure.step("状态码和返回值"):
        #         logger.info('状态码是{}'.format(str(r.status_code)))
        #         logger.info('返回值是{}'.format(str(r.text)))
        #     with allure.step("校验状态码"):
        #         assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        #     with allure.step("校验返回值"):
        #         assert r.json()['external_id'] == external_id, "查询转账记录错误，返回值是{}".format(r.text)
        # else:
        #     with allure.step("校验状态码"):
        #         assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        #     logger.info('由于每日限额超额，该笔transfer交易不成功，message是{}'.format(r.json()['message']))

    # @allure.title('test_transfer_007')
    # @allure.description('从cabital转移到bybit账户并且关联C+T交易')
    # def test_transfer_007(self):
    #     with allure.step("测试用户的account_id"):
    #         account_id = get_json()['email']['accountId']
    #     with allure.step("换汇"):
    #         for i in ApiFunction.get_connect_cfx_list(self.url, connect_header):
    #             sleep(5)
    #             with allure.step('换汇'):
    #                 transaction = ApiFunction.cfx_random(i, i.split('-')[0], type='bybit', account_id=account_id, headers=connect_header, url=self.url)
    #                 cfx_transaction_id = transaction['returnJson']['transaction_id']
    #             with allure.step("获得otp"):
    #                 mfaVerificationCode = get_mfa_code('richard')
    #             with allure.step("获得data"):
    #                 if i.split('-')[0] in get_json()['crypto_list']:
    #                     symbol = i.split('-')[0]
    #                 else:
    #                     symbol = i.split('-')[1]
    #                 data = {
    #                     'amount': transaction['data']['buy_amount'],
    #                     'symbol': symbol,
    #                     'otp': str(mfaVerificationCode),
    #                     'direction': 'DEBIT',
    #                     'external_id': generate_string(15),
    #                     'conversion_id': cfx_transaction_id
    #                 }
    #             with allure.step("验签"):
    #                 unix_time = int(time.time())
    #                 nonce = generate_string(30)
    #                 sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
    #                                                     url='/api/v1/accounts/{}/transfers'.format(
    #                                                         account_id),
    #                                                     nonce=nonce,
    #                                                     body=json.dumps(data))
    #                 connect_header['ACCESS-SIGN'] = sign
    #                 connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
    #                 connect_header['ACCESS-NONCE'] = nonce
    #             with allure.step("把BTC从cabital转移到bybit账户并且关联C+T交易"):
    #                 r = session.request('POST',
    #                                     url='{}/accounts/{}/transfers'.format(self.url, account_id),
    #                                     data=json.dumps(data), headers=connect_header)
    #                 logger.info('r.json返回值是{}'.format(r.json()))
    #             with allure.step("状态码和返回值"):
    #                 logger.info('状态码是{}'.format(str(r.status_code)))
    #                 logger.info('返回值是{}'.format(str(r.text)))
    #             with allure.step("校验状态码"):
    #                 if r.status_code == 200:
    #                     assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
    #                     with allure.step("校验返回值"):
    #                         assert r.json()['status'] == 'SUCCESS', "把BTC从cabital转移到bybit账户并且关联C+T交易错误，返回值是{}".format(r.text)
    #                 else:
    #                     assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
    #                     with allure.step("校验返回值"):
    #                         assert r.json()['code'] == 'PA043', "关联C+T交易错误，返回值是{}".format(r.text)

