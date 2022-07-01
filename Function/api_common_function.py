from datetime import *
import requests
import random
import json
import os
import pytz
import time
import imaplib
import email
import chardet
import logger
import pyotp
import base64


# 获取当前时间
def get_now_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# 生成随机数字长度
def generate_number(number):
    a = ""
    for i in range(0, number):
        a = a + str(random.randint(0, 9))
    return a


# 生成随机字符串
def generate_string(number):
    a = ""
    for i in range(0, number):
        a = a + str(random.choice("0123456789qbcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ"))
    return a


# 生成随机电话号码
def generate_phone():
    return "135" + generate_number(8)


# 生成随机邮箱账号
def generate_email(Type='random', rang='random'):
    email_type = ["@qq.com", "@163.com", "@126.com", "@189.com", "@gmail.com"]
    # 如果没有指定邮箱类型，默认在 email_type中随机一个
    if Type == 'random':
        random_email = random.choice(email_type)
    else:
        random_email = type
    # 如果没有指定邮箱长度，默认在4-10之间随机
    if rang == 'random':
        rang_len = random.randint(4, 10)
    else:
        rang_len = int(rang)
    number = "0123456789qbcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ"
    __randomNumber = "".join(random.choice(number) for i in range(rang_len))
    email_account = __randomNumber + random_email
    return email_account


# 获得资源里面的配置参数
def get_json(file='setting.json'):
    path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/{}'.format(file)
    with open(path, "rb+") as f:
        js = json.load(f)
    return js


# 获得photo的url
def get_photo():
    path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/Photos'
    return path


# 修改资源里面的配置参数
def write_json(key, value, file='setting.json'):
    path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/{}'.format(file)
    with open(path, "rb+") as f:
        js = json.load(f)
    for i in js:
        if i == key:
            js[i] = value
    with open(path, "w") as f:
        json.dump(js, f, sort_keys=True, indent=2)


# 获得本日UTC时间的0点
def get_zero_utc_time():
    utc = pytz.timezone('UTC')
    utc_zero = datetime.now(tz=utc).strftime("%Y-%m-%d") + ' 0:00:00'
    logger.logger.info('UTC时间{}0点的时间戳是{}'.format(utc, utc_zero))
    return time.mktime(time.strptime(utc_zero, '%Y-%m-%d %H:%M:%S'))


# 切分一天时间
def get_zero_time(day_time=(datetime.now(tz=pytz.timezone('UTC')) + timedelta(days=-1)).strftime("%Y-%m-%d")):
    dt = datetime(int(day_time.split('-')[0]), int(day_time.split('-')[1]), int(day_time.split('-')[2]))
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    time_list = []
    i = timestamp
    while i < timestamp + 86400:
        i = i + 60
        time_list.append(i)
    return time_list


# 查询邮件
def get_email():
    client = imaplib.IMAP4_SSL(host=get_json()['email']['host'], port=get_json()['email']['port'])
    client.login(get_json()['email']['email'], get_json()['email']['security_code'])
    # 选择收件夹
    sleep_time = 0
    while sleep_time < 60:
        client.select('INBOX')
        type, data = client.search(None, 'ALL')
        num = str(len(str(data[0], 'utf-8').split(' ')))
        typ, data = client.fetch(num.encode(), '(RFC822)')
        if data[0] is not None:
            encoding = chardet.detect(data[0][1])
            msg = email.message_from_string(data[0][1].decode(encoding['encoding']))
            text, enc = email.header.decode_header(msg['subject'])[0]
            title = text.decode(enc) if enc else text
            if '(UTC)' in title:
                email_time = time.mktime(time.strptime(title.split(' - ')[1].split(' (UTC)')[0], "%Y-%m-%d %H:%M:%S"))
                utc_now_time = time.mktime(
                    time.strptime(datetime.now(tz=pytz.timezone('UTC')).strftime("%Y-%m-%d %H:%M:%S"),
                                  "%Y-%m-%d %H:%M:%S"))
                if int(email_time) + int(30) >= int(utc_now_time):
                    break
        sleep_time = sleep_time + 10
        time.sleep(10)
    assert data[0] is not None, 'email原始数据获取为空'
    return {"title": title, "body": data[0][1].decode(encoding['encoding'])}


# 获取翻译码
def get_language_map(type='app'):
    if type == 'app':
        r = requests.request('GET', url='https://mms.cabital.io/deploycodefile/cabital_app/{}/latest'.format(
            get_json()['language']), timeout=20)
        path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/multiple_languages_app.json'
    elif type == 'web':
        r = requests.request('GET', url='https://mms.cabital.io/deploycodefile/cabital_web/{}/latest'.format(
            get_json()['language']), timeout=20)
        path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/multiple_languages_web.json'
    else:
        r = requests.request('GET', url='https://mms.cabital.io/deploycodefile/cabital_app/{}/latest'.format(
            get_json()['language']), timeout=20)
        path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/multiple_languages_app.json'
    with open(path, "w+", encoding='utf8') as f:
        json.dump(r.json()['data'], f, sort_keys=True, indent=2, ensure_ascii=False)


# 删除小数点后多余的0
def delete_extra_zero(n):
    if isinstance(n, int):
        return n
    elif isinstance(n, float):
        n = str(n).rstrip('0')  # 删除小数点后多余的0
        n = int(n.rstrip('.')) if n.endswith('.') else float(n)  # 只剩小数点直接转int，否则转回float
        return n
    else:
        return n


