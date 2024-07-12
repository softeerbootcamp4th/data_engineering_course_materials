# Pool

import multiprocessing
import time

tasks = [('A', 5), ('B', 2), ('C', 1), ('D', 3)]

def do(task):
    print(f"Process {task[0]} waiting {task[1]} seconds")
    time.sleep(task[1])
    print(f"Process {task[0]} Finished")

if __name__ == "__main__":
    #tasks.sort(key  = lambda x: x[1])
    with multiprocessing.Pool(2) as pool:
        pool.map(do, tasks)
