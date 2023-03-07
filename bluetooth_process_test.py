"""
Bluetooth process test
sends test data over bluetooth
"""
from multiprocessing import Process, Queue
from time import sleep
from bluetooth_process import bluetooth_proc


def data_simulator(data_stream):
    """
    data simulator
    puts sample data into the data stream to be sent over bluetooth
    """

    while True:

        sleep(1)
        data_stream.put(("frequency", [10,20,30,40,50,60,70,80]))
        data_stream.put(("hiss", [False,False]))

        sleep(1)
        data_stream.put(("frequency", [80,70,60,50,40,30,20,10]))
        data_stream.put(("hiss", [True,True]))


if __name__ == "__main__":

    bluetooth_in = Queue()
    simulator_1 = Process(target=data_simulator, args=(bluetooth_in,))
    simulator_1.start()
    bluetooth_1 = Process(target=bluetooth_proc, args=(bluetooth_in,))
    bluetooth_1.start()
    