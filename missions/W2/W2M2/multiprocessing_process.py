import time
from multiprocessing import Process


def work_log(continent='Asia'):
    print('The name of continent is : ', continent)


def main():
    args = ["America", "Europe", "Africa"]
    start = int(time.time())
    
    procs = []
    proc = Process(target=work_log)
    procs.append(proc)
    proc.start()
    for arg in args:
        proc = Process(target=work_log, args=(arg,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
    print("*** run time(sec) :", int(time.time()) - start)


if __name__ == "__main__":
    main()
