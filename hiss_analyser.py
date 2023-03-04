"""
Hiss Analyser
Takes in frequency samples and detects fwhether hiss is above some threshold
"""
from queue import Empty
import numpy as np
from config import HISS_THRESH, HIGH_SAMPLES


def hiss_analyser_proc(freq_in, low_bandwidth_output):
    """
    Hiss analyser process.
    Takes in a frequency queue and outputs hiss bool

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
        
