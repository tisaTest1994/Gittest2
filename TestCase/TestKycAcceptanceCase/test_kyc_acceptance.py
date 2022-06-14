from Function.api_function import *
from Function.operate_sql import *


# kyc acceptance相关cases
class TestKycAcceptanceApi:
    url = get_json()['connect'][get_json()['env']]['url']
    with allure.step("登录客户账户获得后续操作需要的token"):
        ApiFunction.add_headers()

    def test_kyc_acceptance_001(self):
        with allure.step("测试用户的account_id"):
            account_id = 'f8eaf6d3-10e6-4f59-94c1-44f40ad54b4f'
        with allure.step("测试data"):
            data = {
                "metadata": (None, json.dumps({"idDocType": "PASSPORT",  # PASSPORT,ID_CARD,DRIVERS
                                               "idIssuingCountry": "HKG",
                                               "lastName": "060202",
                                               "firstName": "winnie",
                                               "dob": "2000-06-02",
                                               "number": "060202",
                                               "placeOfBirth": "HKG",
                                               "resident": {
                                                   "postalCode": "123456",
                                                   "country": "HKG",
                                                   "state": "STATE060202",
                                                   "city": "SH",
                                                   "streetLine1": "line1",
                                                   "streetLine2": "line2"
                                               },
                                               })),
                "a.png": ("id_doc_front.png",
                          open("/Users/Winnie/Desktop/a.JPG", "rb"),
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

    def test_kyc_acceptance_002(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winnie.wang+052404@cabital.com',
                                                                             password='A!234sdfg')
        with allure.step("获取kyc 预填信息"):
            r = session.request('POST', url='{}/kyc/case/sync/user/prepare/data'.format(env_url), headers=headers)
            print(r.json())

    def test_kyc_acceptance_003(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winnie.wang+051802@cabital.com',
                                                                             password='A!234sdfg')
        with allure.step("获取kyc 信息"):
            r = session.request('GET', url='{}/kyc/user/info/required'.format(env_url), headers=headers)
            print(r.json())
