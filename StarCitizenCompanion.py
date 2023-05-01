# -*- coding: utf-8 -*-
"""
Program Title: StarCitizenCompanion.py
Program Author: Dillon Brandon
Creation Date: 04/04/2023 - 05/12/2023
Purpose:
A tkinter GUI application using Star Citizen ship info and images to create a library of ships that users can
save to their "hangar" or "wishlist".

Variables:
programDirectory(string) - A global variable to offer a way to the home directory.
desiredShip(string) - A global variable to store the desired ship's name between funtions.
loaners(string) - A global variable to store the loaners of a desired ship.
shipList(list) - A global variable to store all available ships.
hangarList(list) - A global variable to store all ships saved to the hangar.
wishList(list) - A global variable to store all ships saved to the wishlist.
"""
from breezypythongui import *
from tkinter import *
from tkinter.font import Font
from PIL import ImageTk, Image
programDirectory = "Not Set Yet"
desiredShip = "Not Set Yet"
loaners = "Not Set Yet"
shipList = []
hangarList = []
wishList = []

#################### Above: Module Imports ############################
#################### Below: Main Window ###############################

class Companion(EasyFrame):
    '''Offers the backbone of the program GUI'''
    global shipList
    global hangarList
    global wishList
    global desiredShip
    def __init__(self):
        '''Sets up the window and the label.'''
        mainWindow = EasyFrame.__init__(self, title="Star Citizen Hangar Companion", width = 1200, height = 700, background="cornsilk4")
        self.own = self.addButton(text = "Hangar", row = 0, column = 0, columnspan = 3, command = self.Hangar)
        self.all = self.addButton(text = "Ship Store", row = 0, column = 3, columnspan = 3, command = self.ShipStore)
        self.want = self.addButton(text = "Wishlist", row = 0, column = 6, columnspan = 3, command = self.Wishlist)
        self.own.grid(sticky="NEW")
        self.all.grid(sticky="NEW")
        self.want.grid(sticky="NEW")
        self.shipFull = self.addListbox(row = 1, column = 0, columnspan = 6, rowspan = 3, height = 40)
        self.shipFull.grid(sticky="NEWS")
        self.Info = self.addButton(text = "Details", row = 1, column = 6, command = self.shipAccess)
        self.ShipStore()

    def Hangar(self):
        import os
        global hangarList
        '''Opens the Hangar and populates it'''
        self.own['state'] = DISABLED
        self.all['state'] = NORMAL
        self.want['state'] = NORMAL
        self.button1.destroy()
        self.button2.destroy()
        self.button1 = self.addButton(text = "Remove from Hangar", row = 2, column = 6, command = self.hangarRemove)
        self.button2 = self.addButton(text = "Show Loaners", row = 3, column = 6, command = self.hangarLoaners)
        self.shipFull.clear()
        listSize = self.shipFull.size()
        hangarDirectory = programDirectory+"/Hangar"
        hangarList = os.listdir(hangarDirectory)
        for item in hangarList:
            if item != "Loaners":
                if listSize <= 165:
                    self.ship = self.shipFull.insert(END, item)
        self.costTotalHangar()
        
    def ShipStore(self):
        '''Opens the Ship Store and populates it'''
        self.own['state'] = NORMAL
        self.all['state'] = DISABLED
        self.want['state'] = NORMAL
        if hasattr(self, 'fullPrice'):
            self.fullPrice.destroy()
        if hasattr(self, 'warbondPrice'):
            self.warbondPrice.destroy()
        if hasattr(self, 'button1'):
            self.button1.destroy()
        if hasattr(self, 'button2'):
            self.button2.destroy()
        self.button1 = self.addButton(text = "Add to Hangar", row = 2, column = 6, command = self.hangarAdd)
        self.button2 = self.addButton(text = "Add to Wishlist", row = 3, column = 6, command = self.wishAdd)
        self.shipFull.clear()
        listSize = self.shipFull.size()
        for item in shipList:
            if listSize <= 165:
                self.ship = self.shipFull.insert(END, item)
            
    def Wishlist(self):
        import os
        global wishList
        '''Opens the Wishlist and populates it'''
        self.own['state'] = NORMAL
        self.all['state'] = NORMAL
        self.want['state'] = DISABLED
        self.button1.destroy()
        self.button2.destroy()
        self.button1 = self.addButton(text = "Remove from Wishlist", row = 2, column = 6, command = self.wishRemove)
        self.button2 = self.addButton(text = "Show Loaners", row = 3, column = 6, command = self.wishLoaners)
        self.shipFull.clear()
        listSize = self.shipFull.size()
        wishDirectory = programDirectory+"/Wishlist"
        wishList = os.listdir(wishDirectory)
        for item in wishList:
            if item != "Loaners":
                if listSize <= 165:
                    self.ship = self.shipFull.insert(END, item)
        self.costTotalWishlist()
                
    def hangarAdd(self):
        '''Copies the ship's Ship Store directory into the Hangar directory, and the loaners into a Loaners directory inside the ship's directory.'''
        global desiredShip
        global shipList
        global loaners
        import os
        import json
        import shutil
        global programDirectory
        global hangarList
        os.chdir(programDirectory)
        
        desiredShip = self.shipFull.getSelectedItem()
        os.chdir("Ship Store/")
        os.chdir(desiredShip)
        file = open("shipInfo.txt", 'r')
        infoJson = file.read()
        file.close()
        os.chdir(programDirectory)
        shipInfo = json.loads(infoJson)
        loaners = shipInfo["Loaners"]
        loaners = loaners.split(", ")
        
        hangarDirectory = programDirectory+"/Hangar"
        hangarList = os.listdir(hangarDirectory)
        
        loanerDirectory = programDirectory+"/Hangar/Loaners"
        loanerList = os.listdir(loanerDirectory)
        
        if desiredShip not in hangarList:
            #shutil copytree function based on comment by nzot
            #https://stackoverflow.com/questions/1994488/copy-file-or-directories-recursively-in-python
            shutil.copytree(programDirectory+"\\Ship Store\\"+desiredShip, programDirectory+"\\Hangar\\"+desiredShip)
        if 'N/A' not in loaners:
            for word in loaners:
                if word in shipList:
                    if word not in loanerList:
                        shutil.copytree(programDirectory+"\\Ship Store\\"+word, programDirectory+"\\Hangar\\Loaners\\"+word)
                else:
                    print("Potential file error, check loaners")
        self.messageBox(title=desiredShip, message = desiredShip+" added to hangar.")
                    
    def wishAdd(self):
        '''Copies the ship's Ship Store directory into the Wishlist directory, and the loaners into a Loaners directory inside the ship's directory.'''
        global desiredShip
        global shipList
        global loaners
        import os
        import json
        import shutil
        global programDirectory
        global wishList
        os.chdir(programDirectory)
        
        desiredShip = self.shipFull.getSelectedItem()
        os.chdir("Ship Store/")
        os.chdir(desiredShip)
        file = open("shipInfo.txt", 'r')
        infoJson = file.read()
        file.close()
        os.chdir(programDirectory)
        shipInfo = json.loads(infoJson)
        loaners = shipInfo["Loaners"]
        loaners = loaners.split(", ")
        
        wishDirectory = programDirectory+"/Wishlist"
        wishList = os.listdir(wishDirectory)
        
        loanerDirectory = programDirectory+"/Wishlist/Loaners"
        loanerList = os.listdir(loanerDirectory)
        
        if desiredShip not in wishList:
            #shutil copytree function based on comment by nzot
            #https://stackoverflow.com/questions/1994488/copy-file-or-directories-recursively-in-python
            shutil.copytree(programDirectory+"\\Ship Store\\"+desiredShip, programDirectory+"\\Wishlist\\"+desiredShip)
        if 'N/A' not in loaners:
            for word in loaners:
                if word in shipList:
                    if word not in loanerList:
                        shutil.copytree(programDirectory+"\\Ship Store\\"+word, programDirectory+"\\Wishlist\\Loaners\\"+word)
                else:
                    print("Potential file error, check loaners")
        self.messageBox(title=desiredShip, message = desiredShip+" added to wishlist.")
                
    def hangarRemove(self):
        '''Deletes the ship's Ship Store directory (and loaners) from the Hangar directory'''
        global desiredShip
        global shipList
        global loaners
        import os
        import json
        import shutil
        global programDirectory
        global hangarList
        os.chdir(programDirectory)
        
        desiredShip = self.shipFull.getSelectedItem()
        hangarList = os.listdir(programDirectory+"\\Hangar")
        
        desiredShip = self.shipFull.getSelectedItem()
        os.chdir("Ship Store/")
        os.chdir(desiredShip)
        file = open("shipInfo.txt", 'r')
        infoJson = file.read()
        file.close()
        os.chdir(programDirectory)
        shipInfo = json.loads(infoJson)
        loaners = shipInfo["Loaners"]
        loaners = loaners.split(", ")
        
        loanerDirectory = programDirectory+"/Wishlist/Loaners"
        loanerList = os.listdir(loanerDirectory)
        
        if desiredShip in hangarList:
            #shutil copytree function based on comment by nzot
            #https://stackoverflow.com/questions/1994488/copy-file-or-directories-recursively-in-python
            shutil.rmtree(programDirectory+"\\Hangar\\"+desiredShip)
        if 'N/A' not in loaners:
            for word in loaners:
                if word in shipList:
                    if word in loanerList:
                        shutil.rmtree(programDirectory+"\\Hangar\\Loaners\\"+word)
        hangarList = os.listdir(programDirectory+"\\Hangar")
        self.Hangar()
                    
    def wishRemove(self):
        '''Deletes the ship's Ship Store directory (and loaners) from the Wishlist directory'''
        global desiredShip
        global shipList
        global loaners
        import os
        import json
        import shutil
        global programDirectory
        global wishList
        os.chdir(programDirectory)
        
        desiredShip = self.shipFull.getSelectedItem()
        wishList = os.listdir(programDirectory+"\\Wishlist")
        
        desiredShip = self.shipFull.getSelectedItem()
        os.chdir("Ship Store/")
        os.chdir(desiredShip)
        file = open("shipInfo.txt", 'r')
        infoJson = file.read()
        file.close()
        os.chdir(programDirectory)
        shipInfo = json.loads(infoJson)
        loaners = shipInfo["Loaners"]
        loaners = loaners.split(", ")
        
        loanerDirectory = programDirectory+"/Wishlist/Loaners"
        loanerList = os.listdir(loanerDirectory)
        
        if desiredShip in wishList:
            #shutil copytree function based on comment by nzot
            #https://stackoverflow.com/questions/1994488/copy-file-or-directories-recursively-in-python
            shutil.rmtree(programDirectory+"\\Wishlist\\"+desiredShip)
        if 'N/A' not in loaners:
            for word in loaners:
                if word in shipList:
                    if word in loanerList:
                        shutil.rmtree(programDirectory+"\\Wishlist\\Loaners\\"+word)
        wishList = os.listdir(programDirectory+"\\Wishlist")
        self.Wishlist()
        
    def costTotalHangar(self):
        import os
        import json
        global programDirectory
        os.chdir(programDirectory)
        
        priceTotal = 0
        discountedTotal = 0
        
        hangarList = os.listdir(programDirectory+"\\Hangar")
        for item in hangarList:
            if item != "Loaners":
                os.chdir("Ship Store/")
                os.chdir(item)
                file = open("shipInfo.txt", 'r')
                infoJson = file.read()
                file.close()
                os.chdir(programDirectory)
                shipInfo = json.loads(infoJson)
                
                cost = shipInfo["Normal Price"]
                cost = cost.replace('$','')
                cost = cost.replace(',','')

                warbond = shipInfo["Warbond Price"]
                warbond = warbond.replace('$','')
                warbond = warbond.replace(',','')

                
                if cost != 'N/A':
                    cost = int(cost)
                    priceTotal = priceTotal + cost
                if warbond != 'N/A':
                    warbond = int(warbond)
                    discountedTotal = discountedTotal + warbond
        if priceTotal != '':
            self.fullPrice = self.addLabel(text = "Standard Price: $"+str(priceTotal)+".00", row = 5, column = 5, sticky = N+W)
        if discountedTotal != '':
            self.warbondPrice = self.addLabel(text = "Warbond Price: $"+str(discountedTotal)+".00", row = 5, column = 2, sticky = N+W)
        os.chdir(programDirectory)
        
    def costTotalWishlist(self):
        import os
        import json
        global programDirectory
        os.chdir(programDirectory)
        
        priceTotal = 0
        discountedTotal = 0
        
        wishList = os.listdir(programDirectory+"\\Wishlist")
        for item in wishList:
            if item != "Loaners":
                os.chdir("Ship Store/")
                os.chdir(item)
                file = open("shipInfo.txt", 'r')
                infoJson = file.read()
                file.close()
                os.chdir(programDirectory)
                shipInfo = json.loads(infoJson)
                
                cost = shipInfo["Normal Price"]
                cost = cost.replace('$','')
                cost = cost.replace(',','')

                warbond = shipInfo["Warbond Price"]
                warbond = warbond.replace('$','')
                warbond = warbond.replace(',','')

                
                if cost != 'N/A':
                    cost = int(cost)
                    priceTotal = priceTotal + cost
                if warbond != 'N/A':
                    warbond = int(warbond)
                    discountedTotal = discountedTotal + warbond
        if priceTotal != '':
            self.fullPrice = self.addLabel(text = "Standard Price: $"+str(priceTotal)+".00", row = 5, column = 5, sticky = N+W)
        if discountedTotal != '':
            self.warbondPrice = self.addLabel(text = "Warbond Price: $"+str(discountedTotal)+".00", row = 5, column = 2, sticky = N+W)
        os.chdir(programDirectory)
        
    def clearFrame(self):
        self.grid_forget()
    
    def shipAccess(self):
        global desiredShip
        desiredShip = self.shipFull.getSelectedItem()
        self.clearFrame()
        Detail().mainloop()
        Companion().mainloop()
    
    def hangarLoaners(self):
        global loaners
        import os
        import json
        global programDirectory
        os.chdir(programDirectory)
        
        os.chdir("Ship Store/")
        
        loanerDirectory = programDirectory+"/Hangar/Loaners"
        loanerList = os.listdir(loanerDirectory)
        
        self.button2.destroy()
        self.button2 = self.addButton(text = "Show Normal", row = 3, column = 6, command = self.Hangar)
        self.shipFull.clear()
        listSize = self.shipFull.size()
        for item in loanerList:
            if listSize <= 165:
                self.ship = self.shipFull.insert(END, item)
   
    def wishLoaners(self):
        global loaners
        import os
        import json
        global programDirectory
        os.chdir(programDirectory)
        
        os.chdir("Ship Store/")
        
        loanerDirectory = programDirectory+"/Wishlist/Loaners"
        loanerList = os.listdir(loanerDirectory)
        
        self.button2.destroy()
        self.button2 = self.addButton(text = "Show Normal", row = 3, column = 6, command = self.Wishlist)
        self.shipFull.clear()
        listSize = self.shipFull.size()
        for item in loanerList:
            if listSize <= 165:
                self.ship = self.shipFull.insert(END, item) 
   
