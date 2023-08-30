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

THIS IS THE CLIENT
"""

import socket
from termcolor import colored, cprint

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9000  # The port used by the server


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # input(colored("Press Enter to continue...\n", attrs=["bold"]))
        # read a string from the standard input
        data = input(colored("Enter a string: ", attrs=["bold"]))
        # convert the string to bytes and limit the size to 4kB
        data = data.encode("utf-8")[:4096]

        # connect to the server
        s.connect((HOST, PORT))
        # print a status
        cprint(f"Connected to {HOST}:{PORT}", "green")

        # send some data
        cprint(f"Sending data {data}", "blue")
        s.sendall(data)

        # closing the connection
        cprint("Closing the connection", "red")
        s.close()
