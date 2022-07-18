from Function.api_function import *
from Function.operate_sql import *


# kyc acceptance相关cases
class TestKycAcceptanceApi:
    url = get_json()['connect'][get_json()['env']]['url']
    with allure.step("登录客户账户获得后续操作需要的token"):
        ApiFunction.add_headers()

    def test_kyc_acceptance_001(self):  # connect vmode
        with allure.step("Latibac提交acceptance信息至kyc-archive"):
            account_id = 'd6ea720b-c971-4f5b-aa53-22c98eaf7986'  # account_vid
        with allure.step("测试data"):
            data = {
                "metadata": (None, json.dumps({"idDocType": "PASSPORT",  # PASSPORT,ID_CARD,DRIVERS
                                               "idIssuingCountry": "HKG",
                                               "lastName": "071305",
                                               "firstName": "winnie",
                                               "dob": "2022-07-14",
                                               "number": "0",
                                               "placeOfBirth": "HKG",
                                               "resident": {
                                                   "postalCode": "532421",
                                                   "country": "HKG",
                                                   "state": "latibac071304",
                                                   "city": "SH",
                                                   "streetLine1": "latibac071304-1",
                                                   "streetLine2": "latibac071304-2"
                                               },
                                               })),
                "a.png": ("id_doc_front.png",
                          open("/Users/Winnie/Desktop/a.JPG", "rb"),
                          "image/png"),
                "b.png": ("id_doc_front.png",
                          open("/Users/Winnie/Desktop/b.JPG", "rb"),
                          "image/png"),
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                url='/api/v1/accounts/{}/kycinfo/submit'.format(account_id),
                                                key='93a99e69-889a-47f4-9811-7bb98e25de62', nonce=nonce)
            headers['ACCESS-KEY'] = "90edccf2-ebee-4b35-9f87-c90bfcd1c174"
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

    def test_kyc_acceptance_002(self):
        with allure.step("gcp提交acceptance信息至kyc-archive"):  # OIDC
            account_id = '4711b473-4112-406a-8962-231c99a1b3c6'  # account_vid
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
                                                key='0d5e13da-d695-11ec-ae7e-0a3898443cb8', nonce=nonce)
            headers['ACCESS-KEY'] = "e1059392-d694-11ec-ae7e-0a3898443cb8"
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

    def test_kyc_acceptance_003(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winnie071301@test.com',
                                                                             password='A!234sdfg')
        with allure.step("获取kyc 预填信息"):
            r = session.request('POST', url='{}/kyc/case/sync/user/prepare/data'.format(env_url), headers=headers)
            print(r.json())

    def test_kyc_acceptance_004(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winnie071301@test.com',
                                                                             password='A!234sdfg')
        with allure.step("获取kyc 信息"):
            r = session.request('GET', url='{}/kyc/user/info/required'.format(env_url), headers=headers)
            print(r.json())

    # @allure.title('test_kyc_acceptance_005')
    # @allure.description('ops查看kyc archive信息')
    def test_kyc_acceptance_005(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("ops查看kyc archive信息"):
            account_id = "1a8891be-7f61-452e-bc87-89cb5b07cf43"
            data = {
                "source": "bybit"
            }
            r = session.request('POST',
                                url='{}/operatorapi/archive/{}'.format(operateUrl, account_id),
                                data=json.dumps(data),
                                headers=headers)
            print(r.json())
