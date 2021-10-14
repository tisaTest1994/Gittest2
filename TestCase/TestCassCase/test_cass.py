from Function.web_function import *
from Function.api_function import *

global driver


class TestCassApi:

    # 初始化
    def setup_method(self):
        pass

    # 结尾清理
    def teardown_method(self):
        pass

    @allure.testcase('test_cass_001 ')
    def test_cass_001(self):
        driver = webFunction.launch_web(get_json()['caas'][get_json()['env']]['url'])
        driver.switch_to_new_tab()
        with allure.step("登录网站"):
            webFunction.login_salesforce(driver=driver)
        driver.find_element_by_css_selector('search-button').send_keys('231')

        sleep(200)



