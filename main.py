from multiprocessing import Process, Queue, Manager
from queue import Empty
from time import sleep

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from sound_input import sound_input_proc
from freq_analyser import freq_analyser_proc
from feedback_analyser import feed_analyser_proc
import sounddevice as sd

if __name__ == '__main__':
    freq_q_1 = Queue()
    freq_q_2 = Queue()

    analysers = [[freq_q_1, freq_q_2]]

    feedback_in_q1 = Queue()
    feedback_in_q2 = Queue()

    graph_q1 = Queue()
    graph_q2 = Queue()

    bluetooth_in = Queue()

    print(sd.query_devices())

    #fap_1 = Process(target=freq_analyser_proc, args=([feedback_in_q1, graph_q1], bluetooth_in,))
    #fap_1.start()

    #fap_2 = Process(target=freq_analyser_proc, args=([feedback_in_q1, graph_q2], bluetooth_in, ))
    #fap_2.start()


    feedp_1 = Process(target=feed_analyser_proc, args=(feedback_in_q1, bluetooth_in))
    feedp_1.start()

    freq_analyser_proc([feedback_in_q1, graph_q1], bluetooth_in)

    #feedp_2 = Process(target=feed_analyser_proc, args=(feedback_in_q2, bluetooth_in ))
    #feedp_2.start()

    #p = Process(target=sound_input_proc, args=(analysers,))
    #p.start()

    #p.join()