import src.dialog as dialog
import src.extractor as extractor
import tkinter as tk
import os

class GUI(tk.Frame):

    def ask_open(self):
        result = dialog.open_dialog("Open Video File",(("MP4 files (.mp4)","*.mp4"),("All Files","*.*")))
        if result == None or result == "" or result == ():
            pass
        else:
            self.inputPath = result
            self.inputPathLabel.configure(text=self.inputPath)

    def ask_save(self):
        result = dialog.save_dialog("Save Video File",(("MP4 files (.mp4)","*.mp4"),("All Files","*.*")))
        if result == None or result == "" or result == ():
            pass
        else:
            self.outputPath = result
            self.outputPathLabel.configure(text=self.outputPath)

    def update_threshold(self, event):
        self.threshold = self.thresholdSlider.get()

    def act(self):
        if self.inputPath == "" or self.outputPath == "":
            dialog.error_dialog("Must specify an input and output path!",caption="Error")
        else:
            if not os.path.exists(self.inputPath):
                dialog.error_dialog("Input file must exist!", caption="Error")
            else:
                success = extractor.extract(self.inputPath,self.outputPath,self.threshold,self.mode.get()==2)
                if success:
                    dialog.info_dialog("File successfully created!",caption="Silence Extractor")
                else:
                    dialog.error_dialog("Could not create file.","Error")

    def create_widgets(self):
        self.inputPath = ""
        tk.Label(self, text="Input Video: ", anchor=tk.W, font=("Courier", 11)).grid(row=0,column=0)
        self.inputPathLabel = tk.Label(self, text=self.inputPath,borderwidth=2, relief="sunken", font=("Courier", 11), anchor=tk.E,width=30,height=1, padx=5)
        self.inputPathLabel.grid(row=0,column=1)
        self.selectInputPath = tk.Button(self,text="...",font=("Courier", 11),command=self.ask_open,width=1,height=1)
        self.selectInputPath.grid(row=0,column=2)

        self.outputPath = ""
        tk.Label(self, text="Output Video: ", anchor=tk.W, font=("Courier", 11)).grid(row=1,column=0)
        self.outputPathLabel = tk.Label(self, text=self.outputPath, borderwidth=2, relief="sunken", font=("Courier", 11), anchor=tk.E,width=30,height=1, padx=5)
        self.outputPathLabel.grid(row=1,column=1)
        self.selectOutputPath = tk.Button(self,text="...",font=("Courier", 11),command=self.ask_save,width=1,height=1)
        self.selectOutputPath.grid(row=1,column=2)


        tk.Label(self, text="Threshold: ", anchor=tk.W, font=("Courier", 11)).grid(row=2,column=0)
        self.threshold = 0.0
        self.thresholdSlider = tk.Scale(self, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, length=400, command=self.update_threshold)
        self.thresholdSlider.grid(row=2,columnspan=2,column=1)

        tk.Label(self, text="Mode: ", anchor=tk.W, font=("Courier", 11)).grid(row=3,column=0)
        self.modeAradio = tk.Radiobutton(self,text="Lower Threshold",variable=self.mode,value=2)
        self.modeBradio = tk.Radiobutton(self,text="Upper Threshold",variable=self.mode,value=1)
        self.modeAradio.grid(row=3,column=1)
        self.modeBradio.grid(row=3,column=2)

        self.actButton = tk.Button(self,text="Run",font=("Courier", 11),command=self.act,width=8,height=1)
        self.actButton.grid(row=4,column=1)


    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.mode = tk.IntVar(master)
        self.mode.set(1)

        self.pack(padx=5, pady=5)
        master.title("Silence Extractor")
        self.create_widgets()

root = tk.Tk()

def gui_closed():
    if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()
        raise SystemExit

def create_gui():

    root.protocol("WM_DELETE_WINDOW", gui_closed)

    gooey = GUI(root)
    return root, gooey