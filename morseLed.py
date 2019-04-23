# coding=utf-8
import sys
import time
import re
from tkinter import *
import tkinter.font
from gpiozero import LED
import RPi.GPIO
RPi.GPIO.setmode(RPi.GPIO.BCM)
## hardware
yellow = LED(18)
blue = LED(23)
red = LED(24)

# Dictionary representing the morse code chart 
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-', '!':'−.−.−−'} 
delay = 0.5
# Function to encrypt the string 
# according to the morse code chart 
def encrypt(message): 
    cipher = '' 
    for letter in message: 
        if letter != ' ': 
  
            # Looks up the dictionary and adds the 
            # correspponding morse code 
            # along with a space to separate 
            # morse codes for different characters 
            cipher += MORSE_CODE_DICT[letter] + ' '
        else: 
            # 1 space indicates different characters 
            # and 2 indicates different words 
            cipher += ' '
  
    return cipher 

def transmitCodeLed(codeMessage, useLed):
    for code in codeMessage:
        if code == '.':
            blue.on()
            print(".", end='')
            time.sleep(delay)
            blue.off()

            time.sleep(delay)
        elif code == '-':   
            blue.on()
            print("-", end='')
            time.sleep(delay*2)
            blue.off()
                
            time.sleep(delay)
        elif code == ' ':
            print(" ", end='')
            time.sleep(delay)

def transmitText(textArea):
    message = textArea.get()
    result = encrypt(message.upper()) 
    print(message)
    print(result)
    transmitCodeLed(result, True)

def close():
        RPi.GPIO.cleanup()
        win.destroy()

def limitSize(*args):
    value = textArea.get()
    if len(value) > charLimit: textAreaText.set(value[:charLimit])

        
if __name__ == "__main__":
    charLimit = 12
    ##GUI Definitions##
    win = Tk()
    win.title("Convert to Morse - Max 12 Char")
    myFont = tkinter.font.Font(family = 'Helvetica' , size = 12, weight = "bold")
    textAreaText = tkinter.StringVar()
    textAreaText.trace('w', limitSize)
    textArea = Entry(win, width = 44, textvariable = textAreaText)
    textArea.grid(row=0, column=1)
    buttonText = tkinter.StringVar()
    buttonText.set('Submit')
    button = Button(win, font = myFont, textvariable=buttonText, command = lambda: transmitText(textArea), bg = 'bisque2', height = 1, width = 44)
    button.grid(row=1, column=1)

    ## EXIT BUTTON ##

    exitButton = Button(win,text = 'Exit', font = myFont, command = close, bg = 'red', height = 1, width = 6)
    exitButton.grid(row=3, column=1)

    win.protocol("WM_DELETE_WINDOW", close) #exit cleanly

    win.mainloop() #loop forever
