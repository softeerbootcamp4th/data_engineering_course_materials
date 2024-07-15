import time
from multiprocessing import Pool


def work_log(item):
    key, value = item
    print(f"Process {key} is waiting {value} seconds")
    time.sleep(value)
    print(f"Process {key} Finished.")


def main():
    processes = {"A": 5, "B": 2, "C": 1, "D": 3}

    # start = int(time.time())
    # list(map(work_log, processes.items()))
    # print("*** normal run time(sec) :", int(time.time()) - start)
    # print()

    start_pool = int(time.time())
    num_cores = 4
    pool = Pool(num_cores)
    pool.map(work_log, processes.items())
    print("*** pool run time(sec) :", int(time.time()) - start_pool)


if __name__ == "__main__":
    main()
