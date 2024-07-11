import time
from multiprocessing import Pool

work = [
    ("A", 5), ("B", 2), ("C", 1), ("D", 3),
]
def work_log(task, cost):
    print("Process {} waiting {} seconds".format(task, cost))
    time.sleep(cost)
    print("Process {} Finished.".format(task))
    return task, cost


if __name__ == '__main__':
    with Pool(2) as p:
        p.starmap(work_log, work)
