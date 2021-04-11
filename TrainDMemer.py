from pynput.keyboard import Key, Controller
from pynput.keyboard import Listener
import random
import time
import numpy
from PIL import Image, ImageGrab
import PIL.ImageOps
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

DoSpam = False
DoMemes = False
DoSearch = True
DoBeg = True

Meme = ["n", "e", "r", "d"]

def Pressed(key):
    pass

def Released(key):
    global Press
    if key == Key.esc:
        Press = 0

def DupeRemove(x):
    return list(dict.fromkeys(x))

def PostAMeme():
    print("Positng A Meme...")
    kb.type("pls postmeme")
    kb.press(Key.enter)
    kb.release(Key.enter)
    time.sleep(2)
    kb.type(random.choice(Meme))
    kb.press(Key.enter)
    kb.release(Key.enter)

def Search():
    print("Searching...")
    kb.type("pls search")
    kb.press(Key.enter)
    kb.release(Key.enter)

def Scan():
    global ExtractText
    global SplitLineExtract
    global Pos
    global ChoiceList
    global DoSearch

    OtherChoices = ["air","street","tree","coat","dresser","bed","bushes","mailbox","grass","uber","sink","laundromat","couch","pumpkin","glovebox","shoe","pantry","bus"]
    BadChoices = ["car","area51","dog","hospital","purse","bank","dumpster","sewer","discord"]
    RlyBadChoices = ["area51","purse","car","purse"]

    print("Scanning...")
    time.sleep(3) 
    ss = ImageGrab.grab((300,50,700,460))
    ss.save('screenshot.png')
    ImgOri = Image.open('screenshot.png')

    if ImgOri.mode == 'RGBA':
        r,g,b,a = ImgOri.split()
        RGBImage = Image.merge('RGB', (r,g,b))
        Invert = PIL.ImageOps.invert(RGBImage)
        r2,g2,b2 = Invert.split()
        InvertSaveRGBA = Image.merge('RGBA', (r2,g2,b2,a))
        InvertSaveRGBA.save('screenshot.png')

    else:
        Invert = PIL.ImageOps.invert(ImgOri)
        Invert.save('screenshot.png')

    ImgInv = Image.open('screenshot.png')

    ExtractText = pytesseract.image_to_string(ImgInv)
    SplitLineExtract = ExtractText.splitlines()

    SplitLineExtractFix = DupeRemove(SplitLineExtract)

    for Sen in SplitLineExtractFix:
        TempChar =  Sen.split(" ")
        for Word in TempChar:
            if Word == "chat.":
                Pos = SplitLineExtractFix.index(Sen)

    try:        
        ChoiceList = SplitLineExtractFix[Pos + 1].split(", ")

        print("Choice Range: " + str(len(ChoiceList)))

        if len(ChoiceList) < 3:
            for Additions in SplitLineExtractFix[Pos + 2].split(", "):
                ChoiceList.append(Additions)
            print("Choice Range Final: " + str(len(ChoiceList)))

        for Item in ChoiceList:
            if Item[-1:] == ",":
                Temp = ChoiceList.index(Item)
                ChoiceList[Temp] = Item[:-1]

        for Check in ChoiceList:
            if Check == "areas1":
                Temp = ChoiceList.index(Check)
                ChoiceList[Temp] = "area51"

        print("Choice List: ", end = "")
        print(ChoiceList)

        BadList = all(Bad in BadChoices for Bad in ChoiceList)

        RlyBadList = all(RlyBad in RlyBadChoices for RlyBad in ChoiceList)

        print("BadList: ", end = "")
        print(BadList)

        print("RlyBadList: ", end = "")
        print(RlyBadList)

        Choice = (random.choice(ChoiceList))        

        print("Choice: " + Choice)

        while BadList == False:
            if (Choice[:-1] in BadChoices) or (Choice in BadChoices):
                Choice = (random.choice(ChoiceList))

                print("Choice: " + Choice)
                
            else:
                print("Choice Final: " + Choice)
                break

        while BadList and RlyBadList == False:
            if (Choice[:-1] in RlyBadChoices) or (Choice in RlyBadChoices):
                Choice = (random.choice(ChoiceList))

                print("Choice: " + Choice)
                
            else:
                print("Choice Final: " + Choice)
                break
    
    except NameError:
        Choice = (random.choice(OtherChoices))
        print("Choice: " + Choice)
        print("Choice Final: " + Choice)

    kb.type(Choice)
    kb.press(Key.enter)
    kb.release(Key.enter)

    DoSearch = True

def Beg():
    global DoBeg

    print("Begging...")
    kb.type("pls beg")
    kb.press(Key.enter)
    kb.release(Key.enter)
    DoBeg = True

def Deposit():
    print("Depositing...")
    time.sleep(6)
    kb.type("pls dep all")
    kb.press(Key.enter)
    kb.release(Key.enter) 

kb = Controller()

infoTime = time.time()
postTime = time.time()
searchTime = time.time()
begTime = time.time()

Action = "0"
QNext = []

Press = 1
Pause = False

time.sleep(5)

listener = Listener(on_press = Pressed, on_release = Released)
listener.start()

while True:
    if Press == 0:
        Pause = not Pause
        print("------------------------")
        print("------------------------")
        if Pause:
            print("Paused")
        else:
            print("Resumed")
        print("------------------------")
        print("------------------------")
        Press = 2

    if Pause:
        pass

    else:
        if QNext and Action == "0":
            Action = QNext.pop(0)

        elif Action != "0":
            if Action == "Spam":
                Spam()
                Action = "0"

            if Action == "Meme":
                PostAMeme()
                Action = "0"

            if Action == "Search":
                time.sleep(1.5)
                Search()
                Action = "0"
            
            if Action == "Beg":
                time.sleep(1.5)
                Beg()
                Action = "0"

            if Action == "Scan":
                time.sleep(3)
                Scan()
                Action = "0"

            if Action == "Deposit":
                time.sleep(5)
                Deposit()
                Action = "0"

        if(time.time() - infoTime) >= 3:
            print("------------------------")
            print("Queue: ", end = "")
            print(QNext)
            print("------------------------")
            infoTime = time.time()

        elif DoMemes and ((time.time() - postTime) >= 63) and Action == "0":
            QNext.append("Meme")
        
        elif DoSearch and ((time.time() - searchTime) >= 33) and Action == "0":
            QNext.append("Search")
            DoSearch = False
            QNext.append("Scan")
            QNext.append("Deposit")
            searchTime = time.time()
            print(QNext)

        elif DoBeg and ((time.time() - begTime) >= 48) and Action == "0":
            QNext.append("Beg")
            DoBeg = False
            QNext.append("Deposit")
            begTime = time.time()
            print(QNext)