from run import *
from TestCase.TestWebCase.conftest import *
from selenium.webdriver.common.keys import Keys


# 操作页面元素
def operate_element_web(driver, page, element_string, type='click', input_string=''):
    if page == '':
        element_type = 'text'
    else:
        element_type = get_json(file='web_tree.json')[page][element_string]
    if type == 'click':
        if element_type == 'id':
            driver.find_element_by_id(element_string).click()
        elif element_type == 'name':
            driver.find_element_by_name(element_string).click()
        elif element_type == 'text':
            driver.find_element_by_xpath('//*[text()="{}"]'.format(element_string)).click()
        else:
            driver.find_element_by_xpath('//*[@{}="{}"]'.format(element_type, element_string)).click()
        logger.info('点击{}页面{}元素'.format(page, element_string))
    elif type == 'input':
        if element_type == 'id':
            driver.find_element_by_id(element_string).send_keys(input_string)
        elif element_type == 'name':
            driver.find_element_by_name(element_string).send_keys(input_string)
        else:
            driver.find_element_by_xpath('//*[@{}="{}"]'.format(element_type, element_string)).send_keys(input_string)
        logger.info("点击{}页面{}元素,输入{}".format(page, element_string, input_string))
    elif type == 'check':
        if element_type == 'id':
            result = driver.find_element_by_id(element_string).is_displayed()
            logger.info('{}页面{}元素是否存在{}'.format(page, element_string, result))
            return result
        elif element_type == 'name':
            result = driver.find_element_by_name(element_string).is_displayed()
            logger.info('{}页面{}元素是否存在{}'.format(page, element_string, result))
            return result
        elif element_type == 'text':
            result = driver.find_element_by_xpath('//*[text()="{}"]'.format(element_string)).is_displayed()
            logger.info('{}页面{}元素是否存在{}'.format(page, element_string, result))
            return result
        else:
            result = driver.find_element_by_xpath('//*[@{}="{}"]'.format(element_type, element_string)).is_displayed()
            logger.info('{}页面{}元素是否存在{}'.format(page, element_string, result))
            return result
    elif type == 'delete':
        if element_type == 'id':
            long = len(driver.find_element_by_id(element_string).get_attribute('value'))
            for i in range(0, long):
                if driver.find_element_by_id(element_string).get_attribute('value') != "":
                    driver.find_element_by_id(element_string).send_keys(Keys.COMMAND + 'a')
                    driver.find_element_by_id(element_string).send_keys(Keys.BACKSPACE)
                    i += 1
        elif element_type == 'name':
            long = len(driver.find_element_by_name(element_string).get_attribute('value'))
            for i in range(0, long):
                if driver.find_element_by_name(element_string).get_attribute('value') != "":
                    driver.find_element_by_id(element_string).send_keys(Keys.COMMAND + 'a')
                    driver.find_element_by_name(element_string).send_keys(Keys.BACKSPACE)
                    i += 1
        else:
            long = len(driver.find_element_by_xpath('//*[@{}="{}"]'.format(type, element_string)).get_attribute('value'))
            for i in range(0, long):
                if driver.find_element_by_xpath('//*[@{}="{}"]'.format(type, element_string)).get_attribute('value') != "":
                    driver.find_element_by_xpath('//*[@{}="{}"]'.format(type, element_string)).send_keys(Keys.BACKSPACE)
                    i += 1
    elif type == 'get_text':
        if element_type == 'id':
            return driver.find_element_by_id(element_string).text
        elif element_type == 'name':
            return driver.find_element_by_name(element_string).text
        else:
            return driver.find_element_by_xpath('//*[@{}="{}"]'.format(element_type, element_string)).text
    elif type == 'check_enabled':
        if element_type == 'id':
            result = driver.find_element_by_id(element_string).is_enabled()
            logger.info('{}页面{}元素是否可被修改{}'.format(page, element_string, result))
            return result
        elif element_type == 'name':
            result = driver.find_element_by_name(element_string).is_enabled()
            logger.info('{}页面{}元素是否可被修改{}'.format(page, element_string, result))
            return result
        else:
            result = driver.find_element_by_xpath('//*[@{}="{}"]'.format(element_type, element_string)).is_enabled()
            logger.info('{}页面{}元素是否可被修改{}'.format(page, element_string, result))
            return result
    elif type == 'check_selected':
        if element_type == 'id':
            result = driver.find_element_by_id(element_string).is_selected()
            logger.info('{}页面{}元素是否被选中{}'.format(page, element_string, result))
            return result
        elif element_type == 'name':
            result = driver.find_element_by_name(element_string).is_selected()
            logger.info('{}页面{}元素是否被选中{}'.format(page, element_string, result))
            return result
        else:
            result = driver.find_element_by_xpath('//*[@{}="{}"]'.format(element_type, element_string)).is_selected()
            logger.info('{}页面{}元素是否被选中{}'.format(page, element_string, result))
            return result
    elif type == 'get_value':
        if element_type == 'id':
            return driver.find_element_by_id(element_string).get_attribute('value')
        elif element_type == 'name':
            return driver.find_element_by_name(element_string).get_attribute('value')
        else:
            return driver.find_element_by_xpath('//*[@{}="{}"]'.format(element_type, element_string)).\
                get_attribute('value')
    elif type == 'check_exist':
        flag = True
        try:
            if element_type == 'id':
                driver.find_element_by_id(element_string)
                return flag
            elif element_type == 'name':
                driver.find_element_by_name(element_string)
                return flag
            else:
                driver.find_element_by_xpath('//*[@{}="{}"]'.format(element_type, element_string))
                return flag
        except:
            flag = False
            return flag
    else:
        return driver.find_element_by_xpath('//*[@{}="{}"]'.format(element_type, element_string))
    sleep(1)


# 图像识别
def check_web_photo(driver, photo_name):
    driver.assert_template(Template("{}/{}".format(get_photo(), photo_name)), "验证图片{}是否存在".format(photo_name))
