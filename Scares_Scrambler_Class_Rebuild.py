
#!py -3.4

import os
import random

import tkinter as Tkinter
from tkinter import *
from tkinter import (Tk, messagebox, ttk)
from tkinter.filedialog import askopenfilename

from Engine_Class_File import * #Import all the important classes I made haha
from Theme_Class_File import *

'''Hello, anyone reading this! Don't mind the disgusting code in some places; I'm not that good at coding, so don't expect it to work perfectly
and/or look pretty! Anyways, hopefully you'll find some enjoyment messing around with this corrupter. Have fun!'''

buildNumber = "15"
versionNumber = "v1.102"
goodIcon = "favi16.ico"

'''for x in range(0, len(__file__)): #Getting the folder path, so that pictures work properly on cmd
    #print(__file__[-x])
    if __file__[-x] == r"\\":
        folderPath = __file__[:-x] + r"\\"
        break'''


root = Tk()
root.title("Scares Scrambler Build "+buildNumber)
root.geometry("310x600+100+100")
root.iconbitmap(goodIcon)
#root.resizable(width=False, height=False)

'''
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

currentEngine = IntVar() #Haha
currentEngine.set(1) #Set to incrememnter
previousEngine = currentEngine.get() #So that we can clear the window
hexadecimalMode = False

fileName = ""
newFileName = ""
newPresetName = ""

cnameLabel = ""

class entry_function_class: #Move this class to Class_File later
    
    def __init__(self, entryBox):
        self.entryBox = entryBox

    def left_click_function(self, event=None):
        '''Increments the entries'''
        try:
            if hexadecimalMode:
                incValue = incValueEntry.get()
                entryBoxValue = self.entryBox.get()
                incValue = int(float.fromhex(incValue))
                entryBoxValue = int(float.fromhex(entryBoxValue))
                endValue = int(float.fromhex(endValueEntry.get()))
                entryBoxValue += incValue
                self.entryBox.delete(0, "end")
                if entryBoxValue > endValue:
                    if endValue != 0: #Preventing division by zero error
                        entryBoxValue = entryBoxValue % endValue #Thanks Telic
                    else:
                        entryBoxValue = 0
                entryBoxValue = hex_convert(entryBoxValue)
            else:
                incValue = int(incValueEntry.get()) #Getting values
                entryBoxValue = int(self.entryBox.get())
                entryBoxValue += incValue #Setting values
                self.entryBox.delete(0, "end")
                if entryBoxValue > int(endValueEntry.get()):
                    
                    if int(endValueEntry.get()) != 0: #Preventing division by zero error
                        entryBoxValue = entryBoxValue % int(endValueEntry.get())
                    else:
                        entryBoxValue = 0
            self.entryBox.insert(0, entryBoxValue)
        except ValueError:
            messagebox.showwarning("What are you doing?", "Please use a whole number for"
                                   " the increment value, thanks!")


    def right_click_function(self, event=None):
        '''Decrements the values'''
        try:
            if hexadecimalMode:
                incValue = incValueEntry.get()
                entryBoxValue = self.entryBox.get()
                incValue = int(float.fromhex(incValue))
                entryBoxValue = int(float.fromhex(entryBoxValue))
                entryBoxValue -= incValue
                self.entryBox.delete(0, "end")
                if entryBoxValue < 0:
                    entryBoxValue = 0
                entryBoxValue = hex_convert(entryBoxValue)
            else:
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
        if hexadecimalMode:
            ran1 = random.randint(0, 15)
            ran2 = random.randint(0, 15)
            ran1 = singular_hex_convert(ran1)
            ran2 = singular_hex_convert(ran2)

            self.entryBox.insert(0, str(ran1)+str(ran2))
        else:
            self.entryBox.insert(0, random.randint(0, 255))


def switch_algorithm(event=None):
    '''The function that's called when the algorithm switches'''
    global previousEngine
    global engineLabel

    whiteSpace = 25-len(algorithms[currentEngine.get()-1].name)
    if whiteSpace < 0:
        whiteSpace = 0
        
    engineLabel["text"]=algorithms[currentEngine.get()-1].name+whiteSpace*" "
    algorithms[previousEngine-1].hide_layout()
    algorithms[currentEngine.get()-1].display_layout(colorList)
    previousEngine = currentEngine.get() #Preparing for next switch


def auto_end_switch(event=None):
    '''Calculates the end of the selected file automatically'''
    baseFile = open(fileName, "rb+")
    nullCounter = 0
    inc = 1000
    while True: #Getting rough value
        nullTester = baseFile.read(inc)
        if nullTester != b"": #If the byte isn't empty
            nullCounter = baseFile.tell()
        else:
            break
    
    if nullCounter-inc < 0: #Making sure the argument isn't a negative number
        nullTester = baseFile.seek(0)
    else:
        nullTester = baseFile.seek(nullCounter-inc)

    while True: #Getting precise value
        if nullTester != b"": #If the byte isn't empty
            nullCounter = baseFile.tell()
        else:
            break
        nullTester = baseFile.read(1)

    endValueEntry.delete(0, "end")
    if hexadecimalMode:
        nullCounter = hex_convert(nullCounter)
    endValueEntry.insert(0, nullCounter)
    baseFile.close()
        

