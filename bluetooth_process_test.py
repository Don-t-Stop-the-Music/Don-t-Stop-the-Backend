from bluetooth_process import bluetooth_proc
from multiprocessing import Process, Queue
from time import sleep
import numpy as np

def data_simulator(data_stream):

    ##still need to simulate bluetooth data

    while True:
        sleep(1)
        data_stream.put(["frequency", 0])
    
    pass


if __name__ == "__main__":

    bluetooth_in = Queue()

    simulator_1 = Process(target=data_simulator, args=(bluetooth_in,))
    simulator_1.start()
    
    bluetooth_1 = Process(target=bluetooth_proc, args=(bluetooth_in,))
    bluetooth_1.start()