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

THIS IS THE SERVER
"""

import socket
import sys
from termcolor import colored, cprint
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 9000  # Port to listen on (non-privileged ports are > 1023)


def client_thread(connection, client_address):
    # Print the remote address
    cprint(f"Connection from {client_address}", "green")
    # Clean up the connection
    connection.close()


while True:
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        sys.stderr.write(f"Failed to create socket. Error code: {msg[1]}")
        sys.exit()

    try:
        # Bind the socket to the port
        cprint(f"Binding socket to {HOST} port {PORT}", "blue")
        sock.bind((HOST, PORT))
    except socket.error as msg:
        sys.stderr.write(f"Failed to bind socket. Error code: {msg}")
        sys.exit()

    # Wait for a connection
    cprint("Waiting for a connection...", attrs=["bold"])
    sock.listen(1)
    connection, client_address = sock.accept()

    # Modify the server code to start a new background thread for each new incoming connection, and handle it there.
    t = threading.Thread(target=client_thread, args=(connection, client_address))
    t.start()
