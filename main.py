'''The main module, the one that is run to start the program'''
from multiprocessing import Process, Manager
import sounddevice as sd
from freq_analyser import freq_analyser_proc
# from freq_visualiser import freq_visualiser_proc
from feedback_hiss_analyser import feed_hiss_analyser_proc
from bluetooth_process import bluetooth_proc
from config import SAMPLE_RATE

# main function run by the Pi
if __name__ == '__main__':
    # vis_high_in = Manager().Queue()
    # queue sent from frequency analyser for use in feedback/hiss analysis.
    feedback_in_q1 = Manager().Queue()

    # queue for all the data to be sent to phone over bluetooth
    bluetooth_in = Manager().Queue()
    # bluetooth queue starts with the max frequency the device will send,
    # just so they will always agree if there are changes.
    bluetooth_in.put(("max_frequency", SAMPLE_RATE / 2))

    # frequency analyser process: take in sound, produce arrays of
    fap_1 = Process(target=freq_analyser_proc, args=(
        [feedback_in_q1], bluetooth_in,))
    fap_1.start()

    # these are visualisers to make sure data is correct.
    # they are commented out as they are quite computationally expensive and not used
    # outside of debug.

    # vis_1 = Process(target=freq_visualiser_proc,
    #                args=(0, vis_high_in, Empty, False))
    # vis_1.start()

    # vis_2 = Process(target=freq_visualiser_proc,
    #                args=(0, Empty, bluetooth_in, True))
    # vis_2.start()

    # this is the feedback/hiss analysis process, taking in an array of frequencies and
    # putting feedback locations and hiss detection into the bluetooth queue.
    feedp_1 = Process(target=feed_hiss_analyser_proc,
                      args=(feedback_in_q1, bluetooth_in))
    feedp_1.start()

    # the bluetooth process. This connects to a phone and sends data from bluetooth queue.
    bluetooth_1 = Process(target=bluetooth_proc, args=(bluetooth_in,))
    bluetooth_1.start()

    # join process so main doesn't die before the processes do.
    fap_1.join()
