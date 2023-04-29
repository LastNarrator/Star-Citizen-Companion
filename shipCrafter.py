# -*- coding: utf-8 -*-
"""
Program Title: shipCrafter.py
Program Author: Dillon Brandon
Creation Date: 04/12/2023 - 05/12/2023
Purpose:
A small program to create ship json files.

Variables:
No global variables.
"""
import json
import os

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
    oneBlankLines()

def echoPrint(pValue):
    print("The data entered is:",pValue)

def inputInfo():
    programDirectory = os.getcwd()
    os.chdir(programDirectory+"/Ship Store")
    storeDirectory = os.getcwd()
    shipList = os.listdir(storeDirectory)
    shipExists = False
    ship = {}
    while shipExists == False:
        shipName = input("Input ship name: ")
        echoPrint(shipName)
        if shipName in shipList:
            oneBlankLines()
            print("This ship already exists. (yes,no) ")
            editChoice = input("Do you wish to edit the ship? ")
            if editChoice == "yes":
                oneBlankLines()
                os.chdir(shipName)
                ship["Name"] = shipName
                    
                shipManu = input("Input ship manufacturer: ")
                echoPrint(shipManu)
                ship["Manufacturer"] = shipManu
                oneBlankLines()
                
                shipStatus = input("Input ship status: ")
                echoPrint(shipStatus)
                ship["Status"] = shipStatus
                oneBlankLines()
                    
                shipPrice = input("Input ship price: ")
                echoPrint(shipPrice)
                ship["Normal Price"] = shipPrice
                oneBlankLines()

                shipWarbond = input("Input ship Warbond price: ")
                echoPrint(shipWarbond)
                ship["Warbond Price"] = shipWarbond
                oneBlankLines()
                
                shipLoaners = input("Input ship loaners: ")
                echoPrint(shipLoaners)
                ship["Loaners"] = shipLoaners
                oneBlankLines()
                
                shipInfo = json.dumps(ship, indent=0)
                print(shipInfo)
                file = open("shipInfo.txt", 'w')
                file.write(shipInfo)
                file.close
                shipList = os.listdir(storeDirectory)
                if shipName in shipList:
                    shipExists = True
                else:
                    print("Something went wrong?")
            else:
                print("Have a good day.")
        else:
                oneBlankLines()
                os.mkdir(shipName)
                os.chdir(shipName)
                ship["Name"] = shipName
                
                shipManu = input("Input ship manufacturer: ")
                echoPrint(shipManu)
                ship["Manufacturer"] = shipManu
                oneBlankLines()
                
                shipStatus = input("Input ship status: ")
                echoPrint(shipStatus)
                ship["Status"] = shipStatus
                oneBlankLines()
                    
                shipPrice = input("Input ship price: ")
                echoPrint(shipPrice)
                ship["Normal Price"] = shipPrice
                oneBlankLines()

                shipWarbond = input("Input ship Warbond price: ")
                echoPrint(shipWarbond)
                ship["Warbond Price"] = shipWarbond
                oneBlankLines()
                
                shipLoaners = input("Input ship loaners: ")
                echoPrint(shipLoaners)
                ship["Loaners"] = shipLoaners
                oneBlankLines()
                
                shipInfo = json.dumps(ship, indent=0)
                print(shipInfo)
                file = open("shipInfo.txt", 'w')
                file.write(shipInfo)
                file.close
                shipList = os.listdir(storeDirectory)
                if shipName in shipList:
                    shipExists = True
                else:
                    print("Something went wrong?")
    
def main():
    welcomeMsg()
    inputInfo()
    twoBlankLines()
    endOfProgram()
    
    
# main program =========================================================
if __name__ == "__main__":
    main()