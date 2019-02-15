import matplotlib.pyplot as plt
import math
from typing import Tuple, List


def time_series_plot_group(title, plot_data):

    def time_series_subplot(plot, time: List[float], data: List[float], events: List[Tuple[float, str]], x_label: str, y_label: str):
        plot.plot(time, data)

        text_at_top = True
        for (event_time, event_name) in events:
            y = max(data) if text_at_top else min(data)
            plot.axvline(x=event_time, color='black', linewidth=0.5, linestyle='--')
            plot.text(x=event_time, y=y, s=event_name)
            text_at_top = not text_at_top

        plot.set_xlabel(x_label)
        plot.set_ylabel(y_label)

    cols = 2
    rows = math.ceil(len(plot_data) / cols)

    fig, ax = plt.subplots(nrows=rows, ncols=cols)

    for i, row in enumerate(ax):
        for j, col in enumerate(row):
            index = i*cols + j

            if index < len(plot_data):
                time_series_subplot(col, *plot_data[index])

    plt.show()








