
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

buildNumber = "19"
versionNumber = "v1.2"
goodIcon = "Assets/favi16.ico"

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
    5 = Smoother
    6 = Blender

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
oldFileName = ""
newPresetName = ""

cnameLabel = ""
stopCorrupt = False #Variable to stop corrupting if needed
newFolder = False #Says whether a new folder is to be created for "Corrupt&Repeat"
nowCorrupting = False #Tells whether we're corrupting


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
    if fileName != "":
        size = os.path.getsize(fileName)
        endValueEntry.delete(0, "end")
        if hexadecimalMode:
            size = hex_convert(size)
        endValueEntry.insert(0, size)


def toggle_newFolder(event=None):
    '''Toggles the value for newFolder'''
    global newFolder
    if newFolder:
        newFolder = False
    else:
        newFolder = True


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
                try:
                    return int(entry.get())
                except:
                    return float(entry.get()) #Fixing problems with exponential
            else:
                return float(entry.get())

    else:
        return ""
        

def hexadecimal_switch(event=None, switchTo=None):
    global hexadecimalMode
    '''Toggles the switch'''
    #"Hex" or "Dec"
    if switchTo == "Hex" and hexadecimalMode: #Prevents invalid values from going into functions
        pass

    elif switchTo == "Dec" and not hexadecimalMode:
        pass
    
    elif switchTo == "Dec":
        for x in algorithms: #Converts hexes already in entries to decimals
            x.hexadecimalMode = False #Changing each algorithm's internal switch
        hexadecimalMode = False
        
    elif switchTo == "Hex":
        for x in algorithms: #Converts decimals in entries to hexes
            x.hexadecimalMode = True #Changing each algorithm's internal switch
        hexadecimalMode = True

    elif hexadecimalMode and switchTo == None:
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

    elif not hexadecimalMode and switchTo == None:
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
    userFileWindow.geometry("450x180+250+250")
    userFileWindow.iconbitmap(goodIcon)
    userFileWindow.resizable(width=False, height=False)

    mainFrame = Frame(userFileWindow)
    applyFrame = Frame(userFileWindow)

    instLabel = Label(mainFrame, text="Select the file you wish to corrupt, and enter the name of the new file\n"
                      "(You may need to use the arrow keys to scroll the textbox):")
    cfileLabel = Label(mainFrame, text="File To Corrupt:")
    
    if fileName == "":
        cnameLabel = Label(mainFrame, text="No File Selected")
    else:
        t = shorten_text(fileName, 25, "Front")
        cnameLabel = Label(mainFrame, text=t)

    userFileButton = Button(mainFrame, text="Select File")
    nfileLabel2 = Label(mainFrame, text="New File Name:")
    newFileButton = Button(mainFrame, text="Select Folder")

    newFileText = Text(mainFrame)
    if newFileName == "":
        newFileText.insert(END, "Enter new file name...")
        newFileText.bind("<Button-1>", lambda x: clear_textWidget(x, newFileText, "Enter new file name..."))
    else:
        newFileText.insert(END, newFileName)
        
    applyButton = Button(applyFrame, text=" Apply ")

    userFileWindow.config(bg=colorList[2])
    mainFrame.config(bg=colorList[2])
    applyFrame.config(bg=colorList[2])
    instLabel.config(bg=colorList[2], fg=colorList[1])
    cfileLabel.config(bg=colorList[2], fg=colorList[1])
    cnameLabel.config(bg=colorList[2], fg=colorList[1])
    userFileButton.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[2], activeforeground=colorList[1])
    nfileLabel2.config(bg=colorList[2], fg=colorList[1])
    newFileText.config(bg=colorList[0], fg=colorList[1], insertbackground=colorList[1], selectbackground=colorList[5])
    newFileButton.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[2], activeforeground=colorList[1])
    applyButton.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[2], activeforeground=colorList[1])

    userFileButton.bind("<Button-1>", select_file)
    newFileButton.bind("<Button-1>", lambda _: folder_selector([newFileText]))
    applyButton.bind("<Button-1>", lambda _: get_file_name(newFileText))

    newFileText.config(width=25, height=1)

    mainFrame.pack()
    applyFrame.pack()

    instLabel.grid(row=1, column=1, columnspan=10, padx=40, pady=10)
    cfileLabel.grid(row=2, column=1, columnspan=2, padx=0, pady=5)
    cnameLabel.grid(row=2, column=3, columnspan=5, padx=10, pady=5)
    userFileButton.grid(row=2, column=8, padx=20, pady=5)

    newFileButton.grid(row=3, column=8, padx=5, pady=5)

    nfileLabel2.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
    newFileText.grid(row=3, column=3, columnspan=5, padx=28, pady=5)
    applyButton.grid(row=4, column=1, columnspan=1, padx=10, pady=15)

    userFileWindow.bind("<Return>", lambda _: get_file_name(newFileText))
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
    global oldFileName
    global fileName
    '''Gets the file name that the user entered'''
    newFileName = text.get(1.0, END)[:-1]
    if newFileName == ("Enter new file name..." or newFileName == "") and fileName == "":
        newFileName = ""
    elif newFileName == "Enter new file name..." or newFileName == "":
        newFileName = "CorruptedFile" #Default file name
        
    p = check_for_char(newFileName)

    if p == False:
        pp = check_for_char(fileName)
        newFileName += fileName[pp:]
        #print(newFileName)

    p = check_for_char(newFileName, "\n")
    if p != False:
        if p == -1:
            newFileName = newFileName[1:] #Removing any newlines from pressing enter
        else:
            newFileName = newFileName[:p] + newFileName[p+1:] #Removing any newlines from pressing enter

    if fileName == "":
        userFileLabel.config(text="No file loaded. Press Alt+F to load one!")
    else:
        hide_userFileLabel()

    oldFileName = newFileName #Saving oldFileName so that it won't get lost
    userFileWindow.destroy()


