from enum import Enum

class Port:
    def __init__(self, ip):
    #Host = type
    Ip = ip

    def getIp():
        return Ip

    def getType():
        return host

class HostType(Enum):
    Client = 1
    Server = 2
