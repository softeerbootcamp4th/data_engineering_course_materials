import multiprocessing
import time

def push_items(queue, items):
    print("pushing items to queue:")
    # queue에 item put
    for i, item in enumerate(items):
        queue.put((item, i+1))
        print(f"item no: {i+1} {item}")
        time.sleep(0.5)

def pop_items(queue):
    print("\npopping items from queue:")
    # queue가 빌 때까지 pop
    while True:
        try:
            items = queue.get_nowait()
            print(f"item no: {items[1]} {items[0]}")
            time.sleep(0.5)
        except multiprocessing.queues.Empty:
            break

items = ["red", "green", "blue", "black"]

if __name__ == "__main__":
    queue = multiprocessing.Queue()

    # Process for pushing
    push_process = multiprocessing.Process(target=push_items, args=(queue, items))
    # Process for popping
    pop_process = multiprocessing.Process(target=pop_items, args=(queue,))

    # push process 수행
    push_process.start()
    push_process.join()

    # pop process 수행
    pop_process.start()
    pop_process.join()
