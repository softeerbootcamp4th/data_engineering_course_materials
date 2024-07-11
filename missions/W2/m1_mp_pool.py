'''
multiprocessing을 사용하기 위한 프로그래밍 지침
https://docs.python.org/ko/3/library/multiprocessing.html#multiprocessing-programming
'''

from multiprocessing import Pool
from time import sleep

class Task:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
    
    def start(self):
        print(f"Process {self.name} waiting {self.duration} seconds.")
        sleep(self.duration)
        print(f"Process {self.name} finished.")
    
# lambda 함수로 f를 선언하면 작동하지 않는다
# lambda는 serializable(피클 가능)하지 않기 때문. 명시적으로 선언된 함수의 사용 필요.
def f(task: Task):
    task.start()

if __name__ == '__main__':
    t1 = Task('A', 5)
    t2 = Task('B', 2)
    t3 = Task('C', 1)
    t4 = Task('D', 3)
    tasks = [t1, t2, t3, t4]

    with Pool(2) as p:
        p.map(f, tasks)