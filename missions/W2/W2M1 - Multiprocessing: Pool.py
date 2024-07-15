import multiprocessing
import time

def work_log(task):
    name, duration = task
    print(f"Process {name} waiting {duration} seconds")
    time.sleep(duration)
    print(f"Process {name} Finished.")

if __name__ == '__main__':
    tasks = [('A', 5), ('B', 2), ('C', 1), ('D', 3)]

    pool = multiprocessing.Pool(processes=4)
    pool.map(work_log, tasks)

    pool.close()
    pool.join()