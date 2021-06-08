import imaplib
import email
import chardet
from Function.common_function import *


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
    encoding = chardet.detect(data[0][1])
    msg = email.message_from_string(data[0][1].decode(encoding['encoding']))
    text, enc = email.header.decode_header(msg['subject'])[0]
    title = text.decode(enc) if enc else text
    return {"title": title, "body": data[0][1].decode(encoding['encoding'])}