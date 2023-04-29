# -*- coding: utf-8 -*-
"""
Program Title: StarCitizenCompanion.py
Program Author: Dillon Brandon
Creation Date: 04/04/2023 - 05/12/2023
Purpose:
A tkinter GUI application using Star Citizen ship info and images to create a library of ships that users can
save to their "hangar" or "wishlist".

Variables:
desiredShip(string) - A global variable to store the desired ship's name between funtions.
loaners(string) - A global variable to store the loaners of a desired ship.
shipList(list) - A global variable to store all available ships.
hangarList(list) - A global variable to store all ships saved to the hangar.
wishList(list) - A global variable to store all ships saved to the wishlist.
"""
from breezypythongui import *
from PIL import ImageTk, Image
from tkinter import PhotoImage
from tkinter.font import Font
desiredShip = "Not Set Yet"
loaners = "Not Set Yet"
shipList = []
hangarList = []
wishList = []

#################### Above: Module Imports ############################
#################### Below: Window Programming ########################

class Companion(EasyFrame):
    '''Offers the backbone of the program GUI'''
    global shipList
    global hangarList
    global wishList
    global desiredShip
    def __init__(self):
        '''Sets up the window and the label.'''
        EasyFrame.__init__(self, title="Star Citizen Hangar Companion", width = 1200, height = 700, background="cornsilk4")
        self.own = self.addButton(text = "Hangar", row = 0, column = 0, command = self.Hangar)
        self.all = self.addButton(text = "Ship Store", row = 0, column = 1, command = self.ShipStore)
        self.want = self.addButton(text = "Wishlist", row = 0, column = 2, command = self.Wishlist)
        self.own.grid(sticky="NEW")
        self.all.grid(sticky="NEW")
        self.want.grid(sticky="NEW")
        EasyFrame.addCanvas(self, row=1, column=0, columnspan=23, width=1200, height=600, background="cornsilk3")
        
    def Hangar(self):
        '''Opens the Hangar and populates it'''
        row = 1
        column = 0
        self.own['state'] = DISABLED
        self.all['state'] = NORMAL
        self.want['state'] = NORMAL
        for item in hangarList:
            row += 1
            self.ship = self.addButton(text = item, row = row, column = column, columnspan=3, command = lambda item = item: self.shipDetails(item))
            self.ship.grid(sticky='NEW')
        
    def ShipStore(self):
        '''Opens the Ship Store and populates it'''
        row = 1
        column = 0
        count = 0
        self.own['state'] = NORMAL
        self.all['state'] = DISABLED
        self.want['state'] = NORMAL
        for item in shipList:
            if row < 10:
                row += 1
                self.ship = self.addButton(text = item, row = row, column = column, columnspan=3, command = lambda item = item: self.shipDetails(item))
                self.ship.grid(sticky='NEW')
            
    def Wishlist(self):
        '''Opens the Wishlist and populates it'''
        row = 1
        column = 0
        self.own['state'] = NORMAL
        self.all['state'] = NORMAL
        self.want['state'] = DISABLED
        for item in wishList:
            row += 1
            ship = item
            self.ship = self.addButton(text = item, row = row, column = column, columnspan=3, command = lambda item = item: self.shipDetails(item))
            self.ship.grid(sticky='NEW')
    
    def shipDetails(self, ship):
        '''Finds the ship's info and displays it along with the ship's image. Also defines the loaners for the desired ship.'''
        global desiredShip
        global shipList
        global loaners
        import os
        import json
        programDirectory = os.getcwd()
        
        desiredShip = ship 
        os.chdir("Ship Store/")
        os.chdir(desiredShip)
        file = open("shipInfo.txt", 'r')
        infoJson = file.read()
        file.close()
        os.chdir(programDirectory)
        shipInfo = json.loads(infoJson)
        for element in shipInfo:
            print(element+": "+shipInfo[element])
        loaners = shipInfo["Loaners"]
        loaners = loaners.split(", ")
        
        os.chdir("Ship Store/"+desiredShip)
        
        img = Image.open(desiredShip+".jpg")
        img = img.resize((280,158), Image.LANCZOS)   #Make it "thumbnail size" for the ship info page
        
        os.chdir(programDirectory)
        
#################### Above: Window Programming ##########################
#################### Below: Program Functions ###########################

def oneBlankLines():
    print("")

def twoBlankLines():
    print("")
    print("")

def endOfProgram():
    print("End of program.")
    oneBlankLines()

def welcomeMsg():
    print(__doc__)

def echoPrint(pValue):
    print("The input value entered is:  ",pValue)
    
