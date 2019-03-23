import sys, getopt, socket, threading, os, time, struct

clientOffset = 1
serverOffset = 2
name = ''

def input():
    return sys.stdin.readline()

def menu(sock, listenPort):
    # print("in Menu")
    while(True):
        print("Enter an option ('m', 'f, 'x):")
        print("(M)essage (send)\n(F)ile (request)\ne(X)it")
        option = (input()).strip().lower()
        if (option == ('x')):
            shutdown(sock)
        elif(option == 'm'):
            sendMessage(sock)
        elif(option == 'f'):
            requestFile(listenPort)

def shutdown(sock):
    print("closing your sockets...goodbye")
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    os._exit(0)

# def requestConnect(portNum):
#     sock = newSocket()
#     sock.connect(('', portNum+1))
#     return sock

def requestFile(portNum):
    if (name == "client"):
        offset = serverOffset
    elif (name == "server"):
        offset = clientOffset
    print("Which file do you want?")
    fileName = input().rstrip('\n')
    sock = newSocket()
    sock.connect(('', portNum+offset))
    sock.send(fileName.encode())
    file_size_bytes = sock.recv( 4 )
    if file_size_bytes:
        file = open(fileName, 'wb')
        file_size = struct.unpack( '!L', file_size_bytes[:4] )[0]
        # print(file_size)
        #CAN GET FILE SIZE BUT NOT BYTES
        if (file_size > 0):
            while True:
                file_bytes = sock.recv(1024)
                if file_bytes:
                    file.write(file_bytes)
                else:
                    break
        else:
            print( 'File does not exist or is empty' )
    file.close()
    # sock.close()
    os._exit(0)

def no_file( sock ):
    zero_bytes= struct.pack( '!L', 0 )
    sock.send( zero_bytes )

def waitForFile(sock):
    file_name = sock.recv(1024).decode()
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
    sock.close()

def sendFile(sock, file_size, file):
    print( 'File size is ' + str(file_size) )
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
    sock.close()
    os._exit(0)

def fileServer(connectPort):
    if (name == "client"):
        offset = clientOffset
    elif (name == "server"):
        offset = serverOffset
    # print("In the File Server")
    serverSocket = newSocket()
    serverSocket.bind(('', connectPort+offset))
    serverSocket.listen(3)
    while(True):
        # print("waiting.....")
        (clientSocket, address) = serverSocket.accept()
        # print("socket connected")
        threading.Thread(target= waitForFile, args = [clientSocket]).start()


def server(listenPort, address):
    serverSocket = newSocket()
    serverSocket.bind((address, listenPort))
    serverSocket.listen(5)
    (clientSocket, address) = serverSocket.accept()
    serverSocket.close()
    threading.Thread(target= menu, args = [clientSocket, listenPort]).start()
    threading.Thread(target= fileServer, args = [listenPort]).start()
    receiveMessage(clientSocket)


def client(connectPort, address):
    # time.sleep(.5)
    clientSocket = newSocket()
    clientSocket.connect((address, connectPort))
    # print("FHDSJLKFHDLKSHFLDKSHFLKDSHFLKD")
    threading.Thread(target= fileServer, args = [connectPort]).start()
    threading.Thread(target= menu, args = [clientSocket, connectPort]).start()
    receiveMessage(clientSocket)

def sendMessage(sock):
    outgoingMessage = input()
    try:
        sock.send(outgoingMessage.encode())
    except:
        print("Could not send message to user")

def receiveMessage(sock):
    # print("in receive")
    message = sock.recv(1024)
    while(message):
        print(message.decode()),# end="")
        message = sock.recv(1024)
    #print("Connection closed")
    print("Shutting shit down")
    shutdown(sock)

def newSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

def readArgs():
    args, extras = getopt.getopt(sys.argv[1:], 'l:p:s:')
    return (args, extras)

if __name__ == '__main__':
    print("hello")
    args, extras = readArgs()
    flags = {}
    for arg in args:
        if (arg[0] == '-l'):
            flags["listenPort"] = int(arg[1])
        if (arg[0] == '-p'):
            flags["connectPort"] = int(arg[1])
        if (arg[0] == '-s'):
            flags["address"] = int(arg[1])
    if("address" not in flags.keys()):
        flags["address"] = "localhost"
    if (len(args) > 1):
        # print("client")
        name = "client"
        #use as client
        client(flags["connectPort"], flags["address"])
    elif (len(args) == 1):
        # print("server")
        name = "server"
        server(flags["listenPort"], flags["address"])
    # if(len(args) < 1):
    #     portNum = extras[0]
    #     try:
    #         #in case user puts in address. Not used currently
    #         address = extras[1]
    #     except:
    #         pass
    #     client(int(portNum))
    # elif(args[0][0] == "-l"):
    #     portNum = args[0][1]
    #     server(int(portNum))
