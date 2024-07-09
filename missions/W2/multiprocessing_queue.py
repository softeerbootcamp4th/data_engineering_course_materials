from multiprocessing import Process, Queue

def push_data(items: list, q: Queue):
    print("pushing items to queue:")
    for idx, item in enumerate(items):
        q.put(item)
        print(f"item no: {idx + 1} {item}")

def pop_data(q: Queue):
    print("popping items from queue:")
    idx=1
    while not q.empty():
        item=q.get()
        print(f"item no: {idx} {item}")
        idx+=1

if __name__ == "__main__":
    q = Queue()
    itemss = ["red", "green", "blue", "yellow", "black"]

    # create processes
    push_process = Process(target=push_data, args=(itemss, q))
    pop_process = Process(target=pop_data, args=(q, ))

    # push items 
    push_process.start()
    push_process.join()

    # pop items
    pop_process.start()
    pop_process.join()