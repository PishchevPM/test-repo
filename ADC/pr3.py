
try:
    import RPi.GPIO as GPIO
    import time
    import matplotlib.pyplot as plt
except ImportError:
    print ("Import error!")
    raise SystemExit
 
outstr = "Digital value: {digital}, analog value: {analog} V"
maxV = 3.3
try:
    out_list = (26, 19, 13, 6, 5, 11, 9, 10)
    in_chan = 4
    V_chan = 17
    GPIO.setmode (GPIO.BCM)
    GPIO.setup (chan_list, GPIO.OUT)
    GPIO.setup (V_chan, GPIO.OUT)
    GPIO.setup (in_chan, GPIO.IN)
except:
    print ("GPIO Initialization error!")
    raise SystemExit
 
 
def decToBinList (decNumber):
    if decNumber < 0 or decNumber > 255:
        raise ValueError
    return [(decNumber & (1 << i)) >> i for i in range (7, -1, -1)]
 
def num2dac (value):
    x = decToBinList (value)
    GPIO.output (out_list, tuple (x))
 
def healthy_search ():
    dg = 0
    i = 128
    while i != 0:
        an = maxV * (dg + i) / 255
        num2dac(dg)
        if GPIO.input (in_chan) == 1:
            dg += i
        i /= 2
    return dg

T_list = []
V_list = []
try:
    GPIO.output (V_chan, 1)
    while True:
        curtime = time.time()
        V_list.append(healthy_search())
        T_list.append(time.time() - curtime)
        time.sleep (0.1)
except:
    print ("Неизвестная ошибка, выходим из программы.")
finally:
    plt.plot(T_list, V_list, 'r-')
    plt.show()
    GPIO.output (chan_list, 0)
    GPIO.output (V_chan, 0)
    GPIO.cleanup (chan_list)