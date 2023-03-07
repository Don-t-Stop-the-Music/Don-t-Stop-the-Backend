'''The main module, the one that is run to start the program'''
from multiprocessing import Process, Manager
import sounddevice as sd
from freq_analyser import freq_analyser_proc
#from freq_visualiser import freq_visualiser_proc
from feedback_hiss_analyser import feed_hiss_analyser_proc
from bluetooth_process import bluetooth_proc
from config import SAMPLE_RATE

if __name__ == '__main__':
    #vis_high_in = Manager().Queue()
    feedback_in_q1 = Manager().Queue()
    hiss_in = Manager().Queue()

    bluetooth_in = Manager().Queue()
    bluetooth_in.put(("max_frequency", SAMPLE_RATE / 2))

    print(sd.query_devices())

    fap_1 = Process(target=freq_analyser_proc, args=(
        [feedback_in_q1], bluetooth_in,))
    fap_1.start()

    #vis_1 = Process(target=freq_visualiser_proc,
    #                args=(0, vis_high_in, Empty, False))
    #vis_1.start()

    #vis_2 = Process(target=freq_visualiser_proc,
    #                args=(0, Empty, bluetooth_in, True))
    #vis_2.start()

    feedp_1 = Process(target=feed_hiss_analyser_proc,
                     args=(feedback_in_q1, bluetooth_in))
    feedp_1.start()

    #hissp_1 = Process(target=hiss_analyser_proc, args=(hiss_in, bluetooth_in))

    bluetooth_1 = Process(target=bluetooth_proc, args=(bluetooth_in,))
    bluetooth_1.start()

    fap_1.join()
