from multiprocessing import Queue, Process


"""
Put() function is used to push an item to the queue.
Get() function is used to pop an item from the queue.
"""


def put_items(queue: Queue):
    items = ['red', 'green', 'blue', 'black']
    for idx, item in enumerate(items):
        print(f"item no: {idx+1} {item}")
        queue.put([idx, item])


def get_items(queue: Queue):
    while not queue.empty():
        num, item = queue.get()
        print(f"item no: {num} {item}")


if __name__ == '__main__':
    queue = Queue()
    
    put_process = Process(target=put_items, args=(queue,))
    get_process = Process(target=get_items, args=(queue,))
    
    print("Pushing items to queue")
    put_process.start()
    put_process.join()
    
    print("Popping items from queue")
    get_process.start()
    get_process.join()
    