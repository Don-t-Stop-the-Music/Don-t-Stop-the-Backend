"""
Feedback Analyser
Takes in frequency samples and detects frequency bands which are feedbacking
And Hiss
"""
from queue import Empty

import numpy as np
from config import FEEDBACK_NOISE_THRESH, SLOW_FACTOR, FAST_FACTOR, HISS_THRESH, HIGH_SAMPLES
from utility import index_to_freq


def feed_hiss_analyser_proc(freq_in, low_bandwidth_output):
    """
    Feedback analyser process and Hiss
    Takes in a frequency queue and outputs feedback bands

    Parameters:
        freq_in (Queue): Frequency input queue
        low_bandwidth_output (Queue): Bands of feedback output

    """
    prev = freq_in.get()
    feedback_tracker = np.zeros(shape=prev.shape)
    temp = freq_in.get()
    while True:
        try:
            while True:
                temp = freq_in.get_nowait()
        except Empty:

            slow_feedback_add = (temp > FEEDBACK_NOISE_THRESH) & (
                temp > prev * SLOW_FACTOR)
            fast_feedback_add = (temp > FEEDBACK_NOISE_THRESH) & (
                temp > prev * FAST_FACTOR)
            feedback_tracker += 1 * slow_feedback_add + 1000 * fast_feedback_add
            feedback_tracker[~(slow_feedback_add | fast_feedback_add)] = 0
            slow_feedback = (feedback_tracker % 1000) > 15
            fast_feedback = (feedback_tracker / 1000) > 10

            slow_bands = []
            fast_bands = []
            bands = []
            for i in range(slow_feedback.shape[0]):
                slow_bands.append(index_to_freq(
                    slow_feedback[i].nonzero()[0], prev.shape[1]))
                fast_bands.append(index_to_freq(
                    fast_feedback[i].nonzero()[0], prev.shape[1]))
                bands.append((slow_bands[i]).tolist())

            # Hiss Detection.
            hiss = [False, False]
            # for each channel, take the quietest 10% of frequencies and check if their average is
            # above the threshold in config.py
            for i in range(2):
                if np.mean(temp[i][np.argpartition(temp[i], int(HIGH_SAMPLES / 10))]) > HISS_THRESH:
                    hiss[i] = True

            # place the results from analysis into the bluetooth queue and block.
            low_bandwidth_output.put(("hiss", hiss))
            low_bandwidth_output.put(("feedback", bands))

            temp = freq_in.get()