def about_program_window(event=None):
    '''The about window'''
    aboutWindow = Tk()
    
    aboutWindow.title("About Scares Scrambler Build "+buildNumber+" "+"("+versionNumber+")")
    aboutWindow.iconbitmap(goodIcon)

    infoLabel = Label(aboutWindow, text="Program created by your man, Scares.\n"
                      "This is an open-source project, so feel free to mess around in the code and stuff.\n"
                      "If you want to release your own modified version of this project, just credit me and I'll be happy! :3\n\n"
                      "I'd also like to extend a huge thank you to anyone who bothered to try this thing!\n"
                      "It isn't the best piece of software out there, but I think it's pretty cool.")
    infoLabel2 = Label(aboutWindow, text="Thank you for being a part of this project. Have fun!")

    aboutWindow["bg"] = colorList[2]
    goodLogo = PhotoImage(master=aboutWindow, file=colorList[4])
    infoLabel.config(bg=colorList[2], fg=colorList[1])
    infoLabel6 = Label(aboutWindow, image=goodLogo)
    infoLabel2.config(bg=colorList[2], fg=colorList[1])

    infoLabel.pack()
    infoLabel6.pack()
    infoLabel2.pack()

    aboutWindow.mainloop()


def credits_window(event=None):
    '''Window to credit bugtesters and any other contributors'''
    creditsWindow = Tk()
    creditsWindow.title("Scares Scrambler Build " +buildNumber+" "+"("+versionNumber+") Contributors")
    creditsWindow.iconbitmap(goodIcon)
    creditsWindow["bg"] = colorList[2]

    label = Label(creditsWindow, text="Here's a list of people who've contributed to this project "
                                       "in one way or another! \n Thank you to everyone for your support!",
                  bg=colorList[2], fg=colorList[1])
    label2 = Label(creditsWindow, text="Dubby (Bugtester) \n"
                                       "Ellestice (Bugtester) \n"
                                       "Rare (Bugtester) \n"
                                       "Tyler (Bugtester) \n"
                                       "Scott (Bugtester, Moral Supporter) \n"
                                       "Telic (Bugtester, Moral Supporter) \n"
                                       "Ircluzar (Supporter, I think)", bg=colorList[2], fg=colorList[1])
    goodLogo = PhotoImage(master=creditsWindow, file=colorList[4])
    label3 = Label(creditsWindow, image=goodLogo)

    label.pack()
    label2.pack()
    label3.pack()

    creditsWindow.mainloop()