def hexadecimal_switch(event=None):
    global hexadecimalMode
    '''Toggles the switch'''
    if hexadecimalMode:
        for x in algorithms: #Converts hexes already in entries to decimals
            x.hexadecimalMode = False #Changing each algorithm's internal switch
            for y in x.entries:
                nonHex = get_value(y[1], isInt=False)
                
                if nonHex != "": #Preventing errors when switching between hex and dec
                    if nonHex == int(nonHex): #Changing to ints if necessary
                        y[1].delete(0, END)
                        y[1].insert(0, int(nonHex))
                    else:
                        y[1].delete(0, END)
                        y[1].insert(0, nonHex)

        nonHex = get_value(startValueEntry, isInt=True)
        startValueEntry.delete(0, END)
        startValueEntry.insert(0, nonHex)
        nonHex = get_value(endValueEntry, isInt=True)
        endValueEntry.delete(0, END)
        endValueEntry.insert(0, nonHex)
        nonHex = get_value(incValueEntry, isInt=True)
        incValueEntry.delete(0, END)
        incValueEntry.insert(0, nonHex)
        hexadecimalMode = False
        
    else:
        for x in algorithms: #Converts decimals in entries to hexes
            x.hexadecimalMode = True #Changing each algorithm's internal switch
            for y in x.entries:
                coolHex = hex_convert(y[1].get())
                y[1].delete(0, END)
                y[1].insert(0, coolHex)

        coolHex = hex_convert(startValueEntry.get())
        startValueEntry.delete(0, END)
        startValueEntry.insert(0, coolHex)
        coolHex = hex_convert(endValueEntry.get())
        endValueEntry.delete(0, END)
        endValueEntry.insert(0, coolHex)
        coolHex = hex_convert(incValueEntry.get())
        incValueEntry.delete(0, END)
        incValueEntry.insert(0, coolHex)
        hexadecimalMode = True


def check_for_period(text):
    '''Checks to see if there's a period in the given text'''
    isDot = False
    position = 0
    for x in range(len(text)-1, -1, -1):
        if text[x] == ".":
            isDot = True
            position = x
            break

    if isDot:
        return position
    else:
        return False


def clear_textWidget(event, textWidget):
    '''Clears newFileText when it's clicked'''
    #Make it only clear when the text is the default message
    textWidget.delete("1.0", END)
    textWidget.unbind("<Button-1>") #Prevents text from clearning when there's important info


def shorten_text(text, length, shorten="Front"):
    '''Shortens text to make my life easier'''
    if len(text) < length:
        dots = ""
    else:
        dots = "..."
        
    if shorten == "Front":
        return dots+text[-length:]
    elif shorten == "Back":
        return text[:length]+dots


def enter_file(event=None):
    global fileName
    global userFileWindow
    #global userFileEntry
    #global newFileText
    global fileName
    global newFileName
    global cnameLabel
    '''Chooses the files to use during corrupting'''
    userFileWindow = Tk()
    userFileWindow.title("Enter filenames...")
    userFileWindow.geometry("450x200+250+250")
    userFileWindow.iconbitmap(goodIcon)
    userFileWindow.resizable(width=False, height=False)

    mainFrame = Frame(userFileWindow)
    applyFrame = Frame(userFileWindow)

    instLabel = Label(mainFrame, text="Select the file you wish to corrupt, and enter the name of the new file:")
    cfileLabel = Label(mainFrame, text="File To Corrupt:")
    
    if fileName == "":
        cnameLabel = Label(mainFrame, text="No File Selected")
    else:
        t = shorten_text(fileName, 25, "Front")
        cnameLabel = Label(mainFrame, text=t)

    userFileButton = Button(mainFrame, text="Select File")
    nfileLabel = Label(mainFrame, text="New File Path:")
    nfileLabel2 = Label(mainFrame, text="New File Name:")
    newFileButton = Button(mainFrame, text="Select Folder")
    
    t = shorten_text(newFileName, 25, "Front")
    newFilePath = Label(mainFrame, text=t)

    newFileText = Text(mainFrame)
    applyButton = Button(applyFrame, text=" Apply ")

    userFileWindow.config(bg=colorList[2])
    mainFrame.config(bg=colorList[2])
    applyFrame.config(bg=colorList[2])
    instLabel.config(bg=colorList[2], fg=colorList[1])
    cfileLabel.config(bg=colorList[2], fg=colorList[1])
    cnameLabel.config(bg=colorList[2], fg=colorList[1])
    userFileButton.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[2], activeforeground=colorList[1])
    nfileLabel.config(bg=colorList[2], fg=colorList[1])
    nfileLabel2.config(bg=colorList[2], fg=colorList[1])
    newFilePath.config(bg=colorList[2], fg=colorList[1])
    newFileText.config(bg=colorList[0], fg=colorList[1], insertbackground=colorList[1], selectbackground=colorList[5])
    newFileButton.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[2], activeforeground=colorList[1])
    applyButton.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[2], activeforeground=colorList[1])

    userFileButton.bind("<Button-1>", select_file)
    newFileButton.bind("<Button-1>", lambda _: folder_selector([newFileText], [newFilePath]))
    applyButton.bind("<Button-1>", lambda _: get_file_name(newFileText))

    newFileText.config(width=25, height=1)

    if newFileName == "":
        newFileText.insert(END, "Enter new file name...")
        newFileText.bind("<Button-1>", lambda x: clear_textWidget(x, newFileText))
    else:
        newFileText.insert(END, newFileName)


    mainFrame.pack()
    applyFrame.pack()

    instLabel.grid(row=1, column=1, columnspan=10, padx=40, pady=10)
    cfileLabel.grid(row=2, column=1, columnspan=2, padx=0, pady=5)
    cnameLabel.grid(row=2, column=3, columnspan=5, padx=10, pady=5)
    userFileButton.grid(row=2, column=8, padx=20, pady=5)
    
    nfileLabel.grid(row=3, column=1, columnspan=2, padx=0, pady=5)
    newFilePath.grid(row=3, column=4, columnspan=2, padx=5, pady=5)
    newFileButton.grid(row=3, column=8, padx=5, pady=5)

    nfileLabel2.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
    newFileText.grid(row=4, column=3, columnspan=5, padx=28, pady=5)
    applyButton.grid(row=5, column=1, columnspan=1, padx=10, pady=15)

    userFileWindow.mainloop()


