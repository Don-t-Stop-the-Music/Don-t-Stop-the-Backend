"""
Frequency Analyser
takes in the sound input, performs fourier transform and downsamples to queues.
"""
import math
from queue import Queue
from queue import Empty
import numpy as np
import sounddevice as sd
from config import DEVICE, BLUETOOTH_SAMPLES, SAMPLE_RATE, LOWEST_FREQUENCY, FREQUENCY_OVERLAP

ANALYSIS_SIZE = math.ceil(SAMPLE_RATE / LOWEST_FREQUENCY) * 2

def freq_analyser_proc(high_bandwidth_output, low_bandwidth_output):
    '''The frequency analyser process. 
    Process sound in and fourier transform, downsample for other processes
        Parameters:
            high_bandwidth_output (Queue[]): A list of queues to place the full fourier array
            low_bandwidth_output (Queue): A queue to place the downsampled fourier array
    '''

    audio_input = Queue()

    print("freq_analyser online")
    with sd.InputStream(device=DEVICE, callback=callback_w(audio_input)):
        frequency_analyser(high_bandwidth_output, low_bandwidth_output, audio_input)


def frequency_analyser(high_bandwidth_output, low_bandwidth_output, audio_input):
    """
    The frequency analyser process.
    Process sound in and fourier transform, downsample for other processes
    Parameters:
        high_bandwidth_output (Queue[]): A list of queues to place the full fourier array
        low_bandwidth_output (Queue): A queue to place the downsampled fourier array
        audio_input (Queue): A queue of samples
    """
    max_size = ANALYSIS_SIZE * 40
    current_size = 0
    audio_block = np.full(shape=(2, max_size), fill_value=np.nan)
    current_analysed = 0
    logspace = np.logspace(0, np.log10((ANALYSIS_SIZE / 2)), BLUETOOTH_SAMPLES, dtype=int)

    sample_chunk = audio_input.get()
    while True:
        try:
            # Checks if buffer already full
            if current_size + sample_chunk.size > max_size:
                print("rollback!")
                audio_block[:, :] = np.nan
                current_size = 0
                current_analysed = 0
            # Copies new sample data into audio block
            audio_block[:, current_size:current_size +
                        sample_chunk.shape[0]] = np.transpose(sample_chunk)
            current_size = current_size + sample_chunk.shape[0]
            sample_chunk = audio_input.get_nowait()
        except Empty:
            # frequency analysis
            working = current_analysed
            magnitude = np.full(
                shape=(2, int(ANALYSIS_SIZE / 2) + 1), fill_value=np.nan)
            magnituded = False
            # analyse as many times as queue allows(is actually only once when on pc)
            while (current_size - working) >= ANALYSIS_SIZE:
                sample_set = audio_block[:,
                                            working:working + ANALYSIS_SIZE]
                magnitude = np.abs(np.fft.rfft(sample_set)) * 0.1
                magnituded = True
                for out in high_bandwidth_output:
                    out.put_nowait(magnitude)
                working += int(ANALYSIS_SIZE / FREQUENCY_OVERLAP)
            # if something changed add the most recent to the bluetooth queue
            if magnituded:
                less_magnitude = np.transpose(list(map(lambda x: list(
                    map(lambda y: max(magnitude[y, x[0] - 1: x[1]]), [0, 1])), np.transpose(
                    np.array([logspace, np.append(logspace[1:], logspace[-1])])))))
                low_bandwidth_output.put(
                    ("frequency", less_magnitude.tolist()))
            current_analysed = working
            sample_chunk = audio_input.get()

def callback_w(audio_input):
    '''Called whenever new information comes into the sound input.
    Places the data coming in into the audio input queue.
        Parameters:
            audio_input (Queue): a queue to put the raw sound in.'''
    # pylint: disable-next=unused-argument
    def callback(indata, frames, time, status):
        audio_input.put(indata)
    return callback
