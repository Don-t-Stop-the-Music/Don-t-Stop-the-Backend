from multiprocessing import Process, Queue
from queue import Empty
import numpy as np
from config import sample_rate, lowest_hz, total_frequencies
import math

def freq_analyser_proc(audio_input, high_bandwidth_output, low_bandwidth_output):
    analysis_size = math.ceil(sample_rate/lowest_hz) * 2
    max_size = analysis_size * total_frequencies
    current_size = 0
    audio_block = np.full(max_size, np.nan)
    current_analysed = 0

    sample_chunk, channel = audio_input.get()
    print("here")
    while True:
        try:
            sample_chunk, channel = audio_input.get_nowait()

            #Checks if buffer already full
            if current_size + sample_chunk.size > max_size:
                print(-(sample_chunk.size - (max_size - current_size)))
                rollback = -(sample_chunk.size - (max_size - current_size))
                np.roll(audio_block, rollback)
                current_size = max_size - sample_chunk.size
                current_analysed -= rollback
            # Copies new sample data into audio block
            audio_block[current_size:current_size+sample_chunk.size] = sample_chunk
            current_size = current_size + sample_chunk.size
            print(f"audio_block end {audio_block[current_size-1]} current_size {current_size} sample_chunk {sample_chunk}")

        except Empty:
            print(f"end {audio_block[-1]}")
            #frequency analysis
            working = current_analysed
            magnitude = None
            while ((current_size - working) >= analysis_size):
                sample_set = audio_block[working:working + analysis_size]
                magnitude = np.abs(np.fft.rfft(sample_set))
                high_bandwidth_output.put((magnitude, channel))
            #after
            if any(magnitude):
                low_bandwidth_output.put((magnitude, "frequency", channel))
            current_analysed = working
            sample_chunk, channel = audio_input.get()

def freq_analysers():
    return 1