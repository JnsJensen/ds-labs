# class enum for message types
class MessageType:
    STRING = 1
    BINARY = 2

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
