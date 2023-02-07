from multiprocessing import Process, Queue
import numpy as np
import sounddevice as sd
from config import device


def callback_w(analysers):
    def callback(indata, frames, time, status):
        #print(f"indata {indata.shape} status {status} end {indata[-1]}")
        #print(f"indata[0] {indata[:, 0]}")

        # Separate analysers for each channel
        for i, analysers_sub in enumerate(analysers):
            for a in analysers_sub:
                a.put((indata[:, 0], i))
    return callback


def sound_input_proc(analysers):
    with sd.InputStream(device=device, channels=1, callback=callback_w(analysers)):
        while True:
            i=1
