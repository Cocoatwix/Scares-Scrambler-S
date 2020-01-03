from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import os
import random

'''Hello anyone reading this! Don't mind the disgusting code in some places. I'm not that good at coding, so dpn't expect it to work perfectly!
Anyways, hopefully you'll find some enjoyment messing around with this corruptor. Ciao!'''

root = Tk()
root.title("Scares Scrambler Build 9")
root.geometry("310x600+100+100")
#root.resizable(width=False, height=False)

'''TODO:
    Add hexadecimal support (powers of 16)
    DO stuff


Engines:
    0 = Incrementer
    1 = Randomizer
    2 = Scrambler
    3 = Copier
    4 = Tilter
    6 = Sentence Mixer (Text Only)

Unbinding is apparently possible: foo.unbind("<Button-1>")
showerror, showinfo, showwarning, _show? ~These are all message box types.
http://wiki.tcl.tk/37701 ~Hex codes work as well
font="Times"'''

currentEngine = 0
autoEndBool = False
exclusiveBool = False
blockSpaceState = "Linear"

fileName = ""
newFileName = ""

listOfEngines = ["Incrementer Engine", "Randomizer Engine", "Scrambler Engine",
                 "Copier Engine", "Tilter Engine", "Mixer Engine"]


class entry_function_class:
    
    def __init__(self, entryBox):
        self.entryBox = entryBox

    def left_click_function(self, event=None):
        '''Increments the entries'''
        try:
            incValue = int(incValueEntry.get()) #Getting values
            entryBoxValue = int(self.entryBox.get())
            entryBoxValue += incValue #Setting values
            self.entryBox.delete(0, "end")
            if entryBoxValue < 0:
                entryBoxValue = 0
            self.entryBox.insert(0, entryBoxValue)
        except ValueError:
            messagebox.showwarning("What are you doing?", "Please use a whole number for"
                                   " the increment value, thanks!")


    def right_click_function(self, event=None):
        '''Decrements the values'''
        try:
            incValue = int(incValueEntry.get()) #Getting values
            entryBoxValue = int(self.entryBox.get())
            entryBoxValue -= incValue #Setting values
            self.entryBox.delete(0, "end")
            if entryBoxValue < 0:
                entryBoxValue = 0
            self.entryBox.insert(0, entryBoxValue)
        except ValueError:
            messagebox.showwarning("What are you doing?", "Please use a whole number for"
                                   " the increment value, thanks!")


    def generate_random_byte(self, event=None):
        '''Generates a number between 1 and 255'''
        self.entryBox.delete(0, "end")
        self.entryBox.insert(0, random.randint(0, 255))


def resource_path(relative_path):
    try:
        base_path = sys.MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def change_engine_right(event=None):
    global currentEngine
    '''Changes the engine label'''
    currentEngine += 1
    if currentEngine > (len(listOfEngines)-1):
        currentEngine = 0
    engineLabel.config(text=listOfEngines[currentEngine])
    update_layout()


def change_engine_left(event=None):
    global currentEngine
    '''Changes the engine label'''
    currentEngine -= 1
    if currentEngine < 0:
        currentEngine = len(listOfEngines)-1
    engineLabel.config(text=listOfEngines[currentEngine])
    update_layout()


def hide_dynamic_widgets():
    '''Hides dynamic widgets, dummy'''
    blockSizeLabel.grid_forget()
    blockSizeEntry.grid_forget()
    blockSizeButton.grid_forget()

    linearRadio.grid_forget()
    exponentialRadio.grid_forget()
    randomRadio.grid_forget()

    blockSpaceLabel.grid_forget()
    blockSpaceEntry.grid_forget()
    blockSpaceButton.grid_forget()

    addValueLabel.grid_forget()
    addValueEntry.grid_forget()
    addValueButton.grid_forget()

    blockGapLabel.grid_forget()
    blockGapEntry.grid_forget()
    blockGapButton.grid_forget()

    replaceLabel.grid_forget()
    replaceEntry.grid_forget()
    replaceButton.grid_forget()

    replaceWithLabel.grid_forget()
    replaceWithEntry.grid_forget()
    replaceWithButton.grid_forget()

    mixerLabel.grid_forget()

    replaceXCheck.grid_forget()