def corrupt_file(event=None, determinedVariables=[]):
    global newFileName
    global userFileLabel
    global stopCorrupt
    '''Corrupts the chosen file'''

    tempIndex = 0 #Holds the index for specific variables
    theEngine = algorithms[currentEngine.get()-1] #The current algorithm being used

    try:
        if determinedVariables == []: #If no values were given; standard Corrupt
            startValue = get_value(startValueEntry)
            endValue = get_value(endValueEntry)

            #Mandatory stuff
            tempIndex = find_engine_index(theEngine, "Block Size", "Entry") 
            blockSize = get_value(theEngine.entries[tempIndex][1])
            if blockSize < 1:
                blockSize = 1

            tempIndex = find_engine_index(theEngine, "Block Space", "Alts") #Checking alts in case the label is different
            #blockSpace = get_value(theEngine.entries[tempIndex][1])

            blockSpaceState = theEngine.radioButtonVariables[tempIndex].get()
            if blockSpaceState == 2: #Exponential
                blockSpace = get_value(theEngine.entries[tempIndex][1], False)
            else:
                blockSpace = get_value(theEngine.entries[tempIndex][1])

            corruptingVariables = theEngine.get_corruption_variables()
            #print(corruptingVariables)
            for x in range(0, len(corruptingVariables)): #Converting variables to usable stuff
                if isinstance(corruptingVariables[x], list): #Making sure we're correcting the proper values
                    for y in range(0, len(corruptingVariables[x])):
                        if x == 0:
                            if not isinstance(corruptingVariables[x][y], str):
                                corruptingVariables[x][y] = get_value(corruptingVariables[x][y]) #Changing from hex if necessary
                        else:
                            if not isinstance(corruptingVariables[x][y], str):
                                corruptingVariables[x][y] = corruptingVariables[x][y].get()

            #print(corruptingVariables)

        else: #If values were given; Corrupt and Repeat
            startValue = determinedVariables[0][1]
            endValue = determinedVariables[1][1]
            blockSpaceState = determinedVariables[-2][1]
            determinedVariables = determinedVariables[2:-2] #Dumb formatting

            for x in determinedVariables:
                if x[0] == "Block Size":
                    if x[1] < 1:
                        x[1] = 1 #Preventing errors?
                    blockSize = x[1]
                elif x[0] in ["Block Space", "Exponent", "Upper Bound"]:
                    blockSpace = x[1]

            cVEntries = [x.copy()[1] for x in determinedVariables] #This should include all the remaining entries
            cVRadios = []
            cVChecks = []
            for x in theEngine.radioButtonVariables: #All remaining radioButtons
                if x != None:
                    cVRadios.append(x.get())
            for x in theEngine.checkButtonVariables: #All remaining checkButtons
                if x != None:
                    cVChecks.append(x.get())

            if theEngine.name == "Blender Algorithm":
                corruptingVariables = [cVEntries.copy(), cVRadios.copy(), cVChecks.copy(), open(theEngine.extraFile, "rb+")] #May not be rb+
            else:
                corruptingVariables = [cVEntries.copy(), cVRadios.copy(), cVChecks.copy()]
            
            #print(corruptingVariables, "the cV")
            
        if startValue < 0: #Fixing possible problems
            startValue = 0
        if endValue > os.path.getsize(fileName):
            endValue = os.path.getsize(fileName)
        elif endValue < 0:
            endValue = 0
        elif startValue > endValue:
            startValue = endValue
        if blockSpaceState == 2 and blockSpace < 1: #Fixing negative exponents and stuff
            blockSpace = 1

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

            if theEngine.name == "Blender Algorithm":
                if corruptingVariables[0][2] < 0:
                    corruptingVariables[0][2] = 0 #Making sure we don't go off the edge
                corruptingVariables[3].seek(corruptingVariables[0][2]) #Setting proper offset
                    
            baseFile.seek(0) #Goto the start byte
            copy_file_contents(baseFile, corruptedFile, startValue) #Add all stuff before start value
            currentPos = 0 #Keeps track of where we are in the file currently
            previousPos = 0 #Keeps track of the previous position in the file

            exponentCounter = 1 #For exponential spacing
            exponentCapValue = 1000000 #Fix this lovely hardcoding
            tempSpace = blockSpace #BlockSpace used by the functions below (setting for linear)

            corruptRange = endValue - startValue #Used for progress bar
            nextUpdate = startValue + 100000 #Tells the window when to update (maybe fix hardcoded number later)
            strCorruptRange = str(corruptRange)
            userFileLabel["text"] = "0/"+strCorruptRange+" (0%) corrupted"

            #print(blockSpace)

            while True: #Main corruption loop

                if blockSpaceState == 2: #Exponential
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

                theEngine.corrupt(corruptingVariables, tempSpace, baseFile, corruptedFile, endValue) #The thing that actually does the corrupting

                currentPos = baseFile.tell() #Getting current pos

                if theEngine.name == "Smoother Algorithm":
                    if currentPos+tempSpace+2*corruptingVariables[0][0] >= endValue:
                        userFileLabel["text"] = "Copying uncorrupted contents..."
                        root.update()
                        break
                if theEngine.name == "Blender Algorithm": #Making sure we don't keep corrupting past the end of the file
                    if currentPos >= endValue:
                        userFileLabel["text"] = "Copying uncorrupted contents..."
                        root.update()
                        break
                elif currentPos == previousPos:
                    userFileLabel["text"] = "Copying uncorrupted contents..."
                    root.update()
                    break

                previousPos = currentPos

                if currentPos > nextUpdate: #Prevents excess method calls
                    if currentPos <= endValue:
                        userFileLabel["text"] = str(currentPos-startValue)+"/"+strCorruptRange+" ("+str(
                            round(((currentPos-startValue)/corruptRange)*100))+"%) corrupted"
                    root.update() #Updates userFileLabel with progress bar
                    nextUpdate = currentPos + 100000

            while True: #This finishes the uncorrupted part
                currentByte = baseFile.read(100)
                if currentByte == b"":
                    hide_userFileLabel() #Changing from progress bar to file name, if needed
                    break
                corruptedFile.write(currentByte)

        baseFile.close()
        corruptedFile.close()
        if theEngine.name == "Blender Algorithm":
            corruptingVariables[3].close()
        stopCorrupting = False
            
    except ValueError:
        messagebox.showwarning("Woah there partner!", "The values you entered were not valid. Make sure that all the values were entered correctly. "
                               "Some values can't be decimals, so uh... check that as well.")
        hide_userFileLabel() #Fixing any stuck progress bars
        try:
            baseFile.close()
            corruptedFile.close()
        except UnboundLocalError: #File was never opened
            pass
        root.update() #Updates userFileLabel with progress bar
        if theEngine.name == "Blender Algorithm":
            corruptingVariables[3].close()
            
        stopCorrupt = True
    except IndexError:
        if baseFile.read() == b"": #Checking to see if endValue was too big
            hide_userFileLabel() #Changing from progress bar to file name, if needed
            baseFile.close()
            corruptedFile.close()
            if theEngine.name == "Blender Algorithm":
                corruptingVariables[3].close()
        else:
            messagebox.showwarning("Woah there partner!", "Make sure to fill in the required values properly!")
            hide_userFileLabel() #Fixing any stuck progress bars
            baseFile.close()
            corruptedFile.close()
            if theEngine.name == "Blender Algorithm":
                corruptingVariables[3].close()
        root.update() #Updates userFileLabel with progress bar

        stopCorrupt = True
    except TypeError:
        messagebox.showwarning("Woah there partner!", "Make sure to fill in the required values properly!")
        hide_userFileLabel() #Fixing any stuck progress bars
        try:
            baseFile.close()
            corruptedFile.close()
        except UnboundLocalError: #File was never opened
            pass
        if theEngine.name == "Blender Algorithm":
            corruptingVariables[3].close()
        root.update() #Updates userFileLabel with progress bar'''
        stopCorrupt = True


