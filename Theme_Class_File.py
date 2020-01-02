
#Scares Scramber Theme Class File
import tkinter as Tkinter
from tkinter import *
from tkinter import (Tk, ttk)

class Theme_Class:
    '''The class for each theme.'''
    def __init__(self, name, colorList):
        '''Initialization function.'''

        self.name = name
        self.colorList = colorList
        self.banner = colorList[3]
        self.icon = colorList[4]
