from tkinter import *
from tkinter import messagebox
import pyaudio
import wave
import threading
import matplotlib
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import *
from matplotlib import style

matplotlib.use("TkAgg")
style.use('ggplot')

f = Figure(figsize=(9, 3), dpi=100)
a = f.add_subplot(111)


def animate(i):
    pullData = open("sampleText.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)


class App:

    def __init__(self, master):
        # Colors defination
        backgroundColor = '#2C2C2C'
        primaryColor = '#FFFFFF'
        accentColor = '#4154FF'
        pressedButton = '#262F81'

        # Initialized static variables
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.channels = 2
        self.fs = 48000  # Record at 48000 samples per second
        self.sample_format = pyaudio.paInt16  # 16 bits per sample

        # Initialized dynamic variables
        self.radioVal = IntVar()
        self.recordingState = False
        self.count = 0
        self.frames = []  # Initialize array to store frames
        self.isrecording = False
        self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
        self.stream = self.p.open(format=self.sample_format, channels=self.channels,
                                  rate=self.fs, frames_per_buffer=self.chunk, input=True)

        # Initialized Main Window
        master.title("SmartBall Sampling App")
        master.geometry('1025x576')
        master.resizable(False, False)
        master.config(bg=backgroundColor)

        # Initialized Plot
        plotCanvas = FigureCanvasTkAgg(f, master)
        # canvas.show()
        plotCanvas.get_tk_widget().grid(row=0, padx=(45, 45), pady=(24, 24), columnspan=5)

        # Initialized Record Button
        recordBtn = Button(master, text='Record', font=(
            "Montserrat 10 bold"), bg=accentColor, activebackground=pressedButton, fg=primaryColor, bd=0, pady=5, padx=5,
            command=self.startRecording)
        recordBtn.grid(row=1, column=2, sticky='w')

        # Initialized Stop Button
        stopBtn = Button(master, text='Stop', font=(
            "Montserrat 10 bold"), bg=accentColor, activebackground=pressedButton, fg=primaryColor, bd=0, pady=5, padx=15,
            command=self.stopRecording)
        stopBtn.grid(row=1, column=2, sticky='e')

        # Initialized Label
        note = Label(text="Please select a label for video file.", font=("Montserrat 13"),
                          fg=primaryColor, bg=backgroundColor)
        note.grid(row=2, columnspan=5, padx=36, pady=(40, 16))

        # Initialized Radio Buttons
        r1 = Radiobutton(master, text="Edge", bg=backgroundColor, font=("Montserrat 12"), activebackground=backgroundColor,
                         fg=primaryColor, highlightcolor=backgroundColor, borderwidth=0, selectcolor=backgroundColor,
                         variable=self.radioVal, value=1, command=self.radioSelect)
        r1.grid(row=3)

        r2 = Radiobutton(master, text="NC",
                         bg=backgroundColor, font=("Montserrat 12"), activebackground=backgroundColor, fg=primaryColor,
                         highlightcolor=backgroundColor, borderwidth=0, selectcolor=backgroundColor, variable=self.radioVal,
                         value=2, command=self.radioSelect)
        r2.grid(row=3, column=1)

        r3 = Radiobutton(master, text="Pad",
                         bg=backgroundColor, font=("Montserrat 12"), activebackground=backgroundColor, fg=primaryColor,
                         highlightcolor=backgroundColor, borderwidth=0, selectcolor=backgroundColor, variable=self.radioVal, value=3,
                         command=self.radioSelect)
        r3.grid(row=3, column=2)

        r4 = Radiobutton(master, text="Pad",
                         bg=backgroundColor, font=("Montserrat 12"), activebackground=backgroundColor, fg=primaryColor,
                         highlightcolor=backgroundColor, borderwidth=0, selectcolor=backgroundColor, variable=self.radioVal, value=4,
                         command=self.radioSelect)
        r4.grid(row=3, column=3)

        r5 = Radiobutton(master, text="Pad",
                         bg=backgroundColor, font=("Montserrat 12"), activebackground=backgroundColor, fg=primaryColor,
                         highlightcolor=backgroundColor, borderwidth=0, selectcolor=backgroundColor, variable=self.radioVal, value=5,
                         command=self.radioSelect)
        r5.grid(row=3, column=4)

        # Initialized Save Button
        saveBtn = Button(master, text='Save', font=(
            "Montserrat 10 bold"), bg=accentColor, activebackground=pressedButton, fg=primaryColor, bd=0, pady=5, padx=15)
        saveBtn.grid(row=4, column=2, pady=(24, 5), padx=15)

    # Handle radio selection
    def radioSelect(self):
        selection = str(self.radioVal.get())

    # Start Recording
    def startRecording(self):
        self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
        self.stream = self.p.open(format=self.sample_format, channels=self.channels,
                                  rate=self.fs, frames_per_buffer=self.chunk, input=True)
        self.isrecording = True

        print('Recording')
        t = threading.Thread(target=self.record)
        t.start()

    # Main recording loop
    def record(self):
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    # Stop Recording and close the stream
    def stopRecording(self):
        if self.isrecording:
            self.isrecording = False
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()  # Terminate the PortAudio interface

            print('Finished recording')
            print('filename'+str(self.count)+'.wav')

            # Save the recorded data as a WAV file
            wf = wave.open('filename'+str(self.count)+'.wav', 'wb')
            self.count = self.count + 1
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            self.frames.clear()


root = Tk()
gui = App(root)
ani = animation.FuncAnimation(f, animate, interval=1000)
root.mainloop()
