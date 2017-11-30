#!/usr/bin/env python3
#coding=utf-8


import imaplib

import email 

HOST='imap.qq.com'

User='linzxmail@qq.com'
Password='nonooklovkshbeej'

conn=imaplib.IMAP4_SSL(host=HOST)


conn.login(User,Password)

conn.select()

typex ,data = conn.search(None,'ALL')

newlist = data[0].split()

typex ,data = conn.fetch(newlist[0],'(RFC822)')

msg = email.message_from_string(data[0][1].decode())

#print(msg)

subject = msg.get('subject')

subject = email.header.decode_header(subject)[0][0]

print('Subject :',subject.decode())

for part in msg.walk():
        # 如果ture的话内容是没用的
        if not part.is_multipart():            
            print(part.get_payload(decode=True).decode())

