from multiprocessing import Process, Queue, Manager
from queue import Empty
from time import sleep
from sound_input import sound_input_proc
from freq_analyser import freq_analyser_proc
from feedback_analyser import feed_analyser_proc

if __name__ == '__main__':
    freq_q_1 = Queue()
    freq_q_2 = Queue()

    analysers = [[freq_q_1, freq_q_2]]

    feedback_in_q1 = Queue()
    feedback_in_q2 = Queue()

    bluetooth_in = Queue()

    fap_1 = Process(target=freq_analyser_proc, args=(freq_q_1, [feedback_in_q1], bluetooth_in,))
    fap_1.start()

    fap_2 = Process(target=freq_analyser_proc, args=(freq_q_2, [feedback_in_q1], bluetooth_in, ))
    fap_2.start()


    feedp_1 = Process(target=feed_analyser_proc, args=(feedback_in_q1, bluetooth_in))
    feedp_1.start()

    feedp_2 = Process(target=feed_analyser_proc, args=(feedback_in_q2, bluetooth_in ))
    feedp_2.start()

    p = Process(target=sound_input_proc, args=(analysers,))
    p.start()
    p.join()