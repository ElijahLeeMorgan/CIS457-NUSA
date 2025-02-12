from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from time import sleep
from re import search, sub
'''
NUSA: NUll Submission Agent
Elijah Morgan
CIS 457 02
'''

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
def getSeperatorBar() -> str:
    # Used for cleaner formatting. Better practice would be to override print function in a class. Too lazy though.
    return f"\n{'=' * 100}\n\n"

def emailClean(emailBytes:bytearray) -> str:
    return sub("[<>:]", '', emailBytes.decode()).strip()

def emailVerify(email:str) -> str:
    # Validate email characters, format, and number of @ symbols.
    # Borrowed from: https://formulashq.com/the-ultimate-guide-to-regex-for-alphanumeric-characters/#10
    validChars = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    validTLDs = "\.(com|org|net|edu|io|app)$"

    # This could be done with one giant regular expression, but who wants to debug that?
    # Plus, this means I can have seprate error messages.
    #print("Validating email: ", email.encode())

    if search("^@.*", email):
        return "550 Empty username"
    if search("@\..*$", email):
        return "550 Empty domain"
    if search("\.$", email):
        return "550 Empty TLD"
    if not search(validChars, email):
        return "550 Invalid email address"

    # Validates accepted TLDs
    if not search(validTLDs, email):
        return "550 Unknown TLD"
    
    return "250 OK"

def returnMsg(clientSocket:socket, message:str) -> None:
    print("Sending message:\t", message)
    clientSocket.sendall(f"{message}\r\n".encode())

def recieveClientdata(clientSocket) -> str:
    seperatorBar = getSeperatorBar()
    
    print("INIT TCP Exchange\n", seperatorBar)
    returnMsg(clientSocket, "220 localhost")

    sender = ""
    recipients = []
    email = ""

    while True:
        # Recieve data in kilobytes, if no data break loop.
        data = clientSocket.recv(1024)
        state = data[:4]

        #Debugging
        print("Incoming Command:\t", state.decode())

        match state:
            case b"EHLO": # Working
                # Reject EHLO, only accept HELO
                returnMsg(clientSocket, "502 OK")
            case b"HELO": # Working
                returnMsg(clientSocket, "250 OK")
            case b"MAIL": # working
                # Extract sender
                #NOTE Assumes that response starts with "MAIL FROM:"
                sender = emailClean(data[9:])
                returnMsg(clientSocket, "250 OK")
            case b"RCPT":
                # Extract recipient
                #NOTE Assumes that response starts with "RCPT TO:"
                #print("Uncleaned Recipient: ", data[7:])
                recipient = emailClean(data[7:])
                print("Recipient:\t\t", recipient) # Cleaned email

                returnCode = emailVerify(recipient)
                if returnCode == "250 OK":
                    # Add recipient to list, normal behavior.
                    recipients.append(recipient)
                
                if len(recipients) > 5:
                    # As per project guidelines, reject any more than 5 recipients.
                    returnCode = "550 Too many recipients"

                returnMsg(clientSocket, returnCode)
            case b"DATA":
                returnMsg(clientSocket, "354 Start mail input")
                # Extract headers and message
                data = clientSocket.recv(1024)
                timeout = 0
                while b"\r\n.\r\n" not in data:
                    email += data.decode()
                    data += clientSocket.recv(1024)
                
                
                print(seperatorBar, email, seperatorBar)
                
                # Check for an empty subject. RFC5321
                if b"Subject:" not in data:
                    returnMsg(clientSocket, "451 Empty subject")
                else:
                    returnMsg(clientSocket, "250 OK")
            case b"QUIT":
                returnMsg(clientSocket, "221 Goodbye")
                clientSocket.close()
                return sender, recipients, email
            case _:
                print("Unknown Command")
                returnMsg(clientSocket, "500 Unknown command")
    return sender, recipients, email
        
def thread_target(clientSocket, result):
    result.append(recieveClientdata(clientSocket))

def main():
    # Create a TCP socket that listens to port 9000 on the local host
    welcomeSocket = socket(AF_INET, SOCK_STREAM) 
    welcomeSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # As per professor's suggestion
    welcomeSocket.bind(("", 9000))
    welcomeSocket.listen(4)    # Max backlog 4 connections

    print('Server is listening on port 9000')

    threads = []

    while True:
        connectionSocket, addr = welcomeSocket.accept()
        print(getSeperatorBar(), f"Accept a new connection at {addr[0]}:{addr[1]}")

        connectionData = Thread(target=thread_target, args=(connectionSocket, []))
        connectionData.start()
        threads.append(connectionData)

        # Clean up finished threads
        threads = [t for t in threads if t.is_alive()]

    welcomeSocket.close()
    print("End of server")

if __name__ == "__main__":
    main()