def update_layout():
    '''Updates the layout, dummy'''
    hide_dynamic_widgets()
    if currentEngine == 0: #Incrementer
        blockSizeLabel.grid(row=5, column=0, pady=5, padx=5, sticky=E)
        blockSizeEntry.grid(row=5, column=1, columnspan=2, pady=5)
        blockSizeButton.grid(row=5, column=3, pady=5)

        linearRadio.grid(row=6, column=0, pady=5)
        exponentialRadio.grid(row=6, column=1, pady=5, sticky=E)
        randomRadio.grid(row=6, column=3, pady=5, sticky=E)

        blockSpaceLabel.grid(row=7, column=0, pady=5, padx=5, sticky=E)
        blockSpaceEntry.grid(row=7, column=1, columnspan=2, pady=5)
        blockSpaceButton.grid(row=7, column=3, pady=5)

        addValueLabel.grid(row=8, column=0, pady=5, padx=5, sticky=E)
        addValueEntry.grid(row=8, column=1, columnspan=2, pady=5)
        addValueButton.grid(row=8, column=3, pady=5)
    elif currentEngine == 1: #Randomizer
        blockSizeLabel.grid(row=5, column=0, pady=5, padx=5, sticky=E)
        blockSizeEntry.grid(row=5, column=1, columnspan=2, pady=5)
        blockSizeButton.grid(row=5, column=3, pady=5)

        linearRadio.grid(row=6, column=0, pady=5)
        exponentialRadio.grid(row=6, column=1, pady=5, sticky=E)
        randomRadio.grid(row=6, column=3, pady=5, sticky=E)

        blockSpaceLabel.grid(row=7, column=0, pady=5, padx=5, sticky=E)
        blockSpaceEntry.grid(row=7, column=1, columnspan=2, pady=5)
        blockSpaceButton.grid(row=7, column=3, pady=5)
    elif currentEngine == 2: #Scrambler
        blockSizeLabel.grid(row=5, column=0, pady=5, padx=5, sticky=E)
        blockSizeEntry.grid(row=5, column=1, columnspan=2, pady=5)
        blockSizeButton.grid(row=5, column=3, pady=5)

        linearRadio.grid(row=6, column=0, pady=5)
        exponentialRadio.grid(row=6, column=1, pady=5, sticky=E)
        randomRadio.grid(row=6, column=3, pady=5, sticky=E)

        blockSpaceLabel.grid(row=7, column=0, pady=5, padx=5, sticky=E)
        blockSpaceEntry.grid(row=7, column=1, columnspan=2, pady=5)
        blockSpaceButton.grid(row=7, column=3, pady=5)
        
        blockGapLabel.grid(row=8, column=0, pady=5, padx=5, sticky=E)
        blockGapEntry.grid(row=8, column=1, columnspan=2, pady=5)
        blockGapButton.grid(row=8, column=3, pady=5)
    elif currentEngine == 3: #Copier
        blockSizeLabel.grid(row=5, column=0, pady=5, padx=5, sticky=E)
        blockSizeEntry.grid(row=5, column=1, columnspan=2, pady=5)
        blockSizeButton.grid(row=5, column=3, pady=5)

        linearRadio.grid(row=6, column=0, pady=5)
        exponentialRadio.grid(row=6, column=1, pady=5, sticky=E)
        randomRadio.grid(row=6, column=3, pady=5, sticky=E)

        blockSpaceLabel.grid(row=7, column=0, pady=5, padx=5, sticky=E)
        blockSpaceEntry.grid(row=7, column=1, columnspan=2, pady=5)
        blockSpaceButton.grid(row=7, column=3, pady=5)
        
        blockGapLabel.grid(row=8, column=0, pady=5, padx=5, sticky=E)
        blockGapEntry.grid(row=8, column=1, columnspan=2, pady=5)
        blockGapButton.grid(row=8, column=3, pady=5)

    elif currentEngine == 4: #Tilter
        blockSizeLabel.grid(row=5, column=0, pady=5, padx=5, sticky=E)
        blockSizeEntry.grid(row=5, column=1, columnspan=2, pady=5)
        blockSizeButton.grid(row=5, column=3, pady=5)

        linearRadio.grid(row=6, column=0, pady=5)
        exponentialRadio.grid(row=6, column=1, pady=5, sticky=E)
        randomRadio.grid(row=6, column=3, pady=5, sticky=E)

        blockSpaceLabel.grid(row=7, column=0, pady=5, padx=5, sticky=E)
        blockSpaceEntry.grid(row=7, column=1, columnspan=2, pady=5)
        blockSpaceButton.grid(row=7, column=3, pady=5)

        replaceLabel.grid(row=8, column=0, pady=5, padx=5, sticky=E)
        replaceEntry.grid(row=8, column=1, columnspan=2, pady=5)
        replaceButton.grid(row=8, column=3, pady=5)

        replaceWithLabel.grid(row=9, column=0, pady=5, padx=5, sticky=E)
        replaceWithEntry.grid(row=9, column=1, columnspan=2, pady=5)
        replaceWithButton.grid(row=9, column=3, pady=5)

        replaceXCheck.grid(row=10, column=1, pady=5, padx=30, sticky=W, columnspan=2)
    elif currentEngine == 5: #Mixer
        mixerLabel.grid(row=5, column=0)


