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
 
try:
    while True:
        try:
            value = int(input ("Введите число (-1 для выхода): "))
            if value < -1 or value > 255:
                print ("Число должно быть от 0 до 255 (или -1 для выхода). Попробуйте еще раз.")
                continue
        except ValueError:
            print ("Необходимо ввести число! Попробуйте еще раз:")
        else:
            if value == -1:
                break
            num2dac(value)
except:
    print ("Неизвестная ошибка, выходим из программы.")
finally:
    GPIO.output (chan_list, 0)
    GPIO.cleanup (chan_list)