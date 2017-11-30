#!/usr/bin/env python3
#coding=utf-8

from imap4ssl import MailCommand
import email

em = MailCommand('linzxmail@qq.com','nonooklovkshbeej',debug=True)

t = em.check_new()

print('check new mail',t)


if t:
	from_name ,from_ , subject = em.getFromSubject(0)

	print('from_name',from_name,'\n','from : ',from_,'\n','subject : ',subject,'\n',sep='')

	#text = em.getTextContent(0)
	#print('这里是文本内容 --> ',text.decode())
	#exit(1)
	msg  = em.getContent(0)
	#print('msg type(msg)',type(msg))
	for part in msg.walk():
		print('执行msg.walk()')
		if not part.is_multipart():
			if part.get_content_type() == 'application/octet-stream':
				attach = part.get_payload(decode=True)
				#print('part.get_payload() --> ',attach)	
				attach = attach.decode(part.get_content_charset())
				print('attach filename',part.get_filename())
			else:
				print('get_content_type',part.get_content_type())
				other = part.get_payload(decode=True)
				other = other.decode(part.get_content_charset())
				print('other --> ',other)
		else:
			ty = part
			print(ty)
	em.close()


