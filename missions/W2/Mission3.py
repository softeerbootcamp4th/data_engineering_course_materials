from multiprocessing import Process, Queue

def push_items(queue, items):
    for idx, item in enumerate(items, 1):  
        queue.put(item)
        print(f"item no: {idx} {item}")

def pop_items(queue):
    idx = 0 
    while not queue.empty():
        item = queue.get()
        print(f"item no: {idx} {item}")
        idx += 1

if __name__ == '__main__':
    items = ["red", "green", "blue", "black"]
    queue = Queue()

    push_process = Process(target=push_items, args=(queue, items))
    pop_process = Process(target=pop_items, args=(queue,))

    print("pushing items to queue:")
    push_process.start()
    push_process.join()

    print("popping items from queue:")
    pop_process.start()
    pop_process.join()



