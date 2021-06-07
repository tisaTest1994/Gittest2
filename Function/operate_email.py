import imaplib
import email
import chardet
from common_function import *


# 查询邮件
def get_email():
    email_info = get_json()[get_json()['email']]
    account = email_info['account']
    security_code = email_info['security_code']
    host = email_info['host']
    client = imaplib.IMAP4_SSL(host)
    client.login(account, security_code)
    type, data = client.search(None, 'ALL')
    for num in data[0].split():
        typ, data = client.fetch(num, '(RFC822)')
        print('Message %s\n%s\n' % (num, data[0][1]))
        if data and data != [None]:
            encoding = chardet.detect(data[0][1])
            msg = email.message_from_string(data[0][1].decode(encoding['encoding']))
            text, enc = email.header.decode_header(msg['subject'])[0]
            subject = text.decode(enc) if enc else text
            print(subject)





receive_host = 'imap.qq.com'
send_host = 'smtp.qq.com'
user = '314627197@qq.com'
password = 'hakgjwsuycrpbija'




