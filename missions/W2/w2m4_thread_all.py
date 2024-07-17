import time
import queue
from multiprocessing import Queue, Process, current_process


def run_task(
    tasks_to_accomplish: Queue,
    tasks_that_are_done: Queue
):
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
        except queue.Empty:
            """Raise Exception When Queue is Empty"""

            break
        else:
            print(task)
            tasks_that_are_done.put(
                task + ' is done by ' + current_process().name)
            time.sleep(.5)


if __name__ == '__main__':
    num_tasks, num_processes = 10, 4
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    processes = []

    # put tasks into tasks_to_accomplish
    for task_id in range(num_tasks):
        tasks_to_accomplish.put("Task no " + str(task_id))

    # execute tasks
    for proc_id in range(num_processes):
        processes.append(
            Process(
                target=run_task,
                args=(tasks_to_accomplish, tasks_that_are_done)
            )
        )
        processes[-1].start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # print results
    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())
