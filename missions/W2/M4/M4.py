import queue
import time
from multiprocessing import Queue, Process, Pool, current_process

NUM_OF_TASKS = 10
NUM_OF_PROCESS = 4


def process_task(tasks, results):
    while True:
        try:
            task = tasks.get_nowait()
        except queue.Empty:
            print("no more tasks")
            return
        else:
            print('Task no {}'.format(task))
            time.sleep(0.5)
            results.put((task, current_process().name))


# terminate the process


if __name__ == '__main__':
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    taskers = []
    for i in range(NUM_OF_TASKS):
        tasks_to_accomplish.put(i)
    for i in range(NUM_OF_PROCESS):
        proc = Process(name=str(i), target=process_task, args=(tasks_to_accomplish, tasks_that_are_done))
        taskers.append(proc)
        proc.start()
    for i in range(NUM_OF_PROCESS):
        taskers[i].join()

    try:
        while True:
            task, proc_id = tasks_that_are_done.get_nowait()
            print("Task no {} is done by Process-{}".format(task, proc_id))
    except queue.Empty:
        pass
