from datetime import *
import logger
from faker import Faker
import random
import json
import os
import pytz
import time


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
    email_type = ["@qq.com", "@163.com", "@126.com", "@189.com", "@cabital.com", "@gmail.com"]
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
    email = __randomNumber + random_email
    return email


# 获得资源里面的配置参数
def get_json():
    path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/setting.json'
    with open(path, "rb+") as f:
        js = json.load(f)
    return js


# 获得本日UTC时间的0点
def get_zero_utc_time():
    utc = pytz.timezone('UTC')
    utc_zero = datetime.datetime.now(tz=utc).strftime("%Y-%m-%d") + ' 0:00:00'
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
