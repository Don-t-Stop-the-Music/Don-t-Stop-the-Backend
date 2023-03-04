"""
Utility Functions
"""
from config import SAMPLE_RATE

def index_to_freq(arr, samples):
    """
    Converts sample array index into frequencies
    Parameters:
          arr (List): Input list of indices
          samples (int): Number of samples in full freq array
    Returns:
          int List: array of frequencies
    """
    return arr * (SAMPLE_RATE/2) / samples


def freq_to_index(freq, samples):
    """
    Converts sample frequencies into index array
    Parameters:
          freq: Input frequency
          samples (int): Number of samples in full freq array
    Returns:
          int: array index
    """
    return int(freq * samples / (SAMPLE_RATE/2))
