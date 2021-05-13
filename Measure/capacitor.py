try:
    import RPi.GPIO as GPIO
    import time
    import numpy as np
    import matplotlib.pyplot as plt
    import math
except ImportError:
    print ("Import error!")
    raise SystemExit

try:
    dac_list = (26, 19, 13, 6, 5, 11, 9, 10)
    led_list = (24, 25, 8, 7, 12, 16, 20, 21)
    cmp_chan = 4
    V_chan = 17
    GPIO.setmode (GPIO.BCM)
    GPIO.setup (dac_list, GPIO.OUT)
    GPIO.setup (led_list, GPIO.OUT)
    GPIO.setup (V_chan, GPIO.OUT)
    GPIO.setup (cmp_chan, GPIO.IN)
except:
    print ("GPIO Initialization error!")
    raise SystemExit

maxV = 3.3

def decToBinList (decNumber):
    if decNumber < 0 or decNumber > 255:
        raise ValueError
    return [(decNumber & (1 << i)) >> i for i in range (7, -1, -1)]
 
def num2pins (pins, value):
    x = decToBinList (value)
    GPIO.output (pins, tuple (x))

def adc():
    dg = 0
    i = 128
    while i >= 1:
        num2pins(dac_list, i)
        time.sleep (0.0001)
        if GPIO.input (cmp_chan) == 1:
            dg += i
        i = int(i / 2)
    return dg

measure = []
timelist = []
try:
    GPIO.output (V_chan, 1)
    dg = 0
    tm0 = time.time()
    while dg <= 254:
        dg = adc ()
        timelist.append (time.time () - tm0)
        measure.append (dg)
    while dg >= 1:
        dg = adc ()
        timelist.append (time.time () - tm0)
        measure.append (dg)

    np.savetxt('setting.txt', [(time.time () - tm0) / len (timelist), maxV / 255], fmt='%d')
    np.savetxt('data.txt', measure, fmt='%d')
    plt.plot(timelist, measure)
    plt.title('Зависимость напряжение на обкладках конденсатора от времени')
    plt.xlabel('Время, с')
    plt.ylabel('Напряжение, В')

except:
    print ("lol")
finally:
    GPIO.output (dac_list, 0)
    GPIO.output (V_chan, 0)
    GPIO.cleanup (dac_list)
    GPIO.cleanup (led_list)
    GPIO.cleanup (V_chan)
    GPIO.cleanup (cmp_chan)