def auto_end_switch(event=None):
    global autoEndBool
    '''Yes'''
    if autoEndBool:
        autoEndBool = False
    else:
        autoEndBool = True


def exclusive_switch(event=None):
    global exclusiveBool
    '''Toggles the switch'''
    if exclusiveBool:
        exclusiveBool = False
    else:
        exclusiveBool = True


def enter_file(event=None):
    global fileName
    global userFileWindow
    global userFileLabel
    global userFileEntry
    global newFileEntry
    '''Chooses the file to use to corrupt'''
    userFileWindow = Tk()
    userFileWindow.title("Enter a Filename")
    userFileWindow.geometry("450x100+250+250")
    userFileWindow.resizable(width=False, height=False)

    instLabel = Label(userFileWindow, text="Enter the name of the file you wish to corrupt, and the name of the corrupted file:")
    userFileEntry = Entry(userFileWindow)
    newFileEntry = Entry(userFileWindow)
    fileButton = Button(userFileWindow, text="Choose File")

    fileButton.bind("<Button-1>", get_file_name)

    instLabel.pack(side=TOP, pady=10)
    userFileEntry.pack(side=LEFT, padx=10)
    newFileEntry.pack(side=LEFT, padx=10)
    fileButton.pack(side=RIGHT, padx=10)

    userFileWindow.mainloop()


def get_file_name(event=None):
    global fileName
    global userFileWindow
    global userFileLabel
    global userFileEntry
    global newFileEntry
    global newFileName
    '''Gets the file name that the user entered'''
    fileName = userFileEntry.get()
    newFileName = newFileEntry.get()
    userFileLabel.config(text=fileName)
    userFileWindow.destroy()
    

def blockSpaceState_to_linear(event=None): #Now this is good coding
    global blockSpaceState
    '''Changes blockSpaceState to Linear'''
    blockSpaceState = "Linear"
    blockSpaceLabel.config(text="Block Space")


def blockSpaceState_to_exponential(event=None):
    global blockSpaceState
    '''Changes blockSpaceState to Exponential'''
    blockSpaceState = "Exponential"
    blockSpaceLabel.config(text="Exponent")


def blockSpaceState_to_random(event=None):
    global blockSpaceState
    '''Changes blockSpaceState to Random'''
    blockSpaceState = "Random"
    blockSpaceLabel.config(text="Upper Bound")


def about_program_window(event=None):
    '''The about window'''
    aboutWindow = Tk()
    aboutWindow.title("About Scares Scrambler Build 9 (v1.0)")

    infoLabel = Label(aboutWindow, text="Program created by your man, Scares. Bugtested by Telic and Ellestice.")
    infoLabel2 = Label(aboutWindow, text="This is an open-source project, so feel free to mess around in the code and stuff.")
    infoLabel3 = Label(aboutWindow, text="If you want to release your own modified version of this project, just credit me! :3")
    goodLogo = PhotoImage(master=aboutWindow, file=resource_path("logo.png"))
    infoLabel4 = Label(aboutWindow, image=goodLogo)

    infoLabel.pack()
    infoLabel2.pack()
    infoLabel3.pack()
    infoLabel4.pack()

    aboutWindow.mainloop()
    

