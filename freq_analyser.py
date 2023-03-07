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
    # this queue buffers the raw audio data for use in analysis.
    audio_input = Queue()
    # set up the inputstream. give it callback function to put data into queue
    with sd.InputStream(device=DEVICE, callback=callback_w(audio_input)):
        # run function to perform frequency analysis on the queue.
        frequency_analyser(high_bandwidth_output,
                           low_bandwidth_output, audio_input)


def frequency_analyser(high_bandwidth_output, low_bandwidth_output, audio_input):
    """
    The frequency analyser process.
    Process sound in and fourier transform, downsample for other processes
    Parameters:
        high_bandwidth_output (Queue[]): A list of queues to place the full fourier array
        low_bandwidth_output (Queue): A queue to place the downsampled fourier array
        audio_input (Queue): A queue of samples
    """
    # the maximum number of samples to be included in the array at any given time
    max_size = ANALYSIS_SIZE * 40
    # keeps a pointer of where the latest data is
    current_size = 0
    # stores the data to be analysed once removed from the queue.
    audio_block = np.full(shape=(2, max_size), fill_value=np.nan)
    # pointer to the first piece of data to be used in the next analysis.
    current_analysed = 0
    # used for downsampling according to how it would be displayed on a graph.
    logspace = np.logspace(0, np.log10(
        (ANALYSIS_SIZE / 2)), BLUETOOTH_SAMPLES, dtype=int)

    # fetch from queue.
    sample_chunk = audio_input.get()
    # while there is data in the queue, keep getting data.
    while True:
        try:
            # Checks if buffer already full, then does rollback.
            # gets rid of all used data.
            if current_size + sample_chunk.size > max_size:
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
            # default data to correct size to prevent errors.
            magnitude = np.full(
                shape=(2, int(ANALYSIS_SIZE / 2) + 1), fill_value=np.nan)
            # bool to check if data has actually been analysed.
            magnituded = False
            # analyse as many times as queue allows(is actually only once when on pc)
            while (current_size - working) >= ANALYSIS_SIZE:
                # a subset of the data, enough to get good results from 20Hz
                sample_set = audio_block[:,
                                         working:working + ANALYSIS_SIZE]
                # does a fast fourier analysis on the sample data
                magnitude = np.abs(np.fft.rfft(sample_set)) * 0.1
                magnituded = True
                # put the data into the high resolution queue for further analysis
                for out in high_bandwidth_output:
                    out.put_nowait(magnitude)
                # update the pointer to where the analysis should start next.
                working += int(ANALYSIS_SIZE / FREQUENCY_OVERLAP)
            # if something changed add the most recent to the bluetooth queue
            if magnituded:
                # complicated line: this takes the analysed data, splits it into chunks based on the logspace,
                # takes the max of each of the chunks and reformats it to be the right shape.
                less_magnitude = np.transpose(list(map(lambda x: list(
                    map(lambda y: max(magnitude[y, x[0] - 1: x[1]]), [0, 1])), np.transpose(
                    np.array([logspace, np.append(logspace[1:], logspace[-1])])))))
                # put the downsampled data in the bluetooth queue.
                low_bandwidth_output.put(
                    ("frequency", less_magnitude.tolist()))
            # update where analysis should be looking next.
            current_analysed = working
            # block
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