def corrupt_repeat_window(event=None):
    '''Function to manage "Corrupt and Repeat"'''
    #global newFolder
    global oldFileName

    repeatWindow = Tk()
    if themeVar.get() == 3: #Dubby theme
        repeatWindow.title("Dubby and Repeat")
    else:
        repeatWindow.title("Corrupt and Repeat")
        
    repeatWindow.iconbitmap(goodIcon)
    repeatWindow.geometry("300x500")

    incFrame = Frame(repeatWindow, width=300, height=480)

    entries = [] #Holds all the entries and labels
    #oldValues = [] #Will hold the user's settings, in case they revert back after repeat
    #currentValues = [] #Will hold the values used for repeat
    
    entries.append([Label(incFrame, text="Start Value Inc:"), Entry(incFrame)])
    entries.append([Label(incFrame, text="End Value Inc:"), Entry(incFrame)])

    for x in algorithms[currentEngine.get()-1].entries: #Goes through all the entries
        entries.append([Label(incFrame, text=x[0]["text"]+" Inc:"), Entry(incFrame)])
    entries.append([Label(incFrame, text="Number of Files:"), Entry(incFrame)])

    if themes[themeVar.get()-1].name == "Dubby": #Dubby theme
        corruptButton = Button(repeatWindow, text="Dubby", font="Helvetica 25")
        instructions = Label(repeatWindow, text='Insert the amount you\'d like the settings to be\n'
                         'incremented each time, then press "Dubby".')
    else:
        corruptButton = Button(repeatWindow, text="Corrupt", font="Helvetica 25")
        instructions = Label(repeatWindow, text='Insert the amount you\'d like the settings to be\n'
                         'incremented each time, then press "Corrupt".')

    newFolderCheck = Checkbutton(repeatWindow, text="Store files in new folder", command=toggle_newFolder) #Checkbox to tell whether user wants a separate folder

    corruptButton.bind("<Button-1>", lambda _: corrupt_repeat(entries))

    repeatWindow["bg"] = colorList[2]
    incFrame["bg"] = colorList[2]
    instructions.config(bg=colorList[2], fg=colorList[1])
    for x in entries:
        x[0].config(bg=colorList[2], fg=colorList[1])
        x[1].config(bg=colorList[0], fg=colorList[1], insertbackground=colorList[1], selectbackground=colorList[5])
    corruptButton.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[2], activeforeground=colorList[1])
    newFolderCheck.config(bg=colorList[2], fg=colorList[1], selectcolor=colorList[0], activebackground=colorList[2],
                          activeforeground=colorList[1])
    
    instructions.pack()
    incFrame.pack()
    for x in range(0, len(entries)):
        entries[x][0].grid(row=x+1, column=0, pady=5, sticky=W)
        entries[x][1].grid(row=x+1, column=1, columnspan=3, padx=10, sticky=W)

    corruptButton.pack(side="bottom", pady=5)
    newFolderCheck.pack(side="bottom", pady=5)

    repeatWindow.mainloop()


