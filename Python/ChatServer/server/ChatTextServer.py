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
                print("Message to broadcast: " + decodedMessage)
                clientToRemove = []
                for k in clientConnections.keys():
                    client = clientConnections[k]
                    send_conn = client.connection
                    try:
                        send_conn.send(("From "+self.nickname+": "+decodedMessage).encode(encoding='utf_8', errors='strict'))
                    except ConnectionAbortedError:
                        #rimuovere dalla lista --> usare un dictionary
                        clientToRemove.append(client)
                    
                for rem in clientToRemove:
                    clientConnections.remove(rem)
                    
        except ConnectionAbortedError:
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