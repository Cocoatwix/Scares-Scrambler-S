
#Scares Scrambler Engine Class File
import tkinter as Tkinter
from tkinter import *
from tkinter import (Tk, ttk)

import random
#import copy #Allows me to copy variables without linking things (giving addresses instead of values)

'''
Thanks to the following stackoverflow questions for helping me with lambda functions:
stackoverflow.com/questions/16215045 (Q: evolutionizer, A: eumiro)
stackoverflow.com/questions/21148471 (Q: Dan, A: iCodez)
stackoverflow.com/questions/31664578 (Q: abc, A: Clodion)
'''

class Engine_Class:
    '''The class for each engine.'''
    def __init__(self, mainFrame, algorithm, name, entries, radioButtons, checkButtons, entryAlts):
        '''Initialization function. Yes, the code is messy, but at least it almost works'''
        
        self.mainFrame = mainFrame
        self.name = name
        self.corrupt = algorithm
        self.entries = []
        self.buttons = []
        self.specials = []
        self.entryAlts = entryAlts
        self.hexadecimalMode = False #Keeps track of whether hexadecimal mode is on

        for x in range(0, len(entries)): #Creating list of entries
            self.entries.append([Label(mainFrame, text=entries[x]), Entry(self.mainFrame)])
            self.buttons.append(Button(self.mainFrame, text="Random",
                                command=lambda x=x: self.random_value(self.entries[x][1]))) #Change this later

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
                    funVar = x #This variable prevents the address being copied into the function
                    y.config(command=lambda x=x: self.switch_entry_text(x)) #
        

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

        return [entryTemp.copy(), radioTemp.copy(), checkTemp.copy()]


    def display_layout(self, colorList=[]):
        '''Puts the layout onto the window'''
        rowCounter = 5 #For placing things in the right row

        for x in range(0, len(self.entries)): #The five is so that we start on the correct row
            self.entries[x][0].grid(row=rowCounter, column=0, pady=5, padx=5, sticky=E)
            self.entries[x][1].grid(row=rowCounter, column=1, columnspan=2, pady=5)
            self.buttons[x].grid(row=rowCounter, column=3, pady=5)

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

            rowCounter += 1
            self.recolor(colorList)


    def recolor(self, colorList):
        '''Recolors the layout stuff with given colors'''
        for x in range(0, len(self.entries)):
            self.entries[x][0].config(bg=colorList[2], fg=colorList[1]) #Labels
            self.entries[x][1].config(bg=colorList[0], fg=colorList[1]) #Entries
            self.buttons[x].config(bg=colorList[2], fg=colorList[1],
                                   activebackground=colorList[0], activeforeground=colorList[1]) #Buttons

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

        for x in self.buttons:
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


    def random_value(self, entry):
        '''Generates a random value for an entry'''
        '''This is basically copied from main file'''
        entry.delete(0, END)
        if self.hexadecimalMode:
            ran1 = random.randint(0, 15)
            ran2 = random.randint(0, 15)
            ran1 = singular_hex_convert(ran1)
            ran2 = singular_hex_convert(ran2)

            entry.insert(0, "0x"+str(ran1)+str(ran2))
        else:
            entry.insert(0, random.randint(0, 255))


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


def add_corrupt_engine(cV, blockSpace, baseFile, corruptedFile):
    '''Does adding and subtracting'''

    for y in range(0, cV[0][0]): #Corrupting part, cV[0][0] = blockSize
        currentByte = baseFile.read(1) #Gets the byte
        if currentByte == b"":
            break
        currentByte = int.from_bytes(currentByte, byteorder="big")
        currentByte += cV[0][2] #cV[0][2] = addValue
        if currentByte > 255 or currentByte < 0: #If it's bigger than a byte OR if it's a negative
            currentByte = currentByte % 256
        currentByte = (currentByte).to_bytes(1, byteorder="big")
        corruptedFile.write(currentByte)

    copy_file_contents(baseFile, corruptedFile, blockSpace) #The gap in between - Shoutout to Jason
    

