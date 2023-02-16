# pylint: disable=unused-import, unused-argument, missing-function-docstring, unused-variable, missing-module-docstring
from queue import Empty
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from config import BLUETOOTH_SAMPLES

def feed_analyser_proc(freq_in, low_bandwidth_output):
    while True:
        i = 1
        # print(f"received {len(freq_in.get())} frequency sets")
