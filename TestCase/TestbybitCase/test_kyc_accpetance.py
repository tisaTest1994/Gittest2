from Function.api_function import *
from Function.operate_sql import *


# kyc acceptance相关cases
class TestKycAcceptanceApi:
    url = get_json()['connect'][get_json()['env']]['url']
    with allure.step("登录客户账户获得后续操作需要的token"):
        ApiFunction.add_headers()

    def test_kyc_acceptance_001(self):
        with allure.step("bybit提交acceptance信息至kyc-archive"):  # OIDC
            account_id = 'bacf2b3e-6599-44f4-adf6-c4c13ff40946'  # account_vid
        with allure.step("测试data"):
            data = {
                "metadata": (None, json.dumps({"idDocType": "ID_CARD",  # 2='PASSPORT',1='ID_CARD',DRIVERS
                                               "idIssuingCountry": "HKG",
                                               "lastName": "071304",
                                               "firstName": "winnie",
                                               "dob": "1992-11-18",
                                               "number": "0",
                                               "placeOfBirth": "HKG",
                                               "resident": {
                                                   "postalCode": "123456",
                                                   "country": "HKG",
                                                   "state": "gcp071304",
                                                   "city": "SH",
                                                   "streetLine1": "gcp071304-1",
                                                   "streetLine2": "gcp071304-2"
                                               },
                                               })),
                # "a.png": ("id_doc_front.png",
                #           open("/Users/Winnie/Desktop/a.JPG", "rb"),
                #           "image/png"),
                # "b.png": ("id_doc_front.png",
                #           open("/Users/Winnie/Desktop/b.JPG", "rb"),
                #           "image/png"),
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                url='/api/v1/accounts/{}/kycinfo/submit'.format(account_id),
                                                key='d7277081-3edd-47b6-b016-114f44f19320', nonce=nonce)
            headers['ACCESS-KEY'] = "8dbb1484-fba8-42ad-b177-48a841ecf045"
            headers['ACCESS-SIGN'] = sign
            headers['Content-Type'] = 'multipart/form-data'
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
            del headers['Content-Type']
        with allure.step("获取kyc info"):
            r = session.request('POST', url='{}/accounts/{}/kycinfo/submit'.format(self.url, account_id),
                                headers=headers, files=data)
            print(r.status_code)
            print(r.text)

