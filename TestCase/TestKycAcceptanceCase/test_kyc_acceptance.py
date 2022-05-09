from Function.api_function import *
from Function.operate_sql import *


# kyc acceptance相关cases
class TestKycAcceptanceApi:
    url = get_json()['connect'][get_json()['env']]['url']

    def test_kyc_acceptance_001(self):
        with allure.step("测试用户的account_id"):
            account_id = '9486e566-01f6-49db-9fe7-76f045683df9'
        with allure.step("测试data"):
            data = {
                "metadata": {"idDocType": "PASSPORT",
                             "country": "HKG",
                             "firstName": "richard",
                             "dob": "1990-01-01",
                             "number": "199001010015"
                             }
            }
            files = [('a.png', ('id_doc_front.png', open('/Users/richard.wan/Desktop/yilei/Test/TestCase/TestKycAcceptanceCase/a.png', 'rb'), 'image/png'))]
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                url='/api/v1/accounts/{}/kycinfo/submit'.format(account_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
            connect_headers['Content-Type'] = 'multipart/form-data'
        with allure.step("获取kyc info"):
            print(connect_headers)
            r = session.request('POST', url='{}/accounts/{}/kycinfo/submit'.format(self.url, account_id), headers=connect_headers, data=json.dumps(data), files=files)
            print(r.url)
            print(r.status_code)
            print(r.json())