from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from time import sleep

# Me when multi-threading :O
#def someWork(val):
#    for k in range(20):
#        print(f"In function {x}")
#        sleep(0.4)   # 400 milliseconds

# NOTE Remember, all sent mail just goes to /dev/null
# NUSA: NUll Submission Agent
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

def main():
    # Create a TCP socket that listens to port 9000 on the local host
    welcomeSocket = socket(AF_INET, SOCK_STREAM) 
    welcomeSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # As per professor's suggestion
    welcomeSocket.bind(("", 9000))
    welcomeSocket.listen(4)    # Max backlog 4 connections
    
    # NOTE Multithreading sample.
    #t1 = Thread(target = someWork, args=(51,))
    #t1.start()
    #for m in range(20):
    #    print(f"In Main {m}")
    #    sleep(0.25)   # 250 milliseconds

    # Args must be a list
    print ('Server is listening on port 9000')
    connectionSocket, addr = welcomeSocket.accept()
    print ("Accept a new connection", addr)

    # Read AT MOST 1024 bytes from the socket
    # decode(): converts bytes to text
    # encode(): convert text to bytes
    text = connectionSocket.recv(1024).decode()
    print (f"Incoming text is {text}")
    connectionSocket.sendall("This is a sample text".encode())
    connectionSocket.close()

    welcomeSocket.close()
    print("End of server")

if __name__ == "__main__":
    main()