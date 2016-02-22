#EID:ta8779

import socket
import sys
import os
import time
import random
import datetime


#making a time.struct_time from	a given time string
def formatTime(timeString):
	date=None
	try:
		date=time.strptime(timeString,'%a, %d %b %Y %H:%M:%S %Z')
	except ValueError:
		try:
			date=time.strptime(timeString)
		except ValueError:
			try:
				date=time.strptime(timeString,'%A, %d-%b-%y %H:%M:%S %Z')
			except ValueError:
				try:
					date=time.strptime(timeString,'%a %b %d %H:%M:%S %Y')
				except ValueError:
					return 1
	return date


host=''
serverPort=int(sys.argv[1])
serverName='NotSoAwesome 9.9'

serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
	serverSocket.bind((host,serverPort))
except socket.error as e:
	print(str(e))
print ('The server is runnning in port:' , serverPort)
serverSocket.listen(1)

timeNow= time.gmtime()
timeNowStr= time.strftime('%a, %d %b %Y %H:%M:%S  %Z', timeNow)

messageToAdd='Date: '+timeNowStr+'\r\n'
messageToAdd+='Server: '+serverName+'\r\n'
messageToAdd+='\r\n'


#loop to accept the connection from any client and keep it open
while 1:
	connection, addr=serverSocket.accept()
	print ('Connected to:'+addr[0]+': ' + str(addr[1]))
	request = connection.recv(1024)
	clientRequest=request.decode()
	print (clientRequest)
	eachLines = clientRequest.split('\r\n')
	lines=len(eachLines)

	#check for 'If-Modified-Since' in the header and gets the line number it is in if exist
	counter=0
	lastModSince=None
	for x in eachLines:
		if 'If-Modified-Since' in x:
			lastModSince=formatTime(eachLines[counter][19:])
			break;
		counter=counter+1

	#split the first line of header to sperate GET,filename and HTTP version if exist
	eachPart=eachLines[0].split(' ')
	parts=len(eachPart)
	ifGET=eachLines[0][0:3]

	#if correct request header 
	if (parts ==3):
		#check if header is GET
		ifGET=eachLines[0][0:3]
		if (ifGET=='GET'):
			#check if HTTP is 1.1
			if eachPart[parts-1]=='HTTP/1.1':
				#check for the spported format of file
					if any(s in eachPart[1] for s in ('.txt','.html','.htm','.jpeg','jpg')):
						if ".txt" in eachPart[1]: 
							fileType='text/plain'
						elif ".html" in eachPart[1]: 
							fileType='text/html'
						elif ".htm" in eachPart[1]: 
							fileType='text/html'
						elif ".jpg" in eachPart[1]: 
							fileType='image/jpeg'
						elif ".jpeg" in eachPart[1]: 
							fileType='image/jpeg'

						#check existence of file
						if os.path.isfile(eachPart[1][1:]):
							dateOfModification=time.ctime(os.path.getmtime(eachPart[1][1:]))
							formatDate=datetime.datetime.strptime(dateOfModification, '%a %b %d %H:%M:%S %Y').strftime('%a, %d %b %Y %H:%M:%S')
							filestat = formatTime(time.ctime(os.path.getmtime(eachPart[1][1:])))

							#check for last-modified-since.if not exist lastModSince=None
							if(lastModSince==None):
								fileName=eachPart[1][1:]
								fileSize=os.stat(fileName).st_size
								response='\nHTTP/1.1 200 OK\r\n'
								response+='Date: '+timeNowStr+'\r\n'
								response+='Server: '+serverName+'\r\n'
								response+='Last-Modified: '+formatDate+'  GMT\r\n'
								response+='Content-Length: '+str(fileSize)+'\r\n'
								response+='Content-Type: '+fileType+'\r\n'
								response+='\r\n'
								connection.sendall(response.encode())
								openFile=open(fileName,'rb')
								readFile=openFile.read(1024)
								while (readFile):
									connection.sendall(readFile)
									readFile=openFile.read(1024)
								openFile.close()
							else:
								if (filestat==lastModSince) or (filestat<lastModSince):
									response='304 Not Modified'+'\r\n'
									response+='Date: '+timeNowStr+'\r\n'
									response+='Server: '+serverName+'\r\n'
									connection.sendall(response.encode())
								elif (filestat>lastModSince):
									fileName=eachPart[1][1:]
									fileSize=os.stat(fileName).st_size
									response='\nHTTP/1.1 200 OK\r\n'
									response+='Date: '+timeNowStr+'\r\n'
									response+='Server: '+serverName+'\r\n'
									response+='Last-Modified: '+formatDate+'  GMT\r\n'
									response+='Content-Length: '+str(fileSize)+'\r\n'
									response+='Content-Type: '+fileType+'\r\n'
									response+='\r\n'
									# response+='Line_based text data:'+fileType+'\r\n'
									connection.sendall(response.encode())
									# print(fileSize)
									openFile=open(fileName,'rb')
									readFile=openFile.read(1024)
									while (readFile):
										connection.sendall(readFile)
										readFile=openFile.read(1024)
									openFile.close()

						else:
							response='404 Not Found\r\n'
							response+=messageToAdd
							connection.sendall(response.encode())
					else:
						response='415 Unsupported Media Type\r\n'
						response+=messageToAdd
						connection.sendall(response.encode())
			else:
				response='505 HTTP Version Not Supported\r\n'
				response+=messageToAdd
				connection.sendall(response.encode())
		else:
			response="405 Method Not Allowed\r\n"
			response+=messageToAdd
			connection.sendall(response.encode())
	else:
		response='400 Bad Request\r\n'
		response+=messageToAdd
		connection.sendall(response.encode())
	
	connection.close()
	