from Function.api_function import *
from Function.operate_sql import *


# Transfer相关cases
class TestTransferApi:
    url = get_json()['infinni_games']['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("多语言支持"):
            headers['locale'] = 'zh-TW'
            headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']

