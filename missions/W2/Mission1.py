import multiprocessing
import time

tasks = [
    ('A', 5),
    ('B', 2),
    ('C', 1),
    ('D', 3)
]

def work_log(task):
    name, duration = task
    print(f"Process {name} waiting {duration} seconds")
    time.sleep(duration)
    print(f"Process {name} finished")

if __name__ == '__main__':
    pool = multiprocessing.Pool(2)
    
    pool.map(work_log, tasks)
    
    pool.close()
    pool.join()