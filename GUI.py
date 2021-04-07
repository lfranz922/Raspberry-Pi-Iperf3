

import tkinter as tk
import tkinter.font as tkFont
import time
import iperfScript as script
import threading

class App(tk.Frame):
    is_running = False
    script = None
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=320
        height=240
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        start_button=tk.Button(root)
        start_button["bg"] = "#6f6f6f"
        start_button["cursor"] = "spraycan"
        ft = tkFont.Font(family='Times',size=10)
        start_button["font"] = ft
        start_button["fg"] = "#ffffff"
        start_button["justify"] = "center"
        start_button["text"] = "START"
        start_button.place(x=110,y=40,width=90,height=40)
        start_button["command"] = self.start_button_command
        self.start_button = start_button

        client1=tk.Label(root)
        client1["bg"] = "#6f6f6f"
        ft = tkFont.Font(family='Times',size=10)
        client1["font"] = ft
        client1["fg"] = "#ffffff"
        client1["justify"] = "left"
        client1["text"] = "1"
        client1.place(x=10,y=110,width=110,height=25)
        self.client1 = client1

        client2=tk.Label(root)
        client2["bg"] = "#6f6f6f"
        ft = tkFont.Font(family='Times',size=10)
        client2["font"] = ft
        client2["fg"] = "#ffffff"
        client2["justify"] = "left"
        client2["text"] = "Client 2: ..."
        client2.place(x=10,y=150,width=110,height=25)
        self.client2 = client2

        server1=tk.Label(root)
        server1["bg"] = "#6f6f6f"
        ft = tkFont.Font(family='Times',size=10)
        server1["font"] = ft
        server1["fg"] = "#ffffff"
        server1["justify"] = "left"
        server1["text"] = "Server 1: ..."
        server1.place(x=190,y=110,width=110,height=25)
        self.server1 = server1

        server2=tk.Label(root)
        server2["bg"] = "#6f6f6f"
        ft = tkFont.Font(family='Times',size=10)
        server2["font"] = ft
        server2["fg"] = "#ffffff"
        server2["justify"] = "left"
        server2["text"] = "Server 2: ..."
        server2.place(x=190,y=150,width=110,height=25)
        self.server2 = server2
        self.root = root

    def start_button_command(self):
        #self.client1.configure(text="1")
        print("OG: ", self.is_running)
        if not self.is_running:
            #script.start(self)
            #threading.Thread(target="script.start(self)")
            print(self.script)
            #print(self.script)
            self.start_button.configure(text=("STOP"))
            self.root.after(0, script.main)
            self.root.after(100, self.run_script)
            self.is_running = not self.is_running
        else:
            self.start_button.configure(text=("START"))
            self.script.end(self.script)
            self.is_running = not self.is_running


    def run_script(self):
        print(self.is_running)
        if self.is_running:
            #now = int(self.client1["text"])
            self.client1.configure(text="str")
            self.loop_cmd()

    def loop_cmd(self):
        if self.is_running:
            print(script.main.get_speeds())
            self.root.after(100, self.run_script)


root = tk.Tk()
app=App(root)
root.wm_title("Tkinter clock")
root.mainloop()
