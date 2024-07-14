import time
from multiprocessing import Process, Queue


def push(queue, colors):
    print('pushing items to queue:')
    for i, color in enumerate(colors):
        queue.put(color)
        print(f'item no: {i + 1} {color}')


def pull(queue):
    while not queue.full():
        time.sleep(0.0001)
    print('popping items from queue:')
    i = 0
    while not queue.empty():
        item = queue.get()
        print(f'item no: {i} {item}')
        i += 1
    

if __name__ == '__main__':
    queue = Queue(4)

    worker_push = Process(target=push, args=(queue, ['red', 'green', 'blue', 'black']))
    worker_pull = Process(target=pull, args=(queue, ))

    worker_push.start()
    worker_pull.start()

    worker_push.join()
    worker_pull.join()

    