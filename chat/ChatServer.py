import sys, getopt, socket, threading, os

listOfSockets = {}

def server(portNum):
    serverSocket = newSocket()
    serverSocket.bind(('', portNum))
    serverSocket.listen(10)
    while True:
        (clientSocket, address) = serverSocket.accept()
        threading.Thread(target= receiveMessage, args = [clientSocket]).start()

def sendMessage(message, currentSock):
    for socket in listOfSockets:
        if (socket == currentSock):
            continue
        #print ("Sending message to " + listOfSockets[socket])
        toSend = (listOfSockets[currentSock] + ": " + message).encode()
        socket.send(toSend)

def receiveMessage(sock):
    #sock.send("Input a user name: ".encode())
    message = sock.recv(1024)
    name = message.decode().strip()
    #print ("Received name from " + name)
    listOfSockets[sock] = name
    while(True):
        message = sock.recv(1024)
        if (not message):
            break
    #    print ("Received message from " + name)
        sendMessage(message.decode(), sock)
    #print("Connection closed by " + listOfSockets[sock])
    del listOfSockets[sock]
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    # if (len(listOfSockets) < 1):
    #     os._exit(0)
    # else:
    sys.exit()


def newSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

if __name__ == '__main__':
    args, extras = getopt.getopt(sys.argv[1:], '')
    try:
        portNum = extras[0]
    except:
        print("Please try again with a port number\nProgram terminated")
        os._exit(0)
    server(int(portNum))
