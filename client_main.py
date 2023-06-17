import client
import tkinter as tk
from ttkbootstrap import *
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter.filedialog as fd
import threading
import time
import ttkbootstrap as sk
from ttkbootstrap.constants import *
import customtkinter
import datetime
import txt_to_list as ttl
import constants

class   PCSync():
    def __init__(self, root, icons) -> None:
        self.clientObj = client.Client()
        self.localFiles = self.clientObj.localFilesCount
        self.localDirs = self.clientObj.localDirsCount
        self.localSize = self.clientObj.driveSize
        self.syncPath = self.clientObj.musicPath
        self.is_Uptodate = False

        #   load widgets
        self.icons = icons
        self.root = root
        self.serverStatus = 0
        self.loadAttributes()
        self.loadWidgets()
        
        self.hidden = 0
        self.animating =0

        #   define bindings
        self.folderFrame.bind('<ButtonPress-1>', self.showAttributes)
        self.folderFrame.bind('<Enter>', self.enterEffect)
        self.folderFrame.bind('<Leave>', self.leaveEffect)

        self.inspectDrives()

    #   compares the drive sizes, if equal then UPTODATE else NOT UPTODATE
    def inspectDrives(self):    
        if float(self.localSize) == float(self.globalSize):
            self.is_Uptodate = True
            self.folderStatus.config(font=("Aquawax", 13), text='Up-to-date', bootstyle=SUCCESS)
        else:
            print(self.localSize)
            print(self.globalSize)
            self.is_Uptodate = False
            self.folderStatus.config(font=("Aquawax", 13), text='Not Up-to-date', bootstyle=DANGER)


    def enterEffect(self, event):
        self.folderFrame.config(width=505, height=47)

    def leaveEffect(self, event):
        self.folderFrame.config(width=500, height=45)

    def loadWidgets(self):
        #   set theme
        style = sk.Style("darkly")	#flatly, darkly

        #	DEFINE WINDOW - Title, Size, If size is changeable or not
        self.root.title("SOFIA.Sync - GUI")
        self.root.geometry('500x650+'+str((700)-int(450/2))+'+100')	#700x500
        self.root.resizable(False, False)

        #   define widgets
        
        #   WATCH FOLDER 
        #   CONTAINER
        self.folderContainer = Frame(self.root, width=500, height=330)
        self.folderContainer.place(relx=0.5, rely=0.44, anchor='center')#0.43

        #   cover frame, to cover anmation of folder attributes
        self.coverFrame = Frame(self.root, width=500, height=220)
        self.coverFrame.place(relx=0.5, rely=0.13, anchor='center')

        #   TOP CONTAINER
        self.topContainer = LabelFrame(self.root, width=490, height=110)
        self.topContainer.place(relx=0.5, rely=0.08, anchor='center')

        self.windowLabel = Label(self.topContainer, text='SOFIA-SYNC', foreground='gray')
        self.windowLabel.config(font=("Righteous", 26,))
        self.windowLabel.place(relx=0.5, rely=0.3, anchor='center')

        self.hostLabel = Label(self.topContainer, text='CLIENT', foreground='gray')
        self.hostLabel.config(font=("Teko Regular", 16))
        self.hostLabel.place(relx=0.5, rely=0.72, anchor='center')

        #   FOLDER
        self.folderFrame = sk.Frame(self.root, width=500, height=45, bootstyle=SECONDARY, relief='')
        self.folderFrame.place(relx=0.5, rely=0.24, anchor='center')

        self.folderLabel = Label(self.folderFrame, text='MUSIC', background="#444444", foreground='gray')
        self.folderLabel.config(font=("Aquawax", 13))
        self.folderLabel.place(relx=0.228, rely=0.81, anchor='se')

        self.folderStatus = Label(self.folderFrame, text='Up to Date', bootstyle=SUCCESS, background="#444444")
        self.folderStatus.config(font=("Aquawax", 13))
        self.folderStatus.place(relx=0.97, rely=0.25, anchor='ne')

        self.testIcon = Label(self.folderFrame, image=self.icons['folder'], background="#444444")
        self.testIcon.place(relx=0.06, rely=0.5, anchor='center')



            #   ->  EXPANDED
            #  FOLDER PATH
        self.folderPathFrame = sk.Frame(self.folderContainer, width=500, height=50, bootstyle=DARK, relief='')
        self.folderPathFrame.place(relx=0.5, rely=0.31, anchor='center')

        self.folderPathLabel = Label(self.folderPathFrame, text='FOLDER PATH', background="#303030", foreground='gray')
        self.folderPathLabel.config(font=("Aquawax", 12))
        self.folderPathLabel.place(relx=0.32, rely=0.769, anchor='se')

        self.folderPathStatus = Label(self.folderPathFrame, text=self.syncPath, background="#303030", foreground='gray')
        self.folderPathStatus.config(font=("Aquawax", 13))
        self.folderPathStatus.place(relx=0.97, rely=0.5, anchor='e')

        self.folderPathIcon = Label(self.folderPathFrame, image=self.icons['folder'], background="#303030")
        self.folderPathIcon.place(relx=0.06, rely=0.5, anchor='center')


            #   Global State
        self.globalFrame = sk.Frame(self.folderContainer, width=500, height=50, bootstyle=SECONDARY, relief='')
        self.globalFrame.place(relx=0.5, rely=0.46, anchor='center')

        self.globalLabel = Label(self.globalFrame, text='GLOBAL STATE', background="#444444", foreground='gray')
        self.globalLabel.config(font=("Aquawax", 12))
        self.globalLabel.place(relx=0.33, rely=0.769, anchor='se')

        self.globalFolderIcon = Label(self.globalFrame, image=self.icons['folder'], background="#444444")
        self.globalFolderIcon.place(relx=0.06, rely=0.5, anchor='center')

        self.globalFileIcon = Label(self.globalFrame, image=self.icons['file'], background="#444444")
        self.globalFileIcon.place(relx=0.56, rely=0.5, anchor='center')

        self.globalFileStatus = Label(self.globalFrame, text=self.globalFiles, bootstyle=SUCCESS, background="#444444", foreground='gray')
        self.globalFileStatus.config(font=("Righteous", 12))
        self.globalFileStatus.place(relx=0.62, rely=0.5, anchor='center')

        self.globalDirStatusIcon = Label(self.globalFrame, image=self.icons['folder'], background="#444444")
        self.globalDirStatusIcon.place(relx=0.7, rely=0.5, anchor='center')

        self.globalDirStatus = Label(self.globalFrame, text=self.globalDirs, bootstyle=SUCCESS, background="#444444", foreground='gray')
        self.globalDirStatus.config(font=("Righteous", 12))
        self.globalDirStatus.place(relx=0.76, rely=0.5, anchor='center')

        self.globalDriveIcon = Label(self.globalFrame, image=self.icons['drive'], background="#444444")
        self.globalDriveIcon.place(relx=0.845, rely=0.5, anchor='center')

        #   formatted global size 
        globalSize = "{:.2}".format(float(self.globalSize))
        self.globalDriveStatus = Label(self.globalFrame, text=str(globalSize)+'G', bootstyle=SUCCESS, background="#444444", foreground='gray')
        self.globalDriveStatus.config(font=("Righteous", 12))
        self.globalDriveStatus.place(relx=0.93, rely=0.5, anchor='center')

            #   Local State
        self.localFrame = sk.Frame(self.folderContainer, width=500, height=50, bootstyle=DARK, relief='')
        self.localFrame.place(relx=0.5, rely=0.61, anchor='center')

        self.localLabel = Label(self.localFrame, text='LOCAL STATE', background="#303030", foreground='gray')
        self.localLabel.config(font=("Aquawax", 12))
        self.localLabel.place(relx=0.31, rely=0.769, anchor='se')

        self.localFolderIcon = Label(self.localFrame, image=self.icons['folder'], background="#303030")
        self.localFolderIcon.place(relx=0.06, rely=0.5, anchor='center')

        self.localFileIcon = Label(self.localFrame, image=self.icons['file'], background="#303030")
        self.localFileIcon.place(relx=0.56, rely=0.5, anchor='center')

        self.localFileStatus = Label(self.localFrame, text=str(self.localFiles), bootstyle=SUCCESS, background="#303030", foreground='gray')
        self.localFileStatus.config(font=("Righteous", 12))
        self.localFileStatus.place(relx=0.62, rely=0.5, anchor='center')

        self.localFolderIcon = Label(self.localFrame, image=self.icons['folder'], background="#303030")
        self.localFolderIcon.place(relx=0.7, rely=0.5, anchor='center')

        self.localDirStatus = Label(self.localFrame, text=str(self.localDirs), bootstyle=SUCCESS, background="#303030", foreground='gray')
        self.localDirStatus.config(font=("Righteous", 12))
        self.localDirStatus.place(relx=0.76, rely=0.5, anchor='center')

        self.localDriveIcon = Label(self.localFrame, image=self.icons['drive'], background="#303030")
        self.localDriveIcon.place(relx=0.845, rely=0.5, anchor='center')

        localSize = "{:.2}".format(self.localSize)
        self.localDriveStatus = Label(self.localFrame, text=str(localSize)+'G', bootstyle=SUCCESS, background="#303030", foreground='gray')
        self.localDriveStatus.config(font=("Righteous", 12))
        self.localDriveStatus.place(relx=0.93, rely=0.5, anchor='center')

            #   Last Sync
        self.lastSyncFrame = sk.Frame(self.folderContainer, width=500, height=50, bootstyle=SECONDARY, relief='')
        self.lastSyncFrame.place(relx=0.5, rely=0.76, anchor='center')

        self.lastSyncLabel = Label(self.lastSyncFrame, text='LAST SYNC', background="#444444", foreground='gray')
        self.lastSyncLabel.config(font=("Aquawax", 12))
        self.lastSyncLabel.place(relx=0.274, rely=0.769, anchor='se')

        self.lastSyncStatus = Label(self.lastSyncFrame, text=self.lastSync, background="#444444", foreground='gray')
        self.lastSyncStatus.config(font=("Righteous", 13))
        self.lastSyncStatus.place(relx=0.97, rely=0.25, anchor='ne')

        self.lastInfoIcon = Label(self.lastSyncFrame, image=self.icons['time'], background="#444444")
        self.lastInfoIcon.place(relx=0.06, rely=0.5, anchor='center')

        self.pullButton = customtkinter.CTkButton(self.folderContainer, text='PULL',command=self.pullThread, width=75, state='normal', height=25, fg_color='#303030', hover_color='#444444', text_color='gray')
        self.pullButton.place(relx=0.73, rely=0.92, anchor='center')

        self.syncButton = customtkinter.CTkButton(self.folderContainer, text='SYNC',command=self.syncThread, width=75, state='normal', height=25, fg_color='#303030', hover_color='#444444', text_color='gray')
        self.syncButton.place(relx=0.883, rely=0.92, anchor='center')

        #   MAIN CONTAINER
        self.mainContainer = LabelFrame(self.root, width=500, height=220)
        #self.mainContainer.place(relx=0.5, rely=0.48, anchor='center')

        #   divide attribute labels
        self.sizeLabel = Label(self.mainContainer, text='SIZE')
        self.sizeLabel.config(font=("", 8, 'bold'))
        self.sizeLabel.place(relx=0.5, rely=0.25, anchor='center')

        self.modifiedLabel = Label(self.mainContainer, text='MODIFIED')
        self.modifiedLabel.config(font=("", 8, 'bold'))
        self.modifiedLabel.place(relx=0.5, rely=0.5, anchor='center')

        self.countLabel = Label(self.mainContainer, text='COUNT')
        self.countLabel.config(font=("", 8, 'bold'))
        self.countLabel.place(relx=0.5, rely=0.75, anchor='center')

        #   divide variables
        self.clientSize = Label(self.mainContainer, text='--')
        self.clientSize.config(font=("", 8, 'bold'))
        self.clientSize.place(relx=0.25, rely=0.25, anchor='center')

        self.clientModified = Label(self.mainContainer, text='--')
        self.clientModified.config(font=("", 8, 'bold'))
        self.clientModified.place(relx=0.25, rely=0.5, anchor='center')

        self.clientCount = Label(self.mainContainer, text='--')
        self.clientCount.config(font=("", 8, 'bold'))
        self.clientCount.place(relx=0.25, rely=0.75, anchor='center')

        #   server divide variables
        self.serverSize = Label(self.mainContainer, text='--')
        self.serverSize.config(font=("", 8, 'bold'))
        self.serverSize.place(relx=0.75, rely=0.25, anchor='center')

        self.serverModified = Label(self.mainContainer, text='--')
        self.serverModified.config(font=("", 8, 'bold'))
        self.serverModified.place(relx=0.75, rely=0.5, anchor='center')

        self.serverCount = Label(self.mainContainer, text='--')
        self.serverCount.config(font=("", 8, 'bold'))
        self.serverCount.place(relx=0.75, rely=0.75, anchor='center')

        #   client divide
        self.clientLabel = Label(self.mainContainer, text='CLIENT')
        self.clientLabel.config(font=("Teko Regular", 16))
        self.clientLabel.place(relx=0.25, rely=0.1, anchor='center')

        #   server divide
        self.serverLabel = Label(self.mainContainer, text='SERVER')
        self.serverLabel.config(font=("Teko Regular", 16,))
        self.serverLabel.place(relx=0.75, rely=0.1, anchor='center')

        #self.mainSeparator = ttk.Separator(self.mainContainer, orient='vertica;')


        #   BUTTONS CONTAINER
        self.buttonsContainer = Frame(self.root, width=630, height=70)
        self.buttonsContainer.place(relx=0.5, rely=0.74, anchor='center')

        self.connectButton = customtkinter.CTkButton(self.buttonsContainer, text='Connect',command=self.connectThread, width=15)
        self.connectButton.place(relx=0.5, rely=0.6, anchor='center')

        #   BOTTOM CONTAINER
        self.bottomContainer = Frame(self.root, width=630, height=90)
        self.bottomContainer.place(relx=0.5, rely=0.85, anchor='center')   

        #   PROGRESS BAR
        self.progressValue = IntVar()
        self.progressValue.set(0.9)
        self.progressBar = customtkinter.CTkProgressBar(self.bottomContainer, mode= 'indeterminate', variable=self.progressValue, width=300)
        self.progressBar.place(relx=0.5, rely=0.3, anchor='center')
        

        self.currentFile = Label(self.bottomContainer, text='OFFLINE', foreground='gray')
        self.currentFile.config(font=("Teko Regular", 18,))
        self.currentFile.place(relx=0.5, rely=0.7, anchor='center')

        #   STATUS BAR
        self.statusContainer = Frame(self.root, width=630, height=60)
        self.statusContainer.place(relx=0.5, rely=0.96, anchor='center')  

        self.serverIcon = Label(self.statusContainer, text='Status', image=self.icons['off'])
        self.serverIcon.place(relx=0.5, rely=0.33, anchor='center')

        self.serverStatusLabel = Label(self.statusContainer, text='SERVER', foreground='gray')
        self.serverStatusLabel.config(font=("Teko Regular", 16))
        self.serverStatusLabel.place(relx=0.5, rely=0.7, anchor='center')


    def showAttributes(self, event):
        if self.animating:
            print('animating...')
            return
        if self.hidden:
            #self.folderContainer.place(relx=0.5, rely=0.43, anchor='center')
            self.animateShowThread()
        else:
            self.animateShowThread()

    def animateShowThread(self):
        self.animating=1
        self.animationThreadObj = threading.Thread(target=self.animateShow)
        self.animationThreadObj.start()
        if self.animating==0: 
            self.animationThreadObj.join()

    def animateShow(self):
        if self.hidden:
            start = 700
            stop = 4400
            step = 20
            self.hidden = 0
        else:
            start = 4400
            stop = 700
            step = -20
            self.hidden = 1
        self.xpos = 0.5
        self.ypos = 0.44

        for x in range(start, stop, step):
            #self.xpos-=x
            c = x/10000   #10000
            self.folderContainer.place(relx=0.5, rely=c, anchor='center')
            time.sleep(0.00001)#0.00001

        self.animating=0
        
        pass

    def updateThread(self):
        self.running = 1
        threading.Thread(target=self.updateUI).start()

    def connectThread(self):
        if self.serverStatus:
            return
        self.serverIcon.config(image=self.icons['ready'])
        threading.Thread(target=self.connect).start()
        threading.Thread(target=self.updateThread).start()

    def pullThread(self):
        self.progressBar.start()
        threading.Thread(target=self.pull).start()
        threading.Thread(target=self.updateThread).start()

    def syncThread(self):
        self.progressBar.start()
        threading.Thread(target=self.sync).start()
        threading.Thread(target=self.updateThread).start()

    def updateUI(self):
        while self.running:
            try:
                self.currentFile.config(text=self.clientObj.status)
                self.clientCount.config(text=self.clientObj.localCount)
                self.serverCount.config(text=self.clientObj.externalCount)
                time.sleep(0.1)
            except:
                pass
        self.currentFile.config(text=self.clientObj.status)
        self.clientCount.config(text=self.clientObj.localCount)
        self.serverCount.config(text=self.clientObj.externalCount)

    def callback(self):
        print('call back')
    def connect(self):
        #   connect to server
        self.clientObj.connection()
        if not self.clientObj.connectionStatus:
            self.running = 0
            self.serverIcon.config(image=self.icons['off'])
            self.serverStatus = 0
            return
        time.sleep(1)
        self.pullButton.configure(state='active')
        self.running = 0
        self.serverIcon.config(image=self.icons['on'])
        self.serverStatus = 1

    def pull(self):
        #   request pull of current register
        self.clientObj.pullRequest()
        time.sleep(4)
        self.syncButton.configure(state='active')
        self.running = 0
        self.globalSize = self.clientObj.globalSize
        self.globalFiles = self.clientObj.globalFiles
        self.globalDirs = self.clientObj.globalDirs
        globalSize = "{:.2}".format(float(self.globalSize))
        self.globalDriveStatus.config(text=str(globalSize)+'G')
        self.globalDirStatus.config(text=self.clientObj.globalDirs)
        self.globalFileStatus.config(text=self.clientObj.globalFiles)
        self.inspectDrives()
        self.progressBar.stop()
        #   save the global pull response attributes to disk
    
    def loadAttributes(self):
        try:
            f = open('saved attributes.txt', 'r')
        except:
            pass
        attributes = ttl.to_list_single(f)

        self.globalFiles = attributes[0].split(':')[-1]
        self.globalDirs = attributes[1].split(':')[-1]
        self.globalSize = attributes[2].split(':')[-1]

        self.lastSync = attributes[3].split('><')[-1]

    def saveAttributes(self):
        f = open('saved attributes.txt', 'w')

        f.write(f'global files:{self.globalFiles}')
        f.write('\n')
        f.write(f'global dirs:{self.globalDirs}')
        f.write('\n')
        f.write(f'global size: {self.globalSize}')

        self.lastSyncStatus.config(text = self.lastSync)

        f.write('\n')
        f.write(f'last sync><{self.lastSync}')

        f.close()

    def sync(self):
        #   first compile and create missing directories
        self.clientObj.compileDirs()

        dateObj = datetime.datetime.now()
        date = str(dateObj.time()).split(':')
        hrs = date[0]
        mins = date[1]
        dayOfWeek = constants.days(dateObj.weekday())
        day = dateObj.day
        month = constants.months(dateObj.month)
        year = dateObj.year
        self.lastSync = f'{hrs}:{mins} , {dayOfWeek} {day} {month} {year}'
        self.saveAttributes()
        
        #   synchronize, request missing files, download missing files
        self.clientObj.syncInit()

        #SyncApp.clientObj.s.close()
        #   update elements
        self.updateElements()
        print('Sync Complete!')

        #   check if local and gloabal size match
        self.clientObj.getAttributes()
        self.localSize = self.clientObj.driveSize
        self.inspectDrives()

        self.running = 0
        self.progressBar.stop()
        pass
    def updateElements(self):
        self.clientObj.getLocal()
        self.clientObj.getAttributes()
        self.localFileStatus.config(text=self.clientObj.localFilesCount)
        self.localDirStatus.config(text=self.clientObj.localDirsCount)
        self.localSize = self.clientObj.driveSize
        self.localDriveStatus.config(text=str("{:.2}".format(self.localSize))+'G')
    
