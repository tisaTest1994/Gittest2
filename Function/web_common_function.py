from airtest_selenium.proxy import WebChrome
from selenium import webdriver
from Function.api_function import *
import os


# 查询页面元素存在
def check_web(driver, page, text):
    wait_time = 0
    type = get_json(file='web_tree.json')[page][text]
    while wait_time < 20:
        if type == 'id':
            if driver.find_element_by_id(text).is_displayed():
                logger.info('在{}页面上寻找到了{}'.format(page, text))
                return True
        elif type == 'alt':
            if driver.find_element_by_xpath('//*[@alt="{}"]'.format(text)).is_displayed():
                logger.info('在{}页面上寻找到了{}'.format(page, text))
                return True
        wait_time = wait_time + 1
    return False


# 操作页面元素
def operate_element(driver, page, text, type='click', input=''):
    element_type = get_json(file='web_tree.json')[page][text]
    if check_web(driver, page, text):
        if element_type == 'id':
            if type == 'click':
                driver.find_element_by_id(text).click()
            elif type == 'clear':
                driver.find_element_by_id(text).clear()
            elif type == 'input':
                driver.find_element_by_id(text).send_keys(input)
        elif element_type == 'alt':
            if type == 'click':
                driver.find_element_by_xpath('//*[@alt="{}"]'.format(text)).click()
            elif type == 'clear':
                driver.find_element_by_xpath('//*[@alt="{}"]'.format(text)).clear()
            elif type == 'input':
                driver.find_element_by_xpath('//*[@alt="{}"]'.format(text)).send_keys(input)


# 获取页面元素的text
def get_element_text(driver, page, text):
    element_type = get_json(file='web_tree.json')[page][text]
    if element_type == 'id':
        return driver.find_element_by_id(text).text