#################### Above: Main Window #################################
#################### Below: Details Window ##############################

class Detail(EasyFrame):
    '''Offers the backbone of the program GUI'''
    global shipList
    global hangarList
    global wishList
    global desiredShip
    def __init__(self):
        '''Sets up the window and the label.'''
        self.detailsWindow = EasyFrame.__init__(self, title=desiredShip, width = 1200, height = 700, background="cornsilk4")
        self.shipDetails()

    def shipDetails(self):
        '''Finds the ship's info and displays it along with the ship's image. Also defines the loaners for the desired ship.'''
        global loaners
        import os
        import json
        global programDirectory
        os.chdir(programDirectory)
        
        os.chdir("Ship Store/")
        os.chdir(desiredShip)
        file = open("shipInfo.txt", 'r')
        infoJson = file.read()
        file.close()
        os.chdir(programDirectory)
        shipInfo = json.loads(infoJson)
        row = 0
        column = -1
        for element in shipInfo:
            column += 1
            relevantInfo = element + ": " + shipInfo[element]
            self.textLabel = self.addLabel(text = relevantInfo, row = row, column = column, sticky = "NEWS")
            if column == 2:
                row += 1
                column = -1
        
        os.chdir("Ship Store/"+desiredShip)

        panel = self.addPanel(row = 3, column = 0, columnspan = 3)
        canvas = panel.addCanvas(row = 3, column = 0, width = 500, height = 500)
        self.img = Image.open(desiredShip+".jpg")
        self.img = self.img.resize((1200,675), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img)
        canvas.drawImage(x = 0, y = 0, anchor="nw", image=self.img)
        
        os.chdir(programDirectory)
        
