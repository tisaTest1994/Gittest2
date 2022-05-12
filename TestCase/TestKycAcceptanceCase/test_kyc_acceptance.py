from Function.api_function import *
from Function.operate_sql import *


# kyc acceptance相关cases
class TestKycAcceptanceApi:
    url = get_json()['connect'][get_json()['env']]['url']

    def test_kyc_acceptance_001(self):
        with allure.step("测试用户的account_id"):
            account_id = 'a1391259-1457-4efa-916c-e052dfcf0b59'
        with allure.step("测试data"):
            data = {
                "metadata": (None, json.dumps({"idDocType": "PASSPORT",
                                               "country": "HKG",
                                               "firstName": "richard",
                                               "dob": "1990-01-01",
                                               "number": "199001010015"
                                               })),
                "a.png": ("id_doc_front.png",
                          open("/Users/richard.wan/Desktop/yilei/Test/TestCase/TestKycAcceptanceCase/a.png", "rb"),
                          "image/png"),
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                url='/api/v1/accounts/{}/kycinfo/submit'.format(account_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
            del connect_headers['Content-Type']
        with allure.step("获取kyc info"):
            print(connect_headers)
            r = session.request('POST', url='{}/accounts/{}/kycinfo/submit'.format(self.url, account_id),
                                headers=connect_headers, files=data)
            print(r.status_code)
            print(r.text)
