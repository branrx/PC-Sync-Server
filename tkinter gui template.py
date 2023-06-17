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

class Instagram():
    def __init__(self, root, icons) -> None:
        self.root = root
        self.icons = icons
        self.selectedPath = ''
        self.serverObj = server.Server()

        self.initWidgets()

    def initWidgets(self):
        #   set theme
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

        #   foramt path from /../../ to \\..\\..\\
        self.selectedPath = self.selectedPath.replace('/', "\\\\")

        print(f'formatted path: {self.selectedPath}')

    def setPath(self):
        if self.selectedPath=='':
            return
        
        dirAsList = self.selectedPath.split('\\\\')
        dirAsList[-1]=''
        path = ''
        #   create abs path
        for filepath in dirAsList:
            if filepath!='':
                path += filepath
                path += '\\\\'

        musicPath = self.selectedPath  #example    'D:\\PC Sync'
        absPath = path   #example    'D:\\'

        print(musicPath)
        print(absPath)

        self.serverObj.musicPath = self.selectedPath
        self.serverObj.absPath = path

        self.progressLabel.config(text=f'root dir: {self.selectedPath[:30]}')

        pass

    def startThread(self):
        try:
            if self.serverRunning:
                return
        except:
            pass
        self.serverRunning = True
        serverThread = threading.Thread(target=self.startServer) 
        serverThread.start()
        if not self.serverRunning:
            serverThread.join()

    
    def startServer(self):
        self.statusLabel.config(image=self.icons['ready'])

        serverThread = threading.Thread(target=self.serverObj.connection)
        serverThread.start()

        try:
            if not self.serverObj.serverRunning:
                serverThread.join()
        except:
            pass

        while self.serverObj.serverRunning:
            self.statusLabel.config(image=self.icons[self.serverObj.serverStatus])
            self.progressLabel.config(text=self.serverObj.serverProgress)
            time.sleep(0.5)

        self.serverRunning = False

    def callback(self):
        print('callback')

root = customtkinter.CTk()
#   resize image
def resizeImage(path, image, fraction, W, H):
    sizeW = int((fraction/100) * W)
    sizeH = int((fraction/100) * H)
    image = Image.open(path + image)
    resizedImg = image.resize((sizeW, sizeH))
    img = ImageTk.PhotoImage(resizedImg)
    return img

onIcon = resizeImage(path='R:\\Photoshop\\', image=str('on.png'), fraction=8, W=400, H=150)
readyIcon = resizeImage(path='R:\\Photoshop\\', image=str('ready.png'), fraction=8, W=400, H=150)
offIcon = resizeImage(path='R:\\Photoshop\\', image=str('off.png'), fraction=8, W=400, H=150)

icons = {'on':onIcon,'ready':readyIcon, 'off':offIcon}

app = Instagram(root, icons)
root.mainloop()