import matplotlib.pyplot as plt
from typing import Tuple, List


def plot(time: List[float], data: List[float], events: List[Tuple[float, str]], x_label: str, y_label: str):
    plt.plot(time, data)

    text_at_top = True
    for (event_time, event_name) in events:
        y = max(data) if text_at_top else min(data)
        plt.axvline(x=event_time, color='black', linewidth=0.5, linestyle='--')
        plt.text(x=event_time, y=y, s=event_name)
        text_at_top = not text_at_top

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
