'''The main module, the one that is run to start the program'''
from multiprocessing import Process, Queue
from queue import Empty
import sounddevice as sd
from freq_analyser import freq_analyser_proc
from freq_visualiser import freq_visualiser_proc
from feedback_analyser import feed_analyser_proc
from bluetooth import bluetooth_proc
from config import SAMPLE_RATE

if __name__ == '__main__':
    freq_q_1 = Queue()
    freq_q_2 = Queue()

    analysers = [[freq_q_1, freq_q_2]]

    vis_high_in = Queue()
    feedback_in_q1 = Queue()

    bluetooth_in = Queue()
    bluetooth_in.put(("max_frequency", SAMPLE_RATE / 2))

    print(sd.query_devices())

    fap_1 = Process(target=freq_analyser_proc, args=(
        [vis_high_in, feedback_in_q1], bluetooth_in,))
    fap_1.start()

    vis_1 = Process(target=freq_visualiser_proc,
                    args=(0, vis_high_in, Empty, False))
    vis_1.start()

    vis_2 = Process(target=freq_visualiser_proc,
                    args=(0, Empty, bluetooth_in, True))
    vis_2.start()

    feedp_1 = Process(target=feed_analyser_proc,
                      args=(feedback_in_q1, bluetooth_in))
    feedp_1.start()

    bluetooth_1 = Process(target=bluetooth_proc, args=(bluetooth_in,))
    bluetooth_1.start()

    fap_1.join()
