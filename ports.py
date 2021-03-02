import subprocess
import platform
import port

class ports:
    ports = []
    def __init__(self):
        ports = get_ports()


    def get_ports():
        return None #TODO

    def ping(host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '1', host]
        tf = subprocess.call(command) == 0
        print(tf)
        return tf

    def pingPorts():
        for port in ports:
            if not ping(ports):
                return False
        return True #TODO
