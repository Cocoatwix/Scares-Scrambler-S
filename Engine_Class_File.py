
#Scares Scrambler Engine Class File
import tkinter as Tkinter
from tkinter import *
from tkinter import (Tk, ttk)
from tkinter.filedialog import askopenfilename

import random
#import copy 

'''
Thanks to the following stackoverflow questions for...

Helping me with lambda functions:
stackoverflow.com/questions/16215045 (Q: evolutionizer, A: eumiro)
stackoverflow.com/questions/21148471 (Q: Dan, A: iCodez)
stackoverflow.com/questions/31664578 (Q: abc, A: Clodion)

Helping change theme colours:
https://stackoverflow.com/questions/14284492 (Q: user1967718, A: Bryan Oakley)
https://stackoverflow.com/questions/55311242 (Q: wowwee, A: Henry Yik)

Helping to update the progress bar:
https://stackoverflow.com/questions/27123676 (Q: Ramon Geessink, A: guest)

Misc:
https://stackoverflow.com/questions/6591931/getting-file-size-in-python (Q: 6966488-1, A: Artsiom Rudzenka)
'''

class Engine_Class:
    '''The class for each engine.'''
    def __init__(self, mainFrame, algorithm, name, buttons, entries, radioButtons, checkButtons, entryAlts):
        '''Initialization function. Yes, the code is messy, but at least it almost works'''
        
        self.mainFrame = mainFrame
        self.name = name
        self.corrupt = algorithm
        self.entries = []
        self.entButtons = [] #Random buttons beside entries
        self.extraFile = ""
        self.entryAlts = entryAlts
        self.hexadecimalMode = False #Keeps track of whether hexadecimal mode is on
        self.hideFileLabels = False

        for x in range(0, len(entries)): #Creating list of entries
            self.entries.append([Label(mainFrame, text=entries[x]), Entry(self.mainFrame)])
            self.entButtons.append(Button(self.mainFrame, text="Random",
                                command=lambda x=x: random_value(self.entries[x][1], self.hexadecimalMode))) #:)


        self.buttons = [] #Standalone buttons
        self.labels = []
        for x in range(0, len(buttons)):
            if buttons[x] == "Select File":
                self.buttons.append(Button(self.mainFrame, text="Select File",
                                           command=lambda x=x: self.get_second_file(x)))
                self.labels.append(Label(self.mainFrame, text="No file selected."))
            else:
                self.buttons.append(None)
                self.labels.append(None)
                

        self.radioButtons = []
        self.radioButtonVariables = []
        for x in range(0, len(radioButtons)): #Setting radio buttons
            tempList = []

            if radioButtons[x] == [None]: #If we don't have any radio buttons on this row
                self.radioButtonVariables.append(None)
            else:
                self.radioButtonVariables.append(IntVar())
                self.radioButtonVariables[x].set(1)
            
            for y in range(0, len(radioButtons[x])): #Formatting list to group radiobuttons together
                        
                if radioButtons[x][y] != None: #If we're actually putting a radiobutton down
                    tempList.append(Radiobutton(self.mainFrame, text=radioButtons[x][y],
                                                 value=y+1, variable=self.radioButtonVariables[x]))
                else:
                    tempList.append(None)
                    
            self.radioButtons.append(tempList)

        self.checkButtons = []
        self.checkButtonVariables = []
        for x in range(0, len(checkButtons)): #Setting checkbuttons
            
            if checkButtons[x] != None: #If we actually need a checkbutton
                self.checkButtonVariables.append(IntVar())
                self.checkButtons.append(Checkbutton(self.mainFrame, text=checkButtons[x],
                                            var=self.checkButtonVariables[x]))
            else:
                self.checkButtons.append(None)
                self.checkButtonVariables.append(None)

        for x in range(0, len(self.entryAlts)):
            if self.entryAlts[x] != [None]:
                for y in self.radioButtons[x]:
                    y.config(command=lambda x=x: self.switch_entry_text(x))
        

    def get_corruption_variables(self):
        '''Returns a list of all the relevant corruption variables'''
        entryTemp = [x[1] for x in self.entries] #Getting all entries
        radioTemp = []
        checkTemp = []

        for x in self.radioButtonVariables:
            if x != None:
                radioTemp.append(x)

        for x in self.checkButtonVariables:
            if x != None:
                checkTemp.append(x)

        if self.extraFile != "":
            return [entryTemp.copy(), radioTemp.copy(), checkTemp.copy(), open(self.extraFile, "rb+")] #May not be rb+
        else:
            return [entryTemp.copy(), radioTemp.copy(), checkTemp.copy()]


    def display_layout(self, colorList=[]):
        '''Puts the layout onto the window'''
        rowCounter = 5 #For placing things in the right row

        for x in range(0, len(self.entries)): #The five is so that we start on the correct row
            self.entries[x][0].grid(row=rowCounter, column=0, pady=5, padx=5, sticky=E)
            self.entries[x][1].grid(row=rowCounter, column=1, columnspan=2, pady=5)
            self.entButtons[x].grid(row=rowCounter, column=3, pady=5)

            if self.radioButtons[x][0] != None:
                rowCounter += 1
                for y in range(0, len(self.radioButtons[x])):
                    if y >= 2: #Accounting for columnspan of entries
                        self.radioButtons[x][y].grid(row=rowCounter, column=y+1, pady=5)
                    else:
                        self.radioButtons[x][y].grid(row=rowCounter, column=y, pady=5)

            if self.checkButtons[x] != None:
                rowCounter += 1
                self.checkButtons[x].grid(row=rowCounter, column=1, pady=5, padx=30, sticky=W,
                                       columnspan=3)

            if self.buttons[x] != None:
                rowCounter += 1
                if self.extraFile == "":
                    self.labels[x]["text"] = "No file loaded."
                elif self.hideFileLabels and self.buttons[x]["text"] == "Select File": #Hiding file paths
                    self.labels[x]["text"] = "File Loaded."
                else:
                    self.labels[x]["text"] = shorten_text(self.extraFile, 15)
                self.labels[x].grid(row=rowCounter, column=1, columnspan=2, pady=5, padx=5)
                self.buttons[x].grid(row=rowCounter, column=3, pady=5, padx=5)
                
            rowCounter += 1

        self.recolor(colorList)


    def recolor(self, colorList):
        '''Recolors the layout stuff with given colors'''
        for x in range(0, len(self.entries)):
            self.entries[x][0].config(bg=colorList[2], fg=colorList[1]) #Labels
            self.entries[x][1].config(bg=colorList[0], fg=colorList[1], insertbackground=colorList[1],
                                      selectbackground=colorList[5]) #Entries
            
            self.entButtons[x].config(bg=colorList[2], fg=colorList[1],
                                   activebackground=colorList[0], activeforeground=colorList[1]) #Buttons

            if self.buttons[x] != None:
                self.buttons[x].config(bg=colorList[2], fg=colorList[1],
                                   activebackground=colorList[0], activeforeground=colorList[1]) #Standalone buttons

            if self.labels[x] != None:
                self.labels[x].config(bg=colorList[2], fg=colorList[1]) #Labels

            if self.radioButtons[x][0] != None:
                for y in range(0, len(self.radioButtons[x])):
                    self.radioButtons[x][y].config(bg=colorList[2], fg=colorList[1], selectcolor=colorList[0],
                                                    activebackground=colorList[2], activeforeground=colorList[1])

            if self.checkButtons[x] != None:
                self.checkButtons[x].config(bg=colorList[2], fg=colorList[1], selectcolor=colorList[0],
                                            activebackground=colorList[2], activeforeground=colorList[1])


    def hide_layout(self):
        '''Hides the layout'''
        for x in self.entries:
            x[0].grid_forget()
            x[1].grid_forget()

        for x in self.entButtons:
            x.grid_forget()

        for x in self.buttons:
            if x != None:
                x.grid_forget()

        for x in self.labels:
            if x != None:
                x.grid_forget()

        for x in self.radioButtons:
            if x != [None]:
                for y in x:
                    y.grid_forget()

        for x in self.checkButtons:
            if x != None:
                x.grid_forget()


    def switch_entry_text(self, num):
        '''Switches the text on an entry when prompted'''
        self.entries[num][0]["text"] = self.entryAlts[num][self.radioButtonVariables[num].get()-1]
        #print(num)
        #print(self.entries[num][0]["text"])
        #Holy shit


    def get_second_file(self, x, event=None):
        '''Gets the file path for the second file'''
        self.extraFile = askopenfilename()
        if self.hideFileLabels == False:
            self.labels[x]["text"] = shorten_text(self.extraFile, 15)
        else:
            self.labels[x]["text"] = "File loaded."


