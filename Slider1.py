''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource,Div,CustomJS
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure,ColumnDataSource
from bokeh.models.widgets import Button
from bokeh.models.widgets import Dropdown
from bokeh import events




# Set up data
N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[-4*np.pi, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="title", value='my Graphs')
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0)
Speed= Slider(title="Speed", value=100, start=100, end=250)
Delay = Slider(title="Delay", value=100, start=50, end=500)


CurveList=[("Sin","C1"),("Polynomial","C2"),("abs","C3")]
dropdown=Dropdown(label="Curve Lists",button_type="warning",menu=CurveList)


button = Button(label="Run ", button_type="success")

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)


div = Div(width=1000)

def display_event(div):
    return CustomJS(args=dict(div=div), code="""
    console.log("run")
    """ )
def update_data(attrname, old, new):

    # Get the current slider values
    a = amplitude.value
    b = offset.value


    # Generate the new curve
    if dropdown.value=='C1':
        x = np.linspace(-4*np.pi, 4*np.pi, N)
        y = a*np.sin(x) + b
    elif dropdown.value=='C2':
        x = np.linspace(-4*np.pi, 4*np.pi, N)
        y = a*(x*x) + b
    elif dropdown.value=='C3':
        x = np.linspace(-4*np.pi, 4*np.pi, N)
        y = a*(x*x) + b        
    else:
        x = np.linspace(-4*np.pi, 4*np.pi, N)
        y = a*np.sin(x) + b
    source.data = dict(x=x, y=y)

for w in [offset, amplitude]:
    w.on_change('value', update_data)

def function_to_call(attr, old, new):
    print(dropdown.value)
    update_data(attr, old, new)
def run():
        print("run")
# Set up layouts and add to document
inputs = widgetbox(dropdown,text, offset, amplitude, Speed, Delay,button)
button.js_on_event(events.ButtonClick, display_event(div))
dropdown.on_change('value', function_to_call)
button.on_click(run)
curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