def houseKeeping():
    '''This function will ensure the Ship Store files exist and that the Hangar and Wishlist directories exist'''
    import os
    global shipList
    global hangarList
    global wishList
    programDirectory = os.getcwd()
    storeDirectory = programDirectory+"/Ship Store"
    hangarDirectory = programDirectory+"/Hangar"
    wishDirectory = programDirectory+"/Wishlist"
    currentDirectories = os.listdir(programDirectory)
    if storeDirectory not in currentDirectories:
        print("You are missing the Ship files.")
    else:
        hangarExist = False
        while hangarExist == False:
            if hangarDirectory not in currentDirectories:
                os.mkdir("Hangar")
                hangarExist = True
                hangarList = os.listDir(hangarDirectory)
                hangarList.sort()
            else:
                hangarExist = True
                hangarList = os.listDir(hangarDirectory)
                hangarList.sort()
        wishlistExist = False
        while wishlistExist == False:
            if wishDirectory not in currentDirectories:
                os.mkdir("Wishlist")
                wishlistExist = True
                wishList = os.listDir(wishDirectory)
                wishList.sort()
            else:
                wishlistExist = True
                wishList = os.listdir(wishDirectory)
                wishList.sort()
    shipStore()
    print(shipList)
    print(hangarList)
    print(wishList)
                
def shipStore():
    '''Lists all available ship options'''
    global shipList
    import os
    programDirectory = os.getcwd()
    os.chdir(programDirectory+"/Ship Store")
    storeDirectory = os.getcwd()
    shipList = os.listdir(storeDirectory)
    shipList.sort()
    os.chdir(programDirectory)

def shipSearch():
    '''Allows the user to input which ship they want to view'''
    global desiredShip
    global shipList
    global loaners
    import os
    programDirectory = os.getcwd()
    shipExists = False
    while shipExists == False:
        shipName = input("Input desired ship: ")
        if shipName not in shipList:
            print("You have entered an invald name.")
        else:
            desiredShip = shipName
            if desiredShip in shipList:
                shipExists = True
            else:
                print("Potential file error, check name")



def userChoice():
    '''Gives the user the choice to add, remove, or cancel.'''
    global desiredShip
    choiceCorrect = False
    inPrompt = "Do you want to add or remove "+desiredShip+"? (add, remove, or no) "
    while choiceCorrect == False:
        userChoice = input(inPrompt)
        if userChoice == "add" or "remove" or "no":
            choiceCorrect = True
            if userChoice == "add":
                shipAdd()
            elif userChoice == "remove":
                shipRemove()
        else:
            print("Please enter a valid response.")

def shipAdd():
    '''Copies the ship's Ship Store directory into the Hangar directory, and the loaners into a Loaners directory inside the ship's directory.'''
    global desiredShip
    global shipList
    global loaners
    import os
    import shutil
    programDirectory = os.getcwd()
    hangarList = os.listdir(programDirectory+"\\Hangar")
    if desiredShip not in hangarList:
        #shutil copytree function based on comment by nzot
        #https://stackoverflow.com/questions/1994488/copy-file-or-directories-recursively-in-python
        shutil.copytree(programDirectory+"\\Ship Store\\"+desiredShip, programDirectory+"\\Hangar\\"+desiredShip)
    if 'N/A' not in loaners:
        for word in loaners:
            if word in shipList:
                    shutil.copytree(programDirectory+"\\Ship Store\\"+word, programDirectory+"\\Hangar\\"+desiredShip+"\\Loaners\\"+word)
            else:
                print("Potential file error, check loaners")

def shipRemove():
    '''Deletes the ship's Ship Store directory (and loaners) from the Hangar directory'''
    global desiredShip
    global shipList
    global loaners
    import os
    import shutil
    programDirectory = os.getcwd()
    hangarList = os.listdir(programDirectory+"\\Hangar")
    loanerList = os.listdir(programDirectory+"\\Hangar\\Loaners")
    if desiredShip in hangarList:
        #shutil copytree function based on comment by nzot
        #https://stackoverflow.com/questions/1994488/copy-file-or-directories-recursively-in-python
        shutil.rmtree(programDirectory+"\\Hangar\\"+desiredShip)
    if 'N/A' not in loaners:
        for word in loaners:
            if word in shipList:
                if word in loanerList:
                    shutil.rmtree(programDirectory+"\\Hangar\\Loaners\\"+word)
            else:
                print("Potential file error, check loaners")

#################### Above: Program Functions ######################
#################### Below: Main Program ###########################

def main():
#    welcomeMsg()
    houseKeeping()
    Companion().mainloop()
#    endOfProgram()
    
    
# main program =========================================================
if __name__ == "__main__":
    main()


    
