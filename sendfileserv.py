import sys
import socket
import commands

# The port on which to listen
listenPort = int(sys.argv[1])

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

# Start listening on the socket
welcomeSock.listen(1)

#used to receive the data by providing the number of bytes to receive
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff
		

print ("Waiting for connections...")
		
# Accept connections
clientSock, addr = welcomeSock.accept()
	
print ("Accepted connection from client: ", addr)
print ("\n")

# Accept connections forever
while True:

	#receive the data 
	data = clientSock.recv(1024).decode()

	if(data [0:3] == 'put'):
		# The buffer to all data received from the
		# the client.
		fileData = ""
		
		# The temporary buffer to store the received
		# data.
		recvBuff = ""
		
		# The size of the incoming file
		fileSize = 0	
		
		# The buffer containing the file size
		fileSizeBuff = ""
		
		# first 10 bytes indicate the file's size so we get that 
		fileSizeBuff = recvAll(clientSock, 10)
			
		# convert the file size to an integer
		fileSize = int(fileSizeBuff)
		
		print ("The file size is ", fileSize)
		
		# Get the file data
		fileData = recvAll(clientSock, fileSize)
		
		print ("The file data is: ")
		print (fileData)
		print("SUCCESS")

	#command was to get the files on the server
	elif(data[0:2] == 'ls'):
		#run the command 'ls' on the server and print the results on the server
		for line in commands.getstatusoutput('ls'):
			print(line)
		#get the size of this output
		dataSize = str(len(str(line)))
		#make that output's size to 10 bytes
		while len(dataSize) < 10:
			dataSize = "0" + dataSize

		#send it back to the client with the file size
		clientSock.send(dataSize + str(line))

		print "SUCCESS"

	#command from the client was get
	elif(data[0:3] == 'get'):

		# The name of the file
		fileName = data[4:]

		try:
			# Open the file
			fileObj = open(fileName, "r")
		except:
			print("FAILED")
			print("FILE DOESN'T EXIST!")
			break

		# The number of bytes sent
		numSent = 0

		# The file data
		fileData = None

		# Keep sending until all is sent
		while True:
			
			#Read the data
			fileData = fileObj.read(65536)
			
			# Make sure we did not hit EOF
			if fileData:
				# Get the size of the data read
				# and convert it to string
				dataSizeStr = str(len(fileData))
				
				# Prepend 0's to the size string
				# until the size is 10 bytes
				while len(dataSizeStr) < 10:
					dataSizeStr = "0" + dataSizeStr
			
				# Prepend the size of the data to the
				# file data.
				fileData = dataSizeStr + fileData	
				
				# The number of bytes sent
				numSent = 0
				# Send the data!
				while len(fileData) > numSent:
					numSent += clientSock.send(fileData[numSent:].encode())
			
			else:
				break
				fileObj.close()
				#EOF so we're done

		print ("Sent ", numSent, " bytes.")
		print ("SUCCESS")

	#all other commands close the server
	else:
		break

#close the socket with the client
clientSock.close()