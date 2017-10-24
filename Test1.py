import numpy as np
import parser
import serial
import time




from threading import Thread,Event
from time import sleep
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource,Div,CustomJS, Circle
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure,ColumnDataSource
from bokeh.models.widgets import Button
from bokeh.models.widgets import Dropdown
from bokeh import events


# Set up data
N = 500
Del=20
Sp=250
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))
ser=serial.Serial('COM4',9600,timeout=0.2)

# Set up plot
plot = figure(plot_height=600, plot_width=800, title="my Graph",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[-4*np.pi, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


def run():
    dx=np.gradient(x)
    dy=np.gradient(y)
    scale=np.divide(dy,dx)
    if np.amax(dy)>=np.amax(dx):
        Scale_number=Sp/np.amax(dy)
    else:
        Scale_number=Sp/np.amax(dy)
    source.data = dict(x=[], y=[])
    for i in range(len(x)-1):
        my_int=int(round(dy[i]*Scale_number))
        mx_int=int(round(dx[i]*Scale_number))
        t=int(round(x[i]))
        new_str = ''.join(['a',str('{:03d}'.format(my_int+256)),'b',str('{:03d}'.format(mx_int+256)),'/r','\n'])
        print(ser.write(new_str .encode('ascii','replace')))
        print(ser.readline())
        sleep(0.001)
        new_data={'x':[x[i],x[i+1]],'y':[y[i],y[i+1]]}
        source.stream(new_data)

    new_str = ''.join(['a',str('{:03d}'.format(256)),'b',str('{:03d}'.format(256)),'r','\n'])
    ser.write(new_str .encode('ascii','replace'))
    sleep(0.01)
    print(ser.readline())
    sleep(0.01)
    print ("Process finished...exiting1")
button = Button(label="Run ", button_type="success")

button.on_click(run)
inputs = widgetbox(button)
# Set up Server

curdoc().add_root(row(inputs,plot, width=1200))
curdoc().title = "Sliders"
