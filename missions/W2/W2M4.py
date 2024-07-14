import multiprocessing
import time

def accomplish_worker(tasks_to_accomplish, tasks_that_are_done, process_num):
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
            print(f"Task no {task}")
            time.sleep(0.5)
            tasks_that_are_done.put((task, process_num))
        except multiprocessing.queues.Empty:
            break

def Done_Work_Print(tasks_that_are_done):
    while True:
        try:
            task_process = tasks_that_are_done.get_nowait()
            print(f"Task no {task_process[0]} is done by Process-{task_process[1]}")
        except multiprocessing.queues.Empty:
            break


if __name__ == '__main__':
    NUM_TASKS = 10
    NUM_PROCESSES = 4

    tasks_to_accomplish = multiprocessing.Queue()
    tasks_that_are_done = multiprocessing.Queue()

    # 큐에 맞는 process 할당 후 추가
    for i in range(NUM_TASKS):
        tasks_to_accomplish.put(i)

    processes = []
    for i in range(NUM_PROCESSES):
        process = multiprocessing.Process(target=accomplish_worker, args=(tasks_to_accomplish, tasks_that_are_done, i+1))
        # print(i, '!!!')
        processes.append(process)
        # print(processes, '@@@@@@@@')
        process.start()
    # print('#############')
    # Ensure all processes have finished
    for process in processes:
        process.join()
        # print("$$$$$$$$$")

    Done_Work_Print(tasks_that_are_done)
