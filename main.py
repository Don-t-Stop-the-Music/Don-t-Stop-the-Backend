from multiprocessing import Process, Queue, Manager
from queue import Empty
from time import sleep
from sound_input import sound_input_proc
from freq_analyser import freq_analyser_proc
def f(q):
    item = q.get()
    while True:
        try:
            item = q.get_nowait()
        except Empty:
            print(item)
            sleep(2)
            item = q.get()
            

if __name__ == '__main__':
    freq_q_1 = Queue()

    analysers = [[freq_q_1]]

    fp = Process(target=freq_analyser_proc, args=(freq_q_1, ))
    fp.start()

    p = Process(target=sound_input_proc, args=(analysers,))
    p.start()
    p.join()