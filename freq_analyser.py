from queue import Queue
from queue import Empty
import numpy as np
from config import sample_rate, lowest_hz, frequency_overlap
import math
import sounddevice as sd
from config import device, bluetooth_samples

def freq_analyser_proc(high_bandwidth_output, low_bandwidth_output):
    #print("what")
    audio_input = Queue()
    analysis_size = math.ceil(sample_rate/lowest_hz) * 2
    max_size = analysis_size * 40
    current_size = 0
    audio_block = np.full(shape=(2,max_size), fill_value=np.nan)
    current_analysed = 0
    logspace = np.logspace(0, np.log10((analysis_size / 2)), bluetooth_samples, dtype=int)
    nums_to_take = np.transpose(np.array([logspace, np.append(logspace[1:], logspace[-1])]))
    #print(nums_to_take)

    print("freq_analyser online")
    with sd.InputStream(device=device, callback=callback_w(audio_input)):
        sample_chunk = audio_input.get()
        while True:
            try:
                #Checks if buffer already full
                if current_size + sample_chunk.size > max_size:
                    print("rollback!")
                    #rollback = max(current_analysed, (sample_chunk.size - (max_size - current_size)))
                    #np.roll(audio_block, -rollback)
                    audio_block[:,:] = np.nan
                    current_size = 0
                    current_analysed = 0
                # Copies new sample data into audio block
                audio_block[:,current_size:current_size+sample_chunk.shape[0]] = np.transpose(sample_chunk)
                current_size = current_size + sample_chunk.shape[0]
                sample_chunk = audio_input.get_nowait()
            except Empty:
                #frequency analysis
                working = current_analysed
                magnitude = np.full(shape=(2, int(analysis_size / 2) + 1), fill_value=np.nan)
                #analyse as many times as queue allows(is actually only once when on pc)
                while ((current_size - working) >= analysis_size):
                    sample_set = audio_block[:,working:working + analysis_size]
                    magnitude = np.abs(np.fft.rfft(sample_set))*0.1
                    for out in high_bandwidth_output:
                        out.put_nowait(magnitude)
                    working += int(analysis_size / frequency_overlap) 
                #after
                if (magnitude[0,0] != np.nan):
                    #put frequency tag back here later
                    less_magnitude = np.transpose(list(map(lambda x: list(map(lambda y: max(magnitude[y, x[0] - 1 : x[1]]), [0,1])), nums_to_take)))
                    low_bandwidth_output.put(("freq_anal", less_magnitude))
                current_analysed = working
                sample_chunk = audio_input.get()

def callback_w(audio_input):
    def callback(indata, frames, time, status):
        audio_input.put(indata)
    return callback