def add_corrupt_engine(baseFile, corruptedFile, blockSpace):
    '''Does adding and subtracting'''

    for y in range(0, int(blockSizeEntry.get())): #Corrupting part
        currentByte = baseFile.read(1) #Gets the byte
        if currentByte == b"":
            break
        currentByte = int.from_bytes(currentByte, byteorder="big")
        currentByte += int(addValueEntry.get())
        if currentByte > 255: #If it's bigger than a byte
            currentByte = currentByte % 256
        currentByte = (currentByte).to_bytes(1, byteorder="big")
        corruptedFile.write(currentByte)

    copy_file_contents(baseFile, corruptedFile, blockSpace) #The gap in between - Shoutout to Jason


def random_corrupt_engine(baseFile, corruptedFile, blockSpace):
    '''Does random byte changes'''
    finished = False

    if finished:
        pass
    else:
        for y in range(0, int(blockSizeEntry.get())): #Corrupting part
            currentByte = baseFile.read(1) #Gets the byte
            if currentByte == b"":
                finished = True
                break
            currentByte = int.from_bytes(currentByte, byteorder="big")
            currentByte += random.randrange(0, 255)
            if currentByte > 255: #If it's bigger than a byte
                currentByte = currentByte % 256
            currentByte = (currentByte).to_bytes(1, byteorder="big")
            corruptedFile.write(currentByte)

        copy_file_contents(baseFile, corruptedFile, blockSpace) #The gap in between


def scrambler_corrupt_engine(baseFile, corruptedFile, blockSpace):
    '''Does scrambles to bytes'''
    currentByteList1 = []
    bufferList = []
    currentByteList2 = []
    finished = False

    if finished:
        pass
    else:
        for y in range(0, int(blockSizeEntry.get())): #Corrupting part
            currentByte = baseFile.read(1)
            if currentByte == b"":
                finished = True
                break
            currentByteList1.append(currentByte) #Gets the bytes

        for z in range(0, int(blockGapEntry.get())): #The gap in between
            currentByte = baseFile.read(1)
            if currentByte == b"":
                finished = True
                break
            bufferList.append(currentByte)

        for y in range(0, int(blockSizeEntry.get())): #Corrupting part
            currentByte = baseFile.read(1)
            if currentByte == b"":
                finished = True
                break
            currentByteList2.append(currentByte) #Gets the bytes
            
        for x in currentByteList2:
            corruptedFile.write(x)

        for x in bufferList:
            corruptedFile.write(x)

        for x in currentByteList1:
            corruptedFile.write(x)

        copy_file_contents(baseFile, corruptedFile, blockSpace) #The gap in between


def copier_corrupt_engine(baseFile, corruptedFile, blockSpace, corruptEndByte):
    '''Does copying stuff'''
    currentByteList1 = []
    bufferList = []
    currentByteList2 = []
    counter = 0
    finished = False

    if finished:
        pass
    else:
        for y in range(0, int(blockSizeEntry.get())):
            currentByte = baseFile.read(1)
            if currentByte == b"":
                finished = True
                break
            currentByteList1.append(currentByte)

        for z in range(0, int(blockGapEntry.get())):
            currentByte = baseFile.read(1)
            if currentByte == b"":
                finished = True
                break
            bufferList.append(currentByte)

        for y in range(0, int(blockSizeEntry.get())):
            currentByte = baseFile.read(1)
            if currentByte == b"":
                finished = True
                break
            currentByteList2.append(currentByte)

        if (int(blockGapEntry.get()) * -1) > int(blockGapEntry.get()): #Negative
            for x in currentByteList2:
                if corruptedFile.tell() >= corruptEndByte:
                    break
                corruptedFile.write(x)
            for x in bufferList:
                if corruptedFile.tell() >= corruptEndByte:
                    break
                corruptedFile.write(x)
            for x in currentByteList2:
                if corruptedFile.tell() >= corruptEndByte:
                    break
                corruptedFile.write(x)
        else: #Positive
            for x in currentByteList1:
                if corruptedFile.tell() >= corruptEndByte:
                    break
                corruptedFile.write(x)
            for x in bufferList:
                if corruptedFile.tell() >= corruptEndByte:
                    break
                corruptedFile.write(x)
            for x in currentByteList1:
                if corruptedFile.tell() >= corruptEndByte:
                    break
                corruptedFile.write(x)

        copy_file_contents(baseFile, corruptedFile, blockSpace)


