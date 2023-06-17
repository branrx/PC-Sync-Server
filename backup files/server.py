import socket
import time
import threading
import main_process
import sys
import txt_to_list as ttl

#       define variables
global users
global status
global serverStatus

users = dict()
status = list()
status.append(0)
status.append(0)
serverStatus='on'

class Server():
    def __init__(self) -> None:
          self.Active = 0
          self.musicPath = 'src dir'
          
    
    def requestHandle(self, req, name):
        if req == 'pull':
            print('request: PULL')
            #   get all files present in local
            path = 'src dir\\'
            extensions = {'.mp3', '.m4a'}
            main_process.getFiles(filename='current register dst.txt', path=path, extensions=extensions)

            #   send the txt response
            self.pullResponse(name)

    #   response to get current register from server
    def pullResponse(self, name):
        #   read destination register file
        register = open('register dst.txt', 'rb')

        file = register
        #   get file as bytes
        bytesToSend = register.read()

        #   get file size and send it before contents
        fileSize = len(bytesToSend)
        fileSize_inBytes = int.to_bytes(fileSize, 10, 'big')
        users[name].send(fileSize_inBytes)
        print(f'file size: {fileSize}')

        #   send destination register contents
        #users[name].send(bytesToSend)

        for byte in file:
             #   send destination register contents
            users[name].send(byte)

        #   tell client end of file reached
        users[name].send('eof'.encode())

        print('finished sending response')
        
    #   handles synce request from client
    def syncRequest(self, name):
        #   create the missing files file 
        f = open('current missing files.txt', 'wb')

        #   receive the size of the file being sent by client
        docSize = users[name].recv(10)
        docSize = int.from_bytes(docSize, 'big')
        print(f'file size: {docSize}')
        count = 0

        #   receive contents of missing files file
        while True:
            #   sock receive missing files file contents
            buff = users[name].recv(docSize)
            
            #   keep track of how many bytes have been read
            if count == 0:
                term = buff
                count = 1
            else:
                term+=buff
            print(len(term))

            if buff.decode() == 'eof':
                break

            f.write(buff)
        
        print('[INFO] Received missing files file.')
        f.close()

        self.syncResponse(name)

    #   send files that are missing - sync
    def syncResponse(self, name):
        #   load missing files file as list
        f = open('current missing files.txt', 'r')
        missingFiles = ttl.to_list_single(f)

        #   store sync variables
        filesCount = len(missingFiles)

        #   send number of files to be sent
        countInBytes = int.to_bytes(filesCount, 10, 'big')
        users[name].send(countInBytes)


        #   send files
        self.sendFiles(name, missingFiles)

    #   sends files one by one
    def sendFiles(self, name, missingFiles):
        for file in missingFiles:
            #   send the index of the file being sent
            fileName = file.split('**')
            fileIndex = fileName[0]
            print(f'file index: {fileIndex}')
            users[name].send(fileIndex.encode())

            time.sleep(1)

            #   send the size of the file
            #   ex. 2**src dir\\Holy Ten - Pfumo(MP3_320K).mp3
            newName = file.replace(f'{fileIndex}**', '')

            audioFile = open(newName, 'rb')
            audioFileB = open(newName, 'rb')
            fileSizeB =  audioFileB.read()
            fileSizeB = len(fileSizeB)
            fileSizeB = int.to_bytes(fileSizeB, 10, 'big')
            users[name].send(fileSizeB)
            for byte in audioFile:
                users[name].send(byte)
            time.sleep(5)
            users[name].send('eof'.encode())
        users[name].send('eos'.encode())

    #     receives messages from server
    def receive(self, name, s):
        global users
        global status
        global serverStatus

        #   informs system that we can receive
        status[0]=1

        print('[INFO] - Server ready to receive.') 

        while True:
            #   receive method
            buff = users[name].recv(1024)
            if len(buff)>0 and len(buff)<6:
                req = buff.decode()
                self.requestHandle(req, name)
            

        #   wait listen for transmission from client  
        #msg = users[name].recv(1024)

        f = open('sample.mp3', 'wb')
        buff = users[name].recv(1024)
        while True:

            print('writing')
            f.write(buff)
            buff = users[name].recv(1024)
            if len(buff) == 0:
                break

        f.close()



        #   close the socket
        s.close()
        return

    #     sends messages to client
    def sending(self, name, s):
        global status
        global serverStatus

        #   informs system that we can send
        status[1]=1

        #   initiate message string variable
        msg = 'ini'
        print('[INFO] - Server ready to send.')  

        #   keep listening for new message input until 
        #   server wants to terminate transmission
        while msg!='bye':
                #   enter message
                msg = input()

                #   encode the message then send to client
                #   with specified name
                users[name].send(msg.encode())

        #   informs system that we can no longer send
        status[1]==0

        #   informs system that we are about to turn off 
        #   the server
        serverStatus='off'

        print('[INFO] - Connection ended: can no longer send.')
        s.close()
        return

    #	ESTABLISH CONNECTION WITH CLIENT
    def connection(self):
        global users
        global status
        #	create socket instance
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #       set ip local ip address for server, and port
        host = '192.168.0.105'
        port = 24300

        #	bind the ip and port to the socket instance
        try:
                s.bind((host, port))
        except Exception as e:
                print(e)
                print('[INFO]- Failed to bind socket')

        #	listen for client connection
        try:
                s.listen(2)
                print('[INFO]- Socket listening...')
        except Exception as e:
                print(e)
                print('[INFO]- Socket not listening.')

        while True:
                #   if connection request received, accept
                #   and store client object and ip
                client, address = s.accept()

                print(f'[INFO] - Connected to: ip - {address[0]} port - {address[1]}')

                #   tell user to send desired username
                client.send('enter username: '.encode())

                #   wait to receive user desired username
                username = client.recv(1024).decode()
                print(f'[INFO] - Client username: {username}')

                #   save client object along with username as
                #   a pair in a dictionary
                users[username]=client

                #   send acknowledgement that user accepted to 
                #   client
                users[username].send('okay!'.encode())

                #   initiate a thread for receiving messages 
                #   from client
                #threading.Thread(target=self.receive, args=[username, s]).start()
                threading.Thread(target=self.syncRequest, args=[username]).start()
                self.Active = 1

                #   if server is off, stop the receive thread
                #   from initiating another send thread upon completion
                if serverStatus=='off':
                    break

                #   initiate a thread for sending messages 
                #   to client  
                threading.Thread(target=self.sending, args=[username, s]).start()

                #   if server is off for send or receive thread
                #   close the sockets to stop unexpected errors
                if status[0]==0 or status[1]==0:
                        s.close()
                        print('[INFO] - Socket closed!')

                break


serverObject = Server()
serverObject.connection()







