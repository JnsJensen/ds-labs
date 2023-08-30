"""
TASK 1: Simple server and client

Implement a socket server in Python, that listens on TCP port 9000 locally for incoming
connections. When a connection is established, print the remote address to the terminal
window and close the socket.

Write a simple client program that connects to the server and print a status message to
the terminal every time when the user hits the Enter key.

Both the server and client should run indefinitely until the user terminates the program
manually (Ctrl+C).

Notice that the server does not do anything with the received data, and does not send
anything back.

Test the communication by hitting Enter in the client a few times, and verify that you
see the intended console messages in both terminal windows.

TASK 2: Multithreaded server

Modify the server code to start a new background thread for each new incoming
connection, and handle it there.

Note:
The threading python package overlaps execution of the logical threads in a single
physical thread. Real parallel execution can be implemented using the multiprocessing
package, which starts a new process and runs a piece of code there. However, a new
process has a lot higher overhead than a new thread. So much that it's not acceptable
when serving small HTTP requests.

TASK 3: Welcome message
Extend the client to read a string from the standard input, and send that to the server.
Limit the string size to 4kB (just drop the rest).

Extend the server to convert the received bytes to string and write it to the console,
together with the remote IP address. The server should respond by
“Message: {received message}“.

TASK 4: Different message types

Define a message format where you have 2 message types.
1. Send a short variable length string, up to 4 kB
2. Send arbitrary size binary data (e.g. file contents).

The client should first ask the user which type of message they want to send. If string
type was selected, read the string from the input and send it to the server in a #1 type
message. If binary type was selected, generate a random byte array and send that to the
server as a #2 type message. The client should write what happened to the console. Keep
doing this until the user exits the program (e.g. after sending the message, the client
should again ask the user what message type to send). Close the connection after each
message.

Extend the server to parse the received message, and handle it according to the message
type. If a string was received, print it to the console. If binary data was sent by the
client, store it as a file with a random generated filename.

THIS IS THE CLIENT
"""

import socket
from termcolor import colored, cprint
import os

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9000  # The port used by the server


# class enum for message types
class MessageType:
    STRING = 1
    BINARY = 2


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Ask which message type to send
        message_type = input(
            colored("Enter message type (1 = string, 2 = binary): ", attrs=["bold"])
        )

        if message_type == "1":
            # read a string from the standard input
            data = input(colored("Enter a string: ", attrs=["bold"]))
            # convert the string to bytes and limit the size to 4kB
            data = data.encode("utf-8")[:4096]
        elif message_type == "2":
            # generate a random byte array
            data = os.urandom(4096)
            # overwrite start byte to
        else:
            # invalid message type
            cprint("Invalid message type", "red")
            continue
        # # read a string from the standard input
        # data = input(colored("Enter a string: ", attrs=["bold"]))
        # # convert the string to bytes and limit the size to 4kB
        # data = data.encode("utf-8")[:4096]

        # connect to the server
        s.connect((HOST, PORT))
        # print a status
        cprint(f"Connected to {HOST}:{PORT}", "green")

        # send some data
        cprint(f"Sending a message of type {message_type}", "blue")
        s.sendall(data)

        # closing the connection
        cprint("Closing the connection", "red")
        s.close()
