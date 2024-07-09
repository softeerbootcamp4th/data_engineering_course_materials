'''
multiprocessing을 사용하기 위한 프로그래밍 지침
https://docs.python.org/ko/3/library/multiprocessing.html#multiprocessing-programming
'''

from multiprocessing import Process, Queue, current_process
from time import sleep
import queue

def f(tasks_to_accomplish, tasks_that_are_done):
    try:
        while True:
            # task = tasks_to_accomplish.get() # 큐가 비지 않을 때까지 기다린 후 pop함 -> 종료 안 됨
            task = tasks_to_accomplish.get_nowait()
            print(f"Task no {task}")
            sleep(0.5)
            tasks_that_are_done.put((task, current_process().name))
    except queue.Empty:
        pass

if __name__ == '__main__':
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()

    for i in range(10):
        tasks_to_accomplish.put(i)

    processes = [Process(
        target=f,
        args=(tasks_to_accomplish, tasks_that_are_done),
        name=str(i) # 명시하지 않아도 자동으로 1부터 이름 매겨짐 
        ) for i in range(1, 5)
    ]

    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()

    while not tasks_that_are_done.empty():
        task, proc = tasks_that_are_done.get()
        print(f"Task no {task} is done by Process-{proc}")