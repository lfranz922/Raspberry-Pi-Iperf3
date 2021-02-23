import os
import datetime
from datetime import datetime
import time
import re
import io
from contextlib import redirect_stdout
import sys
import subprocess

EXPECTED_SPEED = 500

def getMode():
    #TODO
    return 1

def main():
    #os.chdir(os.getcwd())
    print(os.getcwd())
    mode = getMode()
    while (mode == 1):
        time.sleep(1)
        while (not startTwoWayTCP()):
            time.sleep(0.5)
            pass
        time.sleep(1)
        while (isTCPRunning()):
            time.sleep(1)

    #while()


def startTwoWayTCP():
    """
    initates a 2 Way TCP test
    """
    print("=================================\n")
    print("starting TCP test")
    print("\n=================================")
    os.system("iperf3.exe -s -B 11.0.0.50 --logfile Server1.txt")
    os.system("iperf3.exe -s -B 11.0.0.51 --logfile Server2.txt")
    os.system("iperf3.exe -c 11.0.0.50 -b 0 -B 11.0.0.51 -t 0 -V --logfile Client1.txt")
    os.system("iperf3.exe -c 11.0.0.51 -b 0 -B 11.0.0.50 -t 0 -V --logfile Client2.txt")
    time.sleep(0.5)
    return isTCPRunning()

def isTCPRunningStartup():
    """
    returns True if a 2 way TCP test has started and False otherwise
    """

    time.sleep(0.5)
    logs = open("Client1.txt", 'r')
    #print(logs.readlines()[2])
    line = logs.readlines()[2]
    logs.close()
    print(line)
    isRunning = line != 'iperf3: error - unable to connect to server: Cannot assign requested address\n'
    print(isRunning)
    return isRunning

def isTCPRunning():
    """
    Returns True if a 2 way TCP test is currently running False otherwise
    """
    running = True
    for file in LogTypes.getLogFileNames():
        print(file)
        with open(file, 'r') as f:
            try:
                last_line = f.read().splitlines()[-1]
            except:
                last_line = "iperf3: exiting"
                print("file is empty")

            if last_line != "iperf3: exiting" and last_line != "iperf3: error - unable to connect to server: Cannot assign requested address":
                print (last_line)
                speed = re.findall(r"\d+.?\d+ [A-Z]?bits/sec", last_line)
                print(speed)
                number = re.findall(r"\d+.?\d+", speed[-1])
                print(number)
                if float(number[-1]) > EXPECTED_SPEED:
                    print(file[0:-4] + " 2-way TCP test is running")
                else:
                    print(file[0:-4] + " 2-way TCP test is not running well")
            else:
                print(file[0:-4] + " 2-way TCP test is not running")
                time.sleep(1)
                clearFileContents(file)
                running = False
                break

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

main()
