# CPSC 471 Summer Project
 
Languaged Used: Python2
 
Group Members:
* Harlan Chang (espadatiburon@csu.fullerton.edu)
* Thomas-James Le (tjle@csu.fullerton.edu)
* Titus Sudarno (sudarno08@csu.fullerton.edu)
* Lily Tran (derpyhooves@csu.fullerton.edu)
* Daniel Lazo (dalazo@csu.fullerton.edu)


How to run:
PREREQUISITE: Make sure you're using Python 2, not 3 because this will not compile in Python 3
1. Run the file 'sendfileserv.py' using the command 'python sendfileserv.py <PORT NUMBER>' with your desired port number. This will start the server with the desired port.
2. Run the file 'sendfilecli.py' using the command 'python sendfilecli.py <SERVER MACHINE> <SERVER PORT>' with your desired server and port number. This will start the client and have it connect to the server. During testing, we used 'localhost' as the server. The client will then display 'ftp> '. This means that the client is waiting for a command from the user. 
3. Type in one of the available commands (get, put, ls, quit)
  3a. The 'get' command and the 'put' command require that the user puts a file name after the command. For example, 'get file.txt'
  3b. The 'ls' command will return the files in the server. It will post it on both the server and the client.
  3c. The 'quit' command will close both the client and the server
4. When done, use the 'quit' command to exit the client and server. 
