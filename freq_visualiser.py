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

    # update_eq is called by matplotlib to get new data for graphs
    # pylint: disable-next=unused-argument
    def update_eq(frame):
        # this is a loop to make sure that when connected to bluetooth,
        # you actually get a new set of frequency levels instead of just hiss and feedback data.
        got_freq = False
        while not got_freq:
            # collect frequency data from a queue, different for bluetooth data and high res data.
            while True:
                try:
                    if low:
                        new_data = low_in.get_nowait()
                        if new_data[0] == "frequency":
                            data = new_data[1]
                            got_freq = True
                    else:
                        data = freq_in.get_nowait()
                        got_freq = True
                except Empty:
                    break
            # one more data get just to make sure it has a blocking wait at some point.
            if low:
                new_data = low_in.get()
                if new_data[0] == "frequency":
                    data = new_data[1]
                    got_freq = True
            else:
                data = freq_in.get()
                got_freq = True
        # give the graph the new data
        line[0].set_ydata(data[channel])
        return line

    # main code, sets up the graph.
    # default data to prevent errors when no data is read in.
    data = np.zeros((2, BLUETOOTH_SAMPLES))
    # get data from queue, make sure it is the data you want if reading from bluetooth queue.
    if low:
        new_data = low_in.get()
        if new_data[0] == "frequency":
            data = new_data[1]
    else:
        data = freq_in.get()
    # set up the figure in matplotlib to display later.
    length = int(len(data[channel]))
    # pylint: disable-next=invalid-name
    fig, ax = plt.subplots()
    line = ax.plot(np.zeros(length))

    # these are the scales, designed to match the downsampling in freq_analyser
    # if coming from bluetooth, just to make sure the x axis scale is correct for the data.
    # this complicated function is not needed on phone where it just displays linearly.
    if low:
        x_data = np.logspace(0, np.log10((math.ceil(SAMPLE_RATE/LOWEST_FREQUENCY))),
                             BLUETOOTH_SAMPLES, dtype=int)
        x_data *= int(LOWEST_FREQUENCY / 2)
        x_data[0] = 0
    else:
        x_data = np.linspace(num=length, start=0, stop=22050)

    # graph is log scale to show the information as is common in the industry
    ax.set_xscale('log')
    line[0].set_xdata(x_data)
    # sets defualt range to show as much data as needed.
    ax.axis((1, 22050, -5, 150))

    # some config things.
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)
    # set up the animation to update the graph with new data every 3ms.
    # pylint: disable-next=unused-variable
    ani = FuncAnimation(fig, update_eq, interval=3, blit=True)
    # display the graph. this blocks so need one process per graph.
    plt.show()
