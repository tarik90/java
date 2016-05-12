#EID:ta8779

import socket
import sys
import os
import ipaddress



host=''
serverPort=int(sys.argv[1])

serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

routingTable=[]
routingTable.append("A 0.0.0.0/0 100")


try:
	serverSocket.bind((host,serverPort))
except socket.error as e:
	print(str(e))
print ('The server is runnning in port:' , serverPort)
serverSocket.listen(1)


#loop to accept the connection from any client and keep it open
while 1:
	connection, addr=serverSocket.accept()

	request = connection.recv(1024)
	clientRequest=request.decode()
	print (clientRequest)
	response = clientRequest

	#split the client request by \r\n to get individual part	
	eachLines = clientRequest.split('\r\n')
	lines=len(eachLines)

	#check to see if first line is UPDATE
	if (eachLines[0]=='UPDATE'):
		# print ('ACK')
		counter=1
		while (counter < (lines-2)):
			eachUpdate=eachLines[counter].split(" ")
			router=eachUpdate[0] #A
			eachIPmask=eachUpdate[1] #111.1.1.1/1
			pathCost=eachUpdate[2] #100
			routingTableLen=len(routingTable)
			rCounter=0
			
			# loop to compare given CDIR with existing CIDR in the routing table
			while(rCounter<routingTableLen):
			    routes=routingTable[rCounter].split(" ")
			    #routes[0] Routing table ---A
			    #routes[1] Routing table ---111.11.11.1/1
			    #routes[2] Routing table ---- Cost 100

			    ip1=ipaddress.ip_network(routes[1])
			    ip2=ipaddress.ip_network(eachIPmask)

			    if(ip1.overlaps(ip2)):
			    	ip1_prefix=(ip1.prefixlen)
			    	ip2_prefix=(ip2.prefixlen)

			    #take action based on ip prefix & cost of the path
			    	if(ip1_prefix>ip2_prefix):
			    		if(int(routes[2])<=int(pathCost)):
			    			routingTable.append(eachLines[counter])
			    			routingTableLen=len(routingTable)
			    		else:
			    			routingTable[rCounter]=eachLines[counter]
			    	elif(ip1_prefix<ip2_prefix):

			    		if(int(routes[2])>=int(pathCost)):
			    			routingTable.append(eachLines[counter])
			    			routingTableLen=len(routingTable)
			    		else:
			    			#loop to remove all existing path that has higher cost and then break based on ip prefix
			    			while True:
			    				try:
			    					routingTable.remove(eachLines[counter])
			    				except ValueError:
			    					break;
			    			routingTableLen=len(routingTable)
			    			break;
			    	elif(ip1_prefix==ip2_prefix):
			    		if(int(routes[2])>int(pathCost)):
			    			routingTable[rCounter]=eachLines[counter]
			    else:
			    	routingTable.append(eachLines[counter])
			    	routingTableLen=len(routingTable)
			    
			    rCounter+=1

			routingTable=list(set(routingTable))
			counter+=1 

		ack='ACK\r\n'
		ack+='END\r\n'
		
		connection.sendall(ack.encode())
			
		#print the whole routing table
		# print ("Routing table entries:")
		# routingTableLen=len(routingTable)
		# for i in range(0,routingTableLen):
		# 	print (routingTable[i])

	#check to see if first line is QUERY
	if (eachLines[0]=='QUERY'):
		counter=0
		index=0
		routerTableLength=len(routingTable)
		minCost=9999999999999
		longestPrefix=-1
		closestRoutingIPs=[]

		#loop to check the best path based on ip prefix and path cost
		while(counter<routerTableLength):
			eachPartOfRoute=routingTable[counter].split(" ")
			ipAddress=eachLines[1]
			IPmask=eachPartOfRoute[1]
			cost=int(eachPartOfRoute[2])

			ip=ipaddress.ip_network(IPmask)
			ip_prefix=(ip.prefixlen)
			
			#check to see if requested query is in any of the routing table CIDRs
			if ipaddress.ip_address(ipAddress) in ipaddress.ip_network(IPmask):
				if (cost<=minCost):
					if(ip_prefix>longestPrefix):
						minCost=cost
						longestPrefix=ip_prefix
						# print("min:******")
						# print(minCost)
						index=counter
			counter+=1

		#best path
		resultPath=routingTable[index].split(" ")
		result="RESULT\r\n"
		result+=eachLines[1]+" "+resultPath[0]+" "+resultPath[2]+'\r\n'
		result+='END\r\n'

		connection.sendall(result.encode())
	
	