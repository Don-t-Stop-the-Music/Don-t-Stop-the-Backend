from multiprocessing import Process, Queue
from queue import Empty
import numpy as np
from config import sample_rate, lowest_hz, frequency_overlap
import math

def freq_analyser_proc(audio_input, high_bandwidth_output, low_bandwidth_output):
    analysis_size = math.ceil(sample_rate/lowest_hz) * 2
    max_size = analysis_size * 2
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
                #print(-(sample_chunk.size - (max_size - current_size)))
                rollback = (sample_chunk.size - (max_size - current_size))
                np.roll(audio_block, -rollback)
                current_size = max_size - sample_chunk.size
                current_analysed = max((current_analysed - rollback), 0)
                print(f"current_analysed: {current_analysed}")
            # Copies new sample data into audio block
            audio_block[current_size:current_size+sample_chunk.size] = sample_chunk
            current_size = current_size + sample_chunk.size
            #print(f"audio_block end {audio_block[current_size-1]} current_size {current_size} sample_chunk {sample_chunk}")

        except Empty:
            #print(f"end {audio_block[-1]}")
            #frequency analysis
            working = current_analysed
            magnitude = None
            #print("before while loop")
            while ((current_size - working) >= analysis_size):
                print("before sample_set")
                sample_set = audio_block[working:working + analysis_size]
                print("before rfft")
                magnitude = np.abs(np.fft.rfft(sample_set))
                print("before output to queues")
                for out in high_bandwidth_output:
                    out.put((magnitude, channel))
                print(f"working: {working}")
                working += int(analysis_size / frequency_overlap) 
            #after
            #print("before magnitude")
            #if magnitude:
                #low_bandwidth_output.put((magnitude, "frequency", channel))
            #print("before current analysed")
            current_analysed = working
            #print("before audio_input get")
            sample_chunk, channel = audio_input.get()

def freq_analysers():
    return 1