# 控制货币单位长度
def crypto_len(number, type):
    # 删除多余的0
    number = delete_extra_zero(number)
    if '.' in str(number):
        if type == 'BTC' or type == 'ETH':
            if len(str(number).split('.')[1]) > 8:
                end_number = '{}.{}'.format(str(number).split('.')[0], str(number).split('.')[1][:8])
            else:
                end_number = '{}.{}'.format(str(number).split('.')[0], str(number).split('.')[1])
        elif type == 'USDT':
            if len(str(number).split('.')[1]) > 6:
                end_number = '{}.{}'.format(str(number).split('.')[0], str(number).split('.')[1][:6])
            else:
                end_number = '{}.{}'.format(str(number).split('.')[0], str(number).split('.')[1])
        else:
            if len(str(number).split('.')[1]) > 2:
                end_number = '{}.{}'.format(str(number).split('.')[0], str(number).split('.')[1][:2])
            else:
                end_number = '{}.{}'.format(str(number).split('.')[0], str(number).split('.')[1])
    else:
        end_number = number
    return str(end_number)


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if u'\u0030' <= uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar < u'\u0041' or uchar > u'\u005a') and (uchar < u'\u0061' or uchar > u'\u007a'):
        return False
    else:
        return True


# 获取iban账号
def get_iban(iban):
    if iban in ['GB', 'GG', 'JE', 'IM', 'RS']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(18))
    elif iban == 'NO':
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(11))
    elif iban == 'BE':
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(12))
    elif iban in ['DK', 'FI', 'NL', 'FO', 'GL']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(14))
    elif iban in ['MK', 'SI']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(15))
    elif iban in ['AT', 'BA', 'EE', 'KZ', 'LT', 'LU', 'XK']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(16))
    elif iban in ['CH', 'HR', 'LI', 'LV', 'CR']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(17))
    elif iban in ['BG', 'BH', 'DE', 'GE', 'IE', 'ME', 'RS']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(18))
    elif iban in ['CZ', 'ES', 'MD', 'PK', 'RO', 'SE', 'SK', 'TN', 'SA', 'VG', 'AD']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(20))
    elif iban in ['GI', 'IL', 'AE']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(19))
    elif iban in ['PT']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(21))
    elif iban in ['IS, TR']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(22))
    elif iban in ['FR', 'GR', 'IT', 'MC', 'MQ', 'PM', 'SM', 'TF', 'YT', 'MR']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(23))
    elif iban in ['AZ', 'CY', 'DO', 'GT', 'HU', 'LB', 'PL', 'AL']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(24))
    elif iban in ['QA', 'BR', 'PS']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(25))
    elif iban in ['JO', 'KW', 'MU']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(26))
    elif iban in ['MT', 'SC']:
        iban = '{}{}{}'.format(iban, generate_number(2), generate_string(27))
    return iban


# 增加货币符号
def add_currency_symbol(number, currency, is_symbol=False):
    currency = currency.upper()
    # 小数点后不足两位末尾加0,小数点后超过两位，末尾去0
    if '.' in str(number):
        number_int = str(number).split('.')[0]
        number_radix = str(number).split('.')[1]
        if len(number_radix) < 2:
            number_radix = str(number_radix) + '0'
        elif len(number_radix) > 2:
            if number_radix[-1] == 0:
                number_radix = number_radix[0:(len(number_radix) - 1)]
    elif number == 0 or number == '0':
        number_int = '0'
        number_radix = '0'
        if len(number_radix) < 2:
            number_radix = str(number_radix) + '0'
    else:
        number_int = str(number)
        number_radix = '00'
    count = 0
    sumstr = ''
    # 加逗号
    for one_str in number_int[::-1]:  # 注意循环是倒着输出的
        count += 1  # 计数
        if count % 3 == 0 and count != len(number_int):  # 如果count等于3或3的倍数并且不等于总长度
            one_str = ',' + one_str  # 当前循环的字符串前面加逗号
            sumstr = one_str + sumstr  # 拼接当前字符串
        else:
            sumstr = one_str + sumstr  # 正常拼接字符串
    if number_radix != '':
        sumstr = sumstr + '.' + number_radix
    if is_symbol:
        if currency == 'USD':
            sumstr = '$' + sumstr
        elif currency == 'EUR':
            sumstr = '€' + sumstr
        elif currency == 'GBP':
            sumstr = '£' + sumstr
        else:
            sumstr = '$' + sumstr
    return sumstr


# 数量加入,
def add_comma_number(number):
    if '.' in str(number):
        number_int = str(number).split('.')[0]
        number_radix = str(number).split('.')[1]
    else:
        number_int = str(number)
        number_radix = ''
    count = 0
    sumstr = ''
    for one_str in number_int[::-1]:  # 注意循环是倒着输出的
        count += 1  # 计数
        if count % 3 == 0 and count != len(number_int):  # 如果count等于3或3的倍数并且不等于总长度
            one_str = ',' + one_str  # 当前循环的字符串前面加逗号
            sumstr = one_str + sumstr  # 拼接当前字符串
        else:
            sumstr = one_str + sumstr  # 正常拼接字符串
    if number_radix != '':
        sumstr = sumstr + '.' + number_radix
    return sumstr


# 获取2fa google code
def get_mfa_code(secretKey=get_json()['secretKey']):
    old_2fa = get_json(file='latest_2fa.json')['2fa']
    totp = pyotp.TOTP(secretKey)
    new_2fa = totp.now()
    if old_2fa == new_2fa:
        time.sleep(30)
        totp = pyotp.TOTP(secretKey)
        new_2fa = totp.now()
        write_json('2fa', new_2fa, file='latest_2fa.json')
    else:
        write_json('2fa', new_2fa, file='latest_2fa.json')
    return new_2fa

get_mfa_code()
# Basic Auth
def get_basic_auth(username, password):
    temp_str = username + ':' + password
    # 转成bytes string
    bytesString = temp_str.encode(encoding="utf-8")
    # base64 编码
    encode_str = base64.b64encode(bytesString)
    return 'Basic ' + encode_str.decode()