def random_value(entry, hexMode):
    '''Generates a random value for an entry'''
    '''This is basically copied from main file'''
    #I should make this more general, to make it work with the buttons in the main file
    entry.delete(0, END)
    if hexMode:
        ran1 = random.randint(0, 15)
        ran2 = random.randint(0, 15)
        ran1 = singular_hex_convert(ran1)
        ran2 = singular_hex_convert(ran2)

        entry.insert(0, "0x"+str(ran1)+str(ran2))
    else:
        entry.insert(0, random.randint(0, 255))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def inc_entry(hexMode, entry, inc, end, pm="+", event=None):
    '''Increments the entries'''
    try:
        endValue = 0 #Default value
        if hexMode:
            incValue = int(float.fromhex(inc.get())) #Getting values
            entryBoxValue = int(float.fromhex(entry.get()))
            if end != ":)":
                endValue = int(float.fromhex(end.get()))
            
        else:
            incValue = int(inc.get()) 
            entryBoxValue = int(entry.get())
            if end != ":)":
                endValue = int(end.get())
            
        if pm == "+": #Setting values (+/- inc)
            entryBoxValue += incValue
        else:
            entryBoxValue -= incValue
            
        if entryBoxValue < 0:
            entryBoxValue = 0

        if entryBoxValue > endValue and end != ":)":
            if endValue != 0: #Preventing division by zero error
                entryBoxValue = entryBoxValue % endValue
            else:
                entryBoxValue = 0

        if hexMode:
            entryBoxValue = hex_convert(entryBoxValue)

        entry.delete(0, "end")
        entry.insert(0, entryBoxValue)
        
    except ValueError:
        messagebox.showwarning("What are you doing?", "Please use a whole number for"
                               " the increment value, thanks!")


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


