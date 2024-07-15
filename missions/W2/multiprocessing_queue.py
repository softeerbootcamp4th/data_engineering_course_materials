from multiprocessing import Process, Queue
import queue

def push_data(items: list, q: Queue):
    print("pushing items to queue:")
    for idx, item in enumerate(items):
        q.put(item)
        print(f"item no: {idx + 1} {item}")

def pop_data(q: Queue):
    print("popping items from queue:")
    idx=1
    while True:
        try:
            item=q.get_nowait()
            print(f"item no: {idx} {item}")
            idx+=1
        except queue.Empty:
            break

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