def select_file(event=None):
    global fileName
    '''Opens an 'open' window to select the file to corrupt'''
    fileName = askopenfilename()
    cnameLabel["text"] = shorten_text(fileName, 25, "Front")
    if autoEndVar.get() == 1: #If the user requests to always get auto ends
        auto_end_switch() 
    

def get_file_name(text, event=None):
    global userFileWindow
    global userFileLabel
    #global newFileText
    global newFileName
    global fileName
    '''Gets the file name that the user entered'''
    newFileName = text.get(1.0, END)[:-1]
    p = check_for_period(newFileName)

    if p == False:
        pp = check_for_period(fileName)
        newFileName += fileName[pp:]
        print(newFileName)

    if fileName == "":
        userFileLabel.config(text="No file loaded. Press Alt+F to load one!")
    else:
        hide_userFileLabel()
        
    userFileWindow.destroy()


def about_program_window(event=None):
    '''The about window'''
    aboutWindow = Tk()
    
    aboutWindow.title("About Scares Scrambler Build "+buildNumber+" "+"("+versionNumber+")")
    aboutWindow.iconbitmap(goodIcon)

    infoLabel = Label(aboutWindow, text="Program created by your man, Scares. Bugtested by Telic, Ellex, Tyler, and Scott")
    infoLabel2 = Label(aboutWindow, text="This is an open-source project, so feel free to mess around in the code and stuff.")
    infoLabel3 = Label(aboutWindow, text="If you want to release your own modified version of this project, just credit me! :3")
    infoLabel4 = Label(aboutWindow, text="I'd also like to extend a huge thank you to anyone who bothered to try this thing!")
    infoLabel5 = Label(aboutWindow, text="I know this isn't the best corrupter out there, but I tried to make it as special as I could.")
    infoLabel7 = Label(aboutWindow, text="Thank you for being a part of this project. Here's to another year of crappy software!")

    aboutWindow["bg"] = colorList[2]
    goodLogo = PhotoImage(master=aboutWindow, file=colorList[4])
    infoLabel.config(bg=colorList[2], fg=colorList[1])
    infoLabel2.config(bg=colorList[2], fg=colorList[1])
    infoLabel3.config(bg=colorList[2], fg=colorList[1])
    infoLabel4.config(bg=colorList[2], fg=colorList[1])
    infoLabel5.config(bg=colorList[2], fg=colorList[1])
    infoLabel6 = Label(aboutWindow, image=goodLogo)
    infoLabel7.config(bg=colorList[2], fg=colorList[1])

    infoLabel.pack()
    infoLabel2.pack()
    infoLabel3.pack()
    infoLabel4.pack()
    infoLabel5.pack()
    infoLabel6.pack()
    infoLabel7.pack()

    aboutWindow.mainloop()


'''def copy_file_contents(baseFile, corruptedFile, endValue):
    #For copying uncorrupted parts of a file
    
    for z in range(0, endValue): #The gap in between
        currentByte = baseFile.read(1)
        corruptedFile.write(currentByte) #The gap in between'''


def hex_convert(number):
    '''Converts the input to hexadecimal.'''
    '''Might not work 100% yet'''
    
    if number != "": #Prevents errors when switching between hex and dec
        tempNum = float(number)
        newNum = [] #Holds the converted number
        if tempNum < 0:
            returnNum = "-0x" #The number to return
        else:
            returnNum = "0x"
        decimalCounter = 0 #Counts the number of digits past the decimal

        while tempNum % 1 != 0: #White the number still has decimal places
            tempNum = tempNum * 16
            decimalCounter += 1

        while tempNum != 0: #Loop until whole number is converted
            newNum.append(singular_hex_convert(tempNum%16)) #Adding each digit in reverse order
            tempNum = tempNum // 16 #Add a rounding element somewhere

        if newNum == []: #If the number is zero
            return "0x0"

        for x in range(len(newNum)-1, -1, -1): #Going in reverse order through newNum
            returnNum += newNum[x]
            if x == decimalCounter and x != 0: #Adding the decimal back
                returnNum += "."

    else:
        returnNum = ""
            
    return returnNum


'''def singular_hex_convert(n):
    #Converts the numbers 10 to 15 to hex
    newN = str(int(n))
    if newN == "10":
        newN = "a"
    elif newN == "11":
        newN = "b"
    elif newN == "12":
        newN = "c"
    elif newN == "13":
        newN = "d"
    elif newN == "14":
        newN = "e"
    elif newN == "15":
        newN = "f"

    return newN'''


def get_value(entry, isInt=True):
    '''Gets the value from an entry, and converts to decimal if necessary'''
    if entry.get() != "": #Preventing erros while switching between hex and dec
        if hexadecimalMode:
            if isInt:
                return int(float.fromhex(entry.get()))
            else:
                return float.fromhex(entry.get())

        else:
            if isInt:
                return int(entry.get())
            else:
                return float(entry.get())

    else:
        return ""
        

