import socket
import os
import sys

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
		
# Command line checks 
if len(sys.argv) < 2:
	print ("USAGE python " + sys.argv[0] + " <FILE NAME>" )

# Server address
serverAddr = sys.argv[1]

# Server port
serverPort = int(sys.argv[2])

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

#keep running
while True:

	#get the input from the user
	input = raw_input("ftp> ")

	#check if the command is put
	if(input[0:3] == 'put'):
		# The name of the file
		fileName = input[4:]
		try:
			# Open the file
			fileObj = open(fileName, "r")
		except: #file doesn't exist
			print "File doesn't exist!"
			break
		# The number of bytes sent
		numSent = 0

		# The file data
		fileData = None

		#send the command so the server knows which command
		connSock.send('put')

		# Keep sending until all is sent
		while True:
			
			# Read the data
			fileData = fileObj.read(65536)
			
			# Make sure we did not hit EOF
			if fileData:
				
				#get the size of the data
				dataSizeStr = str(len(fileData))
				
				#makes sure the dataSize is 10
				while len(dataSizeStr) < 10:
					dataSizeStr = "0" + dataSizeStr
			
			
				#add the data size before the rest of the command
				fileData = dataSizeStr + fileData	
				
				# The number of bytes sent
				numSent = 0
				
				# Send the data!
				while len(fileData) > numSent:
					numSent += connSock.send(fileData[numSent:])
			
			else:
				break
				#close the file because we're done
				fileObj.close()

		print ("Sent ", numSent, " bytes.")

	#command was to get	
	elif(input[0:3] == 'get'):
		#send the entire input because we need to get data from the server
		connSock.send(input)

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
		
		# get the size of the buffer indicated by the first 10 bytes
		fileSizeBuff = recvAll(connSock, 10)
			
		# Get the file size as an integer
		fileSize = int(fileSizeBuff)
		
		print ("The file size is ", fileSize)
		
		# Get the file data using the first 10 bytes 
		fileData = recvAll(connSock, fileSize)
		
		print ("The file data is: ")
		print (fileData)

	#send the ls command to the server
	elif(input[0:2] == 'ls'):
		connSock.send('ls'.encode())

		#get the first 10 which is the size of the ls command's return
		mySize = recvAll(connSock, 10)
		#print the command's output
		print recvAll(connSock, int(mySize))
	#exit the program
	elif(input[0:4] == 'exit'):
		break
	
#close the socket because we're done
connSock.close()