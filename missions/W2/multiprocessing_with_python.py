import time
import queue
from multiprocessing import Manager, Pool


NUM_WORKERS = 4


def work(worker_id, tasks_to_accomplish, tasks_that_are_done):
    name = str(worker_id)

    while True:
        try:
            item = tasks_to_accomplish.get_nowait()
        except ValueError:
            print(f"Error: Process {name} failed to acess the queue")
            return
        except queue.Empty:
            return
        time.sleep(0.5)
        tasks_that_are_done.put(item)
        print(f"Task no {str(item)} is done by Process-{name}")


if __name__ == '__main__':
    with Manager() as manager:
        tasks_to_accomplish = manager.Queue()
        tasks_that_are_done = manager.Queue()

        for i in range(10):
            tasks_to_accomplish.put(i)
            print(f"Task no {str(i)}")

        with Pool(NUM_WORKERS) as p:
            p.starmap(work, [(i, tasks_to_accomplish, tasks_that_are_done) for i in range(NUM_WORKERS)])

