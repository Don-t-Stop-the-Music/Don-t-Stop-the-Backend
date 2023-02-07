from multiprocessing import Process, Queue
from queue import Empty
import numpy as np
from config import sample_rate, lowest_hz, frequency_overlap
import math

def freq_analyser_proc(audio_input, high_bandwidth_output, low_bandwidth_output):
    #magic numbers
    analysis_size = math.ceil(sample_rate/lowest_hz) * 2
    max_size = analysis_size * 40
    current_size = 0
    audio_block = np.full(max_size, np.nan)
    current_analysed = 0

    sample_chunk, channel = audio_input.get()
    print("frequency analyser running")
    while True:
        try:
            sample_chunk, channel = audio_input.get_nowait()

            #Checks if buffer already full
            if current_size + sample_chunk.size > max_size:
                np.roll(audio_block, -current_analysed)
                current_size -= current_analysed
                current_analysed = 0

            # Copies new sample data into audio block
            audio_block[current_size:current_size+sample_chunk.size] = sample_chunk
            current_size = current_size + sample_chunk.size

        except Empty:
            #frequency analysis
            working = current_analysed
            magnitude = np.empty(int(analysis_size / 2))

            #analyse as many times as queue allows(is actually only once when on pc)
            while ((current_size - working) >= analysis_size):
                sample_set = audio_block[working:working + analysis_size]
                magnitude = np.abs(np.fft.rfft(sample_set))
                for out in high_bandwidth_output:
                    out.put((magnitude, channel))
                working += int(analysis_size / frequency_overlap) 

            #after
            if magnitude.any():
                low_bandwidth_output.put((magnitude, "frequency", channel))
            current_analysed = working
            sample_chunk, channel = audio_input.get()

def freq_analysers():
    return 1