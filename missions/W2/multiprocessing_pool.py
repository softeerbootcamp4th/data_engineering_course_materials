import time
from multiprocessing import Pool

def work_log(work: dict[str, int]):
    print(f"Process {work['name']} waiting {work['duration']} seconds")
    time.sleep(work['duration'])
    print(f"Process {work['name']} Finished.")

if __name__ == '__main__':
    work_list = [
        {'name': 'A', 'duration': 5},
        {'name': 'B', 'duration': 3},
        {'name': 'C', 'duration': 2},
        {'name': 'D', 'duration': 1}
    ]
    with Pool(2) as pool:
        pool.map(work_log, work_list)