def corrupt_repeat(entries, event=None):
    '''The function that manages the corrupt and repeat stuff'''
    '''The random minuses in the range functions are to prevent errors with special corrupting values'''
    global newFileName
    global oldFileName
    global stopCorrupt

    if newFolder and "newFolder" not in newFileName: #If we're making a new folder
        p = check_for_char(newFileName, "\\")
        q = check_for_char(__file__, "\\")
        #print(__file__[:q], "wow")
                
        if p != False: #If the newFileName is a full path
            if not os.path.exists(newFileName[:p]+"\\newFolder"):
                os.mkdir(newFileName[:p]+"\\newFolder") #Make new directory if needed
                
            newFileName = newFileName[:p] + "\\newFolder" + newFileName[p:]
        else:
            if not os.path.exists(__file__[:q]+"\\newFolder"):
                os.mkdir(__file__[:q]+"\\newFolder") #Make new directory if needed
                
            newFileName = __file__[:q] + "\\newFolder\\" + newFileName #Making sure the new folder gets added to path correctly
    elif not newFolder:
        newFileName = oldFileName

    variables = []
    ogFileName = newFileName
    extraOffset = 0 #In case extra things are added to the variables; prevents incrementing errors
    expo = algorithms[currentEngine.get()-1].radioButtonVariables[find_engine_index(
        algorithms[currentEngine.get()-1], "Block Space", "Alts")].get()

    blockSpaceAlts = algorithms[currentEngine.get()-1].entryAlts[find_engine_index(
        algorithms[currentEngine.get()-1], "Block Space", "Alts")]
    #Checking to see if exponential is on
    for x in entries:
        try:
            if x[1].get() != "": #If there's actual data to collect
                if x[0]["text"][:-5] in blockSpaceAlts and expo == 2:
                    variables.append([x[0]["text"][:-5], get_value(x[1], isInt=False)])
                else:
                    variables.append([x[0]["text"][:-5], get_value(x[1], isInt=True)])
            else:
                variables.append([x[0]["text"][:-5], 0])
        except:
            messagebox.showwarning("Good job, Buddy.", "Make sure all entered values are valid numbers!")
        
    variables.insert(-1, ["Block Space State", expo]) #Getting blockSpaceState; NO OTHER ADDITIONS CAN COME AFTER THIS

    dotPos = check_for_char(newFileName) #Gets position of dot in newFileName
    
    currentVariables = [x.copy() for x in variables] #Holds the variables to be used for corrupting
    currentVariables[0][1] += get_value(startValueEntry) #Getting currentVariables ready for corrupting
    currentVariables[1][1] += get_value(endValueEntry)
    for x in range(0, len(algorithms[currentEngine.get()-1].entries)):
        if algorithms[currentEngine.get()-1].entries[x][0]["text"] == "Exponent":
            currentVariables[x+2][1] += get_value(algorithms[currentEngine.get()-1].entries[x][1], isInt=False)
        else:
            currentVariables[x+2][1] += get_value(algorithms[currentEngine.get()-1].entries[x][1], isInt=True)
        
    for x in range(0, variables[-1][1]): #The actual "corrupt and repeat" part
        corrupt_file(determinedVariables=currentVariables)
        for y in range(0, len(variables)-2-extraOffset):
            currentVariables[y][1] += variables[y][1] #This is what does the incrementing
        newFileName = ogFileName[:dotPos] + "_" + str(x) + ogFileName[dotPos:]
        if stopCorrupt: #If we need to stop corrupting
            break

    newFileName = ogFileName #Returning the fileName to normal
    stopCorrupt = False


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

    newPresetWindow.bind("<Return>", lambda _: save_presets(newPresetEntry))
    newPresetWindow.mainloop()


def save_presets(newPresetEntry, event=None):
    '''Saves the presets to a text file'''
    
    presetList = []
    theEngine = algorithms[currentEngine.get()-1]

    presetList.append("~~preset16~~")
    presetList.append(fileName)
    presetList.append(newFileName)
    presetList.append(algorithms[currentEngine.get()-1].extraFile) #extraFile

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
    presetList.append(hideVar.get()) #Add hide file labels
    name = newPresetEntry.get()

    if name[-4:] == ".txt": #If there's a file extension
        presetFile = open(name, "w")
    else:
        presetFile = open(name+".txt", "w")

    for x in presetList:
        presetFile.write(str(x)+"\n")

    #presetFile.write("~~End~~")

    presetFile.close()
    newPresetWindow.destroy() #Close the preset window


