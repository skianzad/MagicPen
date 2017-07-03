import numpy as np
from threading import Thread
from time import sleep



from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider, Button, Div
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Button
from bokeh.models.widgets import Dropdown
from bokeh import events


CurveList=[("Sin","C1"),("Polynomial","C2"),("abs","C2")]
dropdown=Dropdown(label="Curve Lists",button_type="warning",menu=CurveList)
button = Button(label="Run ", button_type="success")

# Set up data
x = np.linspace(0,5*np.pi, 500)
y = np.sin(x)

source = ColumnDataSource(data=dict(x=x, y=y))

# Set up plot
plot = figure(y_range=(-10, 10), plot_width=1000, plot_height=800)

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var A = amp.value;
    //var k = freq.value;
    //var phi = phase.value;
    var B = offset.value;
    x = data['x']
    y = data['y']
    console.log("update")
    for (i = 0; i < x.length; i++) {
        y[i] = B + A*Math.sin(x[i]);
    }
    source.change.emit();
""")

amp_slider = Slider(start=100, end=250, value=1, step=.10,
                    title="Max Speed", callback=callback)
callback.args["MSpeed"] = amp_slider

freq_slider = Slider(start=50, end=500, value=1, step=25,
                     title="Delay", callback=callback)
callback.args["Delay"] = freq_slider

phase_slider = Slider(start=0, end=6.4, value=0, step=.1,
                      title="Amp", callback=callback)
callback.args["amp"] = phase_slider

offset_slider = Slider(start=-5, end=5, value=0, step=.1,
                       title="Offset", callback=callback)
callback.args["offset"] = offset_slider

div = Div(width=1000)

def display_event(div):
    return CustomJS(args=dict(div=div), code="""
    console.log("run")
    """ )


layout = row(
    widgetbox(dropdown,amp_slider, freq_slider, phase_slider, offset_slider,button),plot
)
button.js_on_event(events.ButtonClick, display_event(div))
output_file("slider.html", title="slider.py example")

show(layout)
##def threaded_function(arg):
##    for i in range(arg):
##        print ("running")
##        sleep(1)
##
##
##if __name__ == "__main__":
##    thread = Thread(target = threaded_function, args = (10, ))
##    thread.start()
##    thread.join()
##    print ("thread finished...exiting")
