from airtest_selenium.proxy import WebChrome
from selenium import webdriver
import os


class webFunction:

    @staticmethod
    def launch_web(web):
        # os.path.abspath()获得绝对路径
        path = os.path.abspath(os.path.dirname(__file__))
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        # 指定浏览器的分辨率
        options.add_argument('--window-size=1920,1080')
        # 无界面运行
        # options.add_argument('--headless')
        driver = WebChrome(executable_path=path + "/../Resource/chromedriver", chrome_options=options)
        driver.get(web)
        return driver


