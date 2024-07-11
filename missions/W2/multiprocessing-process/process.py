import random
import time
from multiprocessing import Process
import os


def print_continent(continent: str = 'Asia'):
    # print(os.getpid())
    # time.sleep(random.randint(0,  3))
    print(f'The name of continent is : {continent}')


if __name__ == '__main__':
    p1 = Process(target=print_continent)
    p1.start()
    p1.join()

    processes = [
        Process(target=print_continent, args=('America',)),
        Process(target=print_continent, args=('Europe',)),
        Process(target=print_continent, args=('Africa',)),
    ]
    for process in processes:
        process.start()

    for process in processes:
        process.join()

    for process in processes:
        if process.is_alive():
            print('프로세스가 완료되지 않은 채 끝났습니다.')
