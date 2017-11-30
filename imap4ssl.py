#!/usr/bin/env python3
#coding=utf-8

import email,time,re,base64,imaplib
from email import header


class MailCommand:
	'''基于QQ邮件shell，C/S模式'''
	HOST='imap.qq.com'
	def __init__(self,QQmail,password,debug=False):
		self.mail = QQmail
		self.conn = imaplib.IMAP4_SSL(self.HOST)
		self.conn.login(QQmail,password)
		if debug:
			self.conn.print_log()
		self.conn.select()			
		password=''

	def check_new(self):
		self.typ , self.data = self.conn.search(None,'UNSEEN')
		self.list = self.data[0].split()
		if len(self.list) == 0:
			return False
		self.list.reverse()
		return True

	def getFromSubject(self,count):
		'''-->(from_name ,from_ ,subject)'''
		#typ , data = self.conn.fetch(self.list[count],'BODY[HEADER.FIELDS (FROM SUBJECT)]')
		typ , data = self.conn.fetch(self.list[count],'BODY.PEEK[HEADER]')
		#print(data[0])
		
		em_msg = email.message_from_bytes(data[0][1])
		#print('get(subject)',em_msg.get('subject'))
		
		subject = header.decode_header(em_msg.get('subject'))
		subject = subject[0] # 从列表拿出来
		if subject[1] :
			subject = subject[0].decode(subject[1])
		else:
			if isinstance(subject[0],str):
				subject = subject[0]
			else:
				subject = subject[0].decode()
		#print('subject --> ',subject)

		from_ = em_msg.get('from')
		from_ = from_.replace('"','')
		#print("from_",from_) # QQ邮箱 from : "..." <qq@qq.com> 多了\"字符 要去掉
		from_ = header.decode_header(from_)
		#print('from_ --> ',from_)
		
		from_name = from_[0]
		if from_name[1] :
			from_name = from_name[0].decode(from_name[1])
		else:
			from_name = from_name[0]
		
		
		from_ = from_[1]
		if from_[1] :
			from_ = from_[0].decode(from_[1])
			from_ = re.findall(r'<(.*)>',from_)[0]
		else:
			from_ = from_[0].decode()
			from_ = re.findall(r'<(.*)>',from_)[0]

		#print('from_name',from_name)
		#print('from_',from_)
		'''
		print(data)
		data = data[0][1] #拿出FROM SUBJECT
		print(data)
		data = data.splitlines()
		data = data[0].decode(),data[1].decode()
		print('data --> ',data)
		from_ = re.findall(r'<(.*)>',data[0])[0]
		subject = re.findall(r'(.*)=\?(.*)\?B\?(.*)\?=',data[1])[0]
		subject = base64.decodebytes(subject[2].encode()).decode(subject[1])
		'''
		return from_name ,from_ ,subject

	def getTextContent(self,count):
		typ ,data = self.conn.fetch(self.list[count],'BODY.PEEK[TEXT]')
		data = data[0][1]
		text = data #base64.decodebytes(data).decode()
		return text
	
	def getContent(self,count):
		typ ,data = self.conn.fetch(self.list[count],'(RFC822)')
		msg = email.message_from_bytes(data[0][1])
		'''
		for part in msg.walk():
			if not part.multipart():
				d = part.get_payload(decode=True)
				yield d.decode(part.get_content_charset())
		'''
		return msg
		#print('recode',typ)
		#print('data',data)
		#exit(1)

	def seen(self,count):
		self.conn.store(self[count],'\SEEN')


	def close(self):
		self.conn.close()
		self.conn.logout()

