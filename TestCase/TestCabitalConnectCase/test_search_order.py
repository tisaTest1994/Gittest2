from Function.api_function import *
from Function.operate_sql import *


# 账户操作相关--账户入币信息
class TestSearchOrderApi:

    # 初始化class
    def setup(self):
        ApiFunction.add_headers()

    @allure.title('test_search_order_001')
    @allure.description('以帳號 account ID 查詢轉帳交易列表')
    def test_search_order_001(self, partner):
        with allure.step("获取用户VID"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(20) + str(time.time()).split('.')[0]
            sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/transfers'.format(account_vid), connect_type=partner, nonce=nonce)
            connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("以帳號 account ID 查詢轉帳交易列表"):
            r = session.request('GET', url='{}/accounts/{}/transfers'.format(connect_url, account_vid), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'pagination_response' in r.text, '以帳號 account ID 查詢轉帳交易列表失败，返回值是{}'.format(r.text)

    @allure.title('test_search_order_002')
    @allure.description('以合作方帳號 ID 查詢轉帳交易列表')
    def test_search_order_002(self, partner):
        with allure.step("获取用户VID"):
            user_ext_ref = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['user_ref_id']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(20) + str(time.time()).split('.')[0]
            sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/userextref/{}/transfers'.format(user_ext_ref), connect_type=partner, nonce=nonce)
            connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("以合作方帳號 ID 查詢轉帳交易列表"):
            r = session.request('GET', url='{}/userextref/{}/transfers'.format(connect_url, user_ext_ref), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'pagination_response' in r.text, '以合作方帳號 ID 查詢轉帳交易列表失败，返回值是{}'.format(r.text)

    @allure.title('test_search_order_003')
    @allure.description('以轉帳交易 ID 取得單一轉帳交易詳細資訊')
    def test_search_order_003(self, partner):
        transfer_id = "0b3729d3-cb6c-4e34-9d3c-8d7fc83b8f12"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(20) + str(time.time()).split('.')[0]
            sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/transfers/{}'.format(transfer_id), connect_type=partner, nonce=nonce)
            connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("以轉帳交易 ID 取得單一轉帳交易詳細資訊"):
            r = session.request('GET', url='{}/transfers/{}'.format(connect_url, transfer_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfer_id'] == transfer_id, '以轉帳交易 ID 取得單一轉帳交易詳細資訊失败，返回值是{}'.format(r.text)

    @allure.title('test_search_order_004')
    @allure.description('以合作方轉帳交易 ID 取得單一轉帳交易詳細資訊')
    def test_search_order_004(self, partner):
        external_id = "WU9sq8T8ewJtZBGSDEJ7mtlWu"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(20) + str(time.time()).split('.')[0]
            sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/recon/transfers/{}'.format(external_id), connect_type=partner, nonce=nonce)
            connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("以轉帳交易 ID 取得單一轉帳交易詳細資訊"):
            r = session.request('GET', url='{}/recon/transfers/{}'.format(connect_url, external_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['external_id'] == external_id, '以轉帳交易 ID 取得單一轉帳交易詳細資訊失败，返回值是{}'.format(r.text)

