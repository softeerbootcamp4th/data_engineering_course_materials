from multiprocessing import Lock, Process, Queue, current_process
import time
import queue # imported for using queue.Empty exception
import random

'''
이 연습 문제는 10개의 작업을 4개의 프로세스가 병렬적으로 수행하는 문제입니다.
부모 프로세스는 자식 프로세스들과 공유 가능한 Queue를 생성하여 정보를 공유합니다.
자식 프로세스는 공유된 큐에서 데이터를 병렬적으로 처리합니다.

multiprocessing 모듈의 Queue는 critical section에 대한 처리가 되어있습니다
queue에서 데이터를 꺼내는 작업은 FIFO 순서이지만, queue에서 데이터를 꺼낸 순서가
그 데이터를 처리하여 작업을 마친 순서임은 보장할 수 없습니다
'''
def do_job(tasks_to_accomplish, tasks_that_are_done):
    while True:
        try:
            '''
            try to get task from the queue. get_nowait() function will 
            raise queue.Empty exception if the queue is empty. 
            queue(False) function would do the same task also.
            '''
            task = tasks_to_accomplish.get_nowait()
            # context change에 따른 출력 순서를 화인하기 위한 time.sleep
            # time.sleep(random.randrange(1,10))
        except queue.Empty:

            break
        else:
            '''
            if no exception has been raised, add the task completion 
            message to task_that_are_done queue
            '''
            print(task)
            # context change에 따른 출력 순서를 화인하기 위한 time.sleep
            time.sleep(random.randrange(1,10))
            tasks_that_are_done.put(task + ' is done by ' + current_process().name)
            
    return True


def main():
    number_of_task = 10
    number_of_processes = 4
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    processes = []

    # put tasks(string data) into Queue
    for i in range(number_of_task):
        tasks_to_accomplish.put("Task no " + str(i))

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=do_job, args=(tasks_to_accomplish, tasks_that_are_done))
        processes.append(p)
        p.start()
    
    # completing process
    for p in processes:
        p.join()

    # print the output
    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())

    return True


if __name__ == '__main__':
    main()
    