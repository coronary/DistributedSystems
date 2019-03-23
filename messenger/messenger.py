import sys, getopt, socket, threading, os, time

def server(portNum):
    serverSocket = newSocket()
    serverSocket.bind(('', portNum))
    serverSocket.listen(1)
    (clientSocket, address) = serverSocket.accept()
    serverSocket.close()
    threading.Thread(target= sendMessage, args = [clientSocket]).start()
    threading.Thread(target= receiveMessage, args = [clientSocket]).start()


def client(portNum):
    time.sleep(.5)
    clientSocket = newSocket()
    clientSocket.connect(('localhost', portNum))
    threading.Thread(target= sendMessage, args = [clientSocket]).start()
    threading.Thread(target= receiveMessage, args = [clientSocket]).start()

def sendMessage(sock):
    outgoingMessage = sys.stdin.readline()
    while(outgoingMessage):
        try:
            sock.send(outgoingMessage.encode())
        except:
            print("Could not send message to user")
            break
        outgoingMessage = sys.stdin.readline()

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    os._exit(0)

def receiveMessage(sock):
    message = sock.recv(1024)
    while(message):
        print(message.decode()),# end="")
        message = sock.recv(1024)
    #print("Connection closed")
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    os._exit(0)

def newSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

def readArgs():
    args, extras = getopt.getopt(sys.argv[1:], 'l:')
    return (args, extras)

if __name__ == '__main__':
    args, extras = readArgs()
    if(len(args) < 1):
        portNum = extras[0]
        try:
            #in case user puts in address. Not used currently
            address = extras[1]
        except:
            pass
        client(int(portNum))
    elif(args[0][0] == "-l"):
        portNum = args[0][1]
        server(int(portNum))
