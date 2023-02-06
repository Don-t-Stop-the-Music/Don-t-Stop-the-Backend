from multiprocessing import Process, Queue, Manager
from queue import Empty
from time import sleep

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from sound_input import sound_input_proc
from freq_analyser import freq_analyser_proc
from feedback_analyser import feed_analyser_proc

if __name__ == '__main__':
    freq_q_1 = Queue()
    freq_q_2 = Queue()

    analysers = [[freq_q_1, freq_q_2]]

    feedback_in_q1 = Queue()
    feedback_in_q2 = Queue()

    graph_q1 = Queue()
    graph_q2 = Queue()

    bluetooth_in = Queue()

    fap_1 = Process(target=freq_analyser_proc, args=(freq_q_1, [feedback_in_q1, graph_q1], bluetooth_in,))
    fap_1.start()

    fap_2 = Process(target=freq_analyser_proc, args=(freq_q_2, [feedback_in_q1, graph_q2], bluetooth_in, ))
    fap_2.start()


    feedp_1 = Process(target=feed_analyser_proc, args=(feedback_in_q1, bluetooth_in))
    feedp_1.start()

    feedp_2 = Process(target=feed_analyser_proc, args=(feedback_in_q2, bluetooth_in ))
    feedp_2.start()

    p = Process(target=sound_input_proc, args=(analysers,))
    p.start()

    def update_eq(frame):
        #print(f"plotdata: {len(plotdata)}\nlatest: {len(latest)}")
        #print(plotdata)
        line[0].set_ydata(graph_q1.get()[0][0:2205])
        print("updating")
        return line

    length = int(2205)
    fig, ax = plt.subplots()
    line = ax.plot(np.zeros(length))
    line[0].set_xdata(np.linspace(num=length, start=0, stop=20000))
    ax.axis((20, 20000, -5, 20))
    ax.set_xscale('log')
    ax.tick_params(bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)
    ani = FuncAnimation(fig, update_eq, interval=30, blit=True)
    plt.show()
    #p.join()