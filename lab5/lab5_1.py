import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button
from scipy.signal import iirfilter, filtfilt

# Визначення часу
t = np.linspace(0, 10, 1000)

# Початкові значення параметрів
initial_amplitude = 1.0
initial_frequency = 0.3
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
initial_cutoff_freq = 0.04
show_noise = True

prev_noise_mean, prev_noise_covariance = initial_noise_mean, initial_noise_covariance
noise = np.random.normal(initial_noise_mean, initial_noise_covariance, size=len(t))

def regenerate_noise(nom, noc):
    global noise
    noise = np.random.normal(nom, noc, size=len(t))

# Функція для гармоніки з накладеним шумом
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

# Функція для фільтрації сигналу
def apply_filter(y, cutoff_freq, order=4):
    b, a = iirfilter(order, cutoff_freq, btype='lowpass')
    return filtfilt(b, a, y)

# Функція для оновлення графіків
def update_plot(val):
    amplitude = amp_slider.val
    frequency = freq_slider.val
    phase = phase_slider.val
    noise_mean = noise_mean_slider.val
    noise_covariance = noise_covar_slider.val
    cutoff_freq = cutoff_freq_slider.val
    show_noise = check.get_status()[0]

    y = harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise)
    filtered_y = apply_filter(y, cutoff_freq)

    line.set_ydata(y)
    filtered_line.set_ydata(filtered_y)

    axs[0].relim()
    axs[0].autoscale_view()
    axs[1].relim()
    axs[1].autoscale_view()
    plt.draw()

# Створення графічного вікна та підготовка підграфіків
fig, axs = plt.subplots(2, 1)
fig.subplots_adjust(left=0.25, top=0.95, bottom=0.32)

# Створення графіків
y = harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase, initial_noise_mean, initial_noise_covariance, show_noise)
filt_y = apply_filter(y, initial_cutoff_freq)

line, = axs[0].plot(t, y, color="blue")
axs[0].set_title("Harmonic")

filtered_line, = axs[1].plot(t, filt_y, color='red', label = "Filtered Harmonic")
axs[1].set_title("Filtered Harmonic")

# Створення слайдерів
amp_slider_ax = plt.axes([0.25, 0.25, 0.65, 0.03])
amp_slider = Slider(amp_slider_ax, 'Amplitude', 0.1, 10.0, valinit=initial_amplitude)
amp_slider.on_changed(update_plot)

freq_slider_ax = plt.axes([0.25, 0.2, 0.65, 0.03])
freq_slider = Slider(freq_slider_ax, 'Frequency', 0.01, 3.0, valinit=initial_frequency)
freq_slider.on_changed(update_plot)

phase_slider_ax = plt.axes([0.25, 0.15, 0.65, 0.03])
phase_slider = Slider(phase_slider_ax, 'Phase', 0.0, 2 * np.pi, valinit=initial_phase)
phase_slider.on_changed(update_plot)

noise_mean_slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
noise_mean_slider = Slider(noise_mean_slider_ax, 'Noise Mean', -1.0, 1.0, valinit=initial_noise_mean)
noise_mean_slider.on_changed(update_plot)

noise_covar_slider_ax = plt.axes([0.25, 0.05, 0.65, 0.03])
noise_covar_slider = Slider(noise_covar_slider_ax, 'Noise Covariance', 0.01, 1.0, valinit=initial_noise_covariance)
noise_covar_slider.on_changed(update_plot)

cutoff_freq_slider_ax = plt.axes([0.25, 0, 0.65, 0.03])
cutoff_freq_slider = Slider(cutoff_freq_slider_ax, 'Cutoff Frequency', 0.001, 0.09, valinit=initial_cutoff_freq)
cutoff_freq_slider.on_changed(update_plot)

check_ax = plt.axes([0.01, 0.6, 0.18, 0.1])
check = CheckButtons(check_ax, ['Show Noise'], [True])
check.on_clicked(update_plot)

reset_ax = plt.axes([0.01, 0.5, 0.18, 0.1])
button = Button(reset_ax, 'Reset')

def reset(event):
    amp_slider.reset()
    freq_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_covar_slider.reset()
    cutoff_freq_slider.reset()

button.on_clicked(reset)

plt.show()
