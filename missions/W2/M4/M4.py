import time
from multiprocessing import Queue, Process, Pool

NUM = 10
NUM_OF_TASKS = NUM

NUM_OF_PROCESS = 4


def process_task(tasks, results, i):
    task = tasks.get()
    # check if no further values are expected
    while task is not None:
        print('Task no {}'.format(task))
        time.sleep(0.5)
        results.put((task, i))
        task = tasks.get()
    tasks.put(None)
    # terminate the process


if __name__ == '__main__':
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    taskers = []
    for i in range(NUM_OF_TASKS):
        tasks_to_accomplish.put(i)
    tasks_to_accomplish.put(None)
    for i in range(NUM_OF_PROCESS):
        proc = Process(target=process_task, args=(tasks_to_accomplish, tasks_that_are_done, i))
        taskers.append(proc)
        proc.start()
    for i in range(NUM_OF_PROCESS):
        taskers[i].join()
    for _ in range(NUM_OF_TASKS):
        task, proc_id = tasks_that_are_done.get()
        print("Task no {} is done by Process-{}".format(task, proc_id))
