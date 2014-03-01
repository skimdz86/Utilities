'''
Created on 06/feb/2014

@author: Marco
'''

from tkinter import Frame, Tk, BOTH, Button, RIGHT, BOTTOM, Text, Message, INSERT, END, TOP,\
    StringVar, CENTER, LEFT, X, scrolledtext, WORD, GROOVE, DISABLED, Label, Entry, RAISED, NORMAL, Listbox, Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter import font
import socket
import re
import threading
import winsound
import traceback
#import pywintypes
#import pythoncom # Uncomment this if some other DLL load will fail
#import win32gui
import ctypes


connectedClients = []

conversationBoxList = dict()

class receiveThread (threading.Thread):
    
    def __init__(self, threadID, name, conn, guiWindow):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.conn = conn
        self.guiWindow = guiWindow
    def run(self):
    
        global connectedClients
        global conversationBoxList
    
        print("Starting receiver thread" + self.name)
        #print_time(self.name, self.counter, 5)
        try:
            while True:
                message = self.conn.recv(1024)
                #print("TEST: " + message.decode('utf-8'))
                if not message:
                    raise Exception
                if not message == "":
                    
                    if message.decode('utf-8').startswith("USER_SYNC-"):
                        #aggiorno la lista dei client
                        csvClients = message.decode('utf-8').replace("USER_SYNC-", "")
                        #print("USER LIST: "+csvClients)
                        connectedClients = csvClients.strip(",").split(",")
                        #print(connectedClients)
                        self.guiWindow.updateUsersFrame()
                    else:
                        print(message.decode('utf-8'))
                        m = re.search("^  ##.*##", message.decode('utf-8'), re.MULTILINE)
                        print("Match? ")
                        print(m)
                        if m is not None:
                            privateMessage = re.sub("  ##.*##", "  ", message.decode('utf-8'), re.MULTILINE)
                            print("PM:" + privateMessage)
                            
                            pmnick = re.sub("  ##", "", m.group(0))
                            pmnick = re.sub("##", "", pmnick)
                            print("PMNICK: "+pmnick)
                            print("My nick: "+ getNickname())
                            #if not exists una finestra gia  aperta con quell'utente, call self.guiwindow.privateChat
                            if pmnick not in conversationBoxList and not pmnick == getNickname(): 
                                print("PM non presente per " + pmnick)
                                self.guiWindow.parent.focus()
                                self.guiWindow.receivePrivateChat(pmnick)
                            else:
                                print("PM gia presente per " + pmnick)
                            
                            if pmnick == getNickname():
                                self.guiWindow.setprivatetext(pmnick, privateMessage, True)
                            else:
                                self.guiWindow.setprivatetext(pmnick, privateMessage, False)
                        else:
                            self.guiWindow.printConversation(message.decode('utf-8'))
                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS) #SystemHand / SystemExclamation 
                        #ctypes.windll.user32.FlashWindowEx(self.guiWindow,0,10,1)
                        
                        EnumWindows = ctypes.windll.user32.EnumWindows
                        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
                                            
                        #titles = []
                        
                        EnumWindows(EnumWindowsProc(foreach_window), 0)
                        #print("NOMI VARI")
                        #for i in range(len(titles)):
                        #    print(titles[i])
                        #    print("\n")
                     
        except Exception:
            print(traceback.format_exc())
            print("Server disconnesso")
        print("Exiting receiver thread" + self.name)

def foreach_window(hwnd, lParam):
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    if IsWindowVisible(hwnd):       
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        #titles.append((hwnd, buff.value))
        
        if "Python Chat" in str(buff.value):
            #print("MATCH TROVATO : "+str(buff.value))
            #ctypes.windll.user32.FlashWindowEx(hwnd,2,5,0) # window, flag (solo taskbar: 0x00000002, all: 0x00000003), numero blink, timeout (in ms)
            ctypes.windll.user32.FlashWindow(hwnd,True)
            #ctypes.windll.user32.BringWindowToTop(hwnd)
        
    return True
