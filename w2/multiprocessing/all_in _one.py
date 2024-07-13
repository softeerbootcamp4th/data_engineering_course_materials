# all in one
# 작업 분배

import multiprocessing
import time 

def do(tasks_to_accomplish, tasks_that_are_done):
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
        except multiprocessing.queues.Empty:
            break
        else:
            print(f"{task}")
            #print(f'{multiprocessing.current_process().name}')
            time.sleep(0.5)
            tasks_that_are_done.put(f"{task} is done by {multiprocessing.current_process().name}")    

if __name__ == "__main__":
    # 작업 생성
    tasks = [f"Task no {x}" for x in range(10)]

    # 큐 생성
    tasks_to_accomplish = multiprocessing.Queue()
    tasks_that_are_done = multiprocessing.Queue()

    # 작업을 큐에 할당
    for task in tasks:
        tasks_to_accomplish.put(task)

    # 프로세스 생성 (4개)
    processes = []
    for _ in range(4):
        process = multiprocessing.Process(target=do, args=(tasks_to_accomplish, tasks_that_are_done))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()

    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())