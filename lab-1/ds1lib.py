import socket
from termcolor import colored, cprint
import os
import threading
import time
from pathlib import Path

# class enum for message types
class MessageType:
    STRING = 1
    BINARY = 2

    # Message types for binary data
    # key: message type, value: data size in bytes
    BinaryType = {
        "B1": 1,
        "B10": 10,
        "B100": 100,
        "KB1": 1024,
        "KB10": 10240,
        "KB100": 102400,
        "MB1": 1048576,
        "MB10": 10485760,
        "MB100": 104857600,
    }

"""
DSClient class
Purpose:
    - Connect to a server
    - Send a message to the server
    - Close the connection
Takes:
    - host: server host
    - port: server port
"""
class DSClient:
    def __init__(self, host: int, port: int, mnt: Path):
        self.host = host
        self.port = port
        self.mnt = mnt
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to the server
        self.socket.connect((self.host, self.port))
        # print a status
        cprint(f"Connected to {self.host}:{self.port}", "green")

    def send_msg(self, type, content, length=4096):
        # send some data
        cprint(
            f"Sending a message of type {type},"
            + f" with a length of {length}B",
            "blue",
        )
        self.socket.sendall(content)

    def close(self):
        # closing the connection
        cprint("Closing the connection", "red")
        self.socket.close()
    
    def prompt_user(self) -> bool | tuple:
        # ask which message type to send
        message_type = input(
            colored(
                "Enter message type:"
                + "\n\t1 = string"
                + "\n\t2 = binary"
                + "\n\t3 = upload\n",
                attrs=["bold"]
            )
        )

        # check if message type is valid
        if message_type not in ["1", "2", "3"]:
            cprint("Invalid message type", "red")
            return False

        # else if message type is valid, continue:
        message_length = 0

        if message_type == "1":
            # read a string from the standard input
            data = input(colored("Enter a string (max 4MiB): ", attrs=["bold"]))
            # convert the string to bytes and limit the size to 4kB
            data = bytes([0]) + data.encode("utf-8")[:4097]
        elif message_type == "2":
            # ask for message length
            print("Message length options:")
            print(
                "\t1: 1B\n\t2: 10B\n\t3: 100B"
                + "\n\t4: 1KB\n\t5: 10KB\n\t6: 100KB"
                + "\n\t7: 1MB\n\t8: 10MB\n\t9: 100MB\n"
            )
            binary_message_type_choice = input(
                colored("Enter message length option: ", attrs=["bold"])
            )
            binary_message_type_choice_idx = -1

            try:
                binary_message_type_choice = int(binary_message_type_choice)
                binary_message_type_choice_idx = binary_message_type_choice - 1
                if binary_message_type_choice_idx not in range(len(MessageType.BinaryType)):
                    raise ValueError
            except ValueError:
                cprint("Invalid message length", "red")
                return False

            message_length = list(MessageType.BinaryType.values())[
                binary_message_type_choice_idx
            ]
            # generate a random byte array
            data = os.urandom(message_length)
            # prepend the binary message type in one byte
            data = bytes([binary_message_type_choice]) + data
        
        elif message_type == "3":
            # ask for a file path
            file_path = self.mnt \
                / Path(input(colored("Enter a file path: ", attrs=["bold"])))
            cprint(f"File path: {file_path}", "blue")

            # check if the file exists
            if not os.path.isfile(file_path):
                cprint(f"File {file_path} not found", "red")
                return False
            else:
                # send file name to server
                file_name = file_path.name
                file_name = bytes([3]) + file_name.encode("utf-8")
                self.connect()
                while self.send_msg(1, file_name) == False:
                    pass
                self.close()
            
            # # read the file
            # with open(file_path, "rb") as f:
            #     data = f.read()
            
            # # prepend the binary message type in one byte
            # data = bytes([3]) + data
            # # set the message length to the file size
            # message_length = len(data)
        
        return message_type, data, message_length

    def spin(self):
        while True:
            # msg could be False 
            # or a correctly formed message
            msg = self.prompt_user()
            # if False, it failed
            # so we continue to the next iteration
            if msg == False:
                continue
            
            # if message created correctly
            # unpack the message
            message_type, data, message_length = msg

            self.connect()
            while self.send_msg(message_type, data, length=message_length) == False:
                pass
            self.close()

"""
DSServer class
Purpose:
    - Listen for incoming connections
    - Start a new thread for each connection
    - Receive a message from the client
    - Close the connection
Takes:
    - host: server host
    - port: server port
"""
class DSServer:
    def __init__(self, host: int, port: int, mnt: Path):
        self.HOST = host
        self.PORT = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(1)
    
    def client_thread(self, connection, client_address):
        # Print the remote address
        cprint(f"\nConnection from {client_address}", "green")
        data = b''
        # receive data from the client
        while True:
            received_data = connection.recv(1024)
            # cprint(f"Received {len(data)}B", "green")
            if not received_data:
                break
            data += received_data


        # check the message type
        message_type = data[0]

        if message_type == 0:
            try:
                # convert the bytes to string
                # and remove the message type byte
                data = data.decode("utf-8")[1:]
                cprint(f"\nMessage: {data}", "white", "on_cyan")
            except (UnicodeDecodeError, AttributeError):
                cprint("\nString message decoding failed", "red")
            # If it is supposed to be string message,
            # do not continue handling the message as a binary one
            return
        
        # But if it is a binary message, continue:
        cprint("\nReceived binary data", "red")

        message_type_idx = int(message_type) - 1
        # remove the message type byte
        data = data[1:] 

        expected_message_length = list(MessageType.BinaryType.values())[message_type_idx]
        print(f"Message type: {list(MessageType.BinaryType.keys())[message_type_idx]} with length {expected_message_length}B")
        
        # make sure all bytes are received
        if len(data) == expected_message_length:
            cprint(f"\nReceived {len(data)}B", "green")
        else:
            cprint(
                f"\nReceived {len(data)} bytes,"
                + f" expected {expected_message_length} bytes"
                + " - Data will not be saved to file",
                "red",
            )
            return

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
        
    def spin(self):
        while True:
            # Wait for a connection
            cprint("\nWaiting for a connection...", attrs=["bold"])
            connection, client_address = self.sock.accept()

            # Modify the server code to start a new background thread for each new incoming
            # connection, and handle it there.
            t = threading.Thread(target=self.client_thread, args=(connection, client_address))
            t.start()