def singular_hex_convert(n):
    '''Converts the numbers 10 to 15 to hex'''
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

    return newN


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


def clear_textWidget(event, textWidget, textCondition=""):
    '''Clears newFileText when it's clicked'''
    if textCondition != "":
        if textWidget.get(1.0, END)[:-1] == textCondition: #Only clear if messages match
            textWidget.delete("1.0", END)
            textWidget.unbind("<Button-1>") #Prevents text from clearning when there's important info
    else:
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


def check_for_char(text, char="."):
    '''Checks to see if there's a period in the given text'''
    isChar = False
    position = 0
    for x in range(len(text)-1, -1, -1):
        if text[x] == char:
            isChar = True
            position = x
            break

    if isChar:
        return position
    else:
        return False

#xEndValue is needed to simplify corrupt_file code. It's a variable that doesn't do anything

def add_corrupt_engine(cV, blockSpace, baseFile, corruptedFile, xEndValue):
    '''Does adding and subtracting'''
    currentByte = list(baseFile.read(cV[0][0])) #Gets the byte
    for x in range(0, len(currentByte)):
        currentByte[x] += cV[0][2] #cV[0][2] = addValue
        if currentByte[x] > 255 or currentByte[x] < 0: #If it's bigger than a byte OR if it's a negative
            currentByte[x] = currentByte[x] % 256
        corruptedFile.write(currentByte[x].to_bytes(1, byteorder="big"))

    copy_file_contents(baseFile, corruptedFile, blockSpace) #The gap in between - Shoutout to Jason
    

def random_corrupt_engine(cV, blockSpace, baseFile, corruptedFile, xEndValue):
    '''Does random byte changes'''

    byteList = baseFile.read(cV[0][0]) #Getting remaining length of file
    for y in range(0, len(byteList)): #Corrupting part, cV[0][0] = blockSize
        currentByte = random.randrange(0, 255)
        currentByte = (currentByte).to_bytes(1, byteorder="big")
        corruptedFile.write(currentByte)

    copy_file_contents(baseFile, corruptedFile, blockSpace) #The gap in between


def scrambler_corrupt_engine(cV, blockSpace, baseFile, corruptedFile, xEndValue):
    '''Does scrambles to bytes'''
    currentByteList1 = baseFile.read(cV[0][0])
    bufferList = baseFile.read(cV[0][2])
    currentByteList2 = baseFile.read(cV[0][0])
        
    corruptedFile.write(currentByteList2)
    corruptedFile.write(bufferList)
    corruptedFile.write(currentByteList1)

    copy_file_contents(baseFile, corruptedFile, blockSpace) #The gap in between


def copier_corrupt_engine(cV, blockSpace, baseFile, corruptedFile, endValue):
    '''Does copying stuff'''
    
    #cV[0][0] = blockSize
    currentByteList1 = baseFile.read(cV[0][0])
    
    #cV[0][2] = blockGap
    bufferList = baseFile.read(abs(cV[0][2]))

    currentByteList2 = baseFile.read(cV[0][0])

    if cV[0][2] < 0: #Negative
        if len(currentByteList2) != len(currentByteList1): #If currentByteList2 got cut off
            corruptedFile.write(currentByteList2+currentByteList1[len(currentByteList2):]) #Write corrupted bytes
        else:
            corruptedFile.write(currentByteList2) #Write corrupted bytes
        corruptedFile.write(bufferList) #Write corrupted bytes
        corruptedFile.write(currentByteList2) #Write corrupted bytes

    else: #Positive
        corruptedFile.write(currentByteList1) #Write corrupted bytes
        corruptedFile.write(bufferList) #Write corrupted bytes
        if len(currentByteList2) != len(currentByteList1): #If we need to shorten the first byte list
            corruptedFile.write(currentByteList1[:len(currentByteList2)]) #Write corrupted bytes
        else:
            corruptedFile.write(currentByteList1) #Write corrupted bytes

    copy_file_contents(baseFile, corruptedFile, blockSpace)


