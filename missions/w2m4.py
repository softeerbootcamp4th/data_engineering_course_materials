
from multiprocessing import Lock, Process, Queue, current_process
import time
import queue # imported for using queue.Empty exception


def do_job(tasks_to_accomplish, tasks_that_are_done):
    while True:
        try:
            '''
                대기열에서 작업을 가져옴. get_nowait () 함수가
                queue를 올림. 대기열이 비어 있으면 empty 예외
                queue(False) 함수도 동일한 작업을 수행
            '''
            task = tasks_to_accomplish.get_nowait()
        except queue.Empty:

            break
        else:
            '''
                예외가 발생하지 않은 경우 작업 완료를 추가
                task_that_are_done 대기열에 메시지를 전달
            '''
            print(task)
            tasks_that_are_done.put(task + ' is done by ' + current_process().name)
            time.sleep(.5) #작업 실행 시간을 시뮬레이션합니다.
    return True


def main():
    number_of_task = 10
    number_of_processes = 4
    tasks_to_accomplish = Queue() #tasks_to_accomplish에서 동시에 작업을 검색하고, 이를 실행
    tasks_that_are_done = Queue() # 결과를 저장하는 4개의 프로세스를 생성
    processes = []

    for i in range(number_of_task):
        tasks_to_accomplish.put("Task no " + str(i))

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=do_job, args=(tasks_to_accomplish, tasks_that_are_done))
        #각 프로세스는 현재 실행 중인 작업을 인쇄하고 완료 메시지를 tasks_that_are_done에 추가
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join() #모든 프로세스가 작업을 완료하고 동기화되는지 확인

    # print the output
    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())
    #모든 프로세스가 완료된 후 tasks_that_are_done에 저장된 완료 메시지를 인쇄
    return True


if __name__ == '__main__':
    main()