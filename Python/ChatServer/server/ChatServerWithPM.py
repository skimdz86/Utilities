'''
Created on 02/feb/2014

@author: Marco
'''

import socket
import threading
import time
import traceback
import re

stopServer = False
connectedClients = []
nickList = []
connections = []
threads = []

clientConnections = dict()

class ClientConnection:
    connection = None
    nickname = ""
    address = ""
    
    def __init__(self, connection, nickname, address):
        self.connection = connection
        self.nickname = nickname
        self.address = address

def startServer(maxConnections):
    serverSocket = socket.socket()
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    host = socket.gethostname()
    print("TIMEOUT: " + str(socket.getdefaulttimeout()))
    print("SERVER HOSTNAME: "+host)
    reservedPort = 7777
    serverSocket.bind((host, reservedPort))
    serverSocket.listen(maxConnections)
    
    threadCounter = 0
    
    while not stopServer:
        c, addr = serverSocket.accept()     # Establish connection with client.
        print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] Got connection from", addr)
        c.send("Thank you for connecting".encode(encoding='utf_8', errors='strict'))
        nick = c.recv(1024).decode('utf-8')
        print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] Nickname selected", nick)
        if nickList.count(nick) > 0:
            c.send(("Nickame " + nick +" already exists! Bye bye").encode(encoding='utf_8', errors='strict'))
            continue
        #c.close()                # Close the connection
        connectedClients.append(addr)
        nickList.append(nick)
        connections.append(c)
        cliConn = ClientConnection(c, nick, addr)
        clientConnections[addr] = cliConn
        
        #INVIO LISTA NICK CONNESSI#
        #print("USER LIST: "+userListToString(nickList))
        for cc in clientConnections.keys():
            send_conn = clientConnections[cc].connection
            send_conn.send(userListToString(nickList).encode(encoding='utf_8', errors='strict'))
        
        threadCounter = threadCounter +1
        thread_x = clientThread(threadCounter, addr, nick, c)
        threads.append(thread_x)
        thread_x.start()
        

#def stopServerThread():
#    while True:
#        myStr = input()
#        if myStr == "STOP":
#            stopServer = True
#            _thread.exit()
#        time.sleep(1)



class clientThread (threading.Thread):
    def __init__(self, threadID, name, nickname, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.conn = conn
        self.nickname = nickname
    def run(self):
        print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] Starting client thread" + self.name)
        #print_time(self.name, self.counter, 5)
        try:
            while True:
                message = self.conn.recv(1024)
                decodedMessage = message.decode('utf-8')
                #print("Message to broadcast: #" + decodedMessage + "#")
                if decodedMessage != "":
                    clientToRemove = []
                    for k in clientConnections.keys():
                        client = clientConnections[k]
                        send_conn = client.connection
                        try:
                            if decodedMessage == "QUIT":
                                send_conn.send(("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] "+self.nickname+" si \xe8 disconnesso \n ").encode(encoding='utf_8', errors='strict'))
                            elif decodedMessage == "HELP":
                                send_conn.send(("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] Type QUIT to exit ").encode(encoding='utf_8', errors='strict'))
                            else:
                                m = re.match("^##.*##", decodedMessage)
                                if m is not None:
                                    currentUser = re.sub("##", "", m.group(0))
                                    privateMessage = re.sub("##.*##", "##" + self.nickname + "##", decodedMessage) #PER ORA reinvio con la stringa speciale per PM
                                    print("current user: "+currentUser)
                                    print("PM: "+privateMessage)
                                    if client.nickname == currentUser or client.nickname == self.nickname:
                                        print("MATCH PM")
                                        send_conn.send(("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] From "+self.nickname+": \n  "+privateMessage).encode(encoding='utf_8', errors='strict'))
                                else:
                                    send_conn.send(("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] From "+self.nickname+": \n  "+decodedMessage).encode(encoding='utf_8', errors='strict'))
                        except (ConnectionAbortedError,ConnectionResetError) as ex1:
                            print(traceback.format_exc())
                            #rimuovere dalla lista --> usare un dictionary
                            clientToRemove.append(client.address)
                        
                    for rem in clientToRemove:
                        nickToRemove = clientConnections[rem].nickname
                        del clientConnections[rem]
                        nickList.remove(nickToRemove)
                        #INVIO LISTA AGGIORNATA NICK CONNESSI#
                        for k in clientConnections.keys():
                            #print("USER LIST for a client: "+userListToString(nickList))
                            client = clientConnections[k]
                            send_conn = client.connection
                            send_conn.send(userListToString(nickList).encode(encoding='utf_8', errors='strict'))
                    
                    #if decodedMessage == "QUIT":
                    #    self.conn.close()
                    #    raise ConnectionAbortedError
                    
        except (ConnectionAbortedError,ConnectionResetError) as ex2:
            print(traceback.format_exc())
            print("Client " + self.name + "disconnected")
        print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] Exiting client thread" + self.name)

def userListToString(mylist):
    userListString = "USER_SYNC-"
    for user in mylist:
        userListString = userListString + "," + user
    return userListString

def main():
    #try:
    #    _thread.start_new_thread(stopServerThread, ())
    #except:
    #    print("Unable to start thread")
    startServer(5)
    # Wait for all threads to complete
    #for t in threads:
    #    t.join()
    print("Exiting Main Thread")
    stopServer = True

if __name__ == '__main__':
    print("Start program")
    main()
    print("End program")