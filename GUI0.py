

import tkinter as tk
import tkinter.font as tkFont
import time
from tkinter import ttk
#import iperfScript0 as script
import threading
import time
import re
import subprocess
from datetime import datetime
import time
import re
import subprocess
from datetime import datetime

# TODO:
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


class Ports:
    """
    An object that stores a list of all active ports
    """

    ports = []  # stores the IPs of all ethernet Ports

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
            # print(i)
            temp = subprocess.Popen(
                ["ifconfig", f"eth{i}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
            #temp = subprocess.Popen(["ifconfig eth0"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
            for line in temp.readlines():
                if 'error' in line.decode('utf-8'):
                    searching = False
                    break
                eth.append(line.decode('utf-8'))
                # print(line.decode('utf-8'))

        # print(eth)

        for i in range(len(eth)):
            if len(re.findall(r"eth\d", eth[i])) > 0:
                print("ladies and gentlemen; we got him")
                # print(eth[i])
                inet = re.findall(r"inet \d+.\d+.\d+.\d+", eth[i + 1])
                # print(inet[0])
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
            out = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
            lines = out.readlines()

            print(lines[-1].decode("utf-8"))
            # TODO change this to deal with linux string
            if 'Cannot assign requested address' in lines[-1].decode("utf-8"):
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


EXPECTED_MIN_SPEED = 900  # can be changed to whatever we want



class main:
    threads = []
    ports = []

    def __init__(self, labels):
        global run
        self.labels = labels
        main.clearFileContents("logs.txt")
        subprocess.Popen(['killall iperf3'], shell=True)
        time.sleep(0.25)
        ips = Ports()
        ips.getIps()
        print("ips has ports:", ips.ports)
        print("Script told to run:", run)
        while run:
            while (run and not ips.areConnected()):
                print("connecting Ports...")
                time.sleep(0.5)
            print("=================================\n")
            print("        ports connected")
            print("\n=================================")
            while (run and not self.startTwoWayTCP(ips)):
                time.sleep(0.5)
                continue
            time.sleep(0.5)
            while (run and self.isRunning()):
                time.sleep(0.5)
                print("Script Running: ", run)
                try:
                    for i in range(4):
                        labels[i].configure(text=LogTypes.getNames()[
                                            i] + ": " + str(self.speeds[i]))
                except:
                    print("exception happened. run: ", run)
                    pass

            print("Script told to run:", run)

        print("done while loop")
        for i in range(4):
            labels[i].configure(text=LogTypes.getNames()[i] + ": Not Running")
        subprocess.Popen(['killall iperf3'], shell=True)
        for t in self.threads:
            t.kill()
        return None

    def startTest(self, ips, test):
        """
        initates a 2 Way TCP test with the first 2 ips from the ports list #can be changed
        returns True if the test started running False otherwise
        """
        self.threads = []
        print("=====================================\n")
        print(f"       starting 1 way TCP test")
        print("\n=====================================")

        self.threads.append(subprocess.Popen(
            [f'iperf3 -s -B {ips.ports[0]} -f m --logfile Server1.txt'], shell=True, stdout=None))
        #self.threads.append(subprocess.Popen([f'iperf3 -s -B {ips.ports[1]} -f m --logfile Server2.txt'], shell = True, stdout = None))
        # self.threads.append(subprocess.Popen([f'iperf3 -c {ips.ports[0]} -B {ips.ports[1]} -f m -t 0 -V --logfile Client1.txt'],
        #                                     shell = True, stdout = None))
        self.threads.append(subprocess.Popen([f'iperf3 -c {ips.ports[1]} -B {ips.ports[0]} -f m -t 0 -V --logfile Client2.txt'],
                                             shell=True, stdout=None))
        time.sleep(2)
        return self.isRunning()

    def startTwoWayTCP(self, ips):
        """
        initates a 2 Way TCP test with the first 2 ips from the ports list #can be changed
        returns True if the test started running False otherwise
        """
        self.threads = []
        print("=====================================\n")
        print("       starting 2 way TCP test")
        print("\n=====================================")

        self.threads.append(subprocess.Popen(
            [f'iperf3 -s -B {ips.ports[0]} -f m --logfile Server1.txt'], shell=True, stdout=None))
        self.threads.append(subprocess.Popen(
            [f'iperf3 -s -B {ips.ports[1]} -f m --logfile Server2.txt'], shell=True, stdout=None))
        self.threads.append(subprocess.Popen([f'iperf3 -c {ips.ports[0]} -B {ips.ports[1]} -f m -t 0 -V --logfile Client1.txt'],
                                             shell=True, stdout=None))
        self.threads.append(subprocess.Popen([f'iperf3 -c {ips.ports[1]} -B {ips.ports[0]} -f m -t 0 -V --logfile Client2.txt'],
                                             shell=True, stdout=None))
        time.sleep(2)
        return self.isRunning()

    def isRunning(self):
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
                    # this could be traded out for reading from CMD line
                    last_line = f.read().splitlines()[-1]
                    print(file, last_line)
                except:
                    last_line = "iperf3: exiting"
                    print("file is empty")

                try:
                    if "iperf3: exiting" not in last_line and "iperf3: error" not in last_line:
                        speed = re.findall(
                            r"\d+.?\d+ [A-Z]?bits/sec", last_line)
                        print(speed)
                        number = re.findall(r"\d+.?\d+", speed[-1])
                        speeds.append(float(number[-1]))
                        if float(number[-1]) > EXPECTED_MIN_SPEED:
                            print(file[0:-4] + " 2-way TCP test is running")
                        elif float(number[-1]) > 1:
                            print(file[0:-4] +
                                  " 2-way TCP test is not running well")
                        else:
                            print("\n\n\nTCP TEST IS TOO LOW\n\n\n")
                            for t in self.threads:
                                t.kill()
                            # could be turned into its own function
                            subprocess.Popen(['killall iperf3'], shell=True)
                            running = False
                    else:
                        print(file[0:-4] + " 2-way TCP test is not running")
                        main.clearFileContents(file)
                        subprocess.Popen(['killall iperf3'], shell=True)
                        running = False
                except:
                    print("file contains unexpected strings")
                    subprocess.Popen(['killall iperf3'], shell=True)
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
            log_file.write(str(timestamp) + ": " + str(speeds) + "\n")
        log_file.close()
        return running

    def clearFileContents(fName):
        """
        Empties a test file with the given name
        """
        with open(fName, "w"):
            pass


class LogTypes:
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


class App(tk.Frame):
    is_running = False
    script = None

    def __init__(self, root):
        # setting title
        global run
        run = False
        root.title("undefined")
        # setting window size
        width = 640
        height = 480
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        start_button = tk.Button(root)
        start_button["bg"] = "#6f6f6f"
        ft = tkFont.Font(family='Times', size=10)
        start_button["font"] = ft
        start_button["fg"] = "#ffffff"
        start_button["justify"] = "center"
        start_button["text"] = "START"
        start_button.place(x=275, y=40, width=90, height=40)
        start_button["command"] = self.start_button_command
        self.start_button = start_button

        client1 = tk.Label(root)
        client1["bg"] = "#6f6f6f"
        ft = tkFont.Font(family='Times', size=12)
        client1["font"] = ft
        client1["fg"] = "#ffffff"
        client1["justify"] = "left"
        client1["text"] = "Client 1: Not Running"
        client1.place(x=65, y=150, width=175, height=40)
        self.client1 = client1

        client2 = tk.Label(root)
        client2["bg"] = "#6f6f6f"
        ft = tkFont.Font(family='Times', size=12)
        client2["font"] = ft
        client2["fg"] = "#ffffff"
        client2["justify"] = "left"
        client2["text"] = "Client 2: Not Running"
        client2.place(x=65, y=200, width=175, height=40)
        self.client2 = client2

        server1 = tk.Label(root)
        server1["bg"] = "#6f6f6f"
        ft = tkFont.Font(family='Times', size=12)
        server1["font"] = ft
        server1["fg"] = "#ffffff"
        server1["justify"] = "left"
        server1["text"] = "Server 1: Not Running"
        server1.place(x=400, y=150, width=175, height=40)
        self.server1 = server1

        server2 = tk.Label(root)
        server2["bg"] = "#6f6f6f"
        ft = tkFont.Font(family='Times', size=12)
        server2["font"] = ft
        server2["fg"] = "#ffffff"
        server2["justify"] = "left"
        server2["text"] = "Server 2: Not Running"
        server2.place(x=400, y=200, width=175, height=40)
        self.server2 = server2
        self.root = root

        options = ttk.Combobox(root, values=[
                               "1-way TCP", "2-way TCP", "1-way UDP", "2-way UDP"], state="readonly")
        ft = tkFont.Font(family='Times', size=12)
        options["justify"] = "left"
        options.place(x=260, y=300, width=120, height=20)
        options.current(1)
        self.options = options
        self.root = root

    def start_button_command(self):
        global run
        print(self.options.current())
        print("OG: ", run)
        run = not run
        if run:
            # script.start(self)
            print("run: ", run)
            self.script = threading.Thread(target=main, args=(
                ([[self.client1, self.client2, self.server1, self.server2]])))
            #self.script = threading.Thread(target=App.loop)
            print(self.script)
            self.script.start()
            # print(self.script)
            self.start_button.configure(text=("STOP"))

        else:
            print("run: ", run)
            self.start_button.configure(text=("START"))
            self.script.join()


root = tk.Tk()
app = App(root)
root.wm_title("2-Way TCP Test")
root.mainloop()
