'''
Created on 02/feb/2014

@author: Marco
'''

import socket
import threading
import time

stopServer = False
connectedClients = []
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
    host = socket.gethostname()
    print("TIMEOUT: " + str(socket.getdefaulttimeout()))
    print("SERVER HOSTNAME: "+host)
    reservedPort = 7777
    serverSocket.bind((host, reservedPort))
    serverSocket.listen(maxConnections)
    
    threadCounter = 0
    
    while not stopServer:
        c, addr = serverSocket.accept()     # Establish connection with client.
        print("Got connection from", addr)
        c.send("Thank you for connecting".encode(encoding='utf_8', errors='strict'))
        nick = c.recv(1024).decode('utf-8')
        #c.close()                # Close the connection
        connectedClients.append(addr)
        connections.append(c)
        cliConn = ClientConnection(c, nick, addr)
        clientConnections[addr] = cliConn
        threadCounter = threadCounter +1
        thread_x = clientThread(threadCounter, addr, nick, c)
        threads.append(thread_x)
        thread_x.start()
        #c.send(tutta la lista dei client)

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
        print("Starting client thread" + self.name)
        #print_time(self.name, self.counter, 5)
        try:
            while True:
                message = self.conn.recv(1024)
                decodedMessage = message.decode('utf-8')
                #print("Message to broadcast: " + decodedMessage)
                if decodedMessage != "":
                    clientToRemove = []
                    for k in clientConnections.keys():
                        client = clientConnections[k]
                        send_conn = client.connection
                        try:
                            if decodedMessage == "QUIT":
                                send_conn.send(("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] "+self.nickname+" si \xe8 disconnesso ").encode(encoding='utf_8', errors='strict'))
                            elif decodedMessage == "HELP":
                                send_conn.send(("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] Type QUIT to exit ").encode(encoding='utf_8', errors='strict'))
                            else:
                                if client.nickname != self.nickname: #FIXME: SOLO per quella testuale; per la GUI dovranno ricevere sempre tutto
                                    send_conn.send(("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] From "+self.nickname+": "+decodedMessage).encode(encoding='utf_8', errors='strict'))
                        except (ConnectionAbortedError,ConnectionResetError) as ex1:
                            #rimuovere dalla lista --> usare un dictionary
                            clientToRemove.append(client.address)
                        
                    for rem in clientToRemove:
                        del clientConnections[rem]
                    
        except (ConnectionAbortedError,ConnectionResetError) as ex2:
            print("Client disconnected")
        print("Exiting client thread" + self.name)

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