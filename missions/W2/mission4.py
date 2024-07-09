import time
from multiprocessing import Pool, Queue, Process, current_process, Manager, JoinableQueue

NUM_TASK = 10
NUM_PROCESSES = 4

def target_func(tasks_to_accomplish, tasks_that_are_done):
    try:
        while True:
            val = tasks_to_accomplish.get_nowait()
            print(f"Task no {val}")
            time.sleep(0.5)
            tasks_that_are_done.put(f"Task no {val} is done by {current_process().name}")
    except Exception as e: 
        pass          
    return

if __name__=="__main__":
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    procs = []
    
    for i in range(NUM_TASK):
        tasks_to_accomplish.put(i)
    
    for i in range(NUM_PROCESSES):
        proc = Process(name=f'Process-{i+1}', target=target_func, args=(tasks_to_accomplish, tasks_that_are_done,))
        procs.append(proc) 
        procs[i].start()
                
    # Wait for all processes to finish.
    for proc in procs:
        proc.join()
        
    for i in range(NUM_TASK):
        msg = tasks_that_are_done.get()
        print(msg)