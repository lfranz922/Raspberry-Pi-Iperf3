import time
import re
import subprocess
from datetime import datetime

#TODO:
"""
Made by Lukas Franz
Things to add:
    - a better output screen (I'm thinking the speeds with a green background if iperf has a good speed and red if its slow/off)
    - turn into a proper script
        - when run from cmd line it throws an error
    - look into the iperf termination thing
    - fix the ping function to work for linux
    -

Things that could be expanded on in the future:
    - interface with automation (send logs/speed maybe as JSON idk tho)
    -
"""


class Port:
    """
    A port class that stores the ip (inet) of a port
    """
    Ip = None
    def __init__(self, ip):
        """
        creates a new port
        """
        Ip = ip

    def getIp():
        """
        returns the value of Ip
        """
        return Ip


class Ports:
    """
    An object that stores a list of all active ports
    """

    ports = [] #stores the IPs of all ethernet Ports

    def __init__(self):
        """
        Creates a Ports object and fills it with all active IPs
        """
        self.getIps()


    def getIps(self):
        """
        uses ifconfig to get all current ethernet ports and their IPs and places the IPs in the ports variable in Ports
        returns a list of all active ethernet ports' IPs
        """
        self.ports = []
        eth = []
        i = 0
        searching = True
        #cmd = f"ifconfig eth{i} | grep 'inet '| cut -d: -f2"
        for i in range(2):
            #print(i)
            temp = subprocess.Popen(["ifconfig", f"eth{i}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
            #temp = subprocess.Popen(["ifconfig eth0"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
            for line in temp.readlines():
                if 'error' in line.decode('utf-8'):
                    searching = False
                    break
                eth.append(line.decode('utf-8'))
                #print(line.decode('utf-8'))


        #print(eth)

        for i in range(len(eth)):
            if len(re.findall(r"eth\d", eth[i])) > 0:
                print("ladies and gentlemen; we got him")
                #print(eth[i])
                inet = re.findall(r"inet \d+.\d+.\d+.\d+", eth[i+1])
                #print(inet[0])
                self.ports.append(inet[0][5:])

        print("found ports:", self.ports)
        return(self.ports)



    def ping(ip1, ip2):
        """
        Returns True if host (str) responds to a ping request.
        """
        cmd = ['ping', '-c 1', '-I' + ip1, ip2]
        try:
            print("trying to connect")
            out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
            lines = out.readlines()

            print(lines[-1].decode("utf-8"))
            if 'Cannot assign requested address' in lines[-1].decode("utf-8"): #TODO change this to deal with linux string
                print("Ports could not connect")
                return False
            for line in lines:
                print(line.decode("utf-8")[:-2])
        except:
            print("Ports could not connect: exception")
            return False


        return True


    def areConnected(self):
        """
        tests if any of the ports in self are connected to eachother
        """
        try:
            print(Ports.ports)
            for p1 in self.ports:
                for p2 in self.ports:
                    if p1 == p2:
                        print("ports are same")
                        continue
                    elif Ports.ping(p1, p2):
                        connected_ports = [p1, p2]
                        print("ports connected")
                        return True
        except:
            print("ports not connected")
            pass
        return False

EXPECTED_MIN_SPEED = 900 #can be changed to whatever we want

def getMode():
    #TODO for automation if we want idea is to add a switch that will make you have to manually turn iperf back on when it fails and leave it running for automation
    return 1


class main:
    threads = []
    ports = []

    def __init__(self, run, labels):
        global run
        self.labels = labels
        main.clearFileContents("logs.txt")
        subprocess.Popen(['killall iperf3'], shell = True)
        time.sleep(1)
        ips = Ports()
        ips.getIps()
        print("ips has ports:", ips.ports)
        mode = getMode()
        print("Script told to run:", run)
        while run:
            while (not ips.areConnected() and run):
                print("connecting Ports...")
                time.sleep(0.5)
            print("=================================\n")
            print("        ports connected")
            print("\n=================================")
            while (not self.startTwoWayTCP(ips) and run):
                time.sleep(0.5)
                continue
            time.sleep(0.5)
            while (self.isTCPRunning() and run):
                time.sleep(0.5)
                print("Script Running: ", run)
                try:
                    for i in range(4):
                        labels[i].configure(text=str(self.speeds[i]))
                except:
                    print("exception happened. run: ", run)
                    pass

            print("Script told to run:", run)




    def startTwoWayTCP(self, ips):
        """
        initates a 2 Way TCP test with the first 2 ips from the ports list #can be changed
        returns True if the test started running False otherwise
        """
        self.threads = []
        print("=================================\n")
        print("       starting TCP test")
        print("\n=================================")

        self.threads.append(subprocess.Popen([f'iperf3 -s -B {ips.ports[0]} -f m --logfile Server1.txt'], shell = True, stdout = None))
        self.threads.append(subprocess.Popen([f'iperf3 -s -B {ips.ports[1]} -f m --logfile Server2.txt'], shell = True, stdout = None))
        self.threads.append(subprocess.Popen([f'iperf3 -c {ips.ports[0]} -B {ips.ports[1]} -f m -t 0 -V --logfile Client1.txt'],
                                             shell = True, stdout = None))
        self.threads.append(subprocess.Popen([f'iperf3 -c {ips.ports[1]} -B {ips.ports[0]} -f m -t 0 -V --logfile Client2.txt'],
                                             shell = True, stdout = None))
        time.sleep(2)
        return self.isTCPRunning()


    def get_speeds():
        speeds = []
        for file in LogTypes.getLogFileNames():

            with open(file, 'r') as f:
                try:
                    last_line = f.read().splitlines()[-1] #this could be traded out for reading from CMD line
                    #print(file, last_line)
                except:
                    last_line = "iperf3: exiting"
                    print("file is empty")
                try:
                    if "iperf3: exiting" not in last_line and last_line != "iperf3: error - unable to connect to server: Cannot assign requested address":
                        speed = re.findall(r"\d+.?\d+ [A-Z]?bits/sec", last_line)
                        print(speed)
                        number = re.findall(r"\d+.?\d+", speed[-1])
                        speeds.append(float(numer[-1]))

                    else:
                        print(file[0:-4] + " 2-way TCP test is not running")
                        main.clearFileContents(file)
                        subprocess.Popen(['killall iperf3'], shell = True)
                        running = False
                except:
                    print("file contains unexpected strings")
                    subprocess.Popen(['killall iperf3'], shell = True)
        return speeds

    def isTCPRunning(self):
        """
        Returns True if a 2 way TCP test is currently running False otherwise
        Prints the speeds of the test if it is running
        """
        speeds = []
        running = True
        print("------------------------------------------------------------------------------------------------------------------")
        for file in LogTypes.getLogFileNames():

            with open(file, 'r') as f:
                try:
                    last_line = f.read().splitlines()[-1] #this could be traded out for reading from CMD line
                    print(file, last_line)
                except:
                    last_line = "iperf3: exiting"
                    print("file is empty")

                try:
                    if "iperf3: exiting" not in last_line and "iperf3: error" not in last_line:
                        speed = re.findall(r"\d+.?\d+ [A-Z]?bits/sec", last_line)
                        print(speed)
                        number = re.findall(r"\d+.?\d+", speed[-1])
                        speeds.append(float(number[-1]))
                        if float(number[-1]) > EXPECTED_MIN_SPEED:
                            print(file[0:-4] + " 2-way TCP test is running")
                        elif float(number[-1]) > 1:
                            print(file[0:-4] + " 2-way TCP test is not running well")
                        else:
                            print("\n\n\nTCP TEST IS TOO LOW\n\n\n")
                            for t in self.threads:
                                t.kill()
                            subprocess.Popen(['killall iperf3'], shell = True) #could be turned into its own function
                            running = False
                    else:
                        print(file[0:-4] + " 2-way TCP test is not running")
                        main.clearFileContents(file)
                        subprocess.Popen(['killall iperf3'], shell = True)
                        running = False
                except:
                    print("file contains unexpected strings")
                    subprocess.Popen(['killall iperf3'], shell = True)
                    main.clearFileContents(file)
                    for t in self.threads:
                        t.kill()

        self.speeds = speeds
        print("2 way TCP test has speeds: ", speeds)
        print("------------------------------------------------------------------------------------------------------------------")
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        log_file = open("logs.txt", 'a+')
        if not running:
            log_file.write(str(timestamp) + ": Iperf went down\n")
            time.sleep(0.25)
        else:
            log_file.write(str(timestamp) + ": " + str(speeds)+"\n")
        log_file.close()
        return running

    def clearFileContents(fName):
        """
        Empties a test file with the given name
        """
        with open(fName, "w"):
            pass

class LogTypes():
    """
    An object that stores the arbitrary names of each output file for iperf to
    write to
    """
    def getLogFileNames():
        """
        returns a list of the 4 log file names as strs with their extension/file type (.txt)
        """
        return ["Server1.txt", "Server2.txt", "Client1.txt", "Client2.txt"]

    def getNames():
        """
        returns a list of the 4 log types as strs
        """
        return ["Server1", "Server2", "Client1", "Client2"]

def start(GUI):
    GUI.script = main()

#main() #runs main
