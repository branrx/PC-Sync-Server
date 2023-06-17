import socket
import time
import threading
import main_process
import sys
import txt_to_list as ttl
import directory_crawler as dc
import addTrailingBits

#   users - stores instances of all connected devices, in dict
#   status - is the status of the server receive and send function
#       stored as a list, [1, 1] meaning can recv and send
#       [0, 0] means cannot recieve and send therefore is flag to close server 
#   serverStatus - tells the system if server is running or not
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
          self.serverRunning = True
          self.serverStatus = 'off'
          self.serverProgress = 'Offline'
          
    
    def requestHandle(self, req: str, name: str):
        if req == 'pull':
            print('request: PULL')
            
            #   create root path
            #   extensions, are elligible file types, if a type
            #   is not  incl. in this list then it's skipped 
            #   during directory crawl
            path = self.musicPath + '\\'
            extensions = {'.mp3', '.m4a'}
            
            #   gather all files in root directory and save them 
            #   in txt file = register dst.txt
            main_process.getFiles(filename='register dst.txt', path=path, extensions=extensions, absPath=self.absPath)

            #   send the txt response as the pull response
            self.pullResponse(name)

    #   response to get current register from server
    #   respond to the client's pull request
    #   sends txt file containing files present in global directory
    #   along with attributes of directory incl. size, file and dir  count
    def pullResponse(self, name: str):
        self.serverProgress = 'Preparing pull response.'

        #   read destination register file
        register = open('register dst.txt', 'rb')
        file = open('register dst.txt', 'rb')
        
        #   get file contents as bytes
        bytesToSend = register.read()

        self.serverProgress = 'Sending pull response.'

        #   await ack from client to send file size
        print('waiting for confirmation to start')
        users[name].recv(53)

        #   get file size and send it to the client
        fileSize = len(bytesToSend)
        fileSize = addTrailingBits.addTrail(8, str(fileSize), '0')
        users[name].send(fileSize.encode())
        print(f'file size: {fileSize}')
        
        #   await ack from client to send register data
        users[name].recv(53)

        #   send destination register contents
        #   i dont know why i called it file instead of byteArray or something
        for byte in file:
            users[name].send(byte)

        #   update ui that pull request has been sent
        self.serverProgress = 'Pull response sent.'
        print('finished sending response')
        
    #   handles sync requests from client
    def syncRequest(self, name: str):
        #   create the missing files file, which is a file
        #   containing files that are present globally but not locally
        f = open('current missing files.txt', 'wb')

        #   send confimation to start
        #   and await approval ack
        users[name].send("okay".encode())
        self.serverProgress = 'Waiting for missing files list.'
        confirm = users[name].recv(53)
        print(confirm.decode())
        
        #   receive the missing files file size and data
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
        
        #   write the bytes to a file and save as .txt
        f.write(totalSize)
        totalSize = bytearray()
        self.serverProgress = 'Receieved missing files list.'
        print('[INFO] Received missing files file.')
        f.close()

        #   initiate sync response
        self.syncResponse(name)

    #   send files that are missing - sync
    #   does the actual syncing
    def syncResponse(self, name: str):
        self.serverProgress = 'Sending sync response.'
        time.sleep(5)

        #   load missing files file as list
        f = open('current missing files.txt', 'r')
        missingFiles = ttl.to_list_single(f)
        
        #   store sync variables
        filesCount = len(missingFiles)

        #   send the missing files
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
    def sendFiles(self, name: str, missingFiles: list):

        #   await ack to start sync
        self.name = name
        self.confirmationTicket = False
        self.serverProgress = 'Sending requested files.'
        fileSize = users[name].recv(53)
        print("starting sync")

        #   for file in missing files, send them to the client
        #   send index of the file first
        #   then size of file
        #   then data
        #   no need to send filename as we use the index to find the filename
        #   on the client side
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

            self.confirmationTicket = True
            print('confirmation after index received')
            
            #   get filename and remove index and absolute path
            newName = file.replace(f'{fileIndex}**', '')
            newName = self.absPath + newName
            self.serverProgress = f'Syncing: {newName[30]}'

            print(newName)

            #   load the file as bytes
            audioFile = open(newName, 'rb')
            audioFileB = open(newName, 'rb')
            fileSizeB =  audioFileB.read()
            fileSizeB = len(fileSizeB)

            #   prepare size string and send it
            try:
                fileSizeFinal = addTrailingBits.addTrail(8, str(fileSizeB), "0")
            except Exception as e:
                 print(e)

            users[name].send(fileSizeFinal.encode())
            print(f'file size: {str(fileSizeFinal)}')

            #   await receipt ack
            confirm = ""
            while confirm!="okay": 
                msg = users[name].recv(53)
                confirm = msg.decode()

            self.confirmationTicket = True
            print('confirmation after size received')
            
            #   send file data
            data = audioFile.read()
            users[name].sendall(data)

            #   wait for receipt ack
            confirm = ""
            while confirm!="okay": 
                msg = users[name].recv(53)
                confirm = msg.decode()

            self.confirmationTicket = True
        
        #   ack end of sync
        users[name].send('eos'.encode())
        self.serverProgress = 'Sync Complete.'
        print('Sync Complete.')

        #   means the system is not pulling or syncing
        self.running=0

    #   main function, hangs until a request is made
    #   listens for a pull or sync request
    def mainHub(self, name, s):
        status[0]=1
        while self.running:
            #   if request, then process accordingly
            #   listen for requests
            request = users[name].recv(53)
            request = request.decode()

            if request == 'pull':
                try:
                    self.requestHandle('pull', name)
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

    #	ESTABLISH CONNECTION WITH THE CLIENT
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
                #threading.Thread(target=self.sending, args=[username, s]).start()

                #   if server is off for send or receive thread
                #   close the sockets to stop unexpected errors
                if status[0]==0 or status[1]==0:
                        #s.close()
                        print('[INFO] - Socket closed!')
                #lkjd
                break
        







