import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
import geopandas as gpd
from scipy.ndimage import median_filter
import pandas as pd

class RasterViewer:
    def __init__(self, raster_data):
        self.raster_data = raster_data
        self.num_bands = raster_data.shape[2] if len(raster_data.shape) == 3 else 1

        self.current_band_combination = list(range(min(3, self.num_bands)))
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Raster Viewer")

        self.image = self.ax.imshow(self.get_current_band_combination(), extent=(0, raster_data.shape[1], 0, raster_data.shape[0]))

        self.ax_slider = plt.axes([0.1, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        self.slider = Slider(self.ax_slider, 'Zoom', 1, 10, valinit=1)
        self.slider.on_changed(self.update)

        self.ax_radio = plt.axes([0.8, 0.25, 0.1, 0.15], facecolor='lightgoldenrodyellow')
        self.radio_buttons = RadioButtons(self.ax_radio, tuple(map(str, range(self.num_bands))),
                                  active=self.current_band_combination[0])
        self.radio_buttons.on_clicked(self.update_band_combination)

        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

        plt.show()

    def update(self, val):
        zoom_factor = self.slider.val
        self.ax.set_xlim(0, self.raster_data.shape[1] / zoom_factor)
        self.ax.set_ylim(0, self.raster_data.shape[0] / zoom_factor)
        self.fig.canvas.draw_idle()

    def on_scroll(self, event):
        if event.button == 'up':
            self.slider.set_val(self.slider.val + 1)
        elif event.button == 'down':
            self.slider.set_val(self.slider.val - 1)

    def on_click(self, event):
        if event.button == 2:  # Middle mouse button for panning
            self.fig.canvas.toolbar.pan()
        elif event.button == 3:  # Right mouse button for zooming
            self.fig.canvas.toolbar.zoom()

    def update_band_combination(self, label):
        selected_bands = list(map(int, label))
        self.current_band_combination = selected_bands
        self.image.set_array(self.get_current_band_combination())
        self.fig.canvas.draw_idle()

    def get_current_band_combination(self):
        if self.num_bands == 1:
            return self.raster_data[:, :, 0]
        else:
            return np.stack([self.raster_data[:, :, band] for band in self.current_band_combination], axis=-1)

# Generate a random 3-band raster data for testing
raster_data = np.random.rand(100, 100, 3)

viewer = RasterViewer(raster_data)

# NumPy-based operations
viewer.apply_math_operation(np.sqrt)  # Square root transformation
viewer.apply_filter(median_filter)  # Median filter
viewer.calculate_statistics()  # Calculate statistics
