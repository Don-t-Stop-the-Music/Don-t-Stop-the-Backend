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

    bluetooth_in = Queue()

    print(sd.query_devices())

    fap_1 = Process(target=freq_analyser_proc, args=([feedback_in_q1, feedback_in_q2], bluetooth_in,))
    fap_1.start()

    feedp_1 = Process(target=feed_analyser_proc, args=(feedback_in_q1, bluetooth_in, 0))
    feedp_1.start()

    feedp_2 = Process(target=feed_analyser_proc, args=(feedback_in_q2, bluetooth_in, 1))
    feedp_2.start()

    fap_1.join()