#################### Above: Details Window ##############################
#################### Below: Program Functions ###########################

def oneBlankLines():
    print("")

def twoBlankLines():
    print("")
    print("")

def endOfProgram():
    import os
    global programDirectory
    print("End of program.")
    os.chdir(programDirectory)
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
    global programDirectory
    programDirectory = os.getcwd()
    storeDirectory = programDirectory+"/Ship Store"
    hangarDirectory = programDirectory+"/Hangar"
    wishDirectory = programDirectory+"/Wishlist"
    currentDirectories = os.listdir(programDirectory)
    if "Ship Store" not in currentDirectories:
        print("You are missing the Ship files.")
    else:
        hangarExist = False
        while hangarExist == False:
            if "Hangar" not in currentDirectories:
                os.mkdir("Hangar")
                hangarExist = True
                hangarList = os.listdir(hangarDirectory)
                hangarList.sort()
            else:
                hangarExist = True
                hangarList = os.listdir(hangarDirectory)
                hangarList.sort()
                
        loanersExist = False
        os.chdir("Hangar")
        loanerCheck = os.listdir(hangarDirectory)
        while loanersExist == False:
            if "Loaners" not in loanerCheck:
                os.mkdir("Loaners")
                loanersExist = True
                loanersList = os.listdir(hangarDirectory)
                loanersList.sort()
            else:
                loanersExist = True
                loanersList = os.listdir(hangarDirectory)
                loanersList.sort()
        os.chdir(programDirectory)
        
        wishlistExist = False
        while wishlistExist == False:
            if "Wishlist" not in currentDirectories:
                os.mkdir("Wishlist")
                wishlistExist = True
                wishList = os.listdir(wishDirectory)
                wishList.sort()
            else:
                wishlistExist = True
                wishList = os.listdir(wishDirectory)
                wishList.sort()
                
        loanersExist = False
        os.chdir("Wishlist")
        loanerCheck = os.listdir(wishDirectory)
        while loanersExist == False:
            if "Loaners" not in loanerCheck:
                os.mkdir("Loaners")
                loanersExist = True
                loanersList = os.listdir(wishDirectory)
                loanersList.sort()
            else:
                loanersExist = True
                loanersList = os.listdir(wishDirectory)
                loanersList.sort()
        os.chdir(programDirectory)
        
    os.chdir(programDirectory)
    shipStore()
                
def shipStore():
    '''Lists all available ship options'''
    global shipList
    import os
    global programDirectory
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
    global programDirectory
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

#################### Above: Program Functions ######################
#################### Below: Main Program ###########################

def main():
    welcomeMsg()
    houseKeeping()
    Companion().mainloop()
    endOfProgram()
    
    
# main program =========================================================
if __name__ == "__main__":
    main()


    