def tilter_corrupt_engine(baseFile, corruptedFile, blockSpace):
    '''You know what it does by now'''
    finished = False

    if finished:
        pass
    else:
        for y in range(0, int(blockSizeEntry.get())): #Corrupting part
            currentByte = baseFile.read(1) #Gets the byte
            if currentByte == b"":
                break
            currentByte = int.from_bytes(currentByte, byteorder="big")

            if exclusiveBool:
                compareByte = int(replaceEntry.get())
                if currentByte == compareByte:
                    currentByte = int(replaceWithEntry.get())
            else:
                currentByte = int(replaceWithEntry.get())
                
            currentByte = (currentByte).to_bytes(1, byteorder="big")
            corruptedFile.write(currentByte)

        copy_file_contents(baseFile, corruptedFile, blockSpace)


def copy_file_contents(baseFile, corruptedFile, endValue):
    '''For copying uncorrupted parts of a file'''
    
    for z in range(0, endValue): #The gap in between
        currentByte = baseFile.read(1)
        corruptedFile.write(currentByte) #The gap in between


def corrupt_file(event=None):
    global newFileName
    '''Corrupts the chosen file'''

    nullCounter2 = 0

    try:
    
        if fileName == "":
            messagebox.showinfo("Woah there buddy!", "You need to select a file first before"
                                " you corrupt it! Press Alt+F to select a file.")
        else:
            baseFile = open(fileName, "rb+")
            if newFileName == "":
                corruptedFile = open("CorruptedFile.txt", "wb+")
            else:
                corruptedFile = open(newFileName, "wb+")

            baseFile.seek(int(startValueEntry.get())) #Goto the start byte
            if not autoEndBool: #If auto end is turned off
                corruptEndByte = int(endValueEntry.get())

            else: #If auto end is on
                nullCounter = int(startValueEntry.get())
                while True:
                    nullTester = baseFile.read(1)
                    if nullTester != b"": #If the byte isn't empty
                        nullCounter = baseFile.tell()
                    else:
                        break
                corruptEndByte = nullCounter
                    
            baseFile.seek(0) #Goto the start byte
            if currentEngine <= 5: #All current engines

                copy_file_contents(baseFile, corruptedFile, int(startValueEntry.get()))
                
                if blockSpaceState == "Linear":
                    corruptStepSize = int(blockSizeEntry.get()) + int(blockSpaceEntry.get())
                    for x in range(int(startValueEntry.get()), corruptEndByte, corruptStepSize): #Through the file

                        if currentEngine == 0:
                            add_corrupt_engine(baseFile, corruptedFile, int(blockSpaceEntry.get()))
                        elif currentEngine == 1:
                            random_corrupt_engine(baseFile, corruptedFile, int(blockSpaceEntry.get()))
                        elif currentEngine == 2:
                            scrambler_corrupt_engine(baseFile, corruptedFile, int(blockSpaceEntry.get()))
                        elif currentEngine == 3:
                            copier_corrupt_engine(baseFile, corruptedFile, int(blockSpaceEntry.get()), corruptEndByte)
                        elif currentEngine == 4:
                            tilter_corrupt_engine(baseFile, corruptedFile, int(blockSpaceEntry.get()))

                elif blockSpaceState == "Exponential":
                    nullCounter = baseFile.tell()
                    exponentPower = float(blockSpaceEntry.get())
                    exponentCounter = 1
                    exponentCap = False
                    exponentCapValue = 1000000

                    while nullCounter < corruptEndByte: #Through the file

                        if int(exponentCounter**exponentPower) > exponentCapValue: #If exponent is too big
                            exponentCap = True

                        if not exponentCap:
                            if currentEngine == 0:
                                add_corrupt_engine(baseFile, corruptedFile, int(exponentCounter**exponentPower))
                            elif currentEngine == 1:
                                random_corrupt_engine(baseFile, corruptedFile, int(exponentCounter**exponentPower))
                            elif currentEngine == 2:
                                scrambler_corrupt_engine(baseFile, corruptedFile, int(exponentCounter**exponentPower))
                            elif currentEngine == 3:
                                copier_corrupt_engine(baseFile, corruptedFile, int(exponentCounter**exponentPower), corruptEndByte)
                            elif currentEngine == 4:
                                tilter_corrupt_engine(baseFile, corruptedFile, int(exponentCounter**exponentPower))
                        else:
                            if currentEngine == 0:
                                add_corrupt_engine(baseFile, corruptedFile, exponentCapValue)
                            elif currentEngine == 1:
                                random_corrupt_engine(baseFile, corruptedFile, exponentCapValue)
                            elif currentEngine == 2:
                                scrambler_corrupt_engine(baseFile, corruptedFile, exponentCapValue)
                            elif currentEngine == 3:
                                copier_corrupt_engine(baseFile, corruptedFile, exponentCapValue, corruptEndByte)
                            elif currentEngine == 4:
                                tilter_corrupt_engine(baseFile, corruptedFile, exponentCapValue)


                        if exponentCap:
                            nullCounter += exponentCapValue
                        else:
                            nullCounter += int(exponentCounter**exponentPower)
                            exponentCounter += 1

                elif blockSpaceState == "Random":
                    nullCounter = int(startValueEntry.get())
                    
                    while nullCounter < corruptEndByte: #Through the file

                        tempRand = random.randrange(0, int(blockSpaceEntry.get()))
                        
                        if currentEngine == 0:
                            add_corrupt_engine(baseFile, corruptedFile, tempRand)
                        elif currentEngine == 1:
                            random_corrupt_engine(baseFile, corruptedFile, tempRand)
                        elif currentEngine == 2:
                            scrambler_corrupt_engine(baseFile, corruptedFile, tempRand)
                        elif currentEngine == 3:
                            copier_corrupt_engine(baseFile, corruptedFile, tempRand, corruptEndByte)
                        elif currentEngine == 4:
                            tilter_corrupt_engine(baseFile, corruptedFile, tempRand)

                        nullCounter += tempRand
                        
                while True: #This finishes the uncorrupted part
                    currentByte = baseFile.read(1)
                    if currentByte == b"":
                        break
                    corruptedFile.write(currentByte)
    

        baseFile.close()
        corruptedFile.close()
        
    except ValueError:
        messagebox.showwarning("Woah there partner!", "The values you entered were not valid.")
        

