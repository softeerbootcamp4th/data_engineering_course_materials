import time
from multiprocessing import Pool


class Task:
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration


def work_log(task: Task):
    print('Process ' + task.name + ' waiting ' + str(task.duration) + ' seconds')
    time.sleep(task.duration)
    print('Process ' + task.name + ' Finished')


if __name__ == '__main__':
    task_queue = [
        Task('A', 5),
        Task('B', 2),
        Task('C', 1),
        Task('D', 3),
    ]
    with Pool(4) as p:
        p.map(work_log, task_queue)