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

TASK 5: Send Data Size

Extend message type #2 to include the data size before sending the data itself. You can
choose a number of bytes to encode this information, and make sure the client never
tries to send data more than what can be encoded on this many bytes. Alternatively, you
can introduce different message types that define the data size bytes. For example:

# String message
MESSAGE_STRING = 1  
# Data message, data size is encoded on 1 byte (data size: up to 255 bytes)
MESSAGE_DATA_1B = 2
# Data message, data size is encoded on 2 bytes (data size: up to 64 kB)
MESSAGE_DATA_2B = 3
# Data message, data size is encoded on 3 bytes (data size: up to 16 MB)
MESSAGE_DATA_3B = 4
...

The server should verify that every byte was received before saving the file.

THIS IS THE CLIENT
"""

import socket
from termcolor import colored, cprint
import os
from message_type import MessageType

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9000  # The port used by the server

# print(MessageType.BinaryType.values())
# print(MessageType.BinaryType.keys())

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Ask which message type to send
        message_type = input(
            colored("Enter message type (1 = string, 2 = binary): ", attrs=["bold"])
        )
        message_length = 0

        if message_type == "1":
            # read a string from the standard input
            data = input(colored("Enter a string: ", attrs=["bold"]))
            # convert the string to bytes and limit the size to 4kB
            data = data.encode("utf-8")[:4096]
        elif message_type == "2":
            # ask for message length
            print("Message length options:")
            print(
                "\t1: 1B\n\t2: 10B\n\t3: 100B"
                + "\n\t4: 1KB\n\t5: 10KB\n\t6: 100KB"
                + "\n\t7: 1MB\n\t8: 10MB\n\t9: 100MB\n"
            )
            binary_message_type_choice = input(
                colored("Enter message length in bytes: ", attrs=["bold"])
            )

            try:
                binary_message_type_choice = int(binary_message_type_choice)
                if binary_message_type_choice not in range(len(MessageType.BinaryType)):
                    raise ValueError
            except ValueError:
                cprint("Invalid message length", "red")
                continue

            message_length = list(MessageType.BinaryType.values())[
                binary_message_type_choice
            ]
            # generate a random byte array
            data = os.urandom(message_length)
            # prepend the binary message type in one byte
            data = bytes([binary_message_type_choice]) + data
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
        cprint(
            f"Sending a message of type {message_type},"
            + f" with a length of {message_length}B",
            "blue",
        )
        s.sendall(data)

        # closing the connection
        cprint("Closing the connection", "red")
        s.close()
