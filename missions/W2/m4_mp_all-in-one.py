'''
multiprocessing을 사용하기 위한 프로그래밍 지침
https://docs.python.org/ko/3/library/multiprocessing.html#multiprocessing-programming
'''

from multiprocessing import Process, Queue, current_process
from time import sleep
import queue

MAX_PROCESSES = 4

def f(tasks_to_do, tasks_done):
    while True:
        try:
            task = tasks_to_do.get_nowait()
            print(f"Task no {task}")
            tasks_done.put((task, current_process().name))
        except queue.Empty:
            break
        else:
            sleep(0.5)

if __name__ == '__main__':
    tasks_to_do = Queue()
    tasks_done = Queue()

    for i in range(10):
        tasks_to_do.put(i)

    processes = []
    for _ in range(MAX_PROCESSES):
        processes.append(Process(target=f, args=(tasks_to_do, tasks_done)))
        processes[-1].start()
    for proc in processes:
        proc.join()

    while not tasks_done.empty():
        task, proc = tasks_done.get()
        print(f"Task no {task} is done by Process-{proc}")