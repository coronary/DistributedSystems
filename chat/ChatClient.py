import sys, getopt, socket, threading, os 

def client(portNum):
    clientSocket = newSocket()
    clientSocket.connect(('', portNum))
    threading.Thread(target= sendMessage, args = [clientSocket]).start()
    receiveMessage(clientSocket)

def sendMessage(sock):
    outgoingMessage = sys.stdin.readline()
    while(outgoingMessage):
        try:
            sock.send(outgoingMessage.encode())
        except:
            # print("Could not send message to server")
            break
        outgoingMessage = sys.stdin.readline()

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    os._exit(0)

def receiveMessage(sock):
    message = sock.recv(1024)
    while(message):
        print(message.decode(), end="")
        message = sock.recv(1024)
    #print("Connection closed")
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    os._exit(0)

def newSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

if __name__ == '__main__':
    args, extras = getopt.getopt(sys.argv[1:], '')
    portNum = extras[0]
    client(int(portNum))
