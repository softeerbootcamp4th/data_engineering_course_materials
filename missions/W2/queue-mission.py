import time
from multiprocessing import Queue


def push(queue: Queue, item: str, N: int):
    queue.put(item)
    print(f'item no: {N} {item}')


def pop(queue: Queue, N: int):
    print(f'item no: {N} {queue.get()}')


if __name__ == '__main__':
    items = [
        'red',
        'green',
        'blue',
        'navy',
    ]

    queue = Queue()
    print('pushing items to queue:')
    for i, item in enumerate(items):
        push(queue, item, i+1)

    # time.sleep(1)

    print('popping items from queue:')
    N = 0
    while not queue.empty():
        pop(queue, N)
        N += 1
