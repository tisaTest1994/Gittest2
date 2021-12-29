from Function.web_function import *
from Function.api_function import *


class TestCassApi:
    # 获取测试网站url
    web_url = get_json()['web'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()
        self.driver = webFunction.launch_web(self.web_url)
        webFunction.login_web(self.driver)

    def teardown_method(self):
        webFunction.logout_web(self.driver)
        self.driver.close()

    @allure.testcase('test_web_asset_001 查询Total Asset Value')
    def test_web_asset_001(self):
        pass