def load_presets(event=None, coolName=""):
    global fileName
    global newFileName
    global oldFileName
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

        #try:
        tempVar = ""
        tag = presetFile.readline()
        if tag == "~~preset~~\n": #The preset used in Build 13 and below
            fileName = presetFile.readline()[:-1]
            newFileName = presetFile.readline()[:-1]
            oldFileName = newFileName
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
                hexadecimal_switch(switchTo="Hex")
                hexVar.set(1)
            else:
                hexadecimal_switch(switchTo="Dec")
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

        elif tag == "~~preset14~~\n" or tag == "~~preset16~~\n": #Preset for Build 14
            fileName = presetFile.readline()[:-1]
            newFileName = presetFile.readline()[:-1]
            oldFileName = newFileName
            if tag == "~~preset16~~\n":
                extraFile = presetFile.readline()[:-1] #Extra file name
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
            theEngine.extraFile = extraFile #Actually setting extraFile
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
                hexadecimal_switch(switchTo="Hex")
                hexVar.set(1)
            else:
                hexadecimal_switch(switchTo="Dec")
                hexVar.set(0)

            if tag == "~~preset16~~\n":
                hideVar.set(presetFile.readline()[:-1]) #Setting the hideVar variable

            hide_userFileLabel()#Making sure to hide userFileLabel if necessary

        else: #If the text file isn't a preset
            if manualSelect:
                messagebox.showwarning("Hold up!", "The file you selected isn't a preset file.")

        '''except: #If the file doesn't have lines to read?
            messagebox.showwarning("Hold up!", "The file you selected couldn't be read.")'''

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
    #print(themeVar.get())

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

    if themeVar.get() == 3: #Dubby theme
        corruptButton["text"] = "Dubby"
        corruptRepeatButton["text"] = "Dubby and Repeat"
    else:
        corruptButton["text"] = "Corrupt"
        corruptRepeatButton["text"] = "Corrupt and Repeat"


def select_listbox_item(listbox, pathList, tempFileName, curselection=":)", pathLabel=":)", event=None):
    '''Returns an item within a given listbox'''
    global newFileName

    if curselection == ":)": #Go forward
        if listbox.curselection() != (): #Preventing tuple index errors
            tempFileName += pathList.copy()[listbox.curselection()[0]]+"\\"

    else:
        slashPos = check_for_char(tempFileName[:-1], "\\") #Weird double slash is just a representation
        if slashPos != False:
            tempFileName = tempFileName[:slashPos] + "\\"
            if check_for_char(tempFileName[:-1], "\\") == False:
                tempFileName = "C:/" #Making sure slashes get added properly
        else:
            tempFileName = "C:/"

    pathLabel["text"] = tempFileName #Setting new file path on folder window
            
    newFileName = tempFileName #Actually setting the path

    listbox.delete(0, listbox.size()) #Clearing all elements in the listbox
    pathList.clear() #Clears list

    try:
        for f in os.listdir(newFileName): #Setting new possible paths to use
            listbox.insert(END, f)
            pathList.append(f)
    except: #If we've selected a file, not a folder
        messagebox.showinfo("Hey", "You've selected a file. Only use this if you wish to overwrite that file :)")
        newFileName = tempFileName[:-1] #Cutting off extra slash that we don't need


def folder_selector(textWidgets=[""], labels=[""], event=None):
    '''Custom folder path finder, because Tkinter doesn't have one'''
    global newFileName
    
    main = Tk()
    main.title("Select folder...")
    main.geometry("300x340")
    main.iconbitmap(goodIcon)
    main["bg"] = colorList[2]

    possiblePaths = [] #Holds the current possible paths to travel to
    newFileName = os.getcwd()+"\\" #Holds the current path

    mainMessage = Label(main,
                        text="Click on a folder below, then \"Select File\" to travel to it. \nClick \"Ok\" when you've reached the desired folder.")
    mainMessage.config(bg=colorList[2], fg=colorList[1])
    mainMessage.pack()

    newPathLabel = Label(main, text=newFileName)
    newPathLabel.config(bg=colorList[2], fg=colorList[1])
    newPathLabel.pack()

    pathFrame = Frame(main, width=275, height=250) #Where the folders/files will go
    pathFrame["bg"] = colorList[2]
    pathFrame.pack()
    pathFrameScrollbar = Scrollbar(pathFrame) #Scrollbar for the list
    pathFrameScrollbar.pack(side=RIGHT, fill=Y)
    pathListbox = Listbox(pathFrame, yscrollcommand=pathFrameScrollbar.set, width=40, height=15) #Holds the actual list
    pathListbox.config(bg=colorList[2], fg=colorList[1])
    pathFrameScrollbar.config(command=pathListbox.yview, bg=colorList[2], activebackground=colorList[0],
                              highlightcolor=colorList[1], highlightbackground=colorList[2])
    pathListbox.pack()

    okButton = Button(main, text="Ok")
    selectButton = Button(main, text="Select Folder")
    backButton = Button(main, text="Go Up")
    okButton.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[0], activeforeground=colorList[1])
    selectButton.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[0], activeforeground=colorList[1])
    backButton.config(bg=colorList[2], fg=colorList[1], activebackground=colorList[0], activeforeground=colorList[1])
    
    okButton.bind("<Button-1>", lambda _: kill_window(main, ["newFileName", newFileName, labels], textWidgets)) #Oh boy
    selectButton.bind("<Button-1>", lambda _: select_listbox_item(pathListbox, possiblePaths, newFileName, pathLabel=newPathLabel))
    backButton.bind("<Button-1>", lambda _: select_listbox_item(pathListbox, possiblePaths, newFileName, -2, newPathLabel))
    
    okButton.pack(side=LEFT, expand=TRUE)
    backButton.pack(side=RIGHT, expand=TRUE)
    selectButton.pack(expand=TRUE)

    for f in os.listdir(newFileName):
        pathListbox.insert(END, f)
        possiblePaths.append(f)

    main.mainloop()


