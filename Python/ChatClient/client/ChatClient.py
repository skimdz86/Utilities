'''
Created on 02/feb/2014

@author: Marco
'''
import socket               # Import socket module
import threading
import re
import winsound

threads = []
stopClient = False

class receiveThread (threading.Thread):
    def __init__(self, threadID, name, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.conn = conn
    def run(self):
        global stopClient
        print("Starting receiver thread" + self.name)
        #print_time(self.name, self.counter, 5)
        try:
            while not stopClient:
                message = self.conn.recv(1024)
                if not message:
                    raise Exception
                if not message == "":
                    print(message.decode('utf-8'))
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS) #SystemHand / SystemExclamation 
        except Exception:
            print("Server disconnesso")
        print("Exiting receiver thread" + self.name)
        
class sendThread (threading.Thread):
    def __init__(self, threadID, name, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.conn = conn
    def run(self):
        global stopClient
        print("Starting sender thread" + self.name)
        #print_time(self.name, self.counter, 5)
        while not stopClient:
            messageToSend = input()
            if messageToSend == "QUIT":
                stopClient = True
            self.conn.send(messageToSend.encode(encoding='utf_8', errors='strict'))
        print("Exiting sender thread" + self.name)

def connectToChatServer(s, host, port, nickname):
    print("Connecting...")
    print("host: "+host)
    print("port: "+str(port))
    
    s.connect((host, port))
    print(s.recv(1024))
    s.send(nickname.encode(encoding='utf_8', errors='strict'))
    #s.close                     # Close the socket when done
    return s

def waitAndSend(conn):
    thread_receiver = receiveThread(1, "Receiver-Thread", conn)
    thread_sender = sendThread(2, "Sender-Thread", conn)
    threads.append(thread_receiver)
    threads.append(thread_sender)
    thread_receiver.start()
    thread_sender.start()

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
    
def main():
    s = socket.socket()         # Create a socket object
    #remoteHost = socket.gethostname() # Get local machine name #FIXME DA CAMBIARE con l'host del server
    #port = 7777                # Reserve a port for your service.
    
    localHost = socket.gethostname()
    nickname = getSavedNickName(localHost)
    completeRemoteHost = getRemoteHost()
    remoteHost = re.split(",", completeRemoteHost)[0]
    port = int(re.split(",", completeRemoteHost)[1])
    
    connectToChatServer(s, remoteHost, port, nickname)
    waitAndSend(s)
    # Wait for all threads to complete
    print("Waiting spawned threads")
    for t in threads:
        t.join()
    s.close()
    print("Exiting Main Thread")

#print(__name__)

if __name__ == '__main__':
    main()