import multiprocessing
import time

# Tasks example
tasks = [
    ('A', 5),
    ('B', 2),
    ('C', 1),
    ('D', 3),
]
# Simulate using Pool
def work_log(task):
    name, duration = task
    print(f"Process {name} waiting {duration} seconds")
    time.sleep(duration)
    print(f"Process {name} Finished.")

if __name__ == "__main__":
    # Pool 2
    with multiprocessing.Pool(2) as pool:
        # Mapping
        pool.map(work_log, tasks)
