'''
multiprocessing을 사용하기 위한 프로그래밍 지침
https://docs.python.org/ko/3/library/multiprocessing.html#multiprocessing-programming
'''

from multiprocessing import Queue

if __name__ == '__main__':
    items = ['red', 'green', 'blue', 'black']
    q = Queue()

    n = 0
    print("pushing items to queue")
    for item in items:
        q.put(item)
        print(f"item no: {n} {item}")
        n += 1
    
    print("popping items from queue")
    # while not q.empty():
    while True:
        try:
            item = q.get()
            print(f"item no: {n} {item}")
            n -= 1
            if n == 0:
                break
        except:
            continue
        