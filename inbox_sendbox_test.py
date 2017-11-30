#!/usr/bin/env python3
#coding=utf-8


import imaplib

import re

import email 

HOST='imap.qq.com'

User='linzxmail@qq.com'
Password='nonooklovkshbeej'
try:
	conn=imaplib.IMAP4_SSL(host=HOST)
	
	
	conn.login(User,Password)
	conn.print_log()
	conn.select()
	
	'''
	typ ,data = conn.status('INBOX','(UNSEEN)')
	print('typ  data',typ,data)
	unseen = int(re.findall('INBOX \(UNSEEN ([0-9]+)\)',data[0].decode())[0])
	print('未读邮件数 --->',unseen)
	
	if unseen ==0:
		print('没有新邮件')
		conn.logout()
		exit(1)
	'''
	#typ ,data = conn.namespace()
	#print('IMAP server namespace',typ ,data)
	
	typ,[msg_id] = conn.search(None,'(SUBJECT "MailCommand")',)# ALL : 全部, Seen : 已读 unseen : 未读 , Recent : 最近的 , Answered : 回复 , Flagged  
											#python 中没用   Deleted : 已删除邮件 , Draft : 草稿
	
	print('conn.search() -->',typ , msg_id)
	
	data = msg_id.split()
	if len(data) == 0:
		raise imaplib.IMAP4_SSL.error('没有未读邮件')
	newlist =data
	newlist.reverse() 
	
	typ ,data = conn.fetch(newlist[0],'(BODY[TEXT])')#'BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)]')#'(BODY[HEADER.FIELDS (FROM SUBJECT)])')
	#typ ,data = conn.fetch(newlist[0],'(RFC822)')#'(RFC822.SIZE BODY[HEADER.FIELDS (SUBJECT)])')
	
	#typ ,data = conn.status('INBOX','(FROM)')
	#print('fetch BODY.PEEK[FROM SUBEJCT] --> ',data)

	data = data[0][1]
	em = email.message_from_bytes(data)
	for part in em.walk():
		if not part.is_multipart():
			print('part :',part)
	
	raise imaplib.IMAP4_SSL.error('...')

	import pickle
	with open('data.dump','wb') as f:
		pickle.dump(data,f)
	

	raise imaplib.IMAP4_SSL.error('...')

	print(email.utils.parseaddr(data[0]))
	#print(email.header.decode_header())

	#conn.store(newlist[0],'+FLAGS','\\SEEN')
	print('fetch() typ ---- data',typ , data)
	raise imaplib.IMAP4_SSL.error('测试') 
	'''
	print('typ',typ)#,'data isinstance',data)
	for content in data:
		if isinstance(content,bytes):
			print(content.decode())
		else:
			print(content)
	
	exit(1)
	'''
	
	msg = email.message_from_bytes(data[0][1])
	
	
	for part in msg.walk():
			# 如果ture的话内容是没用的
		if not part.is_multipart():            
			if part.get_content_type() == 'text/plain':
				print(part.get_payload(decode=True).decode(part.get_content_charset()))
except imaplib.IMAP4.error as e:
	print(e)
finally:
	conn.close()
	conn.logout()
