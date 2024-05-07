from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Switch, Button, Paragraph, Select
import numpy as np

t = np.linspace(0, 10, 1000)

initial_amplitude = 1.0
initial_frequency = 0.3
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
initial_cutoff_freq = 10
show_noise = True
initial_filter = "Simple Moving Average"
initial_window_size = 10
initial_coef = 0.5

prev_noise_mean, prev_noise_covariance = initial_noise_mean, initial_noise_covariance
noise = np.random.normal(initial_noise_mean, initial_noise_covariance, size=len(t))


def regenerate_noise(nom, noc):
    global noise
    noise = np.random.normal(nom, noc, size=len(t))

def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    global prev_noise_mean, prev_noise_covariance
    if show_noise:
        if (noise_mean != prev_noise_mean or noise_covariance != prev_noise_covariance):
            prev_noise_mean, prev_noise_covariance = noise_mean, noise_covariance
            regenerate_noise(noise_mean, noise_covariance)
        return signal + noise
    else:
        return signal


def apply_filter(signal, filter_type, window_size, coef):
    if filter_type == 'Exponential Weighted Moving Average':
        ewma_values = [signal[0]]
        alpha = coef
        for i in range(1, len(signal)):
            next_ewma = alpha * signal[i] + (1 - alpha) * ewma_values[-1]
            ewma_values.append(next_ewma)
        return np.array(ewma_values)
            
    elif filter_type == 'Simple Moving Average':
        return np.convolve(signal, np.ones(window_size)/window_size, mode='same')


plot1 = figure(title="Гармоніка з шумом", tools="crosshair,pan,reset,save,wheel_zoom",
                x_axis_label="time", y_axis_label="y", toolbar_location="below")

plot2 = figure(title="Відфільтрована гармоніка", tools="crosshair,pan,reset,save,wheel_zoom",
                x_axis_label="time", y_axis_label="y", toolbar_location="below")

y = harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase, initial_noise_mean, initial_noise_covariance, show_noise)
filt_y = apply_filter(y, initial_filter, initial_window_size, initial_coef)

source = ColumnDataSource(data=dict(x=t, y=y))
filtsource = ColumnDataSource(data=dict(x=t, y=filt_y))

plot1.line('x', 'y', source=source, line_width=2, color='blue')
plot2.line('x', 'y', source=filtsource, color='yellow', line_width=3)

plot1.title_location = "above"
plot1.title.text_font_size = "25px"
plot1.title.align = "center"
plot1.title.text_color = "darkblue"
plot1.grid.grid_line_alpha = 0.9
plot1.grid.grid_line_dash = [6, 4]

plot2.title_location = "above"
plot2.title.text_font_size = "25px"
plot2.title.align = "center"
plot2.title.text_color = "darkblue"
plot2.grid.grid_line_alpha = 0.9
plot2.grid.grid_line_dash = [6, 4]

def update_plot(attrname, old, new):
    amplitude = amplitude_slider.value
    frequency = frequency_slider.value
    phase = phase_slider.value
    noise_mean = noise_mean_slider.value
    noise_covariance = noise_covariance_slider.value
    show_noise = show_noise_checkbox.active
    filter_type = filter_select.value
    window_size = window_size_slider.value
    coef = coef_slider.value

    y = harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise)
    filtered_y = apply_filter(y, filter_type, window_size, coef)

    source.data = dict(x=t, y=y)
    filtsource.data = dict(x=t, y=filtered_y)

# Створення слайдерів
amplitude_slider = Slider(title="Amplitude", value=initial_amplitude, start=-10, end=10, step=1, bar_color="green", margin=12)
frequency_slider = Slider(title="Frequency", value=initial_frequency, start=0, end=3, step=0.01, bar_color="blue", margin=10)
phase_slider = Slider(title="Phase", value=initial_phase, start=0, end=2*np.pi, step=0.1, bar_color="purple", margin=10)
noise_mean_slider = Slider(title="Noise Mean", value=initial_noise_mean, start=-1, end=1, step=0.1, bar_color="yellow", margin=10)
noise_covariance_slider = Slider(title="Noise Covariance", value=initial_noise_covariance, start=0, end=1, step=0.01, bar_color="orange", margin=10)
window_size_slider = Slider(title="Moving Average Window Size", value=initial_window_size, start=1, end=100, step=1, bar_color="darkblue", margin=10)
coef_slider = Slider(title="Expotential Average Window Factor", value=initial_coef, start=0.01, end=1, step=0.01, bar_color="darkblue", margin=10)
filter_select = Select(title="Filter Type:", value=initial_filter, options=["Simple Moving Average", "Exponential Weighted Moving Average"], margin=10)
show_noise_checkbox = Switch(active=show_noise, margin=10, align="center")
p = Paragraph(text="""Show/Not Noise""", margin=10, align="center")

# Створення кнопки Reset
reset_button = Button(label="Reset", button_type="success", margin=10)

def reset():
    amplitude_slider.value = initial_amplitude
    frequency_slider.value = initial_frequency
    phase_slider.value = initial_phase
    noise_mean_slider.value = initial_noise_mean
    noise_covariance_slider.value = initial_noise_covariance
    show_noise_checkbox.active = show_noise
    coef_slider.value = initial_coef
    filter_select.value = initial_filter

reset_button.on_click(reset)

# Оновлення графіків при зміні параметрів
for slider in [amplitude_slider, frequency_slider, phase_slider, noise_mean_slider, noise_covariance_slider, window_size_slider, filter_select, coef_slider]:
    slider.on_change('value', update_plot)

show_noise_checkbox.on_change('active', update_plot)


layout = column(amplitude_slider, frequency_slider, phase_slider, noise_mean_slider, noise_covariance_slider, filter_select,
                  window_size_slider, coef_slider, reset_button, p, show_noise_checkbox)

curdoc().add_root(row(plot1, plot2, layout))
curdoc().title = "Sliders"
