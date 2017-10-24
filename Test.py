import serial
import numpy as np
from time import sleep

ser=serial.Serial('COM4',9600,timeout=0.2)

N=550
x = np.linspace(0, 500, N)
y = 250*np.sin(x)
for i in range(len(x)):
    t=int(round(x[i]))
    new_str = ''.join(['a',str('{:03d}'.format(500)),'b',str('{:03d}'.format(256)),'/r','\n'])
    print(ser.write(new_str .encode('ascii','replace')))
    print(ser.readline())
    sleep(0.001)
for i in range(len(x)):
    t=int(round(x[i]))
    new_str = ''.join(['a',str('{:03d}'.format(256)),'b',str('{:03d}'.format(0)),'/r','\n'])
    print(ser.write(new_str .encode('ascii','replace')))
    print(ser.readline())
    sleep(0.001)
print ("Process finished...exiting1")
new_str = ''.join(['a',str('{:03d}'.format(256)),'b',str('{:03d}'.format(256)),'r','\n'])
ser.write(new_str .encode('ascii','replace'))
sleep(0.01)
print(ser.readline())
sleep(0.01)
