'''Display a frequency queue using MatPlotLib'''
import math
from queue import Empty
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from config import BLUETOOTH_SAMPLES, SAMPLE_RATE, LOWEST_FREQUENCY


def freq_visualiser_proc(channel, freq_in, low_in, low):
    '''Process to take in new frequency information and display it on a graph.
        Parameters:
            freq_in(Queue): a queue holding arrays of frequencies.
            channel(int): wihch channel of the frequency array to look at.'''
    print("visualiser online")

    # pylint: disable-next=unused-argument
    def update_eq(frame):
        # print(f"plotdata: {len(plotdata)}\nlatest: {len(latest)}")
        # print(plotdata)
        while True:
            try:
                if low:
                    new_data = low_in.get_nowait()
                    if new_data[0] == "frequency":
                        data = new_data[1]
                else:
                    data = freq_in.get_nowait()
            except Empty:
                break
        if low:
            new_data = low_in.get()
            if new_data[0] == "frequency":
                data = new_data[1]
        else:
            data = freq_in.get()
        # print(f"data length {len(data[-1])}")
        line[0].set_ydata(data[channel])
        # print("updating")
        return line

    if low:
        new_data = low_in.get()
        if new_data[0] == "frequency":
            data = new_data[1]
    else:
        data = freq_in.get()
    # print("got")
    length = int(len(data[channel]))
    # print(length)
    # pylint: disable-next=invalid-name
    fig, ax = plt.subplots()
    line = ax.plot(np.zeros(length))

    if low:
        x_data = np.logspace(0, np.log10((math.ceil(SAMPLE_RATE/LOWEST_FREQUENCY))),
                             BLUETOOTH_SAMPLES, dtype=int)
        x_data *= int(LOWEST_FREQUENCY / 2)
        x_data[0] = 0
    else:
        x_data = np.linspace(num=length, start=0, stop=22050)

    ax.set_xscale('log')
    line[0].set_xdata(x_data)
    ax.axis((1, 22050, -5, 150))

    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)
    # pylint: disable-next=unused-variable
    ani = FuncAnimation(fig, update_eq, interval=3, blit=True)
    plt.show()
