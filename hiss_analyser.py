"""
Hiss Analyser
Takes in frequency samples and detects fwhether hiss is above some threshold
"""
from queue import Empty
import numpy as np
from config import HISS_THRESH, HIGH_SAMPLES


def feed_analyser_proc(freq_in, low_bandwidth_output):
    """
    Feedback analyser process.
    Takes in a frequency queue and outputs feedback bands

    Parameters:
        freq_in (Queue): Frequency input queue
        low_bandwidth_output (Queue): Bands of feedback output

    """
    while True:
        while True:
            try:
                data = freq_in.get_nowait()
            except Empty:
                break
            data = freq_in.get()
        hiss = [False, False]
        for i in range(2):
            if np.mean(data[i][np.argpartition(data[i], HIGH_SAMPLES / 10)] > HISS_THRESH):
                hiss[i] = True
        low_bandwidth_output.put(("hiss", hiss))
