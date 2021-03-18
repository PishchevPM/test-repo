import RPi.GPIO as GPIO
import time

chan_list = (24, 25, 8, 7, 12, 16, 20, 21)
GPIO.setmode (GPIO.BCM)
GPIO.setup (chan_list, GPIO.OUT)
pwm = GPIO.PWM (24, 50)

def lightUp (ledNumber, period):
    GPIO.output (chan_list[ledNumber], 1)
    time.sleep (period)
    GPIO.output (chan_list[ledNumber], 0)

def blink (ledNumber, blinkCount, blinkPeriod):
    for i in range (blinkCount):
        lightUp (ledNumber, blinkPeriod)
        time.sleep (blinkPeriod)

def runningPattern (pattern, direction):
    if direction == -1:
        return ((pattern << 1) + (pattern >> 7)) % 256
    if direction == 1:
        return ((pattern >> 1) + 128 * (pattern % 2))

def decToBinList (decNumber):
    return [(decNumber & (1 << i)) >> i for i in range (7, -1, -1)]

def lightNumber (number):
    x = decToBinList (number)
    x.reverse()
    GPIO.output (chan_list, tuple (x))

def runningLightDark (count, period, stype):
    x = (1 - stype) * 253 + 1
    for i in range (8 * count):
        lightNumber (x)
        x = runningPattern (x, -1)
        time.sleep (period)

def pwmlight (period):
    pwm.start (0)
    for i in range (0, 101, 5):
        pwm.ChangeDutyCycle (i)
        time.sleep (period)
    for i in range (100, -1, -5):
        pwm.ChangeDutyCycle (i)
        time.sleep (period)
    pwm.stop ()

lightUp (5, 2)
time.sleep (2)

blink (1, 3, 1)
time.sleep (1)

lightNumber (87)
time.sleep (2)
lightNumber (0)

runningLightDark (1, 1, 0)
runningLightDark (1, 1, 1)
lightNumber (0)

pwmlight (0.1)

GPIO.cleanup (chan_list)
