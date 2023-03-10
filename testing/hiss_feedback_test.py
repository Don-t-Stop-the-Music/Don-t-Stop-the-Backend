"""
Feedback/Hiss tests
"""
import unittest
from multiprocessing import Process, Manager
import numpy as np

from feedback_hiss_analyser import feed_hiss_analyser_proc


class FeedbackHissTests(unittest.TestCase):
    """
    Feedback/Hiss tests
    """

    @classmethod
    def tearDownClass(cls):
        for process in cls.processes:
            process.kill()

    processes = []

    def test_hiss_noisy_signal_gives_positive(self):
        """
        Gives a set of frequencies that is noisy, tests if noise is there.
        """
        data = np.full((2, 2206), 16)
        data[0][44] += 50
        high_bandwidth = Manager().Queue()
        for _ in range(20):
            high_bandwidth.put(data)

        feedback_out = Manager().Queue()

        hiss = Process(target=feed_hiss_analyser_proc, args=(
            high_bandwidth, feedback_out))
        hiss.daemon = True
        hiss.start()

        # Required to clean up process after unit test
        FeedbackHissTests.processes.append(hiss)

        sample = feedback_out.get()

        self.assertEqual(sample[0], "hiss")
        self.assertEqual(sample[1][0], True)

    def test_hiss_clean_signal_gives_negative(self):
        """
        Gives a set of frequencies that has noise below the threshold, tests if noise is there.
        """
        data = np.full((2, 2206), 1)
        data[0][44] += 50
        high_bandwidth = Manager().Queue()
        for _ in range(20):
            high_bandwidth.put(data)

        feedback_out = Manager().Queue()

        hiss = Process(target=feed_hiss_analyser_proc, args=(
            high_bandwidth, feedback_out))
        hiss.start()

        # Required to clean up process after unit test
        FeedbackHissTests.processes.append(hiss)

        sample = feedback_out.get()

        self.assertEqual(sample[0], "hiss")
        self.assertEqual(sample[1][0], False)



if __name__ == '__main__':
    unittest.main()
