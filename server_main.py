import tkinter as tk
from ttkbootstrap import *
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter.filedialog as fd
import threading
import time
import ttkbootstrap as sk
from ttkbootstrap.constants import *
import customtkinter
from PIL import Image, ImageTk
import datetime
import txt_to_list as ttl
import server

#   gui for the server socket responsible for
#   setting the root directory and starting the server
#   displays the ip and port the server is running on
#   indicates if server is off, listening or running
class SyncGui():
    def __init__(self, root, icons) -> None:
        self.root = root
        self.icons = icons
        self.selectedPath = ''

        #   create the server object
        self.serverObj = server.Server()

        #   initialise the gui elements
        self.initWidgets()

    #   main window of the gui displays
    #   text box showing the selected root directory path
    #   load button, to load a path
    #   set path, to assign the selected path as the root
    #   server button, which starts the server
    #   info text, shows the ip and port for the server
    #   indicator, red server is off, yellow is listening
    #   green the server is connected.
    def initWidgets(self):
        #   set theme for the gui
        style = sk.Style("darkly")	#flatly, darkly

        #	DEFINE WINDOW - Title, Size, If size is changeable or not
        self.root.title("SOFIA.Instagram - GUI")
        self.root.geometry('450x250+'+str((700)-int(450/2))+'+100')	#700x500
        self.root.resizable(False, False)

        #   MIDDLE CONTAINER
        self.middleContainer = Frame(self.root, width=450, height=100)
        self.middleContainer.place(relx=0.5, rely=0.2, anchor='center')

        self.inputVar = StringVar()
        self.inputBox = Entry(self.middleContainer, textvariable=self.inputVar, width=40, state=DISABLED)
        self.inputBox.place(relx=0.5, rely=0.35, anchor='center')

        self.loadButton = Button(self.middleContainer, text='Load Path', width=10, command=self.selectPath)
        self.loadButton.place(relx=0.35, rely=0.75, anchor='center')

        self.setButton = Button(self.middleContainer, text='Set Path', width=10, command=self.setPath)
        self.setButton.place(relx=0.65, rely=0.75, anchor='center')

        #   BUTTONS CONTAINER
        self.buttonsContainer = Frame(self.root, width=450, height=80)
        self.buttonsContainer.place(relx=0.5, rely=0.55, anchor='center')

        self.startButton = Button(self.buttonsContainer, text='Server', command=self.startThread)
        self.startButton.place(relx=0.5, rely=0.5, anchor='center')

        #   STATUS CONTAINER
        self.statusContainer = Frame(self.root, width=450, height=73)
        self.statusContainer.place(relx=0.5, rely=0.85, anchor='center')

        self.progressLabel = Label(self.statusContainer, text='---')
        self.progressLabel.config(font=("Righteous", 13))
        self.progressLabel.place(relx=0.5, rely=0.4, anchor='center')

        self.statusLabel = Label(self.statusContainer, image=self.icons['off'])
        self.statusLabel.place(relx=0.5, rely=0.8, anchor='center')

    def selectPath(self):
        self.selectedPath =  filedialog.askdirectory()
        self.inputVar.set(self.selectedPath)
        print(self.selectedPath)

        #   format path from /../../ to \\..\\..\\
        #   I'm used to a certain delimiter in my paths so yeah
        self.selectedPath = self.selectedPath.replace('/', "\\\\")

        print(f'formatted path: {self.selectedPath}')

    #   if a new directory path has been selected then this
    #   function assigns it as the root directory for the app
    def setPath(self):
        #   dont do anything if no path has been selected
        if self.selectedPath=='':
            return
        
        #   no comment, I don't remember what the next part is about lmao
        dirAsList = self.selectedPath.split('\\\\')
        dirAsList[-1]=''
        path = ''
        #   create abs path, which is not part of the root directory
        #   e.g is path is D:\\New Folder\\PC Sync\\
        #   D:\\New Folder is the absolute path, -I think lol-
        for filepath in dirAsList:
            if filepath!='':
                path += filepath
                path += '\\\\'

        musicPath = self.selectedPath  #example    'D:\\PC Sync'
        absPath = path   #example    'D:\\'

        #   where music path is the root directory of the app
        #   and abspath is the path before the root
        #   example D:\\New Folder\\PC Sync
        #   our root folder is \\PC Sync
        #   and abspath is D:\\New Folder
        print(musicPath)
        print(absPath)

        self.serverObj.musicPath = self.selectedPath
        self.serverObj.absPath = path

        self.progressLabel.config(text=f'root dir: {self.selectedPath[:30]}')

    #   creates a thread in which we initiate the server socket
    def startThread(self):
        try:
            if self.serverRunning:
                return
        except:
            pass
        self.serverRunning = True
        serverThread = threading.Thread(target=self.startServer) 
        serverThread.start()

        #   joins the thread if server socket is closed
        if not self.serverRunning:
            serverThread.join()

    #   process that initiates the server
    #   changes ui elements to show user current status of the server
    def startServer(self):

        #   change server indicator to yellow, showing server is listening
        self.statusLabel.config(image=self.icons['ready'])

        #   thread to initiate the server, set ip and port and listen
        serverThread = threading.Thread(target=self.serverObj.connection)
        serverThread.start()

        try:
            #   joins the above thread when process concludes
            if not self.serverObj.serverRunning:
                serverThread.join()
        except:
            pass
        
        #   loop that updates ui, whilst server is running
        #   displays current processes e.g pulling, syncing, requesting
        #   also displays what files is being synced
        while self.serverObj.serverRunning:
            self.statusLabel.config(image=self.icons[self.serverObj.serverStatus])
            self.progressLabel.config(text=self.serverObj.serverProgress)
            time.sleep(0.5)

        self.serverRunning = False

root = customtkinter.CTk()

#   function to resize icons
#   loads them and resizes them to a particular fraction or percentage
def resizeImage(path, image, fraction, W, H):
    sizeW = int((fraction/100) * W)
    sizeH = int((fraction/100) * H)
    image = Image.open(path + image)
    resizedImg = image.resize((sizeW, sizeH))
    img = ImageTk.PhotoImage(resizedImg)
    return img

#   initiate all icons before initating the gui,
#   because for some reason tkinter wont allow you add more 
#   images after compilation
onIcon = resizeImage(path='R:\\Photoshop\\', image=str('on.png'), fraction=8, W=400, H=150)
readyIcon = resizeImage(path='R:\\Photoshop\\', image=str('ready.png'), fraction=8, W=400, H=150)
offIcon = resizeImage(path='R:\\Photoshop\\', image=str('off.png'), fraction=8, W=400, H=150)

icons = {'on':onIcon,'ready':readyIcon, 'off':offIcon}

app = SyncGui(root, icons)
root.mainloop()