def corrupt_file(event=None):
    global newFileName
    '''Corrupts the chosen file'''

    tempIndex = 0 #Holds the index for specific variables
    theEngine = algorithms[currentEngine.get()-1] #The current algorithm being used

    try:
        startValue = get_value(startValueEntry)
        endValue = get_value(endValueEntry)
        if startValue > endValue:
            startValueEntry.delete(0, END)
            startValueEntry.insert(endValueEntry.get())

        #Mandatory stuff
        tempIndex = find_engine_index(theEngine, "Block Size", "Entry") 
        blockSize = get_value(theEngine.entries[tempIndex][1])

        tempIndex = find_engine_index(theEngine, "Block Space", "Alts") #Checking alts in case the label is different
        blockSpace = get_value(theEngine.entries[tempIndex][1])

        blockSpaceState = theEngine.radioButtonVariables[tempIndex].get()
        if blockSpaceState == 2: #Exponential
            blockSpace = get_value(theEngine.entries[tempIndex][1], False)
        else:
            blockSpace = get_value(theEngine.entries[tempIndex][1])

        if blockSpace < 1:
            blockSpace = 1 #Fixing negative exponents and stuff

        corruptingVariables = theEngine.get_corruption_variables()
        #print(corruptingVariables)
        for x in range(0, len(corruptingVariables)): #Converting variables to usable stuff
            for y in range(0, len(corruptingVariables[x])):
                if x == 0:
                    corruptingVariables[x][y] = get_value(corruptingVariables[x][y]) #Changing from hex if necessary
                else:
                    corruptingVariables[x][y] = corruptingVariables[x][y].get()

        #print(corruptingVariables)

        if fileName == "":
            messagebox.showinfo("Woah there buddy!", "You need to select a file first before"
                                " you corrupt it! Press Alt+F to select a file.")
        else:
            baseFile = open(fileName, "rb+")
            if newFileName == "" or newFileName == "Enter new file name...":
                corruptedFile = open("CorruptedFile.txt", "wb+")
            else:
                #FULL FILE PATHS WORK I THINK :)
                corruptedFile = open(newFileName, "wb+")
                    
            baseFile.seek(0) #Goto the start byte
            copy_file_contents(baseFile, corruptedFile, startValue) #Add all stuff before start value
            currentPos = 0 #Keeps track of where we are in the file currently
            previousPos = 0 #Keeps track of the previous position in the file

            exponentCounter = 1 #For exponential spacing
            exponentCapValue = 1000000 #Fix this lovely hardcoding
            tempSpace = 0 #BlockSpace used by the functions below

            if blockSpaceState == 1: #Put this out here since it only needs to be done once
                tempSpace = blockSpace

            while True: #Main corruption loop

                if blockSpaceState == 2: #Exponential
                    #blockSpace = exponent
                    #tempSpace = exponentValue
                    
                    if tempSpace != exponentCapValue:
                        try: #Fixes the exponent from getting too big
                            if int(exponentCounter**blockSpace) > exponentCapValue: #If exponent is too big
                                tempSpace = exponentCapValue
                            else:
                                tempSpace = int(exponentCounter**blockSpace) #Check this if errors occur
                                exponentCounter += 1
                        except OverflowError:
                            tempSpace = exponentCapValue

                elif blockSpaceState == 3: #Random
                    tempSpace = random.randrange(0, blockSpace+1)

                if theEngine.name == "Copier Algorithm":
                    theEngine.corrupt(corruptingVariables, tempSpace, baseFile, corruptedFile, endValue) #The thing that actually does the corrupting
                else:
                    theEngine.corrupt(corruptingVariables, tempSpace, baseFile, corruptedFile) 

                currentPos = baseFile.tell() #Getting current pos

                if (currentPos+blockSize) >= endValue or currentPos == previousPos: #If we've reached the end of the corrupting
                    break

                previousPos = currentPos

            while True: #This finishes the uncorrupted part
                currentByte = baseFile.read(1)
                if currentByte == b"":
                    break
                corruptedFile.write(currentByte)

        baseFile.close()
        corruptedFile.close()
        
    except ValueError:
        messagebox.showwarning("Woah there partner!", "The values you entered were not valid. Make sure that all the values were entered correctly. "
                               "Some values can't be decimals, so uh... check that as well.")
    except IndexError:
        messagebox.showwarning("Woah there partner!", "Make sure to fill in the required values!")


def save_presets_window(event=None):
    global newPresetName
    global newPresetEntry
    global newPresetWindow
    '''The UI for saving a preset'''
    
    newPresetWindow = Tk()
    newPresetWindow.title("Enter preset name...")
    newPresetWindow.geometry("300x100+250+250")
    newPresetWindow.iconbitmap(goodIcon)
    newPresetWindow.resizable(width=False, height=False)

    newPresetName = ""
    newPresetLabel = Label(newPresetWindow, text="Enter the name of the new preset file:")
    newPresetEntry = Entry(newPresetWindow)
    newPresetButton = Button(newPresetWindow, text=" Ok ")
    newPresetButton.bind("<Button-1>", lambda _: save_presets(newPresetEntry)) #The _ is catching an usused argument

    newPresetWindow.config(bg=colorList[2])
    newPresetEntry.config(bg=colorList[0], fg=colorList[1], insertbackground=colorList[1], selectbackground=colorList[5])
    newPresetLabel.config(bg=colorList[2], fg=colorList[1])
    newPresetButton.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[2], activeforeground=colorList[1])

    newPresetLabel.pack()
    newPresetEntry.pack(pady=5)
    newPresetButton.pack()

    newPresetWindow.mainloop()


