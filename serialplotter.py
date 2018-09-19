import sys                      # For exception details
import os
import serial                   # Serial comms
import matplotlib               # Graph library
import matplotlib.pyplot as plt # Plotting
matplotlib.use("TkAgg")         # Set GUI for matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg    # matplotlib backend
from matplotlib.figure import Figure
import tkinter as tk            # GUI
from tkinter import ttk
import threading                # Read serial in another thread so it doesn't block the GUI
import argparse                 # read serial port property flags

parser = argparse.ArgumentParser(description='Python real-time serial plotter for Arduino')
parser.add_argument('-p','--port_name', default='COM3', help='The name of the serial port, default=COM3')
parser.add_argument('-b','--baud_rate', default=9600, help ='Baud rate, default=9600', type=int)
args = parser.parse_args()

# Interactive matplotlib graph on (updates instantly)
plt.ion()

# Define port with name, Baud rate = 9600, Arduino default config is 8N1
portName = args.port_name
baudRate = args.baud_rate
ser = serial.Serial()
try:
    ser = serial.Serial(portName, baudRate, timeout=1, parity=serial.PARITY_NONE, bytesize=8, stopbits=1)
except:
    print('Could not open port ' + portName)
    sys.exit(0)

# Define placeholders for plot data
graph_x = []
graph_y = []

# Function for reading a line from the serial port, use asynchronously to avoid blocking to GUI  
def readSerialLine():
    try:
        #Read newline separated line, decode with utf-8 and strip newline
        return ser.readline().decode('utf-8').rstrip()
    except:
        print('Unexpected error:', sys.exc_info()[0])

# Try to parse a string to a float. Returns 0.0 if the string is not a valid float.  
def parseStringToFloat(str):
    try:
        return float(str)
    except ValueError:
        print('ValueError. Could not convert ' + str + ' to float.')
        return 0.0

# App window that holds the graph and graph toolbar
class graphWindown(tk.Tk):

    # boolean flag for background thread to close when the app is closing
    appIsClosing = False

    # Async looping function for listening to the serial port
    def readAsyncPort(self, a_plot, canv):
        while(self.appIsClosing == False):       # loop while the app is open
            if (ser.inWaiting() > 0):       # read only if there are bytes waiting

                # Read line from serial
                str = readSerialLine()

                # skip rest of the loop if the string is empty.
                # This may happen if the serial line read is started from the middle 
                if(len(str) == 0):
                    continue

                # Parse string to float
                val = parseStringToFloat(str)

                # Update data
                graph_x.append(len(graph_x))
                graph_y.append(val)

                # update graph and draw
                a_plot.plot(graph_x, graph_y, '-r')  #-r = red
                canv.draw()

                # print to console for debuggin
                print(val)
        # exited the loop
        print("Background loop ended")
        if(ser.isOpen):
            ser.close()
            print("Closed the serial port")
        os._exit(1)     # not the preferred way of closing but this allows the background thread to shut the app

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)                       # init GUI
        tk.Tk.wm_title(self, "Python serial plotter for Arduino")   # Title for this window

        # define window container frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        
        # setup graph figure
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)

        # get canvas for the figure
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # setup toolbar for the graph
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # start listening to the serial port
        thread = threading.Thread(target=self.readAsyncPort, args=(a, canvas))
        thread.start()

    # Handle for window closing
    def on_closing(self):
        self.appIsClosing = True    # message to background thread that the app is closing

# open app window 
app = graphWindown()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()