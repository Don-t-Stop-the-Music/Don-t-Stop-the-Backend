"""
Integration tests
"""
import unittest
from multiprocessing import Process, Queue, Manager
import numpy as np
import soundfile as sf

from freq_analyser import frequency_analyser
from utility import freq_to_index


class IntegrationTests(unittest.TestCase):
    """
    Integration tests
    """

    @classmethod
    def tearDownClass(cls):
        for process in cls.processes:
            process.kill()

    processes = []

    def test_sin440_frequency_values_file(self):
        """
        Tests that frequency analyser outputs valid 440hz frequency values using test sound file
        """
        data, _ = sf.read("testing/audio/440hz.wav", always_2d=True)
        high_bandwidth = Manager().Queue()

        bluetooth_in = Manager().Queue()
        audio_input = Manager().Queue()

        fap_1 = Process(target=frequency_analyser, args=(
            [high_bandwidth], bluetooth_in, audio_input))
        fap_1.start()
        IntegrationTests.processes.append(fap_1)

        for i in range(0, len(data)-1028, 1028):
            audio_input.put(data[i: i+1028])

        sample = high_bandwidth.get()

        self.assertLess(1, sample[0][freq_to_index(440, len(sample[1]))])
        self.assertGreater(1, sample[0][0])


    def test_sin440_frequency_values_numpy(self):
        """
        Tests that frequency analyser outputs valid 440hz frequency values using numpy array
        """

        high_bandwidth = Manager().Queue()

        bluetooth_in = Manager().Queue()
        audio_input = Manager().Queue()

        fap_1 = Process(target=frequency_analyser, args=(
            [high_bandwidth], bluetooth_in, audio_input))
        fap_1.start()
        IntegrationTests.processes.append(fap_1)

        sample_rate = 44100
        frequency = 440
        length = 5
        time = np.linspace(0, length, sample_rate * length)
        data = np.sin(frequency * 2 * np.pi * time)
        data = np.transpose(data)
        for i in range(0, len(data)-1028, 1028):
            audio_input.put(data[i: i+1028])

        sample = high_bandwidth.get()

        self.assertLess(1, sample[0][freq_to_index(440, len(sample[1]))])
        self.assertGreater(1, sample[0][0])


    
if __name__ == '__main__':
    unittest.main()
