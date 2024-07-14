import time
from multiprocessing import Queue, Process, current_process

NUM_TASKS = 10
NUM_PROCESSES = 4

def target_func(tasks_to_accomplish, tasks_that_are_done):
    while True:
        try:
            val = tasks_to_accomplish.get_nowait()
        except Exception as e: 
            break   
        else:
            print(f"Task no {val}")
            time.sleep(0.5)
            tasks_that_are_done.put(f"Task no {val} is done by {current_process().name}")
    return

if __name__=="__main__":
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    procs = []
    
    for i in range(NUM_TASKS):
        tasks_to_accomplish.put(i)
    
    for i in range(NUM_PROCESSES):
        proc = Process(name=f'Process-{i+1}', target=target_func, args=(tasks_to_accomplish, tasks_that_are_done,))
        procs.append(proc)
        procs[i].start()
        
    # Wait for all processes to finish.
    for proc in procs:
        proc.join()
        
    for i in range(NUM_TASKS):
        msg = tasks_that_are_done.get()
        print(msg)