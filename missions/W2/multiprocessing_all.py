import time
from multiprocessing import Process, Queue, current_process

def worker(tasks_to_accomplish: Queue, tasks_that_are_done: Queue):
    try:
        while True:
            task = tasks_to_accomplish.get_nowait() # eqaul to 'get(False)'

            print(f"Task no {task}")

            time.sleep(0.5)
            log = f"Task no {task} is done by Process-{current_process().name}"

            tasks_that_are_done.put(log)
    except Exception as e:
        return

if __name__ == "__main__":
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()

    num_processes = 4

    # Add tasks to the queue
    for task in range(10):
        tasks_to_accomplish.put(task)

    processes = [Process(
            name=str(process_number), 
            target=worker, 
            args=(tasks_to_accomplish, tasks_that_are_done)
        ) 
        for process_number in range(1, num_processes + 1)
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    while not tasks_that_are_done.empty():
        log = tasks_that_are_done.get()
        print(log)
