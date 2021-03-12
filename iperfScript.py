import os
import datetime
from datetime import datetime
import time
import re
import io
import sys
import subprocess
import platform
import subprocess
import platform
import threading
from enum import Enum

class Port:
    Ip = None
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

class Ports:
    ports = []
    def __init__(self):
        self.getIps()
        

    def getIps(self):
        self.ports = []
        eth = []
        i = 0
        searching = True
        #cmd = f"ifconfig eth{i} | grep 'inet '| cut -d: -f2"
        while searching:
            temp = subprocess.Popen(["ifconfig", f"eth{i}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
            #temp = subprocess.Popen(["ifconfig eth0"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
            for line in temp.readlines():
                if 'error fetching interface information: Device not found' in line.decode('utf-8'):
                    searching = False
                    break
                eth.append(line.decode('utf-8'))
                print(line.decode('utf-8'))
            i += 1
                
        print(eth)
            
#         lines = []
#         for ByteLines in out.readlines():
#             lines.append(ByteLines.decode("utf-8"))
# 
#         ips = []
        for i in range(len(eth)):
            if len(re.findall(r"eth\d", eth[i])) > 0:
                print("ladies and gentlemen; we got him")
                print(eth[i])
                inet = re.findall(r"inet \d+.\d+.\d+.\d+", eth[i+1])
                print(inet[0])
                self.ports.append(inet[0][5:])
# 
#         print(ips)
#         self.ports.extend(ips)
        print(self.ports)
        return(self.ports)
    
   

    def ping(self, ip1, ip2):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """
        cmd = ['ping', '-c 1', '-I' + ip1, ip2]
        #try:
        try:
            print("trying to connect")
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


    def areConnected(self):
        try:
            print(self.ports)
            for p1 in self.ports:
                for p2 in self.ports:
                    if p1 == p2:
                        print("ports are same")
                        continue
                    if self.ping(p1, p2):
                        connected_ports = [p1, p2]
                        print("ports connected")
                        return True
        except:
            print("ports not connected")
            pass
        return False

EXPECTED_SPEED = 300

def getMode():
    #TODO
    return 1
class main:
    threads = []
    ports = []
    def __init__(self):
        subprocess.Popen(['killall iperf3'], shell = True)
        time.sleep(1)
        ips = Ports()
        ips.getIps()
        print("ips has ports:", ips.ports)
        print(os.getcwd())
        mode = getMode()
        while (mode == 1):
            while (not ips.areConnected()):
                print("connecting Ports...")
                time.sleep(0.5)
            print("=================================\n")
            print("        ports connected")
            print("\n=================================")
            #time.sleep(5)
            while (not self.startTwoWayTCP(ips)):
                time.sleep(0.5)
            time.sleep(0.5)
            while (self.isTCPRunning()):
                time.sleep(1)


    def startTwoWayTCP(self, ips):
        """
        initates a 2 Way TCP test
        """
        self.threads = []
        print("=================================\n")
        print("       starting TCP test")
        print("\n=================================")
        #print("IPs: ")
        #print(ips.ports)
        self.threads.append(subprocess.Popen([f'iperf3 -s -B {ips.ports[0]} -f m --logfile Server1.txt'], shell = True, stdout = None))
        #print("s1 done")
        self.threads.append(subprocess.Popen([f'iperf3 -s -B {ips.ports[1]} -f m --logfile Server2.txt'], shell = True, stdout = None))
        #print("s2 done")
        
        self.threads.append(subprocess.Popen([f'iperf3 -c {ips.ports[0]} -b 1001M -B {ips.ports[1]} -f m -t 0 -V --logfile Client1.txt'],
                                             shell = True, stdout = None))
        #print("c1 done")
        self.threads.append(subprocess.Popen([f'iperf3 -c {ips.ports[1]} -b 1001M -B {ips.ports[0]} -f m -t 0 -V --logfile Client2.txt'],
                                             shell = True, stdout = None))
        #print("c2 done")
#         os.system('iperf3 -s -B ' + ips.ports[0] + ' -f m --logfile Server1.txt')
#         print("s1 done")
#         os.system('iperf3 -s -B ' + ips.ports[1] + ' -f m --logfile Server2.txt')
#         print("s2 done")
#         os.system('iperf3 -c ' + ips.ports[0] + ' -b 0 -B ' + ips.ports[1] + ' -f m -t 0 -V --logfile Client1.txt')
#         print("c1 done")
#         os.system('iperf3 -c ' + ips.ports[1] + ' -b 0 -B ' + ips.ports[0] + ' -f m -t 0 -V --logfile Client2.txt')
#         print("c2 done")
#         
        
                              
        return self.isTCPRunning()

    def isTCPRunningStartup():
        """
        returns True if a 2 way TCP test has started and False otherwise
        """

        time.sleep(0.1)
        logs = open("Client1.txt", 'r')
        #print(logs.readlines()[2])
        line = logs.readlines()[2]
        logs.close()
        print(line)
        isRunning = line != 'iperf3: error - unable to connect to server: Cannot assign requested address\n'
        print(isRunning)
        return isRunning

    def isTCPRunning(self):
        """
        Returns True if a 2 way TCP test is currently running False otherwise
        """
        running = True
        for file in LogTypes.getLogFileNames():
        
            with open(file, 'r') as f:
                try:
                    last_line = f.read().splitlines()[-1]
                    print(file, last_line)
                except:
                    last_line = "iperf3: exiting"
                    print("file is empty")
                try:
                    if "iperf3: exiting" not in last_line and last_line != "iperf3: error - unable to connect to server: Cannot assign requested address":
                        #print (last_line)
                        speed = re.findall(r"\d+.?\d+ [A-Z]?bits/sec", last_line)
                        print(speed)
                        number = re.findall(r"\d+.?\d+", speed[-1])
                       # print(number)
                        if float(number[-1]) > EXPECTED_SPEED:
                            print(file[0:-4] + " 2-way TCP test is running")
                        elif float(number[-1]) > 1:
                            print(file[0:-4] + " 2-way TCP test is not running well")
                        else:
                            print("\n\n\nTCP TEST IS TOO LOW\n\n\n")
                            for t in self.threads:
                                t.kill()
                            subprocess.Popen(['killall iperf3'], shell = True)
                            running = False
                    else:
                        print(file[0:-4] + " 2-way TCP test is not running")
                        main.clearFileContents(file)
                        subprocess.Popen(['killall iperf3'], shell = True)
                        running = False
                except:
                    print("file contains unexpected strings")
                    for t in self.threads:
                        t.kill()

        return running

    def clearFileContents(fName):
        with open(fName, "w"):
            pass

class LogTypes():
    def getLogFileNames():
        """
        returns a list of the 4 log file names as strs
        """
        return ["Server1.txt", "Server2.txt", "Client1.txt", "Client2.txt"]

    def getNames():
        """
        returns a list of the 4 log types as strs
        """
        return ["Server1", "Server2", "Client1", "Client2"]

print(Ports.getIps(Ports()))
main()