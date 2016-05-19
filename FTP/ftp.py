#EID:ta8779

import socket
import sys
import os
import time
import random
import datetime
import re

#making a time.struct_time from	a given time string
# def formatTime(timeString):
# 	date=None
# 	try:
# 		date=time.strptime(timeString,'%a, %d %b %Y %H:%M:%S %Z')
# 	except ValueError:
# 		try:
# 			date=time.strptime(timeString)
# 		except ValueError:
# 			try:
# 				date=time.strptime(timeString,'%A, %d-%b-%y %H:%M:%S %Z')
# 			except ValueError:
# 				try:
# 					date=time.strptime(timeString,'%a %b %d %H:%M:%S %Y')
# 				except ValueError:
# 					return 1
# 	return date


host='192.168.1.71'
serverPort=int(sys.argv[1])
serverName='FTP'

serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
	serverSocket.bind((host,serverPort))
except socket.error as e:
	print(str(e))
print ('The server is runnning in port:' , serverPort)
serverSocket.listen(5)

# timeNow= time.gmtime()
# timeNowStr= time.strftime('%a, %d %b %Y %H:%M:%S  %Z', timeNow)

# messageToAdd='Date: '+timeNowStr+'\r\n'
# messageToAdd+='Server: '+serverName+'\r\n'
# messageToAdd+='\r\n'


#loop to accept the connection from any client and keep it open
while 1:
	connection, addr=serverSocket.accept()
	print ('Connected to:'+addr[0]+': ' + str(addr[1]))
	pswd='12345'
	password_request="Enter password: "
	connection.sendall(password_request.encode())
	request = connection.recv(1024)
	clientRequest=request.decode()
	try_count=3
	auth=0
	count=0
	print(clientRequest)

	if(clientRequest==pswd):
		authentication='authenticated\n'
		connection.sendall(authentication.encode())
		request = connection.recv(1024)
		
		while request:
			# if not request:
			# 	break;
			clientRequest=request.decode("utf-8")
			print(clientRequest)
			requestSplit=clientRequest.split(" ")
			command=requestSplit[0]
			objective=""
			partOfRequest=1
			lengthOfRequest=len(requestSplit)
			# print("length of request:")
			# print(lengthOfRequest)
			if(lengthOfRequest>1 and lengthOfRequest<3):
				objective+=requestSplit[partOfRequest]
			elif(lengthOfRequest>2):
				partOfRequest=2
				objective+=requestSplit[1]
				while(partOfRequest<lengthOfRequest):
					objective+=" "	
					objective+=requestSplit[partOfRequest]
					
					partOfRequest=partOfRequest+1

			# print("Objective:")
			# print(objective)
			print(clientRequest)
			if(command == 'cwd'):
				respond=os.getcwd()
				respond+='\n'
				connection.sendall(respond.encode())
			elif(command == 'dwnld' and objective != None):
				# print("came to dwonload")
				fileOrFolder=os.getcwd()
				fileOrFolder+="/"
				fileOrFolder+=objective
				# print(fileOrFolder)
				if (os.path.isdir(fileOrFolder)):
					respond="denied"
				elif (os.path.isfile(fileOrFolder)):
					fileSize=os.stat(fileOrFolder).st_size
					openFile=open(objective,'rb')
					readFile=openFile.read(1024)
					
					while (readFile):
						connection.send(readFile)
						readFile=openFile.read(1024)
					openFile.close()
					# connection.shutdown(socket.SHUT_WR)
					respond="Done"
					print("Done sending")
				else:
					respond="denied"
				connection.sendall(respond.encode())
			elif(command == 'ls'):
				directory=os.listdir(os.getcwd())
				respond=""
				# for file in directory:
				# 	respond=file
				# 	respond+='\n'
				files = [f for f in os.listdir('.')]
				for f in files:
					 if (os.path.isfile(f) or os.path.isdir(f)):
					 	respond+=f
					 	respond+='\n'
				respond+='\n'
				connection.sendall(respond.encode())
				
			elif(command == 'cd'):
				pathToGo=""
				if(objective == ""):
					respond="Please choose a path"
				elif(objective == ".."):
					curPath=os.getcwd()
					temp=curPath.split("/")
					length=len(temp)
					count=0
					pathToGo="/"
					while(count<length-1):
						pathToGo+=temp[count]
						pathToGo+="/"
						count=count+1
					os.chdir(pathToGo)
					respond="Path changed to "
					respond+=os.getcwd()
					respond+='\n'
				else:
					pathToGo+=objective
					try:
						os.chdir(pathToGo)
						respond="Path changed to "
						respond+=os.getcwd()
						respond+='\n'
						
					except OSError as e:
						respond=objective
						respond+="Path syntax error"
				connection.sendall(respond.encode())
					# os.chdir(pathToGo)
					# respond="Path changed to "
					# respond+=os.getcwd()
					# respond+='\n'
				
			else:
				respond=command
				respond+="<-- command does not exist."
				respond+='\n'
				connection.sendall(respond.encode())
			
			clientRequest=None
			
			request = connection.recv(1024)
			# print("this is after: ")
			# print(request)
		
	else:
		while(count != 3):
			if(count==2):
				error_msg="connection refused"
				connection.sendall(error_msg.encode())
				break
			error_msg="Wrong password\n"
			connection.sendall(error_msg.encode())
			connection.sendall(password_request.encode())
			request = connection.recv(1024)
			clientRequest=request.decode()
			if(clientRequest==pswd): 
				auth=1
				authentication='authenticated\n'
				connection.sendall(authentication.encode())
				request = connection.recv(1024)

				while request:
					# if not request:
					# 	break;
					clientRequest=request.decode()
					print(clientRequest)
					if(clientRequest == 'cwd'):
						respond=os.getcwd()
						respond+='\n'
						connection.sendall(respond.encode())
					elif(clientRequest == 'ls'):
						directory=os.listdir(os.getcwd())
						for file in directory:
							respond=file
							respond+='\n'
						respond+='\n'
						connection.sendall(respond.encode())
					elif(clientRequest == 'cd'):
						lol=0
					else:
						respond=clientRequest
						respond+="<-- command does not exist."
						respond+='\n'
						connection.sendall(respond.encode())
					clientRequest=None
					request = connection.recv(1024)

			if(auth == 1):
				break;
			count=count+1
		# break;
		
	auth=0