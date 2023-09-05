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

Modify the server code to start a new background thread for each new incoming connection,
and handle it there.

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

THIS IS THE SERVER
"""

import socket
import sys
from termcolor import colored, cprint
import threading
import time
import os
from message_type import MessageType

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 9000  # Port to listen on (non-privileged ports are > 1023)


def client_thread(connection, client_address):
    # Print the remote address
    cprint(f"\nConnection from {client_address}", "green")
    data = []
    # receive data from the client
    while True:
        data += connection.recv(1024)
        if not data:
            break
    try:
        # convert the bytes to string
        data = data.decode("utf-8")
        # print the received data
        cprint(f"\nMessage: {data}", "white", "on_cyan")
    except UnicodeDecodeError:
        cprint("\nReceived binary data", "red")

        # check the message type
        message_type = data[0]
        data = data[1:]

        print(f"Message type: {list(MessageType.BinaryType.keys())[message_type]}")

        expected_message_length = list(MessageType.BinaryType.values())[message_type]
        # make sure all bytes are received
        if len(data) < expected_message_length:
            cprint(
                f"\nReceived {len(data)} bytes,"
                + f" expected {expected_message_length} bytes"
                + " - Data will not be saved to file",
                "red",
            )
            return
        else:
            cprint(f"\nReceived {len(data)}B", "green")

        # generate a random filename
        filename = f"out/file-{time.time()}.bin"
        # create the directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # write the data to the file
        with open(filename, "wb") as f:
            f.write(data)
        # print the filename
        cprint(f"\nSaved to {filename}", "white", "on_red")

    # Clean up the connection
    connection.close()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

while True:
    # Wait for a connection
    cprint("\nWaiting for a connection...", attrs=["bold"])
    connection, client_address = sock.accept()

    # Modify the server code to start a new background thread for each new incoming
    # connection, and handle it there.
    t = threading.Thread(target=client_thread, args=(connection, client_address))
    t.start()