parentMenu = Menu(root)

fileMenu = Menu(parentMenu, tearoff=0)
aboutMenu = Menu(parentMenu, tearoff=0)
parentMenu.add_cascade(label="File", menu=fileMenu)
parentMenu.add_cascade(label="About", menu=aboutMenu)

fileMenu.add_command(label="Choose File", accelerator="Alt+F", command=enter_file)
fileMenu.add_separator()
fileMenu.add_command(label="Save Presets", foreground="grey50")
fileMenu.add_command(label="Reset Presets", foreground="grey50")

aboutMenu.add_command(label="Info", accelerator="Alt+I", command=about_program_window)

#----------------------------------------------------------------------------------

mainFrame = Frame(root, width=310, height=500)
corruptButtonFrame = Frame(root)

goodBanner = PhotoImage(file=resource_path("banner.png"))
bannerLabel = Label(root, image=goodBanner)

engineLeftButton = Button(mainFrame, text="<")
engineLabel = Label(mainFrame, text="Incrementer Engine")
engineRightButton = Button(mainFrame, text=">")

startValueLabel = Label(mainFrame, text="Start Value")
startValueEntry = Entry(mainFrame)
startValueClass = entry_function_class(startValueEntry)
startValueEntry.insert(0, 0)
startValueButton = Button(mainFrame, text="+/-")

endValueLabel = Label(mainFrame, text="End Value")
endValueEntry = Entry(mainFrame)
endValueClass = entry_function_class(endValueEntry)
endValueEntry.insert(0, 0)
endValueButton = Button(mainFrame, text="+/-")

incValueLabel = Label(mainFrame, text="Inc Value")
incValueEntry = Entry(mainFrame)
autoEndCheck = Checkbutton(mainFrame, text="Auto End")

blockSizeLabel = Label(mainFrame, text="Block Size")
blockSizeEntry = Entry(mainFrame)
blockSizeClass = entry_function_class(blockSizeEntry)
blockSizeButton = Button(mainFrame, text="Random")

linearRadio = Radiobutton(mainFrame, text="Linear", value=1, variable=1)
exponentialRadio = Radiobutton(mainFrame, text="Exponential", value=2, variable=1)
randomRadio = Radiobutton(mainFrame, text="Random", value=3, variable=1)

