from socket import *
import sys
import time

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
# filename = sys.argv[3]

# tnow= time.gmtime()
# tnowstr= time.strftime('%a, %d %b %Y %H:%M:%S  %Z\r\n', tnow)
# print(tnowstr)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
response = clientSocket.recv(8192)
print ('From Server:\n' + response.decode())
while 1:
	if not response:
		print("Server error")
		break;
	objective=""
	request=""	

	clientInput=input("type..")
	print(clientInput)
	seperation=clientInput.split(" ")
	command=seperation[0]
	request+=command
	partOfRequest=1
	lengthOfRequest=len(seperation)
	print("length of request:")
	print(lengthOfRequest)

	if(lengthOfRequest>1 and lengthOfRequest<3):
		objective+=seperation[partOfRequest]
		request+=" "
		request+=objective
		
	elif(lengthOfRequest>2):
		while(partOfRequest<lengthOfRequest):
			objective+=" "	
			objective+=seperation[partOfRequest]
			partOfRequest=partOfRequest+1

		request+=objective
	print("Request")
	print(request)

	if(command == "dwnld" and objective!=""):
		clientSocket.send(request.encode())
		# print("came to download")
		data=clientSocket.recv(1024)
		# print(data)
		folder='denied'
		f=folder.encode('ascii')
		if(data==f):
			print("file does not exist or cant download folder. Please check file/folder name\n")
			continue

		openfile=open(objective,'wb')
		
		done="Done"
		d=done.encode('ascii')

		while True:
			# print(data)
			eofFind=data
			eof=eofFind[(len(data)-4):]

			if(eof == d):
				data=data[:-4]
				openfile.write(data)
				break
			# if not data:
			# 	print("download")
			# 	break
			openfile.write(data)
			data=clientSocket.recv(1024)
		openfile.close()
		print("download complete\n")
		continue
		# clientInput=input("type..")
		# clientSocket.send(request.encode())
	else:
		clientSocket.send(request.encode())

	response = clientSocket.recv(1024)
	print ('From Server:\n' + response.decode())

	
clientSocket.close()