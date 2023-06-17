import socket
import time
import threading
import main_process
import sys
import txt_to_list as ttl
import directory_crawler as dc
import addTrailingBits

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
          self.musicPath = 'D:\\PC Sync'
          self.absPath = 'D:\\'
          self.running=0
          #self.musicPath = 'src dir'
          #self.absPath = ''
          self.serverRunning = True
          self.serverStatus = 'off'
          self.serverProgress = 'Offline'
          
    
    def requestHandle(self, req, name):
        if req == 'pull':
            print('request: PULL')
            #   get all files present in local
            path = self.musicPath + '\\'
            extensions = {'.mp3', '.m4a'}
            
            main_process.getFiles(filename='register dst.txt', path=path, extensions=extensions, absPath=self.absPath)

            #   send the txt response
            self.pullResponse(name)

    #   add attributes at end of register file
    def addAttributes(self):

        pass


    #   response to get current register from server
    def pullResponse(self, name):
        self.serverProgress = 'Preparing pull response.'
        #   read destination register file
        register = open('register dst.txt', 'rb')
        file = open('register dst.txt', 'rb')
        
        #   get file as bytes
        bytesToSend = register.read()

        self.serverProgress = 'Sending pull response.'
        print('waiting for confirmation to start')
        users[name].recv(53)

        #   get file size and send it before contents
        fileSize = len(bytesToSend)
        fileSize = addTrailingBits.addTrail(8, str(fileSize), '0')
        #fileSize_inBytes = int.to_bytes(fileSize, 10, 'big')
        users[name].send(fileSize.encode())
        print(f'file size: {fileSize}')
        
        users[name].recv(53)
        print(f'waiting to send data')
        #   send destination register contents
        #users[name].send(bytesToSend)

        for byte in file:
             #   send destination register contents
            users[name].send(byte)
        #time.sleep(3)
        #   tell client end of file reached
        #users[name].send('eof'.encode())

        self.serverProgress = 'Pull response sent.'
        print('finished sending response')
        
    #   handles synce request from client
    def syncRequest(self, name):
        #   create the missing files file 
        f = open('current missing files.txt', 'wb')

        users[name].send("okay".encode())
        self.serverProgress = 'Waiting for missing files list.'
        confirm = users[name].recv(53)
        #   receive the size of the file being sent by client
        #docSize = users[name].recv(10)
        #docSize = int.from_bytes(docSize, 'big')
        print(confirm.decode())
        
        docSize = users[name].recv(57)
        print(f'file size: {docSize}')
        count = 0
        docSize = int(docSize.decode())
        print(docSize)
        totalSize = bytearray()
        users[name].send("okay".encode())
        #   receive contents of missing files file
        while len(totalSize)!=docSize:
            #   sock receive missing files file contents
            buff = users[name].recv(docSize)
            totalSize += buff
            

        f.write(totalSize)
        totalSize = bytearray()
        self.serverProgress = 'Receieved missing files list.'
        print('[INFO] Received missing files file.')
        f.close()

        self.syncResponse(name)

    #   send files that are missing - sync
    def syncResponse(self, name):
        self.serverProgress = 'Sending sync response.'
        time.sleep(5)
        #   load missing files file as list
        f = open('current missing files.txt', 'r')
        missingFiles = ttl.to_list_single(f)
        print(missingFiles)
        #   store sync variables
        filesCount = len(missingFiles)

        #   send number of files to be sent
        #countInBytes = int.to_bytes(filesCount, 10, 'big')
        #users[name].send(countInBytes)

        #   send files
        self.sendFiles(name, missingFiles)

    def sendConfirmationThread(self):
        self.confirmThreadStop = False
        confirmThread = threading.Thread(target=self.sendConfirmation)
        confirmThread.start()
        if(self.confirmThreadStop):
             confirmThread.join()

    def sendConfirmation(self):
        counter = 0
        while not self.confirmationTicket:
            time.sleep(0.1)
            counter += 1
            if counter%5==0:
                 users[self.name].send("okay".encode())
        self.confirmThreadStop = True
        self.confirmationTicket = False
        pass
         

    #   sends files one by one
    def sendFiles(self, name, missingFiles):
        self.name = name
        self.confirmationTicket = False
        self.serverProgress = 'Sending requested files.'
        #users[name].send("okay".encode())
        fileSize = users[name].recv(53)
        print("starting sync")
        for file in missingFiles:
            #   send the index of the file being sent
            fileName = file.split('**')
            fileIndex = fileName[0]
            print(f'file index: {fileIndex}')
            index = addTrailingBits.addTrail(8, fileIndex, "0")
            users[name].sendall(index.encode())

            
            #   wait for confirmation
            confirm = ""
            while confirm!="okay": 
                msg = users[name].recv(53)
                confirm = msg.decode()

            #users[name].send("okay".encode())
            self.confirmationTicket = True
            print('confirmation after index received')
            
            #   send the size of the file
            #   ex. 2**src dir\\Holy Ten - Pfumo(MP3_320K).mp3
            newName = file.replace(f'{fileIndex}**', '')
            newName = self.absPath + newName
            self.serverProgress = f'Syncing: {newName[30]}'

            print(newName)

            audioFile = open(newName, 'rb')
            audioFileB = open(newName, 'rb')
            fileSizeB =  audioFileB.read()
            fileSizeB = len(fileSizeB)
            #fileSizeB = int.to_bytes(fileSizeB, 10, 'big')
            print(fileSizeB)
            try:
                fileSizeFinal = addTrailingBits.addTrail(8, str(fileSizeB), "0")
            except Exception as e:
                 print(e)
            print('addtrail has return')
            users[name].send(fileSizeFinal.encode())
            #hx = int.from_bytes(fileSizeB, 'big')
            print(f'file size: {str(fileSizeFinal)}')

            confirm = ""
            while confirm!="okay": 
                msg = users[name].recv(53)
                confirm = msg.decode()

            #users[name].send("okay".encode())
            self.confirmationTicket = True


            print('confirmation after size received')
            
            data = audioFile.read()
            users[name].sendall(data)
            '''for byte in audioFile:
                #print(f'sent: {len(byte)}')
                users[name].send(byte)'''
            print('next file')
            #   wait for confirmation
            confirm = ""
            while confirm!="okay": 
                msg = users[name].recv(53)
                confirm = msg.decode()

            self.confirmationTicket = True
            print('confirmation after size received')
            
            print(f'eof confirmation received')
        users[name].send('eos'.encode())
        self.serverProgress = 'Sync Complete.'
        print('Sync Complete.')
        self.running=0

    #   main function, hangs until a request is made
    def mainHub(self, name, s):
        while self.running:
            #   if request, then process accordingly
            #   listen for requests
            request = users[name].recv(53)
            request = request.decode()

            if request == 'pull':
                try:
                    self.receive(name, s)
                except Exception as e:
                    print(e)
            elif request== 'sync':
                try:
                    self.syncRequest(name)
                except:
                    pass
            elif request=='term':
                break
            request = ''

        self.serverRunning = False
        self.serverStatus = 'off'



    #     receives messages from server
    def receive(self, name, s):
        global users
        global status
        global serverStatus

        #   informs system that we can receive
        status[0]=1

        print('[INFO] - Server ready to receive.') 

        self.requestHandle('pull', name)

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
        self.serverStatus = 'ready'
        #	create socket instance
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #       set ip local ip address for server, and port
        host = '192.168.0.105'
        port = 24300

        self.serverProgress = f'Listening on: {host} : port {port}'

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
                #client.send('enter username: '.encode())

                #   wait to receive user desired username
                username = client.recv(53).decode()
                print(f'[INFO] - Client username: {username}')

                #   save client object along with username as
                #   a pair in a dictionary
               
                users[username]=client

                #   send acknowledgement that user accepted to 
                #   client
                #users[username].send('okay!'.encode())
                self.serverStatus = 'on'
                self.serverProgress = f'Connected to: {address[0]}'

                #   initiate a thread for receiving messages 
                #   from client
                #threading.Thread(target=self.receive, args=[username, s]).start()
                #threading.Thread(target=self.syncRequest, args=[username]).start()
                self.running=1
                threading.Thread(target=self.mainHub, args=[username, s]).start()
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
                        #s.close()
                        print('[INFO] - Socket closed!')

                break
        







