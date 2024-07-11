import time
from multiprocessing.dummy import Pool


# Task Execution Function
def work_log(task_data):
    task, time_to_sleep = task_data
    if time_to_sleep > 1:
        print(f"Process {task} waiting {time_to_sleep} seconds.")
    else:
        print(f"Process {task} waiting {time_to_sleep} second.")
    time.sleep(time_to_sleep)
    print(f"Process {task} finished.")
    return None


if __name__ == '__main__':
    # Task Definition
    tasks = [
        ["task1", 5],
        ["task2", 2],
        ["task3", 1],
        ["task4", 3]
    ]

    # Worker Pool Setup / Run with Concurrency
    p = Pool(4)
    p.map(work_log, tasks)
    p.close()
