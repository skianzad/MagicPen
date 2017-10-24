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
N = 400
Del=10
Sp=150
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))
ser=serial.Serial('COM4',19200,timeout=0.2)

# Set up plot
plot = figure(plot_height=600, plot_width=800, title="my Graph",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[-4*np.pi, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)




# Set up widgets
text = TextInput(title="Custom function", value='Enter f(x)')
offset = Slider(title="Offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="Amplitude", value=1.0, start=-3.0, end=3.0, step=0.01)
Speed= Slider(title="Speed", value=100, start=100, end=250)
Delay = Slider(title="Delay", value=1, start=1, end=100)


CurveList=[("Sin","C1"),("Poly","C2"),("Abs","C3"),("inv/inf","C5"),("Frq","C6"),("Custom","C4")]
dropdown=Dropdown(label="Curve Lists",button_type="warning",menu=CurveList)


button = Button(label="Run ", button_type="success")



def update_title(attrname, old, new):
    plot.title.text = text.value
    x=np.linspace(-4*np.pi,4*np.pi,N)


text.on_change('value', update_title)


div = Div(width=1000)
def change_output(attr, old, new):
    global Del
    global Sp
    Del=Delay.value
    Sp=Speed.value

def display_event(div):
    return CustomJS(args=dict(div=div), code="""
    console.log("run")
    """ )
def update_data(attrname, old, new):

    # Get the current slider values
    a = amplitude.value
    b = offset.value
    global x
    global y
    # Generate the new curve
    if dropdown.value=='C1':
        x = np.linspace(-4*np.pi, 4*np.pi, N)
        
        y = a*np.sin(x) + b
    elif dropdown.value=='C2':
        x = np.linspace(-1*np.pi, 1*np.pi, N/2)
        y = a*0.2*(x*x) + b
    elif dropdown.value=='C3':
        x = np.linspace(-1*np.pi, 1*np.pi, N/2)
        y = a*np.abs(x) + b
    elif dropdown.value=='C4':
        x=np.linspace(-4*np.pi,4*np.pi,N)
        eq=parser.expr(text.value).compile()
        y = a*eval(eq)+ b
    elif dropdown.value=='C5':
        t=np.linspace(5,0.1, N/2)
        x = 1/t
        y = 1/(a*x) + b
    elif dropdown.value=='C6':
        x = np.linspace(-4*np.pi, 4*np.pi, N)
        y = np.sin(a*x) + b
    else:
        x = np.linspace(-4*np.pi, 4*np.pi, N)
        y = a*np.sin(x) + b
    source.data = dict(x=x, y=y)

for w in [offset, amplitude]:
    w.on_change('value', update_data)

for Z in [Delay,Speed]:
    Z.on_change('value',change_output)
def stop():
    global flag
    flag=False
    print("stop the thread")

    
def function_to_call(attr, old, new):
    print(dropdown.value)
    update_data(attr, old, new)

def run():
    if(ser.isOpen() == False):
        ser.open()
    dx=np.gradient(x)
    dy=np.gradient(y)
    scale=np.divide(dy,dx)
    if np.amax(dy)>=np.amax(dx):
        Scale_number=Sp/np.amax(dy)
    else:
        Scale_number=Sp/np.amax(dx)
    source.data = dict(x=[], y=[])
    for i in range(len(x)-1):
        my_int=int(round(dy[i]*Scale_number))
        mx_int=int(round(dx[i]*Scale_number))
        new_str = ''.join(['a',str('{:03d}'.format(my_int+256)),'b',str('{:03d}'.format(mx_int+256)),'/r','\n'])
        ser.write(new_str .encode('ascii','replace'))
        print(ser.readline())
        sleep(Del/1000)
        new_data={'x':[x[i],x[i+1]],'y':[y[i],y[i+1]]}
        source.stream(new_data)

    new_str = ''.join(['a',str('{:03d}'.format(256)),'b',str('{:03d}'.format(256)),'r','\n'])
    ser.write(new_str .encode('ascii','replace'))
    sleep(0.01)
    print(ser.readline())
    sleep(0.01)
    ser.close()
    print ("Process finished...exiting1")
    
button = Button(label="Run ", button_type="success")
dropdown.on_change('value', function_to_call)
button.on_click(run)
inputs = widgetbox(dropdown,text, offset, amplitude, Speed, Delay,button)
# Set up Server

curdoc().add_root(row(inputs,plot, width=1200))
curdoc().title = "Sliders"
