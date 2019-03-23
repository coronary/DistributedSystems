import sys, getopt, socket, threading, os, time
from random import randint

listOfSockets = {}
portBound = 0
fileOwnerResponse = 0

def server(portNum):
    serverSocket = newSocket()
    serverSocket.bind(('', portNum))
    serverSocket.listen(10)
    while True:
        (clientSocket, address) = serverSocket.accept()
        threading.Thread(target= receiveMessage, args = [clientSocket]).start()

def sendMessage(message, currentSock):
    for sock in listOfSockets:
        if (sock == currentSock):
            continue

        name = listOfSockets[sock]
        print("sending message to " + name)
        toSend = (listOfSockets[currentSock] + ": " + message)
        # if(tripped > 0):
        #     print("Sending portnumber " + p + " to requester of file " + currentSock)
        #     currentSock.send(("connec: " + p + " " + fileName).encode())
        #     continue

        # print ("Sending message to " + listOfSockets[socket])
        sock.send(toSend)

def findOwnerSocket(fileOwner):
    for sock in listOfSockets:
        if listOfSockets[sock] == fileOwner:
            return sock
    return None

def fileTransfer(requesterSocket, fileOwner, fileName):
    global fileOwnerResponse
    portNum = str(randint(portBound, 8000))
    request = ("server: " + portNum + " " + fileName )
    ownerSocket = findOwnerSocket(fileOwner)
    ownerSocket.send(request.encode())
    while(fileOwnerResponse == 0):
        print("Waiting on response from file owner")
        time.sleep(1)
    fileOwnerResponse = 0
    print("Received response from file owner")
    request = ("connec: " + portNum + " " + fileName)
    requesterSocket.send(request.encode())
    sys.exit()


def receiveMessage(sock):
    global fileOwnerResponse
    #sock.send("Input a user name: ".encode())
    message = sock.recv(1024)
    name = message.decode().strip()
    # print ("Received name from " + name)
    listOfSockets[sock] = name
    while(True):
        message = sock.recv(1024)
        if (not message):
            break
        decodedMsg = message.decode()
        decodedList = decodedMsg.split()
        # print(decodedList)
        if (decodedMsg.startswith("ready_to_connect")):
            fileOwnerResponse = 1
            continue
        if (decodedList[0] == "file_request"):
            fileOwner = decodedList[1]
            fileName = decodedList[2]
            threading.Thread(target= fileTransfer, args = [sock, fileOwner, fileName]).start()
            continue
        # print ("Received message from " + name)
        print("Received message from " + listOfSockets[sock])
        sendMessage(message.decode(), sock)
    # print("Connection closed by " + listOfSockets[sock])
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
    portNum = int(portNum)
    portBound = portNum+1
    server(portNum)
