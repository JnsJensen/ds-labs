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

THIS IS THE CLIENT
"""

import socket
from termcolor import colored, cprint

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9000  # The port used by the server


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        input(colored("Press Enter to continue...", attrs=["bold"]))
        # connect to the server
        s.connect((HOST, PORT))
        # print a status
        cprint(f"Connected to {HOST}:{PORT}", "green")

        # send some data
        data = b"Hello, world"
        cprint(f"Sending data {data}", "blue")
        s.sendall(data)

        # closing the connection
        cprint("Closing the connection", "red")
        s.close()