def tilter_corrupt_engine(cV, blockSpace, baseFile, corruptedFile, xEndValue):
    '''You know what it does by now'''

    currentByte = list(baseFile.read(cV[0][0])) #Gets the bytes
    replaceByte = cV[0][3] % 255 #cV[0][3] = replace with

    if cV[2][0] == 1: #If exclusive
        for x in range(0, len(currentByte)):
            if currentByte[x] == cV[0][2]: #cV[0][2] = compareByte (replace)
                corruptedFile.write(replaceByte.to_bytes(1, byteorder="big")) 
            else:
                corruptedFile.write(currentByte[x].to_bytes(1, byteorder="big")) 
                
    else: #General
        for x in range(0, len(currentByte)):
            corruptedFile.write(replaceByte.to_bytes(1, byteorder="big"))

    copy_file_contents(baseFile, corruptedFile, blockSpace)


def smoother_corrupt_engine(cV, blockSpace, baseFile, corruptedFile, endValue):
    '''Does smoothing stuff'''
    
    #cV[0][0] = blockSize
    if cV[0][0] <= 0:
        bytes1 = baseFile.read(1)
    else:
        bytes1 = baseFile.read(cV[0][0])
    currentByteList1 = list(bytes1)
    
    #cV[0][2] = blockGap
    bufferList = baseFile.read(abs(cV[0][2]))

    if cV[0][0] <= 0:
        bytes2 = baseFile.read(1)
    else:
        bytes2 = baseFile.read(cV[0][0])
    currentByteList2 = list(bytes2)

    if cV[2][0] == 0: #Normal
        theSum = sum(currentByteList1) + sum(currentByteList2)
        try: #Getting average of all bytes in bytes1 and bytes2
            theSum /= (len(currentByteList1) + len(currentByteList2)) #The average of all the bytes
        except ZeroDivisionError:
            theSum = 0
            
        theSum = int(theSum) #Making the average a nice number
        newByteList = [(theSum).to_bytes(1, byteorder="big") for x in range(0, cV[0][0])]

    else: #Termwise
        lenList2 = len(currentByteList2)
        newByteList = []
        for x in range(0, len(currentByteList1)):
            if x < lenList2:
                newByteList.append(((currentByteList1[x]+currentByteList2[x])//2).to_bytes(1, byteorder="big"))
            else:
                newByteList.append(currentByteList1[x].to_bytes(1, byteorder="big"))

    if cV[0][2] < 0: #Negative
        if len(bytes1) != len(bytes2): #Preventing the file's size from changing
            for x in range(0, len(bytes2)):
                corruptedFile.write(newByteList[x]) #Write corrupted bytes
            corruptedFile.write(bytes1[len(bytes2):]) #Write corrupted bytes
        else:
            for x in range(0, cV[0][0]):
                corruptedFile.write(newByteList[x]) #Write corrupted bytes

        corruptedFile.write(bufferList)
        corruptedFile.write(bytes2)

    else: #Positive
        corruptedFile.write(bytes1) #Write corrupted bytes
        corruptedFile.write(bufferList)

        if len(bytes1) != len(bytes2): #Preventing the file's size from changing
            for x in range(0, len(bytes2)):
                corruptedFile.write(newByteList[x])
        else:
            for x in range(0, cV[0][0]):
                corruptedFile.write(newByteList[x])

    copy_file_contents(baseFile, corruptedFile, blockSpace)


def blender_corrupt_engine(cV, blockSpace, baseFile, corruptedFile, xEndValue):
    '''Blends two files together'''
    '''print(cV)
    print(blockSpace)
    print(baseFile)
    print(corruptedFile)'''

    newBytes = cV[3].read(cV[0][0]) #Bytes from extraFile to write

    if newBytes != "": #If we have data to write
        if len(newBytes) < cV[0][0]: #We need to add padding to keep file sizes the same
            corruptedFile.write(newBytes)
            baseFile.seek(len(newBytes)) #Making sure our files are synced up
            padding = baseFile.read(cV[0][0]-len(newBytes))
            corruptedFile.write(padding)
        else:
            corruptedFile.write(newBytes)
            baseFile.seek(baseFile.tell()+cV[0][0]) #Making sure our files are synced up
    else:
        newBytes = baseFile.read(cV[0][0])
        corruptedFile.write(newBytes)
    copy_file_contents(baseFile, corruptedFile, blockSpace)

    
    #cV[3] = secondFile name. Code this later lol
    #cV[0][2] = offset


def copy_file_contents(baseFile, corruptedFile, endValue):
    '''For copying uncorrupted parts of a file'''
    if endValue != 0:
        corruptedFile.write(baseFile.read(abs(endValue))) #The gap in between



        

        


    


    
