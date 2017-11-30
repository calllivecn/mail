


import re,base64,pickle

with open('data.dump','rb') as f:
	data=pickle.load(f)

print('data: ',data)
print()
#print('data[0][1]',data[0][1])
print()

data=data.splitlines()
print('data.splitlines() --> ',data)

data=data[0].decode(),data[1].decode()

from_ = re.findall(r'<(.*)>',data[0])[0]
print('from',from_)

subject = re.findall(r'=\?(.*)\?B\?(.*)\?=',data[1])[0]

print('编码和内容',subject)

subject = base64.decodebytes(subject[1].encode()).decode(subject[0])

print('subject 解码',subject)
