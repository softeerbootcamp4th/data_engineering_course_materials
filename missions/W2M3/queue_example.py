import multiprocessing
import time

def push_items(queue, items):
    print("pushing items to queue:")
    for i, item in enumerate(items):
        print(f"item no: {i + 1} {item}")
        queue.put(item)
        time.sleep(0.5)

def pop_items(queue):
    print("popping items from queue:")
    i = 0
    while not queue.empty():
        item = queue.get()
        print(f"item no: {i} {item}")
        i += 1
        time.sleep(0.5)

if __name__ == "__main__":
    items = ['red', 'green', 'blue', 'black']
    
    # 큐 생성
    queue = multiprocessing.Queue()
    
    # 프로세스 생성
    # 만들어진 큐를 같이 넘겨줌 -> 여기에 갖다 박아라, 여기서 빼라
    p1 = multiprocessing.Process(target=push_items, args=(queue, items))
    p2 = multiprocessing.Process(target=pop_items, args=(queue,))
    
    # 프로세스 시작
    p1.start()
    p1.join()

    p2.start()
    p2.join()