def kill_window(window, variables=["Name", "Value", ["Label"]], textWidgets=[":)"], event=None):
    '''Kills a window'''
    #Jesus, this is terrible
    global newFileName
    if variables[0] == "newFileName":
        newFileName = variables[1]
        if variables[2] != [""]:
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
        algorithms[currentEngine.get()-1].hideFileLabels = True #Making sure extraFile doesn't show
        algorithms[currentEngine.get()-1].hide_layout()
        algorithms[currentEngine.get()-1].display_layout(themes[themeVar.get()-1].colorList)
    else:
        if fileName != "":
            userFileLabel["text"] = shorten_text(fileName, 40, "Front")
        else:
            userFileLabel["text"] = "No file loaded. Press Alt+F to load one!"
        algorithms[currentEngine.get()-1].hideFileLabels = False
        algorithms[currentEngine.get()-1].hide_layout()
        algorithms[currentEngine.get()-1].display_layout(themes[themeVar.get()-1].colorList)


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
optionsMenu.add_checkbutton(label="Hide File Labels", command=hide_userFileLabel, var=hideVar)

aboutMenu.add_command(label="Info", accelerator="Alt+I", command=about_program_window)
aboutMenu.add_command(label="Contributors", command=credits_window)

#----------------------------------------------------------------------------------

lightTheme = Theme_Class("Light", ["SystemWindow", "SystemButtonText", "SystemButtonFace",
                                   PhotoImage(file="Assets/banner.png"), "Assets/logo.png", "SystemHighlight"])
darkTheme = Theme_Class("Dark", ["#1c1c1c", "#c8c8c8", "#1c1c1c",
                                 PhotoImage(file="Assets/darkBanner.png"), "Assets/darkLogo.png", "#6600CC"])
dubbyTheme = Theme_Class("Dubby", ["#004200", "#00ff00", "#006900",
                                   PhotoImage(file="Assets/dubbyBanner.png"), "Assets/dubbyLogo.png", "#00ee00"])

themes = [lightTheme, darkTheme, dubbyTheme]

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
startValueEntry.insert(0, 0)
startValueButton = Button(mainFrame, text="+/-")

endValueLabel = Label(mainFrame, text="End Value")
endValueEntry = Entry(mainFrame)
endValueEntry.insert(0, 0)
endValueButton = Button(mainFrame, text="+/-")

incValueLabel = Label(mainFrame, text="Inc Value")
incValueEntry = Entry(mainFrame)
autoEndButton = Button(mainFrame, text="Auto End")

dividerLabel = Label(mainFrame, text="------------------------------------------------------------")

userFileLabel = Label(corruptButtonFrame, text="No file loaded. Press Alt+F to load one!")

if themes[themeVar.get()-1].name == 3: #Dubby theme
    corruptButton = Button(corruptButtonFrame, text="Dubby", font="Helvetica 25")
    corruptRepeatButton = Button(corruptButtonFrame, text="Dubby and Repeat", font="Helvetica 11")
else:
    corruptButton = Button(corruptButtonFrame, text="Corrupt", font="Helvetica 25")
    corruptRepeatButton = Button(corruptButtonFrame, text="Corrupt and Repeat", font="Helvetica 11")

hardCodedWidgets = [root, mainFrame, corruptButtonFrame,
                    engineLabel, engineSelectButton,
                    startValueLabel, startValueEntry, startValueButton,
                    endValueLabel, endValueEntry, endValueButton,
                    incValueLabel, incValueEntry, autoEndButton,
                    dividerLabel, userFileLabel, corruptButton, corruptRepeatButton,
                    parentMenu, fileMenu, optionsMenu, themesMenu, aboutMenu, engineMenu] #Deal with it, punk

