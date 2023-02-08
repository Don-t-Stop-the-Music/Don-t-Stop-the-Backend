
from queue import Empty
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from config import bluetooth_samples


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
        #print(f"data length {len(data[-1])}")
        line[0].set_ydata(data[channel])
        #print("updating")
        return line

    try:
        data = freq_in.get()
        print("got")
        length = int(len(data[channel]))
        print(length)
        fig, ax = plt.subplots()
        line = ax.plot(np.zeros(length))
        x_data = np.linspace(num=length, start=0, stop=20000)
        if(length == bluetooth_samples):
            np.logspace(0,np.log10(20000), length)
        line[0].set_xdata(x_data)
        ax.axis((20, 20000, -5, 20))
        if(length > 80):
            ax.set_xscale('log')
        ax.tick_params(bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
        fig.tight_layout(pad=0)
        ani = FuncAnimation(fig, update_eq, interval=3, blit=True)
        plt.show()
    except Exception as e:
        print(e)