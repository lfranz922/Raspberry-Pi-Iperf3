import subprocess
import platform
import re

class ports:
    ports = []
    def __init__(self):
        self.ports = find_ports()

    def getIps():
        cmd = ["ifconfig"]#["ping", "-c 4", "google.com"]

        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
        lines = []
        for ByteLines in out.readlines():
            lines.append(ByteLines.decode("utf-8"))
            
        ips = []
        for i in range(len(lines)):
            if len(re.findall(r"eth\d", lines[i])) > 0:
                print("ladies and gentlemen; we got him")
                inet = re.findall(r"inet \d+.\d+.\d+.\d+", lines[i+1])
                print(inet[0])
                ips.append(inet[0][5:])
                
        print(ips)
        return(ips)

    def find_ports():
        """
        cmd "ifconfig" gives all interfaces and we want the inet of eth0 and eth1
        cmd "ping -c 4 \(number of pings) -I \eth0.inet \eth1.inet"
        """
        ips = getIps()
        for ip in ips:
            ports.append(ip)
        return ports

    def ping(ip1, ip2):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """
        cmd = ['ping', '-c 1', '-I' + ip1, ip2]
        #try:
        try:
            out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
            lines = out.readlines()
            print(lines[-1].decode("utf-8"))
            if lines[-1].decode("utf-8") == 'Ping request could not find host google.com. Please check the name and try again.\r\n':
                print("Ports could not connect :'(")
                return False
            for line in lines:
                print(line.decode("utf-8")[:-2])
        except:
            print("Ports could not connect :'( exception")
            return False


        #out = subprocess.run(cmd, check = True, stdout=subprocess.PIPE).stdout
        #print(out)
        return True

    def pingPorts():
        for port in ports:
            if not ping(ports):
                return False
        return True #TODO
        
    ips =  getIps()
    print(ips)
    print(ping(ips[0], ips[1]))
