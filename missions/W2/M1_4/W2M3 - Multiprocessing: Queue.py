from multiprocessing import Queue

'''
이 연습에서는 선입선출 자료구조인 큐에 색상을 삽입한 후 꺼내어 출력합니다
다만 이때 쓰인 Queue는 multiprocessing 모듈의 클래스로서
멀티 프로세싱을 위한, 즉 자원은 공유하기 위한 큐 입니다.
프로세스는 각각 독립적인 프로세스 메모리 영역을 가지고 있습니다. 따라서 자원을 공유하지 않습니다.
'''

colors = ['red', 'green', 'blue', 'black']
cnt = 1
# instantiating a queue object
queue = Queue()
print('pushing items to queue:')
for color in colors:
    print('item no: ', cnt, ' ', color)
    queue.put(color)
    cnt += 1

print('\npopping items from queue:')
cnt = 0
while not queue.empty():
    print('item no: ', cnt, ' ', queue.get())
    cnt += 1