import time
from PIL import Image, ImageTk

#   load tkinter main object
root = customtkinter.CTk()
#root.attributes("-alpha", 0.95)

#   resize image
def resizeImage(path, image, fraction, W, H):
    sizeW = int((fraction/100) * W)
    sizeH = int((fraction/100) * H)
    image = Image.open(path + image)
    resizedImg = image.resize((sizeW, sizeH))
    img = ImageTk.PhotoImage(resizedImg)
    return img

folderIcon = resizeImage(path='R:\\Photoshop\\', image=str('folder icon.png'), fraction=9, W=249, H=182)
fileIcon = resizeImage(path='R:\\Photoshop\\', image=str('file icon.png'), fraction=2, W=716, H=980)
driveIcon = resizeImage(path='R:\\Photoshop\\', image=str('drive icon.png'), fraction=2.5, W=786, H=561)
infoIcon = resizeImage(path='R:\\Photoshop\\', image=str('info icon.png'), fraction=1, W=1600, H=1600)
timeIcon = resizeImage(path='R:\\Photoshop\\', image=str('time icon.png'), fraction=1.9, W=980, H=980)
syncIcon = resizeImage(path='R:\\Photoshop\\', image=str('sync button.png'), fraction=100, W=50, H=30)
onIcon = resizeImage(path='R:\\Photoshop\\', image=str('on.png'), fraction=8, W=400, H=150)
readyIcon = resizeImage(path='R:\\Photoshop\\', image=str('ready.png'), fraction=8, W=400, H=150)
offIcon = resizeImage(path='R:\\Photoshop\\', image=str('off.png'), fraction=8, W=400, H=150)

icons = {'folder':folderIcon, 'file':fileIcon, 'drive':driveIcon, 'info':infoIcon, 'time':timeIcon, 'sync':syncIcon, 'on':onIcon,
         'ready':readyIcon, 'off':offIcon}


SyncApp = PCSync(root, icons)
'''try:
    SyncApp.connect()
    time.sleep(1)
    SyncApp.pull()
    time.sleep(4)
    SyncApp.sync()
    SyncApp.clientObj.s.close()
    print('Sync Complete!')
except Exception as e:
    print(e)'''

root.mainloop()
