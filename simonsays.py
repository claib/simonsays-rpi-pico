
###
# MicroPython for a Simon Says Raspberry Pi Pico game
# Date: November, 2021
# Author: rene.von@gmail.com
###

from machine import Pin, PWM
from utime import sleep
import array
import urandom

# Sound
FAIL = 50
WIN = 1000
GREEN = 300
BLUE = 400
RED = 500

# Game sequence long
SEQ_LONG = 5

# LEDs config
led_green = PWM(Pin(15, machine.Pin.OUT))
led_blue = PWM(Pin(14, machine.Pin.OUT))
led_red = PWM(Pin(13, machine.Pin.OUT))

# Test LEDs
# led_green.toggle()
# led_blue.toggle()
# led_red.toggle()

# Push Button config
pb_red = Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
pb_blue = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_DOWN)
pb_green = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Test Push Buttons
# print(pb_green.value())
# print(pb_blue.value())
# print(pb_red.value())

# Buzzer config
buzzer = PWM(Pin(11, machine.Pin.OUT))

# Test Buzzer
# buzzer.freq(50)
# buzzer.duty_u16(1000)
# sleep(1)
buzzer.duty_u16(0)

# Beep depending on color
def beepColor(color):
    sleep(.25)
    buzzer.freq(color)
    ledOn(color)
    buzzer.duty_u16(1000)
    sleep(.25)
    ledOff(color)
    buzzer.duty_u16(0)

# Turn LED on
def ledOn(color):
    if color == GREEN:
        led_green.duty_u16(65025)
        #led_green.value(1)
    elif color == BLUE:
        led_blue.duty_u16(65025)
        #led_blue.value(1)
    elif color == RED:
        led_red.duty_u16(65025)
        #led_red.value(1)

# Turn LED off
def ledOff(color):
    if color == GREEN:
        #led_green.value(0)
        led_green.duty_u16(0)
    elif color == BLUE:
        #led_blue.value(0)
        led_blue.duty_u16(0)
    elif color == RED:
        #led_red.value(0)
        led_red.duty_u16(0)

# Beep frequency
def beep(frequency):
    buzzer.freq(frequency)
    buzzer.duty_u16(1000)
    sleep(1)
    buzzer.duty_u16(0)

# Win beep
def beepWin():
    buzzer.freq(700)
    buzzer.duty_u16(1000)
    sleep(.25)
    #buzzer.duty_u16(0)
    buzzer.freq(1000)
    buzzer.duty_u16(1000)
    sleep(.5)
    buzzer.duty_u16(0)

# Play Simon Says sequence
def playSequence(seq):
    for x in seq:
        beepColor(x)

# Return pressed push button
def buttonPressed():
    while True:
        if pb_green.value() == 1:
            return GREEN
        elif pb_blue.value() == 1:
            return BLUE
        elif pb_red.value() == 1:
            return RED   

# Possible LEDs colors (and sounds)
elements = [GREEN, BLUE, RED]

# Crete and initialize an array
sequence = [0]*SEQ_LONG

# Generate a random Simon Says sequence
for x in range(SEQ_LONG):
    sequence[x] = elements[urandom.randint(0, 2)]

# Main
x=0
while x<len(sequence):
    seq = sequence[:(x+1)]
    sleep(1)
    playSequence(seq)
    y=0
    while y<=x:
        button_pressed = buttonPressed()
        if button_pressed == sequence[y]:
            y=y+1
            beepColor(button_pressed)
        else:
            beep(FAIL)
            x=99
            break
    x=x+1

if x >= 99:
    print ("Game Over")
else:
    print ("You win!")
    sleep(.5)
    beepWin()
    beepWin()

