from multiprocessing import Process, Queue
from queue import Empty
import numpy as np
from config import sample_rate, lowest_hz
import math

def freq_analyser_proc(audio_input):
    max_size = math.ceil(sample_rate/lowest_hz)
    current_size = 0
    audio_block = np.full(max_size, np.nan)

    sample_chunk, channel = audio_input.get()
    print("here")
    while True:
        try:
            sample_chunk, channel = audio_input.get_nowait()

            #Checks if buffer already full
            if current_size + sample_chunk.size > max_size:
                print(-(sample_chunk.size - (max_size - current_size)))
                np.roll(audio_block, -(sample_chunk.size - (max_size - current_size)))
                current_size = max_size - sample_chunk.size
            # Copies new sample data into audio block
            audio_block[current_size:current_size+sample_chunk.size] = sample_chunk
            current_size = current_size + sample_chunk.size
            print(f"audio_block end {audio_block[current_size-1]} current_size {current_size} sample_chunk {sample_chunk}")

        except Empty:
            print(f"end {audio_block[-1]}")

            sample_chunk, channel = audio_input.get()

def freq_analysers():
    return 1