###############################################################################################################################################
class ChatGUI(Frame):
    
    def __init__(self, parent, conn, title):
        #Frame.__init__(self, parent, background="grey")   
         
        self.parent = parent
        self.conn = conn
        self.title = title
        
        self.centerWindow()
        self.initUI()
    
    def initUI(self):
      
        self.lineCounter = 0
      
        # create a custom font
        self.customFontHeader = font.Font(family="Calibri", slant = "italic") #family="Helvetica", weight="bold", slant="italic")
        self.customFontMessage = font.Font(family="Calibri")
        
        self.parent.title(self.title) 
        
        frame = Frame(self.parent)
        frame.pack(fill=BOTH, expand=1, side=LEFT)
        
        self.box = ScrolledText(frame, wrap=WORD, relief = GROOVE, width=30, height=18, font=self.customFontMessage)
        self.box.insert(END, 'Welcome to Python Chat!')
        self.box.config(state=DISABLED)
        self.box.pack(expand="yes", fill=BOTH, side=TOP)
        
        self.textarea = Text(frame, width=30, height=5)
        #self.textarea.insert(END, "")
        self.textarea.bind("<KeyRelease-Return>", self.gettext) #Se metto on press, rimane una newline in piu
        self.textarea.pack(expand="yes", fill=BOTH, side=TOP)

        
        okButton = Button(frame, text="Panic Button", activebackground="red", command=self.sendFile) 
        okButton.pack(expand="no", fill=BOTH, side=TOP)
        
        self.usersFrame = Frame(self.parent)
        self.usersFrame.pack(fill=BOTH, expand=1, side=RIGHT)
        
        self.userListbox = Listbox(self.usersFrame, width=3)
        self.userListbox.bind("<Double-Button-1>", self.privateChat)
        self.userListbox.pack(fill=BOTH, expand=1)
            
        self.updateUsersFrame()
        
    def centerWindow(self):
      
        w = 600
        h = 475

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
     
    def gettext(self, e): #e sta per event, questo e' un listener
        text = self.textarea.get("1.0", END + " - 2c") # 1.0: row:columa -  END-2c rimuove l'ultimo carattere, una newline \r\n
        self.textarea.delete("0.0", END) #NON VA: il problema e' che viene inviato il carattere di newline ma non incluso nell'area a causa della bind mi sa. Devo escluderlo io
        self.sendToServer(text)
        
    def printConversation(self, message):
        self.box.config(state=NORMAL)
        self.box.insert(END,"\n" + message)
        self.lineCounter = self.lineCounter + 2
        
        #m = re.match("\[.*\] From .*\n", self.box.get("0.0", END))
        m = re.search("\[.*\].*:", message, re.MULTILINE)
        
        
        if m is not None:
            #print("MATCH")
            #print(m.group(0))
            #print(str(m.start(0)) + "_" + str(m.end(0)))
            #print("COUNTER")
            #print(str(self.lineCounter) + "." + str(m.start(0)+1) + "___" + str(self.lineCounter) + "." + str(m.end(0)))
            self.box.tag_add("header", str(self.lineCounter) + "." + str(m.start(0)), str(self.lineCounter) + "." + str(m.end(0)))
            self.box.tag_config("header", font=self.customFontHeader, foreground = "blue")
        
        
        self.box.config(state=DISABLED)
        #self.box.yview_scroll(10000,"units")
        self.box.see(END)

    
    def sendToServer(self, messageToSend):
        self.conn.send(messageToSend.encode(encoding='utf_8', errors='strict'))
    
    def sendFile(self):
        #aprire una dialog di quelle predefinite (Sfoglia...)
        #capire come fare la send di un file sul socket...
        pass
    def updateUsersFrame(self):
        
        global connectedClients
    
        self.userListbox.delete(0, END)
                    
        self.userListbox.insert(END, "Connected users")
        for item in connectedClients:
            self.userListbox.insert(END, item)
        #self.userListbox.update()
        #self.usersFrame.update()
    def privateChat(self, e):
        global conversationBoxList
        userselected = self.userListbox.selection_get()
        if not userselected == "Connected users":
            print("EVVAI CHAT PRIVATA con "+userselected)
            
            newWindow = Toplevel(self.parent)
            newWindow.title("Python Chat with "+userselected)
            newWindow.minsize(400, 475)
            newWindow.focus()
            
            def disconnectPM():
                del conversationBoxList[userselected]
                newWindow.destroy()
            newWindow.protocol('WM_DELETE_WINDOW', disconnectPM)
            
            #label = Label(newWindow, text="PROVA PROVA")
            #label.pack(side="top", fill="both", padx=10, pady=10)
            frame = Frame(newWindow)
            frame.pack(fill=BOTH, expand=1, side=LEFT)
            
            box = ScrolledText(frame, wrap=WORD, relief = GROOVE, width=30, height=18, font=self.customFontMessage)
            box.config(state=DISABLED)
            box.pack(expand="yes", fill=BOTH, side=TOP)
            
            textarea = Text(frame, width=30, height=5)
            textarea.bind("<KeyRelease-Return>", lambda event : self.getprivatetext(event, textarea, userselected)) 
            textarea.pack(expand="yes", fill=BOTH, side=TOP)
            
            #aggiungo alla mappa globale il box di conversazione
            conversationBoxList[userselected] = box
            

    def receivePrivateChat(self, connectingUser):
        global conversationBoxList
        print("CHAT PRIVATA in arrivo con "+connectingUser)
            
        newWindow = Toplevel(self.parent)
        newWindow.title("Python Chat requested by "+connectingUser)
        newWindow.minsize(400, 475)
        newWindow.focus()
        
        def disconnectPM():
            del conversationBoxList[connectingUser]
            newWindow.destroy()
        newWindow.protocol('WM_DELETE_WINDOW', disconnectPM)
        
        #label = Label(newWindow, text="PROVA PROVA")
        #label.pack(side="top", fill="both", padx=10, pady=10)
        frame = Frame(newWindow)
        frame.pack(fill=BOTH, expand=1, side=LEFT)
        
        box = ScrolledText(frame, wrap=WORD, relief = GROOVE, width=30, height=18, font=self.customFontMessage)
        box.config(state=DISABLED)
        box.pack(expand="yes", fill=BOTH, side=TOP)
        
        textarea = Text(frame, width=30, height=5)
        textarea.bind("<KeyRelease-Return>", lambda event : self.getprivatetext(event, textarea, connectingUser)) 
        textarea.pack(expand="yes", fill=BOTH, side=TOP)
        
        #aggiungo alla mappa globale il box di conversazione
        conversationBoxList[connectingUser] = box

    def getprivatetext(self, e, textarea, nickname):
            text = textarea.get("1.0", END + " - 2c") 
            textarea.delete("0.0", END) 
            self.sendToServer("##" + nickname + "##" + text)
    
    def setprivatetext(self, nickname, message, isLocalMessage):
        
            #isLocalMessage identifica un messaggio che mando io e che devo ri-ricevere nella mia finestra
            if isLocalMessage:
                for i in conversationBoxList.keys():
                    box = conversationBoxList[i]
                    box.config(state=NORMAL)
                    box.insert(END,"\n" + message)
                    box.config(state=DISABLED)
                    box.see(END)            
            else:
                conversationbox = conversationBoxList[nickname]
                
                conversationbox.config(state=NORMAL)
                conversationbox.insert(END,"\n" + message)
                #self.lineCounter = self.lineCounter + 2
                
                #m = re.match("\[.*\] From .*\n", self.box.get("0.0", END))
                #m = re.search("\[.*\].*:", message, re.MULTILINE)
                
                '''
                if m is not None:
                    #print("MATCH")
                    #print(m.group(0))
                    #print(str(m.start(0)) + "_" + str(m.end(0)))
                    #print("COUNTER")
                    #print(str(self.lineCounter) + "." + str(m.start(0)+1) + "___" + str(self.lineCounter) + "." + str(m.end(0)))
                    self.box.tag_add("header", str(self.lineCounter) + "." + str(m.start(0)), str(self.lineCounter) + "." + str(m.end(0)))
                    self.box.tag_config("header", font=self.customFontHeader, foreground = "blue")
                '''
                
                conversationbox.config(state=DISABLED)
                #self.box.yview_scroll(10000,"units")
                conversationbox.see(END)       
            
