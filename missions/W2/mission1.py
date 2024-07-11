import time
from multiprocessing import Pool

NUM_CORES = 2
TASKS = [("A", 5), ("B", 2), ("C", 1), ("D", 3)]

def work_log(task):
    name, duration = task
    print(f"Process {name} waiting {duration} seconds")
    time.sleep(duration)
    print(f"Process {name} Finished.")
    return None

if __name__=="__main__":
    pool = Pool(NUM_CORES)
    pool.map(work_log, TASKS)
    pool.close()
    pool.join()