'''Display a frequency queue using MatPlotLib'''
from queue import Empty
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from config import BLUETOOTH_SAMPLES


def freq_visualiser_proc(freq_in, channel):
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
                data = freq_in.get_nowait()
            except Empty:
                break
        data = freq_in.get()
        # print(f"data length {len(data[-1])}")
        line[0].set_ydata(data[channel])
        # print("updating")
        return line

    data = freq_in.get()
    # print("got")
    length = int(len(data[channel]))
    # print(length)
    # pylint: disable-next=invalid-name
    fig, ax = plt.subplots()
    line = ax.plot(np.zeros(length))
    x_data = np.linspace(num=length, start=0, stop=20000)

    if length == BLUETOOTH_SAMPLES:
        np.logspace(0, np.log10(20000), length)

    line[0].set_xdata(x_data)
    ax.axis((20, 20000, -5, 150))

    if length > BLUETOOTH_SAMPLES:
        ax.set_xscale('log')

    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)
    # pylint: disable-next=unused-variable
    ani = FuncAnimation(fig, update_eq, interval=3, blit=True)
    plt.show()