#----------------------------------------------------------------------------------

engineSelectButton.bind("<Button-1>")

startValueButton.bind("<Button-1>", lambda _: inc_entry(hexadecimalMode, startValueEntry, incValueEntry, endValueEntry, pm="+"))
endValueButton.bind("<Button-1>", lambda _: inc_entry(hexadecimalMode, endValueEntry, incValueEntry, ":)", pm="+"))
startValueButton.bind("<Button-3>", lambda _: inc_entry(hexadecimalMode, startValueEntry, incValueEntry, endValueEntry, pm="-"))
endValueButton.bind("<Button-3>", lambda _: inc_entry(hexadecimalMode, endValueEntry, incValueEntry, ":)", pm="-"))

autoEndButton.bind("<Button-1>", auto_end_switch)

corruptButton.bind("<Button-1>", corrupt_file)
corruptRepeatButton.bind("<Button-1>", corrupt_repeat_window)

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
incEngineButtons = [None, None, None]
incEngineRadios = [[None], ["Linear", "Exponential", "Random"], [None]]
incEngineChecks = [None, None, None]
incEngineAlts = [[None], ["Block Space", "Exponent", "Upper Bound"], [None]]
incEngine = Engine_Class(mainFrame, add_corrupt_engine, "Incrementer Algorithm", incEngineButtons,
                         incEngineEntries, incEngineRadios, incEngineChecks, incEngineAlts)

randEngine = Engine_Class(mainFrame, random_corrupt_engine, "Randomizer Algorithm", incEngineButtons,
                          incEngineEntries[:2], incEngineRadios[:2], incEngineChecks[:2], incEngineAlts[:2])

scramEngineEntries = ["Block Size", "Block Space", "*Block Gap"]
scramEngine = Engine_Class(mainFrame, scrambler_corrupt_engine, "Scrambler Algorithm", incEngineButtons,
                           scramEngineEntries, incEngineRadios, incEngineChecks, incEngineAlts)

copiEngine = Engine_Class(mainFrame, copier_corrupt_engine, "Copier Algorithm", incEngineButtons,
                          scramEngineEntries, incEngineRadios, incEngineChecks, incEngineAlts)

tiltEngineEntries = ["Block Size", "Block Space", "*Replace", "*Replace With"]
tiltEngineButtons = [None, None, None, None]
tiltEngineRadios = [[None], ["Linear", "Exponential", "Random"], [None], [None]]
tiltEngineChecks = [None, None, None, "Exclusive"]
tiltEngineAlts = [[None], ["Block Space", "Exponent", "Upper Bound"], [None], [None]]
tiltEngine = Engine_Class(mainFrame, tilter_corrupt_engine, "Tilter Algorithm", tiltEngineButtons,
                          tiltEngineEntries, tiltEngineRadios, tiltEngineChecks, tiltEngineAlts)

smoothEngineChecks = [None, None, "Termwise"]
smoothEngine = Engine_Class(mainFrame, smoother_corrupt_engine, "Smoother Algorithm", incEngineButtons,
                           scramEngineEntries, incEngineRadios, smoothEngineChecks, incEngineAlts)

blendEngineButtons = [None, None, "Select File"]
blendEngineEntries = ["Block Size", "Block Space", "File Offset"]
blendEngine = Engine_Class(mainFrame, blender_corrupt_engine, "Blender Algorithm", blendEngineButtons,
                           blendEngineEntries, incEngineRadios, incEngineChecks, incEngineAlts)

'''print(incEngine.entries)
print(incEngine.radioButtons)
print(incEngine.radioButtonVariables)
print(incEngine.checkButtons)
print(incEngine.checkButtonVariables)
print(incEngine.entryAlts)'''

algorithms = [incEngine, randEngine, scramEngine, copiEngine, tiltEngine, smoothEngine,
              blendEngine]

engineLabel["text"]=algorithms[currentEngine.get()-1].name #Setting algorithm label
algorithms[currentEngine.get()-1].display_layout(colorList) #Displays the current algorithm to window

for x in range(0, len(algorithms)):
    engineMenu.add_radiobutton(label=algorithms[x].name, var=currentEngine, command=switch_algorithm, value=x+1)


#------------------------------------------------------------------------------------

userFileLabel.pack(pady=5)
corruptButton.pack(pady=5)
corruptRepeatButton.pack(pady=5)

root.config(menu=parentMenu)

root.bind("<Alt-f>", enter_file)
root.bind("<Alt-i>", about_program_window)
root.bind("<Alt-s>", save_presets_window)
root.bind("<Alt-l>", load_presets)
root.bind("<Alt-r>", corrupt_repeat_window)

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
