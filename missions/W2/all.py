import time
from multiprocessing import Queue, Process

class Task:
    def __init__(self, task_no: int):
        self.process = None
        self.task_no = task_no

    def __str__(self):
        return f'Task no {self.task_no}'

    def set_process(self, process_no: int):
        self.process = process_no

    def done(self):
        print(self.__str__() + f" is done by Process-{self.process}")


def work(start_queue: Queue, end_queue: Queue, process_no: int):
    while not start_queue.empty():
    # for task in iter(start_queue.get, 'STOP'):
        while True:
            try:
                task = start_queue.get_nowait()
                print(task)
                end_queue.put_nowait(task)
                task.set_process(process_no)
                time.sleep(0.5)
                break
            except:
                continue



if __name__ == '__main__':
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()

    for i in range(10):
        tasks_to_accomplish.put(Task(i))

    processes = []
    for i in range(4):
        processes.append(Process(target=work, args=(tasks_to_accomplish, tasks_that_are_done, i)))

    for process in processes:
        process.start()

    # Tell child processes to stop
    # for i in range(4):
    #     tasks_to_accomplish.put('STOP')

    for process in processes:
        process.join()

    N = 10
    while N > 0:
        try:
            tasks_that_are_done.get_nowait().done()
            N -= 1
            if N == 0:
                break
        except:
            continue
