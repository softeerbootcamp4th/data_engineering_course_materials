from multiprocessing import Process, Queue
import time
import queue

def worker(task_queue, done_queue, process_id):
    while True:
        try:
            task = task_queue.get_nowait()
        except queue.Empty:
            break
        else:
            print(f"Task no {task}")
            time.sleep(0.5)
            done_queue.put(f"Task no {task} is done by Process-{process_id}")

if __name__ == '__main__':
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()

    #10개 작업 tasks_to_accomplish 큐에 추가
    for task in range(10):
        tasks_to_accomplish.put(task)

    processes = []
    #프로세스 4개(1~5) 생성해서 워커 함수 실행
    for process_id in range(1, 5):
        process = Process(target=worker, args=(tasks_to_accomplish, tasks_that_are_done, process_id))
        processes.append(process)
        process.start()

    #모든 프로세스 작업 다 할때까지 대기
    for process in processes:
        process.join()

    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())
