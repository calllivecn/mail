#!/usr/bin/env python3
#coding=utf-8


import email,base64

filename = 'gmail-client.eml'
filename = 'image.eml'
filename = 'a_test.eml'
filename = 'tar.eml'

with open(filename,'r') as f:
	msg=email.message_from_file(f)


#print('#'*40,'eml content',msg)


head_list=['from','to','subject','date']

def get_msg_head(msg,head):
	if head == 'date':
		return msg.get(head)
	head = msg.get(head)
	head = email.header.decode_header(head)
	h_list =''
	for data,charset in head:
		tmp=b''
		if charset == None:
			h_list+=data.decode('utf-8')
		else:
			h_list+=data.decode(charset)
	return h_list


#for h in head_list:
#	print(h,'--->',get_msg_head(msg,h))


h_from = msg.get('from')
print('h_from : ',h_from)
h_from = email.utils.parseaddr(h_from)[1]
h_to = email.utils.parseaddr(msg.get('to'))[1]
h_subject = msg.get('subject')
print('h_subject : ',h_subject)
h_subject = email.header.decode_header(h_subject)[0]
h_subject = h_subject[0].decode(h_subject[1])
h_date = email.utils.parsedate(msg.get('date'))
print('发件人:',h_from)
print('收件人:',h_to)
print('主题:',h_subject)
print('时间:',h_date)

def get_charset(msg):
	encode = msg.get_charset()
	if encode == None:
		return 'utf-8'
	else:
		return encode

for c in msg.walk():
	if not c.is_multipart():

		sub_type = c.get_content_type()

		if sub_type == 'text/plain':
			data = c.get_payload(decode=True).decode(c.get_content_charset())
			print('#'*20,'  邮件内容  ','#'*20)
			print(data)
			print('#'*20,'  邮件内容  ','#'*20)

		elif sub_type == 'text/html':
			continue
		else:
			filename = c.get_param('name')
			print('attach name :',filename)
			data = c.get_payload()#decode=True))
			print('附件数据',data)
			data = base64.decodestring(data.encode())
			with open(filename,'w+b') as f:
				f.write(data)


