import time

from Function.web_function import *
from Function.web_common_function import *
from Function.api_common_function import *

url_buy = "https://portal.latibac.com/connect/light?amount=1&feature=cfx&major_ccy=ETH&partner=coinex&type=buy"
url_sell = "https://portal.latibac.com/connect/light?amount=1&feature=cfx&major_ccy=ETH&partner=coinex&type=sell"

@allure.feature("web ui light mode 相关 testcases")
class TestWebLightMode:
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency

    def teardown_method(self):
        pass

    @allure.title('test_web_light_mode_001')
    @allure.description('Coinex Page从buy进入,cabital未登录')
    def test_light_mode_001(self, chrome_driver):
        with allure.step("打开cabital但不登录，打开light mode buy url"):
            operate_element_web(chrome_driver, '', url_buy, 'new_tab')
            handle1 = chrome_driver.window_handles[0]
            handle2 = chrome_driver.window_handles[1]
            chrome_driver.switch_to.window(handle2)
        with allure.step("点击Go to Cabital"):
            operate_element_web(chrome_driver, 'LightMode', 'header')
        with allure.step("判断是否引导用户到登录页面，并进行登录"):
            assert chrome_driver.current_url == 'https://portal.latibac.com/signin'
            webFunction.login_web(chrome_driver)
        with allure.step("判断是否跳转至Buy&Sell页面"):
            assert chrome_driver.current_url == 'https://portal.latibac.com/convert?shortlink=cfjsygbr&launch_date=apr_2022&c=coinex&af_ad=website&pid=non-network&deep_link_value=https://cabital.com&af_channel=partner'
        chrome_driver.close()
        chrome_driver.switch_to.window(handle1)

    @allure.title('test_web_light_mode_002')
    @allure.description('Coinex Page从buy进入,cabital已登录')
    def test_light_mode_002(self, chrome_driver):
        with allure.step("打开cabital并进行登录"):
            webFunction.login_web(chrome_driver)
        with allure.step("打开light mode buy url"):
            operate_element_web(chrome_driver, '', url_buy, 'new_tab')
            handle1 = chrome_driver.window_handles[0]
            handle2 = chrome_driver.window_handles[1]
            chrome_driver.switch_to.window(handle2)
        with allure.step("点击Go to Cabital"):
            operate_element_web(chrome_driver, 'LightMode', 'header')
        with allure.step("判断是否跳转至Buy&Sell页面"):
            assert chrome_driver.current_url == 'https://portal.latibac.com/convert?shortlink=cfjsygbr&launch_date=apr_2022&c=coinex&af_ad=website&pid=non-network&deep_link_value=https://cabital.com&af_channel=partner'
        chrome_driver.close()
        chrome_driver.switch_to.window(handle1)

    @allure.title('test_web_light_mode_003')
    @allure.description('Coinex Page从sell进入,cabital未登录')
    def test_light_mode_003(self, chrome_driver):
        with allure.step("打开cabital但不登录，打开light mode buy url"):
            operate_element_web(chrome_driver, '', url_sell, 'new_tab')
            handle1 = chrome_driver.window_handles[0]
            handle2 = chrome_driver.window_handles[1]
            chrome_driver.switch_to.window(handle2)
        with allure.step("点击Go to Cabital"):
            operate_element_web(chrome_driver, 'LightMode', 'header')
        with allure.step("判断是否引导用户到登录页面，并进行登录"):
            assert chrome_driver.current_url == 'https://portal.latibac.com/signin'
            webFunction.login_web(chrome_driver)
        with allure.step("判断是否跳转至Buy&Sell页面"):
            assert chrome_driver.current_url == 'https://portal.latibac.com/convert?shortlink=cfjsygbr&launch_date=apr_2022&c=coinex&af_ad=website&pid=non-network&deep_link_value=https://cabital.com&af_channel=partner'
        chrome_driver.close()
        chrome_driver.switch_to.window(handle1)

    @allure.title('test_web_light_mode_004')
    @allure.description('Coinex Page从sell进入,cabital已登录')
    def test_light_mode_004(self, chrome_driver):
        with allure.step("打开cabital并进行登录"):
            webFunction.login_web(chrome_driver)
        with allure.step("打开light mode buy url"):
            operate_element_web(chrome_driver, '', url_buy, 'new_tab')
            handle1 = chrome_driver.window_handles[0]
            handle2 = chrome_driver.window_handles[1]
            chrome_driver.switch_to.window(handle2)
        with allure.step("点击Go to Cabital"):
            operate_element_web(chrome_driver, 'LightMode', 'header')
        with allure.step("判断是否跳转至Buy&Sell页面"):
            assert chrome_driver.current_url == 'https://portal.latibac.com/convert?shortlink=cfjsygbr&launch_date=apr_2022&c=coinex&af_ad=website&pid=non-network&deep_link_value=https://cabital.com&af_channel=partner'
        chrome_driver.close()
        chrome_driver.switch_to.window(handle1)
