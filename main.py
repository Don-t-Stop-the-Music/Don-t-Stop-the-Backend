from multiprocessing import Process, Queue, Manager

from freq_analyser import freq_analyser_proc
from freq_visualiser import freq_visualiser_proc
from feedback_analyser import feed_analyser_proc
from bluetooth import bluetooth_proc
import sounddevice as sd

if __name__ == '__main__':
    freq_q_1 = Queue()
    freq_q_2 = Queue()

    analysers = [[freq_q_1, freq_q_2]]

    vis_high_in = Queue()
    feedback_in_q1 = Queue()

    bluetooth_in = Queue()

    print(sd.query_devices())

    fap_1 = Process(target=freq_analyser_proc, args=([vis_high_in, feedback_in_q1], bluetooth_in,))
    fap_1.start()

    #vis_1 = Process(target=freq_visualiser_proc, args=(vis_high_in, bluetooth_in, 0))
    #vis_1.start()

    vis_2 = Process(target=freq_visualiser_proc, args=(bluetooth_in, bluetooth_in, 0))
    vis_2.start()

    feedp_1 = Process(target=feed_analyser_proc, args=(feedback_in_q1, bluetooth_in))
    feedp_1.start()
    
    bluetooth_1 = Process(target=bluetooth_proc, args=(bluetooth_in,))
    bluetooth_1.start()
    
    fap_1.join()
