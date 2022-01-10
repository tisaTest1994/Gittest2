from Function.web_function import *
from Function.api_function import *


class TestWebEarnApi:
    # 获取测试网站url
    web_url = get_json()['web'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()
        self.driver = webFunction.launch_web(self.web_url)
        webFunction.login_web(self.driver)
        operate_element(self.driver, 'assetPage', 'header-desktop-menu-item-WE099')

    def teardown_method(self):
        webFunction.logout_web(self.driver)
        self.driver.close()

    @allure.title('test_web_earn_001 检查图片')
    def test_web_earn_001(self):
        check_web_photo(self.driver, 'Eaenpage_earn.png')

