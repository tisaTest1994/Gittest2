from airtest_selenium.proxy import WebChrome
from selenium import webdriver
from Function.api_function import *
import os


# 查询页面元素存在
def check_web(driver, text):
    wait_time = 0
    while wait_time < 20:
        if driver.find_element_by_id(text).is_displayed():
            logger.info('在页面上寻找到了{}'.format(text))
            return True
        wait_time = wait_time + 1
    return False

