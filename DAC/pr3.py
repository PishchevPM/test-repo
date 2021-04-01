try:
    import RPi.GPIO as GPIO
    import time
    import numpy as np
    import matplotlib.pyplot as plt
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
    return [(int(decNumber) & (1 << i)) >> i for i in range (7, -1, -1)]
 
def num2dac (value):
    x = decToBinList (value)
    GPIO.output (chan_list, tuple (x))
 
worktime = 0
frequency = 0
samplingFrequency = 0
 
while True:
    try:
        worktime = float(input ("Введите время работы: "))
        if worktime >= 0:
            break
        else:
            print ("Число должно быть неотрицательным. Попробуйте еще раз:")
            continue
    except ValueError:
        print ("Необходимо ввести число! Попробуйте еще раз:")
    except:
        print ("Неизвестная ошибка, выходим из программы.")
        GPIO.output (chan_list, 0)
        GPIO.cleanup (chan_list)
        raise SystemExit
 
while True:
    try:
        frequency = float(input ("Введите частоту синусоидального сигнала: "))
        if frequency > 0:
            break
        else:
            print ("Число должно быть положительным. Попробуйте еще раз:")
            continue
    except ValueError:
        print ("Необходимо ввести число! Попробуйте еще раз:")
    except:
        print ("Неизвестная ошибка, выходим из программы.")
        GPIO.output (chan_list, 0)
        GPIO.cleanup (chan_list)
        raise SystemExit
 
while True:
    try:
        samplingFrequency = float(input ("Введите частоту сэмплироания: "))
        if samplingFrequency > 0:
            break
        else:
            print ("Число должно быть положительным. Попробуйте еще раз:")
            continue
    except ValueError:
        print ("Необходимо ввести число! Попробуйте еще раз:")
    except:
        print ("Неизвестная ошибка, выходим из программы.")
        GPIO.output (chan_list, 0)
        GPIO.cleanup (chan_list)
        raise SystemExit
 
try:
    freqarr = np.arange(0, worktime, 1/samplingFrequency)
    ndarray = np.int32(np.round(127.5 - 127.5*np.cos(2 * np.pi * frequency * freqarr)))
    plt.plot(freqarr, ndarray)
    plt.title('Подаваемый сигнал')
    plt.xlabel('Время')
    plt.ylabel('Амплитуда сигнала')
    plt.show()
except:
    print ("Ошибка в построении графика. Выходим из программы.")
    GPIO.output (chan_list, 0)
    GPIO.cleanup (chan_list)
    raise SystemExit

q = input ("Хотите продолжить? [y/n]: ")
if q != "y":
    GPIO.output (chan_list, 0)
    GPIO.cleanup (chan_list)
    raise SystemExit

try:
    for j in ndarray:
        num2dac (j)
        time.sleep (1/samplingFrequency)
except:
    print("Неизвестная ошибка, выходим из программы.")
finally:
    GPIO.output (chan_list, 0)
    GPIO.cleanup (chan_list)
