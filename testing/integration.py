"""
Integration tests
"""
import unittest
import soundfile as sf
from multiprocessing import Process, Queue
from freq_analyser import frequency_analyser
#from utility import freq_to_index
import numpy as np

class IntegrationTests(unittest.TestCase):
    """
    Integration tests
    """

    def test_Sin440FrequencyValues(self):
        """
        Tests that frequency analyser outputs valid 440hz frequency values
        """
        data, fs = sf.read("audio/Sine_wave_440.ogg", always_2d=True)

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

        for d in y:
            audio_input.put(np.array([d, d]))

        sample = high_bandwidth.get()
        sample = high_bandwidth.get()
        sample = high_bandwidth.get()
        sample = high_bandwidth.get()

        #print(freq_to_index(440, len(sample[1])))
        print(sample[0])
       # print(sample[0][freq_to_index(440, len(sample[1]))+1])
        #print(sample[0][freq_to_index(440, len(sample[1]))-1])

        #self.assertLess(1, sample[0][freq_to_index(440, len(sample[1]))])
        #self.assertGreater(1, sample[0][0] )


if __name__ == '__main__':
    unittest.main()
