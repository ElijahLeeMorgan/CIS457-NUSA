from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from time import sleep

# Me when the multi-thread :O

#def someWork(val):
#    for k in range(20):
#        print(f"In function {x}")
#        sleep(0.4)   # 400 milliseconds
#
#t1 = Thread(target = someWork, args=(51,))
#t1.start()
#for m in range(20):
#    print(f"In Main {m}")
#    sleep(0.25)   # 250 milliseconds

'''
C: (Initiate connection)
                                   S: (Accept connection request)
                                   S: 220 nusa.foo.net
C: EHLO nusa.foo.net
                                   S: 502 OK
C: HELO nusa.foo.net
                                   S: 250 OK
C: MAIL FROM:<me@foo.net>
                                   S: 250 OK
C: RCPT TO:<you@mail.app>
                                   S: 250 OK
C: DATA
                                   S: 354 OK
C: Message-ID: 7123-dd-fc62
Date: Thu, 16 May 2024 10:22:37 -0500
To: you@mail.app
From: Mason Engelberg <me@foo.net>
Subject: Breaking News
Content-Transfer-Encoding: 7bit
Content-Language: en-US

Have you heard about NUSA? An email server which will never
fill up your mailbox?
.
                                   S: 250 OK
C: QUIT
                                   S: 221 OK


Message is really sent like this (bytecode)
Message-ID: 7123-dd-fc62\r\nDate: Thu, 16 May 2024
 10:22:37 -0500\r\nTo: you@mail.app\r\nFrom: Mason
 Engelberg <me@foo.net>\r\nSubject: Breaking News\r
\nContent-Transfer-Encoding: 7bit\r\nContent-Langu
age: en-US\r\n\r\nHave you heard about NUSA? An em
ail server which will never fill up your mailbox?\r
\n.\r\n
'''

class connectionState(Enum):
    INIT = 0
    HELO = 1
    #EHLO = # I'm assuming we're not worried about extended SMTP. Maybe I add more cases later
    MAIL = 2
    RCPT = 3
    DATA = 4
    QUIT = 5


def recieveClientdata(clientSocket) -> tuple[bytearray]:
    clientSocket.sendall(b"220 localhost NUSA\r\n")
    body = bytearray()
    state = connectionState.INIT

    while True:
        match state:
            case connectionState.INIT:
                ...
            case connectionState.EHLO:
                ...
            case connectionState.HELO:
                ...
            case connectionState.MAIL:
                ...
            case connectionState.RCPT:
                ...
            case connectionState.DATA:
                ...
            case connectionState.QUIT:
                break
    


# NOTE Remember, all sent mail just goes to /dev/null
# NUSA: NUll Submission Agent

def main():
    # Create a TCP socket that listens to port 9000 on the local host
    welcomeSocket = socket(AF_INET, SOCK_STREAM) 
    welcomeSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # As per professor's suggestion
    welcomeSocket.bind(("", 9000))
    welcomeSocket.listen(4)    # Max backlog 4 connections
    bytesRecieved = 0
    data = bytearray()

    # Args must be a list
    print ('Server is listening on port 9000')
    connectionSocket, addr = welcomeSocket.accept()
    print ("Accept a new connection", addr)

    connectionData = Thread(target = recieveClientdata, args=(connectionSocket,))
    connectionData.start()

    # decode(): converts bytes to text
    # encode(): convert text to bytes

    text = data.decode() # Recieves data in Kilobytes
    print (f"Incoming text is {text}")
    connectionSocket.sendall("This is a sample text".encode())
    connectionSocket.close()

    welcomeSocket.close()
    print("End of server")

if __name__ == "__main__":
    main()