def save_presets(newPresetEntry, event=None):
    '''Saves the presets to a text file'''
    
    presetList = []
    theEngine = algorithms[currentEngine.get()-1]

    presetList.append("~~preset14~~")
    presetList.append(fileName)
    presetList.append(newFileName)

    presetList.append(startValueEntry.get())
    presetList.append(endValueEntry.get())
    presetList.append(incValueEntry.get())

    presetList.append("~~"+theEngine.name+"~~") #Signifying the start of algorithm specific stuff
    presetList.append("~~Entries~~") #Start of entry section
    for x in range(0, len(theEngine.entries)): #Iterating through all entries
        presetList.append(theEngine.entries[x][1].get())

    presetList.append("~~Radiobuttons~~") #Start of radiobutton section
    for x in theEngine.radioButtonVariables: #Iterating through all radiobutton variables
        if x == None:
            presetList.append("None")
        else:
            presetList.append(x.get())

    presetList.append("~~Checkbuttons~~") #Start of checkbutton section
    for x in theEngine.checkButtonVariables:
        if x == None:
            presetList.append("None")
        else:
            presetList.append(x.get())

    presetList.append(hexadecimalMode) #Add hexadecimal mode
    name = newPresetEntry.get()

    if name[-4:] == ".txt": #If there's a file extension
        presetFile = open(name, "w")
    else:
        presetFile = open(name+".txt", "w")

    for x in presetList:
        presetFile.write(str(x)+"\n")

    #preaetFile.write("~~End~~")

    presetFile.close()
    newPresetWindow.destroy() #Close the preset window


def load_presets(event=None, coolName=""):
    global fileName
    global newFileName
    global startValueEntry
    global endValueEntry
    global incValueEntry
    global hexadecimalMode
    global hexVar

    global userFileLabel
    global currentEngine
    '''Loads the presets from the text file'''
    #Fix all the try/excepts later
    
    manualSelect = False

    try:
        if coolName == "": #If no name was entered
            presetFile = askopenfilename()
            presetFile = open(presetFile, "r")
            manualSelect = True
        else: #Use the name given
            presetFile = open(coolName, "r")

        try:
            tempVar = ""
            tag = presetFile.readline()
            if tag == "~~preset~~\n": #The preset used in Build 13 and below
                fileName = presetFile.readline()[:-1]
                newFileName = presetFile.readline()[:-1]
                startValueEntry.delete(0, END)
                startValueEntry.insert(0, presetFile.readline()[:-1])
                endValueEntry.delete(0, END)
                endValueEntry.insert(0, presetFile.readline()[:-1])
                incValueEntry.delete(0, END)
                incValueEntry.insert(0, presetFile.readline()[:-1])
                presetFile.readline() #Useless auto end toggle

                blockSize = presetFile.readline()[:-1] #Getting blockSize
                spaceType = presetFile.readline()[:-1] #Getting linear, exponential, random (blockSpaceState)
                if spaceType == "Linear":
                    spaceType = 1
                elif spaceType == "Exponential":
                    spaceType = 2
                else:
                    spaceType = 3

                blockSpace = presetFile.readline()[:-1] #Getting blockSpace
                incEngine.entries[2][1].delete(0, END)
                incEngine.entries[2][1].insert(0, presetFile.readline()[:-1]) #Add/subtract

                blockGap = presetFile.readline()[:-1] #Getting blockGap

                exclusiveBool = presetFile.readline()[:-1] #Exclusive switch
                if exclusiveBool == "True":
                    tiltEngine.checkButtonVariables[3].set(1)
                else:
                    tiltEngine.checkButtonVariables[3].set(0)

                tiltEngine.entries[2][1].delete(0, END)
                tiltEngine.entries[2][1].insert(0, presetFile.readline()[:-1]) #Replace
                tiltEngine.entries[3][1].delete(0, END)
                tiltEngine.entries[3][1].insert(0, presetFile.readline()[:-1]) #Replace with

                if presetFile.readline()[:-1] == "True": #Hexadecimal mode
                    hexadecimalMode = True
                    hexVar.set(1)
                else:
                    hexadecimalMode = False
                    hexVar.set(0)
                    
                for x in algorithms: #Setting variables found above
                    x.entries[0][1].delete(0, END)
                    x.entries[0][1].insert(0, blockSize)
                    x.radioButtonVariables[1].set(spaceType)
                    x.switch_entry_text(1)
                    x.entries[1][1].delete(0, END)
                    x.entries[1][1].insert(0, blockSpace)

                for x in range(2, 4): #Scrambler, copier. Inserts blockGap
                    algorithms[x].entries[2][1].delete(0, END)
                    algorithms[x].entries[2][1].insert(0, blockGap)

                hide_userFileLabel() #Making sure to hide userFileLabel if necessary

            elif tag == "~~preset14~~\n": #Preset for Build 14
                fileName = presetFile.readline()[:-1]
                newFileName = presetFile.readline()[:-1]
                startValueEntry.delete(0, END)
                startValueEntry.insert(0, presetFile.readline()[:-1])
                endValueEntry.delete(0, END)
                endValueEntry.insert(0, presetFile.readline()[:-1])
                incValueEntry.delete(0, END)
                incValueEntry.insert(0, presetFile.readline()[:-1])

                theAlgo = presetFile.readline()[2:-3]
                for x in range(0, len(algorithms)): #Getting the right algorithm
                    if algorithms[x].name == theAlgo:
                        currentEngine.set(x+1)
                        break
                    
                theEngine = algorithms[currentEngine.get()-1]
                switch_algorithm() #Making sure layout changes
                
                presetFile.readline() #~~Entries~~
                for x in range(0, len(theEngine.entries)): #Insert correct values for entries
                    theEngine.entries[x][1].delete(0, END)
                    theEngine.entries[x][1].insert(0, presetFile.readline()[:-1])

                presetFile.readline() #~~Radiobuttons~~
                for x in range(0, len(theEngine.radioButtonVariables)):
                    if theEngine.radioButtonVariables[x] != None:
                        theEngine.radioButtonVariables[x].set(presetFile.readline()[:-1])
                        theEngine.switch_entry_text(x)
                    else:
                        presetFile.readline() #Trashing the none values

                presetFile.readline() #~~Checkbuttons~~
                for x in range(0, len(theEngine.checkButtonVariables)):
                    if theEngine.checkButtonVariables[x] != None:
                        theEngine.checkButtonVariables[x].set(presetFile.readline()[:-1]) #Setting checkbuttons
                    else:
                        presetFile.readline() #Trashing none values

                if presetFile.readline()[:-1] == "True": #Hexadecimal Mode
                    hexadecimalMode = True
                    hexVar.set(1)
                else:
                    hexadecimalMode = False
                    hexVar.set(0)

                hide_userFileLabel()#Making sure to hide userFileLabel if necessary

            else: #If the text file isn't a preset
                if manualSelect:
                    messagebox.showwarning("Hold up!", "The file you selected isn't a preset file.")

        except: #If the file doesn't have lines to read?
            messagebox.showwarning("Hold up!", "The file you selected couldn't be read.")

        presetFile.close()
        
    except FileNotFoundError:
        messagebox.showinfo("Hold it!", "The file you selected couldn't be found.")


