'''
Created on 06/feb/2014

@author: Marco
'''

from tkinter import Frame, Tk, BOTH, Button, RIGHT, BOTTOM, Text, Message, INSERT, END, TOP,\
    StringVar, CENTER, LEFT, X, scrolledtext, WORD, GROOVE, DISABLED, Label, Entry, RAISED, NORMAL
from tkinter.scrolledtext import ScrolledText
import socket
import re
import threading
import winsound
import traceback

class receiveThread (threading.Thread):
    def __init__(self, threadID, name, conn, guiWindow):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.conn = conn
        self.guiWindow = guiWindow
    def run(self):
        print("Starting receiver thread" + self.name)
        #print_time(self.name, self.counter, 5)
        try:
            while True:
                message = self.conn.recv(1024)
                #print("TEST: " + message.decode('utf-8'))
                if not message:
                    raise Exception
                if not message == "":
                    #print(message.decode('utf-8'))
                    self.guiWindow.printConversation(message.decode('utf-8'))
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS) #SystemHand / SystemExclamation 
        except Exception:
            print(traceback.format_exc())
            print("Server disconnesso")
        print("Exiting receiver thread" + self.name)

class ChatGUI(Frame):
  
    def __init__(self, parent, conn):
        #Frame.__init__(self, parent, background="grey")   
         
        self.parent = parent
        self.conn = conn
        
        self.centerWindow()
        self.initUI()
    
    def initUI(self):
      
        #mettere qui tutta l'inizializzazione dei frame anche
        #direi 2 frame, uno left e uno right
      
        self.parent.title("Python Chat") 
        
        frame = Frame(self.parent)
        frame.pack(fill=BOTH, expand=1, side=LEFT)
        
        self.box = ScrolledText(frame, wrap=WORD, relief = GROOVE, width=1, height=20)
        self.box.insert(END, 'Welcome to Python Chat!')
        self.box.config(state=DISABLED)
        self.box.pack(expand="yes", fill=BOTH, side=TOP)
        
        self.textarea = Text(frame, width=1, height=5)
        #self.textarea.insert(END, "")
        self.textarea.bind("<KeyRelease-Return>", self.gettext) #Se metto on press, rimane una newline in piu
        self.textarea.pack(expand="yes", fill=BOTH, side=TOP)

        
        okButton = Button(frame, text="Attach file", activebackground="green", command=self.sendFile) 
        okButton.pack(expand="no", fill=BOTH, side=TOP)
        
        
        #per gestire invio con la newline --> http://userpages.umbc.edu/~dhood2/courses/cmsc433/spring2010/?section=Notes&topic=Python&notes=93
        
        #usersFrame = Frame(self.parent)
        #usersFrame.pack(fill=BOTH, expand=1, side=RIGHT)
    
    def centerWindow(self):
      
        w = 600
        h = 450

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
        
        #aggiungo colorazione parte di testo --> troppo complesso per ora
        ''''m = re.search("", message)
        lastIndex = len(m.group(0))
        self.box.tag_add("header", m.start(), m.stop())
        self.box.tag_config("header", foreground="green")
        '''
        self.box.config(state=DISABLED)
        #self.box.yview_scroll(10000,"units")
        self.box.see(END)

    
    def sendToServer(self, messageToSend):
        self.conn.send(messageToSend.encode(encoding='utf_8', errors='strict'))
    
    def sendFile(self):
        #aprire una dialog di quelle predefinite (Sfoglia...)
        #capire come fare la send di un file sul socket...
        pass


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


def initConnection():
    s = socket.socket()         # Create a socket object
    #remoteHost = socket.gethostname() # Get local machine name #FIXME DA CAMBIARE con l'host del server
    #port = 7777                # Reserve a port for your service.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    localHost = socket.gethostname()
    nickname = getSavedNickName(localHost)
    completeRemoteHost = getRemoteHost()
    remoteHost = re.split(",", completeRemoteHost)[0]
    port = int(re.split(",", completeRemoteHost)[1])
    
    connectToChatServer(s, remoteHost, port, nickname)
    return s

def main():
  
    sock = initConnection()
    
    root = Tk()
    root.minsize(400, 450)
    #root.geometry("400x250+450+200")
    #root.call('wm', 'attributes', '.', '-topmost', '1')
    app = ChatGUI(root, sock)
    thread_receiver = receiveThread(1, "Receiver-Thread", sock, app)
    thread_receiver.start()
    root.mainloop()
    #thread_receiver._stop() #non necessario
    sock.send("QUIT".encode(encoding='utf_8', errors='strict'))
    sock.close()

if __name__ == '__main__':
    main()