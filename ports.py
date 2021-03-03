import subprocess
import platform
import port

class ports:
    ports = []
    def __init__(self):
        ports = get_ports()


    def get_ports():
        """
        cmd "ifconfig" gives all interfaces and we want the inet of eth0 and eth1
        cmd "ping -c 4 \(number of pings) -I \eth0.inet \eth1.inet"
        """
        return None #TODO

    def ping(IP1):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """
        cmd = ['ping', 'google.com']
        try:
            out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
            lines = out.readlines()
            if lines[-1] == b'Ping request could not find host google.com. Please check the name and try again.\r\n':
                print("Ports could not connect :'(")
                return False
            for line in lines:
                print(line)
        except:
            print("Ports could not connect :'(")
            return False


        #out = subprocess.run(cmd, check = True, stdout=subprocess.PIPE).stdout
        #print(out)
        return True

    def pingPorts():
        for port in ports:
            if not ping(ports):
                return False
        return True #TODO

    ping("google.com")
