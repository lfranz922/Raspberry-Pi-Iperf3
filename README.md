# Raspberry-Pi-Iperf3

This is a raspberry Pi application that can be used to test TCP/UDP connections and speeds over a network.

## Testing Procedure:

1) Run the GUI.py script and select and specifications to the test that you want (Default is 2-way TCP check the boxes to change to those tests).
2) Once the test is set up press run, the speeds data are displayed on screen monitor these to see if they are what is expected. 
3) perform any other tests to the system that are needed. If the connection goes down the GUI will notify you and continuously try to restablish a connection. (Speeds and Connection breaks are all timestamped and recoreded in the logs.txt file)

## Setup 1: Singluar Pi

Using a USB to ethernet dongle (if the device only has 1 CATX port) create a looped back connection through the system you are trying to test. 
Please note: some devices will internally loopback information meant for a port on the same device this can be seen by the program showing speeds that are higher than the CATX specification.

## Setup 2: Dual Raspberry Pi's

To set this up a second Raspberry Pi will need to be running the script provided (I suggest making it run this script on start up) and connected to the other end of the system being tested.
On the main Raspberry Pi follow the procedure as normal.
