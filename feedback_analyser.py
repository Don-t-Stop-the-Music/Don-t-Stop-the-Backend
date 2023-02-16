
from queue import Empty
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from config import bluetooth_samples


def feed_analyser_proc(freq_in, low_bandwidth_output):
    while True:
        i=1
        #print(f"received {len(freq_in.get())} frequency sets")