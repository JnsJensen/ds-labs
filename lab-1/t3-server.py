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

THIS IS THE SERVER
"""

import socket
import sys
from termcolor import colored, cprint
import threading
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 9000  # Port to listen on (non-privileged ports are > 1023)


def client_thread(connection, client_address):
    # Print the remote address
    cprint(f"Connection from {client_address}", "green")
    # receive data from the client
    data = connection.recv(4096)
    # convert the bytes to string
    data = data.decode("utf-8")
    # print the received data
    cprint(f"Message: {data}", "white", "on_cyan")
    # Clean up the connection
    connection.close()


while True:
    connected = False
    socketed = False
    while not connected and not socketed:
        try:
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            sys.stderr.write(f"Failed to create socket. Error code: {msg[1]}\n")
            sys.exit()
        finally:
            socketed = True
            cprint("Socket created", "light_grey")

        try:
            # Bind the socket to the port
            cprint(f"Binding socket to {HOST} port {PORT}", "blue")
            sock.bind((HOST, PORT))
        except socket.error as msg:
            sys.stderr.write(f"Failed to bind socket. Error code: {msg}\n")
            time.sleep(1)
        finally:
            connected = True
            cprint("Socket bind complete", "light_grey")

    # Wait for a connection
    cprint("Waiting for a connection...", attrs=["bold"])
    sock.listen(1)
    connection, client_address = sock.accept()

    # Modify the server code to start a new background thread for each new incoming connection, and handle it there.
    t = threading.Thread(target=client_thread, args=(connection, client_address))
    t.start()
