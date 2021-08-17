from datetime import *

import requests
from faker import Faker
import random
import json
import os
import pytz
import time
import imaplib
import email
import chardet
import logger


# 获取当前时间
def get_now_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# 生成随机人名
def generate_name():
    fake = Faker('zh_CN')
    return fake.name()


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
def write_json(key, value):
    path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/setting.json'
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
def get_zero_time(day_time='2021-05-17'):
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
    email_info = get_json()['email']
    account = email_info['email']
    security_code = email_info['security_code']
    host = email_info['host']
    port = email_info['port']
    client = imaplib.IMAP4_SSL(host=host, port=port)
    client.login(account, security_code)
    # 选择收件夹
    client.select('INBOX')
    type, data = client.search(None, 'ALL')
    num = str(len(str(data[0], 'utf-8').split(' ')))
    typ, data = client.fetch(num.encode(), '(RFC822)')
    if data[0] is not None:
        encoding = chardet.detect(data[0][1])
        msg = email.message_from_string(data[0][1].decode(encoding['encoding']))
        text, enc = email.header.decode_header(msg['subject'])[0]
        title = text.decode(enc) if enc else text
        return {"title": title, "body": data[0][1].decode(encoding['encoding'])}
    else:
        return {'title': 'error, data is None.'}


# 查询语言map
def get_language_map():
    r = requests.request('GET', url='https://mms.cabital.io/deploycodefile/cabital_app/{}/latest'.format(get_json()['language']), timeout=20)
    path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/multiple_languages.json'
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

