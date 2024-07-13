import multiprocessing
import time

def push_items(queue, items):
    print("pushing items to queue:")
    for i, item in enumerate(items):
        print(f"item no: {i+1} {item}")
        queue.put(item)
        time.sleep(0.1) 

def pop_items(queue):
    print("popping items from queue:")
    count = 0
    while not queue.empty():
        item = queue.get()
        print(f"item no: {count} {item}")
        count += 1
        time.sleep(0.1)  

if __name__ == "__main__":
    items = ['red', 'green', 'blue', 'black']
    queue = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=push_items, args=(queue, items))
    p2 = multiprocessing.Process(target=pop_items, args=(queue,))

    p1.start()
    p1.join()  

    p2.start()
    p2.join()  
