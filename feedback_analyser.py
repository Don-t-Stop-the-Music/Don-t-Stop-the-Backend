
from queue import Empty
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def feed_analyser_proc(freq_in, low_bandwidth_output, channel):
    print("feedback online")
    
    def update_eq(frame):
        #print(f"plotdata: {len(plotdata)}\nlatest: {len(latest)}")
        #print(plotdata)
        while (True):
            try:
                data = freq_in.get_nowait()
            except Empty:
                break
        data = freq_in.get()

        limit = freq_in.qsize()
        #print(f"limit: {limit}")
        for _ in range(limit):
                #print("data get")
                data = freq_in.get()
        #print(f"data length {len(data[-1])}")
        line[0].set_ydata(data[channel])
        #print("updating")
        return line

    length = int(2206)
    fig, ax = plt.subplots()
    line = ax.plot(np.zeros(length))
    line[0].set_xdata(np.linspace(num=length, start=0, stop=20000))
    ax.axis((20, 20000, -5, 20))
    ax.set_xscale('log')
    ax.tick_params(bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)
    ani = FuncAnimation(fig, update_eq, interval=3, blit=True)
    plt.show()
    None