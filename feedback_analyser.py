"""
Feedback Analyser
Takes in frequency samples and detects frequency bands which are feedbacking
"""
import numpy as np
from config import FEEDBACK_NOISE_THRESH, SLOW_FACTOR, FAST_FACTOR


def feed_analyser_proc(freq_in, low_bandwidth_output):
    """
    Feedback analyser process.
    Takes in a frequency queue and outputs feedback bands

    Parameters:
        freq_in (Queue): Frequency input queue
        low_bandwidth_output (Queue): Bands of feedback output

    """
    prev = freq_in.get()
    feedback_tracker = np.zeros(shape=prev.shape)
    while True:
        temp = freq_in.get()
        slow_feedback_add = (temp > FEEDBACK_NOISE_THRESH) & (temp > prev * SLOW_FACTOR)
        fast_feedback_add = (temp > FEEDBACK_NOISE_THRESH) & (temp > prev * FAST_FACTOR)
        feedback_tracker += 1 * slow_feedback_add + 1000 * fast_feedback_add
        feedback_tracker[~(slow_feedback_add | fast_feedback_add)] = 0
        slow_feedback = (feedback_tracker % 1000) > 15
        fast_feedback = (feedback_tracker / 1000) > 10

        slow_bands = []
        fast_bands = []
        bands = []
        for i in range(slow_feedback.shape[0]):
            slow_bands.append(index_to_freq(slow_feedback[i].nonzero()[0], prev.shape[1]))
            fast_bands.append(index_to_freq(fast_feedback[i].nonzero()[0], prev.shape[1]))
            bands.append(slow_bands[i] + fast_bands[i])

        low_bandwidth_output.put(("feedback", bands))


def index_to_freq(arr, samples):
    """
    Converts sample array index into frequencies
    Parameters:
          arr (List): Input list of indices
          samples (int): Number of samples in full freq array
    Returns:
          int List: array of frequencies
    """
    return arr * (22050) / samples
