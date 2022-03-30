import time

from Function.web_function import *
from Function.web_common_function import *
from Function.api_common_function import *


@allure.feature("web ui deposit cash 相关 testcases")
class TestWebDeposit:
    # 获取测试网站url
    web_url = get_json()['web'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency

    def teardown_method(self):
        pass

    @allure.title('test_web_deposit_cash_001')
    @allure.description('select deposit currency')
    def test_deposit_cash_001(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击deposit按钮，并判断是否跳转至deposit页面,默认为deposit Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_deposit')
            assert operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_Deposit Cash', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("从metadata接口获取已开启的币种信息"):
            currency_metadata = session.request('GET', url='{}/core/metadata'.format(env_url), headers=headers)
            currency_list_metadata = currency_metadata.json()['currencies']
            currency_all_metadata = currency_list_metadata.keys()
        with allure.step("从接口获取币种信息,如在metada中关闭，则去除"):
            fiat = session.request('GET', url='{}/pay/deposit/ccy/fiat'.format(env_url), headers=headers)
            fiat_list = fiat.json()['fiat']
            fiat_all = []
            for i in range(0, len(fiat_list)):
                if fiat_list[i]['name'] in currency_all_metadata:
                    fiat_all.append(fiat_list[i]['name'])
            fiat_default = fiat_all[0]
        with allure.step("检查默认币种，并切换币种"):
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash', 'get_value') ==\
                   fiat_default, "默认币种错误"
            if "GBP" in fiat_all:
                # 点击下拉框
                operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
                # 选择GBP
                operate_element_web(chrome_driver, 'assetPage', 'undefined-option-GBP')
                time.sleep(2)
                # 检查币种是否切换成功
                assert operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash', 'get_value') == \
                       'GBP', '币种未切换至GBP'
            if "EUR" in fiat_all:
                # 点击下拉框
                operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
                # 选择EUR
                operate_element_web(chrome_driver, 'assetPage', 'undefined-option-EUR')
                time.sleep(2)
                # 检查币种是否切换成功
                assert operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash', 'get_value') ==\
                       'EUR', '币种未切换至EUR'
            if "EUR" in fiat_all:
                # 点击下拉框
                operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
                # 选择CHF
                operate_element_web(chrome_driver, 'assetPage', 'undefined-option-CHF')
                time.sleep(2)
                # 检查币种是否切换成功
                assert operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash', 'get_value') == \
                       'CHF', '币种未切换至CHF'

    @allure.title('test_web_deposit_cash_002')
    @allure.description('Deposit信息检查（cash）')
    def test_deposit_cash_002(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击deposit按钮，并判断是否跳转至deposit页面,默认为deposit Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_deposit')
            assert operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_Deposit Cash', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("从metadata接口获取已开启的币种信息"):
            currency_metadata = session.request('GET', url='{}/core/metadata'.format(env_url), headers=headers)
            currency_list_metadata = currency_metadata.json()['currencies']
            currency_all_metadata = currency_list_metadata.keys()
        with allure.step("从接口获取币种信息,如在metada中关闭，则去除"):
            fiat = session.request('GET', url='{}/pay/deposit/ccy/fiat'.format(env_url), headers=headers)
            fiat_list = fiat.json()['fiat']
            fiat_all = []
            for i in range(0, len(fiat_list)):
                if fiat_list[i]['name'] in currency_all_metadata:
                    fiat_all.append(fiat_list[i]['name'])
        with allure.step("从接口获取Deposit信息"):
            for j in range(0, len(fiat_all)):
                if fiat_all[j] == 'CHF':
                    operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
                    operate_element_web(chrome_driver, 'assetPage', 'undefined-option-CHF')
                    payment_method = 'SIC'
                elif fiat_all[j] == 'EUR':
                    operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
                    operate_element_web(chrome_driver, 'assetPage', 'undefined-option-EUR')
                    payment_method = 'SEPA'
                elif fiat_all[j] == 'GBP':
                    operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
                    operate_element_web(chrome_driver, 'assetPage', 'undefined-option-GBP')
                    payment_method = 'Faster%20Payments'
                r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, fiat_all[j], payment_method), headers=headers)
                deposit_info = r.json()['bank_accounts'][0]
                account_name = deposit_info['account_name']
                if fiat_all[j] == 'GBP':
                    account_number = deposit_info['account_number']
                    sort_code = deposit_info['sort_code']
                else:
                    iban = deposit_info['iban']
                    bic = deposit_info['bic']
                reference_code = deposit_info['ref_code']
                bank_name = deposit_info['bank_name']
                bank_country = deposit_info['bank_country']
                bank_address = deposit_info['bank_address']
                with allure.step("判断信息是否在页面上显示"):
                    assert operate_element_web(chrome_driver, '', account_name, 'check'), '当前币种是{}, {}显示的信息与接口返回信息不符'.format(fiat_all[j], account_name)
                    if fiat_all[j] == 'GBP':
                        assert operate_element_web(chrome_driver, '', account_number, 'check'), '当前币种是{}, {}显示的信息与接口返回信息不符'.format(fiat_all[j],account_number)
                        assert operate_element_web(chrome_driver, '', sort_code, 'check'), '当前币种是{}, {}显示的信息与接口返回信息不符'.format(fiat_all[j],sort_code)
                    else:
                        assert operate_element_web(chrome_driver, '', iban, 'check'), '当前币种是{}, {}显示的信息与接口返回信息不符'.format(fiat_all[j], iban)
                        assert operate_element_web(chrome_driver, '', bic, 'check'), '当前币种是{}, {}显示的信息与接口返回信息不符'.format(fiat_all[j], bic)
                    assert operate_element_web(chrome_driver, '', reference_code, 'check'), '当前币种是{}, {}显示的信息与接口返回信息不符'.format(fiat_all[j], reference_code)
                    assert operate_element_web(chrome_driver, '', bank_name, 'check'), '当前币种是{}, {}显示的信息与接口返回信息不符'.format(fiat_all[j], bank_name)
                    assert operate_element_web(chrome_driver, '', bank_country, 'check'), '当前币种是{}, {}显示的信息与接口返回信息不符'.format(fiat_all[j], bank_country)
                    assert operate_element_web(chrome_driver, '', bank_address, 'check'), '当前币种是{}, {}显示的信息与接口返回信息不符'.format(fiat_all[j], bank_address)
