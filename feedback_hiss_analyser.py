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
    # Loads initial previous value of samples
    prev = freq_in.get()

    # Cumulative sum of slow and fast feedback detection. One value for each frequency
    feedback_tracker = np.zeros(shape=prev.shape)

    # Blocks until we have a valid second sample
    temp = freq_in.get()
    while True:
        try:
            # Get latest data in queue
            while True:
                temp = freq_in.get_nowait()
        except Empty:
            # Detects in there is frequency magnitude is over threshold and slow feedback multiplicative factor of previous value
            slow_feedback_add = (temp > FEEDBACK_NOISE_THRESH) & (
                temp > prev * SLOW_FACTOR)
            
            # Detects in there is frequency magnitude is over threshold and fast feedback multiplicative factor of previous value
            fast_feedback_add = (temp > FEEDBACK_NOISE_THRESH) & (
                temp > prev * FAST_FACTOR)
            
            # Adds 1 to feedback cum sum for slow and 1000 for fast feedback
            feedback_tracker += 1 * slow_feedback_add + 1000 * fast_feedback_add

            # If neither slow or fast feedback, reset cumulative sum
            feedback_tracker[~(slow_feedback_add | fast_feedback_add)] = 0

            # Checks if cumulative sum is over slow or fast feedback boundaries
            slow_feedback = (feedback_tracker % 1000) > 15
            fast_feedback = (feedback_tracker / 1000) > 10

            # This is mapping from the boolean array of feedback at each index to a compacted array of frequencies which are feedbacking.
            # Is a list as input has multiple channels 
            slow_bands = []
            fast_bands = []
            bands = []
            # For each channel (e.g. stereo, monitor, etc)
            for i in range(slow_feedback.shape[0]):
                # Get true indices and map to frequencies
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

            # Blocks until next value
            temp = freq_in.get()
