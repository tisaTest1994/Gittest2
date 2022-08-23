from Function.api_function import *
from Function.operate_sql import *


# kyc acceptance相关cases
class TestKycAcceptanceApi:
    url = get_json()['connect'][get_json()['env']]['url']
    with allure.step("登录客户账户获得后续操作需要的token"):
        ApiFunction.add_headers()

    def test_kyc_acceptance_001(self):  # connect vmode
        with allure.step("bybit提交acceptance信息至kyc-archive"):
            account_id = 'cd7e353b-6f4c-45db-bdd5-78bdc13a53c7'  # account_vid
        with allure.step("测试data"):
            data = {
                "metadata": (None, json.dumps({"idDocType": "PASSPORT",  # PASSPORT,ID_CARD,DRIVERS
                                               "idIssuingCountry": "HKG",
                                               "lastName": "071305",
                                               "firstName": "winnie",
                                               "dob": "2022-07-14",
                                               "number": "0",
                                               }
                                               ))

            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                url='/api/v1/accounts/{}/kycinfo/submit'.format(account_id),
                                                nonce=nonce, body=json.dumps(data))
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
            # headers['Content-Type'] = 'multipart/form-data'
            del headers['Content-Type']
        with allure.step("获取kyc info"):
            r = session.request('POST', url='{}/accounts/{}/kycinfo/submit'.format(self.url, account_id),
                                data=json.dumps(data), headers=connect_headers)
            print(r.status_code)



