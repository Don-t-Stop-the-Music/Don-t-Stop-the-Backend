"""
Integration tests
"""
import unittest
import soundfile as sf
from multiprocessing import Process, Queue
from freq_analyser import frequency_analyser
from utility import freq_to_index
import numpy as np


class IntegrationTests(unittest.TestCase):
    """
    Integration tests
    """

    def test_Sin440FrequencyValuesFile(self):
        """
        Tests that frequency analyser outputs valid 440hz frequency values using test sound file
        """
        data, fs = sf.read("testing/audio/440hz.wav", always_2d=True)
        high_bandwidth = Queue()

        bluetooth_in = Queue()
        audio_input = Queue()

        fap_1 = Process(target=frequency_analyser, args=(
            [high_bandwidth], bluetooth_in, audio_input))
        fap_1.start()

        for i in range(0, len(data)-1028, 1028):
            audio_input.put(data[i: i+1028])

        sample = high_bandwidth.get()

        self.assertLess(1, sample[0][freq_to_index(440, len(sample[1]))])
        self.assertGreater(1, sample[0][0] )

        fap_1.kill()


    def test_Sin440FrequencyValuesNumpy(self):
        """
        Tests that frequency analyser outputs valid 440hz frequency values using numpy array
        """

        high_bandwidth = Queue()

        bluetooth_in = Queue()
        audio_input = Queue()

        fap_1 = Process(target=frequency_analyser, args=(
            [high_bandwidth], bluetooth_in, audio_input))
        fap_1.start()

        sampleRate = 44100
        frequency = 440
        length = 5
        t = np.linspace(0, length, sampleRate * length)
        y = np.sin(frequency * 2 * np.pi * t)
        y = np.transpose(y)
        for i in range(0, len(y)-1028, 1028):
            audio_input.put(y[i: i+1028])

        sample = high_bandwidth.get()

        self.assertLess(1, sample[0][freq_to_index(440, len(sample[1]))])
        self.assertGreater(1, sample[0][0] )

        fap_1.kill()


if __name__ == '__main__':
    unittest.main()
