try:
    import RPi.GPIO as GPIO
    import time
except ImportError:
    print ("Import error!")
    raise SystemExit
 
try:
    chan_list = (26, 19, 13, 6, 5, 11, 9, 10)
    GPIO.setmode (GPIO.BCM)
    GPIO.setup (chan_list, GPIO.OUT)
except:
    print ("GPIO Initialization error!")
    raise SystemExit
 
 
def decToBinList (decNumber):
    if decNumber < 0 or decNumber > 255:
        raise ValueError
    return [(decNumber & (1 << i)) >> i for i in range (7, -1, -1)]
 
def num2dac (value):
    x = decToBinList (value)
    GPIO.output (chan_list, tuple (x))
 
repetitionsNumber = 0
while True:
    try:
        repetitionsNumber = int(input ("Введите количество повторений: "))
        if repetitionsNumber >= 0:
            break
        else:
            print ("Число должно быть неотрицательным. Попробуйте еще раз:")
            continue
    except ValueError:
        print ("Необходимо ввести число! Попробуйте еще раз:")
    except:
        print ("Неизвестная ошибка, выходим из программы.")
        GPIO.cleanup (chan_list)
        raise SystemExit
 
try:
    for i in range(repetitionsNumber):
        for x in range(0, 256, 1):
            num2dac(x)
            time.sleep (0.01)
        for x in range(254, -1, -1):
            num2dac(x)
            time.sleep(0.01)
except:
    print ("Неизвестная ошибка, выходим из программы")
finally:
    GPIO.output (chan_list, 0)
    GPIO.cleanup (chan_list)