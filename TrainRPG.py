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

Pots = int(input("How many Life Potions do u have: "))

DoHunt = True
DoAdventure = False
DoGatherMaterial = True

def Pressed(key):
    pass

def Released(key):
    global Press
    if key == Key.esc:
        Press = 0

def DupeRemove(x):
    return list(dict.fromkeys(x))

def Hunt():
    print("Hunting...")
    kb.type("rpg hunt")
    kb.press(Key.enter)
    kb.release(Key.enter)

def BuyPots():
    time.sleep(1.2)
    print("Buying Life Potions...")
    kb.type("rpg buy Life Potion 10")
    kb.press(Key.enter)
    kb.release(Key.enter)

def UsePotion():
    print("Healing...")
    kb.type("rpg heal")
    kb.press(Key.enter)
    kb.release(Key.enter)

def Scan():
    global ExtractText
    global SplitLineExtract
    global DoHunt
    global DoAdventure
    global Heal

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
            try:
                if Word[-1:] == ",":
                    Word = Word[:-1]

                Health = eval(Word)

                if Health < 1:
                    RealHealth = Health
            except:
                pass
    
    try:
        print("Health Ratio Remaining: ",RealHealth)
        if RealHealth <= 0.43:
            Heal = True
        
    except NameError:
        print("Health Ratio Remaining: Null")
        Heal = True
        
    if DoHunt == False:
        DoHunt = True

    if DoAdventure == False:
        DoAdventure = True

def Adventure():
    print("Going on an Adventure...")
    kb.type("rpg adv")
    kb.press(Key.enter)
    kb.release(Key.enter)

def GatherMaterial():
    global DoGatherMaterial

    MaterialToGather = ["rpg fish","rpg chop"]

    print("Gathering Materials...")
    kb.type(random.choice(MaterialToGather))
    kb.press(Key.enter)
    kb.release(Key.enter)
    DoGatherMaterial = True

def QueueInfo():
    print("------------------------")
    print("Queue: ", end = "")
    print(QNext)
    print("------------------------")

kb = Controller()

Action = "0"
QNext = []
Press = 1
Pause = False
Heal = False

HuntTime = time.time()
AdventureTime = time.time()
GatherMaterialTime = time.time()

time.sleep(5)

listener = Listener(on_press = Pressed, on_release = Released)
listener.start()

QueueInfo()

while True:
    time.sleep(0.05)
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
            if Action == "Hunt":
                Hunt()
                Action = "0"
                QueueInfo()

            elif Action == "Adventure":
                Adventure()
                Action = "0"
                

            elif Action == "GatherMaterial":
                GatherMaterial()
                Action = "0"
                QueueInfo()

            elif Action == "Scan":
                Scan()
                Action = "0"
                QueueInfo()

            elif Action == "Heal":
                UsePotion()
                print("Life Potions Remaining: ",Pots)
                Action = "0"
                QueueInfo()

            elif Action == "BuyPots":
                BuyPots()
                print("Life Potions Remaining: ",Pots)
                Action = "0"
                QueueInfo()

        if Heal:
            Pots -= 1
            QNext.append("Heal")
            Heal = False
            QueueInfo()

        if Pots == 0:
            Pots = 10
            QNext.append("BuyPots")
            QueueInfo()
        
        elif DoHunt and ((time.time() - HuntTime) >= 69) and Action == "0":
            QNext.append("Hunt")
            DoHunt = False
            QNext.append("Scan")
            HuntTime = time.time()
            QueueInfo()

        elif DoAdventure and ((time.time() - AdventureTime) >= 3612) and Action == "0":
            QNext.append("Adventure")
            DoAdventure = False
            QNext.append("Scan")
            AdventureTime = time.time()
            QueueInfo()

        elif DoGatherMaterial and ((time.time() - GatherMaterialTime) >= 310) and Action == "0":
            QNext.append("GatherMaterial")
            DoGatherMaterial = False
            GatherMaterialTime = time.time()
            QueueInfo()