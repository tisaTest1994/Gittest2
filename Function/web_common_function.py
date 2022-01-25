from airtest_selenium.proxy import WebChrome
from selenium import webdriver
from Function.api_function import *
from airtest.core.api import *
from selenium.webdriver.common.keys import Keys
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
        elif type == 'class':
            if driver.find_element_by_xpath('//*[@class="{}"][1]'.format(text)).is_displayed():
                logger.info('在{}页面上寻找到了{}'.format(page, text))
                return True
        elif type == 'name':
            if driver.find_element_by_name(text).is_displayed():
                logger.info('在{}页面上寻找到了{}'.format(page, text))
                return True
        elif type == 'class':
            if driver.find_element_by_class_name(text).is_displayed():
                logger.info('在{}页面上寻找到了{}'.format(page, text))
                return True
        else:
            if driver.find_element_by_xpath(("//*[@" + type + '="{}"]').format(text)).is_displayed():
                logger.info('在{}页面上寻找到了{}'.format(page, text))
                return True
        wait_time = wait_time + 1
    return False


# 操作页面元素
def operate_element(driver, page, text, type='click', input='', cycle=15):
    element_type = get_json(file='web_tree.json')[page][text]
    if check_web(driver, page, text):
        if element_type == 'id':
            if type == 'click':
                driver.find_element_by_id(text).click()
            elif type == 'clear':
                driver.find_element_by_id(text).clear()
            elif type == 'input':
                driver.find_element_by_id(text).send_keys(input)
            elif type == 'delete':
                for i in range(cycle):
                    driver.find_element_by_id(text).send_keys(Keys.BACKSPACE)
            elif type == "clear2":
                js = 'document.querySelector("#' + text + '").value="";'
                driver.execute_script(js)
        elif element_type == 'alt':
            if type == 'click':
                driver.find_element_by_xpath('//*[@alt="{}"]'.format(text)).click()
            elif type == 'clear':
                driver.find_element_by_xpath('//*[@alt="{}"]'.format(text)).clear()
            elif type == 'input':
                driver.find_element_by_xpath('//*[@alt="{}"]'.format(text)).send_keys(input)
            elif type == 'delete':
                for i in range(cycle):
                    driver.find_element_by_xpath('//*[@alt="{}"]'.format(text)).send_keys(Keys.BACKSPACE)
        elif element_type == 'name':
            if type == 'click':
                driver.find_element_by_name(text).click()
            elif type == 'clear':
                driver.find_element_by_name(text).clear()
            elif type == 'input':
                driver.find_element_by_name(text).send_keys(input)
            elif type == 'delete':
                for i in range(cycle):
                    driver.find_element_by_name(text).send_keys(Keys.BACKSPACE)
        elif element_type == 'class':
            if type == 'click':
                driver.find_element_by_xpath('//*[@class="{}"]'.format(text)).click()
            elif type == 'clear':
                driver.find_element_by_xpath('//*[@class="{}"]'.format(text)).clear()
            elif type == 'input':
                driver.find_element_by_xpath('//*[@class="{}"]'.format(text)).send_keys(input)


# 获取页面元素的text
def get_element_text(driver, page, text):
    element_type = get_json(file='web_tree.json')[page][text]
    if element_type == 'id':
        return driver.find_element_by_id(text).text
    elif element_type == 'class':
        return driver.find_element_by_class_name(text).text
    else:
        return driver.find_element_by_xpath('//*[@{}="{}"]'.format(element_type, text)).text


# 图像识别
def check_web_photo(driver, photo_name):
    driver.assert_template(Template("{}/{}".format(get_photo(), photo_name)), "验证图片{}是否存在".format(photo_name))

