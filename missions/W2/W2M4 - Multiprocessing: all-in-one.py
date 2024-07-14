import multiprocessing
import time

def worker(tasks_to_accomplish, tasks_that_are_done):
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
        except multiprocessing.queues.Empty:
            break
        else:
            print(f"{task}")
            time.sleep(0.5)  
            tasks_that_are_done.put(f"{task} is done by {multiprocessing.current_process().name}")
    return True

if __name__ == "__main__":
    tasks_to_accomplish = multiprocessing.Queue()
    tasks_that_are_done = multiprocessing.Queue()
    
    for i in range(10):
        tasks_to_accomplish.put(f"Task no {i}")

    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=worker, args=(tasks_to_accomplish, tasks_that_are_done))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()

    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())