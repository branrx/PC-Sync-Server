import socket
import time
import threading
import main_process
import txt_to_list as ttl
import os
import directory_crawler as dc

class Client():
    def __init__(self) -> None:
        #self.musicPath = 'C:\\Users\\Brandon\\Documents\\PC Sync\\'
        #self.absPath = 'C:\\Users\\Brandon\\Documents\\'
        self.musicPath = 'C:\\Users\\Brandon\\Music\\PC Sync\\'
        self.absPath = 'C:\\Users\\Brandon\\Music\\'
        self.status = '...'
        self.localCount = '-'
        self.externalCount = '-'
        self.getLocal()
        self.getAttributes()
    def connection(self):
        self.status = 'Connecting to server...'
        #	CREATE INSTANCE
        self.s = socket.socket()

        #	HOST AND PORT
        self.host = '192.168.0.106'
        #self.host = '0.0.0.0'
        #self.port = 27200
        self.port = 24300

        #	CONNECT TO SERVER
        try:
            self.s.connect((self.host, self.port))
        except:
            self.status = 'Failed to connect to server.'
            self.connectionStatus = 0
            return
        self.connectionStatus = 1
        self.status = 'Connected to: Host'
        print(f'admin: {self.s.recv(1024).decode()}')
        self.s.send('Brans UltraBook'.encode())
        #self.s.send(input().encode())
        print(self.s.recv(1024).decode())

        self.status = 'Connected to server successfully.'


    def receive(self):
        msg = self.s.recv(1024)    
        while msg:
            print(f'admin: {msg.decode()}')
            if msg.decode()=='bye':
                    break
            msg = self.s.recv(1024)

    def sendAudio(self):
        audioFile = open('Holy Ten - Pfumo(MP3_320K).mp3', 'rb')

        for byte in audioFile:
            self.s.send(byte)

        print('sent!')

    def sending(self):
        msg = 'ini'
        while msg!='bye':
            msg = input()
            #receipient()
            self.s.send(msg.encode())

    def receipient(self):
        name = 'to:ren'
        while name:
            self.s.send(name.encode())

    #   receives response from pull request
    def pullResponse(self):
        self.status = 'Awaiting pull response.'
        #   create destination register file in local
        f = open('current register dst.txt', 'wb')
    
        #   get size of the destination file
        docSize = self.s.recv(100)
        docSize = int.from_bytes(docSize, 'big')
        print(f'file size: {docSize}')

        count = 0

        #   receive contents of destination register file
        while True:
            self.status = 'Awaiting pull data.'
            #   sock receive destination register contents
            print(docSize)
            buff = self.s.recv(docSize)

            #   keep track of how many bytes have been read
            if count == 0:
                term = buff
                count = 1
            else:
                term+=buff

            try:
                if buff.decode() == 'eof':
                    break
            except Exception as e:
                print(e)

            f.write(buff)
        
        print('writing client')
        f.close()
        self.status = 'Pull response received.'
        self.getPullResponseData()

    def getPullResponseData(self):
        f = open('current register dst.txt', 'r')

        data = ttl.to_list_single(f)
        self.globalSize = data[-1].split(':')[-1]
        self.globalDirs = data[-2].split(':')[-1]
        self.globalFiles = data[-3].split(':')[-1]

        f.close()

    #   asks the server to check files present, and send
    #   them to compare
    def pullRequest(self):
        self.s.send('pull'.encode())
        self.pullResponse()
        self.status = 'Initiating pull request.'
        #   RECENT CHANGE
        '''while True:
            self.s.send('pull'.encode())
            time.sleep(1)
            self.s.send('pull'.encode())
            self.pullResponse()
            break'''

    #   ask the server to sync, request files we dont have
    def syncInit(self):
        #   compile missing files
        #   compiles missing files, assuming we already made a pull request
        self.prepareSync()

        if self.missingCount<1:
            self.status = 'Directories up to date.'
            self.deleteFiles()
            self.status = 'Sync complete.'
            return
        
        self.status = 'Requesting sync.'
        #   request sync, tell server to prepare
        self.s.send('sync'.encode())
        time.sleep(3)
        

        #   send the local register
        self.status = 'Posting local register.'
        self.syncRequest()

    #   post local register and request sync
    def syncRequest(self):
        self.status = 'Loading missing files.'
        #   read local register file
        register = open('missing files.txt', 'rb')
        file = open('missing files.txt', 'rb')
        

        self.fileNameDict = dict()
        f = open('missing files.txt', 'r')
        files = ttl.to_list_single(f)

        #   save files indexed in dictionary
        for item in files:
            #   extract file index from string ex. 2**
            fileName = item.split('**')
            fileIndex = fileName[0]

            #   discard the root dir url ex. src dir\\
            rootDiscard = item.split('\\')[0]
            newUrl = item.replace(rootDiscard, '')

            #   add local sync root folder url
            #newUrl = self.musicPath + newUrl

            self.fileNameDict[fileIndex] = newUrl

    
        #   get file as bytes
        bytesToSend = register.read()

        #   get file size and send it before contents
        fileSize = len(bytesToSend)
        fileSize_inBytes = int.to_bytes(fileSize, 10, 'big')
        self.s.send(fileSize_inBytes)
        print(f'file size: {fileSize}')
        self.status = 'Sending missing files.'
        for byte in file:
            print('sending missing files file.')
            self.s.send(byte)


        #   wait till missing files is received
        confirm = self.s.recv(56)
        #   confirm end of file
        #self.s.send('eof'.encode())
        self.status = 'Sync request sent.'
        print('[INFO] Finished posting sync request.')

        self.syncResponse()
        
    def syncResponse(self):
        self.status = 'Awaiting sync response.'
        filesCount = self.s.recv(28)
        filesCount = int.from_bytes(filesCount, 'big')

        self.status = f'Files to expect: {filesCount}.'
        print(f'Files to expect: {filesCount}')

        #   send confirmation that index recieved
        self.s.sendall('okay'.encode())

        #   receive files
        self.receiveFiles(filesCount)

    def receiveFiles(self, filesCount):
        self.status = 'Sync starting...'
        fileIndex = self.s.recv(28)
        fileIndex = fileIndex.decode()
        self.status = self.fileNameDict[fileIndex].split('\\')[-1][:30] + '...'
        print(f'receiving index: {fileIndex}')

        #   send confirmation that index recieved
        self.s.sendall('index'.encode())
        
        f = open(f'{self.musicPath}\\{self.fileNameDict[fileIndex]}', 'wb')

        count = 1
        fileSize = self.s.recv(28)
        fileSize = int.from_bytes(fileSize, 'big')
        print(f'file sizeA: {fileSize}')
        totalBuff = bytearray()

        #   send confirmation that index recieved
        self.s.sendall('size'.encode())
        startTime = time.time()
        while True:
            #buff = self.s.recv(fileSize)
            #xsize = len(buff)
            #print(f'file size B: {xsize}')

            #buff = self.s.recv(fileSize)
            #xsize = len(buff)
            #print(f'file size B: {xsize}')

            while len(totalBuff) != fileSize:
                buff = self.s.recv(fileSize)
                totalBuff += buff
                #print(f'size downloaded: {len(totalBuff)}')
                #time.sleep(1)

            f.write(totalBuff)
            f.close()
            

            print(f'final received byte size: {len(totalBuff)}')
            totalBuff = bytearray()
            #   tell server to send next file
            self.s.sendall('eof'.encode())

            count = count + 1
            if count>filesCount:
                break
                    
            #   receive index of file being sent
            fileIndex = self.s.recv(28)
            fileIndex = fileIndex.decode()
            print(f'file being received: {fileIndex}')

            #   send confirmation that index recieved
            self.s.sendall('index'.encode())
                    
            self.status = self.fileNameDict[fileIndex].split('\\')[-1][:30]+'...'
            f = open(f'{self.musicPath}\\{self.fileNameDict[fileIndex]}', 'wb')
            fileSize = self.s.recv(28)
            fileSize = int.from_bytes(fileSize, 'big')
            print(f'file size = {fileSize}')
            #   send confirmation that index recieved
            self.s.sendall('size'.encode())
            '''
            try:
                if buff.decode()=='eos':
                    print(' eos close')
                    break
                elif buff.decode() == 'eof':
                    f.close()
                    #   tell server to send next file
                    self.s.sendall('okay'.encode())

                    count = count + 1
                    if count>filesCount:
                        break
                    
                    #   receive index of file being sent
                    fileIndex = self.s.recv(100)
                    fileIndex = fileIndex.decode()
                    print(f'file being received: {fileIndex}')

                    
                    self.status = self.fileNameDict[fileIndex].split('\\')[-1][:30]+'...'
                    f = open(f'{self.musicPath}\\{self.fileNameDict[fileIndex]}', 'wb')
                    fileSize = self.s.recv(100)
                    fileSize = int.from_bytes(fileSize, 'big')
                    print(f'file size = {fileSize}')
                    continue
            except Exception as e:
                pass
            f.write(buff)'''
        endTime = time.time()
        elapsedTime = endTime - startTime
        print(f'time taken: {elapsedTime}')
        self.status = 'Sync complete.'

        #   delete files that exist locally but not globally
        self.deleteFiles()

    def deleteFiles(self):
        #   load registers
        localRegister = open('register local.txt', 'r')
        externalRegister = open('current register dst.txt', 'r')
        
        extList = ttl.to_list_single(externalRegister)
        lclList = ttl.to_list_single(localRegister)

        #   remove folder attributes information
        extList.pop()
        extList.pop()
        extList.pop()

        self.status = 'Compiling files to delete.'
        #   stores missing files, which will be requested on sync
        filesToDelete = list()
        deletee =  True

        for item in lclList:
            #   remove the root dir name from item, 
            #   so they are easily comparable
            lclRoot = item.split('\\')[0]
            lclItem = item.replace(lclRoot, '')
            
            for file in extList:
                extRoot = file.split('\\')[0]
                extItem = file.replace(extRoot, '')

                if extItem == lclItem:
                    deletee = False
                    break
                else:
                    deletee = True
            if deletee:
                filesToDelete.append(item)
        self.deleteCount = len(filesToDelete)

        self.status = 'Deleting local files not in global.'

        print(f"No. files to delete: {self.deleteCount}")

        #   delete files
        for file in filesToDelete:
            name = file.split('\\')[-1]
            self.status = f"Deleting: {name[:30]}"
            filePath = file.split('**')[-1]
            os.remove(self.absPath+filePath)

        self.status = f"Finished deleting files."

        self.status = 'Sync complete.'
        
        
    #  prepare sync files, compare registers and send missing
    def prepareSync(self):
        self.status = 'Creating local register.'
        #   create local files register
        extensions = {'.mp3', '.m4a', '.py', '.txt', '.rar'}
        main_process.getFiles(filename='register local.txt', path=self.musicPath, extensions=extensions, absPath=self.absPath)

        print('[INFO] Done compiling local files.')

        #   load registers
        localRegister = open('register local.txt', 'r')
        externalRegister = open('current register dst.txt', 'r')
        
        extList = ttl.to_list_single(externalRegister)
        lclList = ttl.to_list_single(localRegister)

        self.localCount = len(lclList)
        self.externalCount = len(extList)

        extList.pop()
        extList.pop()
        extList.pop()

        self.status = 'Compiling missing files.'
        #   stores missing files, which will be requested on sync
        missingFiles = list()
        missing =  True
        for item in extList:
            #   remove the root dir name from item, 
            #   so they are easily comparable
            extRoot = item.split('\\')[0]
            extItem = item.replace(extRoot, '')
            
            for file in lclList:
                lclRoot = file.split('\\')[0]
                lclItem = file.replace(lclRoot, '')

                if lclItem == extItem:
                    missing = False
                    break
                else:
                    missing = True
            if missing:
                missingFiles.append(item)
        self.missingCount = len(missingFiles)
        #   save missing files to txt
        f = open('missing files.txt', 'w')

        for item in missingFiles:
            f.write(item)
            f.write('\n')
        print('missing files: ')
        print(missingFiles)
        self.status = 'Finished compiling missing files.'
        print('[INFO] Finished compiling missing files.')

    #   compiles missing directories based on the external register
    def compileDirs(self):
        self.status = 'Creating missing directories.'
        syncRoot = self.musicPath
        f = open('current register dst.txt', 'r')
        files = ttl.to_list_single(f)

        #   where we store the paths for every file
        dirPaths = list()

        for item in files:
            pathBuff = item.split('\\')

            #   change the root dir
            newPath = item.replace(pathBuff[0], syncRoot)

            #   discard filename from path
            newPath = newPath.replace(pathBuff[-1], '')

            print(f'old path: {item}')
            print(f'new path: {newPath}')
            print('*********\n')

            #   store the path in list
            if newPath not in dirPaths:
                dirPaths.append(newPath)

        #   get all paths
        print(dirPaths)

        self.createDirs(dirPaths)


    #   creates new directories after they have been compiled
    def createDirs(self, dirPaths):
        #   check if paths exist, if not create new
        for path in dirPaths:
            if os.path.exists(path=path):
                pass
            else:
                os.mkdir(path=path)

    #   gets attributes and files and dirs count
    def getLocal(self):
        extensions = {'.mp3', '.m4a', '.py', '.txt', '.rar'}
        files, paths, dirs = dc.getFilesAndDirs(self.musicPath, extensions=extensions)

        self.localFilesCount = len(files)
        self.localDirsCount = len(dirs)

    def getAttributes(self):
        extensions = {'.mp3', '.m4a', '.py', '.txt', '.rar'}
        files, paths, dirsCount = dc.getFiles(self.musicPath, extensions=extensions)
        size = 0 
        for file in paths:
            size += os.path.getsize(file)

        self.driveSize  = ((size/1024)/1024)/1024
        pass

    
        

                


    

#clientObject = Client()
#clientObject.connection()
#clientObject.pullRequest()
#clientObject.syncInit()
#clientObject.compileDirs()

#threading.Thread(target=pullRequest).start()
#threading.Thread(target=sending).start()

#threading.Thread(target=receive).start()


#s.close()
