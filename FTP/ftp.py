import select
import socket
import sys
import threading
import os

class Server:
	def __init__(self):
		self.host="192.168.1.71"
		self.port = int(sys.argv[1])
		self.server=None
		self.threads=[]

	def set_connection(self):
		try:
			self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.server.bind((self.host,self.port))
			self.server.listen(5)
		except socket.error as e:
			print(str(e))

		print ('The server is runnning in port:' , self.port)

	def run(self):
		self.set_connection()
		input = [self.server]

		while 1:
			inputready, outputready,exceptready = select.select(input,[],[])

			for s in inputready:
				if (s == self.server):
					c=client(self.server.accept())
					c.start()
					self.threads.append(c)

		self.server.close()
		for c in self.threads:
			c.join()


class client(threading.Thread):

	def __init__(self,connection):
		threading.Thread.__init__(self)
		self.client, addr = connection
		print ('Connected to:'+addr[0]+': ' + str(addr[1]))

	def run(self):
		pswd='12345'
		password_request="Enter password: "
		self.client.sendall(password_request.encode())
		request = self.client.recv(1024)
		clientRequest=request.decode()
		try_count=3
		auth=0
		count=0
		print(clientRequest)

		if(clientRequest==pswd):
			authentication='authenticated\n'
			self.client.sendall(authentication.encode())
			request = self.client.recv(1024)
			
			while request:
				# if not request:
				# 	break;
				clientRequest=request.decode("utf-8")
				# print(clientRequest)
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
					self.client.sendall(respond.encode())
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
							self.client.send(readFile)
							readFile=openFile.read(1024)
						openFile.close()
						# self.client.shutdown(socket.SHUT_WR)
						respond="Done"
						print("Done sending")
					else:
						respond="denied"
					self.client.sendall(respond.encode())
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
					self.client.sendall(respond.encode())
					
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
						pathToGo+=os.getcwd()
						pathToGo+="/"
						pathToGo+=objective
						try:
							os.chdir(pathToGo)
							respond="Path changed to "
							respond+=os.getcwd()
							respond+='\n'
							
						except OSError as e:
							respond=objective
							respond+="Path syntax error"
					self.client.sendall(respond.encode())
					
				else:
					respond=command
					respond+="<-- command does not exist."
					respond+='\n'
					self.client.sendall(respond.encode())
				
				clientRequest=None
				
				request = self.client.recv(1024)
				# print("this is after: ")
				# print(request)
			
		else:
			while(count != 3):
				if(count==2):
					error_msg="connection refused"
					self.client.sendall(error_msg.encode())
					break
				error_msg="Wrong password\n"
				self.client.sendall(error_msg.encode())
				self.client.sendall(password_request.encode())
				request = self.client.recv(1024)
				clientRequest=request.decode()
				if(clientRequest==pswd): 
					auth=1
					authentication='authenticated\n'
					self.client.sendall(authentication.encode())
					request = self.client.recv(1024)

					while request:
						# if not request:
						# 	break;
						clientRequest=request.decode()
						print(clientRequest)
						if(clientRequest == 'cwd'):
							respond=os.getcwd()
							respond+='\n'
							self.client.sendall(respond.encode())
						elif(clientRequest == 'ls'):
							directory=os.listdir(os.getcwd())
							for file in directory:
								respond=file
								respond+='\n'
							respond+='\n'
							self.client.sendall(respond.encode())
						elif(clientRequest == 'cd'):
							lol=0
						else:
							respond=clientRequest
							respond+="<-- command does not exist."
							respond+='\n'
							self.client.sendall(respond.encode())
						clientRequest=None
						request = self.client.recv(1024)

				if(auth == 1):
					break;
				count=count+1
			# break;
			
		auth=0
	# elif (s == sys.stdin):
	# 	junk=sys.stdin.readline()
	# 	running = 0
	# else:
	# 	recv = self.client.recv(1024)
	# 	if(data):
	# 		self.client.send(data)
	# 	else:
	# 		s.close()
	# 		input.remove(connection)

	

def main():
    # my code here
    s=Server()
    s.run()

if __name__ == "__main__":
    main()
	