blockSpaceLabel = Label(mainFrame, text="Block Space")
blockSpaceEntry = Entry(mainFrame)
blockSpaceClass = entry_function_class(blockSpaceEntry)
blockSpaceButton = Button(mainFrame, text="Random")

addValueLabel = Label(mainFrame, text="Add/Subtract")
addValueEntry = Entry(mainFrame)
addValueClass = entry_function_class(addValueEntry)
addValueButton = Button(mainFrame, text="Random")

blockGapLabel = Label(mainFrame, text="Block Gap")
blockGapEntry = Entry(mainFrame)
blockGapClass = entry_function_class(blockGapEntry)
blockGapButton = Button(mainFrame, text="Random")

replaceXCheck = Checkbutton(mainFrame, text="Exclusive")

replaceLabel = Label(mainFrame, text="Replace")
replaceEntry = Entry(mainFrame)
replaceClass = entry_function_class(replaceEntry)
replaceButton = Button(mainFrame, text="Random")

replaceWithLabel = Label(mainFrame, text="Replace with")
replaceWithEntry = Entry(mainFrame)
replaceWithClass = entry_function_class(replaceWithEntry)
replaceWithButton = Button(mainFrame, text="Random")

mixerLabel = Label(mainFrame, text="Currently a WIP")

userFileLabel = Label(corruptButtonFrame, text=fileName)
corruptButton = Button(corruptButtonFrame, text="Corrupt", font="Helvetica 25")

#----------------------------------------------------------------------------------

engineLeftButton.bind("<Button-1>", change_engine_left)
engineRightButton.bind("<Button-1>", change_engine_right)

startValueButton.bind("<Button-1>", startValueClass.left_click_function)
endValueButton.bind("<Button-1>", endValueClass.left_click_function)
startValueButton.bind("<Button-3>", startValueClass.right_click_function)
endValueButton.bind("<Button-3>", endValueClass.right_click_function)

autoEndCheck.bind("<Button-1>", auto_end_switch)

blockSizeButton.bind("<Button-1>", blockSizeClass.generate_random_byte)
blockSpaceButton.bind("<Button-1>", blockSpaceClass.generate_random_byte)

linearRadio.bind("<Button-1>", blockSpaceState_to_linear)
exponentialRadio.bind("<Button-1>", blockSpaceState_to_exponential)
randomRadio.bind("<Button-1>", blockSpaceState_to_random)

addValueButton.bind("<Button-1>", addValueClass.generate_random_byte)
blockGapButton.bind("<Button-1>", blockGapClass.generate_random_byte)

replaceXCheck.bind("<Button-1>", exclusive_switch)
replaceButton.bind("<Button-1>", replaceClass.generate_random_byte)
replaceWithButton.bind("<Button-1>", replaceWithClass.generate_random_byte)

corruptButton.bind("<Button-1>", corrupt_file)

#------------------------------------------------------------------------------------

bannerLabel.pack()

mainFrame.pack()
corruptButtonFrame.pack(side=BOTTOM)

engineLeftButton.grid(row=0, column=0, pady=5)
engineLabel.grid(row=0, column=1, columnspan=2, pady=5)
engineRightButton.grid(row=0, column=3, pady=5)

startValueLabel.grid(row=1, column=0, padx=5, pady=5, sticky=E)
startValueEntry.grid(row=1, column=1, columnspan=2, pady=5)
startValueButton.grid(row=1, column=3, padx=20, pady=5)

endValueLabel.grid(row=2, column=0, padx=5, pady=5, sticky=E)
endValueEntry.grid(row=2, column=1, columnspan=2, pady=5)
endValueButton.grid(row=2, column=3, padx=20, pady=5)

incValueLabel.grid(row=3, column=0, pady=5, padx=5, sticky=E)
incValueEntry.grid(row=3, column=1, columnspan=2, pady=5)
autoEndCheck.grid(row=3, column=3, pady=5)

Label(mainFrame, text="------------------------------------------------------------").grid(row=4,
                                                        column=0, pady=5, columnspan=4)
update_layout()

userFileLabel.pack(pady=5)
corruptButton.pack(pady=5)

root.config(menu=parentMenu)

root.bind("<Alt-f>", enter_file)
root.bind("<Alt-i>", about_program_window)

root.mainloop()









