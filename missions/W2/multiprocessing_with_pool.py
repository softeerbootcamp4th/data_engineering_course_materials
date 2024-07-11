import time
from multiprocessing import Pool


def work_log(name, waiting_time):
    print(f'Process {name} waiting {str(waiting_time)} seconds')
    time.sleep(waiting_time)
    print(f'Process {name} Finished.')


if __name__ == '__main__':
    work = [('A', 5), ('B', 2), ('C', 1), ('D', 3)]
    
    with Pool(2) as p:
        p.starmap(work_log, work)
