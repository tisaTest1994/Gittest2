from Function.web_function import *
from Function.api_function import *


class TestCassApi:

    # 初始化
    def setup_function(self):
        driver = webFunction.launch_web(get_json()['caas'][get_json()['env']]['url'])

    @allure.testcase('test_cass_001 ')
    def test_cass_001(self):
        drivers = self.driver
        drivers.switch_to_new_tab()
