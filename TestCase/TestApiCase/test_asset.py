from Function.api_function import *
from run import *
from Function.log import *
import allure


# asset相关cases
class TestAssetApi:

    @allure.testcase('test_asset_001 查询单笔交易')
    def test_asset_001(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