def theme_switch(event=None):
    global bannerLabel
    global colorList
    '''Changes the GUI to be dark, or light again'''
    #SystemButtonFace - greyish bg
    #SystemButtonText - text colour
    #SystemWindow - Entry Colour (white) and black select colour for checks and radios

    colorList = themes[themeVar.get()-1].colorList #Changes the colors we're using
    bannerLabel["image"] = colorList[3] #Changes the banner

    for x in range(0, len(algorithms)): #Prevents random buttons in other algorithms from changing color
        algorithms[x].recolor(colorList) #Recolors the elements of the corrupter

    for x in hardCodedWidgets: #Deal with it
        if isinstance(x, Tkinter.Label):
            x.config(bg=colorList[2], fg=colorList[1])
        elif isinstance(x, Tkinter.Entry):
            x.config(bg=colorList[0], fg=colorList[1], insertbackground=colorList[1], selectbackground=colorList[5])
        elif isinstance(x, Tkinter.Button) or isinstance(x, Tkinter.Menubutton):
            x.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[0], activeforeground=colorList[1])
        elif isinstance(x, Tkinter.Menu):
            x.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[5], activeforeground=colorList[1],
                     selectcolor=colorList[1])
        else:
            x["bg"] = colorList[2]

    print(newFileName)


def find_engine_index(engine, value, where):
    '''Finds a specific index in a class'''
    if where == "Entry":
        for x in range(0, len(engine.entries)): #Going through all the entries
            if engine.entries[x][0]["text"] == value:
                return x #It also breaks
            
    elif where == "Radio":
        pass
    elif where == "Check":
        pass
    elif where == "Alts":
        for x in range(0, len(engine.entryAlts)): #Going through all entryAlts
            for y in engine.entryAlts[x]: #Going through each set of alts
                if y == value:
                    return x

    return 0 #Make sure this works


def select_listbox_item(listbox, pathList, newFileName, previousPaths, curselection=":)", event=None):
    '''Returns an item within a given listbox'''

    if curselection == ":)": #Go forward
        if listbox.curselection() != (): #Preventing tuple index errors
            newFileName.append(newFileName[0]+pathList[listbox.curselection()[0]]+"/")
            newFileName.reverse()
            newFileName.pop() #Remove first entry in list
            
            previousPaths.append(newFileName[0]) #Keeping track of all file paths, so that we can undo
    elif not len(previousPaths) < abs(curselection): #Preventing index errors
        newFileName.append(previousPaths[curselection]) #Go back to previous path
        newFileName.reverse()
        newFileName.pop() #Remove first entry from list
        
        previousPaths.pop() #Remove path we're now using

    listbox.delete(0, listbox.size()) #Clearing all elements in the listbox
    pathList.clear() #Clears list

    try:
        for f in os.listdir(newFileName[0]): #Setting new possible paths to use
            listbox.insert(END, f)
            pathList.append(f)
    except: #If we've selected a file, not a folder
        messagebox.showinfo("Hey", "You've selected a file. Only use this if you wish to overwrite that file :)")
        newFileName[-1] = newFileName[-1][:-1] #Cutting off extra slash that we don't need


