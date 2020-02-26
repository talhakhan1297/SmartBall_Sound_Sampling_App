from tkinter import *
from tkinter import messagebox
import pyaudio
import wave
import threading
import matplotlib
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import *
from matplotlib import style

matplotlib.use("TkAgg")
style.use('ggplot')


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
        self.radioVal = StringVar()
        self.feedbackVal = StringVar()
        self.rcdStpVal = StringVar()
        self.rcdStpVal.set('Record')  # Initial value
        self.radioVal.set('edge')  # Initial value
        self.feedbackVal.set('')  # Initial value

        try:
            sampleCountFileR = open('sampleCount.txt', "r")
            if sampleCountFileR.read() == '':
                self.count = 0
            else:
                sampleCountFileR = open('sampleCount.txt', "r")
                self.count = int(sampleCountFileR.read())
            sampleCountFileR.close()

        except FileNotFoundError:
            sampleCountFileNW = open('sampleCount.txt', "w")
            sampleCountFileNW.close()
            self.count = 0

        self.frames = []  # Initialize array to store frames
        self.intframes = []
        self.isrecording = False
        self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
        self.stream = self.p.open(format=self.sample_format, channels=self.channels,
                                  rate=self.fs, frames_per_buffer=self.chunk, input=True)
        self.fileName = ''

        # Initialized Main Window
        master.title("SmartBall Sampling App")
        master.geometry('1025x576')
        master.resizable(False, False)
        master.config(bg=backgroundColor)

        self.fig = Figure(figsize=(16, 5), dpi=60)
        self.a = self.fig.add_subplot(111)
        self.a.set_title('Graph of Recorded Sound')
        self.a.set_xlabel('No. of Samples')
        self.a.set_ylabel('Amplitude')

        # Initialized Plot
        self.plotCanvas = FigureCanvasTkAgg(self.fig, master)
        self.plotCanvas.draw()
        self.plotCanvas.get_tk_widget().grid(
            row=0, padx=(35, 35), pady=(24, 24), columnspan=5)

        # Initialized Record/Stop Button
        recordBtn = Button(master, textvariable=self.rcdStpVal, font=(
            "Montserrat 10 bold"), bg=accentColor, activebackground=pressedButton, fg=primaryColor, bd=0, pady=5, padx=5,
            command=self.rcdStpSelect)
        recordBtn.grid(row=1, column=2, sticky='w')

        # Initialized Stop Button
        resetBtn = Button(master, text='Reset', font=(
            "Montserrat 10 bold"), bg=accentColor, activebackground=pressedButton, fg=primaryColor, bd=0, pady=5, padx=10,
            command=self.onReset)
        resetBtn.grid(row=1, column=2, sticky='e')

        # Initialized Label
        note = Label(text="Please select a label for video file.", font=("Montserrat 13"),
                          fg=primaryColor, bg=backgroundColor)
        note.grid(row=2, columnspan=5, padx=36, pady=(40, 16))

        # Initialized Radio Buttons
        r1 = Radiobutton(master, text="Edge", bg=backgroundColor, font=("Montserrat 12"), activebackground=backgroundColor,
                         fg=primaryColor, highlightcolor=backgroundColor, borderwidth=0, selectcolor=backgroundColor,
                         variable=self.radioVal, value="edge", command=self.radioSelect)
        r1.grid(row=3)

        r2 = Radiobutton(master, text="NC",
                         bg=backgroundColor, font=("Montserrat 12"), activebackground=backgroundColor, fg=primaryColor,
                         highlightcolor=backgroundColor, borderwidth=0, selectcolor=backgroundColor, variable=self.radioVal,
                         value="nc", command=self.radioSelect)
        r2.grid(row=3, column=1)

        r3 = Radiobutton(master, text="Pad",
                         bg=backgroundColor, font=("Montserrat 12"), activebackground=backgroundColor, fg=primaryColor,
                         highlightcolor=backgroundColor, borderwidth=0, selectcolor=backgroundColor, variable=self.radioVal,
                         value="pad", command=self.radioSelect)
        r3.grid(row=3, column=2)

        r4 = Radiobutton(master, text="Middle",
                         bg=backgroundColor, font=("Montserrat 12"), activebackground=backgroundColor, fg=primaryColor,
                         highlightcolor=backgroundColor, borderwidth=0, selectcolor=backgroundColor, variable=self.radioVal,
                         value="middle", command=self.radioSelect)
        r4.grid(row=3, column=3)

        r5 = Radiobutton(master, text="Other",
                         bg=backgroundColor, font=("Montserrat 12"), activebackground=backgroundColor, fg=primaryColor,
                         highlightcolor=backgroundColor, borderwidth=0, selectcolor=backgroundColor, variable=self.radioVal,
                         value="other", command=self.radioSelect)
        r5.grid(row=3, column=4)

        # Initialized Save Button
        saveBtn = Button(master, text='Save', font=(
            "Montserrat 10 bold"), bg=accentColor, activebackground=pressedButton, fg=primaryColor, bd=0, pady=5, padx=15,
            command=self.save)
        saveBtn.grid(row=4, column=2, pady=(24, 5), padx=15)

        # Initialized Feedback label
        feedback = Label(textvariable=self.feedbackVal, font=("Montserrat 10"),
                         fg=primaryColor, bg=backgroundColor)
        feedback.grid(row=4, column=4, sticky='s', pady=10)

    # Handle Record/Stop Button
    def rcdStpSelect(self):
        if self.isrecording == False:
            self.startRecording()
        else:
            self.stopRecording()

    # Handle Reset Button
    def onReset(self):
        if self.isrecording == False:
            self.frames = []
            self.a.clear()

    # Start Recording
    def startRecording(self):
        if self.isrecording == False and self.frames.__len__() == 0:
            self.rcdStpVal.set('Stop')
            self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
            self.stream = self.p.open(format=self.sample_format, channels=self.channels,
                                      rate=self.fs, frames_per_buffer=self.chunk, input=True)
            self.isrecording = True

            t = threading.Thread(target=self.record)
            t.start()
            self.feedbackVal.set('Recording ✓')

    # Main recording loop
    def record(self):
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        self.frames = b''.join(self.frames)

    # Stop Recording and close the stream
    def stopRecording(self):
        if self.isrecording:
            self.rcdStpVal.set('Record')
            self.isrecording = False
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()  # Terminate the PortAudio interface

            amplitude = np.frombuffer(self.frames, np.int16)
            self.a.plot(amplitude)
            self.plotCanvas.draw()
            self.feedbackVal.set('Stopped ✓')

    # Handle radio selection
    def radioSelect(self):
        if self.frames.__len__() != 0 and self.isrecording == False:
            self.fileName = str(self.count) + '_' + \
                self.radioVal.get() + '.wav'
            self.feedbackVal.set('Selected ✓')

    # This executes on save button press and saves the file with the name chosen through radio buttons
    # Save the recorded data as a WAV file
    def save(self):
        if self.frames.__len__() != 0 and self.fileName != '' and self.isrecording == False:
            wf = wave.open(self.fileName, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(self.frames)
            wf.close()

            self.count = self.count + 1
            sampleCountFileW = open('sampleCount.txt', "w")
            sampleCountFileW.write(str(self.count))
            sampleCountFileW.close()

            self.frames = []
            self.fileName = ''
            self.a.clear()
            self.feedbackVal.set('Saved ✓')


root = Tk()
gui = App(root)
root.mainloop()
