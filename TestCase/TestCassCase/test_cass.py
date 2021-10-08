from Function.web_function import *
from Function.api_function import *

global driver


class TestCassApi:

    # 初始化
    def setup_method(self):
        driver = webFunction.launch_web(get_json()['caas'][get_json()['env']]['url'])

    # 结尾清理
    def teardown_function(self):
        driver.quit()

    @allure.testcase('test_cass_001 ')
    def test_cass_001(self):
        driver = webFunction.launch_web(get_json()['caas'][get_json()['env']]['url'])
        driver.switch_to_new_tab()


