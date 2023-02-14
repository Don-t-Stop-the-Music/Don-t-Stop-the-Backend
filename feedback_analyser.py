
from queue import Empty
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from config import bluetooth_samples, feedback_noise_thresh, slow_factor, fast_factor

def feed_analyser_proc(freq_in, low_bandwidth_output):
    prev = freq_in.get()
    #buffer = np.array(size=(10, freqs.shape[0], freqs.shape[1]))
    feedback_tracker = np.zeros(shape=prev.shape)
    while True:

        temp = freq_in.get()
        slow_feedback_add = (temp > feedback_noise_thresh) & (temp> prev * slow_factor)
        fast_feedback_add = (temp > feedback_noise_thresh) & (temp> prev * fast_factor)
        feedback_tracker += 1 * slow_feedback_add + 1000 * fast_feedback_add
        feedback_tracker[~(slow_feedback_add| fast_feedback_add)] = 0
        print(f"received {len(freq_in.get())} frequency sets")
        slow_feedback = feedback_tracker % 1000 > 8
        fast_feedback = feedback_tracker / 1000 > 10
        for r in range(slow_feedback.shape[0]):
            print(r)
            print("slow")
            print(index_to_freq(slow_feedback[r].nonzero()[0], prev.shape[1]))
            print("fast")
            print(index_to_freq(fast_feedback[r].nonzero()[0], prev.shape[1]))



        freqs = freq_in.get()

def index_to_freq(arr, samples):
    print(arr)
    return 20 + arr * (20000 - 20)/samples