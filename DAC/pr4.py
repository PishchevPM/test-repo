try:
    import RPi.GPIO as GPIO
    import time
    import numpy as np
    import matplotlib.pyplot as plt
    from os.path import dirname, join as pjoin
    from scipy.io import wavfile
    import scipy.io
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

wav_fname = pjoin('SOUND.WAV')
samplerate, data = wavfile.read(wav_fname)
length = data.shape[0] / samplerate

print ("length: ", int(length), "s, number of channels: ", data.shape[1], ", Sample Rate: ", samplerate, ", data type: ", type (data[1, 0]))

try:
    for i in data[:, 0]:
        num2dac ((int(i) + 32768) / 256)
except ValueError:
    print ("Ошибка в в размере входных данных. Выходим из программы")
except:
    print ("Неизвестная ошибка. Выходим из программы")
finally:
    GPIO.output (chan_list, 0)
    GPIO.cleanup (chan_list)