def folder_selector(textWidgets=[""], labels=[""], event=None):
    '''Custom folder path finder, because Tkinter doesn't have one'''
    global newFileName
    
    main = Tk()
    main.title("Select folder...")
    main.geometry("300x325")
    main.iconbitmap(goodIcon)

    possiblePaths = [] #Holds the current possible paths to travel to
    previousPaths = []
    newFileName = ["C:/"] #Holds the current path
    previousPaths.append(newFileName[0]) #Keeping track of all paths

    mainMessage = Label(main,
                        text="Click on a folder below, then \"Select File\" to travel to it. \nClick \"Ok\" when you've reached the desired folder.")
    mainMessage.pack()

    pathFrame = Frame(main, width=275, height=250) #Where the folders/files will go
    pathFrame.pack()
    pathFrameScrollbar = Scrollbar(pathFrame) #Scrollbar for the list
    pathFrameScrollbar.pack(side=RIGHT, fill=Y)
    pathListbox = Listbox(pathFrame, yscrollcommand=pathFrameScrollbar.set, width=40, height=15) #Holds the actual list
    pathFrameScrollbar.config(command=pathListbox.yview)
    pathListbox.pack()
    
    okButton = Button(main, text="Ok")
    selectButton = Button(main, text="Select Folder")
    backButton = Button(main, text="Go Back")
    okButton.bind("<Button-1>", lambda _: kill_window(main, ["newFileName", newFileName[0], labels], textWidgets)) #Oh boy
    selectButton.bind("<Button-1>", lambda _: select_listbox_item(pathListbox, possiblePaths, newFileName, previousPaths))
    backButton.bind("<Button-1>", lambda _: select_listbox_item(pathListbox, possiblePaths, newFileName, previousPaths, -2))
    okButton.pack(side=LEFT, expand=TRUE)
    backButton.pack(side=RIGHT, expand=TRUE)
    selectButton.pack(expand=TRUE)

    for f in os.listdir(newFileName[0]):
        pathListbox.insert(END, f)
        possiblePaths.append(f)

    main.mainloop()


def kill_window(window, variables=["Name", "Value", ["Label"]], textWidgets=[":)"], event=None):
    '''Kills a window'''
    global newFileName
    if variables[0] == "newFileName":
        newFileName = variables[1]
        for x in variables[2]: #Labels
            if len(newFileName) > 25:
                x["text"] = shorten_text(newFileName, 25, "Front") #Urg, this sucks
            else:
                x["text"] = newFileName

    if textWidgets != [":)"]: #Adding new file path to textbox in select file window
        for x in textWidgets:
            x.delete("1.0", END)
            x.insert("1.0", variables[1])

    window.destroy() #Kill the given window


def hide_userFileLabel(event=None):
    '''Hides the file path above the corrupt button'''
    #Make this more general later
    global userFileLabel

    if hideVar.get() == 1: #Hide it
        if fileName != "":
            userFileLabel["text"] = "File loaded."
    else:
        userFileLabel["text"] = shorten_text(fileName, 40, "Front")


#----------------------------------------------------------------------------------

parentMenu = Menu(root)

fileMenu = Menu(parentMenu, tearoff=0)
optionsMenu = Menu(parentMenu, tearoff=0)
themesMenu = Menu(parentMenu, tearoff=0)
aboutMenu = Menu(parentMenu, tearoff=0)
parentMenu.add_cascade(label="File", menu=fileMenu)
parentMenu.add_cascade(label="Options", menu=optionsMenu)
parentMenu.add_cascade(label="Themes", menu=themesMenu)
parentMenu.add_cascade(label="About", menu=aboutMenu)

#print(optionsMenu.cget("activebackground"))
#foreground="grey50"

fileMenu.add_command(label="Choose File", accelerator="Alt+F", command=enter_file)
fileMenu.add_separator()
fileMenu.add_command(label="Save Presets", accelerator="Alt+S", command=save_presets_window)
fileMenu.add_command(label="Load Presets", accelerator="Alt+L", command=load_presets)

hexVar = IntVar()
autoEndVar = IntVar() #Controls whether to automatically use auto end
autoEndVar.set(0)
themeVar = IntVar() #Keeps track of which theme we're using
themeVar.set(1)
hideVar = IntVar() #Keeps track of whether to hide userFileLabel or not
hideVar.set(0)

optionsMenu.add_checkbutton(label="Hexadecimal Mode", command=hexadecimal_switch, var=hexVar)
optionsMenu.add_checkbutton(label="Auto Insert Auto End", var=autoEndVar)
optionsMenu.add_checkbutton(label="Hide File Label", command=hide_userFileLabel, var=hideVar)

aboutMenu.add_command(label="Info", accelerator="Alt+I", command=about_program_window)

#----------------------------------------------------------------------------------

lightTheme = Theme_Class("Light", ["SystemWindow", "SystemButtonText", "SystemButtonFace",
                                   PhotoImage(file="banner.png"), "logo.png", "SystemHighlight"])
darkTheme = Theme_Class("Dark", ["#1c1c1c", "#c8c8c8", "#1c1c1c",
                                 PhotoImage(file="darkBanner.png"), "darkLogo.png", "#6600CC"])

themes = [lightTheme, darkTheme]

for x in range(0, len(themes)): #Adds themes to menu
    themesMenu.add_radiobutton(label=themes[x].name, command=theme_switch, var=themeVar, value=x+1)

#----------------------------------------------------------------------------------

mainFrame = Frame(root, width=310, height=500)
corruptButtonFrame = Frame(root)

bannerLabel = Label(root, image=themes[themeVar.get()-1].banner)
colorList = themes[themeVar.get()-1].colorList #Holds the colors to use for the program

engineLabel = Label(mainFrame)
engineSelectButton = Menubutton(mainFrame, text="...", relief=RAISED, borderwidth=2) #Teehee
engineMenu = Menu(engineSelectButton, tearoff=0)
engineSelectButton["menu"] = engineMenu #Weird index but ok
#Options for menuButton added below

startValueLabel = Label(mainFrame, text="Start Value")
startValueEntry = Entry(mainFrame)
#startValueEntry["highlightcolor"] = "#ff0000"
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
autoEndButton = Button(mainFrame, text="Auto End")

dividerLabel = Label(mainFrame, text="------------------------------------------------------------")