###############################################################################################################################################

def connectToChatServer(s, host, port, nickname):
    print("Connecting...")
    print("host: "+host)
    print("port: "+str(port))
    
    s.connect((host, port))
    print(s.recv(1024))
    s.send(nickname.encode(encoding='utf_8', errors='strict'))
    #s.close                     # Close the socket when done
    return s

def getSavedNickName(default):
    try:
        config_file = open("chat.conf", "r")
        for l in config_file.readlines():
            if re.match("NICKNAME=", l):
                nickname = re.sub("NICKNAME=", "", l)
                break
    except IOError:
        nickname = default
    return nickname

def getRemoteHost():
    config_file = open("chat.conf", "r")
    for l in config_file.readlines():
            if re.match("REMOTE_HOST=", l):
                remoteHost = re.sub("REMOTE_HOST=", "", l)
                break
    return remoteHost

def getNickname():
    localHost = socket.gethostname()
    #return get_display_name() + " - " + getSavedNickName(localHost)
    #return getSavedNickName(localHost)
    return "B1"

def initConnection():
    s = socket.socket()         # Create a socket object
    #remoteHost = socket.gethostname() # Get local machine name #FIXME DA CAMBIARE con l'host del server
    #port = 7777                # Reserve a port for your service.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    localHost = socket.gethostname()
    nickname = getNickname() #get_display_name() + " - " + getSavedNickName(localHost)
    completeRemoteHost = getRemoteHost()
    remoteHost = re.split(",", completeRemoteHost)[0]
    port = int(re.split(",", completeRemoteHost)[1])
    
    connectToChatServer(s, remoteHost, port, nickname)
    return s

def get_display_name():
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3
 
    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)
 
    nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(NameDisplay, nameBuffer, size)
    return nameBuffer.value

def main():
    
    print(get_display_name())
    sock = initConnection()
    
    root = Tk()
    root.minsize(400, 475)
    #root.geometry("400x250+450+200")
    app = ChatGUI(root, sock, "Python Chat")
    thread_receiver = receiveThread(1, "Receiver-Thread", sock, app)
    thread_receiver.start()
    
    #Qui gestisco eventuali connessioni per chat private
    
    
    root.mainloop()
    #thread_receiver._stop() #non necessario
    sock.send("QUIT".encode(encoding='utf_8', errors='strict'))
    sock.close()

if __name__ == '__main__':
    main()