from Function.api_function import *
from Function.operate_sql import *


# kyc acceptance相关cases
class TestKycAcceptanceApi:

    def test_kyc_acceptance_001(self):
        with allure.step("测试用户的account_id"):
            account_id = '5e5a2a0a-a4c3-4ced-8320-118ccbbc1c23'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce


