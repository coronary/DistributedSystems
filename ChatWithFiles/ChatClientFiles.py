import sys, getopt, socket, threading, os, time, struct

def client(portNum):
    clientSocket = newSocket()
    clientSocket.connect(('localhost', portNum))
    threading.Thread(target= menu, args = [clientSocket]).start()
    receiveMessage(clientSocket)

def fileServer(listenPort, fileName, readySocket):
    readyMsg = "ready_to_connect".encode()
    serverSocket = newSocket()
    serverSocket.bind(('', listenPort))
    serverSocket.listen(1)
    readySocket.send(readyMsg)
    (clientSocket, address) = serverSocket.accept()
    # print("connected")
    # print("connection to requester complete")
    # threading.Thread(target= waitForFile, args = [clientSocket]).start()
    waitForFileName(clientSocket, fileName)


def no_file( sock ):
    zero_bytes= struct.pack( '!L', 0 )
    sock.send( zero_bytes )

def sendFile(sock, file_size, file):
    # print( 'File size is ' + str(file_size) )
    file_size_bytes = struct.pack( '!L', file_size )
    # send the number of bytes in the file
    sock.send( file_size_bytes )
    # read the file and transmit its contents
    while True:
        file_bytes= file.read( 1024 )
        # print("read file correctly")
        if file_bytes:
            sock.send( file_bytes )
        else:
            # print("shit broke")
            break
    file.close()
    sock.shutdown(socket.SHUT_RDWR)
    # sock.close()
    # shutdown(sock)
    sys.exit()

def input():
    return sys.stdin.readline()

def shutdown(sock):
    # print("closing your sockets...goodbye")
    sock.shutdown(socket.SHUT_RDWR)
    # sock.close()
    # os._exit(0)
    sys.exit()

def menu(sock):
    # print("in Menu")
    sendMessage(sock, "")
    while(True):
        print("Enter an option ('m', 'f, 'x):")
        print("(M)essage (send)\n(F)ile (request)\ne(X)it")
        option = (input()).strip().lower()
        if (option == ('x')):
            shutdown(sock)
        elif(option == 'm'):
            sendMessage(sock,"")
        elif(option == 'f'):
            sendMessage(sock,"anything")

def fileR():
    print("Who has the file?")
    owner = input()
    print("What file do you want?")
    fileName = input().strip('\n')
    outgoingMessage = "file_request " + owner + fileName


# def sendMessage(sock):
#     outgoingMessage = sys.stdin.readline()
#     while(outgoingMessage):
#         try:
#             sock.send(outgoingMessage.encode())
#         except:
#             # print("Could not send message to server")
#             break
#         outgoingMessage = sys.stdin.readline()
#
#     sock.shutdown(socket.SHUT_RDWR)
#     sock.close()
#     os._exit(0)
def getFile(connectPort, fileName):
    # print("check")
    time.sleep(1)
    # print("in get file " + str(connectPort))
    fileSocket = newSocket()
    try:
        fileSocket.connect(('localhost', connectPort))
    except Exception as e:
        print(e)
        print("fuck")
        # sys.exit()
    file_size_bytes = fileSocket.recv( 4 )
    if file_size_bytes:
        file = open(fileName, 'wb')
        file_size = struct.unpack( '!L', file_size_bytes[:4] )[0]
        # print(file_size)
        if (file_size > 0):
            while True:
                file_bytes = fileSocket.recv(1024)
                if file_bytes:
                    # print("writing bytes")
                    file.write(file_bytes)
                else:
                    break
        else:
            print( 'File does not exist or is empty' )
    # print("we done here")
    file.close()
    fileSocket.shutdown(socket.SHUT_RDWR)
    # fileSocket.close()
    # shutdown(fileSocket)
    sys.exit()

def waitForFileName(sock, file_name):
    # print("waiting for filename")
    # file_name = (sock.recv(1024)).decode()
    # print(file_name)
    # print(file_name + " we got it boss")
    try:
        file_stat= os.stat( file_name )
        # print("file found")
        if file_stat.st_size:
            # print("size exists")
            file= open( file_name, 'rb' )
            sendFile( sock, file_stat.st_size, file )
        else:
            # print("first No file")
            no_file( sock )
    except OSError:
        # print("exception no file")
        no_file(sock)

def receiveMessage(sock):
    message = sock.recv(1024)
    while(message):
        m = message.decode()
        listOfMessage = m.split()
        if(m.startswith("server")):
            # print("starting fileserver thread")
            #list splice to only get the port number
            # print(listOfMessage)
            portNum = int(listOfMessage[1])
            fileName = listOfMessage[2].strip()
            threading.Thread(target= fileServer, args = [portNum, fileName, sock]).start()
        elif(m.startswith("connec")):
            # print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
            portNum = int(listOfMessage[1])
            # print(portNum)
            fileName = listOfMessage[2]
            threading.Thread(target= getFile, args = [portNum, fileName]).start()
        else:
            print(m),# end="")
        message = sock.recv(1024)
    #print("Connection closed")
    sock.shutdown(socket.SHUT_RDWR)
    # sock.close()
    # shutdown(sock)
    sys.exit()

def newSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

if __name__ == '__main__':
    args, extras = getopt.getopt(sys.argv[1:], 'l:p:')
    portNum = args[1][1]
    print(portNum)
    client(int(portNum))