def random_corrupt_engine(cV, blockSpace, baseFile, corruptedFile):
    '''Does random byte changes'''

    for y in range(0, cV[0][0]): #Corrupting part, cV[0][0] = blockSize
        currentByte = baseFile.read(1) #Gets the byte
        if currentByte == b"":
            break
        currentByte = int.from_bytes(currentByte, byteorder="big")
        currentByte += random.randrange(0, 255)
        if currentByte > 255: #If it's bigger than a byte
            currentByte = currentByte % 256
        currentByte = (currentByte).to_bytes(1, byteorder="big")
        corruptedFile.write(currentByte)

    copy_file_contents(baseFile, corruptedFile, blockSpace) #The gap in between


def scrambler_corrupt_engine(cV, blockSpace, baseFile, corruptedFile):
    '''Does scrambles to bytes'''
    currentByteList1 = []
    bufferList = []
    currentByteList2 = []

    for y in range(0, cV[0][0]): #Corrupting part, cV[0][0] = blockSize
        currentByte = baseFile.read(1)
        if currentByte == b"":
            break
        currentByteList1.append(currentByte) #Gets the bytes

    for z in range(0, abs(cV[0][2])): #The gap in between, cV[0][2] = blockGap
        currentByte = baseFile.read(1)
        if currentByte == b"":
            break
        bufferList.append(currentByte)

    for y in range(0, cV[0][0]): #Corrupting part
        currentByte = baseFile.read(1)
        if currentByte == b"":
            break
        currentByteList2.append(currentByte) #Gets the bytes
        
    for x in currentByteList2:
        corruptedFile.write(x)

    for x in bufferList:
        corruptedFile.write(x)

    for x in currentByteList1:
        corruptedFile.write(x)

    copy_file_contents(baseFile, corruptedFile, blockSpace) #The gap in between


def copier_corrupt_engine(cV, blockSpace, baseFile, corruptedFile, endValue):
    '''Does copying stuff'''
    currentByteList1 = []
    bufferList = []
    currentByteList2 = []
    counter = 0

    for y in range(0, cV[0][0]): #cV[0][0] = blockSize
        currentByte = baseFile.read(1)
        if currentByte == b"":
            break
        currentByteList1.append(currentByte)

    for z in range(0, abs(cV[0][2])): #cV[0][2] = blockGap
        currentByte = baseFile.read(1)
        if currentByte == b"":
            break
        bufferList.append(currentByte)

    for y in range(0, cV[0][0]):
        currentByte = baseFile.read(1)
        if currentByte == b"":
            break
        currentByteList2.append(currentByte)

    if cV[0][2] < 0: #Negative
        for x in currentByteList2:
            if corruptedFile.tell() >= endValue:
                break
            corruptedFile.write(x)
        for x in bufferList:
            if corruptedFile.tell() >= endValue:
                break
            corruptedFile.write(x)
        for x in currentByteList2:
            if corruptedFile.tell() >= endValue:
                break
            corruptedFile.write(x)
    else: #Positive
        for x in currentByteList1:
            if corruptedFile.tell() >= endValue:
                break
            corruptedFile.write(x)
        for x in bufferList:
            if corruptedFile.tell() >= endValue:
                break
            corruptedFile.write(x)
        for x in currentByteList1:
            if corruptedFile.tell() >= endValue:
                break
            corruptedFile.write(x)

    copy_file_contents(baseFile, corruptedFile, blockSpace)


def tilter_corrupt_engine(cV, blockSpace, baseFile, corruptedFile):
    '''You know what it does by now'''

    for y in range(0, cV[0][0]): #Corrupting part, cV[0][0] = blockSize
        currentByte = baseFile.read(1) #Gets the byte
        if currentByte == b"":
            break
        currentByte = int.from_bytes(currentByte, byteorder="big")

        if cV[2][0] == 1: #If exclusive
            compareByte = cV[0][2] #cV[0][2] = replace
            if currentByte == compareByte:
                currentByte = cV[0][3] #cV[0][3] = replace with
        else:
            currentByte = cV[0][3]
            
        currentByte = (currentByte).to_bytes(1, byteorder="big")
        corruptedFile.write(currentByte)

    copy_file_contents(baseFile, corruptedFile, blockSpace)


def copy_file_contents(baseFile, corruptedFile, endValue):
    '''For copying uncorrupted parts of a file'''
    
    for z in range(0, endValue): #The gap in between
        currentByte = baseFile.read(1)
        corruptedFile.write(currentByte) #The gap in between



        

        


    


    