userFileLabel = Label(corruptButtonFrame, text="No file loaded. Press Alt+F to load one!")
corruptButton = Button(corruptButtonFrame, text="Corrupt", font="Helvetica 25")

hardCodedWidgets = [root, mainFrame, corruptButtonFrame,
                    engineLabel, engineSelectButton,
                    startValueLabel, startValueEntry, startValueButton,
                    endValueLabel, endValueEntry, endValueButton,
                    incValueLabel, incValueEntry, autoEndButton,
                    dividerLabel, userFileLabel, corruptButton,
                    parentMenu, fileMenu, optionsMenu, themesMenu, aboutMenu, engineMenu] #Deal with it, punk

#----------------------------------------------------------------------------------

engineSelectButton.bind("<Button-1>")

startValueButton.bind("<Button-1>", startValueClass.left_click_function)
endValueButton.bind("<Button-1>", endValueClass.left_click_function)
startValueButton.bind("<Button-3>", startValueClass.right_click_function)
endValueButton.bind("<Button-3>", endValueClass.right_click_function)

autoEndButton.bind("<Button-1>", auto_end_switch)

corruptButton.bind("<Button-1>", corrupt_file)

#------------------------------------------------------------------------------------

bannerLabel.pack()

mainFrame.pack()
corruptButtonFrame.pack(side=BOTTOM)

engineLabel.grid(row=0, column=0, columnspan=3, pady=5, sticky=E)
engineSelectButton.grid(row=0, column=3)

startValueLabel.grid(row=1, column=0, padx=5, pady=5, sticky=E)
startValueEntry.grid(row=1, column=1, columnspan=2, pady=5)
startValueButton.grid(row=1, column=3, padx=20, pady=5)

endValueLabel.grid(row=2, column=0, padx=5, pady=5, sticky=E)
endValueEntry.grid(row=2, column=1, columnspan=2, pady=5)
endValueButton.grid(row=2, column=3, padx=20, pady=5)

incValueLabel.grid(row=3, column=0, pady=5, padx=5, sticky=E)
incValueEntry.grid(row=3, column=1, columnspan=2, pady=5)
autoEndButton.grid(row=3, column=3, pady=5)

dividerLabel.grid(row=4, column=0, pady=5, columnspan=4)

#------------------------------------------------------------------------------------

incEngineEntries = ["Block Size", "Block Space", "*Add/Subtract"]
incEngineRadios = [[None], ["Linear", "Exponential", "Random"], [None]]
incEngineChecks = [None, None, None]
incEngineAlts = [[None], ["Block Space", "Exponent", "Upper Bound"], [None]]
incEngine = Engine_Class(mainFrame, add_corrupt_engine, "Incrementer Algorithm",
                         incEngineEntries, incEngineRadios, incEngineChecks, incEngineAlts)

randEngine = Engine_Class(mainFrame, random_corrupt_engine, "Randomizer Algorithm",
                          incEngineEntries[:2], incEngineRadios[:2], incEngineChecks[:2], incEngineAlts[:2])

scramEngineEntries = ["Block Size", "Block Space", "*Block Gap"]
scramEngine = Engine_Class(mainFrame, scrambler_corrupt_engine, "Scrambler Algorithm",
                           scramEngineEntries, incEngineRadios, incEngineChecks, incEngineAlts)

copiEngineEntries = ["Block Size", "Block Space", "*Block Gap"]
copiEngine = Engine_Class(mainFrame, copier_corrupt_engine, "Copier Algorithm",
                          copiEngineEntries, incEngineRadios, incEngineChecks, incEngineAlts)

tiltEngineEntries = ["Block Size", "Block Space", "*Replace", "*Replace With"]
tiltEngineRadios = [[None], ["Linear", "Exponential", "Random"], [None], [None]]
tiltEngineChecks = [None, None, None, "Exclusive"]
tiltEngineAlts = [[None], ["Block Space", "Exponent", "Upper Bound"], [None], [None]]
tiltEngine = Engine_Class(mainFrame, tilter_corrupt_engine, "Tilter Algorithm",
                          tiltEngineEntries, tiltEngineRadios, tiltEngineChecks, tiltEngineAlts)

'''print(incEngine.entries)
print(incEngine.radioButtons)
print(incEngine.radioButtonVariables)
print(incEngine.checkButtons)
print(incEngine.checkButtonVariables)
print(incEngine.entryAlts)'''

algorithms = [incEngine, randEngine, scramEngine, copiEngine, tiltEngine]

engineLabel["text"]=algorithms[currentEngine.get()-1].name #Setting algorithm label
algorithms[currentEngine.get()-1].display_layout(colorList) #Displays the current algorithm to window

for x in range(0, len(algorithms)):
    engineMenu.add_radiobutton(label=algorithms[x].name, var=currentEngine, command=switch_algorithm, value=x+1)


#------------------------------------------------------------------------------------

userFileLabel.pack(pady=5)
corruptButton.pack(pady=5)

root.config(menu=parentMenu)

root.bind("<Alt-f>", enter_file)
root.bind("<Alt-i>", about_program_window)
root.bind("<Alt-s>", save_presets_window)
root.bind("<Alt-l>", load_presets)

try: #Looking to see if preset exists
    for f in os.listdir():
        if f.endswith('.txt'):
            load_presets(coolName=f)
except FileNotFoundError:
    try: #Added this to fix weird comapibility bug
        for f in os.listdir():
            if f.endswith('.txt'):
                load_presets(coolName=f)
    except FileNotFoundError:
        pass

root.mainloop()
